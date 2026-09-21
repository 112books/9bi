#!/usr/bin/env python3
"""Formularis — recepció dels formularis del web 9 Barris Imatge (M1, stdlib).

App WSGI en Python pur (sense dependencies) compatible amb Passenger
(Phusion/Python), gunicorn/waitress i el servidor de desenvolupament WSGI.

Rep els POST dels formularis del web (contacte, incorpora-te) que fins ara
enviàvem per FormSubmit (formsubmit.co) i els reenvia per correu via SMTP
de Dinahosting (SMTPS 465 o STARTTLS 587), de manera que no depenem de cap
servei de tercers.

Config: config.ini (exemple a config.example.ini). Variables d'entorn:
  FORMULARIS_CONFIG, FORMULARIS_SECRET.

Routes:
  GET  /health                  -> estat del servei
  POST /envia/<formulari>       -> rep els camps i els envia per correu

Seguretat:
  - Honeypot: camp ocult `_honey`; si ve ple, es descarta en silenci.
  - Rate limit per IP (en memòria, finestra de 60 s).
  - CSRF: HMAC del secret + id de dispositiu (cookie), compare_digest.
  - Whitelist de camps per formulari: res del que no esperem s'hi envia.
  - Longitud màxima de camp (2 kB) i de la petició (64 kB).
"""
import configparser
import hmac
import html as htmlmod
import os
import re
import secrets
import smtplib
import ssl as sslmod
import sys
import time
import urllib.parse
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
from wsgiref.simple_server import make_server

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.environ.get(
    "FORMULARIS_CONFIG", os.path.join(MODULE_DIR, "config.ini"))
DEFAULT_LANG = "ca"
SUPPORTED_LANGS = ("ca", "es", "en")

# Formularis coneguts i els seus camps (whitelist). Tot el que no estigui
# en aquesta llista s'ignora.
KNOWN_FORMS = {
    "contacte": ("nom", "email", "assumpte", "entitat", "missatge",
                 "consentiment"),
    "incorpora-te": ("nom_complet", "nom_artistic", "usuari_codeberg",
                     "email", "web", "instagram", "galeries",
                     "consentiment"),
}

MAX_CAMP = 2000        # caràcters per camp
MAX_COS = 64 * 1024    # mida màxima del cos de la petició


# ---------------------------------------------------------------- helpers

def load_config():
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_PATH, encoding="utf-8")
    return cfg


def secret_key(cfg):
    return os.environ.get(
        "FORMULARIS_SECRET", cfg.get("general", "secret", fallback="CHANGE-ME"))


def get_i18n(lang):
    i18n = {}
    base = {}
    for l in (lang, DEFAULT_LANG):
        path = os.path.join(MODULE_DIR, "i18n", "%s.ini" % l)
        if not os.path.exists(path):
            continue
        cur = i18n if l == lang else base
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith(("#", ";")):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    cur[k.strip()] = v.strip()
    return i18n if i18n else base


def pick_lang(environ):
    q = urllib.parse.parse_qs(environ.get("QUERY_STRING", ""))
    l = (q.get("lang") or [""])[0].lower()
    if l in SUPPORTED_LANGS:
        return l
    accept = environ.get("HTTP_ACCEPT_LANGUAGE", "")
    for part in accept.split(","):
        code = part.strip().split(";")[0].lower()
        if code.startswith(SUPPORTED_LANGS):
            return code
    return DEFAULT_LANG


def page_html(lang, title, body):
    return (
        "<!doctype html><html lang=\"%s\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        "<title>%s</title>"
        "<style>body{font-family:system-ui,sans-serif;max-width:38rem;margin:2rem auto;"
        "padding:0 1rem;line-height:1.55}h1{font-size:1.35rem}a{color:#2a6db5}"
        ".msg{padding:.9rem 1rem;border-radius:8px;margin:1.2rem 0;border:1px solid}"
        ".ok{background:#eaf6ea;border-color:#9ccc9c}.err{background:#fdecec}"
        ".err{border-color:#f0b4b4}"
        "table{border-collapse:collapse;margin:1rem 0}td,th{border:1px solid #ddd;"
        "padding:.35rem .6rem;text-align:left;vertical-align:top;font-size:.95rem}"
        "th{background:#f4f4f4}"
        "</style></head><body>%s</body></html>" % (
            htmlmod.escape(lang), htmlmod.escape(title), body))


def respond(environ, start_response, status, body,
            content_type="text/html; charset=utf-8", extra_headers=()):
    body = body.encode("utf-8") if isinstance(body, str) else body
    headers = [("Content-Type", content_type),
               ("Content-Length", str(len(body))),
               ("Cache-Control", "no-store")]
    headers.extend(extra_headers)
    start_response(status, headers)
    return [body]


# ------------------------------------------------------------ rate limit

_rate = {}


def rate_limited(environ, cfg):
    limit = cfg.getint("general", "rate_limit", fallback=20)
    ip = environ.get("REMOTE_ADDR", "?")
    now = time.time()
    arr = _rate.setdefault(ip, [])
    arr = [t for t in arr if now - t < 60]
    _rate[ip] = arr
    if len(arr) >= limit:
        return True
    arr.append(now)
    return False


def hmac_sig(cfg_secret, parts):
    msg = "|".join(str(p) for p in parts).encode("utf-8")
    return hmac.new(cfg_secret.encode("utf-8"), msg, "sha256").hexdigest()


def device_id(environ):
    cookies = {}
    for part in (environ.get("HTTP_COOKIE") or "").split(";"):
        if "=" in part:
            k, v = part.strip().split("=", 1)
            cookies[k] = v
    c = cookies.get("fid")
    if c and len(c) == 64 and all(x in "0123456789abcdef" for x in c):
        return c
    return secrets.token_hex(32)


def csrf_ok(environ, cfg, given):
    sec = secret_key(cfg)
    dev = device_id(environ)
    expect = hmac_sig(sec, ("csrf", dev, environ.get("REMOTE_ADDR", "")))
    return given and hmac.compare_digest(given, expect)


# ----------------------------------------------------------------- smtp

def send_mail(cfg, to_addr, subject, cos, lang):
    """Envia el correu per SMTP (SMTPS 465 o STARTTLS 587). Torna (ok, detall)."""
    host = cfg.get("smtp", "host", fallback="")
    port = cfg.getint("smtp", "port", fallback=465)
    use_ssl = cfg.getboolean("smtp", "ssl", fallback=True)
    user = cfg.get("smtp", "user", fallback="")
    passw = cfg.get("smtp", "password", fallback="")
    from_addr = cfg.get("smtp", "from", fallback=user)
    from_name = cfg.get("smtp", "from_name", fallback="9 Barris Imatge — web")

    if not (user and passw and "@" in user):
        return False, "SMTP sense credencials (usuari/contrasenya buits a config.ini)"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr((from_name, from_addr))
    msg["To"] = formataddr(("", to_addr))
    msg["Message-ID"] = make_msgid(domain=from_addr.split("@")[-1])
    msg.set_content(cos, subtype="plain")

    try:
        if use_ssl:
            ctx = sslmod.create_default_context()
            with smtplib.SMTP_SSL(host, port, context=ctx, timeout=30) as s:
                s.login(user, passw)
                s.send_message(msg)
        else:
            with smtplib.SMTP(host, port, timeout=30) as s:
                s.ehlo()
                if s.has_extn("starttls"):
                    s.starttls()
                    s.ehlo()
                s.login(user, passw)
                s.send_message(msg)
        return True, ""
    except Exception as e:
        return False, "%s: %s" % (type(e).__name__, e)


# ------------------------------------------------------------ app (routes)

def page_form_ok(lang, i18n, camps):
    taula = "".join(
        "<tr><th>%s</th><td>%s</td></tr>"
        % (htmlmod.escape(k), htmlmod.escape(str(v)))
        for k, v in camps.items())
    cos = ("<h1>%s</h1><p>%s</p>"
           "<table>%s</table>"
           "<p><a href=\"/\">%s</a></p>"
           % (htmlmod.escape(i18n.get("title_ok", "Rebut")),
              htmlmod.escape(i18n.get("msg_ok", "")),
              taula,
              htmlmod.escape(i18n.get("link_back", "Torna a l'inici"))))
    return page_html(lang, i18n.get("title_ok", ""), cos)


def form_post(environ, start_response, form):
    cfg = load_config()
    lang = pick_lang(environ)
    i18n = get_i18n(lang)

    if form not in KNOWN_FORMS:
        return respond(environ, start_response, "404 Not Found",
                       page_html(lang, i18n.get("title_error", ""),
                                 "<p>%s</p>" % htmlmod.escape(
                                     i18n.get("msg_form_unknown", ""))))

    if rate_limited(environ, cfg):
        return respond(environ, start_response, "429 Too Many Requests",
                       page_html(lang, i18n.get("title_error", ""),
                                 "<p>%s</p>" % htmlmod.escape(
                                     i18n.get("msg_rate_limited", ""))))

    length = int(environ.get("CONTENT_LENGTH") or 0)
    raw = environ["wsgi.input"].read(length) if length else b""
    if len(raw) > MAX_COS:
        return respond(environ, start_response, "413 Payload Too Large",
                       page_html(lang, i18n.get("title_error", ""),
                                 "<p>%s</p>" % htmlmod.escape(
                                     i18n.get("msg_too_large", ""))))
    try:
        fields = urllib.parse.parse_qs(raw.decode("utf-8", "replace"))
        fields = {k: v[0] for k, v in fields.items()}
    except Exception:
        fields = {}

    # Honeypot: si el camp ocult ve ple, descartem en silenci
    if fields.get("_honey"):
        return respond(environ, start_response,
                       "200 OK",
                       page_html(lang, i18n.get("title_ok", ""),
                                 "<p>%s</p>" % htmlmod.escape(
                                     i18n.get("msg_ok", ""))))

    # CSRF
    if not csrf_ok(environ, cfg, fields.get("_csrf", "")):
        return respond(environ, start_response, "403 Forbidden",
                       page_html(lang, i18n.get("title_error", ""),
                                 "<p>%s</p>" % htmlmod.escape(
                                     i18n.get("msg_csrf", ""))))

    # Whitelist + neteja de camps
    camps = {}
    allow = KNOWN_FORMS[form]
    for k, v in fields.items():
        if k not in allow:
            continue
        v = v.strip()[:MAX_CAMP]
        if v:
            camps[k] = v

    if not camps:
        return respond(environ, start_response, "400 Bad Request",
                       page_html(lang, i18n.get("title_error", ""),
                                 "<p>%s</p>" % htmlmod.escape(
                                     i18n.get("msg_empty", ""))))

    dest = cfg.get("destinataris", form,
                   fallback=cfg.get("general", "destinatari", fallback=""))
    if not dest or "@" not in dest:
        dest = "info@9barrisimatge.org"

    assumpte_map = {
        "contacte": i18n.get("subject_contacte", "Missatge des del web 9 Barris Imatge"),
        "incorpora-te": i18n.get("subject_incorpora", "Alta de membre — 9 Barris Imatge"),
    }
    subject = assumpte_map.get(form, "")
    if form == "contacte" and camps.get("assumpte"):
        subject = "%s — %s" % (camps["assumpte"], subject)

    taula = "\n".join("%s: %s" % (k, v) for k, v in camps.items())
    ok, detall = send_mail(cfg, dest, subject, taula, lang)
    if ok:
        return respond(environ, start_response, "200 OK",
                       page_html(lang, i18n.get("title_ok", ""),
                                 "<p>%s</p>" % htmlmod.escape(
                                     i18n.get("msg_ok", ""))))
    return respond(environ, start_response, "500 Internal Server Error",
                   page_html(lang, i18n.get("title_error", ""),
                             "<p>%s <code>%s</code></p>"
                             % (htmlmod.escape(i18n.get("msg_error", "")),
                                htmlmod.escape(detall))))


def health(environ, start_response):
    return respond(environ, start_response, "200 OK", "ok",
                   content_type="text/plain; charset=utf-8")


def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET")
    if path == "/health":
        return health(environ, start_response)
    if path.startswith("/envia/") and method == "POST":
        form = path[len("/envia/"):].strip("/")
        return form_post(environ, start_response, form)
    if path in ("/", ""):
        body = ("<h1>Formularis 9 Barris Imatge</h1>"
                "<p>Servei de recepció dels formularis del web. "
                "<code>POST /envia/&lt;formulari&gt;</code></p>")
        return respond(environ, start_response,
                       "200 OK", page_html("ca", "Formularis", body))
    return respond(environ, start_response, "404 Not Found",
                   page_html("ca", "404", "<p>404</p>"))


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8021
    server = make_server("127.0.0.1", port, application)
    print("Formularis a http://127.0.0.1:%d" % port)
    server.serve_forever()

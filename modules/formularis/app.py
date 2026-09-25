#!/usr/bin/env python3
"""Formularis — recepció dels formularis del web 9 Barris Imatge (M1, stdlib).

App WSGI en Python pur (sense dependencies) compatible amb Passenger
(Phusion/Python), gunicorn/waitress i el servidor de desenvolupament WSGI.

Rep els POST dels formularis del web (contacte, incorpora-te) i els reenvia per
correu via SMTP del hosting (SMTPS 465 o STARTTLS 587), de manera que no
depeneixem de cap servei de tercers com FormSubmit.

Es desplega a https://formularis.linuxbcn.com (subdomini del hosting
DINAHOSTING-2248 → linuxbcn.com; el domini 9barrisimatge.org és només correu
i el web és a GitHub Pages).

Config: config.ini (exemple a config.example.ini). Variable d'entorn:
  FORMULARIS_CONFIG.

Routes:
  GET  /health                  -> estat del servei
  POST /envia/<formulari>       -> rep els camps i els envia per correu

Seguretat:
  - Origen: el POST ha d'arribar des d'un dels orígens de la llista
    [general] allowed_origins (capçalera Origin; si no hi és, el Referer).
    Un formulari estàtic de Hugo no pot signar capçaleres, de manera que
    l'origen declarat és la dada de què es pot servir, i és suficient per
    rebutjar enviaments des de pàgines que no són nostres.
  - Honeypot: camp ocult `_honey`; si ve ple, es descarta en silenci.
  - Rate limit per IP (en memòria, finestra de 60 s).
  - Whitelist de camps per formulari: res del que no esperem s'hi envia.
  - Els camps es netegen de caràcters de control; el Reply-To només s'afegeix
    si l'adreça és vàlida (evita injecció de capçaleres).
  - Longitud màxima de camp (2 kB) i de la petició (64 kB).
  - Els errors de SMTP no s'ensenyen al navegador: van al registre del servidor.
"""
import configparser
import html as htmlmod
import os
import re
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


# ------------------------------------------------- origen (anti-CSRF/open-redirect)

DEFAULT_PORTS = {"http": "80", "https": "443"}


def origin_of(environ):
    """Origen declarat del POST, normalitzat a esquema://host[:port] sense port per defecte."""
    val = (environ.get("HTTP_ORIGIN") or "").strip()
    if not val or val == "null":
        ref = (environ.get("HTTP_REFERER") or "").strip()
        if ref:
            val = ref
    if not val or val == "null":
        return ""
    try:
        parts = urllib.parse.urlsplit(val)
    except ValueError:
        return ""
    scheme = parts.scheme.lower()
    host = parts.netloc.lower()
    if not scheme or not host:
        return ""
    if ":" in host and host.rsplit(":", 1)[1] == DEFAULT_PORTS.get(scheme):
        host = host.rsplit(":", 1)[0]
    return "%s://%s" % (scheme, host)


def allowed_origins(cfg):
    raw = cfg.get("general", "allowed_origins", fallback="")
    out = set()
    for item in raw.replace(";", ",").split(","):
        item = item.strip().rstrip("/").lower()
        if item.startswith("http://") or item.startswith("https://"):
            out.add(item)
    return out


def origin_ok(environ, cfg):
    allowed = allowed_origins(cfg)
    got = origin_of(environ)
    return bool(allowed) and bool(got) and got in allowed


# ------------------------------------------------------- neteja de valors

_CONTROL_RE = re.compile(r"[\x00-\x08\x0a-\x1f\x7f]")
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s.]+(\.[^@\s.]+)+$")


def clean_value(v, limit=MAX_CAMP):
    """Treu caràcters de control (evita injecció de capçaleres) i retalla."""
    return _CONTROL_RE.sub(" ", v).strip()[:limit]


def valid_email(v):
    return bool(v) and len(v) <= 254 and bool(_EMAIL_RE.match(v))


# ----------------------------------------------------------------- smtp

def smtp_ready(cfg):
    host = cfg.get("smtp", "host", fallback="").strip()
    user = cfg.get("smtp", "user", fallback="").strip()
    passw = cfg.get("smtp", "password", fallback="")
    if not passw:
        passw = os.environ.get("FORMULARIS_SMTP_PASSWORD", "")
    return bool(host) and "@" in user and bool(passw)


def send_mail(cfg, to_addr, subject, cos, reply_to=None):
    """Envia el correu per SMTP (SMTPS 465 o STARTTLS 587). Torna (ok, detall)."""
    host = cfg.get("smtp", "host", fallback="")
    port = cfg.getint("smtp", "port", fallback=465)
    use_ssl = cfg.getboolean("smtp", "ssl", fallback=True)
    user = cfg.get("smtp", "user", fallback="")
    passw = cfg.get("smtp", "password", fallback="")
    if not passw:
        passw = os.environ.get("FORMULARIS_SMTP_PASSWORD", "")
    from_addr = cfg.get("smtp", "from", fallback=user)
    from_name = cfg.get("smtp", "from_name", fallback="9 Barris Imatge — web")

    if not (user and passw and "@" in user):
        return False, "SMTP sense credencials (usuari/contrasenya)"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr((from_name, from_addr))
    msg["To"] = to_addr
    msg["Message-ID"] = make_msgid(domain=from_addr.split("@")[-1])
    if reply_to and valid_email(reply_to):
        msg["Reply-To"] = reply_to
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

    # Origen: només s'accepten POST des dels orígens configurats
    if not origin_ok(environ, cfg):
        return respond(environ, start_response, "403 Forbidden",
                       page_html(lang, i18n.get("title_error", ""),
                                 "<p>%s</p>" % htmlmod.escape(
                                     i18n.get("msg_origin", ""))))

    # Whitelist + neteja de camps
    camps = {}
    allow = KNOWN_FORMS[form]
    for k, v in fields.items():
        if k not in allow:
            continue
        v = clean_value(v)
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

    site_url = cfg.get("general", "site_url",
                       fallback="https://9barrisimatge.org/").rstrip("/")
    taula = "\n".join("%s: %s" % (k, v) for k, v in camps.items())
    cos = "%s\n\n--\n%s\n%s" % (
        taula,
        i18n.get("mail_footer", "Enviat des del formulari del web 9 Barris Imatge"),
        site_url)

    if not smtp_ready(cfg):
        print("formularis: config.ini sense credencials SMTP", file=sys.stderr)
        return respond(environ, start_response, "503 Service Unavailable",
                       page_html(lang, i18n.get("title_error", ""),
                                 "<p>%s</p>" % htmlmod.escape(
                                     i18n.get("msg_unavailable", ""))))

    ok, detall = send_mail(cfg, dest, subject, cos,
                           camps.get("email") if valid_email(camps.get("email", "")) else None)
    if ok:
        return respond(environ, start_response, "200 OK",
                       page_html(lang, i18n.get("title_ok", ""),
                                 "<p>%s</p>" % htmlmod.escape(
                                     i18n.get("msg_ok", ""))))
    print("formularis: error en enviar (%s): %s" % (form, detall), file=sys.stderr)
    return respond(environ, start_response, "500 Internal Server Error",
                   page_html(lang, i18n.get("title_error", ""),
                             "<p>%s</p>" % htmlmod.escape(
                                 i18n.get("msg_error", ""))))


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

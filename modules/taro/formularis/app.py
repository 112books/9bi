#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Col·lectiu 9 Barris Imatge
# Llicència i avisos (fitxer LICENSE a l'arrel del repositori)
"""Formularis — rep els formularis d'un web i els envia per correu (stdlib).

App WSGI en Python pur (sense dependencies) compatible amb Passenger
(Phusion/Python), gunicorn/waitress i el servidor de desenvolupament WSGI.

Rep els POST dels formularis del web (els que defineixis a la configuració:
per defecte «contacte» i «incorpora-te») i els reenvia per correu via SMTP
(SMTPS 465 o STARTTLS 587), de manera que no depenem de cap servei de tercers
com FormSubmit.

Es desplega en un subdomini del teu propi hosting, darrere d'un proxy que
passa les peticions al procés Python; el web pot ser estàtic, a GitHub Pages
o a qualsevol altre lloc.

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
# Formularis i camps acceptats. Per defecte, aquests dos; per tenir-ne
# d'altres, defineix-los a la configuració (vegeu forms_config).
KNOWN_FORMS = {
    "contacte": ("nom", "email", "assumpte", "entitat", "missatge",
                 "consentiment"),
    "incorpora-te": ("nom_complet", "nom_artistic", "usuari_github",
                     "email", "web", "instagram", "galeries",
                     "consentiment"),
}

MAX_CAMP = 2000        # caràcters per camp
MAX_COS = 64 * 1024    # mida màxima del cos de la petició


# ---------------------------------------------------------------- helpers

def load_config():
    # interpolation=None: sense això configparser tracta '%' com a sintaxi i
    # peta amb contrasenyes que en portin (aquestes acaben en %). Els secrets
    # tenen valors per defecte explícits, no per interpolació.
    cfg = configparser.ConfigParser(interpolation=None)
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

def smtp_password(cfg):
    """Contrasenya SMTP, del config o de l'entorn. Preferim l'entorn.

    Nota: es llegeix amb el valor 'crud' de configparser i cap tipus d'escape,
    perquè una contrasenya pot contenir '%' (que és el caràcter de substitufacció
    de ConfigParser i, amb interpolació activada, provoca InterpolationSyntaxError
    i un 500 al navegador). Amb interpolation=None a load_config() això no
    passa, però el valor es returned tal qual, sense processar-lo.
    """
    v = cfg.get("smtp", "password", fallback="", raw=True)
    if not v:
        v = os.environ.get("FORMULARIS_SMTP_PASSWORD", "")
    return v


def smtp_ready(cfg):
    host = cfg.get("smtp", "host", fallback="").strip()
    user = cfg.get("smtp", "user", fallback="").strip()
    passw = smtp_password(cfg)
    return bool(host) and "@" in user and bool(passw)


def send_mail(cfg, to_addr, subject, cos, reply_to=None, html=None):
    """Envia el correu per SMTP (SMTPS 465 o STARTTLS 587). Torna (ok, detall).

    Si hi ha 'html', el correu s'envia multipart/alternative: el text pla és
    el que mostren els clients que no tenen HTML activat, i l'HTML el que
    permet fer el peu legal en lletra petita amb les etiquetes en negreta.
    """
    host = cfg.get("smtp", "host", fallback="")
    port = cfg.getint("smtp", "port", fallback=465)
    use_ssl = cfg.getboolean("smtp", "ssl", fallback=True)
    user = cfg.get("smtp", "user", fallback="")
    passw = smtp_password(cfg)
    from_addr = cfg.get("smtp", "from", fallback=user)
    from_name = cfg.get("smtp", "from_name", fallback="Formulari del web")

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
    if html:
        msg.add_alternative(html, subtype="html")

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


# ------------------------------------------------------- bloc legal (RGPD)

# Articles 13 i 14 del RGPD. El text va lligat amb la politica de privacitat
# publicada (content/privacitat.md). Always in Catalan because the recipient of
# these emails is always the collective itself, not the visitor.
#
# Cada apartat es una parella (etiqueta, text). Aquesta es l'unica font: el
# correu en text pla i el correu en HTML es construeixen tots dos a partir
# d'aqui, de manera que no es poden desincronitzar.
LEGAL_HEADING = "Informació sobre el tractament de dades (RGPD i LOPDGDD)"

LEGAL_FINALITAT = {
    "contacte": ("atendre i respondre la teva consulta, i les gestions "
                 "internes que se'n derivin."),
    "incorpora-te": ("gestionar el teu perfil de membre i l'accés "
                     "al gestor de continguts del web."),
}


def form_finalitat(cfg, form):
    """Finalitat del tractament, de [formularis.<nom>] finalitat a la config."""
    sec = "formularis." + form
    if cfg.has_section(sec):
        v = cfg.get(sec, "finalitat", fallback="").strip()
        if v:
            return v
    return LEGAL_FINALITAT.get(form, "")


def url_privacitat(cfg, site_url):
    """URL de la política de privacitat: la que posi qui instal·la el mòdul,
    o la del web amb /privacitat/ al final."""
    u = cfg.get("general", "url_privacitat", fallback="").strip()
    return u or (site_url.rstrip("/") + "/privacitat/")


def contacte_public(cfg, i18n, key):
    """Text que parla d'on escriure o des d'on s'envia, amb les dades de qui
    instal·la el mòdul: la traducció porta un %s i aquí hi va el correu o
    el domini. Sense dades a la configuració, el text es queda curt."""
    text = i18n.get(key, "")
    if "%s" not in text:
        return text
    correu = cfg.get("legal", "correu", fallback="").strip()
    domini = urllib.parse.urlsplit(
        cfg.get("general", "site_url", fallback="").strip()).netloc
    return text % (correu or domini or "la nostra adreça")


def legal_sections(form, cfg):
    """Apartats del peu legal com a llista de (etiqueta, text).

    Les dades del responsable surten de la secció [legal] de la configuració:
    qui s'envia el correu ha de poder dir qui és el responsable del tractament.
    Si en falten, es para el servei enlloc d'enviar un correu que ho digui malament.
    """
    entitat = cfg.get("legal", "entitat", fallback="")
    adreca = cfg.get("legal", "adreca", fallback="")
    correu = cfg.get("legal", "correu", fallback="")
    if not (entitat and correu):
        raise SystemExit(
            "formularis: cal omplir [legal] entitat i [legal] correu "
            "(config.ini) — són les dades del responsable del tractament")
    destinataris = cfg.get("legal", "corresponsalia", fallback="")
    aepd = cfg.get("legal", "aepd", fallback="Agència Espanyola de Protecció de Dades (aepd.es)")
    return [
        ("Responsable del tractament", entitat),
        ("Adreça", adreca),
        ("Correu de contacte", correu),
        ("Dades tractades", "les que has enviat en aquest formulari."),
        ("Finalitat", form_finalitat(cfg, form)),
        ("Base legal", "el teu consentiment (article 6.1.a del RGPD), atorgat en "
                       "marcar la casella de consentiment abans d'enviar el "
                       "formulari. El pots retirar en qualsevol moment "
                       "escrivint-nos, sense que això afecti la licitud del "
                       "tractament previ."),
        ("Destinataris", (destinataris or "el servei de formularis del web")
                         + " i el proveïdor de correu electrònic, on "
                           "s'emmagatzemen els missatges. No es cedeixen dades a "
                           "tercers aliens."),
        ("Conservacio", "es conserven mentre es tramita la consulta i, després, "
                        "durant el temps necessari per complir les obligacions "
                        "legals aplicables. Quan no calguin, se suprimeixen de "
                        "manera segura."),
        ("Drets", "pots exercir els drets d'accés, rectificació, supressió, "
                  "oposició, limitació i portabilitat escrivint a "
                  + correu + ", indicant el dret que vols exercir i "
                  "adjuntant un document que acrediti la teva identitat. També "
                  "pots presentar una reclamació davant l'" + aepd + "."),
        ("Camps opcionals", "els camps marcats com a opcionals no són "
                            "necessaris: si no els emplenes, no els "
                            "tractarem."),
        ("Decisions automatitzades", "no hi ha cap decisió automatitzada ni "
                                     "perfilació que pugui produir efectes "
                                     "jurídics sobre les teves dades."),
    ]


def legal_block(form, site_url, cfg):
    """Bloc d'informació GDPR en text pla, per al correu que no llegeix HTML."""
    parts = [LEGAL_HEADING]
    parts += ["%s: %s" % (et, txt) for et, txt in legal_sections(form, cfg) if txt]
    parts.append("Més informació a la política de privacitat: %s"
                 % url_privacitat(cfg, site_url))
    return "\n".join(parts)




# ------------------------------------------------------ correu en HTML

# El peu legal ha de quedar ben separat del missatge i el més petit possible:
# és una obligació legal, no part del contingut que ha llegit qui escriu.
# Els estils van a l'etiqueta style (i no a un <style> del capçal) perquè
# molts clients de correu netegen el capçal i deixarien el correu sense format.
MAIL_HTML = """<!DOCTYPE html>
<html lang="ca"><head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#ffffff;">
<div style="font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#222;
            line-height:1.5;">
__CAMPOS__
</div>
<hr style="border:none;border-top:1px solid #d5d5d5;margin:30px 0 14px 0;">
<div style="font-family:Helvetica,Arial,sans-serif;font-size:11px;color:#666;
            line-height:1.5;">
<p style="margin:0 0 10px 0;"><b style="color:#333;">__HEADING__</b></p>
__LEGAL__
<p style="margin:10px 0 0 0;">Més informació a la política de privacitat:<br>
<a href="__URL__" style="color:#666;">__URL__</a></p>
</div>
</body></html>"""


def mail_html(camps, form, site_url, cfg):
    """Cos del correu en HTML: missatge llegible + peu legal a 11 px."""
    esc = htmlmod.escape
    files = "".join(
        '<p style="margin:0 0 4px 0;"><b>%s:</b> %s</p>'
        % (esc(str(k)), esc(str(v)).replace("\n", "<br>"))
        for k, v in camps.items())
    legal = "".join(
        '<p style="margin:0 0 6px 0;"><b style="color:#333;">%s:</b> %s</p>'
        % (esc(et), esc(txt))
        for et, txt in legal_sections(form, cfg) if txt)
    return (MAIL_HTML
            .replace("__CAMPOS__", files)
            .replace("__LEGAL__", legal)
            .replace("__HEADING__", esc(LEGAL_HEADING))
            .replace("__URL__", esc(url_privacitat(cfg, site_url))))


# ------------------------------------------------------------ app (routes)

def forms_config(cfg):
    """Formularis i camps acceptats, de la configuració.

    Cada secció [formularis.<nom>] pot portar:
        camps           = llista de camps acceptats, separada per comes
        assumpte        = text fix del correu
        prefix_assumpte = si | no  (afegeix-hi el valor del camp «assumpte»)
        finalitat       = per què es tracten les dades (RGPD)
    Sense cap secció, es queden els dos formularis de per defecte."""
    out = {}
    for sec in cfg.sections():
        if not sec.startswith("formularis."):
            continue
        nom = sec.split(".", 1)[1].strip()
        camps = [c.strip() for c in
                 cfg.get(sec, "camps", fallback="").split(",") if c.strip()]
        if nom and camps:
            out[nom] = camps
    return out or dict(KNOWN_FORMS)


def form_subject(cfg, form, i18n, camps):
    """Assumpte del correu: el de la configuració del formulari, o el del
    diccionari de traduccions (subject_<nom>)."""
    sec = "formularis." + form
    fix = cfg.get(sec, "assumpte", fallback="").strip() if cfg.has_section(sec) else ""
    if not fix:
        fix = i18n.get("subject_" + form, "").strip()
    if (cfg.get(sec, "prefix_assumpte", fallback="no")
            if cfg.has_section(sec) else "no") == "si" and camps.get("assumpte"):
        return "%s — %s" % (camps["assumpte"], fix)
    return fix


def page_ok(lang, i18n, form="", cfg=None):
    """Pàgina de confirmació d'un enviament correcte.

    Torna a la web configurada a [general] site_url: l'arrel del servei de
    formularis és una pàgina sense utilitat per a qui escriu.
    """
    site_url = (cfg.get("general", "site_url", fallback="").strip() if cfg
                else "")
    enllaç = ('<p><a href="%s">%s</a></p>' % (htmlmod.escape(site_url, quote=True),
                                             htmlmod.escape(i18n.get("link_back", "Torna a l'inici")))
              if site_url else "")
    return page_html(
        lang, i18n.get("title_ok", ""),
        "<p>%s</p>%s" % (htmlmod.escape(i18n.get("msg_ok", "")), enllaç))


def form_post(environ, start_response, form):
    cfg = load_config()
    lang = pick_lang(environ)
    i18n = get_i18n(lang)

    forms = forms_config(cfg)
    if form not in forms:
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
        return respond(environ, start_response, "200 OK", page_ok(lang, i18n, form, cfg))

    # Origen: només s'accepten POST des dels orígens configurats
    if not origin_ok(environ, cfg):
        return respond(environ, start_response, "403 Forbidden",
                       page_html(lang, i18n.get("title_error", ""),
                                 "<p>%s</p>" % htmlmod.escape(
                                     contacte_public(cfg, i18n, "msg_origin"))))

    # Whitelist + neteja de camps
    camps = {}
    allow = forms[form]
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

    # Consentiment RGPD: la casella és obligatòria també al servidor, no només
    # al navegador (un POST directe sense la casella no s'ha d'enviar).
    if "consentiment" in allow and not camps.get("consentiment"):
        return respond(environ, start_response, "400 Bad Request",
                       page_html(lang, i18n.get("title_error", ""),
                                 "<p>%s</p>" % htmlmod.escape(
                                     i18n.get("msg_consent", ""))))

    dest = cfg.get("destinataris", form,
                   fallback=cfg.get("general", "destinatari", fallback=""))
    if not dest or "@" not in dest:
        raise SystemExit(
            "formularis: no sé a qui enviar el formulari %r — posa "
            "[destinataris] %s o [general] destinatari (config.ini)"
            % (form, form))

    subject = form_subject(cfg, form, i18n, camps)
    site_url = cfg.get("general", "site_url", fallback="").strip().rstrip("/")
    taula = "\n".join("%s: %s" % (k, v) for k, v in camps.items())
    # Separació ampla abans del peu legal: en text pla, línia de guions
    # emmarcada i línies en blanc; en HTML, un fil i marge de 30 px.
    sep = "\n\n" + "-" * 60 + "\n\n\n"
    peu_middle = (i18n.get(
        "mail_footer", "Enviat des del formulari del web")
        + "\n" + site_url)
    cos = taula + sep + peu_middle + sep + legal_block(form, site_url, cfg)

    if not smtp_ready(cfg):
        print("formularis: config.ini sense credencials SMTP", file=sys.stderr)
        return respond(environ, start_response, "503 Service Unavailable",
                       page_html(lang, i18n.get("title_error", ""),
                                 "<p>%s</p>" % htmlmod.escape(
                                     contacte_public(cfg, i18n, "msg_unavailable"))))

    ok, detall = send_mail(cfg, dest, subject, cos,
                           camps.get("email") if valid_email(camps.get("email", "")) else None,
                           html=mail_html(camps, form, site_url, cfg))
    if ok:
        return respond(environ, start_response, "200 OK", page_ok(lang, i18n, form, cfg))
    print("formularis: error en enviar (%s): %s" % (form, detall), file=sys.stderr)
    return respond(environ, start_response, "500 Internal Server Error",
                   page_html(lang, i18n.get("title_error", ""),
                             "<p>%s</p>" % htmlmod.escape(
                                 contacte_public(cfg, i18n, "msg_error"))))


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
        cfg = load_config()
        nom = cfg.get("general", "app_name", fallback="") or "Formularis"
        body = ("<h1>%s</h1>" % htmlmod.escape(nom) +
                "<p>Servei de recepció dels formularis del web. "
                "<code>POST /envia/&lt;formulari&gt;</code></p>")
        return respond(environ, start_response,
                       "200 OK", page_html("ca", nom, body))
    return respond(environ, start_response, "404 Not Found",
                   page_html("ca", "404", "<p>404</p>"))


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8021
    server = make_server("127.0.0.1", port, application)
    print("Formularis a http://127.0.0.1:%d" % port)
    server.serve_forever()

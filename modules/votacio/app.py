#!/usr/bin/env python3
"""Votacio - vot public d'un concurs fotografic. M1 (stdlib nomes).

App WSGI en Python pur (sense dependencies) compatible amb Passenger,
gunicorn/waitress i el servidor de desenvolupament WSGI.

Config: config.ini (exemple a config.example.ini). Variables d'entorn:
  VOTACIO_CONFIG (ruta), VOTACIO_SECRET, VOTACIO_ADMIN.

Routes public/votant:
  GET  /v/<token>        -> formulari de vot d'una edicio
  POST /v/<token>        -> envia el vot
Routes admin:
  GET/POST /admin/...    -> login, estat, tancament, export
"""
import configparser
import csv
import hashlib
import hmac
import html
import io
import json
import math
import os
import re
import secrets
import sqlite3
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from functools import wraps
from wsgiref.simple_server import make_server

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.environ.get(
    "VOTACIO_CONFIG", os.path.join(MODULE_DIR, "config.ini"))
DEFAULT_LANG = "ca"
SUPPORTED_LANGS = ("ca", "es", "en")


# ---------------------------------------------------------------- helpers

def load_config():
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_PATH, encoding="utf-8")
    return cfg


def secret_key(cfg):
    s = os.environ.get("VOTACIO_SECRET") or cfg.get("general", "secret", fallback="")
    if not s or s in ("CHANGE-ME", "CANVIA-ME", "CANVIA-ME-TOKEN"):
        raise SystemExit("votacio: cal configurar general.secret (config.ini o VOTACIO_SECRET)")
    return s


def admin_key(cfg):
    s = os.environ.get("VOTACIO_ADMIN") or cfg.get("general", "admin_secret", fallback="")
    if not s or s in ("CHANGE-ME", "CANVIA-ME", "CANVIA-ME-ADMIN"):
        raise SystemExit("votacio: cal configurar general.admin_secret (config.ini o VOTACIO_ADMIN)")
    return s


def db_path(cfg):
    p = cfg.get("db", "path", fallback="data.db")
    if not os.path.isabs(p):
        p = os.path.join(MODULE_DIR, p)
    return p


def connect(cfg):
    conn = sqlite3.connect(db_path(cfg), timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    if conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='edicions'"
    ).fetchone() is None:
        inietit(conn)
    else:
        schema = os.path.join(MODULE_DIR, "schema.sql")
        with open(schema, encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()
    return conn


def inietit(conn):
    """Crea l'esquema si cal i carrega l'edicio/obres de la config a la BD."""
    schema = os.path.join(MODULE_DIR, "schema.sql")
    with open(schema, encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    cfg = load_config()
    e = cfg["edicio"]
    token = e.get("secret_token", "")
    cur = conn.execute("SELECT id FROM edicions WHERE secret_token=?", (token,))
    row = cur.fetchone()
    if row is None:
        cur = conn.execute(
            "INSERT INTO edicions (nom,data_inici,data_fi,secret_token,mode_geo,lat,lon,radi,collect_data,vot_limit,activa)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (e.get("nom", ""), e.get("data_inici", ""), e.get("data_fi", ""),
             token, e.get("mode_geo", "off"),
             try_float(e.get("lat")), try_float(e.get("lon")),
             try_int(e.get("radi")), e.get("collect_data", "none"),
             try_int(e.get("vot_limit", "1")), try_int(e.get("activa", "0"))))
        ed_id = cur.lastrowid
        conn.commit()
    else:
        ed_id = row["id"]
    if cfg.has_section("obres"):
        cur.execute("SELECT COUNT(*) AS n FROM obres WHERE edicio_id=?", (ed_id,))
        if cur.fetchone()["n"] == 0:
            for line in cfg.items("obres"):
                numero = try_int(line[0])
                if not numero:
                    continue
                parts = [p.strip() for p in line[1].split("|")]
                titol = parts[0] if len(parts) > 0 else ""
                autor = parts[1] if len(parts) > 1 else ""
                cat = parts[2] if len(parts) > 2 else ""
                cur.execute(
                    "INSERT INTO obres (edicio_id,numero,titol,autor,categoria) VALUES (?,?,?,?,?)",
                    (ed_id, numero, titol, autor, cat))
            conn.commit()


def try_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def try_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def get_i18n(lang):
    base = {}
    for path in (os.path.join(MODULE_DIR, "i18n", f"{lang}.ini"),
                 os.path.join(MODULE_DIR, "i18n", f"{DEFAULT_LANG}.ini")):
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith(("#", ";", "[")):
                        continue
                    if "=" in line:
                        k, v = line.split("=", 1)
                        base[k.strip()] = v.strip()
    return base


def pick_lang(environ):
    q = urllib.parse.parse_qs(environ.get("QUERY_STRING", ""))
    if q.get("lang"):
        l = q["lang"][0].lower()
        if l in SUPPORTED_LANGS:
            return l
    accept = environ.get("HTTP_ACCEPT_LANGUAGE", "")
    for part in accept.split(","):
        code = part.strip().split(";")[0].lower()
        if code.startswith(("ca", "es", "en")):
            return code.split("-")[0]
    return DEFAULT_LANG


def page_html(title, body, lang):
    return ("<!doctype html><html lang=\"%s\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<title>%s</title>"
            "<style>body{font-family:system-ui,sans-serif;max-width:40rem;margin:2rem auto;padding:0 1rem;line-height:1.5}"
            "h1{font-size:1.4rem}select{font-size:1.1rem;padding:.4rem}button{font-size:1.05rem;padding:.5rem 1.2rem;cursor:pointer}"
            ".msg{padding:.8rem;border-radius:6px;margin:1rem 0}.ok{background:#e6f4e6}.err{background:#fdecec}"
            "a{color:#2a6db5}"
            ".note{color:#555;background:#f3f6fa;border-left:4px solid #2a6db5;padding:.6rem .8rem;border-radius:4px;font-size:.95rem}"
            ".conditions{border:1px solid #d8d5d0;border-radius:8px;padding:1rem 1.2rem;margin-bottom:1.2rem}"
            ".conditions h2{font-size:1.1rem;margin:.2rem 0 .6rem}"
            ".conditions ul{margin:.2rem 0;padding-left:1.2rem}"
            "</style></head><body>%s</body></html>" % (
                html.escape(lang), html.escape(title), body))


def respond(environ, start_response, status, body, content_type="text/html; charset=utf-8",
            extra_headers=(), content_bytes=None):
    if content_bytes is None:
        content_bytes = body.encode("utf-8") if isinstance(body, str) else body
    headers = [("Content-Type", content_type),
               ("Content-Length", str(len(content_bytes))),
               ("Cache-Control", "no-store")]
    headers.extend(extra_headers)
    start_response(status, headers)
    return [content_bytes]


def hmac_sig(secret, parts):
    msg = "|".join(str(p) for p in parts).encode("utf-8")
    return hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()


def csrf_token(secret, device_id):
    return hmac_sig(secret, ("csrf", device_id))


def device_hash(secret, device_id):
    return hmac_sig(secret, ("device", device_id))


def haversine_m(lat1, lon1, lat2, lon2):
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def parse_iso_local(s):
    if not s:
        return None
    return datetime.fromisoformat(s)


def edition_open(cfg, row):
    if not row or not row["activa"] or row["tancada"]:
        return False
    now = datetime.now().replace(tzinfo=None)
    ini = parse_iso_local(row["data_inici"])
    fi = parse_iso_local(row["data_fi"])
    if ini and now < ini:
        return False
    if fi and now > fi:
        return False
    return True


# ------------------------------------------------------------- rate limit

_rate = {}


def rate_limited(environ, cfg, limit=None, bucket=""):
    if limit is None:
        limit = cfg.getint("general", "rate_limit", fallback=40)
    ip = bucket + environ.get("REMOTE_ADDR", "?")
    now = time.time()
    arr = _rate.setdefault(ip, [])
    arr = [t for t in arr if now - t < 60]
    _rate[ip] = arr
    if len(arr) >= limit:
        return True
    arr.append(now)
    return False


# ---------------------------------------------------------------- body

MAX_BODY = 64 * 1024


def read_body(environ):
    """Llegeix el cos de la petició amb un cap de mida (None = massa gran)."""
    try:
        n = int(environ.get("CONTENT_LENGTH", 0) or 0)
    except ValueError:
        n = 0
    if n <= 0:
        return b""
    if n > MAX_BODY:
        return None
    return environ["wsgi.input"].read(n)


# ---------------------------------------------------------------- app ui

def get_edition_and_works(conn, token):
    row = conn.execute(
        "SELECT id,nom,secret_token,mode_geo,lat,lon,radi,vot_limit,activa,tancada,data_inici,data_fi"
        " FROM edicions WHERE secret_token=?", (token,)).fetchone()
    if row is None:
        return None, None
    works = conn.execute(
        "SELECT id,numero,titol,autor FROM obres WHERE edicio_id=? ORDER BY numero",
        (row["id"],)).fetchall()
    return row, works


def h_radix(token):
    return html.escape(token)


def app_base(environ):
    return (environ.get("SCRIPT_NAME", "") or "").rstrip("/")


def make_vote_form(ed, works, lang, vot_token, csrf, include_geo, geo_js,
                   note="", conditions="", base=""):
    i18n = get_i18n(lang)
    max_num = max((w["numero"] for w in works), default=0)
    extra = ""
    if conditions:
        extra += "<div class=\"conditions\">%s</div>" % conditions
    if note:
        extra += "<p class=\"note\">%s</p>" % html.escape(note)
    form = (
        "<h1>%s</h1><p>%s</p>%s"
        "<form method=\"post\" action=\"%s/v/%s\" id=\"vf\">"
        "<input type=\"hidden\" name=\"csrft\" value=\"%s\">"
        "<label for=\"obra\">%s</label> "
        "<input id=\"obra\" name=\"obra\" type=\"number\" inputmode=\"numeric\""
        " min=\"1\" max=\"%d\" step=\"1\" required>"
        "<input type=\"hidden\" name=\"geo\" id=\"geo\" value=\"none\">"
        "<button type=\"submit\">%s</button>"
        "</form>"
        "<script>%s</script>")
    return form % (
        html.escape(ed["nom"]), i18n.get("vote_intro", ""), extra,
        html.escape(base, quote=True), h_radix(vot_token), html.escape(csrf),
        i18n.get("select_prompt", "Obra"), max_num,
        i18n.get("btn_vote", "Vota"), geo_js)


GEO_JS = """
(function(){
  var geo=document.getElementById('geo');
  if(!geo) return;
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      function(pos){ if(pos.coords){ geo.value='ok;'+(pos.coords.latitude)+';'+(pos.coords.longitude);} },
      function(){ /* es deixa vot; registrem geo:none */ },
      { enableHighAccuracy:true, timeout:8000, maximumAge:60000 }
    );
  }
})();
"""


def vote_page(environ, start_response, token, base=""):
    cfg = load_config()
    conn = connect(cfg)
    try:
        ed, works = get_edition_and_works(conn, token)
        lang = pick_lang(environ)
        i18n = get_i18n(lang)
        if ed is None:
            return respond(environ, start_response, "404 Not Found",
                           page_html(i18n.get("msg_token_invalid", ""),
                                     "<p>%s</p>" % html.escape(i18n.get("msg_token_invalid", "Enllaç no vàlid")), lang))
        if not edition_open(cfg, ed):
            msg = i18n.get("msg_edition_inactive",
                           "msg_edition_inactive")
            if ed["tancada"]:
                msg = i18n.get("msg_edition_closed", "msg_edition_closed")
            return respond(environ, start_response, "200 OK",
                           page_html(msg, "<h1>%s</h1><p>%s</p>" % (
                               html.escape(ed["nom"]), html.escape(msg)), lang))
        include_geo = ed["mode_geo"] in ("soft", "hard")
        geo_js = GEO_JS if include_geo else ""
        if not works:
            return respond(environ, start_response, "200 OK",
                           page_html(i18n.get("msg_no_works", ""),
                                     "<p>%s</p>" % html.escape(i18n.get("msg_no_works", "")), lang))
        device = get_device_id(environ, cfg)
        csrf = csrf_token(secret_key(cfg), device)
        conn.execute(
            "INSERT INTO visites (edicio_id, dispositiu_hash, ts) VALUES (?,?,?)",
            (ed["id"], device_hash(secret_key(cfg), device), int(time.time())))
        conn.commit()
        note = i18n.get("vote_note_mbl", "")
        conditions = ""
        if cfg.getboolean("edicio", "mostrar_condicions", fallback=False):
            conditions = i18n.get("vote_conditions", "")
        body = make_vote_form(ed, works, lang, token, csrf, include_geo, geo_js,
                              note=note, conditions=conditions, base=base)
        return respond(environ, start_response, "200 OK",
                       page_html(i18n.get("vote_header", "Vot"),
                                 body, lang),
                       extra_headers=[set_device_cookie(cfg, device, (base or "") + "/")])
    finally:
        conn.close()


def get_device_id(environ, cfg):
    cookies = parse_cookies(environ.get("HTTP_COOKIE", ""))
    name = cfg.get("general", "cookie_name", fallback="vid")
    dev = cookies.get(name)
    if dev:
        return dev
    dev = secrets.token_hex(16)
    return dev


def set_device_cookie(cfg, device_id, path="/"):
    name = cfg.get("general", "cookie_name", fallback="vid")
    maxage = 60 * 60 * 24 * 30
    secure = "; Secure" if cfg.getboolean("general", "ssl", fallback=True) else ""
    return ("Set-Cookie", "%s=%s; Path=%s; HttpOnly; SameSite=Lax; Max-Age=%d%s"
            % (name, device_id, path, maxage, secure))


def parse_cookies(s):
    out = {}
    for part in s.split(";"):
        if "=" in part:
            k, v = part.strip().split("=", 1)
            out[k] = v
    return out


def submit_vote(environ, start_response, token):
    cfg = load_config()
    conn = connect(cfg)
    try:
        lang = pick_lang(environ)
        i18n = get_i18n(lang)
        if rate_limited(environ, cfg):
            return respond(environ, start_response, "429 Too Many Requests",
                           page_html(i18n.get("msg_rate_limited", ""),
                                     "<p>%s</p>" % html.escape(i18n.get("msg_rate_limited", "")), lang))
        ed, works = get_edition_and_works(conn, token)
        if ed is None or not edition_open(cfg, ed):
            return respond(environ, start_response, "400 Bad Request",
                           page_html(i18n.get("msg_edition_inactive", ""),
                                     "<p>%s</p>" % html.escape(i18n.get("msg_edition_inactive", "")), lang))
        body = read_body(environ)
        if body is None:
            return respond(environ, start_response, "413 Payload Too Large", "413",
                           content_type="text/plain")
        fields = urllib.parse.parse_qs(body.decode("utf-8", "replace"))
        obra_s = fields.get("obra", [""])[0]
        csrf_s = fields.get("csrft", [""])[0]
        geo_s = fields.get("geo", ["none"])[0]
        try:
            obra_num = int(obra_s)
        except ValueError:
            obra_num = None
        device = get_device_id(environ, cfg)
        if not hmac.compare_digest(csrf_s, csrf_token(secret_key(cfg), device)):
            return respond(environ, start_response, "403 Forbidden",
                           page_html("403", "<p>403</p>", lang))
        obra = next((w for w in works if w["numero"] == obra_num), None)
        if obra is None:
            return respond(environ, start_response, "400 Bad Request",
                           page_html(i18n.get("msg_invalid_obra", ""),
                                     "<p>%s</p>" % html.escape(i18n.get("msg_invalid_obra", "")), lang))
        geo_estat = "none"
        if ed["mode_geo"] != "off":
            if geo_s.startswith("ok;"):
                try:
                    _, lat_s, lon_s = geo_s.split(";")
                    lat, lon = float(lat_s), float(lon_s)
                except ValueError:
                    lat = lon = None
                if lat is not None and ed["lat"] and ed["lon"] and ed["radi"]:
                    dist = haversine_m(lat, lon, ed["lat"], ed["lon"])
                    geo_estat = "ok" if dist <= ed["radi"] else "out"
                else:
                    geo_estat = "out"
            else:
                geo_estat = "none"
        if ed["mode_geo"] == "hard" and geo_estat != "ok":
            return respond(environ, start_response, "403 Forbidden",
                           page_html(i18n.get("geo_error_hard", ""),
                                     "<p>%s</p>" % html.escape(i18n.get("geo_error_hard", "")), lang))
        devhash = device_hash(secret_key(cfg), device)
        vot_limit = ed["vot_limit"] or 0
        if vot_limit > 0:
            cur = conn.execute(
                "SELECT COUNT(*) AS n FROM vots WHERE edicio_id=? AND obra_id=? AND dispositiu_hash=?",
                (ed["id"], obra["id"], devhash))
            if cur.fetchone()["n"] > 0:
                return respond(environ, start_response, "200 OK",
                               page_html(i18n.get("msg_vote_repeat", ""),
                                         "<p>%s</p>" % html.escape(i18n.get("msg_vote_repeat", "")), lang))
        ts = int(time.time())
        sig = hmac_sig(secret_key(cfg), (ed["id"], obra["id"], devhash, ts))
        conn.execute(
            "INSERT INTO vots (edicio_id,obra_id,dispositiu_hash,geo_estat,signatura,ts,paper)"
            " VALUES (?,?,?,?,?,?,0)",
            (ed["id"], obra["id"], devhash, geo_estat, sig, ts))
        conn.commit()
        cookies = [set_device_cookie(cfg, device, (app_base(environ) or "") + "/")]
        return respond(environ, start_response, "200 OK",
                       page_html(i18n.get("msg_vote_ok", ""),
                                 "<p>%s</p>" % html.escape(i18n.get("msg_vote_ok", "")), lang),
                       extra_headers=cookies)
    finally:
        conn.close()


# -------------------------------------------------------------- admin

ADMIN_SESSION_TTL = 60 * 60 * 4  # 4 h (també validat server-side)


def make_admin_session(cfg):
    """Cookie de sessió: HMAC(key, ("admin", ts)) + timestamp, amb caducitat server-side."""
    ts = int(time.time())
    sig = hmac_sig(admin_key(cfg), ("admin", ts))
    return "%s:%d" % (sig, ts)


def admin_session_valid(cfg, value):
    if not value or ":" not in value:
        return False
    sig, _, ts_s = value.rpartition(":")
    try:
        ts = int(ts_s)
    except ValueError:
        return False
    expect = hmac_sig(admin_key(cfg), ("admin", ts))
    if not hmac.compare_digest(sig, expect):
        return False
    return 0 <= time.time() - ts <= ADMIN_SESSION_TTL


def admin_csrf_token(cfg, session_value):
    return hmac_sig(admin_key(cfg), ("admin-csrf", session_value))


def admin_ok(environ, cfg):
    cookies = parse_cookies(environ.get("HTTP_COOKIE", ""))
    return admin_session_valid(cfg, cookies.get("admin", ""))


def admin_login_form(lang, base=""):
    i18n = get_i18n(lang)
    body = ("<h1>%s</h1>"
            "<form method=\"post\" action=\"%s/admin/login\">"
            "<label>%s</label> <input type=\"password\" name=\"pass\" autocomplete=\"current-password\">"
            "<button type=\"submit\">%s</button>"
            "</form>" % (html.escape(i18n.get("app_name", "Admin")),
                         html.escape(base, quote=True),
                         html.escape(i18n.get("admin_pass", "Contrasenya")),
                         html.escape(i18n.get("btn_login", "Entra"))))
    return page_html(i18n.get("app_name", "Admin"), body, lang)


def admin_handle(environ, start_response, sub="", base=""):
    cfg = load_config()
    lang = pick_lang(environ)
    i18n = get_i18n(lang)
    if not admin_ok(environ, cfg):
        return respond(environ, start_response, "401 Unauthorized",
                       admin_login_form(lang, base))
    conn = connect(cfg)
    try:
        ed_id = None
        row = conn.execute("SELECT id FROM edicions ORDER BY id LIMIT 1").fetchone()
        if row is not None:
            ed_id = row["id"]
        if sub == "stat":
            rows = conn.execute(
                "SELECT o.numero,o.titol,COUNT(v.id) AS v "
                "FROM obres o LEFT JOIN vots v ON v.obra_id=o.id "
                "GROUP BY o.id ORDER BY o.numero").fetchall()
            body = "<h1>%s</h1><table border=\"1\" cellpadding=\"6\" cellspacing=\"0\"><tr><th>%s</th><th>%s</th></tr>" % (
                html.escape(i18n.get("admin_stat_title", "Recompte")),
                html.escape(i18n.get("admin_obra", "Obra")),
                html.escape(i18n.get("admin_count", "Vots")))
            for r in rows:
                body += "<tr><td>%d %s</td><td>%d</td></tr>" % (
                    r["numero"], html.escape(r["titol"] or ""), r["v"])
            body += "</table><p><a href=\"%s/admin/\">↩ back</a></p>" % html.escape(base, quote=True)
            return respond(environ, start_response, "200 OK", page_html("admin", body, lang))
        if sub == "visites":
            total = conn.execute(
                "SELECT COUNT(*) AS n FROM visites WHERE edicio_id=?", (ed_id,)).fetchone()["n"]
            unics = conn.execute(
                "SELECT COUNT(DISTINCT dispositiu_hash) AS n FROM visites WHERE edicio_id=?",
                (ed_id,)).fetchone()["n"]
            rows = conn.execute(
                "SELECT datetime(ts,'unixepoch','localtime') AS d, COUNT(*) AS n "
                "FROM visites WHERE edicio_id=? GROUP BY strftime('%Y-%m-%d', datetime(ts,'unixepoch','localtime')) "
                "ORDER BY d DESC LIMIT 30", (ed_id,)).fetchall()
            body = ("<h1>%s</h1><p>%s: <b>%d</b> · %s: <b>%d</b></p>"
                    "<table border=\"1\" cellpadding=\"6\" cellspacing=\"0\"><tr><th>%s</th><th>%s</th></tr>"
                    % (html.escape(i18n.get("admin_visits_title", "Visites via QR")),
                       html.escape(i18n.get("admin_visits_total", "Visites")), total,
                       html.escape(i18n.get("admin_visits_uniq", "Dispositius únics")), unics,
                       html.escape(i18n.get("admin_visits_day", "Dia")),
                       html.escape(i18n.get("admin_visits_count", "Visites"))))
            for r in rows:
                body += "<tr><td>%s</td><td>%d</td></tr>" % (html.escape(r["d"]), r["n"])
            body += "</table><p><a href=\"%s/admin/\">↩</a></p>" % html.escape(base, quote=True)
            return respond(environ, start_response, "200 OK", page_html("admin", body, lang))
        if sub == "tancar" and environ.get("REQUEST_METHOD") == "POST":
            cookies = parse_cookies(environ.get("HTTP_COOKIE", ""))
            body = read_body(environ)
            if body is None:
                return respond(environ, start_response, "413 Payload Too Large", "413",
                               content_type="text/plain")
            fields = urllib.parse.parse_qs(body.decode("utf-8", "replace"))
            if not hmac.compare_digest(fields.get("csrft", [""])[0],
                                       admin_csrf_token(cfg, cookies.get("admin", ""))):
                return respond(environ, start_response, "403 Forbidden",
                               page_html("403", "<p>403</p>", lang))
            conn.execute("UPDATE edicions SET tancada=1, tancada_a=datetime('now')")
            conn.commit()
            body = "<p>%s</p><p><a href=\"%s/admin/\">↩</a></p>" % (
                html.escape(i18n.get("admin_closed", "Votació tancada")),
                html.escape(base, quote=True))
            return respond(environ, start_response, "200 OK", page_html("admin", body, lang))
        if sub == "export":
            rows = conn.execute(
                "SELECT e.nom AS edicio,o.numero,o.titol,o.autor,v.geo_estat,v.ts,v.signatura,v.paper "
                "FROM vots v JOIN edicions e ON e.id=v.edicio_id JOIN obres o ON o.id=v.obra_id "
                "ORDER BY v.ts").fetchall()
            buf = io.StringIO()
            writer = csv.writer(buf)
            writer.writerow(["edicio", "obra", "titol", "autor", "geo", "ts", "paper", "signatura"])
            for r in rows:
                writer.writerow([r["edicio"], r["numero"], r["titol"] or "",
                                 r["autor"] or "", r["geo_estat"], r["ts"], r["paper"], r["signatura"]])
            data = buf.getvalue().encode("utf-8")
            digest = hashlib.sha256(data).hexdigest()
            return respond(environ, start_response, "200 OK",
                           data, content_type="text/csv; charset=utf-8",
                           extra_headers=[
                               ("Content-Disposition", 'attachment; filename="vots.csv"'),
                               ("X-Content-SHA256", digest)])
        body = (
            "<h1>%s</h1>"
            "<p><a href=\"%s/admin/stat\">%s</a> · "
            "<a href=\"%s/admin/visites\">%s</a> · "
            "<a href=\"%s/admin/export\">%s (CSV)</a></p>"
            "<form method=\"post\" action=\"%s/admin/tancar\">"
            "<input type=\"hidden\" name=\"csrft\" value=\"%s\">"
            "<button type=\"submit\" onclick=\"return confirm('%s')\">%s</button></form>"
            "<p><a href=\"%s/admin/logout\">%s</a></p>"
            % (html.escape(i18n.get("admin_dashboard", "Admin")),
               html.escape(base, quote=True),
               html.escape(i18n.get("admin_stat", "Recompte en viu")),
               html.escape(base, quote=True),
               html.escape(i18n.get("admin_visits_title", "Visites via QR")),
               html.escape(base, quote=True),
               html.escape(i18n.get("btn_export", "Exporta")),
               html.escape(base, quote=True),
               html.escape(admin_csrf_token(cfg, parse_cookies(
                   environ.get("HTTP_COOKIE", "")).get("admin", ""))),
               html.escape(i18n.get("close_confirm", "Segur que vols tancar la votació?")),
               html.escape(i18n.get("btn_close", "Tanca la votació")),
               html.escape(base, quote=True),
               html.escape(i18n.get("btn_logout", "Surt"))))
        return respond(environ, start_response, "200 OK", page_html("admin", body, lang))
    finally:
        conn.close()


def admin_login(environ, start_response, base=""):
    cfg = load_config()
    lang = pick_lang(environ)
    i18n = get_i18n(lang)
    if environ.get("REQUEST_METHOD") == "POST":
        if rate_limited(environ, cfg, limit=10, bucket="admin:"):
            return respond(environ, start_response, "429 Too Many Requests",
                           page_html(i18n.get("msg_rate_limited", ""),
                                     "<p>%s</p>" % html.escape(i18n.get("msg_rate_limited", "")), lang))
        body = read_body(environ)
        if body is None:
            return respond(environ, start_response, "413 Payload Too Large", "413",
                           content_type="text/plain")
        fields = urllib.parse.parse_qs(body.decode("utf-8", "replace"))
        if hmac.compare_digest(fields.get("pass", [""])[0], admin_key(cfg)):
            tok = make_admin_session(cfg)
            exp = ADMIN_SESSION_TTL
            secure = "; Secure" if cfg.getboolean("general", "ssl", fallback=True) else ""
            return respond(environ, start_response, "302 Found", "",
                           extra_headers=[
                                ("Location", base + "/admin/"),
                               ("Set-Cookie", "admin=%s; Path=/; HttpOnly; SameSite=Lax; Max-Age=%d%s" % (tok, exp, secure))])
        return respond(environ, start_response, "401 Unauthorized", admin_login_form(lang, base))
    return respond(environ, start_response, "200 OK", admin_login_form(lang, base))


def admin_logout(environ, start_response, base=""):
    return respond(environ, start_response, "302 Found", "",
                   extra_headers=[("Location", base + "/admin/"),
                                  ("Set-Cookie", "admin=; Path=/; Max-Age=0")])


# ---------------------------------------------------------------- wsgi

def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET")
    base = app_base(environ)
    if path.startswith("/v/"):
        token = path[3:]
        if method == "GET":
            return vote_page(environ, start_response, token, base)
        if method == "POST":
            return submit_vote(environ, start_response, token)
        return respond(environ, start_response, "405 Method Not Allowed", "405")
    if path == "/admin/login":
        return admin_login(environ, start_response, base)
    if path == "/admin/logout":
        return admin_logout(environ, start_response, base)
    if path.startswith("/admin/"):
        sub = path[len("/admin/"):]
        return admin_handle(environ, start_response, sub, base)
    if path == "/admin" or path == "/admin/":
        return admin_handle(environ, start_response, "", base)
    if path == "/health":
        return respond(environ, start_response, "200 OK", "ok", content_type="text/plain")
    return respond(environ, start_response, "404 Not Found", "404")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", sys.argv[1] if len(sys.argv) > 1 else 8010))
    server = make_server("127.0.0.1", port, application)
    print("Votacio M1 a http://127.0.0.1:%d" % port)
    server.serve_forever()
"""Proves del mòdul formularis amb un servidor WSGI real (servidor de proves)."""
import io
import os
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
from wsgiref.simple_server import WSGIRequestHandler, make_server

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as m  # noqa: E402

PORT = 8021
BASE = "http://127.0.0.1:%d" % PORT
SMTP_RECEIVED = []


def fake_send_mail(cfg, to_addr, subject, cos, reply_to=None, **kw):
    SMTP_RECEIVED.append({"to": to_addr, "subject": subject, "body": cos,
                          "reply_to": reply_to})
    return True, ""


m.send_mail = fake_send_mail


class Quiet(WSGIRequestHandler):
    def log_message(self, *a):
        pass


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


# L'èxit és un 303 cap a la pàgina de gràcies del web; post() el compta com a
# 200 si la Location acaba en /gracies/, així les expectatives no canvien.
NO_REDIRECT = urllib.request.build_opener(_NoRedirect)


def post(path, fields, headers=None, method="POST", consent=True):
    if consent:
        fields = dict(fields, consentiment="sí")
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(BASE + path, data=data, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with NO_REDIRECT.open(req) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        if e.code == 303:
            return 200 if e.headers.get("Location", "").endswith("/gracies/") else 303, ""
        return e.code, e.read().decode()


def get(path):
    try:
        with urllib.request.urlopen(BASE + path) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


cfg = m.load_config()
m.load_config = lambda: cfg
ok = True
print("config trobada:", os.path.exists(m.CONFIG_PATH),
      "| allowed_origins:", sorted(m.allowed_origins(cfg)))

srv = make_server("127.0.0.1", PORT, m.application, handler_class=Quiet)
threading.Thread(target=srv.serve_forever, daemon=True).start()

print("health          ", get("/health")[0], "(esperat 200)")
print("arrel           ", get("/")[0], "(esperat 200)")
print("ruta desconeguda ", get("/no-existeix")[0], "(esperat 404)")

s, _ = post("/envia/contacte", {"nom": "Prova", "email": "prova@example.org",
                                "assumpte": "Hola", "missatge": "Text"},
            {"Origin": "https://9barrisimatge.org"})
print("origen valid    ", s, "(esperat 200)", SMTP_RECEIVED[-1]["subject"] if SMTP_RECEIVED else "sense correu")
ok &= s == 200 and SMTP_RECEIVED[-1]["reply_to"] == "prova@example.org"

s, _ = post("/envia/contacte", {"nom": "Prova"},
            {"Origin": "https://formularis.linuxbcn.com"})
print("origen altre    ", s, "(esperat 403)")

s, _ = post("/envia/contacte", {"nom": "Prova"})
print("sense origen    ", s, "(esperat 403)")

s, _ = post("/envia/contacte", {"nom": "Prova", "_honey": "spam"},
            {"Origin": "https://9barrisimatge.org"})
print("honeypot        ", s, "(esperat 200, i cap correu nou)")
ok &= s == 200 and len(SMTP_RECEIVED) == 1

s, _ = post("/envia/inventat", {"nom": "Prova"},
            {"Origin": "https://9barrisimatge.org"})
print("formulari desconegut", s, "(esperat 404)")

s, _ = post("/envia/contacte", {"_honey": ""}, {"Origin": "https://9barrisimatge.org"},
            consent=False)
print("sense camps     ", s, "(esperat 400)")

n = len(SMTP_RECEIVED)
s, _ = post("/envia/contacte", {"nom": "Prova", "missatge": "x"},
            {"Origin": "https://9barrisimatge.org"}, consent=False)
print("sense consentiment", s, "(esperat 400 i cap correu)")
ok &= s == 400 and len(SMTP_RECEIVED) == n

s, _ = post("/envia/contacte", {"nom": "Prova", "email": "no-es-un-correu",
                                "missatge": "x", "camp_inventat": "surt?"},
            {"Origin": "https://9barrisimatge.org"})
body = SMTP_RECEIVED[-1]
print("email invàlid   ", s, "| Reply-To:", body["reply_to"], "(esperat None)",
      "| camp inventat present:", "camp_inventat" in body["body"])
ok &= s == 200 and body["reply_to"] is None and "camp_inventat" not in body["body"]

s, _ = post("/envia/contacte", {"nom": "Prova\r\nBcc: evil@example.org",
                                "missatge": "x"},
            {"Origin": "https://9barrisimatge.org"})
print("injecció CRLF   ", s, "| cos:", repr(SMTP_RECEIVED[-1]["body"][:40]))
ok &= s == 200 and "\r" not in SMTP_RECEIVED[-1]["body"] and "evil@example.org" in SMTP_RECEIVED[-1]["body"]

s, _ = post("/envia/contacte", {"nom": "Prova", "missatge": "x" * 3000},
            {"Origin": "https://9barrisimatge.org"})
# Es mesura el camp dins del cos, no el cos sencer (porta el peu legal).
valor = SMTP_RECEIVED[-1]["body"].split("missatge: ", 1)[1].split("\n", 1)[0]
print("camp massa llarg", s, "| longitud del camp:", len(valor),
      "(tope %d)" % m.MAX_CAMP)
ok &= s == 200 and len(valor) <= m.MAX_CAMP

s, _ = post("/envia/contacte", {"nom": "Prova", "missatge": "x"},
            {"Origin": "https://9barrisimatge.org", "Referer": "https://www.9barrisimatge.org/contacte/"})
print("sense Origin, amb Referer de www", s, "(esperat 200)")
ok &= s == 200

cfg.set("general", "rate_limit", "3")
m._rate.clear()
codes = [post("/envia/contacte", {"nom": "P", "missatge": "x"},
              {"Origin": "https://9barrisimatge.org"})[0] for _ in range(5)]
print("límit de peticions", codes, "(ha d'aparèixer un 429)")
ok &= 429 in codes

m._rate.clear()
cfg.set("general", "rate_limit", "20")
cfg.set("smtp", "password", "")
os.environ.pop("FORMULARIS_SMTP_PASSWORD", None)
s, _ = post("/envia/contacte", {"nom": "Prova", "missatge": "x"},
            {"Origin": "https://9barrisimatge.org"})
print("sense contrasenya SMTP", s, "(esperat 503 i cap correu)")
ok &= s == 503

srv.shutdown()
print("RESULTAT:", "OK" if ok else "HI HA FALLADES")

# ------------------------------------------------------------ comentaris
import json as _json
import tempfile

m._rate.clear()
cfg.set("smtp", "password", "prova")
if not cfg.has_section("comentaris"):
    cfg.add_section("comentaris")
cfg.set("comentaris", "secret", "x" * 64)
cfg.set("comentaris", "github_token", "fals")
cfg.set("comentaris", "dir", tempfile.mkdtemp())
if not cfg.has_option("general", "site_url"):
    cfg.set("general", "site_url", "https://9barrisimatge.org/")
PUBLICATS = []
srv.server_close()
m.comentaris.publish = lambda c, item: (PUBLICATS.append(item) or True, "")
srv = make_server("127.0.0.1", PORT, m.application, handler_class=Quiet)
threading.Thread(target=srv.serve_forever, daemon=True).start()
ORIG = {"Origin": "https://9barrisimatge.org"}
PAG = "https://9barrisimatge.org/2026/09/prova.html"
BASE_C = {"entrada": "2026-09-20-prova_3", "pagina": PAG,
          "nom": "Veïna", "email": "veina@example.org",
          "comentari": "Molt bones fotos!\r\nGràcies."}


def post_loc(path, fields, headers=None):
    req = urllib.request.Request(BASE + path, method="POST",
                                 data=urllib.parse.urlencode(fields).encode())
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with NO_REDIRECT.open(req) as r:
            return r.status, "", r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location", ""), e.read().decode()


n = len(SMTP_RECEIVED)
s, loc, _ = post_loc("/envia/comentari", dict(BASE_C, consentiment="sí"), ORIG)
pend = os.listdir(os.path.join(cfg.get("comentaris", "dir"), "pendents"))
print("comentari vàlid ", s, loc, "| pendents:", len(pend), "| correus nous:", len(SMTP_RECEIVED) - n)
ok &= s == 303 and loc == PAG + "#comentari-enviat" and len(pend) == 1 and len(SMTP_RECEIVED) == n + 1
cid = pend[0][:-5]
mail = SMTP_RECEIVED[-1]
ok &= mail["reply_to"] == "veina@example.org" and "/comentari/%s?sig=" % cid in mail["body"]
saved = _json.load(open(os.path.join(cfg.get("comentaris", "dir"), "pendents", pend[0])))
ok &= saved["text"] == "Molt bones fotos!\nGràcies."
print("salts de línia conservats:", saved["text"] == "Molt bones fotos!\nGràcies.")

s, _, _ = post_loc("/envia/comentari", dict(BASE_C), ORIG)
print("sense consentiment", s, "(esperat 400)")
ok &= s == 400
s, _, _ = post_loc("/envia/comentari", dict(BASE_C, consentiment="sí", pagina="https://dolent.example/"), ORIG)
print("pàgina d'un altre web", s, "(esperat 400: no hi ha redirecció oberta)")
ok &= s == 400
s, _, _ = post_loc("/envia/comentari", dict(BASE_C, consentiment="sí", entrada="../../etc"), ORIG)
print("entrada amb ../   ", s, "(esperat 400)")
ok &= s == 400
s, _, _ = post_loc("/envia/comentari", dict(BASE_C, consentiment="sí"))
print("sense origen      ", s, "(esperat 403)")
ok &= s == 403
before = len(os.listdir(os.path.join(cfg.get("comentaris", "dir"), "pendents")))
s, loc, _ = post_loc("/envia/comentari", dict(BASE_C, consentiment="sí", _honey="spam"), ORIG)
after = len(os.listdir(os.path.join(cfg.get("comentaris", "dir"), "pendents")))
print("honeypot          ", s, loc, "| pendents nous:", after - before, "(esperat 0)")
ok &= s == 303 and after == before

sig = m.comentaris.sign(cfg, cid)
s, body = get("/comentari/%s?sig=%s" % (cid, "0" * 64))
print("revisió signatura dolenta", s, "(esperat 403)")
ok &= s == 403
s, body = get("/comentari/%s?sig=%s" % (cid, sig))
print("revisió GET       ", s, "| no publica res:", len(PUBLICATS) == 0, "| mostra el text:", "Molt bones fotos!" in body)
ok &= s == 200 and not PUBLICATS and "Molt bones fotos!" in body
s, _, body = post_loc("/comentari/" + cid, {"sig": sig, "accio": "publica"})
print("publica           ", s, "| publicats:", len(PUBLICATS), "| sense correu al repo:", "email" not in _json.dumps({k: PUBLICATS[0][k] for k in ("nom", "text", "data")}) if PUBLICATS else None)
ok &= s == 200 and len(PUBLICATS) == 1
s, _, _ = post_loc("/comentari/" + cid, {"sig": sig, "accio": "publica"})
print("publica dues vegades", s, "(esperat 410)")
ok &= s == 410

s, loc, _ = post_loc("/envia/comentari", dict(BASE_C, consentiment="sí", comentari="Compra a www.spam.example"), ORIG)
cid2 = [f for f in os.listdir(os.path.join(cfg.get("comentaris", "dir"), "pendents"))][0][:-5]
print("avís d'enllaços al correu:", "enllaç" in SMTP_RECEIVED[-1]["body"])
ok &= "enllaç" in SMTP_RECEIVED[-1]["body"]
s, _, _ = post_loc("/comentari/" + cid2, {"sig": m.comentaris.sign(cfg, cid2), "accio": "descarta"})
print("descarta          ", s, "| pendents:", len(os.listdir(os.path.join(cfg.get("comentaris", "dir"), "pendents"))), "| publicats:", len(PUBLICATS))
ok &= s == 200 and len(PUBLICATS) == 1

cfg.set("comentaris", "secret", "CANVIA-ME")
s, _, _ = post_loc("/envia/comentari", dict(BASE_C, consentiment="sí"), ORIG)
print("secret per defecte", s, "(esperat 503)")
ok &= s == 503

srv.shutdown()
print("RESULTAT COMENTARIS:", "OK" if ok else "HI HA FALLADES")

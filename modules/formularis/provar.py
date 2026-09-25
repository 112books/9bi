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


def fake_send_mail(cfg, to_addr, subject, cos, reply_to=None):
    SMTP_RECEIVED.append({"to": to_addr, "subject": subject, "body": cos,
                          "reply_to": reply_to})
    return True, ""


m.send_mail = fake_send_mail


class Quiet(WSGIRequestHandler):
    def log_message(self, *a):
        pass


def post(path, fields, headers=None, method="POST"):
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(BASE + path, data=data, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
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

s, _ = post("/envia/contacte", {"_honey": ""}, {"Origin": "https://9barrisimatge.org"})
print("sense camps     ", s, "(esperat 400)")

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
print("camp massa llarg", s, "| longitud del camp:", len(SMTP_RECEIVED[-1]["body"]))
ok &= s == 200 and len(SMTP_RECEIVED[-1]["body"]) < 2200

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

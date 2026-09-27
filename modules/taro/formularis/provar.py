#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Col·lectiu 9 Barris Imatge
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


def fake_send_mail(cfg, to_addr, subject, cos, reply_to=None, html=None):
    """Substitueix l'SMTP real: es queda el correu per poder-lo comprovar."""
    SMTP_RECEIVED.append({"to": to_addr, "subject": subject, "body": cos,
                          "reply_to": reply_to, "html": html})
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
# L'origen i l'adreça de prova surten del config: així la prova serveix
# qualsevol instal·lació, sense editar el fitxer.
ORIGIN = sorted(m.allowed_origins(cfg))[0] if m.allowed_origins(cfg) else ""
ALT_ORIGIN = "https://altre-exemple.org"
PROVA_EMAIL = cfg.get("general", "destinatari", fallback="") or "prova@example.org"
print("config trobada:", os.path.exists(m.CONFIG_PATH),
      "| allowed_origins:", sorted(m.allowed_origins(cfg)))

srv = make_server("127.0.0.1", PORT, m.application, handler_class=Quiet)
threading.Thread(target=srv.serve_forever, daemon=True).start()

print("health          ", get("/health")[0], "(esperat 200)")
print("arrel           ", get("/")[0], "(esperat 200)")
print("ruta desconeguda ", get("/no-existeix")[0], "(esperat 404)")

s, _ = post("/envia/contacte", {"nom": "Prova", "email": PROVA_EMAIL,
                                "assumpte": "Hola", "missatge": "Text"},
            {"Origin": ORIGIN})
print("origen valid    ", s, "(esperat 200)", SMTP_RECEIVED[-1]["subject"] if SMTP_RECEIVED else "sense correu")
ok &= s == 200 and SMTP_RECEIVED[-1]["reply_to"] == PROVA_EMAIL

s, _ = post("/envia/contacte", {"nom": "Prova"},
            {"Origin": ALT_ORIGIN})
print("origen altre    ", s, "(esperat 403)")

s, _ = post("/envia/contacte", {"nom": "Prova"})
print("sense origen    ", s, "(esperat 403)")

s, _ = post("/envia/contacte", {"nom": "Prova", "_honey": "spam"},
            {"Origin": ORIGIN})
print("honeypot        ", s, "(esperat 200, i cap correu nou)")
ok &= s == 200 and len(SMTP_RECEIVED) == 1

s, _ = post("/envia/inventat", {"nom": "Prova"},
            {"Origin": ORIGIN})
print("formulari desconegut", s, "(esperat 404)")

s, _ = post("/envia/contacte", {"_honey": ""}, {"Origin": ORIGIN})
print("sense camps     ", s, "(esperat 400)")

s, _ = post("/envia/contacte", {"nom": "Prova", "email": "no-es-un-correu",
                                "missatge": "x", "camp_inventat": "surt?"},
            {"Origin": ORIGIN})
body = SMTP_RECEIVED[-1]
print("email invàlid   ", s, "| Reply-To:", body["reply_to"], "(esperat None)",
      "| camp inventat present:", "camp_inventat" in body["body"])
ok &= s == 200 and body["reply_to"] is None and "camp_inventat" not in body["body"]

s, _ = post("/envia/contacte", {"nom": "Prova\r\nBcc: evil@example.org",
                                "missatge": "x"},
            {"Origin": ORIGIN})
print("injecció CRLF   ", s, "| cos:", repr(SMTP_RECEIVED[-1]["body"][:40]))
ok &= s == 200 and "\r" not in SMTP_RECEIVED[-1]["body"] and "evil@example.org" in SMTP_RECEIVED[-1]["body"]

# El camp es retalla a MAX_CAMP. El que es mesura és el camp dins del cos,
# no el cos sencer: el cos inclou el peu legal, que ha de ser-hi sempre.
s, _ = post("/envia/contacte", {"nom": "Prova", "missatge": "x" * 3000},
            {"Origin": ORIGIN})
cos = SMTP_RECEIVED[-1]["body"]
valor = cos.split("missatge: ", 1)[1].split("\n", 1)[0]
print("camp massa llarg", s, "| longitud del camp:", len(valor),
      "(tope %d)" % m.MAX_CAMP)
ok &= s == 200 and len(valor) <= m.MAX_CAMP

s, _ = post("/envia/contacte", {"nom": "Prova", "missatge": "x"},
            {"Origin": ORIGIN, "Referer": ORIGIN + "/contacte/"})
print("sense Origin, amb Referer de www", s, "(esperat 200)")
ok &= s == 200

cfg.set("general", "rate_limit", "3")
m._rate.clear()
codes = [post("/envia/contacte", {"nom": "P", "missatge": "x"},
              {"Origin": ORIGIN})[0] for _ in range(5)]
print("límit de peticions", codes, "(ha d'aparèixer un 429)")
ok &= 429 in codes

m._rate.clear()
cfg.set("general", "rate_limit", "20")
cfg.set("smtp", "password", "")
os.environ.pop("FORMULARIS_SMTP_PASSWORD", None)
s, _ = post("/envia/contacte", {"nom": "Prova", "missatge": "x"},
            {"Origin": ORIGIN})
print("sense contrasenya SMTP", s, "(esperat 503 i cap correu)")
ok &= s == 503

srv.shutdown()
print("RESULTAT:", "OK" if ok else "HI HA FALLADES")

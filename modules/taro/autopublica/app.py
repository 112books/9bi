#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Col·lectiu 9 Barris Imatge
# Llicència i avisos (fitxer LICENSE a l'arrel del repositori)
"""Autopublica — publica el web automàticament en arribar un push al repositori.

App WSGI en Python pur (només stdlib, zero dependències en producció),
compatible amb Phusion Passenger, waitress i el servidor WSGI de desenvolupament.

Flux: el CMS (Sveltia, Decap, el que facis servir) commiteja i fa push a la
branca del web. Un webhook del repositori (Forgejo, Gitea, GitLab…) fa un POST
a /hook amb capçalera de signatura HMAC-SHA256 del cos i el secret compartit.
Aquesta app:
  1. Verifica la signatura HMAC per acceptar només webhooks legítims.
  2. Agafa un lock de build (per evitar builds concurrents).
  3. Executa `tools/deploy.sh` (pull + build + push del build).
  4. Respon 200 (o 500 si el build falla).

Si el teu web es publica amb integració contínua (GitHub Actions, GitLab CI…),
no necessites aquest mòdul: engega el push i deixa que el CI publiqui.

Routes:
    GET  /health    → 200 "ok" (monitorització)
    POST /hook      → rep el webhook, dispara el build
    GET  /          → fàbrica WSGI (Passenger ho fa servir)
"""
import configparser
import hmac
import hashlib
import json
import os
import re
import subprocess
import threading
import time

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.environ.get("AUTOPUBLICA_CONFIG", os.path.join(MODULE_DIR, "config.ini"))
DEPLOY_SCRIPT = os.path.join(MODULE_DIR, "tools", "deploy.sh")

_build_lock = threading.Lock()


def load_config():
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_PATH, encoding="utf-8")
    return cfg


def cfg_get(cfg, section, key, default=""):
    try:
        return cfg.get(section, key)
    except (configparser.NoSectionError, configparser.NoOptionError):
        return default


def verify_signature(payload, signature, secret):
    """Verifica la signatura del webhook: HMAC-SHA256 en hexadecimal del cos.

    S'accepten els capçaleres que envien Forgejo i Gitea (X-Forgejo-Signature,
    X-Gitea-Signature i X-Codeberg-Signature, que és el mateix). Els altres
    forjats poden usar una capçalera equivalent. GitLab, en canvi, envia un
    token pla en comptes d'una signatura, i això no és el mateix protocol."""
    if not secret or not signature:
        return False
    expected = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def redact(text):
    """Elimina credencials del text que es retorna per HTTP."""
    out = text or ""
    push_url = os.environ.get("AUTOPUBLICA_PUSH_URL", "")
    if push_url:
        out = out.replace(push_url, "[push-url redacted]")
    out = re.sub(r"(https?://)[^/\s:@]+:[^@\s]+@", r"\1[redacted]@", out)
    return out


def run_deploy(cfg, branch):
    """Executa el desplegament real (build + push a pages)."""
    log = []
    def line(x):
        log.append(x)
        return x

    env = dict(os.environ)
    env.update({
        "AUTOPUBLICA_DEPLOY_BRANCH": branch,
        "HUGO_BASEURL": cfg_get(cfg, "build", "baseurl", ""),
    })

    if not os.path.exists(DEPLOY_SCRIPT):
        return False, line("Falta el script de desplegament: %s" % DEPLOY_SCRIPT)
    os.chmod(DEPLOY_SCRIPT, 0o755)

    p = subprocess.run(
        ["/bin/bash", DEPLOY_SCRIPT],
        env=env, capture_output=True, text=True, cwd=cfg_get(cfg, "repo", "workdir", MODULE_DIR))
    log.append("exit=%s" % p.returncode)
    if p.stdout:
        log.append(redact(p.stdout.strip()))
    if p.stderr:
        log.append(redact(p.stderr.strip()))
    return p.returncode == 0, "\n".join(log)


def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET")

    if path.rstrip("/") == "/health":
        body = b"ok"
        start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8"),
                                  ("Content-Length", str(len(body)))])
        return [body]

    if path.rstrip("/") == "/hook" and method == "POST":
        cfg = load_config()
        length = int(environ.get("CONTENT_LENGTH") or 0)
        payload = environ["wsgi.input"].read(length) if length else b""

        secret = cfg_get(cfg, "general", "secret", "")
        sig = (environ.get("HTTP_X_CODEBERG_SIGNATURE", "")
              or environ.get("HTTP_X_FORGEJO_SIGNATURE", "")
              or environ.get("HTTP_X_GITEA_SIGNATURE", ""))
        if not verify_signature(payload, sig, secret):
            body = b"signatura no valida"
            start_response("403 Forbidden", [("Content-Type", "text/plain; charset=utf-8"),
                                             ("Content-Length", str(len(body)))])
            return [body]

        # parseja l'esdeveniment per extreure la branca
        ref = ""
        try:
            data = json.loads(payload.decode("utf-8", "replace"))
            ref = data.get("ref", "")
        except Exception:
            pass

        if ref and not ref.endswith("/main"):
            body = b"ignorat (no es push a main)"
            start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8"),
                                      ("Content-Length", str(len(body)))])
            return [body]

        # lock per evitar builds concurrents
        if not _build_lock.acquire(blocking=False):
            body = b"build en curs"
            start_response("409 Conflict", [("Content-Type", "text/plain; charset=utf-8"),
                                            ("Content-Length", str(len(body)))])
            return [body]
        try:
            ok, output = run_deploy(cfg, "main")
        finally:
            _build_lock.release()

        status = "200 OK" if ok else "500 Internal Server Error"
        body = output.encode("utf-8", "replace")
        start_response(status, [("Content-Type", "text/plain; charset=utf-8"),
                                ("Content-Length", str(len(body)))])
        return [body]

    body = ("autopublica: POST /hook amb la signatura del webhook, "
            "o GET /health\n").encode("utf-8")
    start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8"),
                              ("Content-Length", str(len(body)))])
    return [body]


app = application

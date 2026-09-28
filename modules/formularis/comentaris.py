# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Col·lectiu 9 Barris Imatge
# Llicència i avisos (fitxer LICENSE a l'arrel del repositori)
"""Comentaris de les entrades del web, amb moderació prèvia (T-16).

Flux:
  1. POST /envia/comentari (des del formulari de cada entrada): es valida
     com els altres formularis (origen, honeypot, límit, consentiment),
     es desa el comentari a [comentaris] dir/pendents/<id>.json i s'envia un
     correu al moderador amb un enllaç signat (HMAC) per revisar-lo.
  2. GET /comentari/<id>?sig=...: pàgina de revisió amb els botons «Publica»
     i «Descarta». El GET no fa res: els filtres antispam dels correus obren
     els enllaços sols, i no han de poder publicar ni esborrar res.
  3. POST /comentari/<id> (accio=publica|descarta, sig): si es publica, es
     crea data/comentaris/<entrada>/<id>.json al repositori via l'API de
     GitHub; el commit a main dispara el build i el comentari surt al web.
     En tots dos casos s'esborra el fitxer pendent.

Al repositori (públic) només hi van nom, text i data. El correu, si el
posen, només arriba al moderador (Reply-To) i s'esborra del servidor amb
el fitxer pendent.
"""
import base64
import hashlib
import hmac
import html as htmlmod
import json
import os
import re
import secrets
import sys
import time
import urllib.error
import urllib.request

MAX_NOM = 80
MAX_TEXT = 2000
_ENTRADA_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,150}$")
_ID_RE = re.compile(r"^[0-9a-f]{16}$")
_URL_RE = re.compile(r"https?://|www\.", re.I)


# ------------------------------------------------------------- config

def cfg_get(cfg, key, fallback=""):
    return cfg.get("comentaris", key, fallback=fallback, raw=True).strip()


def secret(cfg):
    """Clau HMAC dels enllaços de moderació. Sense clau, el servei no arrenca
    la moderació (millor fallar que signar amb una clau coneguda)."""
    v = cfg_get(cfg, "secret") or os.environ.get("COMENTARIS_SECRET", "")
    if len(v) < 32 or v.upper().startswith(("CANVIA", "CHANGE")):
        return ""
    return v


def store_dir(cfg, module_dir):
    d = cfg_get(cfg, "dir") or os.path.join(module_dir, "comentaris")
    return os.path.join(d, "pendents")


def ready(cfg):
    return bool(secret(cfg)) and bool(cfg_get(cfg, "github_token"))


# ---------------------------------------------------------- signatura

def sign(cfg, cid):
    return hmac.new(secret(cfg).encode(), ("comentari:" + cid).encode(),
                    hashlib.sha256).hexdigest()


def sig_ok(cfg, cid, sig):
    if not secret(cfg) or not sig:
        return False
    return hmac.compare_digest(sign(cfg, cid), sig)


# ------------------------------------------------------------ pendents

def save_pending(cfg, module_dir, item):
    d = store_dir(cfg, module_dir)
    os.makedirs(d, mode=0o700, exist_ok=True)
    path = os.path.join(d, item["id"] + ".json")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(item, f, ensure_ascii=False)


def load_pending(cfg, module_dir, cid):
    if not _ID_RE.match(cid or ""):
        return None
    path = os.path.join(store_dir(cfg, module_dir), cid + ".json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def drop_pending(cfg, module_dir, cid):
    if _ID_RE.match(cid or ""):
        try:
            os.remove(os.path.join(store_dir(cfg, module_dir), cid + ".json"))
        except OSError:
            pass


# ------------------------------------------------------------- entrada

def build_item(fields, site_url, clean_value):
    """Valida els camps del formulari. Torna (item, error) on error és la
    clau i18n del missatge (o None)."""
    entrada = clean_value(fields.get("entrada", ""), 160)
    pagina = clean_value(fields.get("pagina", ""), 500)
    nom = clean_value(fields.get("nom", ""), MAX_NOM)
    email = clean_value(fields.get("email", ""), 254)
    # El comentari pot tenir salts de línia: només es treuen els altres
    # caràcters de control.
    text = fields.get("comentari", "").replace("\r\n", "\n")
    text = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()[:MAX_TEXT]

    if not _ENTRADA_RE.match(entrada):
        return None, "msg_comentari_entrada"
    # La pàgina ha de ser del web: és on tornem després d'enviar (sense
    # això seria una redirecció oberta).
    if not pagina.startswith(site_url.rstrip("/") + "/"):
        return None, "msg_comentari_entrada"
    if not nom or not text:
        return None, "msg_empty"
    if not fields.get("consentiment"):
        return None, "msg_consent"
    return {
        "id": secrets.token_hex(8),
        "entrada": entrada,
        "pagina": pagina,
        "nom": nom,
        "email": email,
        "text": text,
        "data": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "enllacos": len(_URL_RE.findall(text)),
    }, None


# ----------------------------------------------------------- publicació

def publish(cfg, item):
    """Crea data/comentaris/<entrada>/<id>.json al repositori. Torna
    (ok, detall). Només hi van nom, text i data."""
    token = cfg_get(cfg, "github_token")
    repo = cfg_get(cfg, "github_repo", "112books/9bi")
    branch = cfg_get(cfg, "github_branch", "main")
    path = "data/comentaris/%s/%s.json" % (item["entrada"], item["id"])
    doc = {"nom": item["nom"], "text": item["text"], "data": item["data"]}
    body = json.dumps({
        "message": "Comentari aprovat a %s" % item["entrada"],
        "content": base64.b64encode(
            (json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
            .encode("utf-8")).decode("ascii"),
        "branch": branch,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.github.com/repos/%s/contents/%s" % (repo, path),
        data=body, method="PUT",
        headers={"Authorization": "Bearer " + token,
                 "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28",
                 "User-Agent": "9bi-comentaris/1.0",
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status in (200, 201), ""
    except urllib.error.HTTPError as e:
        # 422: el fitxer ja existeix (doble clic a «Publica»): ja és publicat.
        if e.code == 422:
            return True, "ja existia"
        return False, "HTTP %s" % e.code
    except Exception as e:
        return False, "%s: %s" % (type(e).__name__, e)


# ----------------------------------------------------------------- correu

def review_url(cfg, cid):
    base = cfg_get(cfg, "base_url", "https://formularis.linuxbcn.com").rstrip("/")
    return "%s/comentari/%s?sig=%s" % (base, cid, sign(cfg, cid))


def mail_text(cfg, item):
    avis = ""
    if item.get("enllacos"):
        avis = "\nAtenció: el comentari conté %d enllaç(os).\n" % item["enllacos"]
    return (
        "Comentari nou pendent de revisió.\n\n"
        "Entrada: %s\nNom: %s\nCorreu (no es publica): %s\n%s\n"
        "%s\n\n"
        "Per publicar-lo o descartar-lo:\n%s\n\n"
        "Si no fas res, no es publica.\n"
        % (item["pagina"], item["nom"], item["email"] or "(no n'ha posat)",
           avis, item["text"], review_url(cfg, item["id"])))


# ------------------------------------------------------------- pàgines

def review_page(cfg, item, sig):
    esc = htmlmod.escape
    avis = ""
    if item.get("enllacos"):
        avis = ('<p class="msg err">El comentari conté %d enllaç(os): '
                'revisa que no sigui publicitat.</p>' % item["enllacos"])
    return (
        "<h1>Comentari pendent</h1>"
        "<p>Entrada: <a href=\"%s\">%s</a></p>"
        "<table><tr><th>Nom</th><td>%s</td></tr>"
        "<tr><th>Correu</th><td>%s <small>(no es publica)</small></td></tr>"
        "<tr><th>Data</th><td>%s</td></tr>"
        "<tr><th>Comentari</th><td>%s</td></tr></table>%s"
        "<form method=\"post\" style=\"display:flex;gap:.6rem\">"
        "<input type=\"hidden\" name=\"sig\" value=\"%s\">"
        "<button name=\"accio\" value=\"publica\" type=\"submit\">Publica</button>"
        "<button name=\"accio\" value=\"descarta\" type=\"submit\">Descarta</button>"
        "</form>"
        "<p><small>En publicar-lo, el comentari entra al repositori i surt "
        "al web en el pròxim build (un parell de minuts). El correu no "
        "s'hi publica mai.</small></p>"
        % (esc(item["pagina"]), esc(item["pagina"]), esc(item["nom"]),
           esc(item["email"] or "—"), esc(item["data"]),
           esc(item["text"]).replace("\n", "<br>"), avis, esc(sig)))


def log(msg):
    print("comentaris: " + msg, file=sys.stderr)

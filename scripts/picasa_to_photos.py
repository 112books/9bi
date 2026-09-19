#!/usr/bin/env python3
"""
Recupera àlbums de Picasa Web Albums trencats cercant-los a Google Photos.

Els enllaços antics de picasaweb.google.com redirigeixen a l'Album Archive
(desactivat el 19/07/2023) i donen 404. Cada autor pot executar aquest script
amb el seu propi compte de Google per:

  1. Detectar (collect) els àlbums trencats dels posts, agrupats per compte
     Picasa (ID numèric o nom d'usuari).
  2. Autoritzar el seu compte de Google (OAuth2, loopback local).
  3. Llistar els àlbums del seu Google Photos i cercar el(s) equivalent(s)
     pel nom (normalitzat) i, opcionalment, pel rang de dates de les fotos.
  4. Generar l'enllaç compartible nou (photos.app.goo.gl) si l'àlbum no
     estava compartit, i escriure el mapa de substitució a un JSON.

Ús (per autor):
    python3 scripts/picasa_to_photos.py --collect          # corpus d'àlbums trencats
    python3 scripts/picasa_to_photos.py --token <nom>      # login + cerca + enllaços

Requisits: Python 3.9+. Cap dependència externa (només stdlib).
Cal un OAuth Client ID "Desktop" a Google Cloud Console (veure instruccions).
Els tokens es desen a .tokens/<nom>.json (fora del repo, veure .gitignore).
"""

import argparse
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import webbrowser
from difflib import SequenceMatcher
from http.server import BaseHTTPRequestHandler, HTTPServer

PHOTOS_API = "https://photoslibrary.googleapis.com/v1"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"

SCOPES = (
    "https://www.googleapis.com/auth/photoslibrary.readonly "
    "https://www.googleapis.com/auth/photoslibrary.sharing"
)

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content", "posts")
TOKENS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".tokens")
DEFAULT_OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "picasa-repair-map.json")
DEFAULT_CORPUS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "picasa-broken.json")

PICASA_RE = re.compile(
    r"https?://(?:www\.)?picasaweb\.google\.(?:com|es|it|fr|de|br)"
    r"/([^/?#\s]+)/([^/?#\s]+)",
    re.IGNORECASE,
)


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^0-9a-z]+", " ", s.lower())


def nogap(s):
    return norm(s).replace(" ", "")


def score(a, b):
    na, nb = norm(a), norm(b)
    if na and na == nb:
        return 1.0
    ga, gb = nogap(a), nogap(b)
    if ga and gb:
        if ga == gb:
            return 1.0
        if ga in gb or gb in ga:
            return 0.9
        return max(SequenceMatcher(None, na, nb).ratio(), SequenceMatcher(None, ga, gb).ratio())
    return 0.0


def load_posts():
    posts = []
    for root, _dirs, files in os.walk(CONTENT_DIR):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            full = os.path.join(root, fn)
            posts.append(full)
    return posts


def collect_broken(owners=None):
    """Escaneja els posts i agrupa els àlbums Picasa trencats per compte."""
    broken = {}
    fm_album = re.compile(r"^album_url\s*=\s*[\"'](.+?)[\"']\s*$", re.M)

    def add(url, post, album_field):
        m = PICASA_RE.search(url)
        if not m:
            return
        owner, album_slug = m.group(1), m.group(2)
        if owner.lower() == "lh":
            return  # foto directa d'àlbum, no recuperable per nom
        if owners and owner not in owners:
            return
        key = f"{owner}/{album_slug}"
        e = broken.setdefault(key, {"owner": owner, "album": album_slug, "url": url, "posts": []})
        e["posts"].append({"post": post.replace(CONTENT_DIR + os.sep, ""), "album_field": album_field})

    for post in load_posts():
        text = open(post, encoding="utf-8", errors="replace").read()
        for u in PICASA_RE.findall(text) and PICASA_RE.finditer(text):
            add(u.group(0), post, "body")
        m = fm_album.search(text)
        if m and PICASA_RE.search(m.group(1)):
            add(m.group(1), post, "album_url")
    return broken


def json_load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def json_dump(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def api_call(token, method, path, body=None, params=None):
    url = PHOTOS_API + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def refresh_token(tok):
    form = urllib.parse.urlencode({
        "client_id": tok["client_id"],
        "client_secret": tok["client_secret"],
        "refresh_token": tok["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=form, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode())
    tok["access_token"] = data["access_token"]
    tok["expires_at"] = time.time() + data.get("expires_in", 3600) - 120
    return tok


def saved_token(name):
    path = os.path.join(TOKENS_DIR, f"{name}.json")
    if not os.path.exists(path):
        return None, path
    return json_load(path), path


def save_token(name, tok):
    os.makedirs(TOKENS_DIR, exist_ok=True)
    json_dump(os.path.join(TOKENS_DIR, f"{name}.json"), tok)
    print(f"Token guardat a .tokens/{name}.json")


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.urlparse(self.path)
        if q.path != "/":
            self.send_response(404)
            self.end_headers()
            return
        self.server.result = urllib.parse.parse_qs(q.query)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<html><body><h3>Autenticacio rebuda, torna a la terminal.</h3></body></html>")

    def log_message(self, *args):
        pass


def oauth_authorize(client_id, client_secret):
    srv = HTTPServer(("localhost", 0), _Handler)
    port = srv.server_address[1]
    redirect_uri = f"http://localhost:{port}"
    auth_uri = (AUTH_URL + "?" + urllib.parse.urlencode({
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
    }))
    print("Obre l'enllaç següent i autoritza amb el teu compte de Google:")
    print(auth_uri)
    webbrowser.open(auth_uri)
    srv.handle_request()
    srv.server_close()
    q = getattr(srv, "result", {}) or {}
    if "code" not in q:
        sys.exit("OAuth cancel·lat o amb error: " + q.get("error", ["desconegut"])[0])
    form = urllib.parse.urlencode({
        "code": q["code"][0],
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=form, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode())
    if "access_token" not in data:
        sys.exit("Error bescanviant el codi: " + str(data))
    return {
        "access_token": data["access_token"],
        "refresh_token": data.get("refresh_token"),
        "expires_at": time.time() + data.get("expires_in", 3600) - 120,
        "scope": data.get("scope", ""),
        "client_id": client_id,
        "client_secret": client_secret,
    }


def valid_token(tok):
    return tok.get("access_token") and tok.get("expires_at", 0) > time.time()


def list_albums(token):
    albums, page = [], None
    while True:
        try:
            data = api_call(token, "GET", "/albums", params={"pageSize": 50} | ({"pageToken": page} if page else {}))
        except urllib.error.HTTPError as e:
            if e.code == 401 and token.get("refresh_token"):
                refresh_token(token)
                continue
            raise
        albums.extend(data.get("albums", []))
        page = data.get("nextPageToken")
        if not page:
            return albums, token


def fetch_dates(token, album_id, limit=3):
    try:
        data = api_call(token, "POST", "/mediaItems:search", {"albumId": album_id, "pageSize": limit})
        dates = [i.get("mediaMetadata", {}).get("creationTime", "") for i in data.get("mediaItems", [])]
        return min(dates) if dates else "", max(dates) if dates else ""
    except Exception:
        return "", ""


def share_album(token, album_id):
    data = api_call(token, "POST", f"/albums/{album_id}:share", {})
    return data.get("shareInfo", {}).get("shareableUrl", "")


def date_ok(post_rows, lo, hi):
    if not lo or not hi:
        return ""
    import datetime
    try:
        lo_d = datetime.date.fromisoformat(lo[:10])
        hi_d = datetime.date.fromisoformat(hi[:10])
        post_dates = []
        for p in post_rows:
            m = re.search(r"date:\s*\"?(\d{4}-\d{2}-\d{2})\"?", open(p["post"], encoding="utf8").read())
            if m:
                post_dates.append(datetime.date.fromisoformat(m.group(1)))
        if not post_dates:
            return ""
        pd = min(post_dates)
        span = max((pd - lo_d).days, 0)
        span2 = max((hi_d - pd).days, 0)
        close = "data" if min(span, span2) <= 45 and max(span, span2) <= 120 else "data-far"
        return close
    except Exception:
        return ""


def run_match(corpus, token, name, min_score=0.6, date_check=False, no_share=False, out=None):
    albums, token = list_albums(token)
    print(f"{len(albums)} àlbums al Google Photos del compte autoritzat.")
    save_token(name, token)

    results = []
    cand_by_owner = {}
    for a in albums:
        key = a.get("title") or ""
        cand_by_owner.setdefault(key.replace("/", " "), a)

    for key, e in sorted(corpus.items()):
        post_rows = e["posts"]
        best, best_score = None, 0.0
        for a in albums:
            s = score(e["album"], a.get("title", ""))
            if s > best_score:
                best, best_score = a, s
        verdict = "found" if best_score >= min_score else "not_found"
        entry = {
            "owner": e["owner"], "picasa_title": e["album"], "source_url": e["url"],
            "status": verdict, "score": round(best_score, 3), "posts": len(post_rows),
            "google_title": best.get("title") if best else None,
            "product_url": best.get("productUrl") if best else None,
            "new_url": None,
        }
        if best and verdict == "found":
            date_note = ""
            if date_check:
                lo, hi = fetch_dates(token, best["id"])
                date_note = date_ok(post_rows, lo, hi)
                entry["date_check"] = date_note
            if not no_share:
                entry["new_url"] = share_album(token, best["id"])
        results.append(entry)

    found = sum(1 for r in results if r["status"] == "found")
    print(f"\nTrobats: {found} de {len(results)} àlbums.")

    if out:
        json_dump(out, {"file": out, "count": len(results), "found": found, "results": results})
        print(f"Mapa escrit a {out}")

    print("\n--- Resum dels 25 primers ---")
    for r in results[:25]:
        print(f"[{r['status']:>9}] {r['owner']}/{r['picasa_title']}  ->  {r['google_title'] or ''}  ({r['score']}) {r.get('date_check') or ''} {r.get('new_url') or r.get('product_url') or ''}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--collect", action="store_true", help="només: detecta àlbums Picasa trencats i els agrupa per compte")
    ap.add_argument("--corpus", default=DEFAULT_CORPUS, help="JSON amb el corpus d'àlbums trencats (per defecte data/picasa-broken.json)")
    ap.add_argument("--output", default=DEFAULT_OUT, help="JSON de sortida amb el mapa de substitució")
    ap.add_argument("--owners", nargs="*", help="limita als comptes Picasa indicats per id o nom")
    ap.add_argument("--token", default="default", help="nom del fitxer de token a .tokens/ (per autor)")
    ap.add_argument("--client-id", help="OAuth Client ID (alternativa a l'env GOOGLE_PHOTOS_CLIENT_ID)")
    ap.add_argument("--client-secret", help="OAuth Client Secret (alternativa a l'env GOOGLE_PHOTOS_CLIENT_SECRET)")
    ap.add_argument("--min-score", type=float, default=0.6, help="llindar de coincidència de nom (0-1)")
    ap.add_argument("--date-check", action="store_true", help="comprova el rang de dates de les fotos de l'àlbum vs el post")
    ap.add_argument("--no-share", action="store_true", help="no genera l'enllaç compartit; només deixa productUrl")
    args = ap.parse_args()

    if args.collect:
        broken = collect_broken(args.owners)
        json_dump(args.corpus, {"count": len(broken), "albums": broken})
        print(f"{len(broken)} àlbums Picasa trencats únics -> {args.corpus}")
        if args.owners:
            print("Filtrats als comptes:", ", ".join(args.owners))
        return 0

    corpus = json_load(args.corpus).get("albums", {})
    if args.owners:
        corpus = {k: v for k, v in corpus.items() if v["owner"] in args.owners}

    tok, path = saved_token(args.token)
    if tok and not valid_token(tok) and tok.get("refresh_token"):
        try:
            tok = refresh_token(tok)
        except urllib.error.HTTPError as e:
            print(f"Token caduc i refresh fallat ({e.code}); cal autenticar-se de nou.")
            tok = None
    if not tok:
        cid = args.client_id or os.environ.get("GOOGLE_PHOTOS_CLIENT_ID")
        csec = args.client_secret or os.environ.get("GOOGLE_PHOTOS_CLIENT_SECRET")
        if not cid or not csec:
            print("Falten credencials. Crea un OAuth Client ID de tipus 'Desktop' a "
                  "https://console.cloud.google.com/apis/credentials i passa-les amb "
                  "--client-id / --client-secret o amb les variables d'entorn "
                  "GOOGLE_PHOTOS_CLIENT_ID / GOOGLE_PHOTOS_CLIENT_SECRET.", file=sys.stderr)
            return 1
        tok = oauth_authorize(cid, csec)

    run_match(corpus, tok, args.token, args.min_score, args.date_check, args.no_share, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
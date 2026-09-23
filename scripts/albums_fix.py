#!/usr/bin/env python3
"""albums_fix.py — verificar i arreglar els enllaços d'àlbums Picasa/Google Photos.

La recuperació és assistida (per autor): l'API de Google Photos és morta
(scopes retirats el 31/03/2025), així que només l'autor pot generar l'enllaç
compartible nou. Aquesta eina prepara el corpus, els fulls de treball, valida
els enllaços nous i aplica els canvis.

Subcomandes:

  collect   Escaneja content/posts → data/picasa-broken.json
            (corpus agrupat per compte Picasa: àlbums, posts que els referencien)
  sheets    Llegeix el corpus → drafts/candidats/<membre>.md per a cada autor
  fitxes    Genera recuperacio/<membre>/*.yml (una fitxa per àlbum)
            perquè cada autor els corregeixi des del CMS
  recull    Llegeix les fitxes desades → data/links-nous.json (old → new)
  validate  Comprova status HTTP i títol públic dels enllaços nous
  apply     Aplica un mapa «URL antiga → URL nova» al front matter i al cos

Formats de fitxer:

  data/links-nous.json   (entrada per a validate/apply)
    { "<membre>": [ {"old": "<url>", "new": "<url>"}, ... ] }

  data/links-validats.json  (sortida de validate)
    = links-nous.json amb status/title afegits a cada element

Ús:

  scripts/albums_fix.py collect
  scripts/albums_fix.py sheets
  scripts/albums_fix.py fitxes
  scripts/albums_fix.py recull
  scripts/albums_fix.py validate --file data/links-nous.json
  scripts/albums_fix.py apply --file data/links-nous.json --dry-run
  scripts/albums_fix.py apply --file data/links-nous.json --write

Només estàndard de Python; sense dependències de tercers.
"""

import argparse
import html
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content", "posts")
CORPUS = os.path.join(ROOT, "data", "picasa-broken.json")
CANDIDATS = os.path.join(ROOT, "drafts", "candidats")
RECUPERACIO = os.path.join(ROOT, "recuperacio")
SITE_URL = "https://9barrisimatge.org"

PICASA_RE = re.compile(
    r"https?://(?:www\.)?picasaweb\.google\.(?:com|es|it|fr|de|br)/([^/?#\s]+)/([^/?#\s]+)",
    re.IGNORECASE,
)
URL_TOKEN_RE = re.compile(
    r"https?://(?:www\.)?picasaweb\.google\.(?:com|es|it|fr|de|br)/[^)\s>]+",
    re.IGNORECASE,
)

# Compte Picasa → membre (atribució de drafts/informe-links-trencats.md, 2026-09-19).
# Els comptes sense membre (None) queden a la llista «sense membre assignat».
ACCOUNT_MEMBERS = {
    "103138221614479310970": "Joan \"Linux\" Martínez i Serres",
    "linuxbcn": "Joan \"Linux\" Martínez i Serres",
    "115791131166530059320": "Pedro Click",
    "Perdo.Garcia": "Pedro Click",
    "pdro.gracias": "Pedro Click",
    "110015855395179205688": "9 Barris Imatge",
    "116805523004990742624": "9 Barris Imatge",
    "104199960646572363843": "9 Barris Imatge",
    "115452009915421757608": "9 Barris Imatge",
    "inmalcario": "9 Barris Imatge",
    "jaime14bf": "9 Barris Imatge",
    "14birras": "9 Barris Imatge",
    "danigcaballero": "9 Barris Imatge",
    "gtitan": "9 Barris Imatge",
    "101546608348756835393": "9 Barris Imatge",
    "115837747848659272017": "9 Barris Imatge",
    "111777199791376723749": "9 Barris Imatge",
    "104952335506567568674": "9 Barris Imatge",
    "Ignasi9b": "9 Barris Imatge",
    "100268695753733554853": "Manel Sala \"Ulls\" Circ",
    "ulls2006": "Manel Sala \"Ulls\" Circ",
    "ulls1963": "Manel Sala \"Ulls\" Circ",
    "114858497713897843587": "Pedro \"Casal\" Cervera",
    "pedro.cervera": "Pedro \"Casal\" Cervera",
    "111964096227458093905": "Alberto Sanagustín",
    "102149297277529522464": "Manel Villalba",
    "nico9barrisimarge": "Nico YeYe",
    "fotospigmeos": None,  # 9 Barris Imatge? Pendent de confirmar
    "salvadorbayo": None,  # associat a Joan? Pendent de confirmar
    "trobadaalternativa9barris": None,  # compte col·lectiu, del casal?
    "108654039305170515016": None,  # ambigu (Joan ×1 / 9BI ×3) → confirmar
}


def front_matter(text):
    """Retorna (meta, body). meta = dict de claus simples del front matter."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([\w-]+)\s*:\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip("\"'")
    return fm, text[end + 4 :]


def clean_url(url):
    """Treu el protocol, `www.` i la query per comparar iguals."""
    m = re.match(r"https?://(?:www\.)?([^/?#]+)(/[^?#]*)?", url or "", re.I)
    if not m:
        return url or ""
    return (m.group(1) + m.group(2)).rstrip("/")


def slugify(name):
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("'", "").replace('"', "")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def humanize(album):
    """Nom llegible suggerit a partir del slug de l'àlbum (p. ex. ProspeBeach2013)."""
    words = re.split(r"([A-Z][a-z0-9]+|[A-Z]+(?=[A-Z][a-z])|\d+)", album)
    words = [w for w in words if w]
    out = []
    for w in words:
        if w.isdigit():
            out.append(w)
        elif w.isupper() and len(w) > 1:
            out.append(w.title())
        else:
            out.append(w[0].upper() + w[1:])
    return " ".join(out) or album


def iter_posts():
    for root, _dirs, files in os.walk(CONTENT):
        for fn in sorted(files):
            if fn.endswith(".md"):
                yield os.path.relpath(os.path.join(root, fn), ROOT)


def collect():
    accounts = defaultdict(lambda: {"albums": {}, "n_album_url": 0, "n_body": 0})
    no_picasa = []
    lh_single = 0
    t_album = t_body = 0

    for rel in iter_posts():
        text = open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace").read()
        meta, body = front_matter(text)
        date = meta.get("date", "")[:10]
        title = meta.get("title", "")
        slug = meta.get("slug", "")
        url = f"{SITE_URL}/{date[:4]}/{date[5:7]}/{slug}.html" if date and slug else ""

        # Front matter album_url
        au = meta.get("album_url")
        if au:
            t_album += 1
            m = PICASA_RE.search(au)
            if m and m.group(1).lower() != "lh":
                acc = accounts[m.group(1)]
                alb = m.group(2)
                a = acc["albums"].setdefault(
                    alb,
                    {
                        "url": au,
                        "url_clean": f"https://picasaweb.google.com/{m.group(1)}/{alb}",
                        "first_seen": rel,
                        "posts": [],
                    },
                )
                a["posts"].append(
                    {
                        "file": rel,
                        "field": "album_url",
                        "date": date,
                        "title": title,
                        "url": url,
                    }
                )
                acc["n_album_url"] += 1
            elif m:
                lh_single += 1
            else:
                no_picasa.append({"url": au, "field": "album_url", "posts": [rel]})

        # Cos del post
        for mt in URL_TOKEN_RE.finditer(body):
            m = PICASA_RE.search(mt.group(0))
            t_body += 1
            if not m or m.group(1).lower() == "lh":
                if m:
                    lh_single += 1
                continue
            acc = accounts[m.group(1)]
            alb = m.group(2)
            a = acc["albums"].setdefault(
                alb,
                {
                    "url": mt.group(0),
                    "url_clean": f"https://picasaweb.google.com/{m.group(1)}/{alb}",
                    "first_seen": rel,
                    "posts": [],
                },
            )
            a["posts"].append(
                {
                    "file": rel,
                    "field": "body",
                    "date": date,
                    "title": title,
                    "url": url,
                }
            )
            acc["n_body"] += 1

    # membre per compte: derivar del compte (ja que member depèn del compte, produir-lo bé)
    for owner, acc in accounts.items():
        acc["member"] = ACCOUNT_MEMBERS.get(owner)
        unauth = Counter(p["field"] for a in acc["albums"].values() for p in a["posts"])
        acc["n_album_url"] = int(unauth.get("album_url", 0))
        acc["n_body"] = int(unauth.get("body", 0))
        for a in acc["albums"].values():
            a["posts"].sort(key=lambda p: (p["date"], p["file"]))
            a["count"] = {"album_url": sum(1 for p in a["posts"] if p["field"] == "album_url"),
                          "body": sum(1 for p in a["posts"] if p["field"] == "body")}

    total_albums = sum(len(a["albums"]) for a in accounts.values())
    total_refs = sum(a["n_album_url"] + a["n_body"] for a in accounts.values())
    corpus = {
        "generated": datetime.now().strftime("%Y-%m-%d"),
        "source": "content/posts",
        "stats": {
            "accounts": len(accounts),
            "albums": total_albums,
            "references": total_refs,
            "album_url_checked": t_album,
            "body_urls": t_body,
            "lh_single_photos": lh_single,
            "no_picasa_album_url": len(no_picasa),
        },
        "accounts": accounts,
        "no_picasa": no_picasa,
    }

    os.makedirs(os.path.dirname(CORPUS), exist_ok=True)
    with open(CORPUS, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
    print(json.dumps(corpus["stats"], ensure_ascii=False, indent=2))
    print(f"\nEscrit: {CORPUS}")

    sin = sorted(o for o, a in accounts.items() if not a["member"])
    if sin:
        print("\nComptes SENSE membre assignat (revisar):")
        for o in sin:
            print(f"  {o}  ({len(accounts[o]['albums'])} àlbums)")


def sheet_for(member, albums, unassigned=False):
    title = "9 Barris Imatge (compte genèric)" if member == "9 Barris Imatge" else member
    lines = [
        f"# Recuperació d'àlbums — {title}",
        "",
        "Els enllaços següents (àlbums Picasa) han quedat trencats en tancar Picasa Web.",
        "**Com es recupera:** obre un àlbum equivalent al teu Google Photos i genera un",
        "enllaç compartible (Comparteix → Crea un enllaç). Posa'l a la columna «Enllaç nou»",
        "i torna el fitxer, o bé envia'ls a info@9barrisimatge.org.",
        "",
        "| # | Àlbum (suggerit) | Any aprox. | Posts (àlbum) | Exemple al web | Enllaç antic | Enllaç nou |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, (album, data) in enumerate(sorted(albums, key=lambda kv: (kv[1]["posts"][0]["date"], kv[0])), 1):
        dates = [p["date"] for p in data["posts"] if p["date"]]
        first = data["posts"][0]
        example = f"[{first['date']}]({first['url']})" if first["url"] else first["file"]
        year = dates[0][:4] if dates else ""
        n = data["count"]["album_url"]
        n_body = data["count"]["body"]
        posts_n = str(n) if n else f"— ({n_body} al cos)"
        lines.append(
            f"| {i} | {humanize(album)} | {year} | {posts_n} | {example} "
            f"| `{data['url_clean']}` |  |"
        )
    if unassigned:
        lines.insert(1, "")
        lines.insert(2, "> **Pendent de confirmar**: quina membre/entitat és la propietària d'aquest compte.")
        lines.insert(3, "")
    lines.append("")
    return "\n".join(lines)


def sheets():
    corpus = json.load(open(CORPUS, encoding="utf-8"))
    by_member = defaultdict(list)
    unassigned = []
    for owner, acc in corpus["accounts"].items():
        member = acc["member"]
        dest = by_member[member] if member else unassigned
        for album, data in acc["albums"].items():
            dest.append((album, data))

    os.makedirs(CANDIDATS, exist_ok=True)
    written = []
    for member, albums in sorted(by_member.items(), key=lambda kv: kv[0] or "zzz"):
        path = os.path.join(CANDIDATS, f"{slugify(member)}.md")
        open(path, "w", encoding="utf-8").write(sheet_for(member, albums))
        written.append(path)
        print(f"  {path}  ({len(albums)} àlbums)")

    if unassigned:
        path = os.path.join(CANDIDATS, "00-compte-sense-membre.md")
        open(path, "w", encoding="utf-8").write(sheet_for("compte sense membre", unassigned, unassigned=True))
        written.append(path)
        print(f"  {path}  ({len(unassigned)} àlbums, SENSE MEMBRE)")

    print(f"\nFulls de treball generats a {CANDIDATS}/")


def _http(url, timeout):
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (9bi albums_fix)"}
    )
    opener = urllib.request.build_opener(
        urllib.request.HTTPRedirectHandler()
    )
    with opener.open(req, timeout=timeout) as resp:
        status = resp.status
        final = resp.geturl()
        body = resp.read(200_000).decode("utf-8", "ignore")
    title = ""
    m = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
    if m:
        title = html.unescape(m.group(1)).strip().replace("\n", " ")
    return {"status": status, "final": final, "title": title}


def validate(args):
    data = json.load(open(args.file, encoding="utf-8"))
    out = {}
    for member, items in data.items():
        out[member] = []
        for it in items:
            print(f"· {it['new']} ...", end=" ", flush=True)
            try:
                r = _http(it["new"], args.timeout)
                print(f"{r['status']} «{r['title'][:60]}»")
            except urllib.error.HTTPError as e:
                r = {"status": e.code, "final": e.geturl() or "", "title": ""}
                print(f"HTTP {e.code}")
            except Exception as e:  # noqa: BLE001
                r = {"status": 0, "final": "", "title": ""}
                print(f"ERROR {type(e).__name__}: {e}")
            it = dict(it)
            it.update(r)
            out[member].append(it)
            time.sleep(args.pause)
    dest = args.output or os.path.join(ROOT, "data", "links-validats.json")
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\nValidacions escrites a {dest}")


def load_map(path):
    """links-nous.json → {old_clean: {old, new, member}}"""
    data = json.load(open(path, encoding="utf-8"))
    m = {}
    for _member, items in data.items():
        for it in items:
            m[clean_url(it["old"])] = it
    return m


def apply(args):
    repl = load_map(args.file)
    if not repl:
        print("El mapa és buit.")
        return
    affected = []

    for rel in iter_posts():
        path = os.path.join(ROOT, rel)
        text = open(path, encoding="utf-8", errors="replace").read()
        orig = text
        meta, _body = front_matter(text)
        per_file = Counter()

        # front matter album_url
        if meta.get("album_url"):
            cu = clean_url(meta["album_url"])
            if cu in repl:
                text = re.sub(
                    r"^(album_url:\s*).+?(\s*)$",
                    lambda mm: mm.group(1) + repl[cu]["new"] + mm.group(2),
                    text,
                    count=1,
                    flags=re.M,
                )
                per_file["album_url"] += 1

        # cos: reemplaça qualsevol token picasa que coincideixi amb una clau del mapa
        def _sub(mt):
            cu = clean_url(mt.group(0))
            it = repl.get(cu)
            if it:
                per_file["body"] += 1
                return it["new"]
            return mt.group(0)

        text = URL_TOKEN_RE.sub(_sub, text)

        if text != orig:
            affected.append((rel, dict(per_file) or {"body": 0}))
            if args.write:
                open(path, "w", encoding="utf-8").write(text)

    totals = Counter()
    for _rel, c in affected:
        totals.update(c)
    if args.json:
        print(json.dumps({"files": affected, "totals": dict(totals)}, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(dict(totals), ensure_ascii=False))
        print(f"\nFitxers afectats: {len(affected)}")
        for rel, c in affected:
            print(f"  {rel}: {dict(c)}")
    if not args.write:
        print("\n(DRY RUN: cap fitxer modificat; cal --write)")


def _cover_of(rel):
    """Retorna l'URL de portada (cover.image) d'un post, o '' si no en té."""
    try:
        text = open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace").read()
    except OSError:
        return ""
    m = re.search(r"^cover:\s*$([\s\S]*?)^\S", text, re.M)
    if not m:
        return ""
    m2 = re.search(r"^\s+image:\s*(.+?)\s*$", m.group(1), re.M)
    if m2:
        return m2.group(1).strip().strip("\"'")
    return ""


def _dump_fitxa(fitxa):
    """Fitxa en markdown: front matter YAML pla + cos amb la foto de mostra.

    El cos en markdown fa que Sveltia RENDERITZI la imatge al panell de
    preview (un camp string només mostraria el text de l'URL).
    """
    lines = ["---"]
    for k, v in fitxa.items():
        lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    foto = fitxa.get("foto", "")
    body = f"**Foto de mostra** (per identificar l'àlbum):\n\n![Foto de mostra]({foto})\n" if foto else ""
    body += "\n> Obriu l'àlbum equivalent al vostre Google Photos, genereu l'enllaç\n" \
            "> compartible (Comparteix → Crea un enllaç) i enganxeu-lo al camp\n" \
            "> **«Enllaç nou»** d'abaix.\n"
    return "\n".join(lines) + "\n---\n\n" + body


def fitxes():
    """Genera una fitxa YAML per àlbum a recuperacio/<membre>/.

    Cada fitxa = un àlbum Picasa trencat que l'autor ha de corregir al CMS.
    El nom de carpeta (slug del membre) és la carpeta de la collection Sveltia,
    així cada autor veu només els seus àlbums sense cap filtre extra.
    """
    corpus = json.load(open(CORPUS, encoding="utf-8"))
    by_member = defaultdict(list)
    for owner, acc in corpus["accounts"].items():
        member = acc["member"]
        if not member:
            continue  # sense membre assignat → es queda al full de treball
        for album, data in acc["albums"].items():
            by_member[member].append((album, data))

    os.makedirs(RECUPERACIO, exist_ok=True)
    for member, items in sorted(by_member.items(), key=lambda kv: kv[0]):
        folder = os.path.join(RECUPERACIO, slugify(member))
        os.makedirs(folder, exist_ok=True)
        items.sort(key=lambda kv: (kv[1]["posts"][0]["date"], kv[0]))
        n = 0
        for album, data in items:
            dates = [p["date"] for p in data["posts"] if p["date"]]
            year = dates[0][:4] if dates else ""
            first = data["posts"][0]
            fitxa = {
                "autor": member,
                "album": humanize(album),
                "any": year,
                "foto": _cover_of(first["file"]),
                "url_antiga": data["url_clean"],
                "url_nova": "",
                "posts": len(data["posts"]),
                "exemple": first["url"] if first["url"] else first["file"],
            }
            name = f"{dates[0] if dates else '0000'}-{slugify(album)}.md"
            open(os.path.join(folder, name), "w", encoding="utf-8").write(_dump_fitxa(fitxa))
            n += 1
        print(f"  {member}: {n} fitxes → recuperacio/{slugify(member)}/")
    print(f"\nFitxes generades a {RECUPERACIO}/")


def recull():
    """Llegeix les fitxes desades i aplega old → new a data/links-nous.json.

    L'autor es deriva de la CARPETA (recuperacio/<slug>/), no del camp
    «autor» del fitxer: així un error de l'autor en editar-lo no trenca
    l'agrupació. El camp «autor» es conserva al fitxer per a llegir-lo a mà.
    """
    slug_to_member = {}
    for member in {m for m in ACCOUNT_MEMBERS.values() if m}:
        slug_to_member[slugify(member)] = member

    out = defaultdict(list)
    n = 0
    for folder_name in sorted(os.listdir(RECUPERACIO)):
        folder = os.path.join(RECUPERACIO, folder_name)
        if not os.path.isdir(folder):
            continue
        member = slug_to_member.get(folder_name)
        if not member:
            print(f"  [!] carpeta desconeguda, es Salta: {folder_name}")
            continue
        for fn in sorted(os.listdir(folder)):
            if not fn.endswith(".md"):
                continue
            text = open(os.path.join(folder, fn), encoding="utf-8", errors="replace").read()
            meta, _ = front_matter(text)
            nova = (meta.get("url_nova") or "").strip()
            antiga = (meta.get("url_antiga") or "").strip()
            if nova and nova != antiga and antiga:
                out[member].append({"old": antiga, "new": nova})
                n += 1

    path = os.path.join(ROOT, "data", "links-nous.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dict(out), f, ensure_ascii=False, indent=2)
    print(f"Recollits {n} enllaços nous de {len(out)} autors → {path}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("collect", help="genera data/picasa-broken.json")

    sub.add_parser("sheets", help="genera drafts/candidats/<membre>.md")

    sub.add_parser("fitxes", help="genera recuperacio/<membre>/*.yml per al CMS")

    sub.add_parser("recull", help="llegeix les fitxes → data/links-nous.json")

    v = sub.add_parser("validate", help="comprova els enllaços nous")
    v.add_argument("--file", default=os.path.join(ROOT, "data", "links-nous.json"))
    v.add_argument("--output", default=None)
    v.add_argument("--timeout", type=int, default=30)
    v.add_argument("--pause", type=float, default=0.3)

    a = sub.add_parser("apply", help="aplica URL antiga → nova")
    a.add_argument("--file", default=os.path.join(ROOT, "data", "links-nous.json"))
    a.add_argument("--write", action="store_true", help="escriu els canvis (per defecte dry-run)")
    a.add_argument("--json", action="store_true")

    args = p.parse_args()
    if args.cmd == "collect":
        collect()
    elif args.cmd == "sheets":
        sheets()
    elif args.cmd == "fitxes":
        fitxes()
    elif args.cmd == "recull":
        recull()
    elif args.cmd == "validate":
        validate(args)
    elif args.cmd == "apply":
        apply(args)


if __name__ == "__main__":
    main()
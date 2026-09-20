#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recupera_autors_blogger.py v2 — Recupera l'autor real dels posts amb autor genèric.

PER QUÈ EXISTEIX
    De 3.006 posts migrats de Blogger→Hugo, 473 van quedar amb l'autor genèric
    «9 Barris Imatge». La causa: la migració mapejava per <author><uri> (profile
    ID de Google), i quan l'URI no estava al mapa o era absent, el post queia al
    genèric. Però Blogger SEMPRE té l'autor real — aquí el recuperem amb 3 fonts.

FONTS EN CASCADA
    A) Feed JSON de Blogger (en directe, cacheable a /tmp/)
    B) XML export oficial de Blogger (fitxer local, --xml FITXER)
    C) Scraping HTML del blog públic www.9barrisimatge.org (--scrape)

    Per cada post genèric: prova A → si dóna "Unknown"/buit → prova B → si
    tampoc → prova C (si activat). El que queda sense resoldre va al CSV.

ÚS
    python3 scripts/recupera_autors_blogger.py                      # informe
    python3 scripts/recupera_autors_blogger.py --xml export.xml     # + font B
    python3 scripts/recupera_autors_blogger.py --scrape             # + font C
    python3 scripts/recupera_autors_blogger.py --apply              # aplica canvis
    python3 scripts/recupera_autors_blogger.py --csv autors.csv     # exporta CSV
    python3 scripts/recupera_autors_blogger.py --clean-feed         # nova descàrrega

REQUISITS
    Python 3.9+ (stdlib). Cap dependència de tercers.
"""
from __future__ import annotations

import csv
import glob
import html
import json
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

# ── Rutes ────────────────────────────────────────────────────────────────────
WEB = "/Users/joan/Documents/Obsidian/9arrisimatge.org"
POSTS_DIR = os.path.join(WEB, "content", "posts")
CACHE_FEED = "/tmp/blogger_feed_9bi.json"
BACKUP_DIR = "/tmp/backup_autors_9bi"

# ── Blogger ───────────────────────────────────────────────────────────────────
BLOGID = "8034150767456238983"
FEED_JSON = f"https://www.blogger.com/feeds/{BLOGID}/posts/default"
BLOG_PUBLIC = "https://www.9barrisimatge.org"
UA = "Mozilla/5.0 (compatible; 9bi-autors/2.0; +https://9barrisimatge.org)"
ATOM_NS = "{http://www.w3.org/2005/Atom}"
BLOGGER_NS = "{http://schemas.google.com/blogger/2018}"

# ── Autor genèric (el que volem substituir) ───────────────────────────────────
AUTHOR_GENERIC = "9 Barris Imatge"

# Noms que al feed signifiquen «sense autor real»
UNKNOWN_NAMES = {"unknown", "anonymous", "unknown user", "anònim", "anònim/a",
                 "nou barris imatge", "9 barris imatge", ""}

# ── Mapa de normalització: nom brut del feed (lowercase) → membre canònic ────
# Cobreix variacions de noms i pseudònims que poden aparèixer al feed.
NAME_MAP: dict[str, str] = {
    # Joan Linux
    "joan martinez i serres":        'Joan "Linux" Martínez i Serres',
    "joan martínez i serres":        'Joan "Linux" Martínez i Serres',
    "joan martinez":                 'Joan "Linux" Martínez i Serres',
    "linuxbcn":                      'Joan "Linux" Martínez i Serres',
    # Pedro Click
    "predroclick":                   "Pedro Click",
    "pedro click":                   "Pedro Click",
    "pedroclick":                    "Pedro Click",
    "pedro garcia":                  "Pedro Click",
    # Manel Sala «Ulls»
    'manel sala "ulls" circ':        'Manel Sala "Ulls" Circ',
    "manel sala ulls":               'Manel Sala "Ulls" Circ',
    "manel sala":                    'Manel Sala "Ulls" Circ',
    "ulls":                          'Manel Sala "Ulls" Circ',
    # Francesc Barbe
    "francesc barbe":                "Francesc Barbe",
    # Ismael Utrilla
    "ismaelug":                      "Ismael Utrilla",
    "ismael utrilla":                "Ismael Utrilla",
    "ismael":                        "Ismael Utrilla",
    # Alberto Sanagustín
    "alberto":                       "Alberto Sanagustín",
    "alberto sanagustín":            "Alberto Sanagustín",
    "alberto sanagustin":            "Alberto Sanagustín",
    # Iozsef Kiss
    "iozsef kiss":                   "Iozsef Kiss",
    # Pedro Casal
    "pedrocasal":                    'Pedro "Casal" Cervera',
    "pedro casal":                   'Pedro "Casal" Cervera',
    "pedro cervera":                 'Pedro "Casal" Cervera',
    # Núria Laura Orbaneja
    "núria laura orbaneja":          "Núria Laura Orbaneja",
    "nuria laura orbaneja":          "Núria Laura Orbaneja",
    "núria":                         "Núria Laura Orbaneja",
    "nuria":                         "Núria Laura Orbaneja",
    # Manel Villalba
    "manel villalba":                "Manel Villalba",
    # Nico YeYe
    "nico yeye":                     "Nico YeYe",
    "nico derocal":                  "Nico YeYe",
    # Juan Carlos Molina
    "gris medio,casi negro":         "Juan Carlos Molina (Grismedio Casinegro)",
    "grismedio casinegro":           "Juan Carlos Molina (Grismedio Casinegro)",
    "juan carlos molina":            "Juan Carlos Molina (Grismedio Casinegro)",
}


# ─────────────────────────────────────────────────────────────────────────────
# Utilitats
# ─────────────────────────────────────────────────────────────────────────────

def slugify(t: str) -> str:
    t = t.lower()
    t = re.sub(r"[^a-z0-9à-ÿ]+", "-", t)
    return t.strip("-")


def normalitza(nom: str) -> str | None:
    """Retorna el nom canònic del membre, o None si és un Unknown real."""
    k = nom.strip().lower()
    if k in UNKNOWN_NAMES:
        return None
    return NAME_MAP.get(k, nom.strip() or None)


def es_unknown(nom: str) -> bool:
    return not nom or nom.strip().lower() in UNKNOWN_NAMES


def http_get(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for intent in range(5):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except (urllib.error.HTTPError, urllib.error.URLError,
                TimeoutError, OSError) as e:
            if intent == 4:
                raise
            espera = 2 ** (intent + 1)
            print(f"    (HTTP {e} → reintent en {espera}s)", file=sys.stderr)
            time.sleep(espera)
    raise RuntimeError(f"no s'ha pogut descarregar {url}")


# ─────────────────────────────────────────────────────────────────────────────
# Font A: Feed JSON de Blogger
# ─────────────────────────────────────────────────────────────────────────────

def descarrega_feed(forca: bool = False) -> list[dict]:
    if not forca and os.path.isfile(CACHE_FEED):
        print(f"    feed: carregant cache ({CACHE_FEED})", file=sys.stderr)
        with open(CACHE_FEED, encoding="utf-8") as f:
            return json.load(f)

    entries: list[dict] = []
    start = 1
    total = None
    while True:
        qs = urllib.parse.urlencode(
            {"alt": "json", "max-results": "150", "start-index": str(start)}
        )
        doc = json.loads(http_get(f"{FEED_JSON}?{qs}"))
        feed = doc.get("feed", {})
        if total is None:
            total = int(feed.get("openSearch$totalResults", {}).get("$t", "0"))
            print(f"    Blogger: {total} entrades en total", file=sys.stderr)
        nous = feed.get("entry", [])
        if not nous:
            break
        entries.extend(nous)
        start += 150
        if start > total:
            break
        time.sleep(0.35)

    with open(CACHE_FEED, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False)
    print(f"    feed cachejat: {len(entries)} entrades", file=sys.stderr)
    return entries


def index_de_feed(entries: list[dict]) -> dict[str, str]:
    """(data|slug-títol) → nom d'autor (brut, tal com ve del feed)."""
    idx: dict[str, str] = {}
    for e in entries:
        title = (e.get("title") or {}).get("$t", "")
        published = (e.get("published") or {}).get("$t", "")[:10]
        autors = e.get("author") or []
        if not autors:
            continue
        name = (autors[0].get("name") or {}).get("$t", "")
        key = f"{published}|{slugify(title)}"
        idx.setdefault(key, name)
    return idx


# ─────────────────────────────────────────────────────────────────────────────
# Font B: XML export oficial de Blogger
# ─────────────────────────────────────────────────────────────────────────────

def index_de_xml(xml_path: str) -> dict[str, str]:
    """Parseja l'export XML de Blogger. (data|slug-títol) → nom d'autor."""
    idx: dict[str, str] = {}
    try:
        tree = ET.parse(xml_path)
    except ET.ParseError as e:
        print(f"    ERROR parsejant XML: {e}", file=sys.stderr)
        return idx

    root = tree.getroot()
    for entry in root.findall(f"{ATOM_NS}entry"):
        # Filtra: només posts (no pàgines ni comentaris).
        # Suporta dos formats:
        #   - Classic Atom API: <category term="...kind#post">
        #   - Google Takeout 2018: <blogger:type>POST</blogger:type>
        tipo_blogger = entry.findtext(f"{BLOGGER_NS}type", "")
        kind_via_cat = any(
            "kind#post" in c.get("term", "")
            for c in entry.findall(f"{ATOM_NS}category")
        )
        if tipo_blogger not in ("POST", "") and not kind_via_cat:
            continue
        if tipo_blogger and tipo_blogger != "POST":
            continue

        title = entry.findtext(f"{ATOM_NS}title", "")
        published = (entry.findtext(f"{ATOM_NS}published", "") or "")[:10]
        author_el = entry.find(f"{ATOM_NS}author")
        name = ""
        if author_el is not None:
            name = author_el.findtext(f"{ATOM_NS}name", "") or ""

        if published and title:
            key = f"{published}|{slugify(title)}"
            idx.setdefault(key, name)

    print(f"    XML: {len(idx)} posts indexats", file=sys.stderr)
    return idx


# ─────────────────────────────────────────────────────────────────────────────
# Font C: Scraping HTML del blog públic
# ─────────────────────────────────────────────────────────────────────────────

# El bloc d'autor a Blogger usa schema.org/Person amb itemprop='author'.
# Busquem el nom i el profile_id dins d'aquest bloc per evitar capturar el títol del post.
_PAT_AUTHOR_NOM = re.compile(
    r"itemprop=['\"]author['\"].*?itemprop=['\"]name['\"][^>]*>([^<]+)<",
    re.S | re.I,
)
_PAT_AUTHOR_PID = re.compile(
    r"itemprop=['\"]author['\"].*?blogger\.com/profile/(\d+)",
    re.S | re.I,
)
# Fallbacks per a plantilles antigues de Blogger (pre-schema.org)
_PAT_FALLBACKS = [
    re.compile(r"class=['\"][^'\"]*\bfn\b[^'\"]*['\"][^>]*>([^<]+)<", re.I),
    re.compile(r"class=['\"]post-author-name['\"][^>]*>([^<]+)<", re.I),
    re.compile(r"rel=['\"]author['\"][^>]*>([^<]+)<", re.I),
]


def autor_de_html(date_str: str, slug: str) -> tuple[str | None, str | None]:
    """Scraping del blog públic.
    Retorna (nom_autor, profile_id) o (None, None) si no es troba.
    """
    try:
        pub = date_str[:10]
        any_, mes = pub[:4], pub[5:7]
        url = f"{BLOG_PUBLIC}/{any_}/{mes}/{slug}.html"
        body = http_get(url, timeout=20)
        body = html.unescape(body)

        nom = None
        m = _PAT_AUTHOR_NOM.search(body)
        if m:
            nom = m.group(1).strip()
        else:
            for pat in _PAT_FALLBACKS:
                m2 = pat.search(body)
                if m2:
                    nom = m2.group(1).strip()
                    break

        pid = None
        mp = _PAT_AUTHOR_PID.search(body)
        if mp:
            pid = mp.group(1)

        if nom and nom.lower() not in UNKNOWN_NAMES:
            return nom, pid
    except Exception as e:
        print(f"    (scraping {slug}: {e})", file=sys.stderr)
    return None, None


# ─────────────────────────────────────────────────────────────────────────────
# Posts locals amb autor genèric
# ─────────────────────────────────────────────────────────────────────────────

def posts_locals_generic() -> list[dict]:
    """Retorna els posts locals que porten l'autor genèric."""
    out = []
    for p in sorted(glob.glob(os.path.join(POSTS_DIR, "*", "*.md"))):
        raw = open(p, encoding="utf-8").read()
        m = re.search(r"^---\n(.*?)\n---", raw, re.S)
        if not m:
            continue
        fm = m.group(1)

        def camp(k: str) -> str:
            mm = re.search(rf"^{k}:\s*(.*?)\s*$", fm, re.M)
            return mm.group(1).strip().strip("'\"") if mm else ""

        # Recollim NOMÉS els posts amb l'autor genèric (fix del bug original)
        if camp("author") != AUTHOR_GENERIC:
            continue

        out.append({
            "path": p,
            "title": camp("title"),
            "date": camp("date"),
            "slug": camp("slug"),
        })
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Motor principal
# ─────────────────────────────────────────────────────────────────────────────

def processa(locals_g: list[dict],
             idx_a: dict[str, str],
             idx_b: dict[str, str],
             do_scrape: bool) -> list[dict]:
    """Creua cada post genèric amb les tres fonts. Retorna llista de resultats."""
    resultats = []
    for post in locals_g:
        key = f"{post['date'][:10]}|{slugify(post['title'])}"

        # Font A
        nom_a = idx_a.get(key, "")
        font = "A" if nom_a and not es_unknown(nom_a) else ""
        nom_brut = nom_a

        # Font B (si A no resol)
        nom_b = ""
        if not font and idx_b:
            nom_b = idx_b.get(key, "")
            if nom_b and not es_unknown(nom_b):
                font = "B"
                nom_brut = nom_b

        # Font C (si A i B no resolen i s'ha demanat scraping)
        nom_c = ""
        profile_id = ""
        if not font and do_scrape:
            nc, pid = autor_de_html(post["date"], post["slug"])
            nom_c = nc or ""
            profile_id = pid or ""
            if nom_c and not es_unknown(nom_c):
                font = "C"
                nom_brut = nom_c
            time.sleep(0.5)  # cortesia

        # Normalitza
        if font:
            canonical = normalitza(nom_brut)
            if canonical is None or canonical == AUTHOR_GENERIC:
                font = ""  # el nom normalitzat és també genèric
                canonical = AUTHOR_GENERIC
        else:
            canonical = AUTHOR_GENERIC

        resultats.append({
            "path": post["path"],
            "date": post["date"][:10],
            "title": post["title"],
            "slug": post["slug"],
            "nom_feed": nom_a,
            "nom_xml": nom_b,
            "nom_html": nom_c,
            "nom_brut": nom_brut,
            "profile_id": profile_id,
            "canonical": canonical,
            "font": font,
            "estat": "ok" if font else "manual",
        })
    return resultats


# ─────────────────────────────────────────────────────────────────────────────
# Informe i CSV
# ─────────────────────────────────────────────────────────────────────────────

def imprimeix_resum(resultats: list[dict]) -> None:
    total = len(resultats)
    ok = [r for r in resultats if r["estat"] == "ok"]
    manual = [r for r in resultats if r["estat"] == "manual"]

    print(f"\n{'='*60}")
    print(f"RESUM: {total} posts amb autor genèric")
    print(f"  recuperats: {len(ok)}  ({100*len(ok)//total if total else 0}%)")
    print(f"  manuals:    {len(manual)}")
    print()

    if ok:
        per_autor: dict[str, int] = {}
        per_font: dict[str, int] = {}
        for r in ok:
            per_autor[r["canonical"]] = per_autor.get(r["canonical"], 0) + 1
            per_font[r["font"]] = per_font.get(r["font"], 0) + 1
        print("Per autor recuperat:")
        for nom, n in sorted(per_autor.items(), key=lambda x: -x[1]):
            print(f"  {n:4d}  {nom}")
        print()
        print("Per font:")
        for font, n in sorted(per_font.items()):
            etiq = {"A": "Feed JSON", "B": "XML export", "C": "HTML scraping"}
            print(f"  {font} ({etiq.get(font,'?')}): {n}")

    if manual:
        print(f"\nPosts que requereixen revisió manual ({len(manual)}):")
        for r in manual[:15]:
            nom_info = r["nom_feed"] or "(cap)"
            print(f"  {r['date']}  «{r['title'][:45]}»  feed={nom_info!r}")
        if len(manual) > 15:
            print(f"  ... i {len(manual)-15} més (vegeu el CSV)")


def escriu_csv(resultats: list[dict], csv_path: str) -> None:
    camps = ["date", "slug", "title", "font", "canonical",
             "nom_feed", "nom_xml", "nom_html", "profile_id", "estat", "path"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=camps, extrasaction="ignore")
        w.writeheader()
        w.writerows(resultats)
    print(f"\nCSV escrit: {csv_path} ({len(resultats)} files)")


# ─────────────────────────────────────────────────────────────────────────────
# Aplicació dels canvis
# ─────────────────────────────────────────────────────────────────────────────

def aplica(resultats: list[dict]) -> None:
    """Reescriu el camp author als posts on tenim un autor recuperat."""
    a_aplicar = [r for r in resultats if r["estat"] == "ok"]
    if not a_aplicar:
        print("\nRes a aplicar.")
        return

    os.makedirs(BACKUP_DIR, exist_ok=True)
    aplicats = 0
    for r in a_aplicar:
        nou = r["canonical"]
        nou_yml = nou if re.fullmatch(r'[A-Za-zÀ-ÿ0-9 ,.()\'"«»-]+', nou) else f'"{nou}"'
        dest = os.path.join(BACKUP_DIR, os.path.basename(r["path"]))
        if not os.path.exists(dest):
            shutil.copy2(r["path"], dest)
        raw = open(r["path"], encoding="utf-8").read()
        raw2, n = re.subn(
            r"(^author:\s*).*?$",
            lambda m, v=nou_yml: m.group(1) + v,
            raw, count=1, flags=re.M,
        )
        if not n:
            print(f"  AVÍS: no hi ha camp author a {r['path']}")
            continue
        open(r["path"], "w", encoding="utf-8").write(raw2)
        aplicats += 1

    print(f"\nAplicats: {aplicats} fitxers (còpia prèvia a {BACKUP_DIR})")
    print("Ara cal:  hugo  +  commit  +  deploy pages")


# ─────────────────────────────────────────────────────────────────────────────
# Punt d'entrada
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    args = sys.argv[1:]
    do_apply   = "--apply"      in args
    do_scrape  = "--scrape"     in args
    clean_feed = "--clean-feed" in args

    xml_path = None
    csv_path = None
    for i, a in enumerate(args):
        if a == "--xml"  and i + 1 < len(args):
            xml_path = args[i + 1]
        if a == "--csv"  and i + 1 < len(args):
            csv_path = args[i + 1]

    print("=== recupera_autors_blogger.py v2 ===")
    print(f"    mode: {'APPLY' if do_apply else 'informe'}"
          f"  |  scraping: {'sí' if do_scrape else 'no'}"
          f"  |  xml: {xml_path or 'no'}")

    # Font A
    print("\n[A] Descarregant/carregant feed JSON de Blogger...")
    entries = descarrega_feed(forca=clean_feed)
    idx_a = index_de_feed(entries)
    print(f"    índex A: {len(idx_a)} entrades")

    # Font B
    idx_b: dict[str, str] = {}
    if xml_path:
        print(f"\n[B] Parsejant XML export: {xml_path}")
        idx_b = index_de_xml(xml_path)

    # Posts locals amb autor genèric
    print(f"\nCarregant posts locals amb autor «{AUTHOR_GENERIC}»...")
    locals_g = posts_locals_generic()
    print(f"    {len(locals_g)} posts a processar")

    if do_scrape:
        print("\n[C] Scraping del blog públic per als casos no resolts...")

    # Processament
    resultats = processa(locals_g, idx_a, idx_b, do_scrape)

    # Resum
    imprimeix_resum(resultats)

    # CSV
    if csv_path:
        escriu_csv(resultats, csv_path)
    elif not do_apply:
        default_csv = "/tmp/autors_recuperats_9bi.csv"
        escriu_csv(resultats, default_csv)

    # Aplicació
    if do_apply:
        aplica(resultats)
    else:
        print("\n(mode informe: no s'ha tocat res. Usa --apply per escriure els canvis)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Migra tots els posts del blog real (Blogger, blog-id 8034150767456238983)
a Markdown, llegint l'endpoint Atom paginat en directe — no cal l'exportació
manual des del panell de Blogger (verificat 2026-09-17: aquest endpoint serveix
Atom complet, sense truncar, amb start-index paginable).

Ús:
    python3 scripts/migrate_live.py --dry-run
    python3 scripts/migrate_live.py

Reutilitza el processament de contingut (imatges, àlbum, HTML→Markdown) de
migrate_blogger.py.
"""
import argparse
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import migrate_blogger as mb  # noqa: E402
import yaml  # noqa: E402

ATOM = mb.ATOM
BLOG_ID = "8034150767456238983"
FEED_URL = f"https://www.blogger.com/feeds/{BLOG_ID}/posts/default"
PAGE_SIZE = 150

# Mapeig verificat per <author><uri> (profile/<id>) -> membre real.
# Vegeu CLAUDE.md § "Mapeig d'autors" pel detall i comptatge per persona.
AUTHOR_BY_URI = {
    "07873791980606905428": 'Joan "Linux" Martínez i Serres',
    "09502103278209433876": "Pedro Click",
    "09447813154520602112": "Pedro Click",
    "07611922472754557605": 'Manel Sala "Ulls" Circ',
    "00926052916717343447": "Francesc Barbe",
    "06765486609758806432": "Ismael Utrilla",
    "16399715831790649537": "Alberto Sanagustín",
    "04330214459290255808": "Iozsef Kiss",
    "18053814840045725261": 'Pedro "Casal" Cervera',
    "10639085300606178057": "Núria Laura Orbaneja",
    "03875414596834414899": "Manel Villalba",
    "03777963813689534193": 'Manel Sala "Ulls" Circ',
    "15965093973040358649": "Nico YeYe",
    "06831158748343898384": "Juan Carlos Molina (Grismedio Casinegro)",
    "02393670543566068078": "9 Barris Imatge",
}
DEFAULT_AUTHOR = "9 Barris Imatge"

STOPWORDS = {
    "de", "la", "el", "els", "les", "i", "a", "amb", "per", "que", "del",
    "dels", "al", "als", "un", "una", "uns", "unes", "en", "es", "s", "l",
    "d", "o", "no", "més", "com", "però", "va", "han", "ha", "hi", "se",
}
TAG_RE = re.compile(r"<[^>]+>")


def fetch_page(start_index: int) -> bytes:
    url = f"{FEED_URL}?start-index={start_index}&max-results={PAGE_SIZE}"
    req = urllib.request.Request(url, headers={"User-Agent": "9bi-migrate/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def fetch_all_entries(limit=None):
    entries = []
    start = 1
    while True:
        data = fetch_page(start)
        root = ET.fromstring(data)
        page_entries = root.findall(ATOM + "entry")
        if not page_entries:
            break
        entries.extend(page_entries)
        if limit and len(entries) >= limit:
            entries = entries[:limit]
            break
        if len(page_entries) < PAGE_SIZE:
            break
        start += PAGE_SIZE
        time.sleep(0.2)
    return entries


def author_for(entry) -> str:
    a = entry.find(ATOM + "author")
    if a is None:
        return DEFAULT_AUTHOR
    uri = (a.findtext(ATOM + "uri") or "").strip()
    m = re.search(r"profile/(\d+)", uri)
    if m and m.group(1) in AUTHOR_BY_URI:
        return AUTHOR_BY_URI[m.group(1)]
    return DEFAULT_AUTHOR


def slug_from_entry(entry) -> str:
    url = None
    for link in entry.findall(ATOM + "link"):
        if link.get("rel") == "alternate":
            url = link.get("href")
            break
    return mb.slug_from_url(url) if url else None, url


def plain_text(html: str) -> str:
    return TAG_RE.sub(" ", html or "").lower()


def auto_tags(title: str, body_html: str, vocab: Counter, n=5):
    text = (title or "").lower() + " " + plain_text(body_html)
    candidates = []
    for term in vocab:
        t = term.strip()
        if not t or t.lower() in STOPWORDS or len(t) < 3:
            continue
        if t.lower() in text:
            candidates.append(t)
    candidates.sort(key=lambda t: (-len(t), -vocab[t]))
    return candidates[:n]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", default="content/posts")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=None, help="Només processa els N primers (per proves)")
    args = ap.parse_args()

    print("Descarregant entrades del feed en directe...")
    entries = fetch_all_entries(limit=args.limit)
    print(f"Entrades obtingudes: {len(entries)}")

    # Vocabulari global de tags reals (per suggerir-ne als posts sense cap)
    vocab = Counter()
    for e in entries:
        for c in e.findall(ATOM + "category"):
            term = c.get("term")
            scheme = c.get("scheme", "")
            if term and "kind#" not in scheme:
                vocab[term] += 1

    stats = {"ok": 0, "sense_tags": 0, "auto_tags": 0, "errors": []}
    seen_urls = set()

    for entry in entries:
        try:
            slug, orig_url = slug_from_entry(entry)
            title_el = entry.find(ATOM + "title")
            title = (title_el.text or "Sense títol") if title_el is not None else "Sense títol"
            if not slug or not orig_url:
                continue
            # Deduplica per URL real (mateix slug text es repeteix legítimament
            # en mesos diferents, p.ex. "blog-post" — no és col·lisió).
            if orig_url in seen_urls:
                continue
            seen_urls.add(orig_url)

            published = entry.findtext(ATOM + "published") or entry.findtext(ATOM + "updated")
            pub = datetime.fromisoformat(published)
            date_str = pub.strftime("%Y-%m-%dT%H:%M:%S%z")

            author = author_for(entry)

            tags = [c.get("term") for c in entry.findall(ATOM + "category")
                    if c.get("term") and "kind#" not in c.get("scheme", "")]

            content_el = entry.find(ATOM + "content")
            body_html = content_el.text or "" if content_el is not None else ""

            src, parent_href = mb.first_image(body_html)
            image_url = src
            album_url = parent_href if mb.is_album_link(parent_href) else None
            md_body = mb.html_to_md(mb.strip_first_image(body_html)) if body_html else ""

            note = ""
            if not tags:
                tags = auto_tags(title, body_html, vocab)
                if tags:
                    stats["auto_tags"] += 1
                    note = "<!-- tags auto-generades a partir del vocabulari del blog, revisar -->\n\n"
                else:
                    stats["sense_tags"] += 1

            front = {
                "title": title,
                "date": date_str,
                "author": author,
                "slug": slug,
            }
            if tags:
                front["tags"] = tags
            if image_url:
                front["cover"] = {"image": image_url}
            if album_url:
                front["album_url"] = album_url

            fname = os.path.join(args.output, pub.strftime("%Y"), f'{pub.strftime("%Y-%m-%d")}-{slug}.md')
            if not args.dry_run:
                os.makedirs(os.path.dirname(fname), exist_ok=True)
                with open(fname, "w", encoding="utf-8") as f:
                    f.write("---\n")
                    f.write(yaml.safe_dump(front, allow_unicode=True, sort_keys=False))
                    f.write("---\n\n")
                    f.write(note)
                    f.write(md_body + "\n")
            stats["ok"] += 1
        except Exception as e:  # noqa: BLE001
            stats["errors"].append((entry.findtext(ATOM + "title"), str(e)))

    print(f"OK: {stats['ok']}")
    print(f"  amb tags auto-generades: {stats['auto_tags']}")
    print(f"  sense cap tag (ni original ni trobada al vocabulari): {stats['sense_tags']}")
    if stats["errors"]:
        print(f"Errors: {len(stats['errors'])}")
        for t, e in stats["errors"][:20]:
            print(f"  - {t!r}: {e}")


if __name__ == "__main__":
    main()

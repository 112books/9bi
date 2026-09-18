#!/usr/bin/env python3
"""
Migra l'exportació XML de Blogger a entrades Markdown per a Hugo.

Ús:
    python3 scripts/migrate_blogger.py --input exports/blog-EXPORT.xml

Opcions:
    --input FILE        Ruta de l'exportació XML de Blogger (Settings → Other → Back up content)
    --output DIR        Directori de sortida (per defecte: content/posts)
    --download-images   Baixa les imatges a static/images/posts/<slug>/
                        (per defecte manté les URL originals del CDN de Blogger)
    --dry-run           No escriu fitxers, només informe

Depenències (venv):
    python3 -m venv .venv-migracio
    source .venv-migracio/bin/activate
    pip install markdownify pyyaml
"""

import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import urlparse
from urllib.parse import unquote

import yaml
from markdownify import MarkdownConverter, ATX

ATOM = "{http://www.w3.org/2005/Atom}"
BLOGGER_KIND = "http://schemas.google.com/g/2005#kind"
# Hosts d'imatge del propi Blogger: l'enllaç que envolta la primera imatge
# sol apuntar aquí per obrir-la a mida completa (lightbox), no és un àlbum.
BLOGGER_IMAGE_HOSTS = ("blogger.googleusercontent.com", "bp.blogspot.com", "blogspot.com")
IMG_TAG = re.compile(r"<img [^>]*>", re.IGNORECASE)
SRC_ATTR = re.compile(r'src\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
HREF_ATTR = re.compile(r'href\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
GOOGLE_TRANS_PRE = re.compile(
    r'<pre[^>]*class="[^"]*tw-data-text[^"]*"[^>]*>.*?</pre>\s*', re.DOTALL | re.IGNORECASE
)
TRAILING_BR = re.compile(r"(?:\s*<br\s*/?>)+\s*</(?:p|div)>", re.IGNORECASE)


def clean_html(html: str) -> str:
    """Neteja la brossa que genera Blogger/Google Translate."""
    if not html:
        return ""
    html = GOOGLE_TRANS_PRE.sub("", html)
    html = TRAILING_BR.sub("</p>", html)
    return html


def html_to_md(html: str) -> str:
    """Converteix HTML del cos a Markdown net."""
    html = clean_html(html)
    conv = MarkdownConverter(heading_style=ATX)
    md = conv.convert(html)
    # Neteja d'espais en blanc repetits i línies buides triples
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def first_image(html: str):
    """Retorna (src, parental_href) de la primera imatge del cos, si n'hi ha."""
    m = IMG_TAG.search(html)
    if not m:
        return None, None
    tag = m.group(0)
    src_m = SRC_ATTR.search(tag)
    src = src_m.group(1) if src_m else None
    if not src:
        return None, None
    parent = html[max(0, m.start() - 600): m.start()]
    link_m = re.findall(HREF_ATTR, parent)
    parent_href = link_m[-1] if link_m else None
    return src, parent_href


def strip_first_image(html: str) -> str:
    """Elimina del cos la primera imatge, el seu enllaç i els contenidors buits."""

    m = IMG_TAG.search(html)
    if not m:
        return html
    # Si la imatge està dins d'un <a>...</a>, elimina tot l'enllaç
    seg_start = html.rfind("<a ", 0, m.start())
    seg_end = html.find("</a>", m.end())
    if seg_start != -1 and seg_end != -1 and seg_end - m.end() < 100:
        seg_end += len("</a>")
    else:
        seg_start = m.start()
        seg_end = m.end()

    html = html[:seg_start] + html[seg_end:]
    # Elimina els <div class="separator"> que han quedat buits al voltant
    html = re.sub(
        r'<div[^>]*class="[^"]*separator[^"]*"[^>]*>\s*(?:<br\s*/?>)?\s*</div>',
        "",
        html,
        flags=re.IGNORECASE,
    )
    return html


def slug_from_url(url: str) -> str:
    name = urlparse(url).path.rstrip("/").rsplit("/", 1)[-1]
    if name.endswith(".html"):
        name = name[:-5]
    return unquote(name)


def iso_date(raw: str) -> str:
    """Normalitza la data ISO de Blogger (TZ ±hh:mm) a format Hugo."""
    raw = raw.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    return raw


def parse_xml(path: str):
    tree = ET.parse(path)
    root = tree.getroot()
    posts = []
    for entry in root.findall(ATOM + "entry"):
        categories = entry.findall(ATOM + "category")
        kinds = [c.get("term") for c in categories if c.get("scheme") == BLOGGER_KIND]
        if not any("#post" in (k or "") for k in kinds):
            continue  # salta comentaris i config
        title_el = entry.find(ATOM + "title")
        title = title_el.text or "" if title_el is not None else ""
        content_el = entry.find(ATOM + "content")
        content = content_el.text or "" if content_el is not None else ""
        pub_el = entry.find(ATOM + "published")
        published = pub_el.text or "" if pub_el is not None else ""
        upd_el = entry.find(ATOM + "updated")
        updated = upd_el.text or "" if upd_el is not None else ""
        author_el = entry.find(ATOM + "author")
        author = ""
        if author_el is not None:
            name_el = author_el.find(ATOM + "name")
            author = name_el.text if name_el is not None and name_el.text else ""
        tags = [c.get("term") for c in categories
                if c.get("scheme") == "http://www.blogger.com/atom/01/n/"]
        tags = [t for t in tags if t]
        url = None
        for link in entry.findall(ATOM + "link"):
            if link.get("rel") == "alternate":
                url = link.get("href")
                break
        entry_id = entry.findtext(ATOM + "id")
        posts.append({
            "title": title,
            "content": content,
            "published": iso_date(published),
            "updated": iso_date(updated),
            "author": author,
            "tags": tags,
            "url": url,
            "entry_id": entry_id or "",
        })
    return posts


def is_album_link(href: str) -> bool:
    """Un enllaç és àlbum si és extern (no la mateixa imatge de Blogger a mida completa).

    Conserva Google Photos i qualsevol altre servei (Flickr, Picasa, Dropbox...)."""
    if not href:
        return False
    host = urlparse(href).netloc.lower()
    return not any(h in host for h in BLOGGER_IMAGE_HOSTS)


def slugify_sample(slug: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", default="content/posts")
    ap.add_argument("--download-images", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    posts = parse_xml(args.input)
    print(f"Posts trobats: {len(posts)}")

    stats = {"ok": 0, "sense_data": 0, "errors": []}
    for post in posts:
        try:
            pub = datetime.fromisoformat(post["published"])
            date_str = pub.strftime("%Y-%m-%dT%H:%M:%S%z")
            slug = slug_from_url(post["url"]) if post["url"] else slugify_sample(post["title"])
            if not slug:
                slug = "post-" + pub.strftime("%Y%m%d-%H%M%S")

            body_html = post["content"]
            src, parent_href = first_image(body_html)
            image_url = src
            album_url = parent_href if is_album_link(parent_href) else None

            if args.download_images and src:
                image_url = download_image(src, pub, slug, args)

            md_body = html_to_md(strip_first_image(body_html)) if body_html else ""

            front = {
                "title": post["title"] or "Sense títol",
                "date": date_str,
                "author": post["author"] or "9 Barris Imatge",
                "slug": slug,
            }
            if post["tags"]:
                front["tags"] = post["tags"]
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
                    f.write(md_body + "\n")
            stats["ok"] += 1
        except Exception as e:  # noqa: BLE001
            stats["errors"].append((post.get("title"), str(e)))

    print(f"OK: {stats['ok']}")
    if stats["errors"]:
        print(f"Errors: {len(stats['errors'])}")
        for t, e in stats["errors"][:20]:
            print(f"  - {t!r}: {e}")
    if args.dry_run:
        print("Dry run: cap fitxer escrit.")


def download_image(src, pub, slug, args):
    """Baixa una imatge remota a static/images/posts/<any>/<any>-<mes>-<slug>.<ext>."""
    import hashlib
    import urllib.request

    out_dir = os.path.join("static", "images", "posts")
    os.makedirs(out_dir, exist_ok=True)
    ext = os.path.splitext(urlparse(src).path)[1][:6] or ".jpg"
    if not ext or "." not in ext:
        ext = ".jpg"
    fname = f'{pub.strftime("%Y-%m-%d")}-{slug}{ext}'
    dest = os.path.join(out_dir, fname)
    if not os.path.exists(dest):
        req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        with open(dest, "wb") as f:
            f.write(data)
    return "/images/posts/" + fname


if __name__ == "__main__":
    sys.exit(main())
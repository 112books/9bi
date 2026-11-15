#!/usr/bin/env python3
"""Miniatura de portada per als articles publicats amb el gestor.

El gestor (Sveltia) puja les fotos tal com surten de la càmera o del mòbil, i la
portada del web és un mosaic que les carrega totes. Aquest script, doncs, agafa
cada article la portada del qual apunta a un original de `/images/`, en genera
una miniatura **WebP de com a màxim 640 px** a `/images/covers/` (amb un nom
derivat del contingut, com les 2.973 que ja hi ha) i reescriu el `cover.image`
de l'article perquè apunti a la miniatura.

No toca res més del front matter: només la línia `image:` del bloc `cover:`.

El CI el passa abans del build i desa el resultat (imatges + articles), igual
que fa amb el recompte de posts. En local:

    python3 scripts/portades_miniatures.py --dry-run   # veure què faria
    python3 scripts/portades_miniatures.py             # aplicar-ho

Requereix Pillow (pip install pillow).
"""
from __future__ import annotations

import glob
import hashlib
import os
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Cal Pillow: pip install pillow")

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
COVERS_DIR = ROOT / "static" / "images" / "covers"
WIDTH = 640
QUALITY = 82
COVERS_URL = "/images/covers/"

FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
COVER_BLOCK_RE = re.compile(r"^cover:[ \t]*\n((?:[ \t]+.*\n)*)", re.M)
IMAGE_LINE_RE = re.compile(r"^([ \t]+image:[ \t]*)(.+)$", re.M)


def read_front_matter(text):
    m = FM_RE.match(text)
    return m


def parse_fm(text):
    m = read_front_matter(text)
    if not m or yaml is None:
        return None
    try:
        return yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None


def cover_image_of(fm_text):
    """Retorna (match_del_bloc, match_de_la_linia_image, valor)."""
    block = COVER_BLOCK_RE.search(fm_text)
    if not block:
        return None, None, None
    line = IMAGE_LINE_RE.search(block.group(1))
    if not line:
        return None, None, None
    value = line.group(2).strip().strip('"').strip("'")
    return block, line, value


def make_thumbnail(src: Path, dry_run: bool):
    """Genera la miniatura i torna el nom del fitxer, o None si no cal."""
    digest = hashlib.sha1(src.read_bytes()).hexdigest()[:16]
    name = digest + ".webp"
    out = COVERS_DIR / name
    if out.exists():
        return name, 0

    with Image.open(src) as img:
        img = ImageOps.exif_transpose(img)
        has_alpha = img.mode in ("RGBA", "LA") or (
            img.mode == "P" and "transparency" in img.info
        )
        img = img.convert("RGBA" if has_alpha else "RGB")
        width, height = img.size
        if width > WIDTH:
            new_size = (WIDTH, max(1, round(height * WIDTH / width)))
            img = img.resize(new_size, Image.LANCZOS)
        if dry_run:
            return name, 0
        COVERS_DIR.mkdir(parents=True, exist_ok=True)
        img.save(out, "WEBP", quality=QUALITY, method=6)
    return name, out.stat().st_size


def process(path: Path, dry_run: bool):
    text = path.read_text(encoding="utf-8")
    fm_match = read_front_matter(text)
    if not fm_match:
        return None
    fm_text = fm_match.group(1)

    block, line, value = cover_image_of(fm_text)
    if not value:
        return None
    if value.startswith(COVERS_URL) or value.startswith("images/covers/"):
        return None
    if not value.startswith("/images/"):
        return ("extern", value, 0, 0)
    src = ROOT / "static" / value.lstrip("/")
    if not src.exists():
        return ("manca", value, 0, 0)

    before_size = src.stat().st_size
    name, thumb_size = make_thumbnail(src, dry_run)
    new_value = COVERS_URL + name

    # Reescriptura quirúrgica: només la línia image: del bloc cover:
    # Els desplaçaments de «line» són relatius al bloc cover:, cal sumar-los
    # la posició on comença el bloc dins del front matter.
    offset = block.start(1)
    new_fm = (
        fm_text[: offset + line.start(2)]
        + new_value
        + fm_text[offset + line.end(2) :]
    )
    new_text = "---\n" + new_fm + "\n---\n" + text[fm_match.end() :]

    if not dry_run:
        # Comprovació: només ha de canviar cover.image
        old_data, new_data = parse_fm(text), parse_fm(new_text)
        if old_data is not None and new_data is not None:
            old_data.get("cover", {}).pop("image", None)
            new_cover = new_data.get("cover", {})
            new_image = new_cover.pop("image", None)
            if old_data != new_data or new_image != new_value:
                raise SystemExit(
                    "Avortat: el front matter de %s canviaria més del compte" % path
                )
        path.write_text(new_text, encoding="utf-8")

    return ("fet", value, before_size, thumb_size, new_value)


def main():
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    files = sorted(Path(p) for p in glob.glob(str(ROOT / "content/posts/*/*.md")))
    done, extern, missing, errors = [], [], [], []
    total_before = total_after = 0
    for path in files:
        try:
            result = process(path, dry_run)
        except Exception as error:  # noqa: BLE001
            errors.append((path, str(error)))
            continue
        if result is None:
            continue
        if result[0] == "extern":
            extern.append((path, result[1]))
            continue
        if result[0] == "manca":
            missing.append((path, result[1]))
            continue
        _, before_value, before_size, after_size = result[:4]
        done.append((path, before_value, before_size, after_size))
        total_before += before_size
        total_after += after_size

    for path, value, before_size, after_size in done:
        print(
            "%-58s %6.0f KB -> %5.0f KB  %s"
            % (path.name[:58], before_size / 1024, after_size / 1024, value)
        )
    for path, value in missing:
        print("AVÍS: no existeix el fitxer de %s (%s)" % (path.name[:50], value))
    for path, value in extern:
        print("NOTA: portada externa o fora de /images/, no es toca: %s" % value)
    for path, error in errors:
        print("ERROR: %s: %s" % (path.name[:50], error))

    print(
        "\n%s %d portades (%s %.1f MB -> %.1f MB)"
        % (
            "Es generarien" if dry_run else "Fetes",
            len(done),
            "estalvi" if done else "",
            total_before / 1048576,
            total_after / 1048576,
        )
    )
    if errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

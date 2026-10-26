#!/usr/bin/env python3
"""Actualitza el recompte de posts del projecte.

Compta els articles publicats a content/posts/ (fitxers .md, excloent els
draft) i les carpetes d'anys, i reescriu la línia «Posts actuals» de
CLAUDE.md. També actualitza les altres mencions del total («N posts») a
CLAUDE.md i al comentari de static/admin/config.yml.

No toca gestio/SESSIONSLOG.md ni cap altre historial.

Ús:
    python3 scripts/actualitza_recompte.py            # escriu
    python3 scripts/actualitza_recompte.py --dry-run  # només informa
"""

import re
import sys
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
POSTS = ARREL / "content" / "posts"
CLAUDE = ARREL / "CLAUDE.md"
CONFIG = ARREL / "static" / "admin" / "config.yml"

# Articles migrats de Blogger (xifra tancada, no canvia).
BLOGGER_MIGRATS = 3006


def xifra(n: int) -> str:
    """3017 -> '3.017' (separador de milers català)."""
    return f"{n:,}".replace(",", ".")


def recompte() -> dict:
    if not POSTS.is_dir():
        sys.exit(f"ERROR: no existeix {POSTS}")
    total = 0
    for fitxer in POSTS.rglob("*.md"):
        text = fitxer.read_text(encoding="utf-8", errors="replace")
        if re.search(r"^draft:\s*true\s*$", text, re.MULTILINE):
            continue
        total += 1
    anys = sorted(p.name for p in POSTS.iterdir() if p.is_dir() and p.name.isdigit())
    if not anys:
        sys.exit(f"ERROR: cap carpeta d'any a {POSTS}")
    return {"total": total, "anys": anys}


def main() -> int:
    dry = "--dry-run" in sys.argv[1:]
    dades = recompte()
    total, anys = dades["total"], dades["anys"]
    nous = total - BLOGGER_MIGRATS
    rang = f"{anys[0]}\u2013{anys[-1]}"

    claude = CLAUDE.read_text(encoding="utf-8")
    linia = (
        f"- **Posts actuals**: {xifra(total)} "
        f"({xifra(BLOGGER_MIGRATS)} migrats de Blogger + {nous} articles nous), "
        f"{len(anys)} carpetes d'anys ({rang})."
    )

    nou, n = re.subn(r"^- \*\*Posts actuals\*\*:.*$", linia, claude, flags=re.MULTILINE)
    if n != 1:
        sys.exit(f"ERROR: s'esperava 1 línia «Posts actuals» a CLAUDE.md i n'hi ha {n}")

    # Altres mencions del total («3.010 posts») a CLAUDE.md i config.yml.
    PATRO_TOTAL = r"\b\d{1,3}(?:\.\d{3})*\s+posts\b"
    sortides = [(CLAUDE, re.sub(PATRO_TOTAL, f"{xifra(total)} posts", nou))]
    if CONFIG.is_file():
        config = CONFIG.read_text(encoding="utf-8")
        sortides.append((CONFIG, re.sub(PATRO_TOTAL, f"{xifra(total)} posts", config)))

    if dry:
        print(f"Posts: {xifra(total)} ({nous} de nous des de la migració)")
        print(f"Anys: {len(anys)} ({rang})")
        print("\n--- línia resultant ---")
        print(linia)
        for cami, text in sortides:
            canvia = text != cami.read_text(encoding="utf-8")
            print(f"{cami.relative_to(ARREL)}: {'actualitzat' if canvia else 'sense canvis'}")
        return 0

    for cami, text in sortides:
        if text != cami.read_text(encoding="utf-8"):
            cami.write_text(text, encoding="utf-8")
            print(f"Actualitzat {cami.relative_to(ARREL)}")
        else:
            print(f"Sense canvis a {cami.relative_to(ARREL)}")
    print(linia)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

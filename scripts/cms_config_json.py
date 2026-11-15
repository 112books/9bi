#!/usr/bin/env python3
"""Genera static/admin/config.json a partir de static/admin/config.yml.

El gestor de continguts (/admin/) necessita la configuració com a objecte
JSON per poder-la adaptar al navegador segons qui hi entra: el Sveltia llegeix
config.yml, però per afegir-hi filtres per autor cal carregar-la, retocar-la i
passar-la a CMS.init() (vegeu static/admin/index.html).

El CI el regenera a cada publicació. En local:

    python3 scripts/cms_config_json.py

Requereix PyYAML (pip install pyyaml).
"""
from pathlib import Path
import json
import sys

try:
    import yaml
except ImportError:
    sys.exit("Cal PyYAML: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "static/admin/config.yml"
DST = ROOT / "static/admin/config.json"


def main():
    config = yaml.safe_load(SRC.read_text(encoding="utf-8"))
    text = json.dumps(config, ensure_ascii=False, indent=1) + "\n"
    DST.write_text(text, encoding="utf-8")
    print(
        "%s: %d col·leccions, %d caràcters"
        % (DST.relative_to(ROOT), len(config.get("collections") or []), len(text))
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Genera data/popular.json amb els articles més visitats (últims N dies)
llegint l'API de GoatCounter.

Ús:
    export GOATCOUNTER_API_KEY="..."   # GoatCounter → Settings → API keys
    python3 scripts/goatcounter_popular.py --days 30

Resultat:
    data/popular.json  →  [{"path": "/2026/07/el-esport-peu-de-barriprospe-beach26.html", "count": 123}, ...]

El partial que el renderitza (pàgina /mes-visitats/) el consumeix directament.
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from datetime import date, timedelta

API = "https://stats.goatcounter.com/api/v0/stats/pages"


def fetch_top_pages(days: int, api_key: str, site: str = "9barrisimatge"):
    since = date.today() - timedelta(days=days)
    url = f"{API}?as=csv&from={since.isoformat()}&tz=Europe/Madrid"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {api_key}",
        "Accept": "text/csv",
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read().decode("utf-8")
    rows = []
    for line in data.splitlines()[1:]:
        # format CSV: "path","title","count","percent"
        parts = line.split(",")
        # suport simplificat: path,count com a dos últims camps fiables
        path = parts[0].strip('"')
        count = parts[2].strip('"')
        if not path or not count.isdigit():
            continue
        if not re.search(r"^\d{4}/\d{2}/.*\.html$", path):
            continue  # només articles, no pàgines internes
        rows.append({"path": "/" + path.lstrip("/"), "count": int(count)})
    rows.sort(key=lambda r: r["count"], reverse=True)
    return rows[:10]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--output", default="data/popular.json")
    args = ap.parse_args()

    api_key = os.environ.get("GOATCOUNTER_API_KEY")
    if not api_key:
        print("Falta GOATCOUNTER_API_KEY (GoatCounter → Settings → API keys).", file=sys.stderr)
        return 1

    rows = fetch_top_pages(args.days, api_key)
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"Escrites {len(rows)} entrades a {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
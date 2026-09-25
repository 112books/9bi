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

Si la consulta falla, no es torna a escriure el fitxer: es conserva el
contingut anterior i el programa acaba amb error (codi 1) perquè el
desplegament del web continuï igual.
"""

import argparse
import csv
import io
import json
import os
import re
import sys
import urllib.request
from datetime import date, timedelta

# GoatCounter allotja cada lloc al seu propi subdomini; el token és del lloc
# 9bi, de manera que la consulta s'ha de fer a 9bi.goatcounter.com i no al
# API genèric de stats.goatcounter.com.
API = "https://9bi.goatcounter.com/api/v0/stats"
ARTICLE_RE = re.compile(r"^\d{4}/\d{2}/.*\.html$")


def fetch_top_pages(days: int, api_key: str, site: str = "9barrisimatge"):
    since = date.today() - timedelta(days=days)
    url = (f"{API}/pages?as=csv&from={since.isoformat()}"
           f"&tz=Europe/Madrid&site={site}&limit=100")
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {api_key}",
        "Accept": "text/csv",
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read().decode("utf-8")
    rows = []
    # El títol pot contenir comes i cometes, de manera que cal el mòdul csv
    # i no partir la línia a sac: path, title, count, percent
    reader = csv.reader(io.StringIO(data))
    next(reader, None)
    for parts in reader:
        if len(parts) < 3:
            continue
        path = parts[0].strip()
        count = parts[2].strip()
        if not path or not count.isdigit():
            continue
        if not ARTICLE_RE.match(path):
            continue  # només articles, no pàgines internes
        if int(count) == 0:
            continue  # sense visites no és un article "més visitat"
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

    try:
        rows = fetch_top_pages(args.days, api_key)
    except Exception as exc:
        print("No s'ha pogut consultar GoatCounter: %s: %s"
              % (type(exc).__name__, exc), file=sys.stderr)
        print("Es conserva %s tal com estava." % args.output, file=sys.stderr)
        return 1

    if not rows:
        print("GoatCounter no ha retornat cap article als últims %d dies; "
              "es conserva %s tal com estava."
              % (args.days, args.output), file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Escrites {len(rows)} entrades a {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

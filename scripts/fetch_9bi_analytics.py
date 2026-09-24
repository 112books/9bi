#!/usr/bin/env python3
"""
Genera static/stats/analytics.json amb les estadístiques del web per al
dashboard /stats/ (GoatCounter).

Ús:
    export GOATCOUNTER_API_KEY="..."   # GoatCounter → Settings → API key
    python3 scripts/fetch_9bi_analytics.py [--days 30] [--output static/stats/analytics.json]

Adaptat de goatcounter-dashboard (scripts/fetch_goatcounter_analytics.py),
amb:
  - end = avui (GoatCounter 9bi no retorna under end=ahir)
  - trànsit directe (ref_scheme "o") etiquetat com a "Directe"
  - zero dependències (standard library, urllib)
"""

import argparse
import json
import os
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone

API = "https://9bi.goatcounter.com/api/v0/stats"

LANGS = {"ca", "es", "en", "fr", "de", "it", "pt"}


def gc_get(token, endpoint, params):
    url = f"{API}/{endpoint}?" + "&".join(f"{k}={v}" for k, v in params.items())
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def extract_lang(path):
    parts = [p for p in path.strip("/").split("/") if p]
    if parts and parts[0] in LANGS:
        return parts[0]
    if len(parts) >= 2 and parts[1] in LANGS:
        return parts[1]
    return None


def extract_section(path):
    if not path:
        return "inici"
    parts = [p for p in path.strip("/").split("/") if p]
    if not parts:
        return "inici"
    # Staging (linuxbcn.codeberg.page/9bi/) prefixa el path amb /9bi/
    if parts[0] == "9bi":
        parts = parts[1:]
    if not parts:
        return "inici"
    idx = 1 if parts[0] in LANGS else 0
    if idx == 0 and len(parts) > 1 and parts[1] in LANGS:
        idx = 2
    section = parts[idx] if idx < len(parts) else "inici"
    if section in ("index.html", "index"):
        section = "inici"
    return section


def norm_items(items):
    out = []
    for item in items:
        name = item.get("name") or item.get("id") or "Desconegut"
        # Directe (ref_scheme "o") o "(unknown)" → etiqueta llegible
        if item.get("ref_scheme") == "o":
            name = "Directe"
        if name in ("(unknown)", ""):
            name = "Desconegut"
        count = item.get("count", 0)
        if count > 0:
            out.append({"name": name, "id": item.get("id", name), "count": count})
    return sorted(out, key=lambda x: x["count"], reverse=True)


def fetch_analytics(token, days=30):
    now = datetime.now(timezone.utc)
    end = now.strftime("%Y-%m-%d")
    start = (now - timedelta(days=days)).strftime("%Y-%m-%d")
    params = {"start": start, "end": end, "limit": 50}

    try:
        hits_raw = gc_get(token, "hits", params).get("hits", [])
    except Exception as exc:
        print(f"WARN: GoatCounter hits fetch failed: {exc}", file=sys.stderr)
        hits_raw = []

    by_lang, by_section = {}, {}
    total, hits_by_day, hits_pages = 0, {}, {}

    for path_item in hits_raw:
        path = path_item.get("path", "")
        lang = extract_lang(path)
        section = extract_section(path)
        path_total = 0
        for stat in path_item.get("stats", []):
            d = (stat.get("day") or "")[:10]
            count = stat.get("daily", 0)
            if not count:
                continue
            total += count
            path_total += count
            if lang:
                by_lang[lang] = by_lang.get(lang, 0) + count
            by_section[section] = by_section.get(section, 0) + count
            if d:
                hits_by_day[d] = hits_by_day.get(d, 0) + count
        if path_total > 0:
            hits_pages[path] = hits_pages.get(path, 0) + path_total

    hits_by_day_list = [{"date": k, "count": v} for k, v in sorted(hits_by_day.items())]
    hits_top = sorted(
        [{"path": k, "count": v} for k, v in hits_pages.items()],
        key=lambda x: x["count"], reverse=True,
    )[:30]

    def safe(endpoint):
        try:
            return norm_items(gc_get(token, endpoint, params).get("stats", []))
        except Exception as exc:
            print(f"WARN: {endpoint} failed: {exc}", file=sys.stderr)
            return []

    total_data = {}
    try:
        total_data = gc_get(token, "total", {"start": start, "end": end}) or {}
    except Exception as exc:
        print(f"WARN: /stats/total failed: {exc}", file=sys.stderr)

    return {
        "generated": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "period": {"start": start, "end": end},
        "total": total,
        "total_unique": total_data.get("total_unique", 0),
        "hits_by_day": hits_by_day_list,
        "hits": hits_top,
        "by_lang": by_lang,
        "by_section": by_section,
        "browsers": safe("browsers"),
        "systems": safe("systems"),
        "sizes": safe("sizes"),
        "locations": safe("locations"),
        "refs": safe("toprefs"),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--output", default="static/stats/analytics.json")
    args = ap.parse_args()

    token = os.environ.get("GOATCOUNTER_API_KEY")
    if not token:
        print("Falta GOATCOUNTER_API_KEY (GoatCounter → Settings → API key).", file=sys.stderr)
        return 1

    data = fetch_analytics(token, days=args.days)
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ {args.output}: total={data['total']} · {len(data['hits'])} pàgines · {len(data['hits_by_day'])} dies")
    return 0


if __name__ == "__main__":
    sys.exit(main())
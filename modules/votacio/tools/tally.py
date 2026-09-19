#!/usr/bin/env python3
"""Compta els vots d'una edició (digitals de la BD + paper des d'un fitxer).

Ús:
    python3 tools/tally.py                       # llegeix data.db de la config
    python3 tools/tally.py --db /camí/data.db
    python3 tools/tally.py --paper paper.csv     # afegeix vots en paper

El fitxer de paper és un CSV amb una obra per línia: el número, o bé
`obra,titol` (el títol s'ignora en el recompte).
"""

import argparse
import csv
import os
import sys
import sqlite3

MODULE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MODULE_DIR)

import app


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", help="ruta de la BD (per defecte la del config)")
    ap.add_argument("--paper", help="CSV amb els vots en paper (--paper xtra)")
    ap.add_argument("--json", action="store_true", help="sortida JSON")
    args = ap.parse_args(argv)

    if args.db:
        conn = sqlite3.connect(args.db)
    else:
        cfg = app.load_config()
        conn = app.connect(cfg)
    conn.row_factory = sqlite3.Row
    ed = conn.execute("SELECT * FROM edicions ORDER BY id DESC LIMIT 1").fetchone()
    rows = conn.execute(
        "SELECT o.id, o.numero, o.titol, o.autor, "
        " SUM(IFNULL(v.paper,0)) AS paper, COUNT(v.id)-SUM(IFNULL(v.paper,0)) AS digitals "
        " FROM obres o LEFT JOIN vots v ON v.obra_id=o.id "
        " WHERE o.edicio_id=? GROUP BY o.id", (ed["id"],)).fetchall()

    paper = {}
    if args.paper:
        with open(args.paper, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                obra = line.split(",")[0].strip()
                try:
                    numero = int(obra)
                except ValueError:
                    continue
                paper[numero] = paper.get(numero, 0) + 1

    total = {r["id"]: r["digitals"] + paper.get(r["numero"], 0) for r in rows}
    if args.json:
        out = [{"numero": r["numero"], "titol": r["titol"], "autor": r["autor"],
                "digitals": r["digitals"], "paper": paper.get(r["numero"], 0),
                "total": total[r["id"]]} for r in rows]
        print(json.dumps(out, ensure_ascii=False))
    else:
        print("Edició:", ed["nom"])
        print("%-6s %-30s %8s %6s %6s" % ("Obra", "Títol", "Digital", "Paper", "Total"))
        for r in sorted(rows, key=lambda r: -total[r["id"]]):
            print("%-6d %-30s %8d %6d %6d" % (
                r["numero"], (r["titol"] or "")[:30],
                r["digitals"], paper.get(r["numero"], 0), total[r["id"]]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
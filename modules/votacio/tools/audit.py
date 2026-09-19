#!/usr/bin/env python3
"""Audita la integritat i la signatura del recompte d'una edició.

Ús:
    python3 tools/audit.py                     # verifica data.db
    python3 tools/audit.py --db /camí/data.db

Comprova:
  - que cada vot té una signatura HMAC vàlida amb el secret de l'edició,
  - que no hi hagi vots duplicats (mateix dispositiu i obra),
  - i (en mode --strict) que els `ts` estiguin dins de la finestra de votació.

Sortida: línies per vot invalid + resum. Codi de sortida 0 si tot bé.
"""

import argparse
import hmac
import json
import os
import sqlite3
import sys

MODULE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MODULE_DIR)

import app


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", help="ruta de la BD (per defecte la del config)")
    ap.add_argument("--strict", action="store_true", help="comprova la finestra de temps")
    args = ap.parse_args(argv)

    if args.db:
        conn = sqlite3.connect(args.db)
    else:
        cfg = app.load_config()
        conn = app.connect(cfg)
    conn.row_factory = sqlite3.Row

    cfg = app.load_config()
    secret = cfg.get("edicio", "secret", fallback="") or cfg.get("general", "secret", fallback="")
    if not secret:
        print("ERROR: no trobo el secret (clau `secret` de [general] o [edicio]).", file=sys.stderr)
        return 1

    works = {r["id"]: r for r in conn.execute("SELECT id,numero,edicio_id FROM obres")}
    n_bad = 0
    n_paper = 0
    dupes = set()
    for v in conn.execute("SELECT * FROM vots"):
        obra = works.get(v["obra_id"])
        if v["paper"]:
            n_paper += 1
            continue
        if obra is None:
            print("obra inexistent id=%d" % v["obra_id"]); n_bad += 1; continue
        key = (v["edicio_id"], v["obra_id"], v["dispositiu_hash"], v["ts"])
        sig = app.hmac_sig(secret, key)
        if not hmac.compare_digest(sig, v["signatura"]):
            print("vot obra %d ts=%d: signatura invàlida" % (obra["numero"], v["ts"]))
            n_bad += 1
        d = (v["obra_id"], v["dispositiu_hash"])
        if d in dupes:
            print("duplicat obra %d (mateix dispositiu)" % obra["numero"])
            n_bad += 1
        dupes.add(d)
        if args.strict:
            ed = conn.execute("SELECT data_inici,data_fi FROM edicions WHERE id=?",
                              (v["edicio_id"],)).fetchone()
            ini = app.parse_iso_local(ed["data_inici"]).timestamp() if ed and ed["data_inici"] else 0
            fi = app.parse_iso_local(ed["data_fi"]).timestamp() if ed and ed["data_fi"] else 2**63
            if not (ini <= v["ts"] <= fi):
                print("vot obra %d fora de la finestra temporaral" % obra["numero"])
                n_bad += 1

    tot = conn.execute("SELECT COUNT(*) AS n FROM vots").fetchone()["n"]
    print("vots totals: %d (dels quals %d paper)" % (tot, n_paper))
    print("anomalies: %d" % n_bad)
    return 1 if n_bad else 0


if __name__ == "__main__":
    sys.exit(main())
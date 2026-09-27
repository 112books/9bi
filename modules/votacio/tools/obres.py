#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Col·lectiu 9 Barris Imatge
"""Converteix la llista d'obres (CSV) al bloc [obres] del config.ini.

Ús:
    python3 tools/obres.py llista.csv            # imprimeix el bloc [obres]
    python3 tools/obres.py llista.csv -o obres.ini

El CSV porta capçalera: numero,titol,autor,categoria (separat per comes o per
punt i coma, com el deixa l'Excel o el LibreOffice en català). Només el número
és obligatori.

El bloc resultant substitueix SENCERA la secció [obres] del config.ini: si hi
queda una línia «rang = ...», les obres de prova es continuarien generant.
"""
import argparse
import csv
import io
import sys

CATEGORIES = ("A", "B", "C")   # Color, Blanc i negre, Premi Josep Antón Cordoncillo


def llegeix(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        text = f.read()
    try:
        dialect = csv.Sniffer().sniff(text.splitlines()[0], delimiters=",;\t")
    except (csv.Error, IndexError):
        dialect = csv.excel
    return list(csv.DictReader(io.StringIO(text), dialect=dialect))


def valida(files):
    """Retorna (obres, errors, avisos). obres = llista de (numero, titol, autor, cat)."""
    obres, errors, avisos, vistos = [], [], [], {}
    for i, fila in enumerate(files, start=2):          # línia 1 = capçalera
        fila = {(k or "").strip().lower(): (v or "").strip() for k, v in fila.items()}
        if not any(fila.values()):
            continue
        num = fila.get("numero") or fila.get("número") or ""
        if not num.isdigit() or int(num) < 1:
            errors.append("línia %d: número no vàlid «%s»" % (i, num))
            continue
        n = int(num)
        if n in vistos:
            errors.append("línia %d: número %d repetit (ja és a la línia %d)" % (i, n, vistos[n]))
            continue
        vistos[n] = i
        titol, autor = fila.get("titol") or fila.get("títol") or "", fila.get("autor", "")
        cat = fila.get("categoria", "").upper()
        for nom, valor in (("títol", titol), ("autor", autor), ("categoria", cat)):
            if "|" in valor or "\n" in valor:
                errors.append("línia %d: el camp %s no pot portar «|» ni salts de línia" % (i, nom))
        if cat and cat not in CATEGORIES:
            avisos.append("línia %d: categoria «%s» (s'esperava A, B o C)" % (i, cat))
        if not titol:
            avisos.append("línia %d: obra %d sense títol" % (i, n))
        obres.append((n, titol, autor, cat))
    return sorted(obres), errors, avisos


def bloc(obres):
    linies = ["[obres]",
              "# Llista definitiva generada amb tools/obres.py (%d obres)." % len(obres),
              "# numero = titol | autor | categoria"]
    linies += ["%d = %s | %s | %s" % o for o in obres]
    return "\n".join(linies) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv")
    ap.add_argument("-o", "--sortida")
    a = ap.parse_args()
    obres, errors, avisos = valida(llegeix(a.csv))
    for av in avisos:
        print("avís:", av, file=sys.stderr)
    if errors:
        for e in errors:
            print("ERROR:", e, file=sys.stderr)
        sys.exit(1)
    if not obres:
        print("ERROR: el CSV no té cap obra", file=sys.stderr)
        sys.exit(1)
    text = bloc(obres)
    if a.sortida:
        with open(a.sortida, "w", encoding="utf-8") as f:
            f.write(text)
        print("%d obres escrites a %s" % (len(obres), a.sortida), file=sys.stderr)
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()

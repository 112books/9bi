#!/usr/bin/env python3
"""Genera el codi QR de la votació per imprimir (cartells de l'exposició).

Ús:
    python3 tools/qr.py [--token TOKEN] [--out fitxer.png] [--ppp 25]
    python3 tools/qr.py --url 'http://exemple.cat/v/TOKEN' --out fitxer.png

Depèn del paquet `qrcode` (només en desenvolupament) o de l'ordre `qrencode`.
Si no n'hi ha cap, imprimeix la URL perquè la generis amb qualsevol eina.
"""

import argparse
import shutil
import subprocess
import sys

MODULE_DIR = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
sys.path.insert(0, MODULE_DIR)

import app


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--token", help="secret_token de l'edició")
    ap.add_argument("--url", help="URL sencera (alternativa a --token)")
    ap.add_argument("--out", default="votacio.png")
    ap.add_argument("--ppp", type=int, default=25, help="px per punt (resolució)")
    args = ap.parse_args(argv)

    if args.url:
        url = args.url
    elif args.token:
        cfg = app.load_config()
        base = cfg.get("general", "base_url", fallback="")
        token = args.token or cfg["edicio"].get("secret_token", "")
        url = base.rstrip("/") + "/v/" + token
    else:
        cfg = app.load_config()
        base = cfg.get("general", "base_url", fallback="")
        token = cfg["edicio"].get("secret_token", "")
        url = base.rstrip("/") + "/v/" + token
        print("Sense --url ni --token: uso el config.", file=sys.stderr)

    qr_maker = _make_qr(args.ppp)
    if qr_maker is None:
        print("ERROR: cal el paquet `qrcode` o l'ordre `qrencode`.", file=sys.stderr)
        print("Instal·la: pip install qrcode   (només desenvolupament)", file=sys.stderr)
        print("O genera el QR manualment amb la URL:", url, file=sys.stderr)
        print("Exportable per a qualsevol generador:", url)
        return 1
    qr_maker(url, args.out)
    print("QR de", url, "escrit a", args.out)
    return 0


def _make_qr(ppp):
    try:
        import qrcode

        def via_qrcode(url, out):
            img = qrcode.make(url)
            img = img.resize((img.size[0], img.size[1]))
            img.save(out)
        return via_qrcode
    except ImportError:
        pass
    if shutil.which("qrencode"):
        def via_qrencode(url, out):
            subprocess.run(["qrencode", "-s", str(ppp), "-l", "L", "-o", out, url], check=True)
        return via_qrencode
    return None


if __name__ == "__main__":
    sys.exit(main())
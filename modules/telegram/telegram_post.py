#!/usr/bin/env python3
"""
telegram_post.py — publica al canal de Telegram les entrades noves del blog

Ús:
  python3 telegram_post.py [--config config.ini] [--dry-run]

Lògica:
  - Llegeix el RSS del blog
  - Per cada entrada nova (no publicada encara) amb més de `delay_hours` d'antiguitat,
    envia un missatge al canal de Telegram
  - Desa l'estat a state.json per no tornar a publicar el mateix
  - Cron recomanat: cada 15 min (*/15 * * * *)

Instal·lació al servidor:
  1. Copia aquest fitxer i config.ini a ~/apps/telegram/
  2. Omple config.ini amb el token i el chat_id
  3. Afegeix al crontab: */15 * * * * python3 ~/apps/telegram/telegram_post.py
"""

import argparse
import configparser
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / 'config.ini'
STATE_PATH  = SCRIPT_DIR / 'state.json'


def load_config(path):
    cfg = configparser.ConfigParser(interpolation=None)
    if not Path(path).exists():
        print(f'Error: no es troba el fitxer de config {path}', file=sys.stderr)
        sys.exit(1)
    cfg.read(path)
    return cfg


def load_state(path):
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return {'posted': []}


def save_state(path, state):
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')


def fetch_rss(url):
    req = urllib.request.Request(url, headers={'User-Agent': '9bi-telegram/1.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read()


def parse_rss(xml_bytes):
    root = ET.fromstring(xml_bytes)
    items = []
    for item in root.findall('.//item'):
        guid     = item.findtext('guid') or item.findtext('link') or ''
        title    = item.findtext('title') or ''
        link     = item.findtext('link') or ''
        pub_date = item.findtext('pubDate') or ''
        try:
            pub_dt = parsedate_to_datetime(pub_date)
        except Exception:
            continue
        items.append({'guid': guid, 'title': title, 'link': link, 'pub_dt': pub_dt})
    return items


def send_telegram(token, chat_id, text):
    url  = f'https://api.telegram.org/bot{token}/sendMessage'
    data = urllib.parse.urlencode({
        'chat_id':                chat_id,
        'text':                   text,
        'parse_mode':             'HTML',
        'disable_web_page_preview': 'false',
    }).encode()
    req = urllib.request.Request(url, data=data, method='POST')
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def main():
    parser = argparse.ArgumentParser(description='Publica entrades noves al canal de Telegram')
    parser.add_argument('--config',  default=str(CONFIG_PATH), help='Ruta al fitxer config.ini')
    parser.add_argument('--dry-run', action='store_true',      help='Simula sense enviar res')
    args = parser.parse_args()

    cfg     = load_config(args.config)
    token   = cfg.get('telegram', 'token')
    chat_id = cfg.get('telegram', 'chat_id')
    rss_url = cfg.get('blog', 'rss_url', fallback='https://9barrisimatge.org/index.xml')
    delay_h = cfg.getint('telegram', 'delay_hours',  fallback=1)
    max_run = cfg.getint('telegram', 'max_per_run',  fallback=3)

    if token == 'POSA_AQUI_EL_TOKEN':
        print('Error: cal configurar el token a config.ini', file=sys.stderr)
        sys.exit(1)

    state  = load_state(STATE_PATH)
    posted = set(state['posted'])

    now     = datetime.now(timezone.utc)
    cutoff  = now - timedelta(hours=delay_h)

    try:
        xml_bytes = fetch_rss(rss_url)
    except Exception as e:
        print(f'Error llegint el RSS: {e}', file=sys.stderr)
        sys.exit(1)

    items   = parse_rss(xml_bytes)
    pending = [i for i in items if i['guid'] not in posted and i['pub_dt'] <= cutoff]
    pending.sort(key=lambda i: i['pub_dt'])   # del més antic al més nou
    pending = pending[:max_run]

    if not pending:
        print('Res nou per publicar.')
        return

    for item in pending:
        text = f"<b>{item['title']}</b>\n\n{item['link']}"
        prefix = '[dry-run] ' if args.dry_run else ''
        print(f'{prefix}Publicant: {item["title"]}')
        if not args.dry_run:
            try:
                send_telegram(token, chat_id, text)
                posted.add(item['guid'])
            except urllib.error.HTTPError as e:
                body = e.read().decode()
                print(f'Error Telegram {e.code}: {body}', file=sys.stderr)
        else:
            posted.add(item['guid'])

    state['posted'] = list(posted)
    if not args.dry_run:
        save_state(STATE_PATH, state)
    print('Fet.')


if __name__ == '__main__':
    main()

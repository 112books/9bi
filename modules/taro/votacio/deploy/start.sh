#!/bin/sh
# On viu el codi del mòdul (fora del docroot) i el port on escolta.
# Per defecte, la carpeta "apps/votacio" del teu usuari.
DIR="${TARO_DIR:-$HOME/apps/votacio}"
PORT="${TARO_PORT:-8301}"
PIDFILE=$DIR/serve.pid
LOG=$DIR/serve.log

cd "$DIR" || exit 1
umask 077
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    exit 0
fi
rm -f "$PIDFILE"
nohup python3 serve.py "$PORT" >>"$LOG" 2>&1 &
echo $! >"$PIDFILE"

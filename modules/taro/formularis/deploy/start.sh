#!/bin/sh
# Arrenca el servei de formularis com a procés d'usuari i posa un
# vigilant al cron que el torna a arrencar si cau.
# DIR: on viu el codi (fora del docroot). PORT: on escolta.
DIR="${TARO_DIR:-$HOME/apps/formularis}"
PORT="${TARO_PORT:-8302}"
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

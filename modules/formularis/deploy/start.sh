#!/bin/sh
# Arrenca el servei de formularis com a procés d'usuari.
# Patró idèntic al mòdul de votació (Dinahosting no té Passenger).
DIR=/home/linuxbcn0/apps/formularis
PORT=8302
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

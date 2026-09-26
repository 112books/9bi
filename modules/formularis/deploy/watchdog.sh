#!/bin/sh
# El vigilant del cron: si el procés ha caigut, el torna a arrencar.
DIR=/home/linuxbcn0/apps/formularis
PIDFILE=$DIR/serve.pid

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    exit 0
fi
"$DIR/deploy/start.sh"

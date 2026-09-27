#!/bin/sh
DIR="${TARO_DIR:-$HOME/apps/votacio}"
PIDFILE=$DIR/serve.pid

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
    exit 0
fi
"$DIR/deploy/start.sh"

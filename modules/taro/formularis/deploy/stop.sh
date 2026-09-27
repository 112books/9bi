#!/bin/sh
DIR="${TARO_DIR:-$HOME/apps/formularis}"
PIDFILE=$DIR/serve.pid

[ -f "$PIDFILE" ] || exit 0
PID=$(cat "$PIDFILE")
if kill -0 "$PID" 2>/dev/null; then
    kill "$PID" 2>/dev/null
    sleep 1
    kill -0 "$PID" 2>/dev/null && kill -9 "$PID" 2>/dev/null
fi
rm -f "$PIDFILE"

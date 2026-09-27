#!/bin/sh
DIR="${TARO_DIR:-$HOME/apps/votacio}"
PIDFILE=$DIR/serve.pid

[ -f "$PIDFILE" ] || exit 0
kill "$(cat "$PIDFILE")" 2>/dev/null
rm -f "$PIDFILE"

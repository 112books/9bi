#!/bin/sh
DIR=/home/linuxbcn0/apps/vots-cordoncillo
PIDFILE=$DIR/serve.pid

[ -f "$PIDFILE" ] || exit 0
kill "$(cat "$PIDFILE")" 2>/dev/null
rm -f "$PIDFILE"

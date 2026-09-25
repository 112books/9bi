#!/bin/bash
# Desplegament real: pull main → build hugo → push a pages.
# Executat per autopublica (webhook). Variables:
#   AUTOPUBLICA_DEPLOY_BRANCH (main), HUGO_BASEURL (opcional)
set -euo pipefail

REPO="${AUTOPUBLICA_REPO:-$(pwd)}"
BRANCH="${AUTOPUBLICA_DEPLOY_BRANCH:-main}"
echo "[deploy] repo=$REPO branch=$BRANCH"
cd "$REPO"

echo "[deploy] git pull"
git fetch --quiet origin
git checkout --quiet "$BRANCH" 2>/dev/null || git checkout --quiet -b "$BRANCH" origin/"$BRANCH"
git pull --quiet --ff-only origin "$BRANCH"

echo "[deploy] build hugo"
HUGO=$(command -v hugo || echo "$HOME/bin/hugo")
BASEURL_OPT=""
[ -n "${HUGO_BASEURL:-}" ] && BASEURL_OPT="--baseURL $HUGO_BASEURL"
"$HUGO" --minify $BASEURL_OPT --destination /tmp/pages-deploy

echo "[deploy] push a pages"
cd /tmp/pages-deploy
git init -q -b pages
git add -A
git commit -qm "autopublica: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
PUSH_URL="${AUTOPUBLICA_PUSH_URL:-ssh://git@codeberg.org/linuxbcn/9bi.git}"
if printf '%s' "$PUSH_URL" | grep -qE '^https?://[^/]*:[^@]*@'; then
  echo "[deploy] ERROR: AUTOPUBLICA_PUSH_URL no pot dur credencials dins la URL"
  exit 1
fi
git push -f "$PUSH_URL" HEAD:pages
echo "[deploy] OK"

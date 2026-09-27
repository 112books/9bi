#!/bin/bash
# Desplegament real: pull la branca → build hugo → push a la branca de pages.
# Executat per autopublica (webhook). Variables:
#   AUTOPUBLICA_REPO           directori del clon (per defecte, on ets)
#   AUTOPUBLICA_DEPLOY_BRANCH  branca del web (per defecte: main)
#   AUTOPUBLICA_PAGES_BRANCH   branca on es puja el build (per defecte: pages)
#   AUTOPUBLICA_PUSH_URL       on es puja (OBLIGATORI, sense valor per defecte)
#   HUGO_BASEURL               opcional
#
# Si el teu web es publica amb integració contínua (GitHub Actions, GitLab CI…),
# NO necessites aquest mòdul: engega el push a la branca del web i el CI fa
# la resta. Aquest script és per a hosting que puja el build directament.
set -euo pipefail

REPO="${AUTOPUBLICA_REPO:-$(pwd)}"
BRANCH="${AUTOPUBLICA_DEPLOY_BRANCH:-main}"
PAGES_BRANCH="${AUTOPUBLICA_PAGES_BRANCH:-pages}"
echo "[deploy] repo=$REPO branch=$BRANCH"
cd "$REPO"

echo "[deploy] git pull"
git fetch --quiet origin
git checkout --quiet "$BRANCH" 2>/dev/null || git checkout --quiet -b "$BRANCH" origin/"$BRANCH"
git pull --quiet --ff-only origin "$BRANCH"

# El build es fa en un directori nou i buit: sense això, el que sobra del
# build anterior (i el .git vell) es quedaria publicat.
DEST="$(mktemp -d "${TMPDIR:-/tmp}/autopublica-build.XXXXXX")"
trap 'rm -rf "${DEST:-/nonexistent}"' EXIT

echo "[deploy] build hugo"
HUGO=$(command -v hugo || echo "$HOME/bin/hugo")
BASEURL_OPT=""
[ -n "${HUGO_BASEURL:-}" ] && BASEURL_OPT="--baseURL $HUGO_BASEURL"
"$HUGO" --minify $BASEURL_OPT --destination "$DEST"

echo "[deploy] push a $PAGES_BRANCH"
cd "$DEST"
# Historial de la branca de build: un commit nou per publicació.
git init -q -b "$PAGES_BRANCH"
git add -A
git commit -qm "autopublica: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
PUSH_URL="${AUTOPUBLICA_PUSH_URL:-}"
if [ -z "$PUSH_URL" ]; then
  echo "[deploy] ERROR: cal|AUTOPUBLICA_PUSH_URL (a on es puja el build)"
  exit 1
fi
if printf '%s' "$PUSH_URL" | grep -qE '^https?://[^/]*:[^@]*@'; then
  echo "[deploy] ERROR: AUTOPUBLICA_PUSH_URL no pot dur credencials dins la URL"
  exit 1
fi
# Force-push deliberat: la branca de build es regenera sencera a cada
# publicació i no comparteix història amb el repositori del web.
git push -f "$PUSH_URL" HEAD:"$PAGES_BRANCH"
echo "[deploy] OK"

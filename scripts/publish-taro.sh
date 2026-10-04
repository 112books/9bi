#!/usr/bin/env bash
# publish-taro.sh — publica una versió nova de Taro Photo App a Codeberg.
#
# Ús:
#   scripts/publish-taro.sh X.Y.Z ["nota de la versió"]
#
# Variables opcionals:
#   TARO_WORKTREE          worktree net (per defecte: tmp/taro-neta)
#   TARO_REMOTE            remot de Codeberg (per defecte: taro)
#   TARO_BRANCH            branca neta de treball (per defecte: taro-neta)
#   TARO_SNAPSHOT_BRANCH   branca del snapshot (per defecte: taro-public)
#   DRY_RUN=1              només comprova el build, no publica
set -euo pipefail

VERSION="${1:-}"
NOTA="${2:-}"
WT="${TARO_WORKTREE:-tmp/taro-neta}"
REMOTE="${TARO_REMOTE:-taro}"
BRANCH_SRC="${TARO_BRANCH:-taro-neta}"
BRANCH_SNAP="${TARO_SNAPSHOT_BRANCH:-taro-public}"

if [[ -z "$VERSION" ]]; then
  echo "Ús: $0 X.Y.Z [\"nota de la versió\"]" >&2
  exit 1
fi
VERSION="${VERSION#v}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WT_ABS="$ROOT/$WT"

[[ -d "$WT_ABS" ]] || { echo "No existeix el worktree $WT_ABS" >&2; exit 1; }
cd "$WT_ABS"

echo "→ Branca de treball: $BRANCH_SRC"
git checkout -q "$BRANCH_SRC"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "L'arbre de treball no és net. Fes commit o descarta els canvis abans de publicar." >&2
  git status --short >&2
  exit 1
fi

echo "→ Build de verificació..."
rm -rf public resources .hugo_build.lock
hugo --minify --environment production >/dev/null
echo "  build correcte"

if [[ "${DRY_RUN:-0}" == "1" ]]; then
  echo "→ DRY_RUN: build correcte; no es publica res."
  exit 0
fi

if git rev-parse -q --verify "refs/tags/v$VERSION" >/dev/null; then
  echo "El tag v$VERSION ja existeix. Trieu una altra versió." >&2
  exit 1
fi

echo "→ Snapshot d'un sol commit (v$VERSION)..."
git branch -D "$BRANCH_SNAP" >/dev/null 2>&1 || true
git checkout -q --orphan "$BRANCH_SNAP"
git add -A
git commit -q -m "Taro Photo App v$VERSION"
SNAP_SHA="$(git rev-parse --short HEAD)"
echo "  commit $SNAP_SHA"

echo "→ Push a $REMOTE main..."
git push --force "$REMOTE" "$BRANCH_SNAP:main"

echo "→ Tag v$VERSION..."
if [[ -n "$NOTA" ]]; then
  git tag -a "v$VERSION" -m "$NOTA"
else
  git tag -a "v$VERSION" -m "Taro Photo App v$VERSION"
fi
git push "$REMOTE" "v$VERSION"

git checkout -q "$BRANCH_SRC"
echo "✔ Taro Photo App v$VERSION publicat a Codeberg ($REMOTE/main)."

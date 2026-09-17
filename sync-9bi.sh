#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
#  9 Barris Imatge — Script de sync & gestió
#  Ús: ./sync-9bi.sh               (menú interactiu)
#      ./sync-9bi.sh status        (estat del repo)
#      ./sync-9bi.sh sync          (commit + pull --rebase + push)
#      ./sync-9bi.sh build         (build local, amb drafts)
#      ./sync-9bi.sh server        (servidor local → localhost:1313)
# ═══════════════════════════════════════════════════════════════════════

set -euo pipefail

# ── Variables ────────────────────────────────────────────────────────────
REMOTE="origin"
BRANCH_DEPLOY="main"          # branca que dispara el CI/CD (deploy.yml)
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_CODEBERG="linuxbcn/9bi"

# ── Colors i helpers ─────────────────────────────────────────────────────
RED='\033[0;31m'; GRN='\033[0;32m'; YLW='\033[1;33m'
BLU='\033[0;34m'; DIM='\033[2m'; RST='\033[0m'

print() { echo -e "${BLU}▶${RST} $1"; }
ok()    { echo -e "${GRN}✓${RST} $1"; }
err()   { echo -e "${RED}✗ Error:${RST} $1" >&2; }
warn()  { echo -e "${YLW}⚠${RST} $1"; }
dim()   { echo -e "${DIM}  $1${RST}"; }

cd "$REPO_DIR"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  err "No hi ha cap repo git aquí ($REPO_DIR)."
  exit 1
fi

# ── Funcions ─────────────────────────────────────────────────────────────
status() {
  echo ""
  CURRENT=$(git branch --show-current 2>/dev/null || echo "(sense commits)")
  print "Branca actual: ${YLW}${CURRENT}${RST}"
  echo ""
  git status --short
  echo ""
  dim "Últims commits:"
  git log --oneline -5 2>/dev/null || echo "  (encara no hi ha commits)"
  echo ""
}

has_remote() {
  git remote get-url "$REMOTE" >/dev/null 2>&1
}

sync() {
  CURRENT=$(git branch --show-current 2>/dev/null || echo "")

  if ! has_remote; then
    err "No hi ha cap remote configurat ('$REMOTE')."
    echo ""
    echo "  Crea el repositori a Codeberg i executa:"
    echo "    git remote add origin ssh://git@codeberg.org/${REPO_CODEBERG}.git"
    echo ""
    exit 1
  fi

  print "Sincronitzant amb ${REMOTE}/${CURRENT}..."
  git add -A

  if ! git diff --cached --quiet; then
    read -r -p "  Missatge del commit: " msg
    [[ -z "$msg" ]] && msg="sync: $(date '+%Y-%m-%d %H:%M')"
    git commit -m "$msg"
  else
    dim "Sense canvis nous per commitejar."
  fi

  git pull --rebase "$REMOTE" "$CURRENT" || {
    err "Pull/rebase fallat. Resol els conflictes manualment i torna a executar."
    exit 1
  }

  git push "$REMOTE" "$CURRENT" || exit 1
  ok "Sync complet → ${REMOTE}/${CURRENT}"

  if [[ "$CURRENT" != "$BRANCH_DEPLOY" ]]; then
    warn "Recorda: el CI/CD (deploy.yml) només dispara amb push a '${BRANCH_DEPLOY}'."
    warn "Quan estiguis a punt, fes: git checkout ${BRANCH_DEPLOY} i torna a sincronitzar."
  fi
}

server_local() {
  print "Arrancant servidor local (http://localhost:1313)..."
  dim "Ctrl+C per aturar."
  echo ""
  hugo server -D
}

build_local() {
  print "Build local (amb drafts)..."
  hugo --minify --buildDrafts || exit 1
  ok "Build correcte → ${REPO_DIR}/public/"
}

upload() {
  print "Refresh de data/popular.json des de GoatCounter (últims 30 dies)..."
  [[ -z "${GOATCOUNTER_API_KEY:-}" ]] && {
    err "Falta la variable GOATCOUNTER_API_KEY (GoatCounter → Settings → API keys)."
    exit 1
  }
  python3 scripts/goatcounter_popular.py --days 30 || exit 1
  ok "data/popular.json actualitzat."
}

# ── Modo no interactiu ───────────────────────────────────────────────────
case "${1:-menu}" in
  status) status; exit 0 ;;
  sync)   sync;   exit 0 ;;
  build)  build_local; exit 0 ;;
  server) server_local; exit 0 ;;
esac

# ── Menú interactiu ──────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " 9 Barris Imatge — Sync & Gestió"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
CURRENT=$(git branch --show-current 2>/dev/null || echo "?")
echo -e " Branca: ${YLW}${CURRENT}${RST}"
echo ""
echo " 1) Status"
echo " 2) Sync automàtic (commit + pull --rebase + push)"
echo " 3) Servidor local → localhost:1313"
echo " 4) Build local (hugo --minify, amb drafts)"
echo " 5) Refresca els articles més visitats (GoatCounter)"
echo "───────────────────────────────────────"
echo " 0) Sortir"
echo ""

read -r -p "Opció: " opt
echo ""

case $opt in
  1) status ;;
  2) sync ;;
  3) server_local ;;
  4) build_local ;;
  5) upload ;;
  0) exit 0 ;;
  *) err "Opció no vàlida: '${opt}';" exit 1 ;;
esac

echo ""
#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
#  9 Barris Imatge — Script de sync & gestió
#  Ús: ./sync-9bi.sh               (menú interactiu)
#      ./sync-9bi.sh status        (estat del repo, local i remot)
#      ./sync-9bi.sh sync          (commit + pull --rebase + push a main)
#      ./sync-9bi.sh deploy        (build staging + push a 'pages' → producció)
#      ./sync-9bi.sh build         (build local, amb drafts)
#      ./sync-9bi.sh server        (servidor local → localhost:1313)
#
#  Nota sobre el deploy real (2026-09-17): Forgejo Actions no té runner
#  disponible al repo, així que un push a 'main' NO publica el lloc.
#  La publicació la fa la branca 'pages' (build local) + un webhook
#  configurat al repo. Per això 'sync' i 'deploy' són passos separats.
# ═══════════════════════════════════════════════════════════════════════

set -euo pipefail

# ── Variables ────────────────────────────────────────────────────────────
REMOTE="origin"
BRANCH_DEPLOY="main"          # branca de codi font
BRANCH_PAGES="pages"          # branca que serveix Codeberg Pages (via webhook)
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_CODEBERG="linuxbcn/9bi"
REPO_SSH="ssh://git@codeberg.org/${REPO_CODEBERG}.git"
SITE_URL="https://linuxbcn.codeberg.page/9bi/"
DEPLOY_LOG="${REPO_DIR}/.deploy-log"

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

has_remote() {
  git remote get-url "$REMOTE" >/dev/null 2>&1
}

# ── Estat ────────────────────────────────────────────────────────────────
# Només lectura: git fetch actualitza les refs remote-tracking (origin/*),
# no toca la branca local ni el working tree. No esborra ni sobreescriu res.
status() {
  echo ""
  CURRENT=$(git branch --show-current 2>/dev/null || echo "(sense commits)")
  print "Branca actual: ${YLW}${CURRENT}${RST}"
  echo ""
  git status --short
  echo ""
  dim "Últims commits (local):"
  git log --oneline -5 2>/dev/null || echo "  (encara no hi ha commits)"
  echo ""

  if has_remote; then
    print "Comparant amb ${REMOTE} (fetch, no modifica res local)..."
    if git fetch --quiet "$REMOTE" "$BRANCH_DEPLOY" "$BRANCH_PAGES" 2>/dev/null; then
      if git rev-parse --verify -q "${REMOTE}/${BRANCH_DEPLOY}" >/dev/null; then
        AHEAD=$(git rev-list --count "${REMOTE}/${BRANCH_DEPLOY}..${BRANCH_DEPLOY}" 2>/dev/null || echo "?")
        BEHIND=$(git rev-list --count "${BRANCH_DEPLOY}..${REMOTE}/${BRANCH_DEPLOY}" 2>/dev/null || echo "?")
        dim "${BRANCH_DEPLOY} local vs ${REMOTE}/${BRANCH_DEPLOY}: ${AHEAD} per pujar · ${BEHIND} per baixar"
      fi
      if git rev-parse --verify -q "${REMOTE}/${BRANCH_PAGES}" >/dev/null; then
        LAST_DEPLOY=$(git log -1 --format="%h · %ci · %s" "${REMOTE}/${BRANCH_PAGES}" 2>/dev/null)
        dim "Últim deploy publicat ('${BRANCH_PAGES}'): ${LAST_DEPLOY}"
      else
        dim "Encara no hi ha branca '${BRANCH_PAGES}' al remot (cap deploy fet)."
      fi
    else
      warn "No s'ha pogut contactar amb ${REMOTE} (sense connexió?)."
    fi
    echo ""
  fi

  if [[ -f "$DEPLOY_LOG" ]]; then
    dim "Historial de deploys (local, ${DEPLOY_LOG##*/}):"
    tail -5 "$DEPLOY_LOG" | sed 's/^/  /'
    echo ""
  fi
}

# ── Sync del codi font (main) ───────────────────────────────────────────
sync() {
  CURRENT=$(git branch --show-current 2>/dev/null || echo "")

  if ! has_remote; then
    err "No hi ha cap remote configurat ('$REMOTE')."
    echo ""
    echo "  Crea el repositori a Codeberg i executa:"
    echo "    git remote add origin ${REPO_SSH}"
    echo ""
    exit 1
  fi

  print "Sincronitzant codi font amb ${REMOTE}/${CURRENT}..."
  git add -A

  if ! git diff --cached --quiet; then
    echo ""
    git status --short
    echo ""
    read -r -p "  Nom d'aquest commit: " msg
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

  if [[ "$CURRENT" == "$BRANCH_DEPLOY" ]]; then
    warn "Això puja el codi font, però NO publica el lloc."
    warn "Per publicar els canvis, executa: ./sync-9bi.sh deploy"
  fi
}

# ── Deploy real a producció (build → branca 'pages') ────────────────────
# Fa servir un directori temporal per al build, independent del repo local:
# no toca 'main' ni cap fitxer del working tree. Només force-pusha la
# branca 'pages' remota (branca de sortida generada, no de codi font).
deploy() {
  if [[ -n "$(git status --short)" ]]; then
    warn "Hi ha canvis sense commitejar/pujar a '${BRANCH_DEPLOY}'."
    warn "El deploy publica el que hi ha ARA als fitxers locals, encara que no estigui pujat a main."
    read -r -p "  Continuar igualment? (s/N) " cont
    [[ "$cont" != "s" && "$cont" != "S" ]] && { dim "Deploy cancel·lat."; return 0; }
    echo ""
  fi

  read -r -p "  Nom d'aquest deploy (p.ex. 'header x2 + graella 4x2'): " label
  [[ -z "$label" ]] && label="deploy $(date '+%Y-%m-%d %H:%M')"

  BUILD_DIR="$(mktemp -d "${TMPDIR:-/tmp}/9bi-deploy.XXXXXX")"
  print "Build de producció a ${BUILD_DIR}..."
  if ! hugo --minify --environment staging --destination "$BUILD_DIR"; then
    err "Build fallat. Deploy avortat, cap canvi remot."
    rm -rf "$BUILD_DIR"
    exit 1
  fi
  ok "Build correcte."

  echo ""
  warn "Ara es farà un push forçat (force-push) a la branca remota '${BRANCH_PAGES}'."
  warn "Això reemplaça el contingut publicat; NO afecta 'main' ni cap altra branca."
  read -r -p "  Confirmes el deploy \"${label}\"? (s/N) " confirm
  if [[ "$confirm" != "s" && "$confirm" != "S" ]]; then
    dim "Deploy cancel·lat."
    rm -rf "$BUILD_DIR"
    return 0
  fi

  USER_NAME="$(git config user.name || echo "9bi")"
  USER_EMAIL="$(git config user.email || echo "noreply@9barrisimatge.org")"

  (
    cd "$BUILD_DIR"
    git init -q -b "$BRANCH_PAGES"
    git add -A
    git -c user.name="$USER_NAME" -c user.email="$USER_EMAIL" commit -qm "$label"
    git push -f "$REPO_SSH" "HEAD:${BRANCH_PAGES}"
  ) || {
    err "Push a '${BRANCH_PAGES}' fallat."
    rm -rf "$BUILD_DIR"
    exit 1
  }

  rm -rf "$BUILD_DIR"
  echo "$(date '+%Y-%m-%d %H:%M')  ${label}  (font: $(git rev-parse --short HEAD))" >> "$DEPLOY_LOG"
  ok "Deploy complet: \"${label}\" → ${SITE_URL}"
  dim "El webhook de Forgejo publica el lloc en pocs segons."
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
  deploy) deploy; exit 0 ;;
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
echo " 1) Status (local + remot, no modifica res)"
echo " 2) Sync codi font (commit + pull --rebase + push a main)"
echo " 3) Deploy a producció (build + push a 'pages', amb confirmació)"
echo " 4) Servidor local → localhost:1313"
echo " 5) Build local (hugo --minify, amb drafts)"
echo " 6) Refresca els articles més visitats (GoatCounter)"
echo "───────────────────────────────────────"
echo " 0) Sortir"
echo ""

read -r -p "Opció: " opt
echo ""

case "$opt" in
  1) status ;;
  2) sync ;;
  3) deploy ;;
  4) server_local ;;
  5) build_local ;;
  6) upload ;;
  0) exit 0 ;;
  *) err "Opció no vàlida: '${opt}'"; exit 1 ;;
esac

echo ""

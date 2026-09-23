#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
#  9 Barris Imatge — Script de sync & gestió
#  Ús: ./sync-9bi.sh               (menú interactiu)
#      ./sync-9bi.sh status        (estat del repo, local i remot)
#      ./sync-9bi.sh sync          (commit + pull --rebase + push a main)
#      ./sync-9bi.sh deploy [staging|production]   (build + push a 'pages', per entorn)
#      ./sync-9bi.sh deploy-prod   (atall: deploy production)
#      ./sync-9bi.sh build         (build local, amb drafts)
#      ./sync-9bi.sh server        (servidor local → localhost:1313)
#
#  Entorns (baseURL de cada un, vegeu config/<env>/hugo.toml):
#    local      → http://localhost:1313/            comanda: server / hugo server -D
#    staging    → https://linuxbcn.codeberg.page/9bi/   comanda: deploy staging
#    production → https://9barrisimatge.org/        comanda: deploy production / deploy-prod
#    taro (app) → allotjament propi (LinuxBCN/Dinahosting), NO es desplega aquí.
#  Com es construeixen les URLs: tots els enllaços interns i imatges usen
#  `relURL` amb el baseURL de l'entorn actiu (hooks render-image / rel.html),
#  de manera que el mateix contingut es publica correctament a qualsevol entorn.
#
#  Nota sobre el deploy real (2026-09-17): Forgejo Actions no té runner
#  disponible al repo, així que un push a 'main' NO publica el lloc.
#  La publicació la fa la branca 'pages' (build local) + un webhook
#  configurat al repo. Per això 'sync' i 'deploy' són passos separats.
#  ⚠ El domini (production) es publica via un webhook propi de git-pages
#  (TXT _git-pages-repository → linuxbcn/9bi.git); si el domini no es
#  refresca, cal revisar el webhook del domini a Settings → Webhooks.
# ═══════════════════════════════════════════════════════════════════════

set -euo pipefail

# ── Variables ────────────────────────────────────────────────────────────
REMOTE="origin"
BRANCH_DEPLOY="main"          # branca de codi font
BRANCH_PAGES="pages"          # branca que serveix Codeberg Pages (via webhook)
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_CODEBERG="linuxbcn/9bi"
REPO_SSH="ssh://git@codeberg.org/${REPO_CODEBERG}.git"
DEPLOY_LOG="${REPO_DIR}/.deploy-log"

# Entorns de desplegament (build `hugo --environment <env>` → baseURL).
#   staging    → https://linuxbcn.codeberg.page/9bi/   (previsualització)
#   production → https://9barrisimatge.org/            (domini real)
# L'entorn determina com es construeixen les URLs (vegeu config/<env>/hugo.toml).
ENV_STAGING="staging"
ENV_PROD="production"

# Defineix la URL de publicació per entorn (per als missatges i el log).
env_url() {
  case "$1" in
    "$ENV_STAGING") echo "https://linuxbcn.codeberg.page/9bi/" ;;
    "$ENV_PROD")    echo "https://9barrisimatge.org/" ;;
    *)              echo "??" ;;
  esac
}

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

# ── Deploy real (build → branca 'pages'), per entorn ────────────────────
# Ús: deploy [staging|production]  — entorn per defecte: staging
# Deploy INCREMENTAL (canvi 2026-09-21, motiu quota de Codeberg):
# ANTES es feia 'git init' + force-push d'un snapshot complet del build
# (~160 MiB) a cada deploy; els snapshots anteriors quedaven com a objectes
# orfes al servidor i feien créixer la quota fins a superar els 750 MiB.
# ARA es manté un CLON persistent de la branca 'pages' a ~/.cache/9bi-pages,
# es reseteja a l'últim publicat i s'hi sincronitza el build: el push és
# NORMAL (fast-forward) i només es pugen els objectes que realment canvien.
# Els blobs que no canvien es reutilitzen (mateix hash) → creixement mínim.
deploy() {
  local ENV="${1:-$ENV_STAGING}"
  case "$ENV" in
    "$ENV_STAGING"|"$ENV_PROD") ;;
    *) err "Entorn desconegut: '$ENV'. Usa 'staging' o 'production'."; exit 1 ;;
  esac
  local SITE_URL; SITE_URL="$(env_url "$ENV")"

  if [[ -n "$(git status --short)" ]]; then
    warn "Hi ha canvis sense commitejar/pujar a '${BRANCH_DEPLOY}'."
    warn "El deploy publica el que hi ha ARA als fitxers locals, encara que no estigui pujat a main."
    read -r -p "  Continuar igualment? (s/N) " cont
    [[ "$cont" != "s" && "$cont" != "S" ]] && { dim "Deploy cancel·lat."; return 0; }
    echo ""
  fi

  PAGES_CACHE="${HOME}/.cache/9bi-pages"
  if [[ ! -d "$PAGES_CACHE/.git" ]]; then
    print "Primera vegada: clonant la branca '${BRANCH_PAGES}' a ${PAGES_CACHE}..."
    git clone -q --branch "$BRANCH_PAGES" --single-branch "$REPO_SSH" "$PAGES_CACHE" || {
      err "No s'ha pogut clonar ${REPO_SSH}. Revisa quota/connexió."
      exit 1
    }
  fi

  read -r -p "  Nom d'aquest deploy (p.ex. 'header x2 + graella 4x2'): " label
  [[ -z "$label" ]] && label="deploy $(date '+%Y-%m-%d %H:%M')"

  BUILD_DIR="$(mktemp -d "${TMPDIR:-/tmp}/9bi-deploy.XXXXXX")"
  print "Build amb l'entorn '${ENV}' a ${BUILD_DIR}..."
  if ! hugo --minify --environment "$ENV" --destination "$BUILD_DIR"; then
    err "Build fallat. Deploy avortat, cap canvi remot."
    rm -rf "$BUILD_DIR"
    exit 1
  fi
  ok "Build correcte (${ENV}) → ${SITE_URL}"

  echo ""
  warn "Es farà un deploy incremental (només els fitxers que canvien) a la branca '${BRANCH_PAGES}'."
  warn "El clon persistent es resetejarà a l'últim publicat abans de sincronitzar-hi el build."
  read -r -p "  Confirmes el deploy \"${label}\" a '${ENV}'? (s/N) " confirm
  if [[ "$confirm" != "s" && "$confirm" != "S" ]]; then
    dim "Deploy cancel·lat."
    rm -rf "$BUILD_DIR"
    return 0
  fi

  print "Sincronitzant el clon de '${BRANCH_PAGES}' amb el remot..."
  git -C "$PAGES_CACHE" fetch -q origin "$BRANCH_PAGES"
  git -C "$PAGES_CACHE" reset -q --hard "origin/${BRANCH_PAGES}"
  git -C "$PAGES_CACHE" clean -qfd

  print "Copiant el build al clon (eliminant fitxers que ja no hi són)..."
  rsync -a --delete --exclude='.git/' "$BUILD_DIR"/ "$PAGES_CACHE"/

  USER_NAME="$(git config user.name || echo "9bi")"
  USER_EMAIL="$(git config user.email || echo "noreply@9barrisimatge.org")"

  (
    git -C "$PAGES_CACHE" add -A
    git -C "$PAGES_CACHE" -c user.name="$USER_NAME" -c user.email="$USER_EMAIL" \
      commit -qm "$label"
  ) || { err "Commit al clon fallat."; exit 1; }

  print "Push incremental a '${BRANCH_PAGES}'..."
  git -C "$PAGES_CACHE" push origin "$BRANCH_PAGES" || {
    err "Push a '${BRANCH_PAGES}' fallat. Si és per quota de Codeberg, cal tenir"
    err "aprovada la petició '[STORAGE]' a Codeberg-e.V./requests (vegeu drafts/2026-09-21-quota-codeberg.md)."
    exit 1
  }

  rm -rf "$BUILD_DIR"
  echo "$(date '+%Y-%m-%d %H:%M')  [${ENV}] ${label}  (font: $(git rev-parse --short HEAD))" >> "$DEPLOY_LOG"
  ok "Deploy complet: \"${label}\" → ${SITE_URL}"
  dim "El webhook de Forgejo publica el lloc en pocs segons."
}

# Alias shortcuts
deploy-prod() { deploy "$ENV_PROD"; }

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
  deploy) deploy "${2:-staging}"; exit 0 ;;
  deploy-prod) deploy "production"; exit 0 ;;
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
echo " 3) Deploy a staging (build + push a 'pages' → linuxbcn.codeberg.page/9bi/)"
echo " 4) Deploy a producció (build + push a 'pages' → 9barrisimatge.org)"
echo " 5) Servidor local → localhost:1313"
echo " 6) Build local (hugo --minify, amb drafts)"
echo " 7) Refresca els articles més visitats (GoatCounter)"
echo "───────────────────────────────────────"
echo " 0) Sortir"
echo ""

read -r -p "Opció: " opt
echo ""

case "$opt" in
  1) status ;;
  2) sync ;;
  3) deploy "staging" ;;
  4) deploy "production" ;;
  5) server_local ;;
  6) build_local ;;
  7) upload ;;
  0) exit 0 ;;
  *) err "Opció no vàlida: '${opt}'"; exit 1 ;;
esac

echo ""

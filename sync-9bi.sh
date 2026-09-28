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
REMOTE="github"
BRANCH_DEPLOY="main"          # branca de codi font
BRANCH_PAGES="pages"          # branca llegada de Codeberg Pages (legacy, no s'usa)
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_GITHUB="112books/9bi"
REPO_SSH="https://github.com/${REPO_GITHUB}.git"
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
    echo "  Afegeix el remote de GitHub:"
    echo "    git remote add github ${REPO_SSH}"
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
    ok "GitHub Actions construeix i publica el lloc automàticament."
  fi
}

# ── Deploy (desactivat — producció via GitHub Actions) ───────────────────
# Des del 2026-09-24 producció = GitHub Pages. Un push a 'github main' dispara
# .github/workflows/deploy.yml que construeix i publica sol.
# El deploy incremental a Codeberg (branca 'pages') queda suspès fins que
# la quota de Codeberg es resolgui (issue #2522).
deploy() {
  warn "El deploy a Codeberg està desactivat (quota bloquejada)."
  warn "Per publicar: git push github main → GitHub Actions construeix i publica."
}

deploy-prod() { deploy; }

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

# ── Estadístiques del web (/stats/) ──────────────────────────────────────
# Genera static/stats/analytics.json des de GoatCounter per al dashboard
# estàtic de /stats/. Es crida automàticament al deploy de PRODUCCIÓ (abans
# del build) i es pot invocar manualment. Se salta (warn) si manca la clau
# o l'API no respon: mai no ha de bloquejar un deploy.
refresh_stats() {
  print "Refresh de static/stats/analytics.json des de GoatCounter..."
  [[ -z "${GOATCOUNTER_API_KEY:-}" ]] && {
    warn "Falta GOATCOUNTER_API_KEY → no es refresca /stats/ (es desplega l'últim analytics.json)."
    return 0
  }
  if python3 scripts/fetch_9bi_analytics.py --days 30; then
    ok "static/stats/analytics.json actualitzat."
  else
    warn "Refresh d'estadístiques fallat → es desplega l'últim analytics.json."
  fi
}

# ── Modo no interactiu ───────────────────────────────────────────────────
case "${1:-menu}" in
  status) status; exit 0 ;;
  sync)   sync;   exit 0 ;;
  deploy) deploy "${2:-staging}"; exit 0 ;;
  deploy-prod) deploy "production"; exit 0 ;;
  stats)  refresh_stats; exit 0 ;;
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
echo " 3) Deploy a staging  [desactivat — Codeberg quota bloquejada]"
echo " 4) Deploy a producció [desactivat — usa: git push github main]"
echo " 5) Servidor local → localhost:1313"
echo " 6) Build local (hugo --minify, amb drafts)"
echo " 7) Refresca els articles més visitats (GoatCounter)"
echo " 8) Refresca les estadístiques del web (/stats/)"
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
  8) refresh_stats ;;
  0) exit 0 ;;
  *) err "Opció no vàlida: '${opt}'"; exit 1 ;;
esac

echo ""

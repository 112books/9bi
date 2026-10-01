# CLAUDE.md — 9 Barris Imatge

Documentació per a sessions de Claude. Només fets verificats dels fitxers del projecte.

> **Historial de sessions**: [`gestio/SESSIONSLOG.md`](gestio/SESSIONSLOG.md)
> **Recerca** (fotògrafs, concurs Cordoncillo): [`gestio/RECERCA.md`](gestio/RECERCA.md)
> **Tasques pendents**: [`.taques/TASQUES.md`](.taques/TASQUES.md)

- **Demanar permís abans d'inventar**: cal demanar permís per vols inventar creativament coses (textos, funcionalitats, disseny, etiquetes…). Quan hem consensuat un pla cal aplicar-lo sense tonteries (sense re-verificar el que ja està verificat i registrat), a no ser que puguis trencar res — en aquest cas aturar i avisar abans.

## REGLA PRIMERA (obligatòria)

- **No implementar mai res pel meu compte.** Ni contingut, ni textos, ni disseny, ni enllaços, ni estructures noves. Els suggeriments són benvinguts, però **cal presentar-los i esperar una aprovació explícita de l'usuari abans de tocar cap fitxer.**
- **No inventar fets** (dates, dades, textos, noms) ni afegir frases "de farciment" no demanades.
- **No canviar el disseny** (colors, bandes, marges, tipografia, ordre, components) sense aprovació explícita, tant per fer canvis nous com per revertir els existents.
- Si quelcom és ambigu, **preguntar**; no assumir ni improvisar.
- El rigor per sobre de la velocitat: verificar sempre a `content/` i `layouts/` abans de donar per fet què hi ha.
- **Serveis externs**: abans de provar un servei extern nou, cal estudiar-ne totes les condicions d'ús i documentar-ho a `gestio/` o `drafts/` (lligó de la quota de Codeberg, 2026-09-21).

## Protocol d'inici de sessió (obligatori)

A l'inici de **cada** sessió, abans de treballar:

1. **Sincronitzar els repositoris**: `git fetch origin` i comprovar que `main` estigui al dia.
2. **Iniciar la gestió d'hores**: activar/enregistrar el temps (skill `time-tracker`, `.taques/`).
3. **Recompte del web**: nombre de posts i membres (GoatCounter per a usuaris).

## Loop de tasques (definit per l'usuari, 2026-09-24)

Quan l'usuari demani «loop de tasques» o «seguim amb les tasques pendents»:

1. **Llistar** les tasques pendents de `.taques/TASQUES.md` amb l'estat real verificat (no assumir res). En tancar-ne una, moure-la a «Fetes» amb data, temps i commit.
2. **Pensar la millor manera** de fer la tasca i **fer-la** (amb aprovació explícita abans de tocar fitxers/disseny).
3. **Verificar** (build + navegació real + desplegament). **Si no passa la verificació, arreglar-ho** i repetir.
4. **Si no es pot seguir per faltar una decisió**: congelar la tasca (anotar el que falta i per què), avisar, i passar a la següent.
5. Repetir fins acabar la llista.

## El projecte

Lloc web estàtic del **Col·lectiu 9 Barris Imatge** (Barcelona), migrat de Blogger a Hugo + PaperMod i publicat a GitHub Pages.

## Estat real (verificat el 2026-10-01)

- Producció: `https://9barrisimatge.org/`, desplegada per `.github/workflows/deploy.yml` des del push a `main`.
- Repositori de producció i CMS: **GitHub `112books/9bi`** (`main`). Publicació: `git push origin main`.
- Remotes locals: `origin` = GitHub (`git@github.com:112books/9bi.git`); `codeberg` = Codeberg (backup, push bloquejat per quota).
- **Codeberg `linuxbcn/9bi`**: backup read-only. GC demanat a issue #2522 (comentari 28/09); sense resposta. Branca `pages` esborrada el 28/09. Compte a 752,7 MiB.
- Tema PaperMod vendored a `themes/PaperMod/`.
- **Posts actuals**: 3.009 (3.006 migrats de Blogger + 3 articles nous), 20 carpetes d'anys (2008–2026).

## Comandes

- Servei local: `hugo server -D` → http://localhost:1313
- Build: `hugo --minify` → `public/`
- Stats locals: `python3 scripts/fetch_9bi_analytics.py` (requereix `GOATCOUNTER_API_KEY`)
- Més visitats: `python3 scripts/goatcounter_popular.py --days 30` (requereix `GOATCOUNTER_API_KEY`)

## Versions (verificades)

- Hugo **0.164.0 extended** (fixada a `.github/workflows/deploy.yml`)
- Sveltia CMS **0.217.0** (autoallotjat a `static/admin/sveltia-cms.js`)

## Configuració (`hugo.toml`)

- `baseURL` **https://9barrisimatge.org/** (producció) · title "9 Barris Imatge" · `locale ca` · `timeZone Europe/Madrid`
- `uglyURLs = true` · `[permalinks] posts = "/:year/:month/:slug"` · `paginate = 24`
- `[markup.goldmark.renderer] unsafe = true` · `[markup.goldmark.parser.attribute] block = true`
- Taxonomies: `tag → tags`, `category → categories`, `author → author`
- `params`: `defaultTheme = "dark"`, ShowPostAuthors=true, ShowBreadCrumbs=false, ShowReadingTime=false, ShowShareButtons=false, ShowPostNavLinks=true, ShowCodeCopyButtons=true, ShowWordCount=false, comments=false
- `menu.main`: Inici(/), Arxiu(/archive/), Qui som(/qui-som/), El Concurs(/concurs/), FAQ(/faq/), Cerca(/search/), Contacte(/contacte/) — **la Guia NO hi és** (interna, a `/guia/`, `noindex`)
- `menu.footer`: Arxiu 9bi, Etiquetes/Tags, Més visitats, Estadístiques del web, Cerca

## Estructura de fitxers (verificada)

```
content/
├── posts/YYYY/                  # posts en subcarpetes per any; URL depèn del front matter (permalinks /:year/:month/:slug)
├── qui-som.md, concurs.md, contacte.md, privacitat.md, avis-legal.md, cookies.md, credits.md
├── subvencions.md               # url: /qui-som/subvencions/ (pàgina filla)
├── search.md (layout "search"), archive.md (layout "archives")
├── mes-visitats.md (layout "popular" + hiddenInRss: true)
├── guia/                        # _index.md + 7 subpàgines: robotsNoIndex + hiddenInRss + sitemap.disable
└── documentacio/                # draft: true (interna)
layouts/
├── baseof.html                  # SOBREESCRIT: clau de caché del footer
├── single.html                  # SOBREESCRIT: h1 amb visualTitle si el front matter el porta; header_image a tot l'ample
├── index.html                   # portada en mosaic (grid de fotos, paginat)
├── archives.html                # arxiu + índex d'anys a la dreta
├── taxonomy.html                # SOBREESCRIT: núvol d'etiquetes (/tags/)
├── 404.html                     # SOBREESCRIT: 404 útil amb cerca directa
├── author/term.html             # pàgina de posts per autor (mosaic paginat)
├── _shortcodes/membres.html     # taula de membres (actius + antics)
├── _shortcodes/rel.html         # {{< rel "/ruta" >}} → relURL base-aware
├── _default/popular.html        # llista de més visitats (llegeix data/popular.json)
├── _markup/render-image.html    # reescriu rutes d'imatge que comencen per «/» amb relURL
└── _partials/
    ├── header.html              # SOBREESCRIT: icones SVG per .Identifier + sticky + franja vermella
    ├── footer.html              # SOBREESCRIT: banda accent + 5 columnes + CC + count-up + reveal
    ├── post-share.html          # botons de compartir per entrada (WhatsApp, Telegram, FB, correu, copia)
    ├── post-comments.html       # llista de comentaris + formulari (moderació prèvia)
    ├── seo-title.html           # títol SEO: seoTitle o title sense prefix de data
    ├── head.html                # SOBREESCRIT: usa seo-title.html
    ├── extend_head.html         # preload de fonts + GoatCounter → 9bi.goatcounter.com
    ├── extend_footer.html       # BUIT
    └── extend_post_content.html # botó "Veure tot l'àlbum de fotos" (si album_url)
assets/css/extended/custom.css  # mosaic, tipografies, peu, formulari, membres, 404, concurs…
static/admin/{config.yml,index.html,sveltia-cms.js}
static/images/                  # imatges (media_folder del CMS)
static/stats/                   # dashboard /stats/ (Chart.js + analytics.json, noindex)
data/membres/                   # un fitxer .yml per membre (autor, nom, malnom, web, instagram, actiu)
data/popular.json               # top visites (generat per goatcounter_popular.py)
data/comentaris/                # comentaris aprovats (JSON per post, creats via API GitHub)
gestio/SESSIONSLOG.md           # historial detallat de sessions
gestio/RECERCA.md               # recerca: fotògrafs de NB, cronologia concurs Cordoncillo
.github/workflows/deploy.yml    # CI/CD: push a main + cron cada 6 h
.taques/TASQUES.md              # font única de tasques pendents
```

## Front matter (convencions reals)

- **Posts**: `title`, `date` (ISO), `year` (any), `author`, `slug` (obligatori, estable), `tags` (llista), `cover.image` (opcional, `/images/covers/…`), `album_url` (opcional), `description` (opcional = meta SEO), `seoTitle` (opcional = títol SEO sense prefix data)
- **Pàgines**: `title`, `description`, `url` (ruta final explícita)
- **Guia**: `robotsNoIndex: true` + `hiddenInRss: true` + `sitemap.disable: true`
- **Documentació**: `draft: true`

## Sveltia CMS (`static/admin/config.yml`)

- Backend `github`: repo `112books/9bi`, branca `main`. Entrada: PAT classic (scope `repo`) via «Sign In with Token».
- `media_folder: static/images` · `public_folder: /images`
- **32 col·leccions**: 19 d'articles per any (`posts-YYYY`, carpetes físiques `content/posts/YYYY/`, `sortable_fields: date desc`), `web-pages` (13 pàgines fixes, camps tècnics com a `hidden`), `guia`, `actes`, `concurs`, `membres`, 8 col·leccions «Àlbums per arreglar».
- **Cap col·lecció «Tots els articles»**: els 3.009 posts feien trigar el carregament; s'usa la cerca immediata del Sveltia.
- **Rail propi** (`static/admin/index.html`): lateral nativa amagada (`#nc-root .primary-sidebar { display:none !important }` + `MutationObserver`); `<aside class="cms-rail">` amb desplegable d'anys 2026→2008, Documentació, Àlbums (per login a `CMS_ALBUMS`), Administració.
- **`CMS_AUTHORS`**: mapeja login GitHub → nom d'autor (hook `preSave`). Cal afegir cada editor nou.
- **`CMS_ALBUMS`**: mapeja login → col·lecció de recuperació. Ara: `112books` → `recuperacio-joan-linux`.
- Peu del CMS: filet vermell + CC + «Powered by LinuxBCN with Hugo & PaperMod».

## CI/CD (`.github/workflows/deploy.yml`)

- Trigger: **push a `main`** + cron `0 */6 * * *` (cada 6 h per refrescar /stats/) + `workflow_dispatch`
- Steps: checkout → Hugo 0.164.0 → `fetch_9bi_analytics.py` (si `GOATCOUNTER_API_KEY`) → `goatcounter_popular.py` → `hugo --minify --environment production` → deploy GitHub Pages
- **Avisos no bloquejants**: Node.js 20 obsolet a les accions; `ubuntu-latest` migrarà a Ubuntu 26 el 19/10/2026. (T-21 pendent: SHA-pin de les accions.)

## Servidor (Dinahosting — `linuxbcn0`)

- Host: `vl28359.dinaserver.com` (82.98.166.123). SSH: compte **`linuxbcn0`**, key `id_ed25519`.
- **`konsento`/`naubostik` és un compte diferent — no tocar mai.**
- Dinahosting acaba el TLS davant d'Apache i envia `X-Forwarded-Proto`. **No usar `%{HTTPS}` sol** per redirigir (bucle 301); cal comprovar les dues condicions als `.htaccess`.
- Regla del proveïdor: **cap document públic ha de dir «Dinahosting»**. LinuxBCN ofereix l'allotjament com a servei propi.
- **Serveis actius**:
  - `vots-cordoncillo.linuxbcn.com` → `~/apps/vots-cordoncillo/` (port 8301). S'obre **01/12/2026 00:00**, es tanca **15/12/2026 23:59:59**. Geofence: lat 41.441623, lon 2.179794, radi 500 m (Casal de Barri de Prosperitat). **BBDD buida** (0 vots). **T-01 CRÍTIC**: substituir les 100 obres de prova per la llista definitiva abans del 30/11.
  - `formularis.linuxbcn.com` → `~/apps/formularis/` (port 8302). SMTP: `9barrisimatge-org.correoseguro.dinaserver.com:465`.
  - Certificat SSL: vàlid fins al **27/12/2026** (SAN: vots-cordoncillo, formularis, linuxbcn.com, www).
  - Telegram: `~/apps/telegram/telegram_post.py`, cron 30 min, llegeix `/posts/index.xml`. `state.json` amb 3.008 guids marcats — **no tocar ni esborrar**.
  - Comentaris: `~/apps/formularis/comentaris.py`, `github_token` fine-grained (Contents RW de `112books/9bi`).

## Decisions clau (per no repetir debats)

- **Col·lectiu, mai «associació»**: el nom legal és «Col·lectiu 9 Barris Imatge».
- **Slug estable**: el camp `slug` no s'ha de tocar un cop publicat; el canvi trenca l'URL. Hi ha un avís al CMS i un hook que el recupera si queda buit.
- **Antics membres** (no «veterans»): el terme per al grup `actiu: false`.
- **No hi ha col·lecció «Tots els articles»** al CMS: massa lent amb 3.009 posts.
- **`analytics.json` al repo és el fallback**: la versió desplegada es genera en cada CI run. Si GoatCounter retorna buit, el script **conserva el fitxer existent** (no actualitza). Diagnòstic si /stats/ va enrere: comprovar el secret `GOATCOUNTER_API_KEY` a GitHub Actions i els logs del workflow.
- **Codeberg = backup read-only**: producció és GitHub. No fer push ni reset a Codeberg fins que el GC alliberi quota (issue #2522).

## Problemes coneguts / pendents

> Font única: [`.taques/TASQUES.md`](.taques/TASQUES.md).

- **T-01 🔴**: llista definitiva d'obres de la votació — termini **30/11/2026**.
- **T-29 🟡**: publicar la versió distribuïble de Taro a Codeberg, bloquejada per GC.
- **T-28 🟡**: CSS trencats a l'staging de Codeberg (lligat a T-29).
- **T-07 🟡**: convidar editors al CMS amb accés Write.
- La resta a TASQUES.md.

# CLAUDE.md — 9 Barris Imatge

Documentació per a sessions de Claude. Només fets verificats dels fitxers del projecte.

- **Demanar permís abans d'inventar**: cal demanar permís per vols inventar creativament coses (textos, funcionalitats,
  disseny, etiquetes…). Quan hem consensuat un pla cal aplicar-lo sense tonteries (sense re-verificar el que ja està
  verificat i registrat), a no ser que puguis trencar res — en aquest cas aturar i avisar abans.
## REGLA PRIMERA (obligatòria)

- **No implementar mai res pel meu compte.** Ni contingut, ni textos, ni disseny, ni enllaços, ni estructures noves. Els suggeriments són benvinguts, però **cal presentar-los i esperar una aprovació explícita de l'usuari abans de tocar cap fitxer.**
- **No inventar fets** (dates, dades, textos, noms) ni afegir frases "de farciment" no demanades.
- **No canviar el disseny** (colors, bandes, marges, tipografia, ordre, components) sense aprovació explícita, tant per fer canvis nous com per revertir els existents.
- Si quelcom és ambigu, **preguntar**; no assumir ni improvisar.
- El rigor per sobre de la velocitat: verificar sempre a `content/` i `layouts/` abans de donar per fet què hi ha.
- **Serveis externs**: abans de provar un servei extern nou (allotjament, CI/CD, edició de codi, aplicacions…), cal **estudiar-ne bé totes les condicions d'ús**: espai disponible, preus, tipus d'usos permesos, límits i polítiques. Documentar-ho a `gestio/` o `drafts/` abans d'aprovar-ne l'ús (lligó de la quota de Codeberg, 2026-09-21).

## Protocol d'inici de sessió (obligatori)

A l'inici de **cada** sessió (OpenCode, Claude o la que sigui), abans de treballar:

1. **Sincronitzar els repositoris**: `git fetch origin` i comprovar que `main` (i la branca `pages`) estiguin al dia.
2. **Iniciar la gestió d'hores**: activar/enregistrar el temps de la sessió (skill `time-tracker`, `.taques/`).
3. **Recompte del web**: usuaris (GoatCounter), nombre de posts i números del web (posts · anys · membres).

## Loop de tasques (definit per l'usuari, 2026-09-24)

Quan l'usuari demani «loop de tasques» o «seguim amb les tasques pendents»: treballar la llista de tasques **una a una**:

1. **Llistar** les tasques pendents amb l'estat real verificat (no assumir res).
2. **Pensar la millor manera** de fer la tasca i **fer-la** (amb aprovació explícita abans de tocar fitxers/disseny).
3. **Verificar** (build + navegació real + desplegament). **Si no passa la verificació, arreglar-ho** i repetir.
4. **Si no es pot seguir per faltar una decisió**: **congelar la tasca** (anotar el que falta i per què), **avisar entre tasques**, i passar a la següent.
5. Repetir fins acabar la llista. Les 5 dictades el 2026-09-21 tenen prioritat.

## El projecte

Lloc web estàtic del **Col·lectiu 9 Barris Imatge** (Barcelona), migrat de Blogger a Hugo + PaperMod i publicat a GitHub Pages.

## Estat real (verificat el 2026-09-25)

- Producció: `https://9barrisimatge.org/`, desplegada per `.github/workflows/deploy.yml` des del push a `main`.
- Repositori de producció i CMS: **GitHub `112books/9bi`** (`main`). Publicació local: `git push github main`.
- **Codeberg `linuxbcn/9bi`** es conserva com a backup amb historial; el push està bloquejat per quota i no participa en producció.
- Tema PaperMod vendored a `themes/PaperMod/`.

## Comandes

- Servei local: `hugo server -D` → http://localhost:1313
- Build: `hugo --minify` → `public/`
- Migració Blogger (requereix `.venv-migracio` amb `markdownify` + `pyyaml`):
  `source .venv-migracio/bin/activate && python3 scripts/migrate_blogger.py --input exports/blog-EXPORT.xml`
- Més visitats: `python3 scripts/goatcounter_popular.py --days 30` (requereix `GOATCOUNTER_API_KEY`, usa `urllib` de la biblioteca estàndard)

## Versions (verificades)

- Hugo **0.164.0 extended** (fixada a `.github/workflows/deploy.yml`)
- Sveltia CMS **0.217.0** (autoallotjat a `static/admin/sveltia-cms.js`)

## Configuració actual (`hugo.toml`)

- `baseURL` **https://9barrisimatge.org/** (producció; `config/production/hugo.toml`) · `config/staging/hugo.toml` apunta a Codeberg Pages i `config/development/hugo.toml` serveix el lloc local · title "9 Barris Imatge" · `locale ca` · `timeZone Europe/Madrid` · `enableRobotsTXT = true`
- `uglyURLs = true` (preserva les URL `.html` de Blogger)
- `[permalinks] posts = "/:year/:month/:slug"`
- `[markup.goldmark.renderer] unsafe = true` i `[markup.goldmark.parser.attribute] block = true`
- Taxonomies: `tag` → `tags`, `category` → `categories`, `author` → `author` · `paginate = 24`
- `params`: `defaultTheme = "dark"`, description, ShowPostAuthors=true, ShowBreadCrumbs=false, ShowReadingTime=false, ShowShareButtons=false, ShowPostNavLinks=true, ShowCodeCopyButtons=true, ShowWordCount=false, comments=false; `homeInfoParams` (Title + Content)
- `menu.main`: Inici(/), Arxiu(/archive/), Qui som(/qui-som/), El Concurs(/concurs/), FAQ(/faq/), **Cerca(/search/)**, Contacte(/contacte/) — **la Guia NO hi és** al menú públic; és interna, es publica a `/guia/` amb `noindex` i s'accedeix des del chrome del CMS
- `menu.footer` (columnes «El web» del peu): **Arxiu 9bi**(/archive/), **Etiquetes / Tags**(/tags/), Més visitats(/mes-visitats/), **Estadístiques del web**(/stats/), Cerca(/search/)

## Estructura de fitxers (verificada)

```
content/
├── posts/YYYY/                     # 3.008 posts actuals (3.006 migrats de Blogger + 2 articles nous), en subcarpetes per any (2008…2026); les URL no depenen del path (permalinks `/:year/:month/:slug` del front matter)
├── qui-som.md, concurs.md, contacte.md, privacitat.md, avis-legal.md, cookies.md, credits.md   # pàgines estàtiques (amb `url` explícita)
├── subvencions.md                 # pàgina filla de «Qui som» (`url: /qui-som/subvencions/`, amb alias de l'antic URL del post)
├── search.md (layout "search"), archive.md (layout "archives")
├── mes-visitats.md (layout "popular" + hiddenInRss: true)
├── guia/                          # _index.md + 7 subpàgines — `robotsNoIndex`, `hiddenInRss` i `sitemap.disable`; accessibles al web, sense indexar i sense enllaçar des del menú públic
└── documentacio/                  # interna (draft): actes/ (acta 2026-09-10) + concurs/
layouts/
├── baseof.html                    # SOBREESCRIT: clau de caché del footer (condició de «números»)
├── single.html                    # SOBREESCRIT: h1 amb visualTitle (salt de línia) si el front matter el porta
├── index.html                     # portada en mosaic (grid de fotos, paginat)
├── archives.html                  # arxiu + índex d'anys a la dreta (rail)
├── taxonomy.html                  # SOBREESCRIT: núvol d'etiquetes (/tags/)
├── author/term.html               # pàgina de posts per autor (mosaic paginat)
├── _shortcodes/membres.html       # taula de membres (ordenada per nº de posts)
├── _shortcodes/rel.html           # {{< rel "/ruta" >}} → relURL base-aware (per a HTML cru del markdown)
├── _default/popular.html          # llista de més visitats (llegeix data/popular.json)
├── _markup/render-image.html      # reescriu rutes d'imatge que comencen per «/» amb relURL
└── _partials/
    ├── header.html                # SOBREESCRIT: icones de menú per .Identifier + JS .scrolled (sticky)
    ├── footer.html                # SOBREESCRIT: banda accent + 5 columnes (logo, buida, web, legal, números) + CC + count-up + reveal
    ├── extend_head.html           # preload de fonts + GoatCounter → 9bi.goatcounter.com
    ├── extend_footer.html         # BUIT (el contingut del peu s'ha mogut a footer.html)
    └── extend_post_content.html   # botó "Veure tot l'àlbum de fotos" (si album_url)
assets/css/extended/custom.css     # estils: mosaic, botó àlbum, tipografies (@font-face), peu (footer-band/-cols/-bottom), formulari, membres, footer-stats
static/admin/{config.yml,index.html,sveltia-cms.js}  # Sveltia CMS autoallotjat
static/images/                     # imatges (media_folder del CMS)
scripts/{migrate_blogger.py,migrate_live.py,goatcounter_popular.py}
data/popular.json                    # top visites (exemple)
data/membres/                        # un fitxer per membre (autor, nom, malnom, web, instagram, actiu)
.github/workflows/deploy.yml      # CI/CD de producció a GitHub Pages
archetypes/default.md              # front matter per defecte
sync-9bi.sh                        # script de sync/gestió
```

## Front matter (convencions reals)

- **Posts**: `title`, `date` (ISO), `year` (any, afegit 2026-09-18 per al filtratge del CMS), `author`, `slug`, `tags` (llista), `cover.image` (opcional), `album_url` (opcional), `description` (opcional)
- **Pàgines**: `title`, `description`, `url` (ruta final explícita)
- **Guia**: `robotsNoIndex: true` + `hiddenInRss: true` + `sitemap.disable: true`, publicada a `/guia/` i accessible només des de l'editor/CMS
- **Documentació**: `draft: true` (interna; no surt a `public/`)
- **search.md**: `layout: "search"` · **archive.md**: `layout: "archives"` · **mes-visitats.md**: `layout: "popular"` + `hiddenInRss: true`

## Sveltia CMS (`static/admin/config.yml`)

- Backend `github`: repo `112books/9bi`, `branch main`; entrada actual amb PAT classic (`repo`) via «Sign In with Token»
- `media_folder: static/images` · `public_folder: /images`; script de l'aplicació autoallotjat a `static/admin/sveltia-cms.js`
- 32 col·leccions: 19 d'articles per any (`posts-2026`…`posts-2008`, una per subcarpeta `content/posts/YYYY/` amb `sortable_fields` per data desc; camps: title, date, year [hidden, default l'any], slug, author [select], cover.image, album_url, tags, description, body), la col·lecció de fitxers **`web-pages` «Pàgines del web»** (les 13 pàgines fixes de `content/*.md`; camps tècnics `url`, `layout`, `hiddenInRss`, `page_bg`, `aliases`, `build` com a **hidden** perquè no es perdi'n cap en desar), `guia`, `actes` (title, date, lloc, persones_reunides, convidat, ordre_del_dia, draft, body), `concurs` (title, tipo[select], date, draft, body), `membres` (vegeu "Sessió 2026-09-18 (v6)") i 8 col·leccions **«Àlbums per arreglar · <autor>»** (`recuperacio/<autor>/`, llistes de treball per recuperar enllaços d'àlbum Picasa morts; ~1.188 registres). La llista d'autors es reutilitza amb un ancoratge YAML (`x-autors: &autors`).
- Per veure **qualsevol article** s'usa la **cerca immediata del propi Sveltia** (indexa tot el web); **no** hi ha cap col·lecció «Tots els articles» perquè els 3.008 posts feien trigar molt el carregament (decisió de l'usuari, 2026-09-25).
- Capçalera del CMS (`static/admin/index.html`): logo + «Llegir la guia» (→ `/guia/`, pestanya nova) + «Torna al web». El rail propi d'anys de la v8 es va perdre en canviar Decap→Sveltia (`d7cdb3b00`).
- **Rail propi del CMS (FET 2026-09-25)**: la llista de col·leccions de la lateral nativa del Sveltia s'amaga (⚠️ al Sveltia 0.217 **no és un `<aside>`** sinó `<div class="primary-sidebar">` dins d'un divisor redimensionable de `#page-container`, i `#nc-root aside` no hi té efecte; ara s'amaga amb `#nc-root .primary-sidebar { display:none !important }` + `cmsHideNativeSidebar()` amb `MutationObserver`, que oculta el panell i tots els seus ancestres fins a `#page-container` perquè el contingut ocupi tota l'amplada) i la substitueix un `<aside class="cms-rail">` amb la llista mínima: **Articles · <any>** (desplegable 2026→2008, el SUMMARY reflecteix l'any de la ruta `#/collections/posts-YYYY`), «Documentació · Actes», «Documentació · Concurs», «Àlbums per arreglar» i el grup **Administració** (Pàgines del web, Membres, Editar la guia). El JS llegeix `localStorage['sveltia-cms.user'].login` ( dada interna del Sveltia) i mostra «Àlbums per arreglar» només si el login és a l'objecte `CMS_ALBUMS`; a 2026-09-25 només hi ha el login real de l'usuari (`112books` → `recuperacio-joan-linux`, «Joan Linux»; l'únic col·laborador del repo segons l'API de GitHub) i **cada company que tingui compte s'ha d'afegir aquí** amb el seu login → col·lecció (mai logar el `token` de l'objecte d'usuari). La **cerca immediata** del Sveltia (barra superior: icona de llista, miniatures, camp «cerca continguts», «+» i avatar) es conserva malgrat amagar la lateral. Nota honesta: Sveltia no té rols per usuari (`hide: true` és global) i amb Write es pot editar qualsevol fitxer del repo, així que «només admins» és ordenació de la interfície, no protecció.
- Peu del CMS: **només** filet vermell + llicència CC + «Powered by LinuxBCN with Hugo & PaperMod» (logo, columnes El web/Legal i 9 Barris en números eliminats el 2026-09-25 per decisió de l'usuari; el peu del **web** no s'ha tocat).

## CI/CD (`.github/workflows/deploy.yml`)

- Trigger: **push a `main`** + `workflow_dispatch`
- Steps: checkout → Hugo 0.164.0 extended → refresc opcional de GoatCounter → `hugo --minify --environment production` → configure/upload/deploy GitHub Pages
- Producció: **https://9barrisimatge.org/**; el domini apunta als registres A de GitHub Pages i el TLS el provisiona GitHub
- Publicació: `git push github main`; Codeberg `linuxbcn/9bi` queda com a backup i no participa en el desplegament de producció

## Sessió 2026-09-21 — Quota de Codeberg: diagnòstic, petició i deploy incremental

> Tot el context i el text llest de la petició a **`drafts/2026-09-21-quota-codeberg.md`**.
> Decisió de l'usuari: **restar a Codeberg** (programari lliure; defugir GitHub), demanar
> augment **modest** de quota (1500 MiB), garantir ús eficient, i **no pagar mai per quota**
> (si Codeberg cobrès — no és la política — pla B: GitHub).

- **Quota de Codeberg**: límit per **usuari** (no per repo) de **750 MiB per a git**; LFS/packages 1,5 GiB addicionals (no es fan servir). Font: blog oficial «New storage limits on Codeberg» (2025-05-14) i FAQ oficial: *"no quota for valid use-cases"*, excepcions per a ús legítim **gratuïtes** (el propietari les aprova amb un "lgtm"; casos reals aprovats: issues 2103, 2109, 2026 de `Codeberg-e.V./requests`).
- **Ús real del compte `linuxbcn`** (API, 2026-09-21): `9bi` = 767.549 KiB (**≈ 749,6 MiB**), `konsento` = 6.515 KiB, `gestor-hores` = 9 KiB → **total ≈ 756 MiB > 750 MiB** (sobrepas ≈ 6 MiB). Per això el push falla: `Forgejo: Quota exceeded … pre-receive hook declined`.
- **Causa de la mida de `9bi`**: el **deploy antic** feia `git init` + `git add -A` + `git push -f HEAD:pages` amb **tot el build (~164 MiB)** a cada publicació; els snapshots anteriors quedaven com a **objectes orfes** al servidor que compten per a la quota fins al GC. El repo local comprimit és només ~254 MiB (pack 229 MiB) — aquesta és la mida "honesta". Les **fotos reals són externes** (àlbums Google Photos enllaçats); al repo només hi ha covers/miniatures petites.
- **Solució aplicada (3 potes)**:
  1. **Petició `[STORAGE]`** a `Codeberg-e.V./requests/issues/new` (template «Increase storage quota(s)»): Git Repositories **1500 MiB**, LFS 1500 MiB (default). Text complet llest a `drafts/2026-09-21-quota-codeberg.md`. Pend: **enviar-la** (requereix login a Codeberg).
  2. **Deploy incremental** a `sync-9bi.sh` (implementat 2026-09-21): clon persistent de `pages` a `~/.cache/9bi-pages`, reset a l'últim publicat, rsync del build, i **push normal** (fast-forward) — només es pugen els objectes que canvien; no es creen orfes. **Ja no hi ha force-push.**
  3. Es deixa anotada l'opció de demanar que Codeberg faci **GC** al servidor (neteja dels orfes antics) un cop hi hagi marge per pushar; amb el deploy incremental el repo ja no creix.

## Sessió 2026-09-24 — DIAGNÒSTIC DEFINITIU del deploy a producció (no tornar-hi)

> El problema «el domini no es refresca» és RECURRENT i queda resolt/descrit aquí d'una vegada.
> **Quan algú digui que el domini va enrere: llegir aquesta secció i LA SEGUIR, no tornar a investigar.**

- **Dos llocs, dos webhooks SEPARATS** (causa arrel de tots els mals):
  - `https://linuxbcn.codeberg.page/9bi/` (staging/previsualització) → el publica un webhook del repo amb Target `https://linuxbcn.codeberg.page/9bi/`, Branch filter `pages`.
  - `https://9barrisimatge.org/` (producció, domini propi) → el publica **UN ALTRE webhook del repo** amb Target `https://9barrisimatge.org/`, Branch filter `pages`. **Sense aquest webhook el domini NO es refresca mai.**
  - El push a `pages` (el que fa `sync-9bi.sh deploy`) dispara els webhooks; cada un publica només la seva URL. La documentació de Codeberg ho confirma: cal «a webhook for each of them» (per sub/domini).
- **Estat verificat avui (2026-09-24 ~09:20 CEST)**:
  - `pages` remota = `60688d207…` (stats, deploy de les 08:52) — **correccigit**, el push arriba bé.
  - `/9bi/` = **fresc** (Last-Modified 08:53 CEST) → el webhook de staging funciona.
  - `9barrisimatge.org` = **endarrerit** (contingut de ~01:39 CEST = deploy FAQ 01:40) → **el webhook del domini no ha publicat** el deploy de les 08:52.
  - DNS **correcta**: `9barrisimatge.org` A → `217.197.84.141`, AAAA → `2a0a:4580:103f:c0de::2`; `www` CNAME `codeberg.page` + A; TXT a `_git-pages-repository.9barrisimatge.org` i `_git-pages-repository.www.9barrisimatge.org` = `"https://codeberg.org/linuxbcn/9bi.git"`. **No és un problema de DNS.**
- **Per resoldre-ho** (acció d'usuari al panell de Codeberg, repo `linuxbcn/9bi` → **Settings → Webhooks**):
  1. Comprovar que existeix un webhook Forgejo amb **Target `https://9barrisimatge.org/`** (Branch filter `pages`).
  2. Si existeix → pestanya **Recent deliveries**: mirar si les darreres (08:52 en endavant) fallen i per què; si Forgejo l'ha posat en estat desactivat després d'entregues fallides → **re-activar-lo (Enabled)**.
  3. Si **no existeix** → **crear-lo**: tipus Forgejo, Target `http://9barrisimatge.org/` **la primera vegada** (la doc de Codeberg exigeix que el primer deploy vagi per `http://`; després es pot canviar a `https://`), Branch filter `pages`. **No usar «Test delivery»**: falla sempre (és esperat segons la doc).
  - Font: <https://docs.codeberg.org/codeberg-pages/using-custom-domain>
- **Verificació ràpida sempre** (còpia de 3 comandes, sense interpretar):
  1. `git ls-remote origin pages` → ha de coincidir amb l'última entrada de `.deploy-log`.
  2. `curl -sI "https://9barrisimatge.org/?v=$RANDOM" | grep -i last-modified` → si la data NO és la del darrer deploy, el webhook del domini no ha publicat.
  3. `curl -sI "https://linuxbcn.codeberg.page/9bi/?v=$RANDOM" | grep -i last-modified` → sempre s'actualitza.
- **Corol·lari**: el contingut de `pages` i la DNS ja estan comprovats (2026-09-24). Qualsevol «el domini va enrere» = webhook del domini. Point the user to esta secció.

## Sessió 2026-09-24 — MIGRACIÓ DE PRODUCCIÓ a GITHUB PAGES (decisió de l'usuari)

> **Decisió (usuari)**: migrar el lloc de producció a **GitHub Pages**. Codeberg queda com a **backup** (repo `linuxbcn/9bi`). Motiu: la quota de Codeberg (750 MiB) es torna a sobrepassar sovint i bloqueja els deploys; el cicle de demanar augments i fer GC no és sostenible. **No esborrar res de Codeberg.**

- **Repo nou**: `https://github.com/112books/9bi` (públic). Remotes locals: `github` (https://github.com/112books/9bi.git → main) i `origin` (Codeberg, queda com a backup).
- **Build i deploy**: `.github/workflows/deploy.yml` — `actions/checkout@v4` + `peaceiris/actions-hugo@v3` (0.164.0 extended) + pas opcional `fetch_9bi_analytics.py` si existeix el secret `GOATCOUNTER_API_KEY` (comprobació al shell, no als `if:`) + `hugo --minify --environment production` + `actions/configure-pages@v5` + `actions/upload-pages-artifact@v3` + `actions/deploy-pages@v4`. Trigger: push a `main` + `workflow_dispatch`. Build ~28 s.
- **Estat verificat (2026-09-24 ~15:45)**: `https://112books.github.io/9bi/` = 200 (Last-Modified fresc = build del push), `/stats/` = 200, `/page/2/` = 200 (miniatures `relURL`). El domini custom `9barrisimatge.org` està configurat al repo (Settings → Pages, via `gh api -X PUT repos/112books/9bi/pages -f cname=9barrisimatge.org`).
- **PENDENT (acció d'usuari, ~5 min)**: canviar la **DNS** a la registradora — instruccions exactes a `drafts/2026-09-24-migracio-github-pages-dns.md`:
  - Apex `@` → 4 registres A `185.199.108.153 / .109 / .110 / .111`; **eliminar** l'A de Codeberg `217.197.84.141` i la AAAA.
  - `www` → CNAME `112books.github.io`; **eliminar** el CNAME a `codeberg.page` i l'A de `www`.
  - TXT (`_git-pages-repository`, SPF de FormSubmit, google-site-verification) → **conservar**.
- **Després de canviar la DNS (propagació 5–60 min)**: GitHub emet el certificat TLS automàticament. Verificar amb les 3 comandes de la secció anterior (ara comparar Last-Modified = build de GitHub, no de Codeberg).
- **Nota de disseny/estat de protecció del domini**: GitHub Pages no demana cap registre TXT extra per al dominio (els A records són la verificació). Si algún dia GitHub marca el dominia com a "protected domain" caldrà un TXT `_github-pages-challenge-...` (no necessari ara).
- **Procediment publicar ara**: només cal `git push github main` → Actions construeix i publica sol. **Ja no s'usa `sync-9bi.sh deploy` per a producció** (queda com a eina per re-deployar Codeberg si calgués revertir el backup).
- **GOATCOUNTER_API_KEY**: afegida a GitHub → `Settings → Secrets and variables → Actions`; `/stats/` es refresca a cada deploy.

## Sessió 2026-09-25 — CMS a GitHub, concurs, «col·lectiu», audit de seguretat i cert TLS

- **CMS ↔ GitHub (FET)**: `static/admin/config.yml` commitejat i desplegat amb `backend: github` + `repo: 112books/9bi` + `branch: main` (commit `ac75a7448a`). Sveltia autoallotjat (0.217.0) — l'entrada és amb **PAT** (botó «Sign In with Token», token classic scope `repo`) o OAuth App futura. **PKCE amb GitHub no implementat** (GitHub ho té en pausa). Verificat en viu: config amb `backend: github` + pantalla d'entrada amb el chrome del CMS. Els editors entren amb el seu PAT.
- **`modules/autopublica/` (M2) commitejat** (mateix commit, amb `.gitignore` perquè `config.ini` té un token real de Codeberg — el repo de GitHub és públic). `deploy.sh` encara usa el flux antic de Codeberg (`git init` + `push -f` a pages) — **disseny a revisar** (ara producció = GitHub Actions). `modules/votacio/` amb actualitzacions (taula `visites` + admin visites, bloc de condicions opcional, geo `hard` per defecte amb radi 1000).
- **Foto de Cordoncillo al concurs (FET)**: `layouts/single.html` amb mecanisme condicional `header_image` (+ `header_image_alt`/`header_image_caption` al front matter) — la foto surt **a tot l'ample** damunt del títol (decisió usuari; primer es va fer petita a l'altura del títol i l'usuari la volia gran). CSS `.post-header--photo`/`.post-header-photo` a `custom.css`. Base-aware (`TrimPrefix "/"` + relURL).
- **Cards de categories apilades** (decisió usuari): lletra de categoria **a dalt** (A → nom → tema → 100 €), `flex-direction: column`; la card C amb **nom i tema en dues línies** («Josep Antón/Cordoncillo», «Tema:/Arran de terra»); separació calendari→categories **4rem** (primer el triple = 6rem, l'usuari va dir que era excessiu); **efecte hover** (vora accent + translateY(-2px) + ombra, amb `prefers-reduced-motion`). El tema de la C és **«Arran de terra»** ( fet per l'altra IA).
- **«Col·lectiu, mai associació» (FET)**: `avis-legal.md` (description + Denominació + 4 referències) i `privacitat.md` (Identitat + 1) ara diuen **«Col·lectiu 9 Barris Imatge» / «el col·lectiu»**. Pendent: `subvencions.md:11` diu «associacions com la nostra» (text de l'usuari — no tocat sense aprovació). Posts antics amb «Associació de Titellaires», «Associació 9 Barris Acull» etc. = **altres entitats**, no tocats.
- **Àlbums de l'històric del concurs (FET)**: a la taula d'història, celda de fets destacats: **2013** → «Entrega de premis 2013» (`photos.app.goo.gl/Snzr7PpUmCa68ozd7`) i **2022** → «Muntatge de l'exposició» (`photos.app.goo.gl/adGZH2GtQZPgFn6r6`). Els dos enllaços verificats (302 → photos.google.com/share → 200).
- **AUDIT DE SEGURETAT (FET)** — informe complet a **`~/Desktop/cyber-neo-report-9arrisimatge.org-2026-09-25.md`** (Risk Score 49/100, High Risk latent; 0 critical / 2 high / 6 medium / 11 low / 7 info). **Res explotable avui** (votació no desplegada, sense tokens a disc). Positius: SQL parametritzat, sense command injection web, CSRF del vot públic correcte, secrets locals mai commitejats, sense debug.
  - **Quick wins aplicats** (commit `b700c5bbc4`): `/.tokens/` + regles globals (`.env`, `*.pem`, `*.key`, `*.p12`, `credentials*.json`) al `.gitignore` (els tokens OAuth de `scripts/picasa_to_photos.py` anaven un `git add -A` de filtrar-se); **fail hard** a `secret_key()`/`admin_key()` de votacio (SystemExit si unset o CHANGE-ME/CANVIA-ME — testejat: config real passa, placeholder falla); **noindex** meta a `static/admin/index.html`.
  - **Correccions votacio FET (lot audit, commit `ee7769edf5`)**: cookies amb **Secure per defecte** (fallback=True, opt-out amb ssl=0; exemple ssl=true), **rate limit a l'admin login** (10/min per IP, bucket "admin:"), **CSRF a POST /admin/tancar** (HMAC lligat a la sessió, testejat: sense csrf 403), **token de sessió amb caducitat server-side** (format `sig:ts`, 4 h validades server-side), **cap de mida al body** (64 KB, 413; helper `read_body`), **bug funcional geo_js arreglat** (1 script, cap JS visible com a text, cap doble execució). Testejat amb WSGI real: vot OK, repetit bloquejat, login dolent 401, login OK 302, tancar sense/amb CSRF, body 413.
  - **Altres pendents de l'audit**: SHA-pin de les accions de CI/CD (peaceiris@v3 = tag mutable), sortida de deploy.sh dins la resposta HTTP (credencials a la URL), 11 fitxers brossa `.dl-*` a `static/images/covers/`, taro/.gitignore contradir el comentari.
- **GOATCOUNTER_API_KEY (FET, 2026-09-25)**: afegida a GitHub → Actions secrets (usuari). El workflow executa `fetch_9bi_analytics.py` a cada deploy — verificat en viu: `/stats/` mostra «Actualitzat: 24 de set. del 2026, 08:50» (dades fresques de GoatCounter).
- **/stats — text clar (FET, commit `fa9b982261`)**: `static/stats/index.html` topbar amb **«Estadístiques des del 24 de setembre de 2026, (242.780 a Blogger dels darrers anys)»** (text exacte de l'usuari, classe `.topbar-since`). Nota: el dashboard de stats és propi (Chart.js + `static/stats/analytics.json`, noindex) — la pàgina /mes-visitats/ llegeix `data/popular.json`.
- **Cert TLS de 9barrisimatge.org (RESOLT)**: GitHub no emetia el cert (12+ h, `*.github.io` amb SAN mismatch). Fix: **treure i tornar a posar el domini al panell** (Settings → Pages; «DNS Check in Progress») — el cert s'ha emès després (un sol cert amb SAN per apex i www, verificat). **Enforce HTTPS ACTIU (2026-09-25, via panell)**: https 200 · http→https 301 · www→apex 301 · API `https_enforced: true`. Nota: el re-PUT via API no va disparar el provisionament; el cicle del panell sí.
- **Vídeos no indexats (Search Console) — diagnòstic**: els 122 vídeos «no està en una pàgina de visualització» són gairebé segur **dades del blog vell** (el web nou té ~1 embed de vídeo; verificat amb grep d'iframes). Congelat pendent de confirmar quina propietat de Search Console es mira. **Sitemap**: es regenera sol a cada deploy (verificat: Last-Modified fresc, robots.txt correcte) — només cal re-enviar-lo a Search Console si cal.

## Sessió 2026-09-25 (v2) — documentació d' editors, missatge i sincronització

- **Guia d' editors publicada sense indexar**: els 8 fitxers de `content/guia/` (`_index.md` + 7 pàgines) han passat de `draft: true` a `robotsNoIndex: true` + `hiddenInRss: true` + `sitemap.disable: true`. PaperMod genera `<meta name="robots" content="noindex, nofollow">` per a aquestes pàgines; `hiddenInRss` impedeix que les pàgines de la guia apareguin als feeds i `sitemap.disable` les exclou del sitemap. La guia continua fora del menú públic, però ja es pot obrir a `/guia/`.
- **Guia actualitzada al backend real**: `content/guia/crear-compte.md` documenta GitHub + PAT classic (`repo`) + «Sign In with Token»; `content/guia/publicar-article.md` ja no parla de Codeberg. `content/incorpora-te.md` (formulari d'alta pública) també demana el nom d'usuari de GitHub. El chrome del CMS (`static/admin/index.html`) enllaça «Guia al web» a `../guia/`, a més de la col·lecció «Guia i manual» del CMS.
- **Correu d'invitació redactat** a `drafts/emails-usuaris.md`: s'ha d'enviar individualment, sense cap token al missatge; l'editor crea el seu propi PAT. Inclou acceptació de la invitació, entrada al gestor, enllaç a la guia i advertiment de seguretat.
- **Recompte real del repositori (2026-09-25)**: **3.008 posts** (`content/posts/`, 19 carpetes d'anys 2008–2026), **24 anys** de col·lectiu (2002–2026) i **24 fitxers de membre**. El peu del CMS encara mostra els números estàtics antics (3.006 / 24 / 12); el peu del web els calcula. GoatCounter retorna `total_unique: 0`, per tant el recompte d'usuaris únics no és utilitzable amb el dashboard actual.
- **Sincronització segura, sense reset**: `main` local coincideix amb `github/main`; Codeberg `main` i `pages` estan endarrerits i el push hi continua bloquejat per quota. **No esborra ni GitHub ni Codeberg ni facis un repositori de zero**: GitHub Pages és producció i Codeberg és backup amb historial. El procediment correcte és commit → `git push github main` → verificar Actions i les pàgines afectades; Codeberg només es sincronitza si torna a haver quota.
- **Encara pendents**:
  - **Test real de votació pública**: l'usuari proporcionarà un fitxer `numero - títol - categoria` i farà un vot fictici des del telèfon. Abans del tancament cal comprovar la pàgina pública de votació, instruccions, avís legal i resultats finals quan la votació es tanca a la data i hora indicades.

## Sessió 2026-09-25 (v3) — 404 útil, cerca directa i tancament

- **404 publicada (FET, commit `70f4f626f9`)**: `layouts/404.html` substitueix el «404» minimal de PaperMod per la pàgina clara i útil aprovada per l'usuari: «Aquesta pàgina no s'ha trobat», explicació dels motius habituals, cerca directa i enllaços a Portada, Arxiu i Contacte. No s'ha afegit cap il·lustració nova.
- **Cerca directa real**: la 404 reutilitza el mateix índex Fuse de `/search/`. `themes/PaperMod/layouts/_partials/head.html` carrega els recursos de cerca també per a `.Kind = 404`; `layouts/search.html` i `layouts/404.html` indiquen `index.json` amb `relURL`, i `themes/PaperMod/assets/js/fastsearch.js` consumeix aquesta ruta base-aware. La pàgina `/search/` continua funcionant igual.
- **SEO i resposta HTTP**: la 404 genera `<meta name="robots" content="noindex, nofollow">`. GitHub Pages retorna HTTP 404 real per a qualsevol ruta inexistent i mostra aquesta pàgina; els seus tres enllaços interiors retornen HTTP 200.
- **Estil i responsive**: `assets/css/extended/custom.css` inclou `.error-404*`, amb el mateix accent `#e03131` del lloc, cerca i targetes centrades, adaptació a 375 px sense desbordament horitzontal i moviment reduït amb `prefers-reduced-motion`.
- **Validació i deploy**: build de producció net (6.442 pàgines); prova local amb cerca «Cordoncillo» -> 44 resultats; proves desktop i mòbil; GitHub Actions run `36115053496` completat amb èxit i verificació live de la 404 amb cerca, `noindex` i resposta 404.
- **Avisos no bloquejants del workflow**: GitHub Actions avisa que `actions/checkout@v4`, `actions/configure-pages@v5` i `actions/upload-artifact@v4` usen Node.js 20, que està obsolet, i que `ubuntu-latest` migrarà a Ubuntu 26 a partir del 19 d'octubre de 2026. L'actualització/SHA-pin de les accions continua pendent.
- **Tancament i sincronització**: GitHub és el repositori de producció i queda net i sincronitzat. Codeberg continua read-only i desfasat per la quota; no s'hi fa push ni reset. El fitxer de temps local queda registrat a `.taques/9arrisimatge.org/2026-09-25.md`.

## Sessió 2026-09-25 (v4) — CMS: miniatures, pàgines fixes i capçalera

- **Miniatures al CMS (FET, commit `a04d62d56`, Actions `36128375734`)**: els 2.911 valors `cover.image` eren relatius (`images/covers/…`) i Sveltia els resolia contra `public_folder` (`/images`) → `/images/images/…` (404). Normalitzats a `/images/covers/…`; els 19 valors http(s) i els 78 sense portada es van deixar com estan. Confirmat en viu per l'usuari: «Ja es veuen les miniatures!».
- **Col·lecció «Pàgines del web» (FET, commit `0be75db21`)**: nova col·lecció de fitxers `web-pages` amb les 13 pàgines fixes de `content/*.md`, perquè l'editor principal les pugui veure i editar des del CMS. `title`, `description` i cos editables; els camps tècnics (`url`, `layout`, `hiddenInRss`, `page_bg`, `aliases`, `build`) com a **hidden**, de manera que en cap cas es perden en desar. A `concurs.md`, `visualTitle`/`visualDescription` són editables (títol i subtítol visuals amb `<br>` i Markdown).
- **Peu del CMS reduït (decisió de l'usuari)**: només el filet vermell + llicència CC (badge + enllaç a la FAQ de crèdits) + «Powered by LinuxBCN with Hugo & PaperMod». S'han eliminat el logo, les columnes «El web» / «Legal» / «9 Barris en números» i el CSS mort associat. **El peu del web (`layouts/_partials/footer.html`) no s'ha tocat.**
- **Capçalera del CMS (FET)**: «Articles · 2026» ara és un desplegable (`<details>`) amb els 19 anys 2026→2008, 2026 marcat amb `aria-current`; es tanca en triar un any, en fer clic fora i en canviar el hash (JS mínim al final de `static/admin/index.html`). El resta d'enllaços: «Pàgines del web» (→ `web-pages`), «Membres», «Llegir la guia» (→ `/guia/`, pestanya nova) i «Editar la guia» (→ col·lecció `guia») — abans tots dos es deien «Guia i manual» / «Guia al web» i no es distingien prou.
- **Veure qualsevol article**: cap col·lecció nova; s'usa la **cerca immediata del Sveltia** (indexa tot el web) i els 19 anys per publicar o retocar els darrers posts. Decisió de l'usuari, 2026-09-25: es rebutja «Tots els articles» perquè els 3.008 posts feien trigar molt el carregament.
- **«Àlbums per arreglar»**: 8 col·leccions a `recuperacio/<autor>/` (~1.188 registres); no s'afegeixen al desplegable d'anys. Com que la llista nativa de col·leccions s'amaga (v5), només s'hi accedeix pel rail «Àlbums per-arreglar · <autor>» i només si el login de l'usuari hi és mapejat a `CMS_ALBUMS`.
- **Rail propi del CMS (FET, commit `8d98f192f`, Actions `36131260075`)**: capçalera reduïda a logo + «Llegir la guia» + «Torna al web» i `<aside class="cms-rail">` propi a l'esquerra: Articles · <any> (desplegable), Documentació · Actes, Documentació · Concurs, Àlbums per-arreglar i Administració (Pàgines del web, Membres, Editar la guia). Detall de l'amagat de la lateral a la secció Sveltia de més amunt.
- Build `hugo --minify` net; YAML de `config.yml` validat (32 col·leccions, 13 pàgines, cap camp ocult absent del front matter). Totes les canvis d'aquesta v4 v4 publicats i verificats en viu.

## Sessió 2026-09-25 (v5) — lateral nativa del Sveltia, àlbums per login i crèdit «Taro»

- **Bug de la lateral duplicada (corregit, commit `b3b57a54d`, Actions `36132308723`)**: el selector `#nc-root aside` del rail propi **no funcionava** — al Sveltia 0.217 la lateral nativa no és un `<aside>` sinó un panell `<div class="primary-sidebar">` dins d'un divisor redimensionable de `#page-container`, i la llista de col·leccions («Col·leccions / articles 2026 / …») continuava visible al costat del rail. Correcció: `#nc-root .primary-sidebar { display:none !important }` + `cmsHideNativeSidebar()` amb `MutationObserver` que oculta el panell i tots els ancestres fins a `#page-container` (perquè el panell del divisor tampoc reservi amplada). La cerca immediata de la barra superior es conserva. Verificat en viu.
- **Mapejament login→àlbums (FET)**: `CMS_ALBUMS` a `static/admin/index.html` conté `112books` → `recuperacio-joan-linux` («Joan Linux»). A 2026-09-25 `gh api repos/112books/9bi/collaborators` retorna **només `112books` (admin)**: encara no s'ha creat cap compte de company. Quan se'n creï, cal afegir `login` → col·lecció; el rail mostra «Àlbums per-arreglar · <autor>» només si el login hi és.
- **Secció «Per què l'aplicació es diu Taro?» (FET, commit `3984c84ca`, Actions `36132517005`)**: text dictat per l'usuari afegit a `content/credits.md`, dins de «L'aplicació Taro», amb dades verificades (Gran Enciclopèdia Catalana + altres fonts): Gerda Pohorylle (Stuttgart, 1 agost 1910 — El Escorial, 26 juliol 1937), companya de Robert Capa, reportatges de primera línia a la Guerra Civil espanyola; va morir als 26 anys atropellada per un tanc republicà en la retirada del front de Brunete; el cos es va traslladar a París i descansa al **cementiri del Père-Lachaise**. Enllaç a `enciclopedia.cat/gran-enciclopedia-catalana/gerda-taro`. **Pendent**: l'usuari pot retocar el text al CMS; no s'ha escrit el model concret del tanc (T-26) perquè cal verificar-lo en una font específica. **No s'ha tocat** el text de `credits.md` que diu que el codi viu a Codeberg com a «versió de referència» (obsolet, pendent de decisió).

## Sessió 2026-09-25 (v6) — Votació desplegada al subdomini `vots-cordoncillo.linuxbcn.com`

- **Accés SSH correcte**: el compte Dinahosting de `linuxbcn.com` és **`linuxbcn0`** (key `id_ed25519`, ja autoritzada al servidor). **`konsento`/`naubostik` és un compte diferent i PF a altres llocs — no tocar-lo mai.** Decisió de l'usuari (2026-09-25/26), a recordar sempre.
- **Host**: `vl28359.dinaserver.com` (82.98.166.123). Dinahosting **no té Passenger** ni CGI functional a aquest host: el patró que funciona és **procés d'usuari + proxy al docroot + crontab watchdog**, el mateix que fa l'app `konsento` del compte veí (només-inspeccionada, no modificada). Dinahosting acaba el TLS davant d'Apache i **envia `X-Forwarded-Proto`** (sonda verificada el 2026-09-26: `https` per https, `http` per http, i `HTTPS=on` només a https). Per això els redirects han de ser explícits i en absolut. **No usar `%{HTTPS}`** per redirigir: provoca un bucle de 301.
- **Certificat del subdomini**: emès el 2026-09-25 22:45 (SAN amb `vots-cordoncillo` i `formularis`, vàlid fins al 2026-12-24). Abans dels vots caldrà renovació automàtica; avui està dins del període de l'exposició.
- **Desplegament real (documentat a `modules/votacio/README.md`)**: codi a `~/apps/vots-cordoncillo/` (fora del docroot), procés a 127.0.0.1:8301 amb `deploy/start.sh` (`umask 077`), watchdog cada 5 min + `@reboot` al crontab de `linuxbcn0`, docroot `~/www/vots-cordoncillo/` amb només `deploy/htaccess` (redirect arrel → formulari, `.well-known` passa, proxy `[P,QSA,L]`). Còpia primera del docroot anterior a `apps/vots-cordoncillo/COPIA-docroot-20260925.tgz`.
- **Estat del servei**: `/health` → `ok`; `/v/cordoncillo-2026` → formulari; `/admin/login` → 302 amb `admin_secret`; export CSV signat; geofence `hard` a 500 m del Casal verificat (dins admet, fora rebutja 403); sense geo = 403. BD creada amb **0 vots** a l'hora de la posada.
- **Config real al servidor** (gitignored, campa només a `~/apps/vots-cordoncillo/config.ini` amb permisos 600): secrets nous (43/32 chars), `base_url` correcte, **finestra de proves 2026-09-25→2026-10-31** (ha de canviar-se a les dates de l'exposició: 1–15 desembre 2026), 3 obres de prova, `rate_limit=120` (perquè amb el proxy `REMOTE_ADDR` és sempre 127.0.0.1; defensades reals = CSRF + testimoni HMAC + geofence). La BD es re-crea amb la configuració nova esborrant `data.db`.
- **Formularis — FET I PUBLICAT (2026-09-26, commit `57b021ae78`)**: `formularis.linuxbcn.com` servei el mòdul `modules/formularis/` (WSGI, **només biblioteca estàndard**, sense base de dades: les dades passen i surten per correu). Mètode idèntic al de la votació: codi a `~/apps/formularis/` (fora del docroot), procés `python3 serve.py 8302` a 127.0.0.1, `deploy/start.sh` + `stop.sh` + `watchdog.sh`, `@reboot` i watchdog cada 5 min al crontab, docroot `~/www/formularis/` amb **només `.htaccess` i `.well-known`**. `/health` → `200 ok`. **SMTP directe** de Dinahosting: `9barrisimatge-org.correoseguro.dinaserver.com:465` (SSL, hostname del panell; **no** `mail.9barrisimatge.org`, que té certificat que no correspon), `config.ini` a `~/apps/formularis/config.ini` amb permisos 600 i `interpolation=None` + `raw=True` (per a passwords amb `%`). Els dos formularis del web (`/contacte/` i `/incorpora-te/`) apunten a `POST /envia/contacte` i `/envia/incorpora-te`; **ja no es fa servir FormSubmit** (que no entregava). Controls: `Origin`/`Referer` contra `allowed_origins` (403 si no), honeypot `_honey` (200 silenciós), rate limit per IP, `MAX_COS`, whitelist de camps, `Reply-To` només si l'adreça és vàlida. Peu legal RGPD/LOPDGDD a cada correu. **Correu verificat en viu** pels tres tipus amb entrega a INBOX, `DKIM-Signature s=default a=rsa-sha256` i SPF passat. **README.txt reescrit** amb el mètode real (l'antic donava Passenger, que Dinahosting no té).
- **Carpeta remota lliure**: `~/www/app/taro/votacio/` (buida) per a la fase 2 del projecte Taro (tot sota `taro.linuxbcn.com`).
- **Pendent sens dubte**: prova del vot real des del telèfon al Casal (l'usuari la farà); abans del tancament, verificar recompte i export finals per la finestra real.

## Sessió 2026-09-26 — Mode de proves de la votació (re-vot, botó d'ubicació, privacitat)

- **Diagnòstic del «no em demana la ubicació»**: la pàgina també es servia per `http://` sense redirigir. En un origen no segur el navegador **no ofereix geolocalització** (`navigator.geolocation` no hi és) i, amb `mode_geo=hard`, el vot es rebutjava sense demanar permís. Ara l'`.htaccess` redirigeix **totes** les rutes `http`→`https` amb 301, conservant ruta i query, i l'`.well-known` i `/fonts/` queden fora del proxy.
- **Mode de proves (decidit per l'usuari)**: `revote_minutes = 10` a la `[edicio]` del `config.ini` del servidor. Es pot tornar a votar la mateixa obra passats 10 min; la votació anterior **se substitueix** perquè la taula té `UNIQUE (edicio_id, obra_id, dispositiu_hash)`. `0` (per defecte i valor de l'exposició) = un sol vot per obra i dispositiu per tota l'edició.
- **Botó «Activar la ubicació»**: la petició automàtica no sempre mostra el permís (iOS exigeix un toc de l'usuari). El botó torna a demanar-la, serveix per reintentar si el permís estava bloquejat i **s'amaga quan la ubicació s'aconsegueix**.
- **Privacitat**: nota al formulari (vots anònims, no es demana nom ni correu, **no es desen les coordenades**; només un codi aleatori del dispositiu — cookie `vid` HttpOnly, no és una empremta digital — i si la ubicació era dins del radi) i enllaç «Protecció de dades» a `https://9barrisimatge.org/privacitat/` al peu de totes les pàgines.
- **Mode obert de proves (decidit per l'usuari el 2026-09-26, fins al dia de l'exposició)**: `vot_limit = 0` al servidor = **sense límit de vots per obra i dispositiu**; la votació anterior de la mateixa obra se substitueix (`INSERT OR REPLACE`, perquè la taula té `UNIQUE (edicio_id, obra_id, dispositiu_hash)`). Després de votar la pàgina informa dels vots del mateix dispositiu («Des d'aquest dispositiu has votat 3 obres», amb singular/plural). L'usuari el provarà amb companyia des de diferents sistemes operatius i distàncies. Obres de proves: **1 a 100** (`Obra de prova 001`…`100`); 0 i 101 es rebutgen amb «Aquest número d'obra no existeix».
- **PUNT DEL GEOfence (corregit el 2026-09-26)**: les coordenades estaven mal posades i eren la causa dels rebuts. El punt correcte és el **Casal de Barri de Prosperitat, Plaça d'Àngel Pestanya (08016 Barcelona): `lat = 41.441623`, `lon = 2.179794`, `radi = 500`**, verificat amb Nominatim, Photon i geocodi invers. El punt anterior (41.3948/2.1775) era a **5,2 km** i cap vot es podia registrar.
- **`connect()` sincronitza la configuració** (`nom`, dates, `mode_geo`, `lat`, `lon`, `radi`, `collect_data`, `vot_limit`, `activa`) al registre de l'edició en cada arrencada i ho deixa escrit al log. Canviar aquests valors al `config.ini` doncs sí que té efecte en reiniciar **sense cal esborrar `data.db`**. No toca les obres ni els vots.
- **Pàgina de votació (2026-09-26)**: calcula la distància al punt del concurs i la mostra («Ubicació activada: ets a 26 m del punt del concurs»); si la precisió és > 250 m avisa que cal activar l'«ubicació precisa» del telèfon (cas típic de la ubicació aproximada d'iOS); si es rebutja el vot, el missatge diu la distància real («el telèfon indica que ets a 5,2 km»).
- **Estat verificat**: 1 i 100 acceptats, 0 i 101 rebutjats, recompte per dispositiu 1/2/3, repetició de la mateixa obra en mode obert, `vot_limit=1` rebutja el repetit, 0 errors de consola en directe; base del servidor amb 0 vots (esboren els de prova); commits `60dda04f47`, `7db44dbc15`, `c29ba99436` i `35ab4dd85b`.
- **Abans del dia de votació (llista de tasques)**:
  1. `vot_limit = 1` a `~/apps/vots-cordoncillo/config.ini` i reiniciar (`deploy/stop.sh` + `deploy/start.sh`). Deixar `revote_minutes` en actiu no fa res amb `vot_limit = 1` sense finestra, però es pot posar a `0` per claredat.
  2. Dates reals: `data_inici = 2026-12-01T00:00:00`, `data_fi = 2026-12-15T23:59:59`.
  3. Substituir les 100 `[obres]` de prova per la llista definitiva (número, títol, autor, categoria). **Les obres només es carregen en la creació de la base**: per canviar-les cal esborrar `data.db` (és el pas 4) o inserir-les a mà.
  4. Aturar el servei i **esborrar `data.db`** perquè el recompte comenci a zero i les obres definitives es carreguin des del config.
  5. **Tornar a verificar el punt del geofence** amb una font i que la distància que mostra la pàgina sigui coherent amb on serà l'exposició.
  6. Integrar el QR real a `content/votacio.md` (el lloc reservat és el `<div class="cartell-qr">`, amb la nota de developer ja convertida en comentari HTML).
  7. Comprovar la renovació del certificat (vàlid fins al 2026-12-24, dins del període de l'exposició).

## Problemes coneguts / pendents (verificats)

1. **Quota de git de Codeberg superada** (≈756 MiB vs 750 MiB) → cap push a `origin` (ni `main` ni `pages`) des de 2026-09-24. **Mitigat per la migració a GitHub Pages**: producció ja no depèn de Codeberg. El repo de Codeberg queda com a **backup read-only** fins que (opcionalment) s'aprovï l'augment de quota a `Codeberg-e.V./requests` (issue #2522, tancada el 2026-09-23 amb GC del servidor sense augment; text de reobertura preparat però no enviat). (Vegeu `drafts/2026-09-21-quota-codeberg.md`.)
2. **Codeberg ja no participa en el desplegament de producció**: el workflow canònic és `.github/workflows/deploy.yml`; `sync-9bi.sh` i la branca `pages` només es conserven com a eines/backups antigues de Codeberg. No hi ha runner útil de Forgejo Actions.
3. `static/admin/config.yml` ja usa el backend `github` (repo `112books/9bi`) i entrada amb PAT; queda pendent convidar els editors com a col·laboradors amb accés de **Write** i comprovar els permisos reals.
4. GoatCounter està creat a `9bi.goatcounter.com` i el secret `GOATCOUNTER_API_KEY` refresca `/stats/` a cada deploy.

## Blog real (verificat el 2026-09-17)

- El blog original i encara viu és **https://www.9barrisimatge.org** (Blogger, `blog-id` `8034150767456238983` — mateix ID que `exports/sample-blogger.xml`, que és un extracte real, no dades falses).
- **3.006 entrades confirmades** (`openSearch:totalResults`, comptatge exacte verificat: 21 pàgines de 150 sumen 3.006).
- El domini propi (`www.9barrisimatge.org/feeds/posts/default`) serveix **RSS** per defecte, però l'endpoint directe **`https://www.blogger.com/feeds/8034150767456238983/posts/default?start-index=N&max-results=150`** serveix **Atom complet** (`<feed>`, `<content type="html">` sencer, sense truncar, paginable amb `start-index`) — mateix format que espera `migrate_blogger.py`. Font vàlida per a la migració real, no cal l'exportació manual des del panell si aquest endpoint és accessible.
- Aquest endpoint no inclou categoria `#kind` per entrada (a diferència de l'export oficial, que barreja posts/pàgines/comentaris) — no cal el filtre `#post` de `parse_xml()`, totes les entrades d'aquest feed ja són posts.

### Mapeig d'autors (verificat, comptatge real per `<author><uri>`)

| Posts | Nom Blogger | `profile/<id>` | Membre |
|---|---|---|---|
| 1307 | Joan Martinez i Serres "linuxbcn" | 07873791980606905428 | Joan "Linux" Martínez i Serres |
| 397+11 | PredroClick / pedro click (2 comptes) | 09502103278209433876 / 09447813154520602112 | Pedro Click |
| 274 | Manel Sala "Ulls" | 07611922472754557605 | Manel Sala "Ulls" Circ |
| 118 | francesc barbe | 00926052916717343447 | Francesc Barbe |
| 110 | ismaelug | 06765486609758806432 | Ismael Utrilla |
| 86 | Alberto | 16399715831790649537 | Alberto Sanagustín |
| 78 | Iozsef Kiss | 04330214459290255808 | Iozsef Kiss |
| 53 | pedrocasal | 18053814840045725261 | Pedro "Casal" Cervera |
| 29 | núria laura orbaneja | 10639085300606178057 | **Núria Laura Orbaneja** (nou) |
| 27 | manel villalba | 03875414596834414899 | **Manel Villalba** (nou) |
| 26 | Ulls (compte diferent) | 03777963813689534193 | assumit = Manel Sala "Ulls" Circ (2n compte; **verificar amb ell**) |
| 12 | Nico YeYe | 15965093973040358649 | **Nico YeYe** (nou) |
| 5 | Gris Medio,casi negro | 06831158748343898384 | Juan Carlos Molina (Grismedio Casinegro) |
| 469+2 | Unknown / Anonymous | (sense uri) | "9 Barris Imatge" (genèric) |
| 2 | Nou Barris Imatge | 02393670543566068078 | "9 Barris Imatge" (compte de l'entitat) |

**Decidit (2026-09-17)**: s'afegeix tothom que hagi publicat com a membre — Núria Laura Orbaneja, Manel Villalba i Nico YeYe afegits a `static/admin/config.yml` (select `author`) i "9 Barris Imatge" com a genèric pels posts sense autor identificable. Pendent: revisar més endavant qui és actiu/inactiu actualment (no tocat `qui-som.md`, que llista només membres actius — aquesta llista del CMS és l'autoria històrica completa).

### Migració real executada (2026-09-17)

- **`scripts/migrate_live.py`**: migra directament des del feed Atom en directe (no cal export manual), reutilitza el processament de `migrate_blogger.py` (imatges, àlbum, HTML→MD). Mapeig d'autor per `<author><uri>` (taula `AUTHOR_BY_URI`), vocabulari de tags real agregat de tot el blog per suggerir-ne 5 als posts sense cap (marcats amb comentari HTML `<!-- tags auto-generades... -->` per revisar-los).
- **Resultat**: **3.006/3.006 posts migrats a `content/posts/`**, 0 errors. Build local net (`hugo`, 3006 pàgines, ~30s, sense warnings de col·lisió).
- **Bug detectat i corregit durant la migració**: la primera passada deduplicava per slug sense any/mes i en va perdre 118 (p.ex. "blog-post" es repeteix 41 cops en mesos diferents — cap col·lisió real d'URL). Fix: dedup per URL original de Blogger, no per slug.
- **Advertència coneguda**: `album_url` s'extreu de l'enllaç que envolta la primera imatge del post. Si un post té més d'un enllaç rellevant (p.ex. tant un àlbum de Google Photos com un crosspost a `blog.pocallum.cat`), només es captura el primer — pot no ser sempre el que un humà triaria. Detectat al post de Prospe Beach 2026 (l'enllaç de Google Photos que l'usuari havia enganxat manualment al xat va quedar substituït per l'enllaç al crosspost de pocallum.cat en re-executar la migració completa).
- **Estat**: els 3.006 posts estan committejats i desplegats.

## Sessió 2026-09-17 (v2) — formulari RGPD i ordre del peu

- **Menú del peu reordenat** (`config/_default/hugo.toml`, `menu.footer`): **Arxiu, Etiquetes, Més visitats, Estadístiques, Cerca, RSS** (weights 1–6). Verificat al build.
- **`content/contacte.md`**: formulari reestructurat per complir RGPD:
  - casella de **consentiment obligatòria** (`name="consentiment"`, no premarcada) amb enllaç a la política;
  - **honeypot** anti-spam (`_honey`, camp ocult);
  - bloc "informació bàsica" (responsable, finalitat, legitimació, destinataris, drets) i enllaç a la política;
  - la línia "També pots escriure'ns directament…" **es manté** però separada del botó (bloc `.contact-alt` amb `border-top`).
- **`content/privacitat.md`** (nou, `url: "/privacitat/"`): política de privacitat amb responsable, finalitats, base jurídica, destinataris (FormSubmit + proveïdor de correu), conservació, drets i AEPD. **Conté placeholders `[PENDENT: NIF…]` i `[PENDENT: adreça…]` que s'han d'omplir abans de publicar** (vegeu backlog).
- **`assets/css/extended/custom.css`**: estils `.contact-consent`, `.contact-honeypot` (off-screen), `.contact-after`/`.contact-alt`.

## Sessió 2026-09-18 — membres, imatges, peu en números i tema fosc

- **Llistat de membres implementat** (`content/qui-som.md` → `{{< membres >}}`):
  - Taxonomia nova `author = "author"` a `config/_default/hugo.toml` (en Hugo el **valor** és la clau de front matter; amb `author = "authors"` no es genera cap terme).
  - `data/membres.yml`: 12 membres (`autor`, `nom`, `web`, `instagram`), editable des del CMS.
  - `layouts/_shortcodes/membres.html`: taula ordenada pel nombre de posts (desc); nom i número enllacen a la pàgina de l'autor; els perfils de Blogger es mostren com «Perfil a Blogger»; si `nom` és buit s'usa `autor`. Exclou "9 Barris Imatge".
  - `layouts/author/term.html`: pàgina per autor amb graella tipus mosaic de portada, paginada (`/author/<slug>.html` i `/author/<slug>/page/N.html`); títol pres de `data/membres.yml` per preservar majúscules/minúscules.
  - `static/admin/config.yml`: col·lecció de fitxers Decap «membres» sobre `data/membres.yml` (select `autor` amb 13 opcions, `nom`, `web`, `instagram`).
  - **Pendent**: enllaç de reserva al perfil de «Els components de 9 barris imatge» del bloc vell per als membres sense web (ara mostren «—») i completar els Instagram que falten.
- **Imatges noves** (mogudes de l'arrel a `static/images/`): `Membres-casalL1300396.jpg` (dalt de «Qui som»), `reunións-dojous-L1420055-1024x576.jpg` (secció Reunions), `juan-sinsangre-trofeus_DSF5756.jpg` (secció nova «Història dels trofeus»). `alt` escrits per nosaltres.
- **`content/qui-som.md`**: secció nova **«Com funcionem»** (entre Reunions i Membres); text de «Reunions» reescrit per l'usuari amb enllaç a **Las Rudas** (`https://www.instagram.com/rudascooperativa/`), també afegida a «Links amics».
- **`content/concurs.md`**: secció **«## Història dels trofeus»** (Juan Sin Sangre → Carlitos).
- **Peu «9 Barris en números»** (només **portada** i **Qui som**): «3.006 posts · 24 anys · 12 membres», amb count-up en entrar a pantalla (IntersectionObserver; amb `prefers-reduced-motion` o sense JS es mostren els valors finals). Valors: `len (where site.RegularPages "Section" "posts")`, `sub now.Year 2002`, `len hugo.Data.membres.membres`; format amb `lang.FormatNumber 0` → «3.006».
  - **`layouts/_partials/footer.html` sobreescrit** (còpia del tema + bloc + script).
  - **`layouts/baseof.html` sobreescrit**: cal afegir la condició a la clau de `partialCached "footer.html"` (era `.Layout`+`.Kind`, i «Qui som» comparteix clau amb els posts → agafava el peu cachejat d'un post). **Atenció en actualitzar PaperMod: `baseof.html` i `_partials/footer.html` ara són nostres.**
- **Tema fosc per defecte**: `config/_default/hugo.toml` → `[params] defaultTheme = "dark"` (el botó sol/lluna del header, Alt+T, passa a clar i ho recorda via localStorage).
- **Arxiu**: l'índex d'anys de la dreta només apareixia a ≥1200px; baixat a **≥1024px** (`custom.css`).
- **Tipografia**: només feta la **vista prèvia** (cos **Montserrat** + títols **Gillius ADF**) a `/tmp/font-preview`; **no s'ha canviat cap fitxer del web**. Pendent d'instal·lar autoallotjada.
- **Peu**: redisseny a **4 columnes** (banda d'accent `#e03131` a dalt + logo · columna buida · «El web» · «Legal»), tot dins de `layouts/_partials/footer.html`; `extend_footer.html` queda **buit**. Línia inferior amb copyright i «Powered by LinuxBCN with Hugo & PaperMod» (links als tres; en hover/focus sobre LinuxBCN es revela «· Consultoria | Desenvolupament | Allotjament | Disseny»). Responsive: 4→2→1 columnes (la buida s'amaga al mòbil).
- **`content/qui-som.md`**: «FaVB» → «**FAVB**» a «Links amics».
- **Tipografies autoallotjades aplicades**: cos **Montserrat** + títols **Gillius ADF** (`static/fonts/`, `@font-face` i overrides a `custom.css`, `preload` a `extend_head.html`; sense cap CDN).
- **Crèdits ampliats** (`content/credits.md`): links a totes les eines, llicència **CC BY-NC-SA 4.0** explicada en català clar i **mini-FAQ** d'ús de les imatges.
- **Cerca** afegida al `menu.main` (abans de «Contacte»).

## Sessió 2026-09-18 (v2) — capçalera sticky, imatges, peu, legal, subvencions i concurs

- **Capçalera sticky amb icones** (implementat): `layouts/_partials/header.html` **sobreescrit** (`dict $icons` per `.Identifier`: home→casa, archive→arxiu, qui-som→persones, concurs→trofeu, search→lupa, contacte→sobre). En fer scroll (>120px) el JS afegeix `.scrolled` a `#header` i es mostren `.menu-icon` (SVG de línia, `currentColor`) en lloc de `.menu-text`; logo encongit a 48px. Només escriptori (≥769px).
- **Imatges base-aware**: `layouts/_markup/render-image.html` (nou) reescriu amb `relURL` les rutes d'imatge que comencen per «/» (`strings.TrimPrefix "/"`). Abans `qui-som.md` i `concurs.md` generaven `src=/images/...` i donaven 404 sota `/9bi/`.
- **Peu de 5 columnes** (abans 4): `layouts/_partials/footer.html` amb logo · buida · «El web» · «Legal» · **«9 Barris en números»**. La columna de números ara és **sempre visible** (abans només portada/Qui som) i s'ha tret la condició `$showStats` de la clau de `partialCached` a `baseof.html`. `grid-template-columns: repeat(5,1fr)` (5→3 @1024 →2 @700 →1 @480; la buida s'amaga ≤1024).
- **Logo CC a la línia de llicència**: `static/images/cc-by-nc-sa.svg` + `<img class="cc-badge">` dins `.footer-copyright`.
- **Reveal de LinuxBCN**: `.footer-powered` inline-block i `.footer-powered-reveal` (consultoria…) es desplega en `:hover`/`:focus` sense desplaçar el text.
- **Amplada unificada**: `.footer-cols` i `.footer-bottom` amb `max-width: calc(var(--nav-width) + var(--gap) * 2); margin: auto` (com «Avui fa» / el mosaic).
- **Núvol d'etiquetes**: `layouts/taxonomy.html` **sobreescrit** (`.terms-tags.tag-cloud`), mida `0.85 + 0.9*(count/max)` rem (rang ~0.85–1.75rem); CSS `.tag-cloud`.
- **Text de Cerca**: `content/search.md` amb `description`.
- **Logo 138×229**: `--logo-width: 138px` / `--logo-height: 229px` a `:root`; `iconHeight = 229` a `[params.label]` de `hugo.toml`; `<img width="138" height="229">` al peu.
- **Avís legal i privacitat**: `content/avis-legal.md` reescrit (Titular **sense NIF** —l'associació no en té—, adreça **Casal de Barri de Prosperitat, Plaça d'Ángel Pestaña, s/n, 08016 Barcelona**, i secció «Responsabilitat»: cada autor respon dels seus textos; opinions compartides sense comprometre l'entitat). `content/privacitat.md` amb la mateixa adreça i **sense placeholders**.
- **Subvencions**: el text «Subvencions públiques: per què hi renunciem» s'ha mogut de `posts/` a **pàgina filla de Qui som** (`content/subvencions.md`, `url: /qui-som/subvencions/`), enllaçada des de «Com funcionem», amb `aliases` que redirigeix l'antic URL `/2026/09/renunciem-a-les-subvencions.html`.
- **Pàgina del Concurs (36è, 2026)** a `content/concurs.md`:
  - Bloc superior amb **línia del temps de fulls de calendari**: Set 25 (inici) · Nov 20 (data límit) · Des 01 (inici exposició) · Des 18 (lliurament de premis + concert) · Des 30 (fi). Els passos interns (23 i 30 nov) **no** es mostren al públic.
  - **Pestanyes** «Bases» i «Com participar» amb **CSS pur** (radios, sense JS) + botó **Descarrega en PDF** (`window.print()`; `@media print` deixa visibles només les bases).
  - Bases adaptades de la 35a a la 36a (correu `dinamitzacio@casalprospe.org`). **Pendent de confirmar**: premis 100 €, votació popular 1–15 des, hora 19 h i tema de la categoria C.
  - `<hr class="concurs-sep">` separa el bloc del concurs de «Història».
- **Eslògan de portada** (`[params.homeInfoParams] Content` a `hugo.toml`): de «Des de 2002 documentant Nou Barris - Barcelona» a **«Documentant Nou Barris (Barcelona) des del 2002»**.
- **Decisió (votació popular per QR, en estudi)**: per evitar vots sospitosos i facilitar el recompte. Regla triada: **1 vot per obra i dispositiu**; identitat **anònima per dispositiu** (testimoni firmat + registre al servidor); accés **només amb QR presencial** (secret d'edició). Allotjament previst: **app Python** (`venv` + FastAPI/Flask + SQLite) al **servidor de LinuxBCN** (sense Docker, per decidir). Pendent d'estudiar/decidir.

## Sessió 2026-09-18 (v3) — recerca «Història de la fotografia a Nou Barris» i diagnòstic responsive/etiquetes

> **Sessió de recerca i diagnòstic (només lectura). No s'ha tocat cap fitxer de disseny ni contingut.** Els canvis d'eslògan (`hugo.toml` + `qui-som.md`) estan aplicats però **no committejats**.

### Recerca de fotògrafs (per a la secció nova proposada a «Qui som»)

- **Kim Manresa** — el nom imprescindible. **Nascut a Nou Barris** (el nostre post del 2016-07-01 el descriu com «el fotògraf nascut a Nou Barris»); fotoperiodista **en actiu des de 1974**; **Premi Miravisions d'Honor 2026**; exposició **«Nou Barris 1970-1980»** (marquesina de Via Júlia, 1 juliol 2016, organitzada per la Coordinadora d'Associacions de Veïns i Entitats de Nou Barris). **Donant destacat del fons fotogràfic de l'Arxiu Històric de Roquetes-Nou Barris** (blog de l'Arxiu, 2011). Ja és al nostre arxiu: posts `2016-07-01-exposicio-fotografica-de-kim-manresa.md` i `2016-07-02-exposicio-kim-manresa-nou-barris-1970.md` (la imatge font es diu `expo-quim.jpg`, d'aquí el «Quim»). Enllaços verificats: <https://www.miravisions.cat/ponent/kim-manresa> · <http://arxiuhistoric.blogspot.com/2011/02/fons-fotografic.html>. **Pendent de confirmar el barri de naixement.**
- **Ginés Cuesta** (Barcelona, **1945–2023**, veí del **Verdum**) — «fotografia al pas»; fons llegat a l'Arxiu Històric de Roquetes-Nou Barris (2011); llibre **«La Barcelona fotografiada de Ginés Cuesta»** (text d'Isabel Segura; ed. Barcelona Llibres, presentat 2024). Enllaç: <https://juditmusachs.com/project/gines-cuesta>. *(L'usuari deia 1944; la font verificada diu 1945.)*
- **Manel «Ulls» Sala Aponte** — membre de 9 Barris Imatge (`data/membres.yml`: `Manel Sala "Ulls" Circ`; 274 posts), **referent de la fotografia de circ i arts escèniques**. Cognom «Aponte» i condició de «referent» aportats per l'usuari, **sense font externa**: verificar amb ell.
- **Jesús Atienza** — fotògraf **especialista en titelles/putxinel·lis** i teatre. Verificat al nostre post `2018-04-07-rombic-lateneu-popular-de-nou-barris_7.md` («el fotògraf especialista en el món de les titelles») i a <https://larevoltadelstitelles.bibliomusicineteca.com/fotografies>.
- **Manel Mora Palau** — fotògraf esportiu, botiga **Foto Mora** (pg. Fabra i Puig); referent de Manel Montilla (betevé).
- **Manel Montilla** — **barri de Porta**; fotoperiodista esportiu, 35 anys (des de març 1991), llibre **«Soc fotògraf»** (2026). <https://beteve.cat/cultura/fotoperiodista-esportiu-manel-montilla-reivindica-professio-soc-fotograf>.
- **José María Medina «El Nostálgico»** — veí, projecte **«Nou Barris d'abans i ara»** (exposició 2018 amb l'Arxiu, Via Favència/CC Can Verdaguer). <https://beteve.cat/cultura/fotografies-el-nostalgico-nou-barris-abans-ara>.
- **Arnau Bach** i **Myriam Meloni** — coautors de **«Linde»** (2020), sobre **Canyelles, Torre Baró, Vallbona i Ciutat Meridiana**.
- **Mónica Rosselló** — projecte **«16 barris, 1000 ciutats»** (li tocà La Verneda i La Pau).
- **Gregori Civera** i **Carmen Secanella** — projecte **«Una ciutat desconeguda sota la boira. Noves imatges de la Barcelona dels barris»** (MACBA, 21/06/2024–12/01/2025, comissari Jorge Ribalta).
- **Taula rodona MACBA «Fotògrafs a la perifèria»** (27/11/2024, Espai Fotogràfic **Can Basté**): Arnau Bach, Gregori Civera, Carmen Secanella i Mónica Rosselló. <https://www.macba.cat/ca/activitats/fotografs-a-la-periferia/> · exposició: <https://www.macba.cat/ca/exposicions/una-ciutat-desconeguda-sota-la-boira-noves-imatges-de-la-barcelona-dels-barris>.
- **Arxiu Històric de Roquetes-Nou Barris** — font principal de la fotografia veïnal: <https://arxiuhistoric.blogspot.com/> · Instagram [@arxiuhistoric9b](https://www.instagram.com/arxiuhistoric9b/) · revista «L'Arxiu» a <https://raco.cat/index.php/larxiu/issue/archive>.
- **Fòrum Fotogràfic Can Basté** — <https://www.canbaste.com/> (19è Fòrum). Espai institucional de fotografia del districte.
- **SENSE ENLLAÇ VERIFICABLE** (no inventar): Juan Manuel Rodríguez Coria **«Morocho»**, **José Antonio Cordoncillo** (el concurs porta el seu nom), **Rafael Juncadella**, **Eva Orti**, **Carlos Navas**, exposició **«L'àpat»** i reportatge «Collserola crema». Probablement consten només a publicacions de l'Arxiu (pendent cercar dins la revista «L'Arxiu», raco.cat).
- **Decisió pendent (usuari)**: on ubicar-ho — **A)** ampliar la secció «Història» de `qui-som.md`, o **B)** pàgina nova; i si s'estructura amb **pestanyes** (vegeu backlog).

### Estructura proposada per a la recerca (idea aportada per l'usuari, 2026-09-18)

> Objectiu: no una llista, sinó una **genealogia de la fotografia a Nou Barris (~1960–2026)** amb noms, col·lectius, espais, exposicions, llibres i arxius, i una columna **«per què és conegut?»** per distingir trajectòria professional de fons documental excepcional.

- **Dos pols documentals a creuar**: **Arxiu Històric de Roquetes-Nou Barris** (memòria fotogràfica del territori) i **Centre Cívic Can Basté** (fotografia contemporània, formació, exposició, Fòrum Fotogràfic).
- **Quatre categories** (eviten barrejar perfils):
  - **A. Fotògrafs de Nou Barris** — nascuts, residents o fortament arrelats, amb activitat fotogràfica significativa: Manresa, Cuesta, Mora, Montilla, Medina, Sala «Ulls», Joan «Linux»…
  - **B. Fotògrafs que han documentat Nou Barris** — de fora o vinculació territorial menys clara però amb obra significativa sobre el districte: Bach, Meloni, Rosselló, Civera, Secanella…
  - **C. Fotografia comunitària i de barri** — 9 Barris Imatge, Grup Foto Roquetes, Arxiu Històric, Morocho, Silva, Cordoncillo, Juncadella…
  - **D. Ecosistema fotogràfic de Nou Barris** — Can Basté + Fòrum Fotogràfic + formació + laboratori + exposicions + beques + fotògrafs que hi han passat.
- **Llista de treball** (1–9 ja a la nostra recerca; 10–17 nous aportats; 18–22 categoria B):
  1. Kim Manresa · 2. Manel «Ulls» Sala Aponte · 3. Jesús Atienza · 4. Manel Mora Palau · 5. Manel Montilla · 6. José María Medina «El Nostálgico» · 7. Grup Foto Roquetes · 8. Joan «Linux» Martínez · 9. 9 Barris Imatge (col·lectiu) · 10. Ginés Cuesta · 11. Juan Manuel Rodríguez «Morocho» · 12. Antonio Silva · 13. Eva Orti · 14. Carlos Navas · 15. Arnaldo Gil Albacete · 16. José Antonio Cordoncillo · 17. Rafael Juncadella · 18. Arnau Bach · 19. Myriam Meloni · 20. Mónica Rosselló · 21. Gregori Civera · 22. Carmen Secanella.
- **Humberto Rivas** — no és «fotògraf de Nou Barris», però **va ser professor de fotografia a Can Basté**, té una **plaça dedicada al districte** i Can Basté li va fer un homenatge: clau per entendre la cultura fotogràfica generada al districte (categoria D, no A).
- **Can Basté** (aportat per l'usuari, pendent de verificar): funciona **des de 1996** com a equipament especialitzat en fotografia; disposa de **plató, laboratori i estació digital** (analògic i digital); **19è Fòrum Fotogràfic Can Basté** convocat per al **novembre de 2026** amb beques de producció expositiva i publicació fotogràfica; exposició **«L'ahir i l'avui de Nou Barris»** (creua fotografies històriques de l'Arxiu amb noves interpretacions; hi apareix una **foto de Torre Baró d'Arnaldo Gil Albacete, 1990**).

### Verificació de fets/enllaços de la recerca (rodada 2, 2026-09-18)

- **Grup Foto Roquetes**: confirmat com a grup real de fotografia comunitària de Roquetes; hi consten obres de **Manel Villalba** i **Núria Orbaneja** (tots dos membres de 9 Barris Imatge). Font: <https://ctoniguida.wixsite.com/toniguida/fotos> («Fotos cedides pel Manel Villalba del Grup FotoRoquetes», «Fotos cedides per la Núria Orbaneja del Grup FotoRoquetes»).
- **Can Basté**: confirmat com a equipament especialitzat en fotografia (exposicions, tallers, agenda) a <https://www.canbaste.com/>; **19è Fòrum Fotogràfic Can Basté** actiu amb **beca expositiva i beca de publicació**; exposició «30 anys de Can Basté» (2025) → coherent amb la fundació ~1995/96.
- **Humberto Rivas**: confirmat com a figura clau de la fotografia a Espanya — Humberto Luis Rivas Ribeiro (**1937–2009**, nascut a Buenos Aires, instal·lat a Barcelona el **1976**; «el fotògraf del silenci»; retrospectiva al **MNAC 2006**; Fundación MAPFRE 2018; **Premi Ciutat de Barcelona d'Arts Plàstiques 1997**; biblioteca donada a la **UAB** el 2017). **Pendent de confirmar**: que fos professor a Can Basté, la plaça dedicada al districte i l'homenatge de Can Basté (no s'ha trobat cap font).
- **Arnaldo Gil Albacete** i l'exposició **«L'ahir i l'avui de Nou Barris»**: **sense font externa trobada** (caldrà preguntar o cercar a l'Arxiu/Can Basté).
- **19è Fòrum «novembre 2026»** i el detall de **plató/laboratori/estació digital**: aportats per l'usuari; confirmada l'existència i especialització del Fòrum, no la data exacta ni els serveis.

### Concurs Josep Anton Cordoncillo — recerca i cronologia (2026-09-18)

> Recerca aportada per l'usuari + verificació a l'arxiu propi (`content/posts/`). És una **peça pròpia** de la investigació: «Concurs Josep Anton Cordoncillo — 1990–2026».

- **Origen 1990 (deducció, no font)**: el post propi de **2008** (`content/posts/2008-03-29-concurs-fotogrfic-josep-antn.md`) diu literalment **«XIXª edició»**; el de **2009** (`2009-09-08-...`) diu **«XXena edició»**. Si la numeració és consecutiva, la primera edició seria **1990**. **Pendent** una font de 1990/1991 que ho confirmi.
- **Cronologia reconstruïda** (any → número; **negreta** = el post diu un número equivocat, error de xifra romana al títol):
  1990 I · 2008 XIX · 2009 XX · 2010 XXI · 2011 XXII · 2012 **XXIII** (post: «XIII») · 2013 **XXIV** (post: «XIX») · 2014 XXV · 2015 **XXVI** (post: «XVI») · 2016 XXVII · 2017 XXVIII · 2018 XXIX · 2019 XXX · **2020 (no consta cap edició; possible any saltat, p. ex. COVID)** · 2021 XXXI · 2022 XXXII · 2023 XXXIII · 2024 XXXIV · 2025 XXXV · 2026 XXXVI (en curs).
- **Anomalies de numeració** (anotar com a incidència documental, **no corregir a mà**): 2012 «XIII», 2013 «XIX», 2015 «XVI». La seqüència quadra de 2008 (XIX) a 2019 (XXX) i de 2021 (XXXI) a 2025 (XXXV) **si el 2020 no es va celebrar**.
- **Categories 2008–2011** (font pròpia): A color tema lliure; B B/N tema lliure; **C Premi Josep Anton Cordoncillo** (tema específic); **D Fotomòbil** (enviament per correu: 2008 a `cbarri@telefonica.net`, 2009 ja a `info@9barrisimatge.org`); E Infantil (des de 2009). Temes C: 2008 «20 anys de Casal de Barri», 2009 «Surrealisme», 2010 «Surrealisme», 2011 «Moviment Indignats 15M». Jurat: **Agrupació Fotogràfica de Catalunya** (2008–2010); **9 Barris Imatge** (des de 2011).
- **2012** (post «XIII», tema «Erotisme»): 24×30 cm sobre cartolina, lliurament físic; només fotos inèdites; màxim 3 per categoria; 150 € als guanyadors A/B/C.
- **2014** XXV: reportatge de **Manel Villalba**; àlbum a Picasa (títol «XXV», nom d'àlbum «XVConcurs…»).
- **2019** XXX: tema «Jubilats»; 100 € per categoria; premi del públic.
- **2021** XXXI: tema «Vacances, temps lliure»; guanyador Cordoncillo **Cristian Rodríguez** («El despertador»).
- **2022** XXXII: tema «Menjar»; jurat 9 Barris Imatge; concert **Daniel Higiénico**; el Casal ja el descriu com un «clàssic».
- **2023** XXXIII: tema «Petó»; **23 participants i 52 fotografies** (memòria del Casal); concert Sweet Marta & Johnny Bigstone.
- **2024** XXXIV: tema «Mirades»; concert **Jo Solana Trio**; el post diu explícitament «homenatge al membre fundador de 9 Barris Imatge que va deixar-nos».
- **2025** XXXV: tema «Peus»; bases digitals (1 foto/categoria, JPEG ≥4 MB, correu, RAW de verificació, **prohibició d'IA**); 100 € per categoria + 100 € vot popular; exposició al Casal al desembre (concert Dani Roto).
- **Cordoncillo (persona) — PENDENT**: només és documentat que era **membre fundador de 9 Barris Imatge** i que el concurs es manté en homenatge seu. Falten naixement/mort, barri, fotografia, fons i origen del nom. Pista: post propi **`content/posts/2010-11-07-lherencia-de-josep-anton-cordoncillo.md`** (enllaç a BTVnotícies, sense text) → possible mort/legat cap al 2010 (però el 2008 el concurs ja portava el seu nom).
- **Pendent**: reconstruir **35 anys de guanyadors** (any → tema → color → B/N → Cordoncillo → premi públic), que pot revelar fotògrafs no llistats. Fonts: arxius del Casal de Barri Prosperitat, de 9 Barris Imatge i de l'Arxiu Històric de Roquetes-Nou Barris.
- **Fonts de veritat per a les dades de cada edició** (2026-09-18): el **mateix blog 9barrisimatge.org** (la convocatòria s'ha publicat habitualment, ni que sigui amb una imatge) i el blog **`blog.pocallum.cat`** (que té totes les dades de cada edició). Ús per a la reconstrucció de l'arxiu del concurs i per al sistema de votació.

### Concurs — reestructuració en pestanyes (2026-09-18)

> Implementat (aprovat 2026-09-18). Fitxers: `content/concurs.md`, `assets/css/extended/custom.css`, `layouts/_partials/footer.html`, nou `layouts/_shortcodes/rel.html`.

- **3 pestanyes principals al capdamunt**: **L'edició 2026** (amb sub-pestanyes Bases / Com participar + botó PDF) · **Història del concurs** · **Els trofeus**. CSS pur amb radios (`name="concurs-view"` → `view-2026`/`view-historia`/`view-trofeus`); les sub-pestanyes mantenen `name="concurs-tab"` (`concurs-tab-bases`/`concurs-tab-participar`).
- **Més aire**: `.concurs` amb més marge; pestanyes, taula i seccions amb espaiat nou.
- **Història del concurs**: resum + **taula de cronologia 1990/2008–2026** (temes, fets destacats) + evolució del format + apartat Cordoncillo; els punts no confirmats (1990, 2020, numeracions 2012/2013/2015) marcats amb `.is-pending` «per confirmar».
- **Compartir + enllaços propis**: `.concurs-share` amb botons WhatsApp/Telegram/Correu/Copiar (JS a `footer.html`, via `location.href`) i enllaços a l'etiqueta del concurs (`/tags/concurs-fotogràfic-josep-antón-cordoncillo.html`), al Casal de la Prosperitat i a l'Arxiu Històric.
- **`layouts/_shortcodes/rel.html`** (nou): `{{< rel "/ruta" >}}` → `relURL` amb `TrimPrefix "/"`. Cal perquè els enllaços/imatges dins blocs HTML crus del markdown no passen pels hooks `render-image`/`render-link`. Utilitzat a `concurs.md` per a la imatge dels trofeus i l'enllaç de l'etiqueta.
- **Impressió**: `@media print` actualitzat per forçar `#concurs-2026` i el panell de Bases visibles.
- Build net (6.539 pàgines). Verificat: enllaços i imatge surten amb `/9bi/` (base-aware).

### Concurs — desplegament final (2026-09-18, sessió v4)

- **Títol de pàgina sense abreviatures**: `content/concurs.md` amb `title` sencer («Concurs fotogràfic Josep Antón Cordoncillo») + `visualTitle` (amb `<br>`) per a l'h1. Nou **`layouts/single.html` SOBREESCRIT** (còpia del tema): si la pàgina té `.Params.visualTitle`, l'usa com a h1 amb `safeHTML`; si no, `.Title`. **Atenció en actualitzar PaperMod.**
- **Subtítol amb enllaç al Casal**: `description` en text pla (per al `<meta>` net) + `visualDescription` (markdown) renderitzada com a subtítol visual a `single.html` (`{{ .Params.visualDescription | .RenderString (dict "display" "inline") }}`); hi ha enllaç a casalprospe.org.
- **4 pestanyes principals**: L'edició 2026 · **El vot del públic** · Història del concurs · Els trofeus (CSS pur, radios `name="concurs-view"`, `#view-vot`).
- **Pestanya «El vot del públic»**: premi de 100 € que decideix el públic; sistema digital de vot en estudi — **QR únic a l'exposició** + cada obra porta el seu **número** i al QR s'hi indica el número a votar; 1 vot per obra i dispositiu, anònim; votar al Casal de Barri de Prosperitat.
- **Botons de compartir amb icones SVG** (WhatsApp/Telegram/Correu/Copia) — text conservat.
- **Enllaços externs del bloc «Comparteix i enllaços»** trets (petició usuari): només queda l'enllaç intern a l'etiqueta del concurs.
- **Espaiat**: dates importants `4.8rem 0 2rem` (triple/doble); línia de Categories `3rem 0`; pestanyes inactives amb `background: var(--tertiary)`.
- **Bug icones del menú arreglat**: `.menu-icon` i `.menu-icon svg` ara tenen mida base **fora** de `@media (min-width: 769px)`; a ≤768px les icones es mostren a 17px (abans l'SVG sense width/height es renderitzava gegant i trencava el mòbil).
- **Abreviatures corregides** (`J. A. Cordoncillo` / `J.A.Cordoncillo` → nom sencer): `content/concurs.md` i posts `2014-12-16-...` i `2025-12-21-...`.
- Build net (6.539 pàgines). **Desplegat a Codeberg Pages** (branca `pages`).

### Peu amb l'ample del header i versió mòbil (2026-09-18, sessió v5)

- **`.footer` ara mesura com el header**: el tema fixa `max-width: calc(var(--main-width) + var(--gap) * 2)` (720px), mentre el header fa 1024 (`--nav-width`). Override a `custom.css`: `.footer { max-width: calc(var(--nav-width) + var(--gap) * 2) }`. **Atenció en actualitzar PaperMod.**
- **Versió de telèfon (≤480px)**: `.footer-cols` amb `grid-template-areas` → **Logo + «El web»** (costat a costat) · **«Legal»** amb tots els links en una sola línia · **«9 Barris en números»** amb totes les dades en una sola línia (separats per «·»).
- Classes noves als menús del footer: `footer-col--web` i `footer-col--legal` (a `layouts/_partials/footer.html`).
- **Títols de columna més grans** (aprovat 2026-09-18): `.footer-col-title` de `0.78rem` → **`0.95rem`**, mateix color `var(--secondary)`.
- **`.footer-bottom` en columna**: «Powered by…» centrat i a sota del copyright (CC), amb un **filet** `1px solid var(--border)` a sobre de la línia de Creative Commons.
- **Tasques anotades al backlog (2026-09-18)**: auditoria SEO i IA, document d'URLs de Blogger (SEO/redireccions), i links a Instagram + Grup de Facebook amb eina automàtica de publicació de posts nous (a més del bot de Telegram pendent).

### Diagnòstic del núvol d'etiquetes (`/tags/` i `/search/`)

- **A la pàgina de Cerca (`/search/`) NO hi ha núvol d'etiquetes** — cal afegir-lo (pendent d'aprovació).
- **Recompte real** (2026-09-18): 3.006 fitxers; **11.377 aparicions**; **1.742 tags literals** (1.719 normalitzats: espais/accents/majúscules).
- **23 grups de variants** a unificar (exemples): `exposicio`/`exposició` (102), `musica`/`música` (101), `presentacio`/`presentació` (78), `veins`/`veïns` (27), `VIA JULIA`/`vía júlia` (28), `torre baro`/`torre baró` (18), `República`/`republica` (28), `prego`/`pregó`, `futbol sala`/`futbol-sala`, `dia de la dona` (amb doble espai), `nit d´animes`/`nit d'ànimes`, `placa Àngel Pestaña`/`Ángel`, etc.
- **Famílies grans a unificar**: `prospe`(339)/`Prosperitat`(330)/`barri de Prosperitat`(96)/`la prosperitat`(66); `casal de barri`(140)/`casal barri prosperitat`(122)/`Casal de barri Prosperitat`(107)/`Casal de barri de Prosperitat`(95); `9 barris`(89)/`9barris`(52); `festa`(109)/`festes`(88).
- **890 tags amb 1 sol ús** — molts brossa: hashtags (`#el47 #lluitaveinal…`), dates (`29-09-2010`), noms puntuals, etc.
- **Etiqueta trencada detectada**: `manel sala "ulls` (73 aparicions, cometes desbalancejades).
- Eina d'anàlisi temporal usada: `/tmp/tag_analysis.py` (parseja el front matter de `content/posts/*.md`).

### Diagnòstic responsive: icones del header massa grans

- Causa probable: a `custom.css`, **`.menu-icon svg { width: 20px; height: 20px }` i `.menu-icon { display: none }` només existeixen dins `@media (min-width: 769px)`** (línies ~546–581). Per sota de 769px no hi ha cap mida per a l'SVG → l'SVG inline (viewBox sense width/height) es renderitza enorme i el span es mostra.
- Proposta (requereix aprovació de disseny): definir `.menu-icon`/`.menu-icon svg` amb mida base **fora** del media query i decidir el comportament mòbil (amagar icones o fer-les de ~18 px), o restringir les icones a escriptori.

### Altres

- **Eslògan «arreu»**: **aplicat i desplegat (2026-09-18)** — `config/_default/hugo.toml` (línia 50, `description`) i `content/qui-som.md` (línia 7).
- **Reestructurar el footer «amb lògica»**: **implementat (2026-09-18)** — amplada igual al header (`--nav-width`) i versió de telèfon: Logo + El web / Legal / Números, en una sola línia cadascuna.

## Sessió 2026-09-18 (v6) — Client ID CMS, depuració d'etiquetes, header scroll i membres amb actiu/històrics

- **CMS Client ID**: `static/admin/config.yml` amb `app_id: 0c6b6c51-bea8-4b64-8c1e-96bbf02eef15` — **commitejat (`dd36e51e`) i desplegat**, verificat en viu a `/9bi/admin/config.yml`. Redirect URI `https://9barrisimatge.org/admin/`, «Confidential client» desmarcat.
- **Depuració d'etiquetes APLICADA** (commit `215cdfc8`, desplegat): 3 passades (renames de variants + brossa; variants per cas; Vídeo→vídeo). **430 fitxers** (+315/−524). **Estat final**: 2.891 posts amb tags / 115 sense; **1.675 tags literals únics** (abans 1.743); **11.203 aparicions** (abans 11.382); **0 grups de variants**. Els **anys** com a tag s'han **conservat** (decisió editorial pendent).
- **Header scroll fix** (commit `a28ea96d`, desplegat): elecció de l'usuari «Canvi instantani» — se suprimeixen `transition: line-height 0.25s ease` i `transition: height 0.25s ease, margin 0.25s ease`; només queda `box-shadow 0.2s ease` (causaven tremolor en fer scroll).
- **Membres → carpeta amb actiu/històrics**: `data/membres.yml` **substituït per `data/membres/<slug>.yml`** (12 fitxers). Campos: `autor` (clau d'atribució, no es toca), `nom` (real), `malnom` (el que es mostra), `web`, `instagram`, `actiu` (bool, per defecte true).
  - Taula de membres (`_shortcodes/membres.html`): mostra el **malnom** (si no n'hi ha, el nom real); es parteix en **actius** i «**Membres històrics**» (`actiu: false`) a sota.
  - Pàgina d'autor (`author/term.html`): títol = **malnom** + línia amb el **nom real** (només si és diferent).
  - Peu «9 Barris en números»: comptador = **total (actius + històrics)**; ara llegeix el mapa `len (hugo.Data.membres)`.
  - Decap (`config.yml`): col·lecció `membres` passa de `files` a **folder** (`data/membres`, `identifier_field: autor`, `extension: yml`, `format: yaml`) amb el camp **ACTIU** (boolean, default true).
  - **Noms reals/malnoms confirmats per l'usuari (2026-09-18)**: Joan = «Linux»; Pedro Click = malnom (nom **Pedro García**); Manel Sala = «Ulls»; Pedro Cervera **sense malnom** (sort com «Pedro Cervera»); Francesc Barbe, Ismael Utrilla, Alberto Sanagustín, Iozsef Kiss, Manel Villalba **sense malnom**; Núria = «Nuria»; Nico YeYe = malnom de **Nico Derocal**; Juan Carlos = «Grismedio Casinegro».
  - **Limitació Decap**: no hi ha ACL per usuari/registre — els inactius «que ja no editen» es gestionen **traient-los l'accés d'escriptura a Codeberg** (no al config).
- **Peu — filet d'accent sobre «Powered by»**: `border-bottom` de `.footer-copyright` passa a **4px solid #e03131** (mateix gruix i color que la banda `.footer-band` que separa el footer de la resta).
- **`.gitignore`**: afegit `/.taques/` (gestió d'hores, local).
- **Pendents nous**: pestanya «9bi als mitjans» a Qui som (+ material de 27 links verificats de les edicions del concurs); chrome del CMS (header amb logo + «Edició de 9 Barris Imatge», footer igual que el web, Manual consultable des del header); demandes del llistat del CMS (ordenació més recents, miniatures, normalitzar **384 títols en majúscules**, permisos per usuari = inviable a Decap).

## Sessió 2026-09-18 (v7) — CMS: articles per anys

- **Camp `year` a tots els posts**: aprovat per l'usuari (col·leccions per any, opció «Recomanat»). Script `add_year.py` afegeix `year: YYYY` derivat de la `date` al front matter de **3.006 fitxers** (commit `81e67deff`, desplegat a `pages`). Rang: 2008 (102)…2026 (63), total 3.006, 0 errors; verificat que any coincideix amb la data en tots. El tema ignora la clau (clau de front matter extra inofensiva).
- **19 col·leccions filtrades al CMS (APROXIMACIÓ INICIAL, SUBSTITUÏDA a la sessió v8)**: `static/admin/config.yml` substitueix la col·lecció `posts` per 19 col·leccions tipus folder `posts-YYYY` amb `filter: { field: "year", value: "YYYY" }`, `create: true` i un camp `year` hidden amb default de l'any corresponent (perquè els posts nous entrin al filtre). Menú ordenat de més recent (2026) a més antic (2008). La llista de 13 autors es manté amb **ancoratge YAML** `x-autors: &autors` per no duplicar-la 19 vegades. **Nota (v8)**: el `filter` carregava igualment els 3.006 fitxers de la carpeta → penjament «carregant entrades a la cache»; substituït per subcarpetes físiques per any.
- **Resultat pràctic**: «Articles · 2026» mostra només els 63 posts d'aquell any (l'any per defecte primer); crear un post nou preomple l'any sol. Redueix el llistat de 3.006 a ~60–250 per any.
- **Chrome del CMS implementat** (commit `16534a4ae`, desplegat; pages `d1830af`): `static/admin/index.html` amb capçalera i peu propis usant el **Custom Mount Element** oficial (`<div id="nc-root">` + script `defer` — Decap munta la UI dins, no ocupa tota la pàgina). Header: logo (`../images/logo-header.jpg`) + **«9 Barris Imatge - Gestor de continguts»** + enllaços per consulta dels editors: **Guia i manual** (`#/collections/guia`), Articles · 2026 (`#/collections/posts-2026`), Membres i «Torna al web». Footer: **replica del del web** (banda accent `#e03131`, columnes logo · El web · Legal · 9 Barris en números amb links relatius `../`, CC BY-NC-SA + Powered by LinuxBCN/Hugo/PaperMod amb reveal; estils propis prefixats `cms-`, CSS inline, sense assets del web carregats). **Nota**: els números del peu del CMS (`3.006 posts · 24 anys · 12 membres`) són **estàtics** (quedaran vells); els del web es generen a cada build.

## Sessió 2026-09-18 (v8) — CMS: posts en subcarpetes per any + rail propi

- **Porblema**: les col·leccions amb `filter` carregaven tota la carpeta `content/posts` (3.006 fitxers) per mostrar-ne només 63 → el CMS quedava «carregant entrades a la cache». Decap aplica el filtre a client, no a server.
- **Solució (aprovada per l'usuari, opció «Moure per anys»)**: els **3.006 posts es mouen a subcarpetes físiques** `content/posts/YYYY/` (2008…2026). Les **URL no canvien**: els permalinks `/:year/:month/:slug` surten del front matter (`date` + `slug`), no del path. Verificat comparant l'arbre `public/` abans/després (8.446 pàgines idèntiques).
- **`config.yml` (commit `77e3d61c9`)**: les 19 col·leccions `posts-YYYY` ara apunten a `folder: content/posts/YYYY` (sense `filter`) i porten **`sortable_fields`** (`date` amb `default_sort: desc` → llistat de més recent a més antic dins de cada any).
- **Rail propi al CMS** (`static/admin/index.html`, mateix commit): barra lateral esquerra que **substitueix la sidebar nativa de Decap**:
  - «**Articles**» amb `<details open>` i els **19 anys** (2026→2008, 2026 actiu per defecte) enllaçant a `#/collections/posts-YYYY`;
  - «Seccions»: Membres, Guia i manual, Actes, Concurs Cordoncillo;
  - «Torna al web»; JS destaca l'any segons el hash (`#/collections/posts-YYYY`).
  - CSS: `#nc-root aside { display: none }` i `#nc-root main { padding-left: 0 }` per amagar la sidebar interna de Decap (classes internes → **fràgil davant actualitzacions de Decap**, versió fixada `^3.0.0`). A ≤900 px el rail passa a horitzontal amb els anys en files.
- **Scripts de migració**: `migrate_live.py` i `migrate_blogger.py` escriuen ara a `content/posts/YYYY/` (`os.path.join(args.output, pub.strftime("%Y"), …)`).
- Desplegat (webhook ~1-2 min en la verificació): main `77e3d61c9` → pages `65efc85d`. Verificat en viu: config amb `folder: content/posts/2026` + `sortable_fields`, i HTML del rail present.

## Sessió 2026-09-19 (v1) — votació per QR: pla + mòdul M1 fet i testejat

> **Abans de retocar el web**: els canvis d'aquesta sessió són **documents de planificació (`drafts/`)** i el **mòdul `modules/votacio/`** (0 afectació al web). Committejat el 2026-09-19 a `main` (`387f283a6`) i pujat a Codeberg; branca `pages` resincronitzada amb `origin/pages`.

- **`drafts/2026-09-19-votacio-pla-desenvolupament.md`** (nou): pla de la votació del públic. Seccions: 1) investigació (geofencing off/soft/hard; prova que el vot sense mòbil és «vot en paper»; RGPD: consentiment i never-store de coordenades; comparació d'allotjament), 2) abast M1, 3) estructura de fitxers, 4) pla de treball 11 passos, 5) decisions aprovades, 6) pendents.
- **Decisions de l'usuari (2026-09-19)**: 1) geofencing **off** per defecte global, **soft** a l'edició 2026 (radi **500 m**, centre Casal de Barri de Prosperitat, `lat=41.3948 lon=2.1775`); 2) sense mòbil → **vot en paper** (urna física + `tally --paper`); 3) `collect_data = none` el 2026; 4) allotjament: **primer Dinahosting compartit** (Passenger), VPS Lite (~34 €/mes) només si falla. Llicència proposada **AGPL-3.0** (per confirmar); repo `9bi-apps` (orientatiu).
- **Config = INI amb configparser (stdlib)**, no YAML → **zero `pip` en producció**.
- **`drafts/2026-09-19-apps-modulars-votacio-albums.md`**: document de la suite **completat i coherent**, títol ampliat a «Suit modular de programari lliure per a associacions i escoles de fotografia»; §6 «Mòduls futurs a avaluar — i el vincle amb Llumàtics» (inclou `tallers` i `sortides` com a candidats) + taula de candidats i regla de l'adoptant real; seccions reenumerades 7–12; Fase 7 afegida.
- **`drafts/2026-09-19-noms-suite.md`** (nou): proposta de noms per a la suite per categories; **top 5: Trípode, Objectiu, Revela, Enquadra, Focus**; decidir català vs internacional.
- **`modules/votacio/`** (nou, M1) — app WSGI **només stdlib**, sense dependències de tercers en producció:
  - `app.py`: rutes `/v/<token>` (GET form / POST vot), `/admin/` (login, recompte, export CSV signat, tancar, logout), `/health`. Vot per obra i dispositiu (HMAC-cookie), CSRF per petició, rate-limit per IP, geofencing off/soft/hard amb haversine, i18n ca/es/en, `connect()` auto-crea l'esquema.
  - `schema.sql` (taules edicions/obres/vots amb UNIQUE per duplicats), `config.example.ini`, `passenger_wsgi.py` (punt d'entrada Phusion Passenger per a Dinahosting/cPanel), `i18n/{ca,es,en}.ini`.
  - `tools/qr.py` (QR del cartell; `qrcode` només en dev o `qrencode`), `tools/tally.py` (+ `--paper`), `tools/audit.py` (verifica HMAC i duplicats).
  - **Testejar**: via WSGI i servidor real — vot OK, repetit bloquejat, token dolent 404, geo `hard` fora de radi → 403 i dins → 200, `soft` marca `out`, `off` ignora; `audit` 0 anomalies.
  - Config local `config.ini` **gitignored** (secrets fora del repo).
- **`scripts/picasa_to_photos.py`** + `drafts/2026-09-18-pla-recuperacio-albums.md`, `drafts/informe-links-trencats.md`, `drafts/emails-usuaris.md`, `drafts/2026-09-18-codeberg-usuaris.md`: documentació/script de la recuperació d'àlbums i dels usuaris Codeberg (vegeu backlog).
- **Pendent**: confirmar Python/Passenger al panell de Dinahosting i desplegar amb dates reals (1–15 des 2026), secrets reals (`secrets.token_urlsafe`) i `ssl=1`; confirmar AGPL-3.0 i crear el repo `9bi-apps`; moure el mòdul al repo nou.

## Sessió 2026-09-19 (v2) — cura de tags aplicada i reconciliació amb la sessió de casa

> La feina d'aquesta sessió (cura de tags, formulari, membres) s'havia fet sobre l'estructura **plana** antiga (`content/posts/*.md`) i va quedar sense commitejar. Mentrestant, una altra sessió (del 2026-09-18/19, des de casa) havia pujat a `main` tota la feina del CMS (posts en subcarpetes per any, camp `year`, rail, votació QR, «Santa Brava», …). Aquesta sessió ha **reconciliat** les dues línies: la cura es reaplica sobre l'estructura nova i es commiteja tot de nou.

### Cura de tags — REAPLICADA sobre l'estructura nova (258 posts a `content/posts/<any>/`)

- Mètode: es va salvar el treball del working tree a la branca `wip-cura-tags-plana` (commit `aeea1b18`), es va posar `main` a `origin/main` (c17741aa) i es van reaplicar les tags finals dels 258 fitxers des d'aquesta branca sobre els posts de l'estructura nova (preservant el camp `year` afegit per la sessió de casa i la resta del front matter).
- **143 posts** amb l'any com a tag **trets** (regla: eliminar tags-any excepte `1972`, nom d'una banda). Verificat: **0 anys restants com a tag**; `1972` conservat (1 post).
- **125 posts** sense tags (o només d'any) **curats** amb overrides confirmades: The Chanclettes → `ARTS ESCÈNIQUES` · SENYALS DE FUM (×2) → `música` + `Festa Major de la Prosperitat` · POR HAITI → `fotografia` + `solidaritat` · AntivirusProspe → `covid-19` + `solidaritat` · LLORENÇ FA 91 → `activisme` + `veïns`.
- Els 10 posts curades amb el comentari `<!-- tags auto-generades…revisar -->` s'han quedat sense ell. La resta de posts amb el comentari (1.687) resten intactes.
- **Formulari** (`content/contacte.md`): camp nou `entitat` (patró `assumpte`), entre `assumpte` i `missatge`.
- **Membres** (`layouts/_shortcodes/membres.html`): sense `web` → enllaç «Posts al blog» a la pàgina `/author/<slug>.html` (abans «—»); activats i històrics.
- Build local `hugo` **net** (verificat abans del commit).

### Nota per sessions futures

- La branca `wip-cura-tags-plana` es pot esborrar (ja integrada a `main`); si es manté, no esborrar fins a confirmar el commit de la sessió a `main`.

## Sessió 2026-09-20 — autors recuperats, membres veterans, Cordoncillo, header

- **Recuperació d'autors (2026-09-20)**: commit i deploy de la feina de la sessió anterior. **439 de 473 posts** reassignats (93%); **34 irresolubles** documentats a `drafts/autors-no-resolts.md` (comptes Google completament eliminats). Script `scripts/recupera_autors_blogger.py` v2 commitat.
- **Autors nous descoberts** (principal: **Pili E. G.**, 339 posts): 11 fitxers nous a `data/membres/` + 11 opcions noves al select del CMS (`static/admin/config.yml`, ara 24 opcions).
- **«Membres veterans»**: nomenclatura aprovada per l'usuari per al segon grup (en lloc de «Membres històrics»).
- **Josep Anton Cordoncillo**: afegit a `data/membres/` com a membre fundador honorífic (`rol: 'Membre fundador honorífic'`, `actiu: false`, sense posts al blog). El shortcode `layouts/_shortcodes/membres.html` **reescrit** per iterar `data/membres/` com a font primària (en lloc de la taxonomia), de manera que membres sense posts publicats apareixen igualment. Camp `rol` mostrat en cursiva quan `count=0`.
- **Noms i malnoms actualitzats**: Linux→Joan Linux, Ulls→Manel "Ulls", Nuria→Núria Orbaneja; Ivan Ortiz, Inma Alicio, Antonio Sedano, Pepa Calatrava com a noms reals; Sandra "Casal" i Ignasi "Casal" com a malnoms.
- **Bug tremolor header (fix definitiu)**: histèresi al listener de scroll — afegeix `.scrolled` a `scrollY > 120px`, treu-la a `scrollY < 90px`. Trenca el bucle reflow que causava el tremolor (el canvi de mida del logo de 229px → 48px provoca un salt de layout que modificava `scrollY` i tornava a fer toggle).

## Tasques pendents (backlog curt)

> **Anotat 2026-09-21 — 5 pendents dictats per l'usuari (per no oblidar-los; cap acció feta, només registre):**
> 1. ~~**Revisar i arreglar que surtin les imatges en miniatura al backend**~~ — **FET 2026-09-25** (commit `a04d62d56`; confirmat en viu per l'usuari).
> 2. **Revisar si ja algú ha iniciat el procès de creació del seu usuari**.
> 3. **Revisar que els que no son ADMIN (Tots menys jo i els que diré) només puguin veure els seus posts**.
> 4. **Migrar ja al domini de prodicció (9barrisimatge.org)**: Canviar DNS, revisar que tot es veurà bé, revisar que les URL actuals de blogger es redireccionen on pertoca i finalment desactivar el blogger.
> 5. **Ordenar a l'apartat de cerca les etiquetes per les que apareixen més a les que apareixen menys**.

> **Anotat 2026-09-24 — futures features no prioritàries:**
> 6. **Cerca per autor a la pàgina de l'autor** (baixa prioritat): a `/author/<slug>.html`, afegir un camp de cerca que filtra només els posts d'aquell autor. Ha de quedar clar a l'usuari que la cerca és limitada a l'autor. Implementació probable: Pagefind amb filtre de metadades per autor, o un camp `<input>` amb JS que filtra el llistat actual.
> 7. **/stats — indicar clarament des de quan es recullen les estadístiques** i el **total que teníem a Blogger** fins al canvi de Blogger a Taro Photo App. **FET el 2026-09-25.**
> 8. **Pàgina 404 amb cerca directa — FET (2026-09-25)**: `layouts/404.html` publica el missatge aprovat, cerca Fuse directa i enllaços a Portada, Arxiu i Contacte; resposta HTTP 404 real, `noindex` i validació responsive. Commit `70f4f626f9`, Actions `36115053496`.
> 9. **Test real de votació pública**: l'usuari proporcionarà `numero - títol - categoria` i farà un vot des del telèfon. Cal verificar la pàgina de vot, les instruccions, l'avís legal i els resultats finals quan la votació es tanqui a la data i hora indicades.

- **Pàgina de Crèdits (`content/credits.md`) — FET (2026-09-21)**: títol «Crèdits d'aquest projecte»; secció «Desenvolupament» reescrita (LinuxBCN a partir de la necessitat vista per **Joan Linux**, membre de 9 Barris Imatge: fer en programari lliure el que es portava a Blogger amb les seves limitacions — publicar àlbums per a perfils poc tècnics, dependència i poca flexibilitat de Blogger —; enllaç al repo `linuxbcn/9bi`); secció nova **«L'aplicació Taro»** (programari lliure per a associacions fotogràfiques: gestió i exhibició de fotografies; versió definitiva a LinuxBCN.com, ara en fase beta, suggeriments benvinguts especialment dels membres de 9bi); Python actualitzat a «les aplicacions dels mòduls de Taro (formularis, votació, autopublicació)»; **blog → web** a les FAQ («Puc fer servir les fotografies del web?», «En webs, xarxes…»).
- **Logo Taro al peu — FET (2026-09-21)**: fons blanc arrodonit (`<rect rx="230">`) dins `taro-logo-text.svg` (arrel + `assets/images/`) perquè es vegi en tema fosc (la flor és negra); el text «Taro» ja porta contorn negre (stroke) que l'aguanta sobre el blanc. `layouts/_partials/footer.html`: `a.taro-mark` amb el logo 69×70 + `<span class="taro-app-name">Photo App</span>` a sota. `custom.css`: flex columna, alineat esquerra, font «Helvetica Neue», color `var(--primary)` (fosc en clar / clar en fosc).
- **Formulari (`content/contacte.md`)**: **fet (2026-09-19)** — camp nou `entitat` ("A quina entitat de Nou Barris pertanys o representes (opcionalment)", input opcional, patró `assumpte`), entre `assumpte` i `missatge`.
- **Membres (`layouts/_shortcodes/membres.html`)**: **fet (2026-09-19)** — els membres sense `web` enllacen a «Posts al blog» (`/author/<slug>.html`) en lloc de «—».
- **`content/privacitat.md`**: **fet (2026-09-18)** — adreça real (Casal de Barri de Prosperitat) i **sense NIF** (el col·lectiu no en té); sense placeholders. (El correu ja hi és: info@9barrisimatge.org.)
- **Peu / legal**: peu de **5 columnes** fet (logo · buida · «El web» · «Legal» · «9 Barris en números»). `avis-legal.md`, `privacitat.md` i `cookies.md` tenen contingut publicat. Pendent: revisió jurídica final de la resta d'adequació RGPD.
- **Auditoria de seguretat**: **fet (2026-09-25)**; informe a `~/Desktop/cyber-neo-report-9arrisimatge.org-2026-09-25.md`, quick wins i correccions de la votació aplicats. Queden pendents els SHA-pin de CI/CD, la sortida de credencials de `deploy.sh`, 11 fitxers `.dl-*` i revisar `modules/taro/.gitignore`.
- **Enllaços d'àlbums trencats (Picasa Web → Google Photos)** (proposada 2026-09-18): quan Google va capturar/tanar Picasa Web, van quedar **llocs a enllaços d'àlbums morts a molts posts**. El camp `album_url` (extret per `migrate_live.py` del primer enllaç al voltant de la imatge) apunta a rels URLs de Picasa. Tasca fosca: **detectar quins `album_url` (i enllaços de Google Photos/Picasa dins dels posts) no funcionen** i **refer-los** o bé apuntar-los a l'àlbum equivalent de Google Photos si s'ha reconstruit. Nota de l'usuari: ell (Joan "Linux") va fixar els seus a mà, però **la resta d'autors no ho van fer** → cal revisar per autor. Estratègia proposada: revisar `content/posts/` per patrons `<a href="https://picasaweb.google.com/…">` (i variants) i valorar-ne la resposta HTTP, després decidir com refer-los (buscar a Google Photos pel títol/àlbum, o eliminar l'enllaç si no es recupera). Pot anar lligat al pipeline de votació/àlbums del Concurs.
- **Auditoria d'accessibilitat** (encarregada 2026-09-17, pendent).
- **Auditoria de SEO i IA** (encarregada 2026-09-18): deixar el web **ben preparat per a motors de cerca i agents d'IA** (metadades, dades estructurades, sitemap/robots, OpenGraph, etc.).
- **Document d'URLs de Blogger (SEO/redireccions)** (encarregat 2026-09-18): recull de **totes les URL actuals del blog Blogger** per comprovar que coincideixen amb les entrades actuals del web (l'estructura `/:year/:month/:slug.html` + `uglyURLs = true` ho preserva) o fer una **redirecció a la nova URL** — tema cercadors i SEO.
- **`content/qui-som.md`** (secció «Membres»): **implementat**. Shortcode `{{< membres >}}` itera `data/membres/` (24 fitxers: 12 actius + 11 veterans + Cordoncillo). Pendent: completar els **Instagram** que falten i no donar accés d'escriptura als membres inactius.
- **Comentaris al web**: implementar un sistema de comentaris amb **fort control d'spam** (pendent d'escollir la solució/proveïdor).
- **Compartir a xarxes**: botons per compartir fàcilment a **Instagram** i les xarxes que es portin ara (pendent).
- **Tipografies**: **implementat (2026-09-18)** — cos **Montserrat** (woff2 400/700/800) + títols **Gillius ADF** (OTF 400/700), autoallotjades a `static/fonts/`, `@font-face` i overrides a `custom.css` (urls `../../fonts/…`) i `preload` a `extend_head.html`. **Sense cap CDN** (RGPD). Pendent opcional: convertir els OTF de Gillius a woff2.
- **Votació popular per QR** (concurs): **`modules/votacio/` (M1) fet i testejat (2026-09-19)** — app WSGI stdlib (0 deps en producció): `/v/<token>`, admin recompte/export/tancar, CSRF, rate-limit, geofencing off/soft/hard, i18n ca/es/en. **Decisions 2026-09-19**: geo **soft** (radi 500 m Casal Prospe), sense mòbil → **vot en paper** (`tally --paper`), `collect_data=none`, allotjament **Dinahosting compartit (Passenger)** primer (VPS Lite ~34 €/mes només si falla). **Pendent**: confirmar Python/Passenger al panell de Dinahosting → desplegar (1–15 des 2026, secrets reals, `ssl=1`); confirmar **AGPL-3.0** i repo `9bi-apps`. Vegeu la sessió 2026-09-19 (v1).

- **Pestanyes a «Qui som»** (aplicat 2026-09-18): **4 pestanyes fetes** — Qui som (Història) · Com funcionem (Reunions + Com funcionem + subvencions) · Membres (`{{< membres >}}`) · Relacions (entitats + links amics) — amb el patró CSS pur del Concurs (radios `name="qsb-view"`, classes `.qsb-*` a `custom.css`). **Pendent: 5a pestanya «Història de la fotografia a Nou Barris»** (contingut de la recerca, sessió separada).
- **Història de la fotografia a Nou Barris** (aprovat: incloure a la pestanya nova): genealogia ~1960–2026 amb 4 categories (A fotògrafs de Nou Barris · B que l'han documentat · C fotografia comunitària/de barri · D ecosistema Can Basté) i columna «per què és conegut?»; noms sense font es marquen «pendent de verificar».
- **Núvol d'etiquetes a la Cerca** (`/search/`): **implementat (2026-09-18)**. La **depuració d'etiquetes** ja està **aplicada** (sessió v6). **2026-09-19 (v2)**: anys com a tag eliminats (excepte `1972`) i els **125 articles sense tag** curats — vegeu la sessió v2.
- **Responsive header**: **fix fet i desplegat (2026-09-18)** — mides base de `.menu-icon`/`.menu-icon svg` fora del media query; icones a 17 px al mòbil.
- **Footer «amb lògica»**: **implementat (2026-09-18)** — amplada igual a la del header (`--nav-width`) arreu; versió de telèfon: **Logo + «El web»** · **«Legal»** amb tots els links en una sola línia · **«9 Barris en números»** amb totes les dades en una sola línia.
- **Concurs Cordoncillo (investigació pròpia)**: biografia de Cordoncillo, origen documentat (1990), cronologia i 35 anys de guanyadors; incidències de numeració a l'arxiu.

## Infraestructura i comunicació (pendent)

- **Butlletí**: cal tenir un butlletí (newsletter) per al col·lectiu.
- **DNS i correu**: repensar què fer amb els DNS; es vol **correu gratuït i lliure per a cada membre** i un de **genèric** de l'entitat.
- **Grup de correu**: llista/grup per enviar un correu a tots els membres.
- **Telegram**: grup **privat** i **públic** (aquest darrer unidireccional, on s'envien els posts quan es publiquen). **Tasca (2026-09-18)**: muntar un **bot** (token de @BotFather), afegir-lo al grup, obtenir el `chat_id` i crear `scripts/telegram.py` que enviï missatges llegint `TELEGRAM_BOT_TOKEN` i `TELEGRAM_CHAT_ID` de l'entorn (mai al repo).
- **Xarxes socials (Instagram i Facebook)** (2026-09-18): posar links a l'**Instagram** i al **Grup de Facebook** al web, i dissenyar una **eina automàtica** perquè cada post nou es publiqui automàticament a IG i FB (mateix patró que el bot de Telegram pendent).

## Properes sessions

- **Muntar el CMS**: backend GitHub + entrada amb PAT **fets**. **Articles per anys fet (v7/v8)**: camp `year`, col·leccions en subcarpetes físiques per any (`sortable_fields` desc) + desplegable d'anys a la capçalera (v4). **Chrome del CMS fet**: capçalera amb desplegable d'anys, «Pàgines del web» i «Llegir la guia» / «Editar la guia»; peu reduït al filet vermell + CC + Powered by. Pendent: **convidar editors com a col·laboradors amb Write** i comprovar permisos reals; els membres inactius no reben accés. Queden pendents les altres demandes del llistat (normalització de títols en majúscules, etc.).
- **Control de fitxers del Concurs Cordoncillo** (bases, històric, etc.).
- **Secció per fer i gestionar les reunions** del col·lectiu.

## Decisions pendents per a la migració real (2026-09-17)

- **Etiquetes**: al blog original són molt incompletes (moltes entrades sense tag o amb tags inconsistents). No fer còpia cega amb `migrate_blogger.py` — caldrà revisar/curar les etiquetes, no assumir que el que hi ha al Blogger és la taxonomia final.
- **Autors**: **439/473 resolts (2026-09-20)**. 34 posts irresolubles (comptes eliminats) queden com «9 Barris Imatge» — documentats a `drafts/autors-no-resolts.md`. El CMS ja té tots els autors al select (24 opcions). Pendent: crear comptes GitHub i convidar els editors actius com a col·laboradors amb Write.

## El que encara no existeix (per no assumir)

- Migració de Blogger: **feta** (3.006/3.006 posts migrats; 3.008 fitxers actuals després dels articles nous). No cal l'export XML oficial: `scripts/migrate_live.py` llegeix el feed Atom en directe.
- ~~OAuth2 de Codeberg~~ **obsolet**: el CMS actual usa el backend GitHub i PAT classic; l'OAuth App de GitHub continua sent opcional.
- ~~Pàgina de privacitat amb placeholders.~~ **FET (2026-09-18)** — adreça real, sense placeholders.
- ~~Lloc GoatCounter i API key.~~ **FET (2026-09-25)** — `9bi.goatcounter.com`; secret disponible a GitHub Actions.
- Confirmació que `info@9barrisimatge.org` rep correus (FormSubmit).
- ~~DNS cap a Codeberg Pages.~~ **FET** — producció a GitHub Pages; Codeberg és només backup.
- ~~Contingut real de `cookies.md`.~~ **FET** — política publicada; pendent només la revisió jurídica final de la resta d'adequació RGPD.
- Configuració SEO/IA per a tot el web (metadades, dades estructurades, etc.).
- Suport Python/Passenger al panell de Dinahosting sense confirmar (per al desplegament de `modules/votacio/`).
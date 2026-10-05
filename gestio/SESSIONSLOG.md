# Historial de sessions — 9 Barris Imatge

Notes detallades de les sessions de treball, des del 2026-09-17.
Per a l'estat actual i la configuració del projecte, vegeu [`CLAUDE.md`](../CLAUDE.md).

## Sessió 2026-10-04 (vespre) — Miniatures de portada i cobertes externes mortes

- **Diagnòstic**: el mosaic de la portada (`layouts/index.html`) carregava l'original de `cover.image`, sense miniatures generades (les imatges viuen a `static/`, que Hugo no processa). Les 3 entrades més noves (29/09 i 01/10) apuntaven a originals de `static/images/` (512 KB PNG, 400 KB JPG i 156 KB WebP), mentre la resta de `covers/` feien 23–225 KB. La portada pesava ~1,5 MB.
- **Fix**: generades 3 miniatures WebP de 640 px (`cordoncillo-36`, `img-3603`, `libros-mellizos`) i canviat `cover.image` dels 3 posts. Portada: ~1,5 MB → ~0,58 MB. Commit `d3b79bef9c`, workflow `37226981213` OK i verificat en viu.
- **Auditoria de les 19 cobertes externes**: 18 mortes (404 o DNS/TLS) i 1 viva (Blogger). Cap post tenia imatge local ni al cos.
- **Recuperades 6**: `xix-concurs-cordoncillo-2013`, `xxii-concurs-cordoncillo-2011` i `exposicio-les-casernes` (Wayback/casalprospe), `festes-2013` i `picnic-de-blues-2013` (Wayback/Flickr) i `ballada-sardanes-2020` (Blogger viva), convertides a WebP 640 px. El `cap-de-creus` no s'ha pogut recuperar (l'única captura de Wayback és una pàgina HTML, no la imatge).
- **Tretes 13 cobertes** irrecuperables: eliminat el bloc `cover:` i les entrades mostren el placeholder amb el títol. YAML validat i 0 cobertes externes al build. Commit `cac4f3a152`, workflow `37227842628` OK i verificat en viu (les 6 imatges responen 200).
- **Pendent detectat**: uns quants `album_url` (botó «Veure tot l'àlbum») apunten a dominis morts fora de Picasa (casalprospe, ulls.info, linuxbcn.homeip, cybercasal9b, dropbox, posterous…) → nova **T-33**.
- **Tasques**: cap tasca de la llista tancada; alta de T-33. Registre horari a `.taques/2026-10-04.md`.

---

## Sessió 2026-10-04 — Taro Photo App publicat a Codeberg (v1.0.0 i v1.0.1) i pàgina a LinuxBCN

- **Sincronització**: `git fetch github --prune`; `main` = `github/main` (`0ac6cc9c44`). El remot `origin` (Codeberg `linuxbcn/9bi`) responia «Cannot find repository»: l'usuari l'havia esborrat. Recompte: 3.010 posts i 24 membres (12 actius).
- **Branca neta de Taro**: creada `taro-neta` des de `distribucio` en un worktree (`tmp/taro-neta`). Tret el contingut i els interns del 9bi (`.taques/`, `CLAUDE.md`, `drafts/`, `recuperacio/`, `.github/`, `.forgejo/`, `sync-9bi.sh` i els scripts de migració) i els mòduls de producció duplicats (`modules/formularis`, `modules/votacio`, `modules/autopublica`), que ja són dins del bundle `modules/taro/`.
- **Generalització**: referències del 9bi substituïdes per valors d'exemple o `[POSA-HI: …]` (Telegram, comentaris, CSS, `config/`, `data/`). Reescrits `README.md`, `modules/README.txt` i `data/README.txt`; nous `INSTALL.md` (requisits i instal·lació de cada part) i `CHANGELOG.md`. Es conserva l'atribució al 9bi com a cas fundador.
- **Publicació v1.0.0**: snapshot d'un sol commit (`24ae3471da`, 241 fitxers, ~4 MiB) a `codeberg.org/linuxbcn/taro-photo-app` (`main` + tag `v1.0.0`). Build de Hugo net (18 pàgines) i Python compilat.
- **Autoria v1.0.1**: per indicació de l'usuari, l'autoria passa a **Joan "Linux" Martínez i Serres (LinuxBCN.com)** a les capçaleres de copyright dels 13 `.py`, `LICENSES/README.md`, `modules/taro/README.md`/`.txt`, `README.md` i `CHANGELOG.md`. Republicat: `main` = `e1ad2a4a26`, tags `v1.0.0` i `v1.0.1`.
- **Pàgina de LinuxBCN** (`linuxbcn-2026/linuxbcn`): fitxa `content/projectes/taro-photo-app/` (CA+EN) actualitzada (`lastmod`, enllaç al repo nou i punt a «Fet»). Commit `5a09705`, build de producció, `rsync` al servidor i permisos; verificat en viu.
- **Crèdits del 9bi**: `content/credits.md` reescrit (el web viu a GitHub; el Taro es distribueix des de Codeberg) i `drafts/2026-09-27-taro-photo-app.md` actualitzat a la v2. Commit i push `c817b57355`; verificat en viu.
- **README del contenidor Taro** (`taro-photo-app/README.md`): el web del 9bi és producció a `112books/9bi` i el repo genèric és a Codeberg `linuxbcn/taro-photo-app`.
- **Script `scripts/publish-taro.sh`** (commit `81c0bc2490`): publica una versió nova (build de verificació + snapshot d'un commit + `push --force` a `taro main` + tag `vX.Y.Z`), amb mode `DRY_RUN` per comprovar-ho sense publicar.
- **Tasques**: T-29 i T-32 a «Fetes»; T-22 i T-28 a «Tancades sense fer» (el repositori vell s'ha esborrat). Registre horari a `.taques/2026-10-04.md`.

---

## Sessió 2026-10-02 (vespre) — Sincronització, peu del CMS i camp de vídeos

- **Sincronització**: el `main` local anava 36 commits enrere de `github/main` (producció, GitHub); `git pull --ff-only github main` ha fet fast-forward fins a `c949802900`. Recompte: 3.010 posts i 24 membres.
- **Peu del CMS**: verificat que ja s'havia eliminat al commit `cfd0e3ba86` (1/10) i que `/admin/` en directe no en té. Restava només CSS mort `.cms-footer*` (sense cap element) a `static/admin/intern/index.html`; eliminat (línies 218–291).
- **CMS `config.yml`**: ampliat el hint de «Cos de l'article» de les 19 col·leccions d'anys amb com incrustar vídeos: `{{< youtube ID >}}` i `{{< vimeo ID >}}`; els exemples van entre accents perquè Sveltia renderitza el hint com a Markdown. Shortcodes natius de Hugo provats abans en un projecte de prova. Commit `d2789d6097`.
- **Guia pública**: afegida la secció «Vídeos de YouTube o Vimeo» a `content/guia/publicar-article.md`.
- **Verificació**: `hugo --minify --environment production` OK (6.471 pàgines) i desplegament confirmat a `https://9barrisimatge.org/admin/config.yml`.
- **Vídeo de Vimeo (Andrés Naya)**: el shortcode havia quedat malmès (`{ { < [url](url) > } } ;`) perquè l'editor rich text de Sveltia destrueix els `{{< ... >}}` en desar. Corregit a `{{< vimeo 1232409395 >}}`.
- **Editor per defecte (revert)**: l'usuari prefereix que els editors vegin l'editor enriquit com abans; es retira el `modes: [raw, rich_text]` de tots els camps (el mode «Edita en Markdown» ja és disponible per defecte).
- **Camp de vídeo (solució robusta)**: com que l'editor enriquit esborrava els shortcodes en desar (el commit `f47dd64aa1` va eliminar el vídeo del post d'Andrés Naya), s'afegeix un camp `video` (URL de YouTube o Vimeo) a les 19 col·leccions d'articles; `layouts/_partials/extend_post_content.html` en renderitza el reproductor responsiu. El post s'ha migrat al camp i el hint del cos i la guia s'han simplificat.
- **Vídeo retirat (pendent de permís)**: l'usuari ha buidat el camp `video` del post d'Andrés Naya (`video: ''`, commit `480ffef535`) perquè encara no té permís per publicar-lo; la resta de la solució (camp + plantilla) queda disponible per quan el tingui.
- **Diversos vídeos per article**: el camp `video` es converteix en `videos`, una llista d'enllaços (widget `list`), opcional; la plantilla en renderitza un reproductor per element i manté compatibilitat amb el camp singular antic.
- **Tancament de sessió**: `main` = `github/main`, arbre net (últim commit `628ce3eacf`); SESSIONSLOG i control horari actualitzats.

---

## Sessió 2026-10-01 (tarda) — Àlbums: aplicar enllaços nous i filtrar els corregits

- **Context**: l'usuari havia corregit àlbums des del CMS («Àlbums per arreglar · Joan Linux») i dubtava si els posts s'actualitzaven sols. Verificat: **no**; el CMS només desa la fitxa a `recuperacio/`, i cal el pas final manual.
- **Pipeline verificat end-to-end** (`scripts/albums_fix.py`): `recull` (10 enllaços) → `validate` (10/10 HTTP 200) → `apply --write` → commit `b42e04f85`. 10 posts actualitzats (9 `album_url` + 10 enllaços al cos). El nou enllaç substitueix l'antic de Picasa, query inclosa.
- **CMS — camp «Àlbum» visible**: a les 8 col·leccions de recuperació, `album` passa de `widget: hidden` a `widget: string, readonly: true` perquè es pugui **seleccionar i copiar** el nom i cercar-lo a Google Photos. Commit `9a7043c5e`.
- **CMS — filtre de corregits**: afegit `filter: { field: url_nova, value: ["", null] }` a les 8 col·leccions; les fitxes amb enllaç desat desapareixen de la llista, però el fitxer es conserva perquè `recull` el trobi. Verificat contra el codi de Sveltia 0.217.0 (`matchesCollectionFilter`, `value ?? null`). Commit `3c33b4b7c`.
- **Fitxes**: 1.178 pendents (Joan Linux 445 · 9BI 232 · Manel «Ulls» 192 · Pedro Click 191 · Pedro «Casal» 49 · Alberto Sanagustín 33 · Manel Villalba 20 · Nico YeYe 16) i 10 corregides.
- **Sync**: `git pull --rebase` (el CMS havia empès 2 fitxes mentre treballàvem) i push a `origin/main`.

---

## Sessió 2026-10-01 — CMS: millores de camps i fix d'estadístiques

- **CLAUDE.md reduït** (697 → 173 línies): historial de sessions mogut a `gestio/SESSIONSLOG.md`, recerca de fotògrafs i concurs a `gestio/RECERCA.md`.
- **CMS `config.yml`**: camp `seoTitle` reordenat just a sobre de la descripció en els 19 reculls d'any; hint al camp d'etiquetes aclarint que cal usar Intro o el botó «+» (la coma no divideix etiquetes a Sveltia).
- **CMS `index.html`**: footer eliminat completament (CSS + HTML, 87 línies). Estava buit de contingut útil i interfereixi amb l'editor del cos de l'article. Commit `cfd0e3ba86`.
- **Estadístiques (`/stats/` i `/mes-visitats/`)**: `analytics.json` i `popular.json` congelats des del 24/09 i del deploy inicial respectivament. Causa: `GOATCOUNTER_API_KEY` absent de GitHub Actions Secrets. Solucionat: clau posada, `workflow_dispatch` verificat, tots dos scripts actualitzen correctament.
- **Aclarit**: les «1000 visites» d'Instagram eren impressions del post, no clics al web. GoatCounter compta menys per ad blockers.

---

## Sessió 2026-09-17 — Migració real des de Blogger

- **Migrat**: `scripts/migrate_live.py` — 3.006/3.006 posts des del feed Atom en directe (sense export XML). Mapeig d'autor per `<author><uri>` (taula `AUTHOR_BY_URI`). Vocabulari de tags real agregat per suggerir-ne als posts sense cap (marcats amb comentari HTML `<!-- tags auto-generades... -->`).
- **Bug corregit**: dedup per URL original (no per slug) — el primer intent en va perdre 118 posts amb slug repetit en mesos diferents.
- **Advertència**: `album_url` s'extreu del primer enllaç que envolta la primera imatge; si n'hi ha més d'un rellevant, pot no ser el millor (detectat al post Prospe Beach 2026).
- **Formulari RGPD**: `content/contacte.md` amb consentiment obligatori + honeypot + bloc informatiu. `content/privacitat.md` nou amb adreça real (Casal de Barri de Prosperitat, Plaça d'Ángel Pestaña, s/n, 08016 Barcelona).
- **Menú del peu reordenat**: Arxiu → Etiquetes → Més visitats → Estadístiques → Cerca → RSS.

### Mapeig d'autors (verificat, comptatge real per `<author><uri>`)

| Posts | Nom Blogger | Membre |
|---|---|---|
| 1307 | Joan Martinez i Serres "linuxbcn" | Joan "Linux" Martínez i Serres |
| 397+11 | PredroClick / pedro click (2 comptes) | Pedro Click |
| 274 | Manel Sala "Ulls" | Manel Sala "Ulls" Circ |
| 118 | francesc barbe | Francesc Barbe |
| 110 | ismaelug | Ismael Utrilla |
| 86 | Alberto | Alberto Sanagustín |
| 78 | Iozsef Kiss | Iozsef Kiss |
| 53 | pedrocasal | Pedro "Casal" Cervera |
| 29 | núria laura orbaneja | Núria Laura Orbaneja |
| 27 | manel villalba | Manel Villalba |
| 26 | Ulls (2n compte) | Manel Sala "Ulls" Circ (verificar) |
| 12 | Nico YeYe | Nico YeYe |
| 5 | Gris Medio,casi negro | Juan Carlos Molina (Grismedio Casinegro) |
| 469+2 | Unknown / Anonymous | "9 Barris Imatge" (genèric) |
| 2 | Nou Barris Imatge | "9 Barris Imatge" |

---

## Sessió 2026-09-18 — Membres, imatges, peu, legal, subvencions i concurs

- **Membres**: `data/membres/<slug>.yml` (12 fitxers), camps `autor`, `nom`, `malnom`, `web`, `instagram`, `actiu`. Taula al shortcode `membres.html` (actius + «Antics membres»). Pàgina d'autor (`author/term.html`) amb mosaic paginat.
- **Peu**: 5 columnes (logo · buida · El web · Legal · Números), banda accent `#e03131`, CC badge, reveal de LinuxBCN. Ample = `--nav-width`. Responsive 5→3→2→1.
- **Taxonomia `author`**: valor = `"author"` (no `"authors"`).
- **Tema fosc**: `defaultTheme = "dark"`.
- **Capçalera sticky amb icones SVG**: `layouts/_partials/header.html` sobreescrit; JS afegeix `.scrolled` a >120px; histèresi a 90px (fix tremolor).
- **Imatges base-aware**: `layouts/_markup/render-image.html` amb `relURL`.
- **`content/subvencions.md`**: pàgina filla de Qui som (`url: /qui-som/subvencions/`), amb alias de l'antic URL.
- **Concurs Cordoncillo** (`content/concurs.md`): 4 pestanyes CSS pur (Edició 2026/Vot del públic/Història/Trofeus), calendari, bases, botons de compartir.
- **Tipografies**: Montserrat (cos) + Gillius ADF (títols), autoallotjades a `static/fonts/`.
- **CMS Client ID**: `app_id: 0c6b6c51-bea8-4b64-8c1e-96bbf02eef15`.
- **Depuració de tags**: 430 fitxers modificats, 1.675 tags literals únics (de 1.743). 0 grups de variants. 143 posts amb l'any com a tag: eliminats (excepte `1972`).
- **Posts en subcarpetes per any** (`content/posts/YYYY/`): les URL no canvien (permalink del front matter). 19 col·leccions al CMS amb `sortable_fields: date desc`.
- **Chrome del CMS**: `static/admin/index.html` amb capçalera + peu + rail propi (desplegable d'anys 2026→2008, Documentació, Àlbums, Administració). Lateral nativa del Sveltia amagada (`#nc-root .primary-sidebar { display:none !important }` + `MutationObserver`).
- **`layouts/single.html` sobreescrit**: usa `visualTitle` (si present) com a h1 amb `safeHTML`.

---

## Sessió 2026-09-19 — Votació per QR: pla + mòdul M1

- **`modules/votacio/`** (M1): app WSGI stdlib, sense dependències de tercers en producció. Rutes `/v/<token>` (formulari/vot), `/admin/` (login, recompte, export CSV, tancar, logout), `/health`. Vot per obra i dispositiu (HMAC-cookie), CSRF, rate-limit, geofencing off/soft/hard, i18n ca/es/en.
- **Decisions**: geofencing `soft` 500m, `collect_data = none`, allotjament Dinahosting compartit.
- **`drafts/2026-09-19-votacio-pla-desenvolupament.md`**: pla complet de la votació.

---

## Sessió 2026-09-20 — Recuperació d'autors i membres

- **Recuperació d'autors**: 439/473 posts reassignats (93%); Pili E. G. (339 posts) descoberta principal. 34 irresolubles a `drafts/autors-no-resolts.md`. Script `scripts/recupera_autors_blogger.py` v2.
- **11 membres nous**: fitxers nous a `data/membres/` + opcions al CMS (ara 24).
- **Josep Anton Cordoncillo**: membre fundador honorífic (`actiu: false`, sense posts). Shortcode reescrit per iterar `data/membres/` com a font primària.
- **«Antics membres»** (terme definitiu, confirmat 2026-09-28; havia passat per «Membres veterans»).

---

## Sessió 2026-09-21 — Quota de Codeberg: diagnòstic

- **Causa de la mida**: el deploy antic feia `git push -f` a `pages` amb tot el build (~164 MiB); objectes orfes acumulats. Repo local comprimit: ~254 MiB.
- **Quota**: límit per usuari de 750 MiB. Ús de `linuxbcn`: ≈756 MiB → push rebutjat (`Forgejo: Quota exceeded`).
- **Deploy incremental** implementat a `sync-9bi.sh`: clon persistent a `~/.cache/9bi-pages`, fast-forward, sense force-push.
- Context complet: `drafts/2026-09-21-quota-codeberg.md`.

---

## Sessió 2026-09-24 — DIAGNÒSTIC DEL DEPLOY A CODEBERG (historial)

> Ara obsolet per a producció (migrada a GitHub Pages). Es conserva per a entendre el passat.

- Causa arrel: dos llocs (staging + domini) requerien dos webhooks separats a Codeberg.
- La DNS apuntava a Codeberg (`217.197.84.141`) i el webhook del domini estava desactivat.

---

## Sessió 2026-09-24 — Migració de producció a GitHub Pages

- **Motiu**: quota de Codeberg insostenible.
- **Repo nou**: `https://github.com/112books/9bi` (públic). Remotes locals: `origin` = GitHub, `codeberg` = Codeberg (backup).
- **Workflow**: `.github/workflows/deploy.yml` — Hugo 0.164.0 + stats opcionals + deploy Pages.
- **Producció**: `https://9barrisimatge.org/` → DNS canviada als IPs de GitHub Pages (185.199.108.153/.109/.110/.111). TLS emès per GitHub. `Enforce HTTPS` actiu.
- **Cert TLS**: va requerir treure i tornar a posar el domini al panell (no via API); fix aplicat el 2026-09-25.

---

## Sessió 2026-09-25 — CMS a GitHub, seguretat, guia i peu

- **CMS ↔ GitHub**: `backend: github`, repo `112books/9bi`, branca `main`. Entrada amb PAT classic (scope `repo`).
- **Miniatures al CMS** (commit `a04d62d56`): 2.911 valors `cover.image` normalitzats de `images/covers/…` a `/images/covers/…`.
- **Col·lecció «Pàgines del web»**: 13 pàgines fixes editables al CMS; camps tècnics com a `hidden`.
- **Rail propi del CMS** (commit `8d98f192f`): lateral nativa amagada; `<aside class="cms-rail">` propi. Articles per any (desplegable), Documentació, Àlbums (per login) i Administració.
- **Guia publicada sense indexar**: `content/guia/` amb `robotsNoIndex + hiddenInRss + sitemap.disable`.
- **Auditoria de seguretat** (informe: `~/Desktop/cyber-neo-report-9arrisimatge.org-2026-09-25.md`): Risk Score 49/100. Quick wins aplicats (commit `b700c5bbc4`): `.gitignore`, fail hard als secrets, noindex al CMS. Lot audit votació (commit `ee7769edf5`): cookies Secure, rate limit admin, CSRF POST /admin/tancar, caducitat de sessió, cap de mida 64 KB.
- **Peu del CMS reduït**: filet vermell + CC + «Powered by LinuxBCN with Hugo & PaperMod».
- **404 útil** (commit `70f4f626f9`): `layouts/404.html` amb cerca directa, `noindex`, HTTP 404 real.
- **GOATCOUNTER_API_KEY**: afegida a GitHub Actions secrets. `/stats/` es refresca a cada deploy (cron cada 6 h).

---

## Sessió 2026-09-25 (v2) — Guia, formularis i sincronització

- **Formularis** (commit `57b021ae78`): `modules/formularis/` al servidor (`~/apps/formularis/`, port 8302, htaccess proxy). SMTP directe de Dinahosting: `9barrisimatge-org.correoseguro.dinaserver.com:465`. `config.ini` al servidor (600). Formularis `/contacte/` i `/incorpora-te/` apunten al nou servei. FormSubmit desactivat.
- **Guia d'editors**: `content/guia/crear-compte.md` amb GitHub + PAT. Correu d'invitació preparat a `drafts/emails-usuaris.md`.

---

## Sessió 2026-09-26 — Mode de proves de la votació

- **Punt del geofence corregit**: Casal de Barri de Prosperitat, Plaça d'Àngel Pestanya (08016): `lat = 41.441623`, `lon = 2.179794`, `radi = 500`. El punt anterior (41.3948/2.1775) era a 5,2 km.
- **http→https**: `.htaccess` redirigeix totes les rutes `http→https` (sense afectar `.well-known`).
- **`revote_minutes`**: en mode proves = 10 min; en producció = 0 (1 vot per obra i dispositiu).
- **Privacitat al formulari**: coordenades no es desen, cookie `vid` HttpOnly.
- **`connect()` sincronitza config** (nom, dates, geo, etc.) al registre de l'edició en cada arrencada, sense tocar obres ni vots.

---

## Sessió 2026-09-27 — Paquet Taro, llicències i votació

- **Regla del proveïdor**: cap document públic ni el paquet distribuïble ha de dir «Dinahosting». LinuxBCN ofereix l'allotjament com a servei propi.
- **Quatre bugs corregits**: `SELECT *` amb SQLite nou, `UnboundLocalError body_estat`, `mktemp -d` al deploy, `html_link()` sense URL.
- **Protecció TLS als `.htaccess`**: condicions `%{HTTPS}` + `X-Forwarded-Proto` per evitar bucles de 301.
- **Llicències**: AGPL-3.0 + `LICENSES/` amb avisos de tercers. Sveltia és MIT (no GPL-3.0).
- **Data d'activació definitiva**: votació obre **01/12/2026 00:00**, es tanca **15/12/2026 23:59:59**.
- **BBDD buida** al servidor (8 vots de proves esborrats). `/admin/obres` 200 verificat.
- **PENDENT CRÍTIC (T-01)**: la BBDD conté les 100 obres de prova. Cal substituir-les amb la llista real abans del 30/11 i esborrar `data.db`.

---

## Sessió 2026-09-28 — Telegram, compartir, comentaris, títols

- **Autopublicació Telegram** (commit `33d5a437d`): `modules/telegram/telegram_post.py`, feed `/posts/`, cron 30 min, `state.json` amb 3.008 guids marcats. **No tocar `state.json`**.
- **Botons de compartir** (commit `7e5406ec6`): `layouts/_partials/post-share.html`, icones rodones per post.
- **Comentaris** (commits `d4b7c6a45`, `f4cb6d8c1`): `modules/formularis/comentaris.py`. Flux: formulari → pendent → correu a info@ → revisió signada (HMAC) → «Publica» crea `data/comentaris/<fitxer-post>/<id>.json` via API GitHub → commit → build. «Descarta» provat OK. **«Publica» pendent de provar amb el primer comentari real.**
- **399 títols normalitzats** (commit `969076cc4`): només el camp `title`; URL intactes.
- **RSS**: peu i `/contacte/` apunten a `/posts/index.xml`.
- **T-15 tancada**: butlletí aparcat; comunicació per Telegram intern.
- **T-14 (Instagram/Facebook)**: de moment manual. 2.930/3.008 posts tenen portada.

---

## Sessió 2026-09-28 (v2) — GoatCounter i distribuïble Taro

- **GoatCounter** (commit `16bdec539`): `/stats/` usa `total` de `/stats/total` (no la suma de hits limitats a 50 pàgines).
- **Branca `distribucio`** (local, `90ebcc6379` + `af8a537d6f`): plantilla Taro sense contingut del 9bi, marcadors `[POSA-HI: …]`. **No publicada** (bloquejada per quota de Codeberg).
- **Codeberg**: branca `pages` esborrada. Compte a 752,7 MiB. GC demanat a issue #2522 (comentari 28/09 20:17).

---

## Sessió 2026-09-28 (v3) — Estadístiques i títols (T-08/T-30)

- **T-08** (commit `699e52a1b5`): 95 canvis de títol (21 «Sense títol» + 75 repetits), esborrat post buit `2008-04-08-blog-post.md`. Build: 8.707 pàgines, 3.007 posts.
- **T-30** (commits `d2cc9eacf9`, `d6cd104746`): 6 títols llargs escurçats + convenció Joan Linux `any-mes-dia - títol` als 26 posts seus.
- **Estadístiques** (commit `27d4b914ff`): `hits_by_day` construïda des de `stats` de `/stats/total` (suma quadra). Etiqueta «total any» → «total període».

---

## Sessió 2026-09-29 — Concurs: guanyadors, trofeus, franja de capçalera

- **Guanyadors del concurs** (commit `c900a64d1a`): recerca a `blog.pocallum.cat`, Blogger, Casal i Wayback Machine. Afegits 2023, 2022, 2019, 2018, 2017, 2016 i 2014.
- **2020 confirmat**: no hi va haver edició (comunicat 28/09/2020 pel tancament del Casal).
- **Trofeus Carlitos** (commit `2ee33f6af5`): `trofeus-9bi-carlitos.jpg` a «Els trofeus», reduïda al 50%.
- **Ordre taula**: 2026→1990 (commit `f83d399461`).
- **Crèdit logotip** (commits `cb21aac09d` etc.): Toni Pagès, 2002, Instagram `pages2147`.
- **Franja de capçalera** (commits `bd0129a3a6` etc.): capa `position:absolute`, `rgba(224,49,49,0.55)`, `z-index:0` sota el nav (`z-index:1`). Atenuació: fosc 0,72→0,8; clar 0,9→0,94; `page_bg` 0,14→0,10.

---

## Sessió 2026-09-30 — SEO al CMS, autor per defecte, slug estable

- **Redirecció URL post Naya** (commit `e36dc4c8ba`): `aliases` afegit; causa = Sveltia buida el `slug` quan canvia el `title`.
- **`seoTitle`** (commit `3af5e5b920`): camp opcional als 19 reculls; si buit, usa `title` sense prefix de data. Plantilles: `seo-title.html`, `head.html` (sobreescrit), `opengraph.html`, `twitter_cards.html`, `schema_json.html`.
- **Autor per defecte** (commit `3af5e5b920`): hook `preSave` al CMS mapeja login GitHub → nom d'autor (`CMS_AUTHORS`). Cal afegir cada editor nou.
- **URLs estables** (commit `cfbd4d2c3b`): `slug` explícit als 4 posts que no en tenien; hook `preSave` omple `slug` dels articles nous.
- **Ajuda camp `slug`** (commit `0d473080fa`): etiqueta «Adreça web de l'article (no tocar)» amb avís.
- **Regressió `slug`** (commit `c1781d476d`): restaurat + alias; hook recupera `slug` si queda buit.
- **Bug CI**: `layouts/README.txt` contenia `<title>` → Hugo el parsejava com a plantilla. Corregit (`6cd5ee98e2`).

---

## Sessió 2026-09-30 (v2) — /admin/intern/: actes i tasques al repo privat (Fase 1)

- **El repo `112books/9bi` és públic**: `draft: true` no amaga res a GitHub. Per decisió de l'usuari, la documentació interna (`content/documentacio/`: acta del 10/09 i documents del concurs) s'ha **mogut** al repo **privat `112books/9bi-intern`** (commit `d478254`, carpetes `actes/` i `concurs/`) i s'ha esborrat del públic **sense reescriure l'historial** (hi continua visible a l'historial antic).
- **Gestor intern** `static/admin/intern/`: segon Sveltia (reutilitza `../sveltia-cms.js`) amb `backend.repo: 112books/9bi-intern`. Sessió compartida amb `/admin/` (mateix `localStorage`); el PAT classic `repo` ja hi serveix, un fine-grained ha d'incloure 9bi-intern. Els estils de `index.html` són **còpia** dels de `../index.html`.
  - `actes`: title, date, lloc, **assistents** (select múltiple de membres actius, llista `x-membres` a mà: el CMS no pot relacionar amb `data/membres/` d'un altre repo), `persones_reunides` (text lliure per a no-membres), convidat, ordre_del_dia, **acords** `{text, projecte}`, votacions, **tasques** `{id (uuid), text, responsable, termini, projecte, estat: pendent|en curs|feta|descartada}`, **visibilitat** `interna|publica` (per defecte interna), body.
  - `concurs`: igual que abans.
- **`/admin/intern/tasques.html`**: llegeix les actes per l'API de GitHub amb el token de la sessió (res es publica), agrega les tasques no tancades (l'acta **més recent** mana, per `id`; sense id, per text), filtres responsable/projecte (també `?responsable=&projecte=`) i botó **«Acta nova amb les tasques obertes»** (crea `actes/acta-YYYY-MM-DD-reunio.md` amb les tasques obertes i els seus id). `js-yaml` 4.1.0 (MIT) autoallotjat.
- Decisió: les tasques **no** surten a la pàgina pública dels projectes (només a l'admin).
- Verificat: build net; prova amb navegador i API simulada (filtres, fusió per id, termini vençut, creació d'acta, acta ja existent, 375 px sense desbordament); Sveltia accepta el config intern.
- **Pendent**: Fase 2 (projectes públics: 13-B i «retrat gegant col·lectiu»).

---

## Sessió 2026-10-01 — Admin intern publicat i Projectes (Fase 2)

- **Fase 1 publicada**: PR #11 fusionada (`5035f5c`). Conflicte previ al `CLAUDE.md` (reduït a `main`) resolt; la nota de sessió de la Fase 1 és a la secció de sobre. Decisions confirmades per l'usuari: estats de tasca `pendent / en curs / feta / descartada`; nom de les actes noves `acta-AAAA-MM-DD-reunio`.
- **Projectes (Fase 2, `dc193fe`)**, decisions de l'usuari: sessions com a **llista dins del projecte**; accés des del **peu** (columna «El web»), no del menú principal; estats de sessió `prevista / feta / anul·lada`; 13-B **aturat**, responsable **Joan Linux**; l'Antonio Silva es cita com «Antonio Silva, de l'Arxiu de Roquetes» **sense enllaç** (l'Arxiu va demanar poc protagonisme el 28/09).
  - 13-B: 3 sessions extretes dels posts (`2016-10-16` primera ruta amb l'Antonio Silva; `2016-10-23` ruta oberta, plaça Virrei Amat 10 h, estat desconegut; `2017-04-02` «04 – Roquetas», data = data del post). Les rutes 02 i 03 no consten al blog. El post del 16/10/2016 no porta l'etiqueta `13-B`, per això el mosaic en mostra 2.
  - Retrat gegant col·lectiu per barri: estat `idea`, sense dades.
  - Plantilles `layouts/projectes/{list,single}.html`: fitxa, sessions (només columnes amb dades; desplaçament horitzontal al mòbil amb `.projecte-taula`) i mosaic dels articles de l'etiqueta. Les tasques **no** surten.
- Verificat: build net, navegador a 1280 i 375 px sense desbordament, Sveltia accepta el config (31 col·leccions).

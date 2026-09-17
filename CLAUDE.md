# CLAUDE.md — 9 Barris Imatge

Documentació per a sessions de Claude. Només fets verificats dels fitxers del projecte.

## REGLA PRIMERA (obligatòria)

- **No implementar mai res pel meu compte.** Ni contingut, ni textos, ni disseny, ni enllaços, ni estructures noves. Els suggeriments són benvinguts, però **cal presentar-los i esperar una aprovació explícita de l'usuari abans de tocar cap fitxer.**
- **No inventar fets** (dates, dades, textos, noms) ni afegir frases "de farciment" no demanades.
- **No canviar el disseny** (colors, bandes, marges, tipografia, ordre, components) sense aprovació explícita, tant per fer canvis nous com per revertir els existents.
- Si quelcom és ambigu, **preguntar**; no assumir ni improvisar.
- El rigor per sobre de la velocitat: verificar sempre a `content/` i `layouts/` abans de donar per fet què hi ha.

## Protocol d'inici de sessió (obligatori)

A l'inici de **cada** sessió (OpenCode, Claude o la que sigui), abans de treballar:

1. **Sincronitzar els repositoris**: `git fetch origin` i comprovar que `main` (i la branca `pages`) estiguin al dia.
2. **Iniciar la gestió d'hores**: activar/enregistrar el temps de la sessió (skill `time-tracker`, `.taques/`).
3. **Recompte del web**: usuaris (GoatCounter), nombre de posts i números del web (posts · anys · membres).

## El projecte

Lloc web estàtic de l'Associació fotogràfica 9 Barris Imatge (Barcelona), migrat de Blogger a Hugo + PaperMod, hostatjat a Codeberg Pages.

## Estat real (verificat el 2026-09-17)

- Repo local: branca `main`, primer commit `feb0ba8` pujat a **Codeberg `linuxbcn/9bi`** (SSH `ssh://git@codeberg.org/linuxbcn/9bi.git`).
- **Forgejo Actions NO actives** al repo (`has_actions: false`): el workflow de deploy encara no s'ha executat; el lloc viu no existeix.
- Web en desenvolupament: `https://linuxbcn.codeberg.page/9bi/` (Codeberg Pages de projecte). Quan el domini estigui connectat, revertir `baseURL` i el `site` del workflow a `9barrisimatge.org`.
- Tema PaperMod vendored a `themes/PaperMod/`.

## Comandes

- Servei local: `hugo server -D` → http://localhost:1313
- Build: `hugo --minify` → `public/`
- Migració Blogger (requereix `.venv-migracio` amb `markdownify` + `pyyaml`):
  `source .venv-migracio/bin/activate && python3 scripts/migrate_blogger.py --input exports/blog-EXPORT.xml`
- Més visitats: `python3 scripts/goatcounter_popular.py --days 30` (requereix `GOATCOUNTER_API_KEY`, usa `requests`)

## Versions (verificades)

- Hugo **0.164.0 extended** (fixada a `.forgejo/workflows/deploy.yml`)
- Decap CMS **^3.0.0** (càrrega via unpkg a `static/admin/index.html`)

## Configuració actual (`hugo.toml`)

- `baseURL` **https://linuxbcn.codeberg.page/9bi/** (FASE DESENVOLUPAMENT; revertir a https://9barrisimatge.org/ quan el domini apunti al Codeberg) · title "9 Barris Imatge" · `locale ca` · `timeZone Europe/Madrid` · `enableRobotsTXT = true`
- `uglyURLs = true` (preserva les URL `.html` de Blogger)
- `[permalinks] posts = "/:year/:month/:slug"`
- `[markup.goldmark.renderer] unsafe = true` i `[markup.goldmark.parser.attribute] block = true`
- Taxonomies: `tag` → `tags`, `category` → `categories`, `author` → `author` · `paginate = 24`
- `params`: `defaultTheme = "dark"`, description, ShowPostAuthors=true, ShowBreadCrumbs=false, ShowReadingTime=false, ShowShareButtons=false, ShowPostNavLinks=true, ShowCodeCopyButtons=true, ShowWordCount=false, comments=false; `homeInfoParams` (Title + Content)
- `menu.main`: Inici(/), Arxiu(/archive/), Qui som(/qui-som/), El Concurs(/concurs/), Contacte(/contacte/) — **la Guia NO hi és** (és interna, s'accedeix des del CMS); **falta Cerca** (pendent, abans de Contacte)
- `menu.footer`: Arxiu(/archive/), Etiquetes(/tags/), Més visitats(/mes-visitats/), Estadístiques(goatcounter), Cerca(/search/), RSS(/index.xml)

## Estructura de fitxers (verificada)

```
content/
├── posts/                         # 3.006 posts migrats de Blogger
├── qui-som.md, concurs.md, contacte.md, privacitat.md, avis-legal.md, cookies.md, credits.md   # pàgines estàtiques (amb `url` explícita)
├── search.md (layout "search"), archive.md (layout "archives")
├── mes-visitats.md (layout "popular" + hiddenInRss: true)
├── guia/                          # _index.md + 6 subpàgines — TOTES amb `draft: true`
└── documentacio/                  # interna (draft): actes/ (acta 2026-09-10) + concurs/
layouts/
├── baseof.html                    # SOBREESCRIT: clau de caché del footer amb la condició de «números»
├── index.html                     # portada en mosaic (grid de fotos, paginat)
├── archives.html                  # arxiu + índex d'anys a la dreta (rail)
├── author/term.html               # pàgina de posts per autor (mosaic paginat)
├── _shortcodes/membres.html       # taula de membres (ordenada per nº de posts)
├── _default/popular.html          # llista de més visitats (llegeix data/popular.json)
└── _partials/
    ├── footer.html                # SOBREESCRIT: bloc «9 Barris en números» + count-up
    ├── extend_head.html           # GoatCounter → 9barrisimatge.goatcounter.com
    ├── extend_footer.html         # menú footer + fila legal (Avís legal · Privacitat · Cookies · Crèdits) + "Powered by LinuxBCN" (→ linuxbcn.com)
    └── extend_post_content.html   # botó "Veure tot l'àlbum de fotos" (si album_url)
assets/css/extended/custom.css     # estils: mosaic, botó àlbum, footer-nav, powered-by, formulari, membres, footer-stats
static/admin/{config.yml,index.html}  # Decap CMS
static/images/                     # imatges (media_folder del CMS)
scripts/{migrate_blogger.py,migrate_live.py,goatcounter_popular.py}
data/{popular.json,membres.yml}    # top visites (exemple) + membres (CMS)
.forgejo/workflows/deploy.yml      # CI/CD
archetypes/default.md              # front matter per defecte
sync-9bi.sh                        # script de sync/gestió
```

## Front matter (convencions reals)

- **Posts**: `title`, `date` (ISO), `author`, `slug`, `tags` (llista), `cover.image` (opcional), `album_url` (opcional), `description` (opcional)
- **Pàgines**: `title`, `description`, `url` (ruta final explícita)
- **Guia i documentació**: `draft: true` (internes, només des del CMS; no surten a `public/`)
- **search.md**: `layout: "search"` · **archive.md**: `layout: "archives"` · **mes-visitats.md**: `layout: "popular"` + `hiddenInRss: true`

## Decap CMS (`static/admin/config.yml`)

- Backend `forgejo`: repo `linuxbcn/9bi`, `branch main`, `api_root` https://codeberg.org/api/v1
- `media_folder: static/images` · `public_folder: /images`
- 4 col·leccions: `posts` (title, date, author[select amb els 9 membres reals], cover.image, album_url, tags, description, body), `guia`, `actes` (title, date, lloc, persones_reunides, convidat, ordre_del_dia, draft, body) i `concurs` (title, tipo[select], date, draft, body)

## CI/CD (`.forgejo/workflows/deploy.yml`)

- Trigger: **push a `main`** + `workflow_dispatch`
- Steps: checkout → Hugo 0.164.0 extended (`hugo --minify --environment staging`) → deploy a Codeberg Pages (`https://codeberg.org/git-pages/action@v2` amb `token: ${{ forge.token }}` i `server: codeberg.page`)
- `site: https://linuxbcn.codeberg.page/9bi/` (FASE DESENVOLUPAMENT; revertir a https://9barrisimatge.org/ quan el domini apunti)
- **PERÒ DIA 2026-09-17**: Codeberg ja NO ofereix l'antic pages server als usuaris nous i els runners gestionats no estan disponibles (`/actions/approval` → 404). El workflow queda en "Waiting for a runner". El desplegament real es fa **sense Actions**:
  1. Build local: `hugo --minify --environment staging --destination /tmp/pages-deploy`
  2. Push a la branca `pages`: `cd /tmp/pages-deploy && git init -q -b pages && git add -A && git commit -qm x && git push -f ssh://git@codeberg.org/linuxbcn/9bi.git HEAD:pages`
  3. **Webhook configurat al repo** (Settings → Webhooks → Forgejo, Target `https://linuxbcn.codeberg.page/9bi/`, Branch filter `pages`) — és el que publica el lloc (sense ell, 400).
- Nota: en el workflow hi ha un pas comentat per refrescar `data/popular.json` amb GoatCounter (secret `GOATCOUNTER_API_KEY`)

## Problemes coneguts / pendents (verificats)

1. **Forgejo Actions activades al repo** però **sense runner disponible** (Codeberg no dona els runners gestionats a usuaris nous: `/actions/approval` → 404). El deploy es fa manualment via branca `pages` + webhook; el workflow no s'ha executat.
2. `static/admin/config.yml` té `app_id: SUBSTITUEIX-CI-AMB-EL-CLIENT-ID` (placeholder). Pendent: Client ID de l'OAuth2 de Codeberg.
3. `extend_head.html` apunta a `9barrisimatge.goatcounter.com`: cal crear el lloc al GoatCounter.

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
- **Peu legal**: fila nova `.footer-legal` (**Avís legal · Privacitat · Cookies**) sota el menú del peu; `content/avis-legal.md` i `content/cookies.md` nous (esquelet amb `[PENDENT]`). Espai sota «Powered» (`.powered-by` → `margin-bottom: 1.2rem`).
- **`content/qui-som.md`**: «FaVB» → «**FAVB**» a «Links amics».

## Tasques pendents (backlog curt)

- **`content/contacte.md`**: afegir al formulari un camp nou "A quina entitat de Nou Barris pertanys o representes (opcionalment)" (input opcional, com `assumpte`).
- **`content/privacitat.md`**: omplir els `[PENDENT: ...]` amb el **NIF** i l'**adreça** reals de l'associació; sense això la política no és vàlida. (El correu ja hi és: info@9barrisimatge.org.)
- **Peu legal**: fila legal creada (Avís legal · Privacitat · Cookies · Crèdits). Pendent: contingut real d'`avis-legal.md`, `cookies.md` i completar `privacitat.md` (NIF/adreça); resta d'adequació RGPD.
- **Auditoria de seguretat** (encarregada 2026-09-17, pendent).
- **Auditoria d'accessibilitat** (encarregada 2026-09-17, pendent).
- **`content/qui-som.md`** (secció «Membres»): **implementat (2026-09-18)** amb `{{< membres >}}` + `data/membres.yml` + `layouts/author/term.html` + col·lecció Decap «membres» (vegeu la sessió 2026-09-18). Pendent: enllaç de reserva al **perfil del bloc vell** («Els components de 9 barris imatge») per als membres sense web (ara mostren «—») i completar els **Instagram** que falten.
- **Comentaris al web**: implementar un sistema de comentaris amb **fort control d'spam** (pendent d'escollir la solució/proveïdor).
- **Compartir a xarxes**: botons per compartir fàcilment a **Instagram** i les xarxes que es portin ara (pendent).
- **Tipografies**: cos **Montserrat** + títols **Gillius ADF** (combinació triada per l'usuari; feta només la vista prèvia a `/tmp/font-preview`). Pendent d'instal·lar autoallotjades (`static/fonts/` + `@font-face`, `font-display: swap`, preload) i aplicar-les a `custom.css`. **Res de Google Fonts CDN** (RGPD). Gillius ADF és GPL+excepció de font.
- **Capçalera sticky amb icones**: en fer scroll, transformar el menú de navegació en icones. **Falta afegir «Cerca» abans de «Contacte»** al menú principal.

## Infraestructura i comunicació (pendent)

- **Butlletí**: cal tenir un butlletí (newsletter) per a l'associació.
- **DNS i correu**: repensar què fer amb els DNS; es vol **correu gratuït i lliure per a cada membre** i un de **genèric** de l'entitat.
- **Grup de correu**: llista/grup per enviar un correu a tots els membres.
- **Telegram**: grup **privat** i **públic** (aquest darrer unidireccional, on s'envien els posts quan es publiquen).
- **Facebook**: publicar automàticament els posts.

## Properes sessions

- **Muntar el CMS**: OAuth2 de Codeberg (Client ID real), usuaris i permisos.
- **Control de fitxers del Concurs Cordoncillo** (bases, històric, etc.).
- **Secció per fer i gestionar les reunions** de l'associació.

## Decisions pendents per a la migració real (2026-09-17)

- **Etiquetes**: al blog original són molt incompletes (moltes entrades sense tag o amb tags inconsistents). No fer còpia cega amb `migrate_blogger.py` — caldrà revisar/curar les etiquetes, no assumir que el que hi ha al Blogger és la taxonomia final.
- **Autors**: es crearan comptes reals a Codeberg per a cada membre amb el seu correu actual (el que consta ara — no l'email públic del feed de Blogger, que Google no exposa). El camp `author` de cada post migrat s'haurà de fer correspondre als 9 membres reals de `static/admin/config.yml` (select), no deixar el nom lliure que ve de Blogger.

## El que encara no existeix (per no assumir)

- Migració de Blogger: **feta** (3.006/3.006 posts a `content/posts/`). Pendent: curar etiquetes i autors. No cal l'export XML oficial: `scripts/migrate_live.py` llegeix el feed Atom en directe.
- OAuth2 Application creada ni Client ID.
- Lloc GoatCounter creat ni API key.
- Confirmació que `info@9barrisimatge.org` rep correus (FormSubmit).
- DNS / CNAME cap a Codeberg Pages (el lloc de producció serà 9barrisimatge.org).
- Pàgina de privacitat creada (`/privacitat/`) però **amb placeholders de NIF/adreça pendents**; falta l'avís legal i la resta d'adequació RGPD (cookies, etc.).
- Configuració SEO/IA per a tot el web (metadades, dades estructurades, etc.).
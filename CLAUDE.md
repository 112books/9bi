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
- `menu.main`: Inici(/), Arxiu(/archive/), Qui som(/qui-som/), El Concurs(/concurs/), **Cerca(/search/)**, Contacte(/contacte/) — **la Guia NO hi és** (és interna, s'accedeix des del CMS)
- `menu.footer` (columnes «El web» del peu): **Arxiu 9bi**(/archive/), **Etiquetes / Tags**(/tags/), Més visitats(/mes-visitats/), **Estadístiques del web**(goatcounter), Cerca(/search/), RSS(/index.xml)

## Estructura de fitxers (verificada)

```
content/
├── posts/YYYY/                     # 3.006 posts migrats de Blogger, en subcarpetes per any (2008…2026); les URL no depenen del path (permalinks `/:year/:month/:slug` del front matter)
├── qui-som.md, concurs.md, contacte.md, privacitat.md, avis-legal.md, cookies.md, credits.md   # pàgines estàtiques (amb `url` explícita)
├── subvencions.md                 # pàgina filla de «Qui som» (`url: /qui-som/subvencions/`, amb alias de l'antic URL del post)
├── search.md (layout "search"), archive.md (layout "archives")
├── mes-visitats.md (layout "popular" + hiddenInRss: true)
├── guia/                          # _index.md + 6 subpàgines — TOTES amb `draft: true`
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
    ├── extend_head.html           # preload de fonts + GoatCounter → 9barrisimatge.goatcounter.com
    ├── extend_footer.html         # BUIT (el contingut del peu s'ha mogut a footer.html)
    └── extend_post_content.html   # botó "Veure tot l'àlbum de fotos" (si album_url)
assets/css/extended/custom.css     # estils: mosaic, botó àlbum, tipografies (@font-face), peu (footer-band/-cols/-bottom), formulari, membres, footer-stats
static/admin/{config.yml,index.html}  # Decap CMS
static/images/                     # imatges (media_folder del CMS)
scripts/{migrate_blogger.py,migrate_live.py,goatcounter_popular.py}
data/popular.json                    # top visites (exemple)
data/membres/                        # un fitxer per membre (autor, nom, malnom, web, instagram, actiu)
.forgejo/workflows/deploy.yml      # CI/CD
archetypes/default.md              # front matter per defecte
sync-9bi.sh                        # script de sync/gestió
```

## Front matter (convencions reals)

- **Posts**: `title`, `date` (ISO), `year` (any, afegit 2026-09-18 per al filtratge del CMS), `author`, `slug`, `tags` (llista), `cover.image` (opcional), `album_url` (opcional), `description` (opcional)
- **Pàgines**: `title`, `description`, `url` (ruta final explícita)
- **Guia i documentació**: `draft: true` (internes, només des del CMS; no surten a `public/`)
- **search.md**: `layout: "search"` · **archive.md**: `layout: "archives"` · **mes-visitats.md**: `layout: "popular"` + `hiddenInRss: true`

## Decap CMS (`static/admin/config.yml`)

- Backend `forgejo`: repo `linuxbcn/9bi`, `branch main`, `api_root` https://codeberg.org/api/v1
- `media_folder: static/images` · `public_folder: /images`
- 23 col·leccions: 19 d'articles per any (`posts-2026`…`posts-2008`, una per subcarpeta `content/posts/YYYY/` amb `sortable_fields` per data desc; camps: title, date, year [hidden, default l'any], slug, author [select], cover.image, album_url, tags, description, body), més `guia`, `actes` (title, date, lloc, persones_reunides, convidat, ordre_del_dia, draft, body), `concurs` (title, tipo[select], date, draft, body) i `membres` (vegeu "Sessió 2026-09-18 (v6)"). La llista d'autors es reutilitza amb un ancoratge YAML (`x-autors: &autors`).

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
2. `static/admin/config.yml` amb el Client ID real de l'OAuth2 de Codeberg (`app_id: 0c6b6c51-…`) — **fet i desplegat (2026-09-18, commit `dd36e51e`)**. Pendent: **usuari i permisos** dels col·laboradors (es treuran a membres inactius perquè no editin).
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

## Tasques pendents (backlog curt)

- **`content/contacte.md`**: afegir al formulari un camp nou "A quina entitat de Nou Barris pertanys o representes (opcionalment)" (input opcional, com `assumpte`).
- **`content/privacitat.md`**: **fet (2026-09-18)** — adreça real (Casal de Barri de Prosperitat) i **sense NIF** (l'associació no en té); sense placeholders. (El correu ja hi és: info@9barrisimatge.org.)
- **Peu / legal**: peu de **5 columnes** fet (logo · buida · «El web» · «Legal» · «9 Barris en números»). `avis-legal.md` i `privacitat.md` fets (2026-09-18). Pendent: contingut real d'`cookies.md` i la resta d'adequació RGPD.
- **Auditoria de seguretat** (encarregada 2026-09-17, pendent).
- **Enllaços d'àlbums trencats (Picasa Web → Google Photos)** (proposada 2026-09-18): quan Google va capturar/tanar Picasa Web, van quedar **llocs a enllaços d'àlbums morts a molts posts**. El camp `album_url` (extret per `migrate_live.py` del primer enllaç al voltant de la imatge) apunta a rels URLs de Picasa. Tasca fosca: **detectar quins `album_url` (i enllaços de Google Photos/Picasa dins dels posts) no funcionen** i **refer-los** o bé apuntar-los a l'àlbum equivalent de Google Photos si s'ha reconstruit. Nota de l'usuari: ell (Joan "Linux") va fixar els seus a mà, però **la resta d'autors no ho van fer** → cal revisar per autor. Estratègia proposada: revisar `content/posts/` per patrons `<a href="https://picasaweb.google.com/…">` (i variants) i valorar-ne la resposta HTTP, després decidir com refer-los (buscar a Google Photos pel títol/àlbum, o eliminar l'enllaç si no es recupera). Pot anar lligat al pipeline de votació/àlbums del Concurs.
- **Auditoria d'accessibilitat** (encarregada 2026-09-17, pendent).
- **Auditoria de SEO i IA** (encarregada 2026-09-18): deixar el web **ben preparat per a motors de cerca i agents d'IA** (metadades, dades estructurades, sitemap/robots, OpenGraph, etc.).
- **Document d'URLs de Blogger (SEO/redireccions)** (encarregat 2026-09-18): recull de **totes les URL actuals del blog Blogger** per comprovar que coincideixen amb les entrades actuals del web (l'estructura `/:year/:month/:slug.html` + `uglyURLs = true` ho preserva) o fer una **redirecció a la nova URL** — tema cercadors i SEO.
- **`content/qui-som.md`** (secció «Membres»): **implementat (2026-09-18)** amb `{{< membres >}}` + **`data/membres/<slug>.yml`** (carpeta, amb `nom`/`malnom`/`actiu`) + `layouts/author/term.html` + col·lecció Decap «membres» **folder** amb camp ACTIU (vegeu la sessió v6). Pendent: enllaç de reserva al **perfil del bloc vell** («Els components de 9 barris imatge») per als membres sense web (ara mostren «—»), completar els **Instagram** que falten i marcar les baixes com a `actiu: false` (+ treure l'accés d'escriptura a Codeberg).
- **Comentaris al web**: implementar un sistema de comentaris amb **fort control d'spam** (pendent d'escollir la solució/proveïdor).
- **Compartir a xarxes**: botons per compartir fàcilment a **Instagram** i les xarxes que es portin ara (pendent).
- **Tipografies**: **implementat (2026-09-18)** — cos **Montserrat** (woff2 400/700/800) + títols **Gillius ADF** (OTF 400/700), autoallotjades a `static/fonts/`, `@font-face` i overrides a `custom.css` (urls `../../fonts/…`) i `preload` a `extend_head.html`. **Sense cap CDN** (RGPD). Pendent opcional: convertir els OTF de Gillius a woff2.
- **Votació popular per QR** (concurs): **`modules/votacio/` (M1) fet i testejat (2026-09-19)** — app WSGI stdlib (0 deps en producció): `/v/<token>`, admin recompte/export/tancar, CSRF, rate-limit, geofencing off/soft/hard, i18n ca/es/en. **Decisions 2026-09-19**: geo **soft** (radi 500 m Casal Prospe), sense mòbil → **vot en paper** (`tally --paper`), `collect_data=none`, allotjament **Dinahosting compartit (Passenger)** primer (VPS Lite ~34 €/mes només si falla). **Pendent**: confirmar Python/Passenger al panell de Dinahosting → desplegar (1–15 des 2026, secrets reals, `ssl=1`); confirmar **AGPL-3.0** i repo `9bi-apps`. Vegeu la sessió 2026-09-19 (v1).

- **Pestanyes a «Qui som»** (aplicat 2026-09-18): **4 pestanyes fetes** — Qui som (Història) · Com funcionem (Reunions + Com funcionem + subvencions) · Membres (`{{< membres >}}`) · Relacions (entitats + links amics) — amb el patró CSS pur del Concurs (radios `name="qsb-view"`, classes `.qsb-*` a `custom.css`). **Pendent: 5a pestanya «Història de la fotografia a Nou Barris»** (contingut de la recerca, sessió separada).
- **Història de la fotografia a Nou Barris** (aprovat: incloure a la pestanya nova): genealogia ~1960–2026 amb 4 categories (A fotògrafs de Nou Barris · B que l'han documentat · C fotografia comunitària/de barri · D ecosistema Can Basté) i columna «per què és conegut?»; noms sense font es marquen «pendent de verificar».
- **Núvol d'etiquetes a la Cerca** (`/search/`): **implementat (2026-09-18)**. La **depuració d'etiquetes** ja està **aplicada** (sessió v6); pendent de decisions editorials: **anys** com a tag i els **115 articles sense tag**.
- **Responsive header**: **fix fet i desplegat (2026-09-18)** — mides base de `.menu-icon`/`.menu-icon svg` fora del media query; icones a 17 px al mòbil.
- **Footer «amb lògica»**: **implementat (2026-09-18)** — amplada igual a la del header (`--nav-width`) arreu; versió de telèfon: **Logo + «El web»** · **«Legal»** amb tots els links en una sola línia · **«9 Barris en números»** amb totes les dades en una sola línia.
- **Concurs Cordoncillo (investigació pròpia)**: biografia de Cordoncillo, origen documentat (1990), cronologia i 35 anys de guanyadors; incidències de numeració a l'arxiu.

## Infraestructura i comunicació (pendent)

- **Butlletí**: cal tenir un butlletí (newsletter) per a l'associació.
- **DNS i correu**: repensar què fer amb els DNS; es vol **correu gratuït i lliure per a cada membre** i un de **genèric** de l'entitat.
- **Grup de correu**: llista/grup per enviar un correu a tots els membres.
- **Telegram**: grup **privat** i **públic** (aquest darrer unidireccional, on s'envien els posts quan es publiquen). **Tasca (2026-09-18)**: muntar un **bot** (token de @BotFather), afegir-lo al grup, obtenir el `chat_id` i crear `scripts/telegram.py` que enviï missatges llegint `TELEGRAM_BOT_TOKEN` i `TELEGRAM_CHAT_ID` de l'entorn (mai al repo).
- **Xarxes socials (Instagram i Facebook)** (2026-09-18): posar links a l'**Instagram** i al **Grup de Facebook** al web, i dissenyar una **eina automàtica** perquè cada post nou es publiqui automàticament a IG i FB (mateix patró que el bot de Telegram pendent).

## Properes sessions

- **Muntar el CMS**: OAuth2 de Codeberg **fet** (Client ID `0c6b6c51-…`, desplegat). **Articles per anys fet (v7/v8)**: camp `year`, primer com a col·leccions filtrades i, en veure que filtraven llistant tot igualment, **posts movent-se a subcarpetes físiques per any** (carpeta per any al config, `sortable_fields` desc) + **rail propi** substituint la sidebar de Decap. **Chrome del CMS fet (v7)**: header amb logo + «9 Barris Imatge - Gestor de continguts» + enllaços a la Guia, footer del web replicat. Pendent: **usuaris i permisos** dels col·laboradors (membres actius amb escriptura; inactius sense) i la resta de demandes del llistat (miniatures, títols en majúscules, normalitzar títols...).
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
- Suport Python/Passenger al panell de Dinahosting sense confirmar (per al desplegament de `modules/votacio/`).
# CLAUDE.md — 9 Barris Imatge

Documentació per a sessions de Claude. Només fets verificats dels fitxers del projecte.

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
- Taxonomies: `tag` → `tags`, `category` → `categories` · `paginate = 24`
- `params`: description, ShowPostAuthors=true, ShowBreadCrumbs=false, ShowReadingTime=false, ShowShareButtons=false, ShowPostNavLinks=true, ShowCodeCopyButtons=true, ShowWordCount=false, comments=false; `homeInfoParams` (Title + Content)
- `menu.main`: Inici(/), Articles(/posts/), Qui som(/qui-som/), Concurs J. A. Cordoncillo(/concurs/), Contacte(/contacte/) — **la Guia NO hi és** (és interna, s'accedeix des del CMS)
- `menu.footer`: Articles, Etiquetes(/tags/), Arxiu(/archive/), Més visitats(/mes-visitats/), Cerca(/search/), RSS(/index.xml)

## Estructura de fitxers (verificada)

```
content/
├── posts/                         # 2 posts de prova migrats
├── qui-som.md, concurs.md, contacte.md   # pàgines estàtiques (amb `url` explícita)
├── search.md (layout "search"), archive.md (layout "archives")
├── mes-visitats.md (layout "popular" + hiddenInRss: true)
├── guia/                          # _index.md + 6 subpàgines — TOTES amb `draft: true`
└── documentacio/                  # interna (draft): actes/ (acta 2026-09-10) + concurs/
layouts/
├── index.html                     # portada en mosaic (grid de fotos, paginat)
├── _default/popular.html          # llista de més visitats (llegeix data/popular.json)
└── _partials/
    ├── extend_head.html           # GoatCounter → 9barrisimatge.goatcounter.com
    ├── extend_footer.html         # menú footer + "Powered by LinuxBCN" (→ linuxbcn.com)
    └── extend_post_content.html   # botó "Veure tot l'àlbum de fotos" (si album_url)
assets/css/extended/custom.css     # estils: mosaic, botó àlbum, footer-nav, powered-by, formulari, etc.
static/admin/{config.yml,index.html}  # Decap CMS
scripts/{migrate_blogger.py,goatcounter_popular.py}
data/popular.json                  # top visites (exemple)
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
- **Encara sense fer**: commit/push/deploy d'aquests 3.006 fitxers — pendent de revisió de l'usuari al servidor local abans de pujar-ho.

## Tasques pendents (backlog curt)

- **`content/contacte.md`**: afegir al formulari un camp nou "A quina entitat de Nou Barris pertanys o representes (opcionalment)" (input opcional, com `assumpte`).
- **`content/contacte.md`**: treure la línia final "També pots escriure'ns directament a info@9barrisimatge.org." — motiu: exposar l'email fa que la gent contacti pesadament fora del formulari.
- **Auditoria de seguretat** (encarregada 2026-09-17, pendent).
- **Auditoria d'accessibilitat** (encarregada 2026-09-17, pendent).
- **`content/qui-som.md`**: llistat de membres ordenat pel nombre de posts, amb enllaç "Publicacions" (decidit: taxonomia `authors` + shortcode), web personal i Instagram opcionals. Roster decidit: tots els autors amb posts excepte "9 Barris Imatge" (12). Pendent d'implementar.

## Properes sessions

- **Muntar el CMS**: OAuth2 de Codeberg (Client ID real), usuaris i permisos.
- **Control de fitxers del Concurs Cordoncillo** (bases, històric, etc.).
- **Secció per fer i gestionar les reunions** de l'associació.

## Decisions pendents per a la migració real (2026-09-17)

- **Etiquetes**: al blog original són molt incompletes (moltes entrades sense tag o amb tags inconsistents). No fer còpia cega amb `migrate_blogger.py` — caldrà revisar/curar les etiquetes, no assumir que el que hi ha al Blogger és la taxonomia final.
- **Autors**: es crearan comptes reals a Codeberg per a cada membre amb el seu correu actual (el que consta ara — no l'email públic del feed de Blogger, que Google no exposa). El camp `author` de cada post migrat s'haurà de fer correspondre als 9 membres reals de `static/admin/config.yml` (select), no deixar el nom lliure que ve de Blogger.

## El que encara no existeix (per no assumir)

- Migració real de Blogger: només 2 posts de prova migrats, dels 3.006 reals. `markdownify`+`pyyaml` ja instal·lats a `.venv-migracio` (verificat), falta l'export XML oficial del blog real.
- OAuth2 Application creada ni Client ID.
- Lloc GoatCounter creat ni API key.
- Confirmació que `info@9barrisimatge.org` rep correus (FormSubmit).
- DNS / CNAME cap a Codeberg Pages (el lloc de producció serà 9barrisimatge.org).
- Pàgines legals (privacitat, avís legal) i adequació RGPD.
- Configuració SEO/IA per a tot el web (metadades, dades estructurades, etc.).
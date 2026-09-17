# CLAUDE.md — 9 Barris Imatge

Documentació per a sessions de Claude. Només fets verificats dels fitxers del projecte.

## El projecte

Lloc web estàtic de l'Associació fotogràfica 9 Barris Imatge (Barcelona), migrat de Blogger a Hugo + PaperMod, hostatjat a Codeberg Pages.

## Estat real (verificat el 2026-09-17)

- Repo git local, branch `master`, **sense cap commit encara**.
- Res pujat a Codeberg; tot el codi és a l'àrea de treball.
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

- `baseURL` https://9barrisimatge.org · title "9 Barris Imatge" · `locale ca` · `timeZone Europe/Madrid`
- `uglyURLs = true` (preserva les URL `.html` de Blogger)
- `[permalinks] posts = "/:year/:month/:slug"`
- `[markup.goldmark.renderer] unsafe = true`
- Taxonomies: `tag` → `tags`, `category` → `categories` · `paginate = 24`
- `params`: description, ShowPostAuthors=true, ShowBreadCrumbs=false, ShowReadingTime=false, ShowShareButtons=false, ShowPostNavLinks=true, ShowCodeCopyButtons=true, ShowWordCount=false, comments=false; `homeInfoParams` (Title + Content)
- `menu.main`: Inici(/), Articles(/posts/), Qui som(/qui-som/), Concurs J. A. Cordoncillo(/concurs/), Contacte(/contacte/), Guia(/guia/)
- `menu.footer`: Articles, Etiquetes(/tags/), Arxiu(/archive/), Més visitats(/mes-visitats/), Cerca(/search/), RSS(/index.xml)

## Estructura de fitxers (verificada)

```
content/
├── posts/                         # 2 posts de prova migrats
├── qui-som.md, concurs.md, contacte.md   # pàgines estàtiques (amb `url` explícita)
├── search.md (layout "search"), archive.md (layout "archives")
├── mes-visitats.md (layout "popular" + hiddenInRss: true)
└── guia/                          # _index.md + 6 subpàgines
layouts/
├── index.html                     # portada en mosaic (grid de fotos, paginat)
├── _default/popular.html          # llista de més visitats (llegeix data/popular.json)
└── _partials/
    ├── extend_head.html           # GoatCounter → 9barrisimatge.goatcounter.com
    ├── extend_footer.html         # menú footer
    └── extend_post_content.html   # botó "Veure tot l'àlbum de fotos" (si album_url)
assets/css/extended/custom.css     # estils: mosaic, botó àlbum, footer-nav, formulari, etc.
static/admin/{config.yml,index.html}  # Decap CMS
scripts/{migrate_blogger.py,goatcounter_popular.py}
data/popular.json                  # top visites (exemple)
.forgejo/workflows/deploy.yml      # CI/CD
archetypes/default.md              # front matter per defecte
```

## Front matter (convencions reals)

- **Posts**: `title`, `date` (ISO), `author`, `slug`, `tags` (llista), `cover.image` (opcional), `album_url` (opcional), `description` (opcional)
- **Pàgines**: `title`, `description`, `url` (ruta final explícita)
- **search.md**: `layout: "search"` · **archive.md**: `layout: "archives"` · **mes-visitats.md**: `layout: "popular"` + `hiddenInRss: true`

## Decap CMS (`static/admin/config.yml`)

- Backend `forgejo`: repo `linuxbcn/9bi`, `branch main`, `api_root` https://codeberg.org/api/v1
- `media_folder: static/images` · `public_folder: /images`
- Una col·lecció: `posts` (camps: title, date, author[select], cover.image, album_url, tags, description, body)

## CI/CD (`.forgejo/workflows/deploy.yml`)

- Trigger: **push a `main`** + `workflow_dispatch`
- Steps: checkout → Hugo 0.164.0 extended (`hugo --minify`) → deploy a Codeberg Pages (action `git-pages/action@v2`, site https://9barrisimatge.org)
- Nota: hi ha un pas comentat per refrescar `data/popular.json` amb GoatCounter (secret `GOATCOUNTER_API_KEY`)

## Problemes coneguts / pendents (verificats)

1. `static/admin/config.yml` té `app_id: SUBSTITUEIX-CI-AMB-EL-CLIENT-ID` (placeholder). Pendent: Client ID de l'OAuth2 de Codeberg.
2. `extend_head.html` apunta a `9barrisimatge.goatcounter.com`: cal crear el lloc al GoatCounter.
3. Repo remot i push pendents; no s'ha creat el repositori a Codeberg.

## El que encara no existeix (per no assumir)

- Migració real de Blogger (només 2 posts de prova; `markdownify` no està instal·lat al Python del sistema).
- OAuth2 Application creada ni Client ID.
- Lloc GoatCounter creat ni API key.
- Confirmació que `contacte@9barrisimatge.org` rep correus (FormSubmit).
- DNS / CNAME cap a Codeberg Pages.
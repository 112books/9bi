# 9 Barris Imatge

Llocs web de l'**Associació fotogràfica 9 Barris Imatge** de Barcelona, migrat de Blogger a un lloc estàtic 100% lliure.

Cada membre del col·lectiu publica un article amb una fotografia principal, l'enllaç a l'àlbum de fotos (Google Photos o similar) i un text que contextualitza les imatges.

## Stack

| Component | Tecnologia | Cost |
|---|---|---|
| Generador de llocs estàtics | **Hugo** (extended) | 0 € |
| Repositori de codi | **Codeberg** (Forgejo) | 0 € |
| Hosting estàtic + domini | **Codeberg Pages** | 0 € |
| CMS pels editors | **Decap CMS** (backend Forgejo) | 0 € |
| CI/CD | **Forgejo Actions** | 0 € |
| Estadístiques | **GoatCounter** | 0 € (<2.000 pàgines/mes) |

## Estructura de directoris

```
.
├── hugo.toml                    # Configuració de Hugo
├── content/
│   ├── posts/                   # Articles (un fitxer Markdown per article)
│   ├── search.md                # Pàgina de cerca
│   ├── archive.md               # Arxiu històric
│   └── mes-visitats.md          # Articles més visitats
├── layouts/
│   ├── _partials/
│   │   ├── extend_head.html     # Snippet de GoatCounter
│   │   └── extend_post_content.html  # Botó "Veure tot l'àlbum"
│   └── _default/popular.html    # Layout de la pàgina d'estadístiques
├── static/
│   ├── admin/                   # Decap CMS (config.yml + index.html)
│   └── images/                  # Imatges pujades pels editors
├── data/popular.json            # Top d'articles (generable via script)
├── scripts/
│   ├── migrate_blogger.py       # Migració Blogger XML → Markdown
│   └── goatcounter_popular.py   # Genera data/popular.json des de l'API
└── .forgejo/workflows/deploy.yml  # CI/CD a Codeberg Pages
```

## Desenvolupament local

```bash
hugo server -D
# → http://localhost:1313
```

Build de producció:

```bash
hugo --minify
# → public/
```

## Publicació a Codeberg

1. Creeu el repositori a Codeberg (p. ex. `9barrisimatge`) i afegiu-lo com a `origin`.
2. Activeu **Forgejo Actions** al repositori (cal demanar accés al CI de Codeberg si teniu un compte nou).
3. Feu push a `main`. El workflow `.forgejo/workflows/deploy.yml` construeix Hugo i publica a Codeberg Pages.
4. Domini personalitzat: afegiu al DNS un CNAME de `9barrisimatge.org` a `linuxbcn.codeberg.page` (o el que indiqui Codeberg Pages) i configureu el domini des de **Codeberg → Repo → Settings → Pages**.

> El deploy amb domini propi fa servir `server: codeberg.page`, que resol el bucle de certificat TLS (documentat per Codeberg).

## Decap CMS (editors)

1. A Codeberg: **Settings → Applications → Create new OAuth2 Application**.
   - Nom: `9barrisimatge CMS`
   - Redirect URI: `https://9barrisimatge.org/admin/`
   - Desmarcar "Confidential client"
2. Copieu el **Client ID** a `static/admin/config.yml` (camp `app_id`).
3. L'editor entra a **https://9barrisimatge.org/admin/**, fa login amb el seu compte Codeberg i publica.

### Rols
- **Admin**: accés total al repositori i al CMS; gestiona usuaris, theme i configuració.
- **Editor**: crea i edita els seus propis articles (títol, foto, àlbum, tags, text). Cal que tingui accés *push* al repositori; l'admin el convida des de Codeberg → Repo → Settings → Collaborators.

## Migració des de Blogger

1. Blogger → **Settings → Other → Back up content** (descarrega un XML).
2. Deseu el XML a `exports/`.
3. Executeu la migració:

```bash
python3 -m venv .venv-migracio
source .venv-migracio/bin/activate
pip install markdownify pyyaml

python3 scripts/migrate_blogger.py --input exports/blog-EXPORT.xml
# (opcional) --download-images per baixar les fotos a static/images/posts/
```

Genera un fitxer per article a `content/posts/` amb front matter (títol, data, autor, tags, slug, `cover.image`, `album_url`) i el cos en Markdown. Les URL es conserven (`/2026/07/slug.html`).

> Si voleu que la llista de més visitats es refresqui sola amb cada deploy, descomenteu al workflow les passes que criden `goatcounter_popular.py` i afegiu el secret `GOATCOUNTER_API_KEY` a Codeberg → Repo → Settings → Actions → Secrets.

## Estadístiques (GoatCounter)

1. Creeu un lloc nou a **GoatCounter** amb nom `9barrisimatge` (o ajusteu el subdomini a `layouts/_partials/extend_head.html`).
2. El contador s'envia automàticament a cada pàgina.
3. Per refrescar els articles més visitats:

```bash
export GOATCOUNTER_API_KEY="..."   # GoatCounter → Settings → API keys
python3 scripts/goatcounter_popular.py --days 30
hugo
```

## Enllaços útils

- Repositori: `ssh://git@codeberg.org/linuxbcn/9bi.git`
- CMS: `https://9barrisimatge.org/admin/`
- RSS: `https://9barrisimatge.org/index.xml`
- Cerca: `https://9barrisimatge.org/search/`
- Arxiu: `https://9barrisimatge.org/archive/`
# 9 Barris Imatge

Web del **Col·lectiu 9 Barris Imatge** de Barcelona, migrat de Blogger a un lloc estàtic construït amb Hugo i publicat a GitHub Pages.

Cada membre publica un article amb una fotografia principal, un enllaç a l'àlbum de fotos i un text que contextualitza les imatges.

## Pila tecnològica

| Component | Tecnologia |
|---|---|
| Generador | Hugo 0.164.0 extended |
| Tema | PaperMod, versionat dins del repositori |
| Producció i CMS | GitHub `112books/9bi` + Sveltia CMS 0.217.0 |
| Hosting | GitHub Pages a `https://9barrisimatge.org/` |
| CI/CD | GitHub Actions |
| Backup | Codeberg `linuxbcn/9bi` |
| Estadístiques | GoatCounter |

## Estructura principal

```text
config/                     Configuració de Hugo per entorn
content/posts/YYYY/         Articles, agrupats per any
content/guia/               Guia d'editors, publicada sense indexar
layouts/                    Plantilles del lloc, inclosa la 404
assets/css/extended/        Estils personalitzats
static/admin/               Sveltia CMS autoallotjat
static/images/              Imatges
static/stats/               Dashboard d'estadístiques
data/membres/               Fitxer de dades per membre
modules/                    Aplicacions WSGI independents del web estàtic
scripts/                    Migració i obtenció d'estadístiques
.github/workflows/          Desplegament a GitHub Pages
```

## Desenvolupament local

```bash
hugo server -D
```

El lloc queda disponible a `http://localhost:1313`.

Build de producció:

```bash
hugo --minify --environment production
```

El resultat es genera a `public/`.

## Publicació

La branca `main` local segueix el remot `github`:

```bash
git push github main
```

GitHub Actions construeix el lloc i el publica a `https://9barrisimatge.org/`. Cal comprovar el deploy i les pàgines affectedes abans de considerar la feina tancada.

`origin` apunta al backup de Codeberg. No hi ha cap push habitual fins que la quota permeti sincronitzar-lo de nou. **No s'ha d'esborrar ni reinicialitzar cap dels dos repositoris**: GitHub és producció i Codeberg conserva l'historial de reserva.

## CMS dels editors

El gestor és a `https://9barrisimatge.org/admin/` i fa servir el backend GitHub.

### Donar accés a un editor

1. Obrir el repositori `112books/9bi` a GitHub.
2. Anar a **Settings → Collaborators → Add people**.
3. Convidar la persona amb accés **Write**.
4. La persona accepta la invitació i crea el seu propi token.

### Entrar al gestor

1. La persona crea un token a **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**.
2. Ha de marcar l'àmbit `repo`.
3. A `https://9barrisimatge.org/admin/` fa clic a **Sign In with Token** i enganxa el token.

Els tokens no s'inclouen als correus ni es desen al repositori. Si un token es filtra, cal revocar-lo immediatament.

La guia pública per als editors és `https://9barrisimatge.org/guia/`, amb `robotsNoIndex` i fora del menú públic.

### Límits actuals de permisos

El backend del CMS utilitza els permisos del repositori. Una persona amb accés Write pot llegir i escriure al repositori sencer; el gestor actual no aplica una ACL que limiti cada editor a verificar només els seus propis articles. Cal revisar aquests permisos abans d'obrir l'accés a tots els membres.

## Guia d'editors

Les pàgines viuen a `content/guia/` i es construeixen amb:

- `robotsNoIndex: true`
- `hiddenInRss: true`
- `sitemap.disable: true`
- enllaç «Guia al web» al capçalera del CMS

La documentació de manteniment més àmplia, l'estat real, el backlog i les decisions es mantenen a `CLAUDE.md`.

## Pàgina 404

`layouts/404.html` genera la resposta personalitzada que GitHub Pages mostra per a qualsevol ruta inexistent. Inclou el missatge «Aquesta pàgina no s'ha trobat», cerca directa amb el mateix índex Fuse de `/search/` i enllaços a Portada, Arxiu i Contacte.

La pàgina conserva HTTP 404, inclou `noindex, nofollow` i no depèn d'una il·lustració externa. Les rutes de l'índex de cerca es construeixen amb `relURL`, de manera que la funcionalitat també és base-aware en entorns desplegats sota un subdirectori.

## Estadístiques

El lloc `9bi.goatcounter.com` registra les visites sense cookies. El secret `GOATCOUNTER_API_KEY` està a GitHub Actions i el dashboard de `/stats/` es refresca durant cada desplegament.

Per generar localment la llista d'articles més visitats:

```bash
export GOATCOUNTER_API_KEY="..."
python3 scripts/goatcounter_popular.py --days 30
```

## Migració de Blogger

La migració dels 3.006 articles originals s'ha completat. Els fitxers viuen a `content/posts/YYYY/`; els permisos, enllaços especials, autors i altres correccions s'han aplicat després de la migració.

Scripts relacionats:

- `scripts/migrate_blogger.py`
- `scripts/migrate_live.py`

## Enllaços principals

- Producció: `https://9barrisimatge.org/`
- CMS: `https://9barrisimatge.org/admin/`
- Guia: `https://9barrisimatge.org/guia/`
- Cerca: `https://9barrisimatge.org/search/`
- Arxiu: `https://9barrisimatge.org/archive/`
- RSS: `https://9barrisimatge.org/index.xml`

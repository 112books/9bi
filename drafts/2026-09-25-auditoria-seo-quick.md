# Auditoria ràpida SEO / GEO / AEO — 9barrisimatge.org

**Data:** 25 de setembre de 2026
**Abast:** Quick Audit (portada + 7 pàgines clau + 1 article + `robots.txt` + `sitemap.xml`)
**Mètode:** HTML en viu del web publicat + revisió dels fitxers del tema i del build local.
**No avaluat:** Core Web Vitals, velocitat real, backlinks, autoritat de domini (necessiten Google PageSpeed Insights, Search Console i eines de backlinks).

## Resum executiu

El web té una base sòlida i molt ben treballada per a un arxiu fotogràfic: `robots.txt` obert amb sitemap, 4.724 URL al sitemap, canòniques a totes les pàgines, un únic H1, text alternatiu al 100% de les imatges, HTTPS i dades estructurades reals (`Organization`, `BlogPosting`, `BreadcrumbList`). El problema més seriós no és la falta de senyal, sinó **l'escala**: les 1.676 pàgines d'etiquetes i les 25 pàgines d'autors comparteixen **exactament la mateixa meta descripció que la portada**, i la pàgina de cerca interna `/search/` és indexable i surt al sitemap. En segon lloc, `/faq/` — una pàgina feta per respondre preguntes — no té cap `FAQPage` schema ni cap H2, de manera que motors de cerca i assistents d'IA no tenen res estructurat a què recórrer. L'oportunitat més gran és barata: les metadades i schema es resolen en el tema, en quatre o cinc llocs.

| Dimensió | Puntuació | Estat |
|---|---|---|
| SEO | 7/10 | Bona base, correccions pendents |
| GEO | 6/10 | Bona base, entitat a reforçar |
| AEO | 5/10 | Oportunitat clara i barata |
| **Combinat** | **18/30** | |

## Pàgines auditades

| URL | Tipus | Notes |
|---|---|---|
| `/` | Portada | Títol 37 car., desc. 95 car., canònica apunta a `/index.html`, Organization JSON-LD, `og:image` absent |
| `/qui-som/` | Pàgina interna | Descripció pròpia, 1.446 paraules, BreadcrumbList + BlogPosting |
| `/concurs/` | Pàgina clau | 2.049 paraules, títol de 82 car. (es talla al resultat), sense `og:image` |
| `/faq/` | Pàgina clau | 7 preguntes en H3, cap H2, cap `FAQPage` schema, 242 paraules |
| `/contacte/` | Pàgina interna | 258 paraules, formulari, sense schema de contacte |
| `/archive/` | Arxiu | Index de 49.518 paraules, descripció genèrica («Arxiu - Col·lectiu...») |
| `/search/` | Cerca interna | **Indexable i al sitemap**; hauria de ser `noindex` |
| `/2026/09/2026-09-19-...html` | Article | `og:image` + `summary_large_image`, BlogPosting ric, títol de 92 car. |
| `/robots.txt` | Configuració | `Disallow:` buit + `Sitemap:` correcte |
| `/sitemap.xml` | Configuració | 4.724 URL, pla (sense sitemap index) |

## Anàlisi SEO — 7/10

### Tècnic i a pàgina

| Senyal | Troballa | Estat |
|---|---|---|
| Title | Present a totes les pàgines, però sovint >60 car.: `/concurs/` 82, `/faq/` 77, articles 92 (`Títol | Col·lectiu fotogràfic 9 Barris Imatge`) | Cal attention |
| Meta description | Les 8 pàgines principals tenen text propi i bo; **1.676 tags + 25 autors comparteixen la descripció de la portada** | Cal atenció |
| Canonical | Present a totes, però la portada declara `https://9barrisimatge.org/index.html` en lloc de `/` (també a l'JSON-LD) | Cal atenció |
| H1 | Exactament 1 a cada pàgina auditada | Bé |
| Jerarquia H2/H3 | `/faq/` té 7 H3 i cap H2; `/concurs/` té 5 H2 | Cal atenció |
| Robots meta | `index, follow` a tot, excepte `/guia/` (`noindex, nofollow`, correcte) | Bé |
| Viewport / mòbil | Present, disseny responsive | Bé |
| Text alternatiu | 0 imatges sense `alt` a les 8 pàgines (21 imatges a la portada) | Bé |
| Enllaços interns | Navegació completa (Arxiu, Tags, Cerca, Més visitats, Stats) | Bé |
| Open Graph | `og:title/description/url/site_name/locale/type` presents; **`og:image` només als articles amb portada**; a la portada i 6 pàgines no hi ha imatge | Falta |
| Twitter Card | `summary` a les pàgines internes, `summary_large_image` als articles | Cal atenció |
| URL | Netes, amb `uglyURLs` conservant les URL `.html` de Blogger | Bé |
| Sitemap / robots | 4.724 URL, correctes; **`/search/` i `/mes-visitats/` hi són dins**; `/guia/` i `/stats/` fora (però `/stats/` és rastrejable: no té cap meta robots) | Cal atenció |
| Pàgines amb contingut prim: 1.676 tags | Moltes amb un sol article; totes amb la mateixa descripció i sense text propi | Cal atenció |

### Contingut

| Senyal | Troballa | Estat |
|---|---|---|
| Extensió | Articles de 171–2.049 paraules; pàgines clau amb contingut real | Bé |
| Paraules clau | Tema geogràfic (Nou Barris, Barcelona) i noms d'esdeveniments molt ben establerts | Bé |
| Frescor | `datePublished`/`dateModified` reals als articles; «Avui fa…» a la portada | Bé |
| Legibilitat | Mosaic, capçaleres i pàgines clau amb estructura clara | Bé |
| Portada | 234 paraules: només H1 + l'eslògan + mosaic. Poca narració per a qui arriba de cerca o d'un assistent d'IA | Cal atenció |

### Dades estructurades

| Senyal | Troballa | Estat |
|---|---|---|
| Organization (portada) | Nom, URL, descripció, logo, `sameAs` | Bé |
| Logo de l'entitat | `favicon.ico` com a logo (Organization i `publisher` dels articles) — imatge molt petita | Cal atenció |
| `sameAs` | Buit: hi ha Instagram i Telegram al peu però no hi són al schema (`SocialIcons` buit a la config) | Cal atenció |
| BlogPosting | Molt complet: `headline`, `description`, `keywords`, `articleBody`, `wordCount`, `inLanguage`, `image`, `datePublished`, `dateModified`, `author` (Person), `publisher` | Bé |
| BreadcrumbList | A totes les pàgines i seccions | Bé |
| FAQPage | **Cap**, tot i que `/faq/` té 7 preguntes | Falta |
| Person (pàgines d'autor) | **Cap** a les 25 pàgines d'autor (ni H1 ni schema amb el nom real) | Falta |
| Validesa | JSON-LD sintàcticament correcte a les pàgines auditades | Bé |

## Anàlisi GEO — 6/10

### E-E-A-T

| Senyal | Troballa | Estat |
|---|---|---|
| Autors | Només via `BlogPosting.author` (Person amb nom real, sense `@id` ni enllaç) | Bé |
| About / Qui som | Pàgina de 1.446 paraules amb història, com funcionen, membres, relacions iadreça | Bé |
| Contacte | Formulari + correu + adreça del Casal a `/contacte/` i pàgines legals | Bé |
| Senyals de confiança | 24 anys d'activitat, 3.008 articles, 24 membres, exposicions, concurs anual, llicència CC clara | Bé |
| Organization schema | Present però amb logo = favicon i `sameAs` buit | Cal atenció |

### Contingut per a síntesi d'IA

| Senyal | Troballa | Estat |
|---|---|---|
| Densitat factual | Dates, ubicacions, noms de les festes, categories i premis del concurs; articles amb data i lloc | Bé |
| Reclamacions clares | Eslògan a la portada, missió a `/qui-som/` | Bé |
| Cites de fonts | Poques; no hi ha referències a arxius o institucions dins el text | Cal atenció |
| Comprehensió | Les pàgines clau responen el que prometen | Bé |
| Claritat d'entitat | «Col·lectiu 9 Barris Imatge» coherent a tot arreu | Bé |
| Originalitat | Fons fotogràfic propi de 24 anys: és l'activitat més difícil de copiar | Bé |

### Tècnic GEO

| Senyal | Troballa | Estat |
|---|---|---|
| Profunditat del schema | `BlogPosting` molt ric; manquen `FAQPage`, `Person`, `ProfilePage`, `HowTo` | Cal atenció |
| HTTPS | Cert vàlid, redirecció `http`→`https` | Bé |
| Rastrejabilitat | `robots.txt` obert, HTML estàtic servit directament, sense renderitzat JS obligatori | Bé |
| Enllaços d'entitat | Instagram i Telegram al peu, però absents del `sameAs` | Cal atenció |

## Anàlisi AEO — 5/10

### Els millors resultats

| Senyal | Troballa | Estat |
|---|---|---|
| Pàgines de preguntes | `/faq/` amb 7 preguntes reals sobre llicència i ús de les fotos | Bé |
| Llistes i taules | Cronologia i categories del concurs, taules de membres i d'història | Bé |
| Contingut fàctic | Dates del concurs, categories, premis, termini: fàcil d'extreure | Bé |

### Formats de resposta estructurada

| Senyal | Troballa | Estat |
|---|---|---|
| FAQ schema | **Cap** a `/faq/` | Falta |
| HowTo schema | «Com participar» és un candidat natural i no està marcat | Falta |
| Encapçalats amb pregunta | Les 7 preguntes són H3, sense H2 que les agrupi; cap formulada com a «Com puc…?» | Cal atenció |
| Speakable | Cap | Falta |

### Cerca per veu

| Senyal | Troballa | Estat |
|---|---|---|
| Llenguatge | Text fàcil i natural en català | Bé |
| Preguntes de cua llarga | Les 7 de la FAQ cobreixen com citar, on usar, ús comercial | Bé |
| Senyals locals | Adreça del Casal a les pàgines legals, «Nou Barris (Barcelona)» a la portada; sense schema `LocalBusiness`/`Place` | Cal atenció |

## Prioritats

| # | Prioritat | Problema | Dimensió | Esforç | Impacte |
|---|---|---|---|---|---|
| 1 | 🔴 Crítica | Descripció meta idèntica a la portada en 1.676 pàgines d'etiquetes i 25 d'autors; `/search/` indexable i al sitemap; `/stats/` rastrejable sense `noindex` | SEO | Baix (config del tema) | Alt |
| 2 | 🟠 Alta | Pàgina `/faq/` sense `FAQPage` schema ni H2 | AEO / GEO | Baix | Alt |
| 3 | 🟠 Alta | Canònica de la portada a `/index.html` en lloc de `/` | SEO | Molt baix | Mitjà |
| 4 | 🟠 Alta | Sense `og:image` a portada i pàgines internes (només als articles amb portada) | SEO / GEO | Baix | Mitjà-alt |
| 5 | 🟡 Mitjana | Títols >60 car. a `/concurs/`, `/faq/` i articles (sufix llarg del nom del lloc) | SEO | Baix | Mitjà |
| 6 | 🟡 Mitjana | `Organization` amb logo = favicon i `sameAs` buit; sense `Person`/`ProfilePage` a les pàgines d'autor | GEO | Mitjà | Mitjà-alt |
| 7 | 🟡 Mitjana | Portada amb només 234 paraules: poc text per a Visió IA i motors | GEO / AEO | Mitjà (contingut, cal aprovació) | Mitjà |
| 8 | 🟢 Ràpida guanya | `HowTo` schema a «Com participar»; agrupar les preguntes de la FAQ en H2 | AEO | Baix | Mitjà |

## Què funciona molt bé

- **Arquitectura i rastrejabilitat**: `robots.txt` net amb sitemap, 4.724 URL, cap pàgina interna bloquejada, HTML estàtic.
- **Dades estructurades reals i validades**: `BlogPosting` amb `articleBody`, comptador de paraules, imatge, dates, autor i editor; `BreadcrumbList` a tot arreu; JSON-LD sense errors de sintaxi.
- **Accessibilitat i semàntica**: un H1 per pàgina, text alternatiu al 100% de les imatges (0 de 106 imatges sense `alt` a les pàgines auditades), `lang=ca`, enllaços amb text.
- **Autoria real**: 24 membres amb nom i cognom, perfil propi, i `author` a l'esquema de cada article.
- **Riquesa del material**: 24 anys i 3.008 articles propis és un actiu originals que cap competidor pot replicar; el concurs anual dona actualitat periòdica.
- **Protecció de la guia**: `/guia/` amb `noindex, nofollow` i fora del sitemap, sense exposar el material intern.

## Notes tècniques i on tocar-ho

- Canònica i JSON-LD de portada: `themes/PaperMod/layouts/_partials/head.html:25` i `themes/PaperMod/layouts/_partials/templates/schema_json.html:1-22`.
- `logo` i `publisher.logo`: `themes/PaperMod/layouts/_partials/templates/schema_json.html:12` i `:119-122` (demanen `params.assets.favicon`).
- `sameAs`: `themes/PaperMod/layouts/_partials/templates/schema_json.html:14-20` (llegeix `params.schema.sameAs` o `params.socialIcons`).
- Descripció per defecte de taxonomies: `hugo.toml` `[params] description` (és la que hereten autor i etiqueta).
- `noindex` de `/search/`: `content/search.md` (afegir `robotsNoIndex: true` + `sitemap.disable: true`, com ja es fa a `content/guia/`).
- `og:image` per defecte: cap punt central actual; cal un `images/og-default.jpg` i inserir-lo a `layouts/_partials/extend_head.html` per a les pàgines sense portada.
- `FAQPage`: cal un esquema nou a `layouts/`, per exemple `layouts/_partials/schema-faq.html`, inclòs des de `baseof.html` només a `.Params.layout == "faq"`; les respostes ja són a la pàgina.
- Pàgines d'autor: `layouts/author/term.html` (sobreescrit) pot afegir `Person` amb `name`, `url` i `sameAs` de la instància; les dades reals són a `data/membres/<slug>.yml`.

## Priorització suggerida d'execució

1. Metadades en massa: descripció pròpia per autor i etiqueta, `noindex` a `/search/` i `/stats/`, fora del sitemap on toqui.
2. Canònica de la portada a `/` i `og:image` per defecte.
3. `FAQPage` + H2 a `/faq/`; `HowTo` a `/concurs/`.
4. `Organization` enrichment (logo real, `sameAs` amb Instagram i Telegram) i `Person` a les pàgines d'autor.
5. Títols curts (sufix «9 Barris Imatge» en lloc del nom sencer) i text propi a la portada.

Cada canvi és del tema o de configuració: es pot aplicar per commit, amb build i verificació en viu, sense tocar el contingut dels articles.

---
title: "Com publicar un article"
description: "El flux complet per publicar una entrada al web amb el CMS (Sveltia)"
robotsNoIndex: true
hiddenInRss: true
sitemap:
  disable: true
---

{{< guia-tabs >}}

Al bloc, cada membre publica un article amb **una fotografia principal**, un **enllaç a l'àlbum** i un **text** que contextualitza les imatges. Aquí tens el flux complet.

## 1. Entra a l'administració

- Ves a **https://9barrisimatge.org/admin/**, fes clic a **"Sign In with Token"** i utilitza el token personal de GitHub creat segons la [guia per crear un compte d'editor](/guia/crear-compte/).

## 2. Crea un article nou

- A la llista d'"Articles", fes clic a l'apartat **"Articles"** del menú lateral i després a **"Nou article"** (botó *New*).

## 3. Omple els camps

La fitxa de l'article té aquests camps, **en aquest mateix ordre**. A cada fila hi tens què s'hi posa i per a què serveix.

| Camp | Què hi has de posar i per a què serveix |
|---|---|
| **Títol** | El títol de la crònica (p. ex. *Prospe Beach '26: la Prosperitat torna a plena de sorra*). És el que surt a la portada, a l'article, al RSS i a la cerca. |
| **Data de publicació** | La data de l'esdeveniment (per defecte, avui). Ordena l'article a la portada, a l'arxiu i a les llistes per autor: el més recent surt primer. |
| **Any (el posa el sistema)** | No s'ha de tocar: el gestor el dedueix de la carpeta de l'any on es desa l'article i serveix per classificar-lo a l'arxiu per anys. |
| **Adreça web de l'article (no tocar)** | La part final de l'enllaç (…/2026/10/nom-de-l-article.html). S'omple sola i no s'ha de canviar: si la canvies, l'enllaç antic deixa de funcionar i no es redirigeix. |
| **Autor** | El nom que signa l'article: surt al peu de l'entrada, a la pàgina de l'autor i a les fitxes de projectes. Si el teu compte de GitHub ja està donat d'alta, et surt posat i no l'has de tocar. |
| **Fotografia principal** | La foto que encapçala l'article: es veu al mosaic de la portada, a «Avui fa…», a les llistes per autor i a l'article. La puges amb el botó d'imatge del camp «Imatge». |
| **Text alternatiu (ALT)** | Dins de «Fotografia principal»: descripció curta del que es veu a la foto. La fan servir els lectors de pantalla i els cercadors. Si el deixes buit, s'usa el títol. |
| **Foto de capçal de l'article (opcional)** | Una foto gran a tot l'ample, just sota el títol de l'article. No és la foto de portada: si la deixes buida, l'article simplement no en mostra cap. Si hi poses la mateixa foto que a «Fotografia principal», la veuràs **dues vegades**. |
| **Text alternatiu de la foto de capçal (ALT)** | La descripció de la foto de capçal, per als lectors de pantalla i els cercadors. Si el deixes buit, s'usa el títol. |
| **Destaca'l al capdamunt de la portada** | Marca-ho només si l'article ha de sortir el primer al mosaic de la portada (per exemple, el concurs mentre és vigent). Desmarca-ho quan deixi de ser-ho. |
| **Enllaç a l'àlbum de fotos** | L'enllaç públic de l'àlbum sencer (vegeu les guies de cada plataforma). És el que fa aparèixer el botó «Veure tot l'àlbum de fotos» al final de l'article. |
| **Vídeos (YouTube o Vimeo)** | Un enllaç per línia. Els reproductors surten al final de l'article, en el mateix ordre. |
| **Paraules clau (tags)** | Temes que ajuden a trobar l'article, p. ex. `prospebeach`, `festa major`, `música en viu`. Cada etiqueta té la seva pàgina i alimenta el núvol d'etiquetes. |
| **Títol SEO (opcional)** | El títol per als cercadors i les xarxes (fins a ~60 caràcters). Si el deixes buit, s'usa el títol de l'article sense la data inicial. |
| **Descripció (SEO, opcional)** | Resum que apareix a la llista, al RSS i com a meta descripció. Si el deixes buit, s'agafa un resum de l'article. |
| **Cos de l'article** | El text: crònica, comentari de les imatges, agraïments… Admet Markdown (ho tens al punt següent). |

### Quina foto va a cada lloc

L'article té dos camps de foto i **no fan el mateix**. Aquesta és la diferència:
{.guide-note}

| Camp | On surt | Què hi va |
|---|---|---|
| **Fotografia principal** (amb el seu ALT) | Al mosaic de la portada del web, a les llistes per autor, a «Avui fa…», al RSS, a la imatge que es veu en compartir l'enllaç i com a figura gran a l'inici de l'article | La foto de portada: una de sola i lleugera (uns 640 px d'amplada) |
| **Foto de capçal de l'article** (opcional) | Només dins de l'article, a tot l'ample i just sota el títol | Una foto **diferent**, pensada per a tota l'amplada. Si hi poses la mateixa que la principal, la veuràs dues vegades |

Si només tens una foto, omple **«Fotografia principal»** i deixa la foto de capçal buida.
{.guide-note}

## 4. Escriviu el text (Markdown)

El cos de l'article admet format senzill:

- **Negreta**: escriu `**text en negreta**`.
- *Cursiva*: escriu `*text en cursiva*`.
- Llistes: escriu `- element` a cada línia (o `1.` per a llistes numerades).
- Enllaços: escriu `[text de l'enllaç](https://exemple.cat)`.
- Imatges addicionals dins del text: `![títol](URL_de_la_imatge)` (si l'enllaç és una URL pública).

Heu de separar els paràgrafs amb una línia en blanc. No passeu d'una línia sense paràgraf.
{.guide-note}

### Text alternatiu (ALT) de les fotos

El camp **«Text alternatiu (ALT)»**, dins de «Fotografia principal», és la descripció de la foto que fan servir els lectors de pantalla (persones cegues o amb poca visió) i els cercadors. Escriu-hi una descripció curta del que es veu, per exemple: *Públic assegut a les grades del Casal durant el concert*.
{.guide-note}

Si el deixes buit, s'usa el títol de l'article (és el que fan tots els articles publicats abans que existís aquest camp, així que no cal omplir-lo en els antics). El mateix text es fa servir a la portada, a «Avui fa…», a les llistes per autor i a la fitxa de projectes.

La **foto de capçal** té el seu propi camp d'ALT, amb la mateixa finalitat i la mateixa regla: si el deixes buit, s'usa el títol.

### Foto de capçal de l'article (opcional)

El camp **«Foto de capçal de l'article»** mostra una foto gran, a tot l'ample, just sota el títol de l'article. És opcional i no substitueix la fotografia principal: aquella és la que surt al mosaic de la portada i a les llistes, i aquesta només surt dins de l'article.
{.guide-note}

- Si no n'hi poses cap, l'article no mostra cap foto de capçal i queda com sempre.
- Serveix per a reportatges on vols obrir amb una imatge panoràmica, sense que aquesta hagi de fer de portada a la portada del web.
- Si hi poses la mateixa foto que a «Fotografia principal», surt dues vegades dins de l'article: la figura de portada i la capçal.

### Destacar un article al capdamunt de la portada

La casella **«Destaca'l al capdamunt de la portada»** fa que l'article surti el primer al mosaic de la portada, per davant dels més recents. La resta d'articles continuen ordenats per data.
{.guide-note}

- Serveix per a casos puntuals: el concurs mentre el període de presentació és obert, una convocatòria, un avís important.
- Quan deixi de ser vigent, edita l'article i desmarca la casella.
- Només afecta la portada: l'arxiu, les etiquetes i les llistes per autor continuen ordenades per data.
- Si hi ha més d'un article destacat, surten tots davant la resta, ordenats per data entre ells.

### L'adreça web de l'article (no tocar)

El camp **«Adreça web de l'article (no tocar)»** és el final de l'enllaç de l'article (per exemple, `/2026/10/prospe-beach-26.html`). El gestor l'omple sol quan crees l'article i normalment no cal tocar-lo.
{.guide-note}

- Si el canvies, l'enllaç antic que ja s'ha compartit deixa de funcionar i **no hi ha redirecció**: qui el tingui desat trobarà una pàgina d'error.
- Només té sentit canviar-lo just abans de publicar, si el nom automàtic ha quedat malament.

### Vídeos de YouTube o Vimeo

Per posar vídeos a l'article, ompliu el camp **«Vídeos (YouTube o Vimeo)»** de la fitxa amb l'enllaç de cada vídeo, un per línia (el botó «+» n'afegeix més):

- **YouTube:** `https://www.youtube.com/watch?v=dQw4w9WgXcQ` o `https://youtu.be/dQw4w9WgXcQ`.
- **Vimeo:** `https://vimeo.com/146022717`.

Els reproductors apareixeran al final de l'article, en el mateix ordre, amb la mida adaptada a la pantalla. No cal tocar el text ni canviar de mode de l'editor.
{.guide-note}

### Títol SEO i Descripció

Els dos camps opcionals de la part de baix de la fitxa són per als cercadors i les xarxes socials, no per a la gent que llegeix el web:
{.guide-note}

- **Títol SEO**: el títol que veuran Google i les xarxes. Si el deixes buit, s'usa el títol de l'article sense la data inicial.
- **Descripció**: el resum que surt a la llista d'articles, al RSS i a la fitxa que es comparteix. Si el deixes buit, s'agafa un resum del text.

### El pes de la foto principal

La portada és un mosaic que carrega moltes fotos alhora, així que la imatge que hi surt ha de ser petita. No te n'has de preocupar: quan publiques, el web **genera tot sol una miniatura** de la fotografia principal (WebP de com a màxim 640 px d'amplada) i la fa servir a la portada i a les llistes.

- Pots pujar l'original que tinguis: la miniatura es fa automàticament.
- La foto gran de dins de l'article no es toca: si en vols una de grossa, posa-la a «Foto de capçal».
{.guide-note}

## 5. Desa i publica

- Per desar i estar pendent: utilitzeu el botó **"Desa com a esborrany"** (draft).
- Quan estigui llest, utilitzeu **"Publica"** (Publish).
- En uns **2–3 minuts**, el lloc es reconstruirà automàticament i l'article sortirà a la portada, al RSS i a la cerca.

## 6. Revisa el resultat

- La teva publicació apareixerà al **mosaic de la portada** amb la foto com a portada.
- A l'article sencer hi haurà el botó **"Veure tot l'àlbum de fotos"** que porta a l'àlbum complet.

## Errors freqüents

- **La foto no es veu**: revisa que s'hagi pujat bé al gestor (bàsicament per files, el camp de la imatge).
- **L'àlbum no s'obre**: l'enllaç ha de ser *públic* (compartit), no només visible per a tu.
- **El text surt tot junt**: recorda separar els paràgrafs amb una línia en blanc.
- **L'article no surt el primer a la portada**: revisa que hagis marcat «Destaca'l al capdamunt de la portada» i que hagis desat (triga uns 2–3 minuts a reconstruir-se el web).
- **L'enllaç antic ja no funciona**: algú ha canviat «Adreça web de l'article». Torna a posar-hi el valor anterior; no hi ha redireccions.

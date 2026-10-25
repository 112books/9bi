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

| Camp | Què hi has de posar |
|---|---|
| **Títol** | El títol de la crònica (p. ex. *Prospe Beach '26: la Prosperitat torna a plena de sorra*). |
| **Data** | La data de l'esdeveniment (per defecte, avui). |
| **Autor** | El teu nom d'usuari. |
| **Fotografia principal** | La foto que encapçala l'article (la veuran tothom a la portada i a l'article). La podeu pujar amb el botó d'imatge del gestor. |
| **Text alternatiu (ALT)** | Dins de «Fotografia principal»: descripció curta del que es veu a la foto. Si el deixes buit, s'usa el títol de l'article. |
| **Destaca'l al capdamunt de la portada** | Marca-ho només si l'article ha de sortir el primer al mosaic de la portada (per exemple, el concurs mentre és vigent). |
| **Enllaç a l'àlbum de fotos** | L'enllaç de l'àlbum sencer (vegeu les guies específiques de cada plataforma). |
| **Paraules clau (tags)** | Temes que ajuden a trobar l'article, p. ex. `prospebeach`, `festa major`, `música en viu`. |
| **Descripció (opcional)** | Resum que apareix a la llista i al RSS. |
| **Cos** | El text: crònica, comentari de les imatges, agraïments… |

## 4. Escriviu el text (Markdown)

El cos de l'article admet format senzill:

- **Negreta**: escriu `**text en negreta**`.
- *Cursiva*: escriu `*text en cursiva*`.
- Llistes: escriu `- element` a cada línia (o `1.` per a llistes numerades).
- Enllaços: escriu `[text de l'enllaç](https://exemple.cat)`.
- Imatges addicionals dins del text: `![títol](URL_de_la_imatge)` (si l'enllaç és una URL pública).

Heu de separar els paràgrafs amb una línia en blanc. No passeu d'una línia sense paràgraf.
{.guide-note}

### Vídeos de YouTube o Vimeo

Per posar vídeos a l'article, ompliu el camp **«Vídeos (YouTube o Vimeo)»** de la fitxa amb l'enllaç de cada vídeo, un per línia (el botó «+» n'afegeix més):

- **YouTube:** `https://www.youtube.com/watch?v=dQw4w9WgXcQ` o `https://youtu.be/dQw4w9WgXcQ`.
- **Vimeo:** `https://vimeo.com/146022717`.

Els reproductors apareixeran al final de l'article, en el mateix ordre, amb la mida adaptada a la pantalla. No cal tocar el text ni canviar de mode de l'editor.
{.guide-note}

### Text alternatiu (ALT) de la foto

El camp **«Text alternatiu (ALT)»**, dins de «Fotografia principal», és la descripció de la foto que fan servir els lectors de pantalla (persones cegues o amb poca visió) i els cercadors. Escriu-hi una descripció curta del que es veu, per exemple: *Públic assegut a les grades del Casal durant el concert*.
{.guide-note}

Si el deixes buit, s'usa el títol de l'article (és el que fan tots els articles publicats abans que existís aquest camp, així que no cal omplir-lo en els antics). El mateix text es fa servir a la portada, a «Avui fa…», a les llistes per autor i a la fitxa de projectes.

### Destacar un article al capdamunt de la portada

La casella **«Destaca'l al capdamunt de la portada»** fa que l'article surti el primer al mosaic de la portada, per davant dels més recents. La resta d'articles continuen ordenats per data.
{.guide-note}

- Serveix per a casos puntuals: el concurs mentre el període de presentació és obert, una convocatòria, un avís important.
- Quan deixi de ser vigent, edita l'article i desmarca la casella.
- Només afecta la portada: l'arxiu, les etiquetes i les llistes per autor continuen ordenades per data.
- Si hi ha més d'un article destacat, surten tots davant la resta, ordenats per data entre ells.

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
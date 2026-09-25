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
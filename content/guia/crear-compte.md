---
title: "Com crear un compte d'editor"
description: "Com obtenir accés per publicar al web de 9 Barris Imatge"
robotsNoIndex: true
hiddenInRss: true
sitemap:
  disable: true
url: "/guia/crear-compte/"
---

{{< guia-tabs >}}

Per poder publicar al web, tots els editors entren al **Gestor de continguts** amb el seu **token personal de GitHub**. Això garanteix que només les persones convidades poden publicar i que cada article queda identificat amb el seu autor.

## Si ets administrador/a del web

1. A **GitHub**, entra al repositori del web (`112books/9bi`).
2. Ves a **Settings → Collaborators → Add people**.
3. Escriu el nom d'usuari de GitHub de la persona editora i concedeix-li accés de **Write** (pot crear i editar articles).
4. La persona rebrà una invitació per correu i haurà d'**acceptar-la** (des de GitHub, secció **Notifications**, o des del correu).

## Si ets editor/a (primer cop)

1. Crea un compte a **GitHub** (https://github.com/signup) i tria **un nom d'usuari senzill**, p. ex. `jpbarris` (el teu usuari apareix com a autor del web).
2. Accepta la **invitació de col·laborador** que rebràs (al correu de GitHub o a la secció **Notifications** de github.com).
3. Genera el teu **token personal**: GitHub → Settings → Developer settings → **Personal access tokens → Tokens (classic)** → Generate new token, amb l'àmbit **`repo`** marcat. Copia'l (només es mostra un cop).
4. Entra al gestor: **https://9barrisimatge.org/admin/**
5. Fes **login amb el token**: botó **"Sign In with Token"** i enganxa el token que acabes de copiar.
6. Ja pots començar a escriure articles. Continua a [Com publicar un article](/guia/publicar-article.html).

Notes de seguretat:
- El token equival a accés d'escriptura al repositori: **no el comparteixis** amb ningú i no el publictis.
- Si creus que algú té el teu token, revoca'l i genera'n un de nou (mateix lloc: Settings → Developer settings).

Si no tens cap compte de GitHub i no saps com crear-lo, demana ajuda a l'administració del col·lectiu.
{.guide-note}

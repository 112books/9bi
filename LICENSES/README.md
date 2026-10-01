# Llicències dels components

El codi del projecte (plantilles, guions i mòduls) és del **Col·lectiu 9 Barris
Imatge** i es publica sota la **AGPL-3.0**, amb el text complet a `LICENSE`.
Els continguts (textos i fotografies) es publiquen sota
**CC BY-NC-SA 4.0**, i es declara a la pàgina de crèdits del web.

Aquesta carpeta conté els textos de llicència dels components de tercers que
s'inclouen al repositori. Cap d'ells es re-licencia: cadascun conserva la seva
llicència original i el seu text viu aquí.

| Fitxer de text | Component | Llicència | On s'usa |
|---|---|---|---|
| `GPL-2.0.txt` | Text oficial de la GNU GPL versió 2 | GPL-2.0 | base de la llicència de les tipografies Gillius |
| `GPL-2.0-FONT-EXCEPTION-Gillius.txt` | Excepció de font d'Arkandis Digital Foundry | GPL-2.0-or-later WITH Font-exception-2.0 | `static/fonts/gillius/` |
| `OFL-1.1-Montserrat.txt` | Montserrat | SIL Open Font License 1.1 | `static/fonts/montserrat/` |

## Altres components de tercers

| Component | Llicència | On és el text |
|---|---|---|
| PaperMod (tema de Hugo) | MIT | `themes/PaperMod/LICENSE` |
| Sveltia CMS | MIT | distribuït dins `static/admin/sveltia-cms.js` (verificat al repositori oficial `sveltia/sveltia-cms`, 2026-09-27) |
| Hugo (generador) | Apache-2.0 | no s'inclou al repositori, s'instal·la separat |
| js-yaml 4.1.0 (pàgina de tasques del gestor intern) | MIT | capçalera `@license` dins `static/admin/intern/js-yaml.min.js` (paquet oficial d'npm, sha1 verificat 2026-09-30) |
| React (dins del paquet del CMS) | MIT | capçalera `@license` dins `static/admin/sveltia-cms.js` |
| GoatCounter (estadístiques) | Apache-2.0 | servei extern, no s'inclou |

## Per què importa el fitxer de l'excepció de les tipografies

Les tipografies **Gillius ADF** són d'Arkandis Digital Foundry i es publiquen
sota GPL amb una **excepció de font**. Sense aquesta excepció, un document que
incrusti la font podria considerar-se cobert pel GPL, i això xocaria amb
l'AGPL-3.0 del web. Per això el fitxer de l'excepció ha d'acompanyar sempre els
fitxers de font, també en qualsevol redistribució.

# Auditoria d'accessibilitat (T-18) — 2026-10-02

**Només informe: no s'ha tocat cap fitxer del web.** Les correccions de colors i de disseny necessiten aprovació.

## Mètode

- Eina: **axe-core 4** (lliure, MPL-2.0), executada amb Chromium sobre el build de producció local (`hugo --minify --environment production`).
- Regles: WCAG 2.0/2.1 nivells A i AA + bones pràctiques d'axe.
- **15 pàgines × 2 temes (fosc i clar) = 30 passades**: portada, portada pàg. 2, un post (13-B 1B), Arxiu, Qui som, Concurs, Cerca, Contacte, Incorpora-t'hi, FAQ, Projectes, fitxa 13-B, pàgina d'autor (Pedro Click), Etiquetes i la 404.
- Límit: una eina automàtica en detecta aproximadament un terç dels problemes. No s'ha provat amb lector de pantalla ni només amb teclat.

## Resultat

Cap problema amb el text alternatiu de les imatges, l'idioma de la pàgina, els noms dels enllaços o dels botons, ni les etiquetes dels formularis. Les incidències trobades són aquestes, de més a menys greu:

| Gravetat | Regla | On | Què passa |
|---|---|---|---|
| Crítica | `aria-required-children` | /concurs/ | El contenidor de pestanyes `.concurs-tablist` porta `role="tablist"` però conté un `<button>` (el botó «Descarrega en PDF»), que no és una pestanya. |
| Seriosa | `color-contrast` | Posts (etiquetes), /archive/ (índex d'anys), /concurs/ | Text amb contrast per sota de 4,5:1. Detall a sota. |
| Moderada | `landmark-unique` | Portada, pàg. 2, posts, autor | Hi ha dues navegacions (`<nav>`) sense nom distintiu (`aria-label`). |
| Moderada | `heading-order` | /faq/ | Salt de nivell de títol a «Puc fer servir les fotografies del web?». |
| Moderada | `landmark-one-main`, `region` | 404 | La pàgina 404 no té `<main>`: el contingut queda fora de regions. |
| Menor | `aria-allowed-role` | /qui-som/, /concurs/ | `role="tab"` posat sobre `<label>` de les pestanyes CSS (no és un element permès per a aquest rol). |
| Menor | `presentation-role-conflict` | Totes | El logo `img[aria-label="logo"]` té també un rol presentacional (ve del tema PaperMod). |

### Detall de contrast

| Element | Tema | Colors (text / fons) | Contrast | Mínim |
|---|---|---|---|---|
| Etiquetes al peu dels posts (`.post-tags a`) | fosc | `#9b9c9d` / `#37383e` | 4,24 | 4,5 |
| Recompte d'anys de l'índex de l'Arxiu (`.archive-rail-count`) | fosc | `#6b6b6c` / `#17181a` | 3,33 | 4,5 |
| Índex d'anys de l'Arxiu (`.archive-rail-link`) | clar | `#c3c3c4` / `#6a6a6b` | 3,06 | 4,5 |
| Recompte d'anys de l'Arxiu | clar | `#a0a0a0` / `#6a6a6b` | 2,06 | 4,5 |
| «Eyebrow» del concurs (`.concurs-eyebrow`) | fosc | `#e03131` / `#1d1e20` | 3,69 | 4,5 |
| Premi de les targetes de categoria (`.concurs-cat-prize`) | fosc | `#e03131` sobre la targeta | 2,99 | 4,5 |

El vermell d'accent `#e03131` sobre fons fosc no arriba a 4,5:1 en text petit. Com a banda o filet decoratiu no hi ha cap problema.

## Propostes (pendents d'aprovació, cap aplicada)

1. **Concurs, pestanyes**: treure el botó PDF de dins de `.concurs-tablist` (posar-lo just a fora) **o** treure `role="tablist"`. Canvi d'estructura, sense cap canvi visual si el botó queda al mateix lloc.
2. **Contrast**:
   - etiquetes dels posts: aclarir el text a ~`#b5b6b7`;
   - índex de l'Arxiu: aclarir o enfosquir els colors del recompte en tots dos temes;
   - concurs: per al text petit en vermell, fer servir un vermell més clar sobre fosc (~`#ff6b6b`, ≈5,6:1) i mantenir `#e03131` per a les bandes. **Canvi de disseny: cal decidir-ho.**
3. **Navegacions**: afegir `aria-label` a cada `<nav>` (per exemple «Menú principal» i «Paginació»). No té cap efecte visual.
4. **FAQ**: corregir el nivell del títol (p. ex. `###` → `##`). Pot canviar-ne la mida visual.
5. **404**: embolcallar el contingut amb `<main>`. Sense canvi visual.
6. **Pestanyes CSS (Qui som, Concurs)**: treure `role="tab"` dels `<label>`, o passar a botons reals amb JS. Sense canvi visual en la primera opció.

**Actualització 02/10**: aplicades 1 i 3, que no canvien res visible (captures idèntiques píxel a píxel). La 5 era un fals positiu: la 404 del web ja té `<main>`, i l'error venia del servidor de proves local, que servia la seva pròpia 404. Queden 2, 4 i 6.

**Recomanació original**: aplicar primer 1, 3 i 5 (no canvien res visible) i decidir 2 i 4 amb criteri de disseny.

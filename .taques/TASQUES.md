# Tasques de 9 Barris Imatge

Font única de tasques del projecte (des del 2026-09-27). **Els pendents ja no s'escriuen al `CLAUDE.md`.**

- **Pendents**: aquí, amb ID fix (`T-NN`), prioritat, data d'alta i termini.
- **Fetes**: quan es tanca una tasca, passa a «Fetes» amb data, temps i commit.
- **Detall de cada sessió** (hora a hora, què s'ha verificat): el registre diari `AAAA-MM-DD.md` d'aquesta mateixa carpeta.
- Aquesta carpeta és **pública** (el repositori de GitHub ho és): mai cap secret, contrasenya ni token.
- Històric del backlog anterior, tal com era al `CLAUDE.md`: [`arxiu-backlog-claude-2026-09-27.md`](arxiu-backlog-claude-2026-09-27.md).

Prioritats: 🔴 crític · 🟠 abans de l'exposició · 🟡 quan puguem · ⚪ idea / sense data.

## Pendents

| ID | P | Tasca | Alta | Termini | Estat / notes |
|---|---|---|---|---|---|
| T-01 | 🔴 | **Llista definitiva d'obres de la votació** (número, títol, autor, categoria) a `[obres]` del `config.ini` del servidor; després esborrar `data.db` i reiniciar | 27/09 | **30/11** | Bloquejada: el concurs acaba de començar (25/09) i les fotos es presenten fins al **20/11** → finestra real **21/11–30/11**. La votació s'obre sola l'01/12. **Preparat (27/09)**: omplir `drafts/obres-concurs-2026-plantilla.csv` → `python3 modules/votacio/tools/obres.py llista.csv -o obres.ini` (valida números repetits, `|`, categories A/B/C) → substituir **sencera** la secció `[obres]` del `config.ini` del servidor (treure la línia `rang = …`, si no les 100 obres de prova continuen) → aturar, esborrar `data.db`, arrencar i comprovar `/admin/obres` |
| T-06 | 🟡 | Desactivar Blogger | 21/09 | — | En espera, decisió de l'usuari: **de moment no s'apaga**. DNS ja apunten a 9barrisimatge.org |
| T-07 | 🟡 | Editors al CMS: convidar col·laboradors amb Write, comprovar que els no-admin només veuen els seus posts i si algú ja ha iniciat el seu usuari | 21/09 | — | Quan puguem |
| T-09 | 🟡 | Enllaços d'àlbums morts (Picasa → Google Photos), autor per autor | 18/09 | — | En marxa. Pipeline verificat (`scripts/albums_fix.py recull/validate/apply`); 10 fitxes de Joan Linux aplicades als posts (commit `b42e04f85`). CMS: camp `album` readonly + `filter` per amagar les corregides. 1.178 pendents de 1.189 fitxes a `recuperacio/`. |
| T-14 | ⚪ | Publicació automàtica a Instagram i Facebook + enllaços al web | 18/09 | — | Mateix patró que T-13 (`modules/telegram/`: RSS de `/posts/` + `state.json` + cron) |
| T-18 | 🟡 | Auditoria d'accessibilitat | 17/09 | — | **Informe** a `drafts/2026-10-02-auditoria-accessibilitat.md`. **Aplicades (02/10)** les correccions sense canvi visual: botó PDF fora del `tablist` del concurs, `aria-label` a les navegacions (menú, paginació, entrada anterior/següent); la 404 ja tenia `<main>` (fals positiu del servidor de proves). **Pendent de decisió de disseny**: contrast (etiquetes, Arxiu, vermell petit del concurs) i nivell de títol de la FAQ |
| T-19 | ⚪ | 5a pestanya de «Qui som»: Història de la fotografia a Nou Barris | 18/09 | — | Recerca feta, galeria en suspens |
| T-20 | ⚪ | Membres: completar els Instagram que falten | 18/09 | — | |
| T-22 | ⚪ | Reobrir l'issue #2522 de Codeberg (quota) | 21/09 | — | **Comentari de petició de GC enviat el 28/09 20:17** (branca `pages` esborrada abans). Pendent de resposta. Text a `drafts/2026-09-27-codeberg-issue-2522-reobrir.md` |
| T-23 | ⚪ | Revisió jurídica final de l'adequació RGPD | 18/09 | — | |
| T-26 | ⚪ | Control de fitxers del Concurs Cordoncillo (bases, històric…) | 18/09 | — | |
| T-28 | 🟡 | Staging a Codeberg (`https://linuxbcn.codeberg.page/9bi/`): els CSS es veuen trencats | 28/09 | — | **Diagnosticat (28/09)**: l'staging serveix el build vell del 24/09 fet amb l'`baseURL` de producció; l'enllaç surt `/assets/...` (sense `/9bi/`) → 404. Queda lligat a T-29 (el distribuïble nou substituirà aquest staging) |
| T-29 | 🟡 | **Publicar la versió distribuïble de Taro a Codeberg** (`linuxbcn/9bi` → `main`): la plantilla ja està feta i verificada a la branca local `distribucio` (`90ebcc6379`, `af8a537d6f`). Bloquejat pel **GC de Codeberg** (issue #2522, comentari enviat el 28/09 20:17; el compte encara marca 752,7 MiB). Quan passi: `git push origin distribucio:main` | 28/09 | — | Pla B si Codeberg no es desencalla: publicar la mateixa branca en un repo nou a GitHub |
| T-31 | 🟡 | Projectes (Fase 2): fitxes públiques a `/projectes/` (13-B, retrat gegant) | 01/10 | — | **Publicada** (PR #12). 02/10: taula de sessions per ruta (1B, 2B, 3, 4) amb articles, apilada al mòbil; etiqueta `13-B` afegida a 5 posts; projecte nou **Els Inoblidables** (Residència Porta, 2015). Falta: revisió en viu de l'usuari i dades no publicades (coordinació, estat de la ruta oberta del 23/10/2016). 02/10: **Els Inoblidables en esborrany** (`draft: true`, decisió de l'usuari: àlbums de Picasa morts i pendent de confirmar si es pot publicar); Retrat gegant passa a `aturat`, **text pendent que el dicti l'usuari**. 02/10: **to propi i fil d'Ariadna** (franja suau vermell 9bi, «Inici › Projectes › …», xips d'estat/responsable/dates) i **`/projectes/proposa/`** (formulari que envia al servei de contacte amb assumpte «Proposta de projecte»; botó a la llista i a cada fitxa). **Pendent provar l'enviament real** |

### Tancades sense fer

| ID | Tasca | Data | Motiu |
|---|---|---|---|
| T-02 | Rotar `admin_secret` i `secret` de la votació | 27/09 | Decisió de l'usuari: risc acceptat, no es rota |
| T-15 | Butlletí, correu per a cada membre + genèric, i grup de correu | 28/09 | Decisió de l'usuari: el pla de correu només permet 10 comptes. Cada membre fa servir el seu correu personal i el col·lectiu es comunica (i vota) pel grup privat de Telegram. El butlletí queda aparcat: les novetats ja surten al canal públic de Telegram |

## Fetes

### Registre per tasca (des del 2026-09-25)

| Data | ID | Tasca | Temps | Commit |
|---|---|---|---|---|
| 02/10 | T-31 | **Projectes: to propi i propostes**: franja suau vermell 9bi, fil d'Ariadna, xips; `/projectes/proposa/`; enllaç de tornada; Els Inoblidables en esborrany; Retrat gegant aturat | ~40 min | `5682586`, `86b95e0`, `faa17b6` |
| 02/10 | — | **Concurs**: coorganitzat amb el Casal de barri de Prosperitat + enllaços (text de l'usuari) | ~10 min | `7e2713c` |
| 02/10 | T-24 | **Gillius en woff2**: `GilliusADF-{Regular,Bold}.woff2` generats amb fontTools (mateixos glifs, 37→19 KB); el CSS els carrega primer i deixa l'OTF de reserva; preload passat a woff2. Els OTF es conserven (els fa servir la votació). Provat: el navegador baixa només els woff2 | ~10 min | (aquest commit) |
| 02/10 | T-11 | **Cerca a les pàgines d'autor**: quadre de cerca a `/author/<slug>.html` que només busca entre les entrades d'aquell autor (camp `author` afegit a `index.json`, filtre a `fastsearch.js`, scripts carregats a les pàgines d'autor). Provat: Pedro Click + «concurs» → 18 resultats, tots seus; `/search/` igual; 375 px sense desbordament | ~25 min | (aquest commit) |
| 02/10 | T-10 | **Etiquetes per freqüència**: verificat que ja estava fet — `/search/` i `/tags/` ordenen les 1.684 etiquetes de més a menys (`ByCount`) | ~5 min | — |
| 02/10 | T-21 | **Seguretat CI/CD**: verificat que ja estava fet — accions del workflow fixades per SHA, els 11 `.dl-*` ja no hi són, `deploy.sh` rebutja credencials a la URL i `app.py` les redacta, `modules/taro/.gitignore` coherent. Únic canvi: `modules/autopublica/tools/deploy.sh` fa el build en un directori temporal nou (`mktemp` + `trap`), com la versió de Taro; provat amb un remot local | ~15 min | (aquest commit) |
| 02/10 | T-27 | **Reunions (Fase 1) tancada**: l'usuari ha creat l'acta real del 01/10 des de `/admin/intern/` (repo privat `9bi-intern`, commit `a8bc079`) | — | PR #11 |
| 01/10 | T-31 | **Projectes (Fase 2)**: `content/projectes/` (13-B amb 3 sessions dels posts, retrat gegant en idea), fitxa pública amb sessions i reportatges de l'etiqueta, enllaç al peu, col·lecció al CMS. Provat en navegador (escriptori i 375 px) | ~45 min | `dc193fe` |
| 30/09–01/10 | T-27 | **Admin intern (Fase 1)**: documentació interna moguda al repo privat `112books/9bi-intern`, `/admin/intern/` (actes amb assistents, acords, tasques, visibilitat) i `tasques.html` (tasques obertes + acta nova amb les obertes). Fusionat amb la PR #11 | ~2 h | `f5d0383`…`78bd705`, merge `5035f5c` |
| 30/09 | — | **Redirecció de l'URL del post de Naya** (canvi de títol al CMS) | ~10 min | `e36dc4c8ba` |
| 30/09 | — | **SEO al CMS**: `seoTitle` + títol SEO automàtic (sense data) i `description` com a meta descripció; plantilles `seo-title`/`head`/`opengraph`/`twitter_cards` | ~20 min | `3af5e5b920` |
| 30/09 | — | **Autor per defecte segons el login** (`CMS_AUTHORS` + hook `preSave`) | ~10 min | `3af5e5b920` |
| 30/09 | — | **URLs estables**: `slug` explícit als 4 posts sense slug + hook per als articles nous | ~12 min | `cfbd4d2c3b` |
| 30/09 | — | **Ajuda planera del camp slug** al CMS | ~4 min | `0d473080fa` |
| 30/09 | — | **Regressió del slug buidat pel CMS**: restaurat + alias + hook que el recupera | ~8 min | `c1781d476d` |
| 30/09 | — | Documentació, registre d'hores i sincronització | ~8 min | — |
| 28/09 | T-30 | 6 títols llargs escurçats (T-08) i convenció de Joan Linux `any-mes-dia - títol` aplicada als 26 posts seus del lot | ~25 min | `d2cc9eacf9`, `d6cd104746` |
| 28/09 | — | **Estadístiques**: `hits_by_day` es construeix amb els dies de `/stats/total` (abans la suma del top-50 no quadrava: 159 vs 166). Verificat en viu: total 166 = suma dels dies. Etiqueta «total any» → «total període» | ~30 min | `27d4b914ff` |
| 28/09 | T-08 | Títols: 20 posts que eren «Sense títol» + 75 títols repetits desambiguats (95 posts en total) i esborrat el post buit del 2008. Només el camp `title`; URL intactes. Build: 8.707 pàgines | ~1 h 20 min | `699e52a1b5` |
| 28/09 | T-12 | Proves de vot fetes per l'usuari des del telèfon; **el sistema va bé** (queda la prova final amb la llista definitiva, lligada a T-01) | — | — |
| 28/09 | T-04 | Certificat SSL: **renovat el 28/09** (automàtic), vàlid fins al **27/12/2026**, SAN per `vots-cordoncillo`, `formularis`, `linuxbcn.com` i `www`; `/health` 200 als dos serveis | ~10 min | — |
| 28/09 | — | **Versió distribuïble de Taro** (branca local `distribucio`): contingut del 9bi eliminat, plantilla amb marcadors `[POSA-HI: …]`, logo de l'aplicació i README de personalització. Build net | ~1 h 30 min | `90ebcc6379`, `af8a537d6f` |
| 28/09 | — | **Codeberg**: esborrada la branca `pages` (el build vell); el compte queda a l'espera del GC. GC demanat a l'issue #2522 | ~5 min | — |
| 28/09 | — | **GoatCounter**: `/stats/` usa el total oficial de `/stats/total` (159 → 166 en viu). Documentat que l'API no exposa usuaris únics | ~20 min | `16bdec539` |
| 28/09 | — | Qui som (història): enllaços a Eva Orti, Elena Bulet i Humberto Rivas, Joan «Linux» a Nou Barris9, Mónica Rosselló treta de la taula | ~20 min | `b9cd90bd1`, `2a44e715b` |
| 28/09 | T-16 | Comentaris a les entrades amb moderació prèvia (mòdul `formularis`: avís a info@, revisió signada, publicació via l'API de GitHub) + pàgina de revisió amb l'aspecte del 9bi + paràgraf a `/privacitat/`. Desplegat al servidor i provat en real: formulari → correu → «Descarta» OK. **«Publica» pendent de provar amb el primer comentari real** | ~1 h | `d4b7c6a45`, `f4cb6d8c1` |
| 28/09 | T-25 | 399 títols en majúscules normalitzats: l'usuari els va triar un per un en una pàgina de revisió (382 propostes, 17 de propis). Només el camp `title`; les 8.708 pàgines HTML tenen les mateixes URL abans i després | ~35 min | `969076cc4` |
| 28/09 | T-17 | Botons discrets per compartir cada entrada (WhatsApp, Telegram, Facebook, correu, copia, menú del sistema al mòbil) + correcció del botó «Copia» del concurs | ~24 min | `7e5406ec6` |
| 28/09 | — | Enllaços RSS del web al feed de les entrades (`/posts/index.xml`) | ~5 min | `0cbbed841` |
| 28/09 | T-13 | Autopublicació al canal de Telegram @NouBarrisImatge: script al servidor, feed de `/posts/`, arxiu (3.008 entrades) marcat com a publicat, cron cada 30 min, prova real OK. Docs a `modules/telegram/README.txt` | ~33 min | `33d5a437d` + docs |
| 27/09 | — | `/mes-visitats/` amb el top 10 real: l'script cridava un endpoint de GoatCounter que no existeix (400) i es publicaven dades velles | ~10 min | `428593971` |
| 27/09 | — | Pàgines de gràcies dels formularis amb el disseny del web (`/contacte/gracies/`, `/incorpora-te/gracies/`) i redirecció 303 des del servidor, desplegada | ~15 min | `b1e399dd8` |
| 27/09 | T-05 | Cartell de `/concurs/votacio/` amb el text propi del 36è concurs (fora la còpia de «demostració Taro») | ~5 min | `e6346bcef` |
| 27/09 | T-04 | Avís de calendari `.ics` per a la caducitat del certificat | ~5 min | `e6346bcef` |
| 27/09 | T-03 | Consentiment RGPD al servidor (codi + proves, 9bi i Taro; proves de 9bi reparades). **Desplegat 19:20**: POST sense casella → 400 en viu | ~15 min | `e6346bcef` |
| 27/09 | — | Registre de tasques fora del `CLAUDE.md` (aquest fitxer) | ~10 min | `e6346bcef` |
| 27/09 | — | Data d'activació de la votació (01/12–15/12) i verificació del QR | 7 min | `c244a17bd` |
| 27/09 | — | Documentació, registre d'hores i sincronització | 12 min | `42c8f6c84` |
| 27/09 | — | Desplegament de la votació al servidor (BBDD buida, `/admin/obres` 200) | 8 min | `42c8f6c84` |
| 27/09 | — | Proveïdor únic: LinuxBCN a tota la documentació pública | 7 min | `42c8f6c84` |
| 27/09 | — | Protecció TLS als quatre `.htaccess` (sense bucles de 301) | 8 min | `42c8f6c84` |
| 27/09 | — | Quatre bugs reals corregits + bateria de proves | 2 h 38 min | `42c8f6c84` |
| 27/09 | — | Manual del paquet distribuïble Taro | 18 min | `42c8f6c84` |
| 27/09 | — | Llicència AGPL, llicències de tercers i avisos SPDX | 26 min | `42c8f6c84` |
| 27/09 | — | Cerca: límit de 100 resultats, tolerància 0.3 i data a cada resultat | — | `bf7f1ba12` |
| 27/09 | — | Qui som: pestanya «als mitjans», enllaç directe a cada pestanya | — | `7b592a2f5`, `c8360f4b5` |
| 27/09 | — | SEO: JSON-LD vàlid i metadades socials | — | `359d3f717` |
| 25/09 | — | Loop de tasques: seguretat i SEO | en curs (no tancat) | — |
| 25/09 | — | Pestanyes de la guia en dues files | no tancat | — |
| 25/09 | — | Avís flotant del 36è concurs | no tancat | — |
| 25/09 | — | Per què l'aplicació es diu Taro (crèdits) | 15 min | — |
| 25/09 | — | Lateral nativa del Sveltia + àlbums enllaçats al login | 20 min | — |
| 25/09 | — | Rail propi del CMS | 25 min | — |
| 25/09 | — | Pàgines fixes al CMS + peu reduït | 35 min | — |
| 25/09 | — | Miniatures al backend del CMS | 35 min | `a04d62d56` |

### Totals per dia

Els dies anteriors al 25/09 només tenen el total al registre diari (el detall hi és per blocs).

| Data | Temps | Registre |
|---|---|---|
| 02/10 | ~2 h 40 min (sessió al núvol, ~16:00–18:20) | [2026-10-02.md](2026-10-02.md) |
| 01/10 | ~3 h 08 min (matí + tarda + núvol) | [2026-10-01.md](2026-10-01.md) |
| 30/09 | ~2 h 22 min (matí ~09:28–10:40 + núvol ~17:45–18:50) | [2026-09-30.md](2026-09-30.md) |
| 28/09 | ~3 h 05 min (sessió al núvol, 08:35–11:40, inici estimat) | [2026-09-28.md](2026-09-28.md) |
| 27/09 | ~5 h 41 min (sessió 2 ~4 h 55 min + sessió 3 46 min) | [2026-09-27.md](2026-09-27.md) |
| 25/09 | ≥ 2 h 10 min (3 tasques sense tancar) | [2026-09-25.md](2026-09-25.md) |
| 22/09 | ~5 h (amb pauses) | [2026-09-22.md](2026-09-22.md) |
| 20/09 | ~1 h 17 min | [2026-09-20.md](2026-09-20.md) |
| 19/09 | ~1 h 45 min | [2026-09-19.md](2026-09-19.md) |
| 18/09 | 1 h 09 min (el registre té més sessions sense total) | [2026-09-18.md](2026-09-18.md) |
| 17/09 | 1 h 58 min | [2026-09-17.md](2026-09-17.md) |

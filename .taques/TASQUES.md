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
| T-30 | ⚪ | Repassar 6 títols massa llargs/truncats de la T-08 (acaben amb «a», «Aque», «Entrega», «part», «habilidade», «especial») | 28/09 | — | Són primers paràgrafs sencers; l'usuari els va aprovar, però caldria escurçar-los |
| T-09 | 🟡 | Enllaços d'àlbums morts (Picasa → Google Photos), autor per autor | 18/09 | — | Quan puguem. Eines a `scripts/albums_fix.py`, fitxes a `data/recuperacio/` |
| T-10 | ⚪ | Cerca: etiquetes ordenades de més a menys freqüents | 21/09 | — | |
| T-11 | ⚪ | Cerca limitada a l'autor a `/author/<slug>.html` | 24/09 | — | Baixa prioritat |
| T-14 | ⚪ | Publicació automàtica a Instagram i Facebook + enllaços al web | 18/09 | — | Mateix patró que T-13 (`modules/telegram/`: RSS de `/posts/` + `state.json` + cron) |
| T-18 | ⚪ | Auditoria d'accessibilitat | 17/09 | — | |
| T-19 | ⚪ | 5a pestanya de «Qui som»: Història de la fotografia a Nou Barris | 18/09 | — | Recerca feta, galeria en suspens |
| T-20 | ⚪ | Membres: completar els Instagram que falten | 18/09 | — | |
| T-21 | ⚪ | Seguretat CI/CD: SHA-pin de les accions, credencials fora de `deploy.sh`, 11 fitxers `.dl-*`, `modules/taro/.gitignore` | 25/09 | — | De l'auditoria del 25/09 |
| T-22 | ⚪ | Reobrir l'issue #2522 de Codeberg (quota) | 21/09 | — | **Comentari de petició de GC enviat el 28/09 20:17** (branca `pages` esborrada abans). Pendent de resposta. Text a `drafts/2026-09-27-codeberg-issue-2522-reobrir.md` |
| T-23 | ⚪ | Revisió jurídica final de l'adequació RGPD | 18/09 | — | |
| T-24 | ⚪ | Tipografia Gillius: OTF → woff2 | 18/09 | — | Opcional |
| T-26 | ⚪ | Control de fitxers del Concurs Cordoncillo (bases, històric…) | 18/09 | — | |
| T-28 | 🟡 | Staging a Codeberg (`https://linuxbcn.codeberg.page/9bi/`): els CSS es veuen trencats | 28/09 | — | **Diagnosticat (28/09)**: l'staging serveix el build vell del 24/09 fet amb l'`baseURL` de producció; l'enllaç surt `/assets/...` (sense `/9bi/`) → 404. Queda lligat a T-29 (el distribuïble nou substituirà aquest staging) |
| T-29 | 🟡 | **Publicar la versió distribuïble de Taro a Codeberg** (`linuxbcn/9bi` → `main`): la plantilla ja està feta i verificada a la branca local `distribucio` (`90ebcc6379`, `af8a537d6f`). Bloquejat pel **GC de Codeberg** (issue #2522, comentari enviat el 28/09 20:17; el compte encara marca 752,7 MiB). Quan passi: `git push origin distribucio:main` | 28/09 | — | Pla B si Codeberg no es desencalla: publicar la mateixa branca en un repo nou a GitHub |
| T-27 | ⚪ | Secció per preparar i gestionar les reunions del col·lectiu | 18/09 | — | |

### Tancades sense fer

| ID | Tasca | Data | Motiu |
|---|---|---|---|
| T-02 | Rotar `admin_secret` i `secret` de la votació | 27/09 | Decisió de l'usuari: risc acceptat, no es rota |
| T-15 | Butlletí, correu per a cada membre + genèric, i grup de correu | 28/09 | Decisió de l'usuari: el pla de correu només permet 10 comptes. Cada membre fa servir el seu correu personal i el col·lectiu es comunica (i vota) pel grup privat de Telegram. El butlletí queda aparcat: les novetats ja surten al canal públic de Telegram |

## Fetes

### Registre per tasca (des del 2026-09-25)

| Data | ID | Tasca | Temps | Commit |
|---|---|---|---|---|
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
| 28/09 | ~3 h 05 min (sessió al núvol, 08:35–11:40, inici estimat) | [2026-09-28.md](2026-09-28.md) |
| 27/09 | ~5 h 41 min (sessió 2 ~4 h 55 min + sessió 3 46 min) | [2026-09-27.md](2026-09-27.md) |
| 25/09 | ≥ 2 h 10 min (3 tasques sense tancar) | [2026-09-25.md](2026-09-25.md) |
| 22/09 | ~5 h (amb pauses) | [2026-09-22.md](2026-09-22.md) |
| 20/09 | ~1 h 17 min | [2026-09-20.md](2026-09-20.md) |
| 19/09 | ~1 h 45 min | [2026-09-19.md](2026-09-19.md) |
| 18/09 | 1 h 09 min (el registre té més sessions sense total) | [2026-09-18.md](2026-09-18.md) |
| 17/09 | 1 h 58 min | [2026-09-17.md](2026-09-17.md) |

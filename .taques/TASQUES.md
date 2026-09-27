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
| T-01 | 🔴 | **Llista definitiva d'obres de la votació** (número, títol, autor, categoria) a `[obres]` del `config.ini` del servidor; després esborrar `data.db` i reiniciar | 27/09 | **30/11** | Bloquejada: encara no tenim la llista. La votació s'obre sola l'01/12. **Preparat (27/09)**: omplir `drafts/obres-concurs-2026-plantilla.csv` → `python3 modules/votacio/tools/obres.py llista.csv -o obres.ini` (valida números repetits, `|`, categories A/B/C) → substituir **sencera** la secció `[obres]` del `config.ini` del servidor (treure la línia `rang = …`, si no les 100 obres de prova continuen) → aturar, esborrar `data.db`, arrencar i comprovar `/admin/obres` |
| T-04 | 🟠 | Certificat SSL de `vots-cordoncillo` i `formularis` (Let's Encrypt, caduca 24/12 20:47) | 27/09 | 26/11 | Avís al calendari: `drafts/avis-certificat-votacio-2026-12-24.ics` (26/11 comprovar, 17/12 urgent) |
| T-06 | 🟡 | Desactivar Blogger | 21/09 | — | En espera, decisió de l'usuari: **de moment no s'apaga**. DNS ja apunten a 9barrisimatge.org |
| T-07 | 🟡 | Editors al CMS: convidar col·laboradors amb Write, comprovar que els no-admin només veuen els seus posts i si algú ja ha iniciat el seu usuari | 21/09 | — | Quan puguem |
| T-08 | 🟡 | Títols repetits: 21 posts «Sense títol» + ~33 grups amb el mateix títol | 27/09 | — | Quan puguem |
| T-09 | 🟡 | Enllaços d'àlbums morts (Picasa → Google Photos), autor per autor | 18/09 | — | Quan puguem. Eines a `scripts/albums_fix.py`, fitxes a `data/recuperacio/` |
| T-10 | ⚪ | Cerca: etiquetes ordenades de més a menys freqüents | 21/09 | — | |
| T-11 | ⚪ | Cerca limitada a l'autor a `/author/<slug>.html` | 24/09 | — | Baixa prioritat |
| T-12 | ⚪ | Test real de vot des del telèfon (número, títol, categoria, avís legal, resultats) | 24/09 | abans de l'01/12 | Depèn de T-01 |
| T-13 | ⚪ | Telegram: canal públic unidireccional amb els posts nous | 18/09 | — | Cal token de @BotFather + `chat_id` (usuari) i un script després del build |
| T-14 | ⚪ | Publicació automàtica a Instagram i Facebook + enllaços al web | 18/09 | — | Mateix patró que T-13 |
| T-15 | ⚪ | Butlletí, correu per a cada membre + genèric, i grup de correu | 18/09 | — | Cal repensar DNS i correu |
| T-16 | ⚪ | Comentaris amb control d'spam fort | 18/09 | — | Solució per triar |
| T-17 | ⚪ | Botons per compartir a xarxes | 18/09 | — | |
| T-18 | ⚪ | Auditoria d'accessibilitat | 17/09 | — | |
| T-19 | ⚪ | 5a pestanya de «Qui som»: Història de la fotografia a Nou Barris | 18/09 | — | Recerca feta, galeria en suspens |
| T-20 | ⚪ | Membres: completar els Instagram que falten | 18/09 | — | |
| T-21 | ⚪ | Seguretat CI/CD: SHA-pin de les accions, credencials fora de `deploy.sh`, 11 fitxers `.dl-*`, `modules/taro/.gitignore` | 25/09 | — | De l'auditoria del 25/09 |
| T-22 | ⚪ | Reobrir l'issue #2522 de Codeberg (quota) | 21/09 | — | Text a `drafts/2026-09-27-codeberg-issue-2522-reobrir.md`, no enviat |
| T-23 | ⚪ | Revisió jurídica final de l'adequació RGPD | 18/09 | — | |
| T-24 | ⚪ | Tipografia Gillius: OTF → woff2 | 18/09 | — | Opcional |
| T-25 | ⚪ | CMS: normalització de títols en majúscules | 18/09 | — | |
| T-26 | ⚪ | Control de fitxers del Concurs Cordoncillo (bases, històric…) | 18/09 | — | |
| T-27 | ⚪ | Secció per preparar i gestionar les reunions del col·lectiu | 18/09 | — | |

### Tancades sense fer

| ID | Tasca | Data | Motiu |
|---|---|---|---|
| T-02 | Rotar `admin_secret` i `secret` de la votació | 27/09 | Decisió de l'usuari: risc acceptat, no es rota |

## Fetes

### Registre per tasca (des del 2026-09-25)

| Data | ID | Tasca | Temps | Commit |
|---|---|---|---|---|
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
| 27/09 | ~5 h 11 min (sessió 2 ~4 h 55 min + sessió 3 16 min) | [2026-09-27.md](2026-09-27.md) |
| 25/09 | ≥ 2 h 10 min (3 tasques sense tancar) | [2026-09-25.md](2026-09-25.md) |
| 22/09 | ~5 h (amb pauses) | [2026-09-22.md](2026-09-22.md) |
| 20/09 | ~1 h 17 min | [2026-09-20.md](2026-09-20.md) |
| 19/09 | ~1 h 45 min | [2026-09-19.md](2026-09-19.md) |
| 18/09 | 1 h 09 min (el registre té més sessions sense total) | [2026-09-18.md](2026-09-18.md) |
| 17/09 | 1 h 58 min | [2026-09-17.md](2026-09-17.md) |

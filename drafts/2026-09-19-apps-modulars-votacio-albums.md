# Suit modular de programari lliure per a associacions i escoles de fotografia

Data: 2026-09-19. Estat: **proposta per aprovar**. Autor: sessió 9 Barris Imatge (OpenCode).
Objectiu: definir, com a **mòduls independents d'un projecte de programari lliure**, les aplicacions que s'han estat dissenyant —(1) votació popular del públic d'un concurs, (2) recuperació/reconstrucció d'enllaços d'àlbum trencats i (3) migració d'un blog de Blogger— de manera que qualsevol altra associació de fotografia les pugui reutilitzar.

Principis vinculants (decidits per l'usuari, 2026-09-19): **programari lliure, mínimes dependències, segur i funcional.**

---

## 1. Per què mòduls

Cada aplicació és una **unitat autònoma** (codi, config, documentació i llicència pròpies). No comparteixen res obligatòriament: poden desplegar-se juntes o per separat, i una associació externa pot agafar només el mòdul que li convingui.

Tenen una base comuna (fitxer `README.md` de la suit + plantilles de config) però **zero acoblament** entre elles:

- **`votacio`** — vot del públic d'un concurs fotogràfic, per QR presencial. (Aquest document desenvolupa aquest mòdul; existeix un enllaç des de `content/concurs.md`.)
- **`albums`** — gestió i reconstrucció d'enllaços d'àlbum trencats d'un blog migrat (Picasa → Google Photos). Detall tècnic ja documentat a `drafts/2026-09-18-pla-recuperacio-albums.md`; aquí només se n'estructura el paquet com a mòdul.
- **`migracio`** — migració d'un blog de **Blogger** al nostre generador estàtic (Hugo + PaperMod): llegir el feed Atom, convertir HTML→Markdown, baixar/oferir imatges, escriure els posts amb front matter i organitzar-los en anys. Ja funciona a 9 Barris Imatge (`scripts/migrate_live.py`, 3.006/3.006 posts, 0 errors); es tracta de netejar-lo, parametritzar-lo i alliberar-lo com a mòdul.

Altres mòduls potencials de la mateixa suit (futur, fora d'abast ara): vegeu la llista de candidats a avaluar a la §6.

---

## 2. Mòdul `votacio` — especificació funcional

Basat en el que ja hi ha publicat a `content/concurs.md` («El vot del públic») i en les decisions registrades:

Verificades (2026-09-17/18, registrades a CLAUDE.md):
- Premi del públic: **100 €**, decidit pel públic. Recollida el 18 de desembre (lliurament de premis).
- Votació oberta de l'1 al 15 de desembre de 2026, **durant l'exposició al Casal de Barri de Prosperitat**.
- **QR únic a l'exposició**; cada obra portarà el seu **número**; en obrir la pàgina del QR, la persona indica el número de la fotografia a votar.
- **1 vot per obra i dispositiu**; identitat **anònima per dispositiu**.
- Accés **només amb QR presencial** (secret per edició, no enllaç públic indexable).
- **Testimoni firmat + registre al servidor**: els vots es guarden com a registre verificable (signat) per poder auditar el recompte.

Casos d'ús (funció mínima viable, M1; millores M2):
- M1.1 Obrir la URL del QR → pàgina que demana el número d'obra.
- M1.2 Registrar el vot (màx. 1 per obra i dispositiu).
- M1.3 Confirmació al dispositiu + avís si ja s'ha votat aquella obra.
- M1.4 Administrador: alta de l'edició (obra numerades, dates, secret QR), consulta del recompte en directe i **tancament** (congela comptadors + export).
- M1.5 Verificació pública del recompte a partir del testimoni firmat (presentar comptes o nuls publicats).
- M2 (opcional): multiedició simultània, estadístiques, text i idioma configurable (ca/es), plantilles de cartell/QR.

---

## 3. Investigació: millor forma de construir i desplegar `votacio`

### 3.1 Restriccions de partida

- Allotjament existent: **servidor de LinuxBCN → linuxbcn.com (Dinahosting)**.
- "Mínimes dependències": idealment **només llibreria estàndard** de Python (zero `pip install` en producció).
- Sense Docker (per decidir, preferència venv).
- Segur: HTTPS, secrets fora del codi, SQLite amb signatures, registre a prova de manipulacions.

### 3.2 Estat de l'allotjament a Dinahosting (investigat, pendent de confirmar al teu compte)

Fets verificats sobre Dinahosting (fonts: dinahosting.com):

- El **hosting compartit** és clarament orientat a **PHP** (versions 7.4–8.5) i bases MySQL/MariaDB. La taula de plans llista **Python** entre els llenguatges "de programación" amb versions fins a **3.13.5**, però amb la columna ambigua; com a mínim significa que Python és present en el panell d'alguns plans.
- Dinahosting té una **"Sección de Ruby y Node"** a l'ajuda del seu panel (aplicacions Ruby on Rails i Node configurades des del Panel), cosa que suggereix que el Panel gestiona llenguatges web diversos i que **és probable que hi hagi una secció Python equivalent** — cal comprovar-ho al teu compte (`panel.dinahosting.com`).
- El patró estàndard de Python en els hostings que el suporten és **WSGI via Phusion Passenger**: un directori d'app amb `passenger_wsgi.py` (punt d'entrada `application`) + `start.py` que llança l'entorn virtual. Aquest mateix patró el documenta la KB de cPanel (kb.hosting.com): **"Setup Python App" + Passenger**.
- **Fallback garantit**: **VPS Lite no gestionat** (Debian/Ubuntu/AlmaLinux, accés root, ~34 €/mes) amb una app WSGI + venv + waitress/gunicorn. Més fiable però cost extra; només si el compartit no permet Python.

### 3.3 Recomanació d'arquitectura (mòdul `votacio`)

- **App WSGI en Python, dependència única = llibreria estàndard** (`app.py` d'un sol fitxer, pur WSGI). Punt d'entrada `application(obj)` = compatible Passenger i amb qualsevol servidor WSGI.
- **SQLite** (`sqlite3` de la stdlib) com a base de dades: taula única `vots` append-only + taules `edicions` i `obres`. SQLite va perfecte per a un volum de desenes/milers de vots i elimina un servidor de BD.
- **Identitat per dispositiu sense dades personals**: el primer accés crea un ID aleatori en una **cookie HttpOnly+Secure+SameSite=Lax**; el servidor només guarda un **hash salat** (HMAC amb secret servidor) d'aquest ID. Cap IP, cap dada personal emmagatzemada → RGPD lleuger.
- **Un vot per obra i dispositiu**: constraint a la BD (UNIQUE(edicio, obre, dispositiu_hash)) + rate-limit senzill (p. ex. màx. N intents/min per IP com a heurística).
- **Testimoni firmat**: cada registre de vot emmagatzema un **xifrat HMAC-SHA256 del propi vot** (edició + obra + hash dispositiu + timestamp) signat amb secret del servidor. Recomptes i nuls es poden publicar junt amb les signatures; es pot re-verificar que la BD no s'ha manipulat.
- **Secret per edició (QR)**: la URL del QR conté un **token aleatori alt/secreció per edició** generat pel servidor. Sense el token (present físicament), la votació no s'obre. Evita que la votació quedi indexada/accessible a distància.
- **CSS/JS inline o molt petites**: una sola pàgina HTML senzilla; sense frameworks front-end (funcional i sense CDNs).

### 3.4 QR i material imprès

El QR mateix no cal generar-lo a l'app (es pot generar amb qualsevol eina lliure en el moment de preparar l'exposició). El mòdul pot incloure una ordre opcional `votacio qr <token> <numeros...>` que imprimeix el cartell amb tants QR com obres (passa a l'edició següent; no és requeriment M1).

---

## 4. Mòdul `albums` — estructura com a mòdul reutilitzable

El contingut funcional ja està definit al pla (`drafts/2026-09-18-pla-recuperacio-albums.md`). Com a mòdul independitzat:

- CLI pur (stdlib): tres ordres → `albums collect` (escaneja posts i genera corpus), `albums validate` (comprova status+nom d'àlbum dels links rebuts), `albums apply` (aplica substitucions al front matter/body i ho reporta).
- Config per repositori: quines carpetes de posts, camps (front matter vs body), patrons de «dominio mort» (Picasa, Posterous…) configurables.
- Sortides: fulls de treball per autor (CSV/MD) + informe `informe-links-trencats.md`.
- Reutilitzable per a altres blogs migrats de Blogger (els patrons Picasa/àlbums són idèntics per a qualsevol blog). Es pot executar en local (sense servidor).

---

## 5. Mòdul `migracio` — Blogger → solució pròpia

La tercera peça natural de la suit: el camí d'entrada d'una associació que encara viu a Blogger.

### 5.1 Què fa (i què ja està provat)

- Lectors del **feed Atom de Blogger** paginable (`start-index`), sense necessitat d'exportació manual: `openSearch:totalResults` per al total, `start-index&max-results=150`.
- **HTML cru → Markdown** (reutilitza el processament de `migrate_blogger.py`/`migrate_live.py`: imatges, àlbums, taules).
- Dedup segura **per URL original de Blogger, no per slug** (el slug "blog-post" es repeteix 41 cops en mesos diferents).
- Mapeig d'autor per `<author><uri>` del feed + taula d'àlies configurable (l'endi, malnoms).
- Tags suggerides a partir del vocabulari agregat del blog (marcats amb comentari HTML per revisar).
- Escriptura a `content/posts/YYYY/` amb front matter: `title, date, year, author, slug, tags, cover.image, album_url, description`.
- Resultat verificat en la nostra migració: **3.006/3.006 posts, 0 errors**, build sense col·lisions.

### 5.2 Què cal per alliberar-lo

- **Parametrització**: treure les constants específiques de 9bi (mapeig `AUTHOR_BY_URI`, vocabulari de tags propi, patrons del nostre blog) → fitxer de config del mòdul.
- **Adaptació de targeta**: avui escriu front matter i estructura pensada per al nostre Hugo; cal fer-ho configurable (plantilla del bloc de front matter, patró de carpeta per any).
- **Cura de dependències**: `markdownify` + `pyyaml` en un venv propi (`.venv-migracio`) — es manté com a eina local d'un sol ús, no com a app desplegada. Això xoca amb "mínimes dependències" i cal decidir-ho explícitament.
- El codi ja existeix i està provat end-to-end; parlem de **neteja + config + docs**, no de programar-ho des de zero.

### 5.3 Funcionalitat i factibilitat (valoració)

- **Funcionalitat**: alta per a terceres associacions (la majoria de blogs d'associacions encara són a Blogger i molts volen sortir-se'n cap a una solució lliure). Per a nosaltres ja no cal operativament (migració feta), però dona coherència a la suit: **entrar (migracio), arreglar (albums) i interactuar (votacio)** són els 3 cicles de vida d'una associació fotogràfica. Una suit amb "entrada + manteniment + eina d'activitat" és molt més atractiva de regalar que mòduls solts.
- **Factibilitat**: mitjana-alta i barata, perquè és refactor, no creació. Risc principal: la integració amb el nostre Hugo concret és molt "nostra" i cal fer-la genèrica sense trencar-la; convé fer-ho **després** d'haver estabilitzat `votacio` i `albums`, com a mòdul de documentat i consolidat, no com a prioritat.

---

## 6. Mòduls futurs a avaluar — i el vincle amb Llumàtics

**Llumàtics (llumatics.com)** és l'escola de fotografia vinculada a l'associació (Nau Bostik, la Sagrera), també allotjada per LinuxBCN. És el **primer adoptant extern natural de la suit**: les seves necessitats (agenda de tallers, inscripcions, reserves del laboratori, butlletí, l'app del positivador) generen exactament el mateix tipus de mòduls petits, lliures i funcionals que 9 Barris Imatge. També imposa un bon test de portabilitat: ha de servir un context diferent (escola, no associació) i probablement amb idiomes CA/ES/EN.

### 6.1 Mòduls que Llumàtics fa candidats naturals

| Mòdul | per a 9 Barris Imatge | per a Llumàtics | valor | factibilitat |
|---|---|---|---|---|
| `tallers` — documentació de tallers i pràctiques (objectius, material, passos, imatges) | formacions internes (concurs, història) | docència: fitxes de taller i guies de pràctica | alt | mitjà: plantilles + contingut estructurat |
| `sortides` — organització de sortides fotogràfiques (mapes, posició del sol, clima, llista d'assistents) | sortides de pràctica dels membres | sortides de «pràctica fotogràfica» | alt | mitjà-alta: APIs obertes (OpenStreetMap, dades solars, meteorologia) |
| `butlleti` | pendent al backlog | ja en té un (servei extern) | alt (RGPD, independència) | mitjà: SMTP + subscripció + arxiu; podria substituir el servei extern |
| `agenda` | esdeveniments/concurs | agenda pública de tallers (ja en té una) | mitjà-alt | mitjà: calendari + RSS/iCal |
| `inscripcions` | inscripció al concurs | inscripció als tallers | alt | mitjà: formularis + llista per edició/curs |
| `reserves-espais` | (no: el Casal és propi) | plató, laboratori, escaneig, biblioteca | mitjà | baix-mitjà: franges + bloqueig |
| `positivador` | (no aplica) | ja existeix com a webapp pròpia | alt per a la comunitat analògica | fàcil: alliberar l'existent com a mòdul |
| `notificacions` | bot de Telegram + publicació IG/FB (pendent) | novetats del blog a xarxes | mitjà | mitjà: API de cada xarxa |
| `comentaris` | pendent al backlog (control d'spam) | (sense comentaris al web) | mitjà (9bi) | mitjà-baix |
| `socis` | gestió de membres (avui `data/membres` + CMS) | (no aplica) | mitjà-alt per a terceres associacions | mitjà: cens, altes/baixes, quotes |

### 6.2 Detall dels dos primers candidats

**`tallers` (documentació de tallers i pràctiques).** Per a escoles i associacions que imparteixen formació o fan pràctiques amb material (revelat, cianotípia, gran format, laboratori). Funcionalitat: fitxes de taller amb objectius, material necessari, passos, imatges del resultat i guies de pràctica enllaçades; llistat i cerca; es pot publicar com a secció del web o com a document intern.

**`sortides` (organització de sortides fotogràfiques).** Per a associacions que organitzen sortides de pràctica o de projecte: proposar un punt de trobada sobre un **mapa (OpenStreetMap)**, calcular **la posició del sol** per a la data escollida (hora d'alba/posta, hora daurada i hora blava, orientació del sol al lloc), mostrar **la previsió meteorològica** (font lliure/oberta) i portar **la llista d'assistents**. Tot amb dades obertes i sense serveis tancats.

La regla d'incorporació segueix sent: **un mòdul s'afegeix quan té un adoptant real** (9 Barris Imatge o Llumàtics) que el necessiti; no s'anticipa cap desenvolupament fins que el necessiti algú.

---

## 7. Principis comuns de la suit (aplicats a tots els mòduls)

| Principi            | Pràctica concreta |
|---|---|
| **Programari lliure** | Llicència per decidir amb l'usuari (proposta: **AGPL-3.0**; alternativa EUPL-1.2 o MIT segons preferència de difusió). Codi a Codeberg (ja s'hi treballa) en repositori públic. |
| **Mínimes dependències** | Python stdlib per `votacio` (0 `pip` en producció); stdlib per `albums` (no hi ha cap dependència externa). `migracio` és l'única excepció justificada: `markdownify` + `pyyaml` en venv propi, com a eina local d'un sol ús (vegeu §5.2). Només un virtualenv buit + Python del servidor. |
| **Segur** | HTTPS; secrets per variables d'entorn (mai al repo); cookies HttpOnly/Secure/SameSite; hashing de dispositius; HMAC per als testimonis; SQL parametritzat; registre de respostes a límits (rate limit). |
| **Funcional** | M1 mínim viable desplegable de veritat; config simple en YAML; idioma i textos per fitxer (ca per defecte); README amb guia pas a pas per a una associació aliena. |

---

## 8. Estructura proposada del repositori

```
9bi-apps/                       # nom orientatiu (per decidir)
├── LICENSE                     # una per tot el repo
├── README.md                   # què és la suit, com s'usa, llicència, contacte
├── config.example.yml          # exemple arrel (org, idioma, domini...)
└── modules/
    ├── votacio/
    │   ├── app.py              # app WSGI (stdlib) — M1
    │   ├── schema.sql          # DDL SQLite
    │   ├── config.example.yml  # edició, dates, secret, obres
    │   ├── templates/          # plantilles minúscules (inline)
    │   ├── README.md           # guia d'instal·lació i desplegament
    │   └── tools/ qr.py        # (opcional, M2) generador de QR/impressió
    ├── albums/
    │   ├── collect.py, validate.py, apply.py   # CLI stdlib
    │   ├── config.example.yml
    │   └── README.md
    └── migracio/
        ├── migrate.py                          # CLI: feed Blogger → posts
        ├── config.example.yml                  # mapeig d'autors, targeta, etc.
        ├── requirements.txt                    # markdownify, pyyaml (venv propi)
        └── README.md
```

Cada mòdul funciona **sense el repo sencer**: una associació pot copiar `modules/votacio/` i tenir la votació, i ignorar `albums` si no la necessita.

---

## 9. Desplegament previst (pilot 9 Barris Imatge)

1. Verificar al panel de Dinahosting si el pla actual permet crear una app Python (secció d'aplicacions / llenguatges). Si sí → Passenger WSGI amb venv.
2. Si no → VPS Lite (Debian) + app WSGI + HTTPS (certificat gratuït) → subdomini `vots.linuxbcn.com` o camí `/votacio/`.
3. Config de l'edició 2026 (nov–des): obres numerades, finestra 1–15 des, secret QR imprès.
4. Prova pilot interna set. abans de l'obertura (1 des) amb un QR real al Casal.
5. Obertura, monitoratge, **tancament** (15 des a la nit) i export del recompte amb testimonis.

---

## 10. Fases

- **Fase 0** — Aprovació d'aquest document (marcs de l'apartat 12).
- **Fase 1** — Muntar el repositori `9bi-apps` a Codeberg (públic, amb llicència escollida), README + esquelet de mòduls.
- **Fase 2** — Implementar `votacio` M1 (app WSGI + SQLite + HMAC + secret QR + registre/admin), amb tests senzills en local.
- **Fase 3** — Implementar `albums` com a CLI (reutilitzar resultats del pla de recuperació d'àlbums).
- **Fase 4** — Desplegar `votacio` a Dinahosting (via Python o VPS Lite) i executar la prova pilot.
- **Fase 5** — Retorn a l'equip: traduir textos (ca/es), documentar README per a terceres associacions, penjar les dues apps a la suit.
- **Fase 6** (opcional, després) — Refactor de `migracio` (neteja dels migradors actuals → mòdul configurable). Baixa prioritat, no bloqueja res.
- **Fase 7** (llarg termini) — Avaluar i, si hi ha adoptant real, construir els mòduls futurs de la §6 (`tallers`, `sortides`, `butlleti`, `agenda`, `inscripcions`, `reserves-espais`, `positivador`, `notificacions`, `comentaris`, `socis`). Res es construeix sense adoptant.

---

## 11. Riscos i punts pendents de verificar

- **Pendent**: confirmar a `panel.dinahosting.com` si el pla de hosting suporta Python/WSGI (el més probable segons la taula de llenguatges, però cal validar-lo al compte real).
- **Cost**: si cal VPS Lite (~34 €/mes) s'ha d'aprovar; alternativa: provar primer al hosting compartit.
- **Secret del QR**: l'exposició és un entorn físic obert; si algú fotografia el QR i el comparteix, es podria votar a distància. Mitigació: token per edició vigent només en la finestra, rate limit, i revisió de signatures en tancar (l'auditoria és la que dona confiança, més que el bloqueig).
- **Cicle de vida del dispositiu**: un mateix mòbil pot votar cada obra 1 cop; qui vulgui "repetir" pertocarà el rate limit i serà visible al registre.
- **Dependència del temps**: l'edició 2026 té data límit de tancament (15 des 23:59). El desplegament s'ha de fer amb marge (nov).

---

## 12. Decisions pendents d'aprovació

- [ ] Aprovat el concepte de **suit modular** (3 mòduls independents + futurs) com a **programari lliure** públic.
- [ ] Aprovada la **llicència** (proposta: **AGPL-3.0**; alterna EUPL/MIT) i el nom del repositori (`9bi-apps` o similar) a **Codeberg**.
- [ ] Aprovada l'arquitectura de `votacio` (WSGI stdlib + SQLite + HMAC + secret QR; M1 mínim viable).
- [ ] Aprovat **verificar el pla de Dinahosting** abans de decidir entre hosting compartit-Passenger i VPS Lite (i el cost si n'hi ha).
- [ ] Aprovada la Fase 2 (implementar `votacio` M1) i la Fase 3 (`albums` CLI) un cop acceptat aquest document.
- [ ] Aprovat **incloure `migracio` com a mòdul** (Fase 6, opcional, de baixa prioritat) i acceptar l'excepció de dependències (`markdownify`/`pyyaml` en venv propi).
- [ ] Aprovat **considerar Llumàtics com a primer adoptant extern** i mantenir `tallers`/`sortides`/`butlleti`/etc. com a candidats a avaluar (Fase 7), sense crear-los fins que hi hagi adoptant real.
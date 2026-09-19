# Mòdul `votacio` — pla de desenvolupament (prioritat 1)

Data: 2026-09-19. Estat: **proposta per aprovar**. Autor: sessió 9 Barris Imatge (OpenCode).
Base: `drafts/2026-09-19-apps-modulars-votacio-albums.md`.

Decisions de l'usuari per a aquesta iteració:
- **`votacio` és la prioritat absoluta**: cal tenir-la desplegada i provada per al concurs (finestra 1–15 des 2026).
- **Restricció a la ubicació de l'exposició**: com més restrictiu millor, però **opcional i configurable per geolocalització**.
- **1 vot per dispositiu per defecte** (configurable).
- **Registre de dades opcional** — RGPD!! — «per dispositiu» (és a dir, identificador per dispositiu emmagatzemat de forma no personal + cap dades externes innecessàries).
- **Alternativa per a qui no té telèfon**.
- Reaprofitable per a altres associacions: **màxim de possibilitats configurables**.
- **i18n** (CA per defecte, però es pot configurar ES/EN).

---

## 1. Investigació (fonts verificades, 2026-09-19)

### 1.1 Geofencing (restricció per ubicació) — conclusions

**Fets verificats:**
- La Geolocation API del navegador (W3C, Candidate Recommendation 2026-03-26) dona lat/lon/accuracy (95% confiança, en metres) amb `enableHighAccuracy`, **només en context segur (HTTPS)** i **només si l'usuari atorga permís** (diàleg del navegador).
- El GPS no funciona bé o gens en interiors (NIST: testes en 5 edificis grans; investigació acadèmica: GPS perdut a l'entrar en un edifici; WiFi indoor 5–15 m, amb calibracions). **El Casal de Barri de Prosperitat és un interior** → GPS poc fiable dins l'edifici.
- Sense permís de l'usuari o sense resposta (> timeout), no hi ha posició. Això **bloquejaria votants legítims** si el geofence fos dur.
- La posició és **dada de caràcter personal** (RGPD): la seva recollida requereix consentiment i minimització (opinions AEPD sobre localització: base jurídica = consentiment exprés, informació prèvia, drets de revocació). **No s'ha d'emmagatzemar**: només comprovar i descartar.

**Disseny recomanat (geolocalització OPcional per fer-la configurable):**
- 3 modes per edició/concurs:
  - `off` — sense geolocalització (per defecte per a tests i votacions en línia no presencials).
  - `soft` — s'intenta la posició (timeout ~8 s); si és dins del radi (configurable, per defecte 500 m al voltant de les coordenades del lloc) el vot s'accepta normal; si no hi ha posició o està fora, **es deixa votar però es marca el vot** com a `geo:none`/`geo:out` al registre perquè en l'auditoria es puguin revisar (recompte normal + informe separat).
  - `hard` — només s'accepta amb posició dins del radi; els que no poden donar posició queden fora (no recomanat en interiors; es pot activar per a votacions a l'aire lliure).
- La confiança DOsP del geofence mai substitueix el **QR presencial**: el QR només existeix físicament a l'exposició, que és la prova de presència forta. Geolocalització = capa addicional *soft* per dissuadir i auditar, no la porta.
- **No es guarda cap coordenada**; la comprovació es fa al navegador (JS) o al servidor sobre el resultat `in/out`, i el registre només emmagatzema `geo:OK`. Màxima minimització (RGPD).
- **Anti-trampa nota**: la geolocalització del navegador és signable/forçable (un expert pot falsificar-la), com tot client-side. Per això és capa de dissuasió + auditoria, i el vot continua sent anònim per dispositiu.

### 1.2 Qui no té telèfon → alternativa inclusiva

Requisit real i freqüent a una exposició de barri. Solució per parell d'implementació baixa i robusta:

- **Opció A (recomanada): vot per paper.** Urna física a l'exposició amb paperetes numerades (mateixos números d'obra). Recompter manual i suma al recompte final. El mòdul no necessita res especial: el recompte digital + papereta és la dada final; s'hi pot afegir una ordre `votacio tally` que importi el recompte de paper com a entrades `paper` per tenir una sola xifra.
- **Opció B: tauleta/portàtil quiosc** cedit per l'associació a la sala. Problema: el límit per dispositiu faria que els 100 visitants usessin la mateixa tauleta → 1 sola obra votable. Per tant: si hi ha quiosc, ha de tenir un **mode quiosc** que habilita un flux «per torn» (el personal o un codi de torn per torn); complica la privacitat i l'anti-frau. **No recomanat com a via principal**; paper és més senzill, més barat i 100% inclusiu.
- **Opció C: assistència del personal amb un mòbil corporatiu** i política «1 obra per telèfon» — es barreja molt fàcilment amb els vots personals i afegeix risc. Descartada.

**Decisió proposada**: implementar el paper com a alternativa oficial (documentada), opcional per configuració (`paperVotes: true/false` + ordre d'import). El mòdul manté el «1 vot per obra i dispositiu» com a regla digital.

### 1.3 RGPD — registre de dades «per dispositiu»

- **Identificador per dispositiu, NO personal**: el primer accés crea un ID aleatori en cookie HttpOnly+Secure+SameSite; el servidor emmagatzema només una **signatura HMAC-SHA256** (secret del servidor) d'aquell ID. Cap IP, cap UA, cap dada personal emmagatzemada. Això **no és dada personal** (no identifica una persona física) i és la pràctica de *privacy by design*.
- **Registre de dades opcional**: configurable `collectData: none|contact` (ex.: correu o telèfon voluntari per a un sorteig). **Si s'activa, és tractament de dades personals** → exigir: consentiment exprés (casella sense premarcar), informació prèvia (responsable, finalitat, base = consentiment, destinataris, drets), RSA per edició, i funció d'export/borrat (drets ARSULIPO).
- La **geolocalització**, si s'activa, s'ha de tractar dins el consentiment (finalitat de seguretat anti-frau) i **no emmagatzemar-la**.
- Documentació per a l'associació adoptant: plantilla de clàusula informativa + apartat a la política de privacitat.

### 1.4 On hostejar-ho — comparativa (2026-09-19)

| Opció | Cost | Fiabilitat (15 dies) | Assola els requisits | Comentari |
|---|---|---|---|---|
| **Dinahosting VPS Lite no gestionat** (LinuxBCN, preferència) | ~34 €/mes | Alta | Sí (python + venv + WSGI + HTTPS) | Propi, autoallotjat, reprogramable; és l'opció «nosalts» del projecte |
| Dinahosting hosting compartit (si permet Python/Passenger) | inclòs al pla actual | Mitjana-alta | Depèn de confirmar al panel | Cal verificar `panel.dinahosting.com`; patró WSGI → Passenger |
| **PythonAnywhere free** | 0 € | Mitjana (1 web app, caduca als ~1 mes si és el nou pla «1 month expiry», 100 CPU-s/dia) | Parcial (WSGI sí; outbound restringit; sense domini propi al free) | Bé per a tests/períodes curts; la finestra de 15 dies hi cap; poca portabilitat de domini |
| **Render free** | 0 € | Mitjana (aturada per inactivitat 15 min, cold-start 30–50 s) | Parcial (WSGI sí, PostgreSQL però no cal) | Cold-start dolent per a un QR d'exposició (el públic no espera) |
| Railway free | crèdit $5 (no realment permanent) | — | — | No lliure permanent; descartat |
| Fly.io | ~2 $/mes | Alta | Sí (containers) | Docker → trenca la regla «mínimes deps» del context Dinahosting |

**Recomanació**: **Desplegament principal a Dinahosting** (VPS Lite si el compartit no permet Python), i de **documentar PythonAnywhere i Render** com a plantilles alternatives al README per a associacions sense VPS (amb l'advertència de cold-start/caducitat). L'app serà 100% portàtil: WSGI stdlib + SQLite = qualsevol d'aquests hostings la pot servir.

### 1.5 i18n i reutilització (màxim de possibilitats)

L'app ha de venir amb totes les cadenes en un fitxer de text pla per idioma (`i18n/ca.txt`, `es.txt`, `en.txt`), seleccionable per configuració i/o `Accept-Language`. Defecte: ca. Això la fa útil a tota associació, no només a nosaltres.

Reutilització — llistat de possibilitats que el disseny ha de permitir (taula config):
- múltiples **edicions** (una exposició pot tenir 2 concursos a la vez, o votació en curs + històric);
- votació **presencial QR** (secret per edició) o **en línia oberta** (sense secret: per a concursos a distància);
- límit de vots per dispositiu (per defecte 1 per obra; configurable 0 = sense límit, o N);
- geolocalització off/soft/hard (configurable per edició);
- recollida de dades opcional (none/contact);
- vot únic global vs. una votació per obra;
- textos i idiomes configurables.

---

## 2. Abast del M1 (mínim viable) — tancat

Funcionalitats que **sí** fan falta per a l'edició 2026 i per a la bondat del projecte:

1. App WSGI (stdlib) amb `application()` — funcionament a Passenger/WSGI i test local.
2. Esquema SQLite: `edicions(id, nom, dates, secret_edicio, mode_geo, radi_geo, lat_geo, lon_geo, collect_data, vot_limit, activa)`, `obres(id, edicio_id, numero, titol?, autor?, cat?)`, `vots(id, edicio_id, obre_id, dispositiu_hash, signatura, ts, geo_estat)` append-only.
3. ID de dispositiu per cookie (HttpOnly/Secure/SameSite) + HMAC hash.
4. Portal vist per al votant (amb el número d'obra): ca (es/en per config).
5. Límit «1 vot per obra i dispositiu» via constraint UNIQUE(edicio, obre, dispositiu_hash) + rate-limit senzill.
6. Geofence soft/hard/off opcional (JS en el navegador per a `soft`; servidor per a `hard`) sense emmagatzemar coordenades.
7. Registre firmat de cada vot (HMAC) + verificar (script d'auditoria).
8. Admin (passadís per secret d'admin): estat en viu per obra/dia, tancar edició (congela) i exportar recompte + signatures per publicar.
9. Ordre `votacio qr` que imprimeix els codis (o fitxer PDF) amb l'enllaç+token — única dependència acceptable traduïble.
10. Importació de vots de paper (`votacio tally --paper`) opcional.
11. i18n (cadenes per fitxer, ca/es/en).
12. README amb guia d'instal·lació i desplegament (Dinahosting + PythonAnywhere + Render), ideals per a terceres associacions.

**Fora de M1**: multiedició simultània completa, estadístiques avançades, panell gràfic, comentaris, app mòbil nativa. Es deixen per M2 si hi ha adoptants.

---

## 3. Estructura de fitxers del mòdul (M1)

```
modules/votacio/
├── app.py               # app WSGI stdlib (routes: /v/<token>, /admin, /tancar, /export)
├── passenger_wsgi.py    # punt d'entrada Passenger (importa application)
├── schema.sql           # DDL (taules edicions, obres, vots)
├── config.example.ini   # edició 2026: nom, dates, límit, mode_geo, radi, secrets, idioma
├── i18n/
│   ├── ca.ini
│   ├── es.ini
│   └── en.ini
├── tools/
│   ├── qr.py            # genera URL/QR (qrcode dev opcional o qrencode)
│   ├── tally.py         # recompte final + import de paper
│   └── audit.py         # verifica les signatures d'un export
├── templates/           # HTML inline a app.py (sense fitxers)
└── README.md
```

---

## 4. Pla de treball (sequència per apurar el temps)

Per ordre d'execució, per a tenir-ho tot desplegat a novembre:

1. **[Aprovat]** document + llicència + nom de repo.
2. **Config + esquelet** (`config.example.yml`, `schema.sql`, estructura). *Clau: definir bé els modes off/soft/hard i els camps d'edició aviat.*
3. **app.py nucli** (formularis, vots, límit, HMAC firmat, cookie).
4. **Geofence** (JS `soft` + check server `hard`).
5. **Admin**: estat en viu, tancament, export amb signatures.
6. **i18n** (ca/es/en) — cadenes en 3 fitxers.
7. **Test local** complet (curl/selenium bàsic) sobre SQLite temporal.
8. **Curi QR** (`tools/qr.py`) — o decidir una ordre que generi l'enllaç per al tauler d'un generador extern.
9. **Desplegament**: confirmar Dinahosting (panel) o VPS Lite; base en HTTPS; prova pilot.
10. **Pilot al Casal** (set. 2026): QR real, tauleta + paper, testejar geofence, tests de càrrega mínima.
11. **README** de reutilització + plantilles alternatives d'allotjament.

*Els punts 2–7 es poden fer en seqüència en una mateixa tanda de treball i no depenen d'allotjament → comencem pel codi mentre es resol el hosting.*

---

## 5. Decisions aprovades per l'usuari (2026-09-19)

1. **Geolocalització**: el mòdul surt **off per defecte global** (reutilitzable en línia); a l'edició 2026 s'activa **soft** amb radi 500 m (es deixa votar sense posició però es registra `geo_estat` per auditar).
2. **Alternativa sense telèfon**: **vot per paper** (urna física, paperetes numerades) amb import al recompte (`votacio tally --paper`). Descartat el quiosc amb tauleta.
3. **Registre de dades (RGPD)**: per a l'edició 2026, **`collectData: none`** (sense correu/telèfon); el mòdul queda preparat per a `contact` (consentiment exprés) en edicions futures.
4. **Hosting**: **primer Dinahosting hosting compartit** (Passenger WSGI si el panel ho permet); **VPS Lite només si falla**. Llicència **AGPL-3.0 proposada** (pendent confirmar quan es pari el repo) i nom `9bi-apps` orientatiu.
5. **Detall d'arquitectura**: la config del mòdul serà **INI (configparser, stdlib)** en lloc de YAML, per mantenir 0 `pip` en producció (el YAML exigiria `pyyaml`). `tools/qr.py` genera les URL i, si hi ha `qrcode` (dev) o `qrencode` al sistema, produeix els QR; en cas contrari imprimeix la URL per a qualsevol generador de QR lliure. El temps i les coordenades van en hora local del servidor (Europe/Madrid).

## 6. Decisió pendent (no bloquejant)

- Llicència final i nom del repo a Codeberg (es poden decidir quan es pari).
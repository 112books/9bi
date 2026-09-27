# votació · vot del públic d'una exposició

Aplicació WSGI amb la llibreria estàndard de Python (**sense cap dependència
en producció**) per recollir el vot del públic d'una exposició amb un únic
QR present.

Idea: una persona amb un dispositiu escaneja el QR (que depèn d'un
`secret_token` per edició), escriu el número de l'obra que li agrada i vota.
Un vot per obra i per dispositiu (testimoni signat amb HMAC). Opcional:
geolocalització configurable (off / soft / hard) i, si una edició ho
requereix, recollida de dades de contacte amb consentiment explícit.

**Sense telèfon?** Vot en paper: urna física i comptatge amb
`python3 tools/tally.py --paper paper.csv`.

## Decisions de configuració (què triar i per què)

- **Geofencing** `off` | `soft` | `hard`
  - `off`: no es demana ubicació.
  - `soft`: s'accepta el vot i es marca `geo=out` si és lluny.
  - `hard`: un vot llunyà **es rebutja** (`403`) i el missatge recorda
    d'activar la ubicació.
- **Punt i radi**: `lat` / `lon` / `radi` defineixen on es pot votar. Amb
  `hard` posa un radi raonable (habitualment 200–1000 m). **Comprova el punt
  amb una font abans de cada edició**: si les coordenades no són les del lloc
  on es fa la votació, tots els vots es rebutgen. Un error d'1,5 km en la
  latitud passa completament per alt.
- **L'obra es tria escrivint el número** imprès al costat de la fotografia,
  no amb un desplegable: el servidor valida el número contra la llista
  d'obres (`msg_invalid_obra`).
- **Un sol vot per obra i dispositiu** (`vot_limit = 1`) per tota l'edició.
  `vot_limit = 0` = **mode obert**, sense límit de vots per obra i
  dispositiu (per a proves); la votació anterior de la mateixa obra se
  substitueix (`INSERT OR REPLACE`, la taula té
  `UNIQUE (edicio_id, obra_id, dispositiu_hash)`).
- **`revote_minutes`** (per defecte `0`) obre una finestra de re-vot en
  minuts quan `vot_limit > 0`: passats N minuts es pot tornar a votar la
  mateixa obra.
- **Dades personals**: `collect_data = none` no demana res. Les
  coordenades **mai** no es desen: només una etiqueta `ok|out|none` i la
  distància, calculada al navegador.
- **Sincronització de la config**: `connect()` aplica els camps de
  configuració de l'edició (`nom`, dates, `mode_geo`, `lat`, `lon`, `radi`,
  `collect_data`, `vot_limit`, `activa`) en cada arrencada i en deixa
  registre al log. Canviar-los al `config.ini` té efecte en reiniciar, sense
  haver d'esborrar `data.db`. **No toca les obres ni els vots**: la llista
  d'obres només es carrega en la creació de la base.
- **Ubicació i mòbils**: alguns navegadors (iOS) no mostren el permís fins
  que hi ha un toc de l'usuari. Per això hi ha el botó **«Activar la
  ubicació»**, que torna a demanar-la i s'amaga quan s'aconsegueix. La pàgina
  calcula la distància al punt i la mostra; si la precisió és de més de
  250 m avisa que cal activar l'«ubicació precisa»; si es rebutja el vot, el
  missatge diu la distància real.
- **Idiomes**: ca (per defecte), es, en — seleccionats per l'Accept-Language.
- **Marca i enllaços** (`url_home`, `url_edicio`, `url_privacitat`,
  `entitat`, `subtitol`) i el **lloc on es vota** (`lloc_votacio`) surten de
  la configuració: res del mòdul depèn d'una entitat concreta.

## Estructura

```
config.example.ini   # plantilla de configuració
config.ini           # configuració real (gitignored, mai al repositori)
schema.sql           # esquema SQLite (edicions, obres, vots)
i18n/{ca,es,en}.ini  # textos de la interfície
app.py               # app WSGI (stdlib; zero dependències)
passenger_wsgi.py    # punt d'entrada per a Phusion Passenger
serve.py             # servidor WSGI filat (stdlib), per a producció sense pip
tools/qr.py          # genera el QR de la votació per al cartell
tools/tally.py       # recompte (digitals + paper opcional)
tools/audit.py       # verifica signatura HMAC i duplicats
deploy/start.sh      # arrenca el procés amb pidfile i log
deploy/stop.sh       # l'atura
deploy/watchdog.sh   # el reinicia si ha mort (cridat pel cron)
deploy/htaccess      # proxy del docroot del subdomini → 127.0.0.1:8301
```

## Rutes

- Votar: `GET /v/<secret_token>` (formulari) → `POST /v/<secret_token>`.
- Admin (amb `admin_secret`): `/admin/` (recompte), `/admin/export` (CSV
  signat), `/admin/tancar`, `/admin/logout`.
- Health: `GET /health`.

## Desplegament

1. `cp config.example.ini config.ini` i omple `[general]` (`secret`,
   `admin_secret`, `app_name`, `entitat`, `url_*`) i `[edicio]`.
2. Genera secrets: `python3 -c "import secrets;print(secrets.token_urlsafe(24))"`.
3. La base de dades i les obres de `[obres]` es creen **sols** al primer
   accés (el primer `connect()`); si vols tenir-ho fet abans d'arribar gent:
   `python3 -c "import app; app.connect(app.load_config()).close()"`.
4. Servidor de prova: `python3 app.py 8010` → http://127.0.0.1:8010

**Opció A — amb Passenger** (cPanel i molts altres): copia la carpeta al
directori d'aplicacions i apunta a `passenger_wsgi.py`.

**Opció B — procés d'usuari darrere d'Apache** (hosting sense Passenger ni
CGI funcional; verificat en allotjaments d'aquest tipus):

- Codi a `~/apps/votacio/` (fora del docroot).
- `deploy/start.sh` engega `python3 serve.py 8301` (filat, només stdlib) amb
  pidfile i log al mateix directori. Vés `TARO_DIR` / `TARO_PORT` si el codi
  viu en un altre lloc o un altre port.
- Docroot `~/www/votacio/` amb només el `.htaccess` de `deploy/htaccess`:
  deixa passar `/.well-known/` (repòtex del certificat) i fa proxy de tot a
  `127.0.0.1:8301`. **Edita el domini i el port del fitxer abans de pujar-lo.**
- Cron (`crontab -e`): `@reboot` + cada 5 min `deploy/watchdog.sh`.

**Punt delicat del TLS en aquests hostings**: si un frontal acaba el TLS
davant d'Apache, Apache creu que és HTTP. El `.htaccess` de `deploy/htaccess`
ja ho cobreix amb les **dues** condicions (`%{HTTPS} !=on` **i**
`X-Forwarded-Proto !=https`), de manera que redirigeix només quan la
petició és http de debò, estigui on acabi el TLS, i no hi ha bucle de 301.
Si al teu hosting el TLS arriba directament a Apache, no cal tocar res.

- **Amb proxy, `REMOTE_ADDR` és 127.0.0.1** per a tothom: el límit de
  peticions actua com a límit global del lloc. Les defenses reals són el CSRF,
  el testimoni HMAC i el geofence.
- **Tipus de lletra**: `@font-face` apunta a `/fonts/…`. Si el teu web ja en
  serveix, no cal copiar-los; altrament, posa'ls al docroot o al directori
  estàtic del teu lloc.
- Fitxers sensibles: `config.ini` a 600 amb els secrets reals; scripts a
  755. El `start.sh` fa `umask 077` perquè `data.db` i els logs neixin
  amb 600.
- Abans d'obrir l'edició: posa la llista d'obres reals a `[obres]`, les
  dates reals a `[edicio]` i esborra `data.db` (es re-crea amb la
  configuració nova al primer trànsit). ⚠️ **esborrar `data.db` esborra també
  els vots**: fes-ho abans de l'exposició, mai després.

La BD (SQLite) es crea al camí de `[db]`. Fes còpies de seguretat periòdiques.

## Seguretat

- Cap secret al codi: tot a `config.ini` (gitignored) o variables d'entorn.
- **CSRF per petició** (HMAC del secret + id de dispositiu).
- Els vots s'enregistren amb **signatura HMAC-SHA256** sobre (edició, obra,
  hash de dispositiu, timestamp) per detectar manipulació; `tools/audit.py`
  la verifica.
- Límit de peticions per IP en memòria.
- A HTTPS, `ssl = true` afegeix `Secure` a les cookies.
- `data.db` i `config.ini` **fora del docroot**.

## RGPD

- Amb `collect_data = none` no es demana cap dada de contacte.
- Geolocalització: només es registra l'etiqueta `ok|out|none`. Les
  coordenades es comparen al navegador i **no es desen mai**.
- Si una edició activa `collect_data = contact`, el consentiment s'ha de
  demanar explícitament a cada petició i qui administra l'edició ha d'esborrar
  les dades quan es tanca.

## Tools

```
python3 tools/qr.py --out votacio.png            # QR del cartell
python3 tools/tally.py                           # recompte digital
python3 tools/tally.py --paper paper.csv         # + vots en paper
python3 tools/audit.py                           # integritat/signatures
```

El format de `paper.csv` és una obra per línia (número), o `obra,titol`.

## Llicència

AGPL-3.0-or-later. Vegeu el fitxer `LICENSE` a l'arrel del repositori. Cap
dependència de tercers en producció.

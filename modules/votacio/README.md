# votacio · vot del públic del Concurs Cordoncillo

Mòdul M1 de la suite modular. Aplicació WSGI amb la llibreria estàndard de
Python (sense cap dependència en producció) per recollir el vot del públic
d'una exposició amb un únic QR present.

Idea: una persona amb un dispositiu escaneja el QR (que depèn d'un
`secret_token` per edició), tria una obra i vota. Un vot per obra i per
dispositiu (HMAC-cookie anònima). Opcional: geolocalització configurable
(off / soft / hard) i registre d'una dada de contacte amb consentiment RGPD
per a edicions que ho requereixin.

## Decisions de configuració (edició 2026)

- Geofencing: `hard` (radi 500 m al voltant del Casal de Barri de
  Prosperitat). En `hard` un vot llunyà **es rebutja** (`403`) i el missatge
  recorda d'activar la ubicació; en `soft` s'accepta però es marca `geo=out`.
  `off` sense geolocalització.
- L'obra es tria **escrivint el número** imprès al costat de la fotografia,
  no amb un desplegable: el servidor valida el número contra la llista
  d'obres (`msg_invalid_obra`).
- Sense mòbil? **Vot en paper**: urna física + comptatge amb
  `python3 tools/tally.py --paper vots_paper.csv`.
- Dades personals: `collect_data = none` (no es demana res; les
  coordenades **mai** es desen, només una etiqueta `ok|out|none`).
- Idiomes: ca (per defecte), es, en — seleccionats per l'Accept-Language.

## Estructura

```
config.example.ini   # plantilla de configuració
config.ini           # configuració real (gitignored)
schema.sql           # esquema SQLite (edicions, obres, vots)
i18n/{ca,es,en}.ini  # textos de la interfície
app.py               # app WSGI (stdlib; zero dependències)
passenger_wsgi.py    # punt d'entrada per a Phusion Passenger
tools/qr.py          # genera el QR de la votació per al cartell
tools/tally.py       # recompte (digitals + paper opcional)
tools/audit.py       # verifica signatura HMAC i duplicats
serve.py             # servidor WSGI filat (stdlib), per a producció sense pip
deploy/start.sh      # arrenca el procés amb pidfile i log
deploy/stop.sh       # l'atura
deploy/watchdog.sh   # el reinicia si ha mort (cridat pel cron)
deploy/htaccess      # proxy del docroot del subdomini → 127.0.0.1:8301
```

## Desplegament ràpid

1. `cp config.example.ini config.ini` i omple els camps de `[general]`
   (`secret`, `admin_secret`, `base_url`, `ssl = 1`) i de `[edicio]`.
2. Genera secrets: `python3 -c "import secrets;print(secrets.token_urlsafe(24))"`.
3. Creaciona la BD i carrega obres: `python3 -c "import app;c=app.connect(app.load_config());app.inietit(c);c.close()"`.
4. Servidor de prova: `python3 app.py 8010` → http://127.0.0.1:8010
5. **Desplegament real (Dinahosting, verificat el 2026-09-26)**. Aquest host
   **no té Passenger** ni CGI utilitzable; el patró que funciona és
   **procés d'usuari + proxy** (el mateix que altres apps del mateix host):

   - Codi a `~/apps/vots-cordoncillo/` (fora del docroot).
   - `deploy/start.sh` engega `python3 serve.py 8301` (filat, només stdlib)
     amb pidfile i log (`serve.log`) al mateix directori.
   - Docroot `~/www/vots-cordoncillo/` amb només el `.htaccess` de
     `deploy/htaccess`: redirigeix l'arrel al formulari, deixa passar
     `/.well-known/` (renovació Let's Encrypt) i fa proxy de tot a
     `127.0.0.1:8301`.
   - Cron (`crontab -e`): `@reboot` + cada 5 min `deploy/watchdog.sh`.
   - **Atenció**: Dinahosting termina el TLS davant d'Apache; Apache creu
     que és HTTP. Per això el redirect de l'arrel és HTTPS explícit i el
     proxy envia `X-Forwarded-Proto: https` (konsento-ho fa igual).
   - Amb el proxy, `REMOTE_ADDR` és 127.0.0.1 per a tots: el límit de
     peticions actua com a límit global del lloc (configurat a 120/min
     al `config.ini`); les defenses reals són CSRF + testimoni HMAC +
     geofence. El límit de login d'admin (10/min) és global, també.
   - Fitxers sensibles: `config.ini` a 600 amb secrets reals; el cron i els
     scripts, a 755. `umask 077` al `start.sh` perquè `data.db` i els logs
     neixin amb 600.
   - Abans de l'exposició: posar la llista d'obres real a `[obres]`, la
     finestra `data_inici`/`data_fi` reals i esborrar `data.db` (es re-crea
     amb la configuració nova al primer trànsit).
6. Per provar: `curl https://vots-cordoncillo.linuxbcn.com/health` → `ok`;
   el formulari a `/v/cordoncillo-2026`; l'admin a `/admin/` (login a
   `/admin/login` amb `admin_secret`).

La BD (SQLite) es crea al camí de `[db]`. Fes còpies de seguretat periòdiques.

## Ús

- Votar: `GET /v/<secret_token>` (formulari) → `POST /v/<secret_token>`.
- Admin (protegit per `admin_secret`): `/admin/` (recompte),
  `/admin/export` (CSV signat), `/admin/tancar`. Accés a `/admin/logout`.
- Health: `GET /health`.

## Seguretat

- Cap secret al codi: tot a `config.ini` (gitignored) o variables d'entorn.
- CSRF per petició (HMAC del device secret + id de dispositiu).
- Les vots s'enregistren amb signatura HMAC-SHA256 sobre els camps
  (edició, obra, hash de dispositiu, timestamp) per detectar manipulació.
- Límit de peticions per IP en memòria (40 req/min).
- A HTTPS `ssl = 1` afegeix `Secure` a les cookies.

## RGPD

- `collect_data = none` (edició 2026): no es demana cap dada de contacte.
- Geolocalització: només s'enregistra l'etiqueta `ok|out|none`; les
  coordenades es comparen a client i no es desen mai.
- Si alguna edició futura activa `collect_data = contact`, el consentiment
  s'ha de demanar de manera explícita per a cada petició; el mòdul només el
  referencia entre les votacions i l'exportació, i qui administra l'acabada
  de guardar ha d'esborrar-ho (tasca `tools/tally.py --net` en preparació).

## Tools

```
python3 tools/qr.py --out votacio.png            # QR del cartell
python3 tools/tally.py                           # recompte digital
python3 tools/tally.py --paper paper.csv         # + vots en paper
python3 tools/audit.py                           # integritat/signatures
```

El format de `paper.csv` és una obra per línia (número), o `obra,titol`.

## Llicència

Programari lliure. Llicència proposada: AGPL-3.0 (pendent de confirmar).

Aquest mòdul no té cap dependència de tercers en producció.
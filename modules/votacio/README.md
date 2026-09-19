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

- Geofencing: `soft` (radi 500 m al voltant del Casal de Barri de
  Prosperitat). En `soft` un vot llunyà **s'accepta però es marca `geo=out`**;
  en `hard` es rebutja (`403`). `off` sense geolocalització.
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
```

## Desplegament ràpid

1. `cp config.example.ini config.ini` i omple els camps de `[general]`
   (`secret`, `admin_secret`, `base_url`, `ssl = 1`) i de `[edicio]`.
2. Genera secrets: `python3 -c "import secrets;print(secrets.token_urlsafe(24))"`.
3. Creaciona la BD i carrega obres: `python3 -c "import app;c=app.connect(app.load_config());app.inietit(c);c.close()"`.
4. Servidor de prova: `python3 app.py 8010` → http://127.0.0.1:8010
5. Producció (Dinahosting/cPanel amb Passenger): apunta el teu domini al
   directori del mòdul; `passenger_wsgi.py` s'hi carrega sol.

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
Taro Photo App — programari lliure per a col·leccions de fotografies
====================================================================

QUÈ ÉS
------
Taro és un conjunt de petites aplicacions web per a col·leccions,
associacions i agrupaments de fotografia: recollir el vot del públic d'una
exposició, rebre els formularis del web per correu i publicar el web
automàticament.

Aquesta carpeta és **la versió distribuïble**: no conté ni dades, ni
nombres, ni correus, niadreces, ni configuració de cap entitat. Els fitxers
`config.example.ini` són plantilles amb valors d'exemple per llegir; el que
serveix de veritat (`config.ini`) no s'hi inclou mai.

Què conté
----------
    app.py               Router WSGI: munta els tres mòduls sota /taro/
    passenger_wsgi.py    Punt d'entrada per a Phusion Passenger
    autopublica/         Publica el web en arribar un push al repositori
    formularis/          Rep formularis del web i els envia per correu
    votacio/             Vot del públic d'una exposició amb QR

Cada mòdul té la seva pròpia documentació (`README.md` o `README.txt`) amb
la configuració i el desplegament pas a pas. **Llegeix la del mòdul que
instal·lis.**

REQUISITS
---------
- **Python 3.6 o superior.** Res més: cap dependència de tercers, ni
  `pip install`, ni base de dades per instal·lar. (`votacio` usa la biblioteca
  `sqlite3`, que ve amb Python.)
- Un servidor web: Apache amb `mod_rewrite` (només si vols el patró de
  procés + proxy), o qualsevol hosting amb Phusion Passenger.
- Per a `autopublica`: `git` i el lloc on allotjar el web.
- Per a `formularis`: un compte de correu sortient (SMTP) del teu hosting.

DUES MANERES DE DESPLEGAR
-------------------------

**A) El bundle sencer amb el router.** Un sol procés, un sol punt de
muntatge, tres aplicacions:

    navegador ──https://el-teu-domini/taro/votacio/…
                              └─ router (app.py) → votacio/
                            /taro/formularis/…   → formularis/
                            /taro/autopublica/…  → autopublica/
                            /taro/health         → ok

Amb Passenger: apunta el domini (o el directori `public_html/taro`) a
aquesta carpeta; Passenger carrega `passenger_wsgi.py`, que exposa el
`application` d'`app.py`. Sense Passenger: fes servir els `deploy/start.sh`
del mòdul que vulguis darrere d'un proxy.

`/taro/health` respon `ok` **sense passar per cap mòdul**: serveix per
saber si el router viu, encara que no tinguis cap mòdul instal·lat.

**B) Cada mòdul per separat.** Tots tres es poden instal·lar sols, amb el
seu propi `config.ini`, la seva base de dades i el seu port, sense el
router ni res més del bundle. És la opció si els vols a subdominis
diferents o en servidors diferents.

CONFIGURACIÓ
------------
Cada mòdul té el seu `config.example.ini`; copia'l a `config.ini` al
servidor i omple'l. Els secrets (claus, contrasenyes, tokens) **no s'han de
pujar mai al repositori**: el `.gitignore` del bundle ja hi és, per
seguretat, però la responsabilitat és de qui instal·la.

Genera secrets de debò, no de manual:

    python3 -c "import secrets; print(secrets.token_urlsafe(32))"

Proves
------
Abans de posar res en producció, proves-ho tot en local:

    votacio/      python3 app.py 8010        # servidor de proves
    formularis/   cp config.example.ini config.ini && python3 provar.py
    autopublica/  (health) i una entrega de webhook de prova

`formularis/provar.py` arrenca un servidor real, substitueix l'SMTP per una
funció que es queda els correus i comprova l'origen, el camp trampa, la
injecció de capçalera, el retall de camps, el límit de peticions i
l'error quan falta la contrasenya. Acaba amb `RESULTAT: OK`.

SEGURETAT — REGLES QUE DONEN PER FETS
-------------------------------------
- Els fitxers amb secrets (`config.ini`, `data.db`) **fora del document
  root**. El codi, també.
- `config.ini` amb permisos `600`, scripts amb `755`.
- Comprova sempre que `allowed_origins` (formularis) i el `secret` /
  `admin_secret` (votació) estan posats: en defecte, el servei rebutja o
  s'atura, però no ho donis per bo.
- Els tres mòduls tenen límit de peticions, control d'origen o CSRF, i
  secrets de la configuració. La documentació de cada mòdul en detalla el
  cas.

LICÈNCIA
--------
AGPL-3.0-or-later (fitxer `LICENSE` a l'arrel del repositori). Si
modifiques el programari i el poses en marxa com a servei per a tercers,
has d'oferir-ne el codi font. Els textos de la interfície (i18n) són
també AGPL. Cap dependència de tercers en producció.

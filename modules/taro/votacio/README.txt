QUÈ ÉS
------
Mòdul "votació" de Taro: aplicació web per recollir el vot del públic d'una
exposició o concurs.

Com funciona: al local de l'exposició hi ha un cartell amb un codi QR. En
sortir-hi, el telèfon obre la pàgina de votació, s'escriu el número de la
fotografia i es compta un vot. Un sol vot per obra i dispositiu, i el
dispositiu es reconeix amb un testimoni signat (HMAC), de manera que no es
pot tornar a votar la mateixa obra des del mateix telèfon. Sense telèfon, el
vot es fa en paper a una urna i es compta amb l'eina de retorn.

Què hi ha dins
--------------
app.py                 Aplicació WSGI (Python, només biblioteca estàndard).
                       Rutes: /v/<token> (vot), /admin/ (recompte,
                       export CSV, tancar edició), /health.
schema.sql             Esquema de la base de dades SQLite.
config.example.ini     Model de configuració: entitat i enllaços, dates de
                       l'edició, obres (número|títol|autor|categoria), punt,
                       radi i mode de geolocalització, token secret del QR.
                       S'ha de copiar com a config.ini AL SERVIDOR.
                       config.ini NO s'ha de pujar mai al repositori.
passenger_wsgi.py      Punt d'entrada per a Phusion Passenger.
serve.py               Servidor WSGI filat per a hostings sense Passenger.
i18n/                  Textos de la interfície en català, castellà i anglès.
tools/qr.py            Genera el codi QR del cartell.
tools/tally.py         Recompte final; amb --paper compta els vots en paper.
tools/audit.py         Verifica que no hi hagi vots duplicats ni manipulats.
deploy/                Arrencada, aturada, vigilant i .htaccess del proxy.

La documentació completa (configuració, geofencing, seguretat, RGPD i
desplegament pas a pas) és al README.md del mateix directori.

Si el directori desapareix del servidor, el web no es trenba (el vot és un
enllaç extern), però es perd el recompte de la votació.

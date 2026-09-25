QUÈ ÉS
-------
Mòdul "votació" del Col·lectiu 9 Barris Imatge: aplicació web per al
vot del públic del Concurs fotogràfic Josep Antón Cordoncillo.

Com funciona: al Casal de Barri de Prosperitat hi ha un cartell amb un
codi QR. En sortir-hi, el telèfon obre la pàgina de votació, es tria el
número de la fotografia i es compta un vot. Un sol vot per obra i
dispositiu, i el dispositiu es reconeix amb un testimoni signat (HMAC),
de manera que no es pot tornar a votar la mateixa obra des del mateix
telèfon. Sense telèfon, el vot es fa en paper a una urna i es compta
amb l'eina de retorn.

Què hi ha dins
--------------
app.py                 Aplicació WSGI (Python, només biblioteca estàrdia).
                       Rutes: /v/<token> (vot), /admin/ (recompte,
                       export CSV, tancar edició), /health.
schema.sql             Esquema de la base de dades SQLite.
config.example.ini     Model de configuració: dates de l'edició, obres
                       (número|títol|autor|categoria), radi i mode de
                       geolocalització, token secret del QR.
                       S'ha de copiar com a config.ini AL SERVIDOR.
                       config.ini NO s'ha de pujar mai al repositori.
passenger_wsgi.py      Punt d'entrada per a Phusion Passenger.
i18n/                  Textos de la interfície en català, castellà i anglès.
tools/qr.py            Genera el codi QR del cartell.
tools/tally.py         Recompte final; amb --paper compta els vots en paper.
tools/audit.py         Verifica que no hi hagi vots duplicats ni manipulats.

Estat
-----
El mòdul està escrit i provat, però la votació encara NO està
desplegada: cal l'hospedatge (un subdomini del compte linuxbcn.com amb
Python), el fitxer config.ini amb les dates reals i el token del QR, i
el llistat definitiu d'obres (número - títol - categoria).

Si el directori desapareix del servidor, el web no es trenca (el vot és
un enllaç extern), però es perd el recompte de la votació.

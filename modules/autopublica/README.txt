QUÈ ÉS
-------
Mòdul "autopublica" del Col·lectiu 9 Barris Imatge: aplicació web per
publicar alhora un article del web i la seva fitxa a Taro Photo App
(programari lliure per a col·leccions de fotografies).

Què fa: rep una sol·licitud amb la informació de l'article, crea el
fitxer Markdown dins del repositori del web i el registra a la base de
dades de Taro, de manera que l'article apareix al web i a l'exposició
virtualsense tornar a introduir les dades dues vegades.

Què hi ha dins
--------------
app.py               Aplicació WSGI (Python, només biblioteca estàndria).
config.example.ini   Model de configuració amb el repositori, la branca,
                    el servidor i les credencials. config.ini NO s'ha de
                    pujar mai al repositori.
passenger_wsgi.py    Punt d'entrada per a Phusion Passenger.
i18n/                Textos de la interfície.
tools/deploy.sh      Publica al servidor de Pages: FA SERVIR config.ini
                    per obtenir el token, i mai no el mostra per pantalla
                    ni el deixa a la URL.

Seguretat
---------
Les credencials només es llegeixen del servidor. A l'agost de 2026 es va
revisar el codi i es van treure els tokens dels registres i de les URLs,
perquè quedessin exposats al registre del servidor i a l'historial del
navegador.

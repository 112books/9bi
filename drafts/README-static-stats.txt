Aquest document descriu el directori static/stats/ del repositori. És aquí perquè Hugo copia tot el que hi ha dins de static/ al domini públic i no hi pot haver cap documentació dins.

QUÈ ÉS
-------
El tauler d'estadístiques del web: quantes persones visiten el col·lectiu
i quins articles són els més llegits. És la pàgina /stats/.

Què hi ha dins
--------------
index.html         La pàgina del tauler, amb gràfics (Chart.js). Té
                   noindex: no té sentit que un cercador la trobi ni la
                   publiqui.
analytics.json     Les dades de visites que hi ha dibuixades. NO s'han
                   d'editar a mà: es generen soles a cada desplegament
                   amb el programa scripts/fetch_9bi_analytics.py, que
                   consulta el comptador GoatCounter del col·lectiu.

De què depèn
------------
Del secret GOATCOUNTER_API_KEY, que és al servidor (GitHub Actions) i no
al repositori. Si es per el secret, el web es publica igual però aquest
tauler deixa d'actualitzar-se i mostra les dades de l'última vegada.

Dades i privacitat
------------------
GoatCounter no posa galetes ni deixa identificar els visitants amb un
codi persistent. Per això les xifres són aproximades: un nombre alt de
visites des del mateix equip pot comptar com una sola.

Es pot esborrar? El tauler, sí (el web no en depèn). El fitxer
analytics.json, no: el codi el llegeix i el tauler es quedaria buit.

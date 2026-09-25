QUÈ ÉS
-------
Taro Photo App: programari lliure per a col·leccions i associacions de
fotografies. Publicat a https://linuxbcn.com/taro/ i en fase beta.

Aquesta còpia del codi viu dins del mateix repositori que el web 9 Barris
Imatge perquè tots els programes del col·lectiu es publiquin junts i
comparteixin la mateixa instal·lació de Python al servidor.

Què conté
----------
app.py               Aplicació WSGI principal de Taro (Python, només
                     biblioteca estàndria).
passenger_wsgi.py   Punt d'entrada per a Phusion Passenger.
autopublica/        Còpia del mòdul d'auto-publicació (crea l'article al
                     web i el registra a Taro alhora).
formularis/         Còpia del servei de formularis del web.
votacio/            Còpia del servei de votació del concurs.

Per què hi ha còpies i no enllaços
----------------------------------
Cada mòdul és una aplicació independent amb la seva pròpia configuració
(config.ini), les seves traduccions i la seva base de dades, i es pot
desplegar sola. Les còpies permeten que Taro les executi al seu propi
servei sense dependre d'un directori extern del repositori del web. Quan
es modifica un mòdul, cal copiar els fitxers nous també dins de Taro.

Configuració
------------
Taro necessita config.ini (copia de config.example.ini) al servidor.
Els secrets no s'han de pujar mai al repositori.

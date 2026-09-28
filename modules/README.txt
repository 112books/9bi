QUÈ ÉS
-------
Aplicacions pròpies del Col·lectiu 9 Barris Imatge, separades del web
estàtic. Són programes en Python (WSGI) que necessiten un servidor: el
web estàtic de GitHub Pages no els pot allotjar.

Cada aplicació té el seu propi directori, la seva configuració
(config.ini, que no es puja mai al repositori) i el seu README amb
explicacions i instruccions de desplegament.

QUÈ HI HA
---------
formularis/   Rep els missatges dels formularis del web i els envia per
              correu. Subdomini: formularis.linuxbcn.com
              (carpeta www/formularis al servidor del compte
              linuxbcn.com, perquè 9barrisimatge.org és només correu i
              el web és a GitHub Pages).
votacio/      Vot del públic del Concurs Cordoncillo per codi QR al
              Casal de Barri de Prosperitat. Desplegada al subdomini
              vots-cordoncillo.linuxbcn.com.
autopublica/  Publica el web sol quan hi ha un push al repositori
              (ja no cal per a la publicació real: el web es publica amb
              GitHub Actions, que fa el build i el desplegament).
telegram/     Publica cada entrada nova del web al canal públic de
              Telegram @NouBarrisImatge (cron cada 30 min, 1 h de
              marge). No és una aplicació web: és un script al
              servidor (~/apps/telegram).
taro/         Taro Photo App, el programa de gestió i exposició de
              fotografies, amb còpies dels tres mòduls anteriors. És la
              versió que es distribueix a altres col·leccions: no hi ha
              ni dades ni configuració de 9 Barris Imatge dins.

On són les documentacions
-------------------------
- Mòduls en producció: el README.txt de cada carpeta.
- Versió distribuïble: modules/taro/README.txt (manual del bundle) i el
  README de cada mòdul dins de modules/taro/.

Per què Python i no un servei de tercers
----------------------------------------
Per no dependre de FormSubmit ni de cap empresa externa per rebre els
missatges, i per tenir tot el programari en programari lliure, al
servidor que ja tenim i que podem mirar i modificar nosaltres mateixos.

QUÈ ÉS
-------
Aplicacions pròpies del Col·lectiu 9 Barris Imatge, separades del web
estàtic. Són programes en Python (WSGI) que necessiten un servidor: el
web estàtic de GitHub Pages no els pot allotjar.

Cada aplicació té el seu propi directori, la seva configuració
(config.ini, que no es puja mai al repositori) i el seu README.txt amb
explicacions i instruccions de desplegament.

QUÈ HI HA
---------
formularis/   Rep els missatges dels formularis de Contacte i
              "Incorpora't" i els envia per correu a
              info@9barrisimatge.org. Subdomini: formularis.linuxbcn.com
              (carpeta www/formularis al servidor del compte
              linuxbcn.com, perquè 9barrisimatge.org és només correu i
              el web és a GitHub Pages).
votacio/      Vot del públic del Concurs Cordoncillo per codi QR al
              Casal de Barri de Prosperitat. Encara no desplegada.
autopublica/  Publica un article al web i el registra a Taro Photo App
              alhora.
taro/         Taro Photo App, el programa de gestió i exposició de
              fotografies, amb còpies dels tres mòduls anteriors.

Per què Python i no un servei de tercers
----------------------------------------
Per no dependre de FormSubmit ni de cap empresa externa per rebre els
missatges, i per tenir tot el programari en programari lliure, al
servidor que ja tenim i que podem mirar i modificar nosaltres mateixos.

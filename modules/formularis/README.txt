README.txt — mòdul "formularis" del Col·lectiu 9 Barris Imatge
============================================================

QUÈ ÉS
------
Aplicació web petita (Python, només biblioteca estàndria) que rep els
dos formularis del web — Contacte i "Incorpora't" — i envia el missatge
per correu a info@9barrisimatge.org.

Per què existeix: fins al 2026 els formularis passaven per FormSubmit
(formsubmit.co), un servei de tercers. Aquest mòdul fa el mateix amb el
correu del nostre propi hosting i no depèn de cap servei exterior.

No hi ha cap base de dades: les dades passen per la memòria i surten
cap a un correu. No es desen enlloc (ni al servidor ni al repositori).


ON VIU AL SERVIDOR (important: el codi NO és al document root)
---------------------------------------------------------------
    ~/apps/formularis/          codi i configuració
    ~/www/formularis/           document root: només el .htaccess del proxy

El document root conté exactament dos coses: .htaccess i .well-known
(aquest darrer per al repòtex del certificat). El codi viu a ~/apps per
xar, perquè el web no el pugui servir ni downloadable.

Servidor: linuxbcn0@vl28359.dinaserver.com (82.98.166.123). No tocar mai
els comptes veïns konsento ni naubostik: no són nostres.


COM ES FA SERVIR (no és Passenger)
-----------------------------------
Dinahosting no té Passenger ni CGI funcional en aquest host. El patró que
funciona és un procés d'usuari darrere d'Apache:

    navegador ──HTTPS──> Apache (acaba el TLS)
                          ├─ .htaccess: si no és https, 301 a https
                          └─ proxy [P,QSA,L] ──> 127.0.0.1:8302 (serve.py)

Per tant, per arrencar el servei NO cal el panell ni Passenger:

    ~/apps/formularis/deploy/start.sh      arrenca (si no ja és en marxa)
    ~/apps/formularis/deploy/stop.sh       atura
    ~/apps/formularis/deploy/watchdog.sh   revisa i arrenca si cal

Al crontab de l'usuari ja hi ha (no s'ha de tornar a afegir):

    @reboot sleep 20 && ~/apps/formularis/deploy/start.sh
    */5 * * * * ~/apps/formularis/deploy/watchdog.sh >> .../watchdog.log 2>&1

El watchdog és el que fa que el servei torni sol si es mor, i l'@reboot
el que fa que torni després d una reiniciada del servidor.


CONFIGURACIÓ
------------
config.ini viu NOMÉS al servidor, a ~/apps/formularis/config.ini, amb
 permisos 600 i NO s'ha de pujar mai al repositori. Es crea a partir de
config.example.ini. Les línies que importen:

    [general] allowed_origins = https://9barrisimatge.org
    [general] site_url = https://9barrisimatge.org/
    [smtp] host = 9barrisimatge-org.correoseguro.dinaserver.com
    [smtp] port = 465
    [smtp] user = info@9barrisimatge.org
    [smtp] password = (la contrasenya real del compte)

allowed_origins és OBLIGATORI: sense aquesta línia el mòdul rebutja tots
els enviaments amb 403.

Detall del hostname de SMTP: el correu s'envia pel servidor que indica el
panell de Dinahosting, que té certificat vàlid. No s'ha de fer servir
mail.9barrisimatge.org encara que apunti a la mateixa IP: el seu
certificat no correspon al hostname i la connexió TLS fallaria.

Detall de la contrasenya: es llegeix amb raw=True i el fitxer es llegeix
amb interpolation=None, perquè una contrasenya amb el caràcter % no
doni error de ConfigParser.


COM ES PROVA
------------
1. Comprovar que el servei respon:

       curl -s -o /dev/null -w '%{http_code}\n' \
         https://formularis.linuxbcn.com/health     # ha de dir 200

2. Enviar un missatge de prova:

       curl -i -X POST https://formularis.linuxbcn.com/envia/contacte \
         -H "Origin: https://9barrisimatge.org" \
         -d "nom=Prova" -d "email=prova@example.org" \
         -d "assumpte=Prova" -d "missatge=Missatge de prova" \
         -d "consentiment=Sí"

   Ha de respondre 200 i el correu ha d'arribar a info@9barrisimatge.org.

3. Comprovar que l'origen es filtra: el mateix curl sense la capçalera
   Origin ha de respondre 403. Això és el que impedeix que un altre lloc
   enviï formularis en nom nostre.


SEGURETAT (per què està fet així)
---------------------------------
- Origen: només accepta POST des del domini del web (capçalera Origin; si
  no hi és, mira el Referer). Un formulari estàtic no pot signar
  capçaleres, de manera que l'origen declarat és el que es pot comprovar.
- Honeypot: camp ocult _honey; si el bot l'omple, el missatge es descarta
  sense resposta d'error (no li donem informació al bot).
- Límit de peticions per minut i per IP.
  NOTA: per la configuració actual el límit és de 20/min per a tot el
  servei (no per IP), perquè darrere del proxy d'Apache el REMOTE_ADDR
  és sempre 127.0.0.1. S'ha decidit deixar-ho així: per a dos formularis
  de contacte és suficient i fa de fre contra l'abús. Si algun dia es
  vol per IP real, cal llegir el darrer valor de X-Forwarded-For (l'únic
  que posa el nostre Apache i que el client no pot falsejar).
- Cos de la petició limitat (MAX_COS), per no permetre enviaments enormes.
- Només s'envien els camps coneguts de cada formulari; la resta es
  descarta. Els texts es netegen de caràcters de control i el Reply-To
  només s'afegeix si l'adreça és vàlida (evita injecció de capçaleres).
- Els errors del servidor de correu no es mostren al navegador: només al
  registre del servidor (per no filtrar informació).
- Errors i reinicis van a ~/apps/formularis/serve.log i watchdog.log.


CORREU SORTINT
--------------
El servidor envia directament per SMTP, sense passar per cap servei de
tercers. A més, el compte signa amb DKIM (registre TXT a
default._domainkey.9barrisimatge.org) i el SPF del domini apunta a la
IP del servidor, de manera que el correu arriba a la bandeja d'entrada
en lloc de a spam.

El peu de cada correu inclou el text legal (responsable, dades tractades,
finalitat, base legal, destinataris, conservació, drets i AEPD), que és
el que demana la LOPDGDD.


SI MAI ES VOL ESBORRAR AQUEST MÒDUL
-----------------------------------
Cal tornar primer els dos formularis del web a un servei que funcioni, o
el web es quedarà sense formulari de contacte. I cal retirar també el
proxy i el crontab del servidor.

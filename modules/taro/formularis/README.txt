README.txt — DIRECTORI IMPORTANT: NO L'ESBORRIU
=================================================

QUÈ ÉS AQUEST DIRECTORI
-----------------------
Mòdul "formularis" del Col·lectiu 9 Barris Imatge: una aplicació web
petita que rep els missatges dels dos formularis del web (Contacte i
"Incorpora't") i els envia per correu electrònic a info@9barrisimatge.org.

Per què existeix: fins al 2026 els formularis passaven per FormSubmit
(formsubmit.co), un servei de tercers. Aquest mòdul ho fa tot amb el
correu del nostre propi hosting i no depèn de cap servei exterior.

ON S'HA DE PUJAR AL SERVIDOR
-----------------------------
Aquest directori S'HA DE COPIAR al servidor, a la carpeta del subdomini
formularis.linuxbcn.com:

    www/formularis/

Si el directori del servidor es diu www/formularis i aquí el mòdul es
diu formularis, el servidor rebrà els mateixos fitxers amb un altre nom.
NO L'ESBORRIU ni el buidis: el formulari de contacte deixarà de funcionar.

QUÈ HI HA DINS
--------------
app.py               Aplicació WSGI (Python, només biblioteca estàndria).
                     Rutes: GET /health  i  POST /envia/<formulari>
passenger_wsgi.py   Punt d'entrada per a Phusion Passenger (el servidor
                     de Python del hosting).
config.example.ini   Model de configuració. S'ha de copiar com a
                     config.ini AL SERVIDOR i omplir-hi l'usuari i la
                     contrasenya del correu. config.ini NO s'ha de pujar
                     mai al repositori.
i18n/               Textos de les pàgines de resposta, en català, castellà
                     i anglès. Fitxers .ini senzills, un text per línia.

COM ES CONFIGURA I ES PROVA
----------------------------
1. Subir els fitxers a www/formularis/.
2. Crear config.ini (a partir de config.example.ini) amb:
     [smtp] user = info@9barrisimatge.org
     [smtp] password = (la contrasenya real del compte de correu)
     [general] allowed_origins = https://9barrisimatge.org
   allowed_origins és OBLIGATORI: sense aquesta línia el mòdul rebutja
   tots els enviaments.
3. Registrar l'aplicació Python al panell del hosting
   (Servidores > Otras aplicaciones) indicant com a executable WSGI
   aquest mateix directori.
4. Comprovar que respon:  https://formularis.linuxbcn.com/health
   Ha de retornar "ok".

PROVAR UN ENVIOAMENT DES DE LA CONSOLA
---------------------------------------
curl -i -X POST https://formularis.linuxbcn.com/envia/contacte \
  -H "Origin: https://9barrisimatge.org" \
  -d "nom=Prova" -d "email=prova@example.org" \
  -d "assumpte=Prova" -d "missatge=Missatge de prova"

HA DE RESPONDRE 200 I ARRIBAR UN CORREU A info@9barrisimatge.org.
Sense la capçalera Origin ha de respondre 403: això és el que
impedeix que un altre lloc enviï formularis en nom nostre.

SEGURETAT (per què està fet així)
---------------------------------
- Origen: només accepta POST des del domini del web (capçalera Origin;
  si no hi és, mira el Referer). Un formulari estàtic no pot signar
  capçaleres, de manera que l'origen declarat és el que es pot comprovar.
- Honeypot: camp ocult _honey; si el bot l'omple, el missatge es
  descarta sense resposta d'error (no li donem informació al bot).
- Límit de peticions per minut i per IP.
- Només s'envien els camps coneguts de cada formulari; la resta es
  descarta. Els texts es netegen de caràcters de control i el Reply-To
  només s'afegeix si l'adreça és vàlida.
- Els errors del servidor de correu no es mostren al navegador: només
  al registre del servidor (per no filtrar informació).

Si algun dia es vol esborrar aquest mòdul del servidor, cal tornar
primer els dos formularis del web a un servei que funcioni (FormSubmit
o un correu directe), o el web es quedarà sense formulari de contacte.

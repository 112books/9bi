formularis — servei de formulari per correu
==========================================

QUÈ ÉS
------
Aplicació web petita (Python, **només biblioteca estàndria**, zero
dependències en producció) que rep els formularis d'un web i envia el
contingut per correu a l'adreça que tu configuris.

Per què existeix: serveis com FormSubmit (formsubmit.co) són de tercers i
no sempre entreguen. Aquest mòdul fa el mateix amb el correu del teu propi
hosting i no depèn de cap servei exterior.

**No hi ha cap base de dades.** Les dades passen per la memòria del procés i
surten cap a un correu. No es desen enlloc: ni al servidor, ni al repositori.

RUTES
-----
| Mètode | Ruta                  | Què fa                                   |
|--------|-----------------------|------------------------------------------|
| GET    | `/health`             | Respon `ok`. Per a monitors i balancejadors |
| POST   | `/envia/<formulari>`  | Rep i envia el formulari                 |
| GET    | `/`                   | Pàgina d'informació del servei           |
| altres | —                     | 404                                      |

Els formularis són els que vulguis: cada secció `[formularis.<nom>]` de la
configuració en crea un. Sense cap secció, hi ha els dos de per defecte
(`contacte` i `incorpora-te`) amb els camps de sempre.

CONFIGURACIÓ
------------
Copia `config.example.ini` a `config.ini` i omple'l. **`config.ini` no s'ha
de pujar mai al repositori** (ja és al `.gitignore`).

    [general]
    app_name        Nom que surt al títol de les pàgines del servei
    default_lang    ca | es | en   (per defecte: idioma del navegador)
    rate_limit      peticions per minut i IP (0 = sense límit)
    allowed_origins dominis autoritzats a enviar, separats per comes
                    (ex.: https://exemple.org,https://www.exemple.org).
                    Buit = es rebutja tot (millor per començar).
    destinatari     adreça on arriba tot (si el formulari no en té cap)
    site_url        URL del web: la pàgina de confirmació hi torna
    url_privacitat  URL de la política de privacitat. Si es deixa buit es
                    construeix com site_url + /privacitat/

    [legal]         dades que surten al peu de cada correu (RGPD/LOPDGDD)
    entitat         nom de l'entitat responsable
    adreca          adreça postal
    correu          adreça de contacte amb la gent
    corresponsalia  qui més tracta les dades (proveïdor d'hosting, de correu…)
    aepd            nom i web de l'agència de protecció de dades

    [smtp]
    host, port, ssl servidor de correu sortint (465 amb ssl, 587 amb STARTTLS)
    user            usuari del compte de correu
    password        contrasenya. Millor al sistema com a variable
                    d'entorn FORMULARIS_SMTP_PASSWORD; si és al config, es
                    llegeix en mode «crud» perquè un «%» no faci fallar res
    from            adreça remitent (per defecte, la de user)
    from_name       nom que es veu al client de correu

    [destinataris]
    <formulari>     adreça on arriba cada formulari. **Obligatori**: si un
                    formulari no té adreça, el procés no arrenca.

    [formularis.<nom>]
    camps           camps acceptats, separats per comes
    assumpte        text fix de l'assumpte del correu
    prefix_assumpte si = hi afegeix davant el valor del camp «assumpte»
    finalitat       per què es tracten les dades ( apareix al correu)

Per què és obligatori `destinataris`: sense adreça on enviar, el mòdul
s'atura en comptes d'admetre la pèrdua de missatges en silenci.

CONTROL DE L'ORIGEN (llegeix-abans de fer res)
----------------------------------------------
A cada enviament es comprova l'cabçalera `Origin` (i si no hi ha, el
`Referer`) contra `allowed_origins`. Si no hi ha coincidència: **403**, i no
s'envia cap correu. Amb `allowed_origins` buit es rebutja tot, de manera que
fins que l'omplis el servei no accepta res.

A més:
- **limitador per IP** (`rate_limit`); encendir 429 en passar-se.
- **camp trampa** `_honey`: si ve omplert, es respon 200 però **no s'envia
  cap correu** (el bot no ho sap).
- **llista blanca de camps**: només s'accepten els del formulari.
- **retall a 2.000 caràcters per camp** i neteja de caràcters de control.
- **cabecalera Bcc a un altre correu**: es rebutja amb 400.
- `Reply-To` només si el correu del remitent és vàlid.

Per poder respondre el correu, l'usuari que escriu ha de poder deixar la
seva adreça. Això no és un problema: qui rep el correu ja és el remitent
del mateix servidor. El que **no** fa el mòdul és adreçar la resposta a
ningú que no sigui el remitent del correu.

INSTAL·LACIÓ
------------
**Opció A — amb Passenger** (cPanel, DreamHost i molts altres):
copia la carpeta al directori d'aplicacions i fes que apunti a
`passenger_wsgi.py`. Aplica-li un `chmod +x` i prou. El hosting s'encarrega
d'arrencar-la.

**Opció B — procés d'usuari darrere d'Apache** (hosting sense Passenger ni
CGI funcional, com alguns hostings compartits):

    navegador ──HTTPS──> Apache (acaba el TLS)
                          ├─ .htaccess: si no és https, 301 a https
                          └─ proxy [P,QSA,L] ──> 127.0.0.1:8302 (serve.py)

El document root només ha de contenir `deploy/htaccess` i `.well-known`
(per al repòtex del certificat). **El codi viu fora del document root**
(per exemple a `~/apps/formularis/`), perquè el web no el pugui servir ni
descarregar:

    cp -r a/quest/modul ~/apps/formularis
    cp ~/apps/formularis/config.example.ini ~/apps/formularis/config.ini
    $EDITOR ~/apps/formularis/config.ini        # omple secrets i destinataris
    cp ~/apps/formularis/deploy/htaccess ~/www/formularis/.htaccess
    ~/apps/formularis/deploy/start.sh           # arrenca

Si el codi no viu a `~/apps/formularis`, digues-ho als scripts amb variables
d'entorn:

    TARO_DIR=/opt/meu/formularis TARO_PORT=8302 ./deploy/start.sh

Gestió amb `deploy/start.sh` (ja arrenca si és en marxa), `deploy/stop.sh`
i `deploy/watchdog.sh`. Al cron, cada 5 minuts:

    */5 * * * * $HOME/apps/formularis/deploy/watchdog.sh >/dev/null 2>&1
    @reboot $HOME/apps/formularis/deploy/start.sh

Abans de pujar el `.htaccess`, **tria el domini** (el fitxer posa
`exemple.org` com a exemple) i el port del procés.

**Opció C — darrere del router del bundle** (`modules/taro/app.py`):
no cal res més; el mòdul queda a `/taro/formularis/` i hereta el mateix
patró de proxy del router.

PROVES
------
`provar.py` arrenca un servidor de proves real (wsgiref), substitueix
l'SMTP per una funció que es queda els correus i comprova el comportament
sense tocar res extern:

    cp config.example.ini config.ini     # i omple [destinataris]
    python3 provar.py

Comprova: `/health`, arrel, 404, origen vàlid i origen rebutjat, camp
trampa, formulari desconegut, camps buits, correu invàlid, injecció de
capçalera amb CRLF, retall de camps, límit de peticions i error quan falta
la contrasenya SMTP. Acaba amb `RESULTAT: OK` si tot va bé.

LÍMIT DE CONEIXEMENT
---------------------
Aquest mòdul no desa res i no comprova cap correu real: en proves el
`send_mail` s'ha substituït. Abans d'anar en producció, comprova amb un
correu de debò que el teu servidor sortint no rebutja el teu domini
(SPF, DKIM i, si aplicables, les regles del proveïdor).

LICÈNCIA
--------
AGPL-3.0-or-later. Vegeu el fitxer `LICENSE` a l'arrel del repositori.
El codi no conté cap dada ni configuració de cap entitat: el que apareix a
la configuració d'exemple són valors deExemple per llegir.

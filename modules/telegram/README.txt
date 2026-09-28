README.txt — mòdul "telegram" del Col·lectiu 9 Barris Imatge
==========================================================

QUÈ ÉS
------
Script petit (Python, només biblioteca estàndard) que publica al canal
públic de Telegram @NouBarrisImatge cada entrada nova del web. És el que
fa certa la promesa de la pàgina de contacte: «Cada post nou, al teu
mòbil».

El canal és unidireccional: el bot hi publica, els membres del canal
només llegeixen. No hi ha cap base de dades ni cap servei de tercers
entremig: l'script llegeix el RSS públic del web i crida directament
l'API de Telegram.

En marxa des del 2026-09-28 (primera publicació real: «Festa Major de
Verdum - Verdum PunkFest»).


COM FUNCIONA
------------
Cada 30 minuts el cron del servidor executa telegram_post.py, que:

  1. Llegeix el RSS de les entrades: https://9barrisimatge.org/posts/index.xml
  2. Descarta les que ja són a state.json (ja publicades).
  3. Descarta les que tenen menys de `delay_hours` (1 h per defecte):
     marge per corregir una errada just després de publicar.
  4. Ordena la resta de la més antiga a la més nova i n'envia com a
     màxim `max_per_run` (3 per defecte) al canal.
  5. Afegeix el guid de cada entrada enviada a state.json.

Resultat: una entrada nova surt al canal entre 1 h i 1 h 30 min després
de publicar-la al web. Si se'n publiquen moltes de cop, surten de 3 en 3
cada mitja hora, per no inundar el canal.

IMPORTANT: el feed ha de ser el de /posts/. El feed arrel /index.xml
inclou també les pàgines fixes (Avís legal, Contacte...), que no s'han
de publicar al canal.


ON VIU AL SERVIDOR
------------------
    ~/apps/telegram/telegram_post.py    l'script (còpia d'aquest directori)
    ~/apps/telegram/config.ini          token + chat_id (NOMÉS al servidor)
    ~/apps/telegram/state.json          entrades ja publicades
    ~/apps/telegram/telegram.log        sortida de cada execució

Servidor: linuxbcn0@vl28359.dinaserver.com (el mateix que formularis i
vots-cordoncillo). No és al document root: el web no el pot servir.

Línia del crontab de l'usuari (ja hi és, no s'ha de tornar a afegir):

    */30 * * * * cd /home/linuxbcn0/apps/telegram && /usr/bin/python3 telegram_post.py >> telegram.log 2>&1

Per afegir-la sense perdre les altres tasques del crontab:

    (crontab -l; echo '<línia>') | crontab -

Mai `crontab -r`: esborraria també els watchdogs de formularis i
votació.


CONFIGURACIÓ
------------
config.ini viu NOMÉS al servidor, amb permisos 600, i NO s'ha de pujar
mai al repositori (el repositori és públic). Es crea a partir de
config.example.ini:

    [telegram] token       = (token del bot, de @BotFather)
    [telegram] chat_id     = @NouBarrisImatge
    [telegram] delay_hours = 1
    [telegram] max_per_run = 3
    [blog]     rss_url     = https://9barrisimatge.org/posts/index.xml

El token s'escriu directament al servidor (nano o `read -s`), mai per
xat, correu ni cap altre canal. Si mai s'ha exposat, es revoca a
@BotFather amb /revoke i es posa el nou al config.ini.

El bot ha de ser administrador del canal amb permís per publicar.

Si el token és buit o encara és el marcador de l'exemple (POSA_AQUI...),
l'script s'atura amb un error i no envia res.


INSTAL·LACIÓ DES DE ZERO
------------------------
1. Copiar l'script i l'exemple al servidor:

       scp modules/telegram/telegram_post.py modules/telegram/config.example.ini \
           linuxbcn0@vl28359.dinaserver.com:~/apps/telegram/

2. Al servidor, crear el config.ini i posar-hi el token:

       cd ~/apps/telegram
       cp config.example.ini config.ini && chmod 600 config.ini
       nano config.ini

3. MARCAR L'ARXIU COM A PUBLICAT (imprescindible). Sense state.json,
   l'script publicaria totes les entrades del web (més de 3.000), de la
   més antiga a la més nova, 3 cada mitja hora:

       python3 - <<'EOF'
       import json, telegram_post as t
       items = t.parse_rss(t.fetch_rss('https://9barrisimatge.org/posts/index.xml'))
       with open('state.json', 'w', encoding='utf-8') as f:
           json.dump({'posted': [i['guid'] for i in items]}, f, indent=2, ensure_ascii=False)
       print(len(items), 'entrades marcades com a publicades')
       EOF

4. Prova en sec: ha de dir «Res nou per publicar.»

       python3 telegram_post.py --dry-run

5. Afegir la línia del crontab (vegeu més amunt).


COM ES PROVA I COM ES VIGILA
----------------------------
- Simular sense enviar res:

      python3 telegram_post.py --dry-run

- Veure les darreres execucions del cron:

      tail ~/apps/telegram/telegram.log

  Cada execució escriu «Res nou per publicar.» o «Publicant: <títol>»
  seguit de «Fet.».

- Prova real amb l'entrada més recent: treure-la de state.json i
  executar l'script sense --dry-run.

      python3 - <<'EOF'
      import json, telegram_post as t
      items = t.parse_rss(t.fetch_rss('https://9barrisimatge.org/posts/index.xml'))
      last = max(items, key=lambda i: i['pub_dt'])
      s = json.load(open('state.json', encoding='utf-8'))
      s['posted'].remove(last['guid'])
      json.dump(s, open('state.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
      print('Pendent:', last['title'])
      EOF
      python3 telegram_post.py

Errors habituals de l'API de Telegram:
  Unauthorized      el token és incorrecte o s'ha revocat.
  chat not found    chat_id incorrecte, o el bot no és administrador
                    del canal.


ACTUALITZAR L'SCRIPT
--------------------
Només cal copiar telegram_post.py. No tocar mai config.ini ni state.json
del servidor: el primer té el token i el segon evita republicar l'arxiu.

    scp modules/telegram/telegram_post.py \
        linuxbcn0@vl28359.dinaserver.com:~/apps/telegram/


SI MAI ES VOL ATURAR
--------------------
Treure la línia de telegram_post.py del crontab (crontab -e), sense tocar
les altres. El canal es queda com està; per reprendre-ho, tornar a
afegir la línia: state.json recorda on s'havia quedat.

# Taro Photo App

> Document de referència i article per a LinuxBCN.com. Versió 2 — 2026-10-04.
> Estat: **el que fa avui està verificat amb el codi i amb el web en producció**;
> la secció 9 recull, amb els mateixos criteris, el que encara no existeix.
> Llicència prevista del programari: **AGPL-3.0** (pendent d'escriure el fitxer).

## Resum

El Col·lectiu 9 Barris Imatge (9bi) documenta el barri de Nou Barris de Barcelona
des del 2002 i des del 2018 ho fa amb el seu propi sistema: un lloc web
estàtic i un gestor de continguts que permet als membres publicar articles amb
fotografia principal, text i enllaç a l'àlbum de fotos.

Aquest sistema és **Taro Photo App**. La seva cara actual és el web
d'9barrisimatge.org, que és la referència viva del projecte: 3.008 articles
publicats, 24 fitxes de membres, 19 anys d'arxiu. La cara que es distribueix és **el mateix
sistema sense les dades**: un col·lectiu, associació o un grup fotogràfic de qualsevol
lloc del món el pot instalar amb els seus membres, els seus articles i els seus àlbums.

L'objectiu de l'article no és vendre un producte sinó explicar **com es fa i per què**:
un cas real d'una entitat sense ànim de lucre que deixa el programari d'una gran
corporació per passar a tenir el seu, amb el codi obert, i deixa al camí un programa
reutilitzable per a d'altres col·lectius.

## 1. Què és Taro Photo App

Taro Photo App és un sistema per a col·leccions i associacions fotogràfiques compost
de tres parts, construïdes amb programari lliure:

1. **Un lloc web estàtic** generat amb [Hugo](https://gohugo.io/) i el tema
   [PaperMod](https://github.com/adityatelange/hugo-PaperMod), amb disseny propi.
2. **Un gestor de continguts** ([Sveltia CMS](https://github.com/sveltia-cms/sveltia-cms),
   versió 0.217.0, autoallotjat al mateix web) perquè els membres publiquin sense
   tocar codi ni línia de comandes.
3. **Uns mòduls en Python** (votació, formularis, autopublicació) que resolen
   problemes que un lloc estàtic no resol sol: vots presencials, formularis que
   arriben al correu i construcció automàtica del web quan hi ha un canvi.

El web d'9barrisimatge.org és la implementació de referència: hi publiquen els
membres des del 2018, i a la tardor del 2026 se li ha afegit la votació del públic d'un
concurs de fotografia, que ara mateix s'està assajant abans de l'exposició de
desembre. El distribuible és **aquest mateix sistema, sense les dades del col·lectiu**.

El nom és un homenatge a [Gerda Taro](https://www.enciclopedia.cat/gran-enciclopedia-catalana/gerda-taro)
(1910–1937), fotoperiodista i companya de Robert Capa, autora d'una part
determinant dels reportatges de la Guerra Civil espanyola. Descansa al cementiri
del Père-Lachaise de París.

## 2. Per què vam deixar Blogger

La resposta honesta és que Blogger no es va Poder aguantar: es va quedar petit, i
cada limitació es converteix en feina manual per a gent que no treballa amb l'ordinador.

Les limitacions reals que vam patir, i què hi hem fet:

| Limitació de Blogger | Què fa Taro en el seu lloc |
|---|---|
| Publicar un àlbum de fotos era gairebé equivalent a «fer una entrada i enllaçar-la» | L'article té un camp `album_url`: l'àlbum és **un enllaç** i el sistema no en depèn (Google Photos, Flickr, el servei que sigui) |
| Poc control sobre qui pot editar què | Control real de versions: cada canvi és un commit, amb autor i data, i es pot revisar i revertir |
| Dependència total d'un servei extern: si la plataforma canvia les normes, l'activitat s'atura | El contingut és **Markdown en fitxers del repositori**, un format obert que es llegeix amb qualsevol eina i no caduca mai |
| Pàgines fixes i seccions com a entrades més, sense tractament especial | Pàgines fixes com a objecte propi, editables des del CMS, amb els seus camps tècnics ocults perquè no es toquin per error |
| Sense gestió de membres amb perfil propi | Fitxa per membre (nom, malnom, web, Instagram, actiu o veterà) i pàgina pròpia amb els seus articles |
| Publicar era «premer un botó» que ningú sabia explicar | Un model de publicació clar, amb els mateixos conceptes per a tothom: **autor, portada, text, àlbum, paraules clau** |

La dada que resumeix la situació: **3.006 articles** havien viscut a Blogger, alguns
de 2008. Vam migrar-los **tots, sense perdre-ne ni un** (`scripts/migrate_live.py`),
inclosos els àlbums, les imatges i les etiquetes, i l'operació va acabar amb zero
errors. La URL de cada article es conserva (`uglyURLs`), de manera que els enllaços
que havíeu compartit durant divuit anys continuen funcionant.

## 3. El model de publicació

Aquest és el cor del sistema, i és intencionadament simple. Un article és:

| Camp | Què hi va |
|---|---|
| Autor | Membre del col·lectiu. Cada article té un autor, i té la seva pàgina |
| Fotografia principal | La imatge que representa l'article a la galeria |
| Text | El cos de l'article, en Markdown, amb imatges i enllaços |
| Enllaç a l'àlbum | Un sol enllaç a l'àlbum extern. **El sistema no n'és mestre**: pot ser Google Photos, Flickr, un servei propi o el que calgui |
| Paraules clau (tags) | Les que permeten trobar l'article |

Res més. Un article és una fotografia, un text i un enllaç. Tota la resta del
sistema serveix per fer que això es publiqui, es trobi i es comparteixi bé.

## 4. Funcionalitats del lloc web

Verificat amb el web en producció:

- **Galeria en mosaic** a la portada, paginada, i **pàgina pròpia per autor** amb el
  seu propi mosaic. La imatge que veiem és sempre la fotografia principal de
  l'article.
- **Arxiu navegable** per anys, índex d'anys i pàgina de totes les entrades.
- **Núvol d'etiquetes** amb pesos segons la quantitat d'articles.
- **Cerca immediata** al web (instantània, al navegador) i a la pàgina d'error 404,
  que a més ofereix enllaços a la portada, l'arxiu i el contacte. La cerca mostra
  fins a cent resultats i la data de cada article, perquè un mateix títol pot
  aparèixer diverses vegades en 19 anys d'història.
- **Botó «Veure tot l'àlbum de fotos»** a cada article que en té.
- **Més visitats** i **estadístiques del web** des de GoatCounter (sense galetes,
  sense publicitat, sense traçar gent més enllà del que és necessari). Les dades es
  refresquen soles a cada publicació.
- **RSS** de les entrades i pàgines.
- **Pàgina d'error útil**: qui escriu una URL d'article antic que ja no existeix
  arriba a una pàgina 404 amb cerca i enllaços a la portada, l'arxiu i el contacte, no
  a una pàgina d'error buida.
- **Mode fosc** per defecte, tipografies pròpies servides des del mateix web (cap
  CDN extern), disseny adaptat a mòbil, i textos legals i de privacitat
  accessibles.
- **Metadades per a motors de cerca i xarxes socials**: dades estructurades
  (JSON-LD), títol i descripció per article, imatge social, i sitemap. Aquesta part
  es va revisar i corregir el setembre del 2026, i el resultat es pot llegir a
  `drafts/2026-09-25-auditoria-seo-quick.md`.

## 5. El CMS de gestió

Gestor de continguts propi, **autoallotjat al mateix web** (`/admin/`), sense cap
servei de gestió de continguts de tercers ni publicitat. Els editors s'identifiquen
amb el seu compte de GitHub. El gestor funciona sobre el repositori: el que un
editor veu és el fitxer, i el que es desa és un commit.

- **32 col·leccions**: 19 d'articles, una per any (per tractar els 3.008 articles
  sense que la llista es faci inservible), les pàgines fixes, la guia d'edicions,
  els membres, les actes de reunions, la documentació del concurs i les llistes de
  treball de recuperació d'àlbums.
- **Articles per any** desplegables des de la capçalera, amb miniatures correctes i
  ordenació per data descendent.
- **Pàgines fixes** (14) editables amb títol, descripció i cos, amb els camps
  tècnics (URL, plantilla, redireccions) ocults a la interfície perquè no es
  perdin en desar i no s'editin sense voler.
- **Guia d'edicions** per als membres, accessible però **no indexada** pels motors
  de cerca i no publicada als feeds.
- **Membres** amb fitxa pròxima, actiu o veterà.
- **Actes de reunions** amb data, lloc, assistents, convidat i ordre del dia.
- **Barra lateral pròpia** que substitueix la del gestor, perquè les 19 col·leccions
  d'articles del col·lectiu competeixin per l'atenció.
- **Sense dependències de build**: el gestor és un únic fitxer JavaScript servit des
  del mateix lloc. El web no en depèn per funcionar: qui parla amb GitHub és
  l'editor, des del seu navegador.

## 6. Els mòduls (plugins)

Tres aplicacions en Python, **només amb la biblioteca estàndard** (cap `pip`, cap
`pip install`, cap entorn virtual), que comparteixen servidor i que es guarden les dades
en SQLite quan cal.

### 6.1 Votació (`votacio`) — en producció

Per a exposicions i concursos on el públic ha de votar **presenta**, sense poder
votar des de casa mil vegades.

- Pàgina de votació amb **teclat numèric** i instruccions, feta per a mòbil.
- **Codi QR** del cartell i de cada obra, generats amb una eina pròpia
  (`tools/qr.py`).
- **Vot per obra i dispositiu**: el vot es lliga a un codi del dispositiu, calculat
  amb clau secreta. No es desa cap dada personal: ni nom, ni correu, ni
  coordenades del qui vota.
- **Geofencing**: només es pot votar dins d'un radi (500 m) del punt de l'exposició.
  Si el telèfon diu que ets a 5 km, la resposta ho diu clarament, i si la precisió
  és baixa avisa que cal activar l'ubicació exacta.
- **Mode de proves** (re-vot cada 10 min, sense límit d'obres) i mode de votació
  oberta per a fer assaigs.
- **Panel d'administració** amb recompte, llistat d'obres, visites, tancament
  automàtic de l'edició i **exportació CSV** signada. Tancar l'edició demana
  confirmació i va protegit contra CSRF.
- Tres idiomes (català, castellà, anglès), amb els textos d'error, de geofencing i
  de privacitat ja redactats.
- Sense rastreig de tercers: sense galetes publicitàries i sense cap servei extern
  que compti les visites als vots.

Allotjament actual: `vots-cordoncillo.linuxbcn.com`.

### 6.2 Formularis (`formularis`) — en producció

Els formularis d'un lloc estàtic no tenen on enviar les dades. Aquest mòdul les
rep i les fa arribar **per correu, des del nostre propi servidor**, sense intermediaris
(Servicios com FormSubmit existeixen perquè el hosting estàtic no ofereix correu).

- Dos formularis: **contacte** i **incorpora't al col·lectiu**.
- **Sense base de dades**: el missatge entra per correu i el correu és l'arxiu.
- Proteccions, totes implementades i provades: validació de l'**origen** de la
  petició (403 si no és del nostre web), **trap de mel** (honeypot), **límit de taxa
  per IP**, filtratge de camps (llista blanca), limitació de mida de la petició
  (64 KB) i de cada camp, i neteja de caràcters de control.
- Cap error tècnic del servidor no arriba al navegador: si el correu falla, el
  visitant rep un avís genèric i el problema es queda al registre.
- **Peu legal** (RGPD i LOPDGDD) a cada missatge enviat.
- Adreça de resposta (`Reply-To`) només si l'adreça del remitent és vàlida.

Allotjament actual: `formularis.linuxbcn.com`.

### 6.3 Autopublicació (`autopublica`)

Un component petit que escolta un **webhook** de push i reconstrueix el web.
Només s'ha connectat al repositori de Codeberg, que ja no publiquem, i **no s'ha
activat sobre GitHub**: la publicació real la fa l'acció `deploy.yml` de GitHub
Actions. Queda pendent de decidir si es manté com a component de Taro o si es deixa
de banda, perquè la funcionalitat que li promet el nom (crear l'article i
registrar-lo) encara no existeix.

## 7. Scripts i eines

Tot el que hi ha al repositori per fer feina, ordenat per finalitat:

**Migració i neteja de contingut** (`scripts/`)

| Script | Què fa |
|---|---|
| `migrate_live.py` | Migra els articles des del feed en directe del blog, amb imatges, àlbums i etiquetes. Va migrar els 3.006 articles, zero errors |
| `migrate_blogger.py` | El mateix, però des d'un export XML oficial |
| `recupera_autors_blogger.py` | Recupera l'autoria dels articles des del perfil antic. En va assignar 439 de 473; els 34 restants queden documentats |
| `albums_fix.py`, `picasa_to_photos.py` | Recupació d'àlbums morts i transvasament de Picasa a Google Photos |
| `auto_tags.py` | Genera paraules clau candidates per als articles que no en tenen |

**Estadístiques** (`scripts/`)

| Script | Què fa |
|---|---|
| `goatcounter_popular.py` | Consulta GoatCounter i genera la llista d'articles més visitats. S'executa a cada publicació; si l'API falla, es conserven les dades anteriors |
| `fetch_9bi_analytics.py` | Baixa les estadístiques del tauler |

**Eines de la votació** (`modules/votacio/tools/`)

| Eina | Què fa |
|---|---|
| `qr.py` | Genera el codi QR del cartell i de cada obra |
| `tally.py` | Recompte dels vots, amb opció de paper, per poder fer un recompte transparent amb urna |
| `audit.py` | Verifica que les empremtes de votació són vàlides i que no hi ha duplicats |

**Posada en marxa i manteniment** (`modules/*/deploy/`, `sync-9bi.sh`)

| Fitxer | Què fa |
|---|---|
| `start.sh` / `stop.sh` | Arrenca i atura el procés, amb permisos restringits i sense deixar secrets llegibles |
| `watchdog.sh` | Comprova cada 5 minuts que el servei és viu i el reactiva si ha caigut (també a l'arrencada del servidor) |
| `htaccess` | Redireccions a HTTPS i proxy cap al servei intern, sense exposar el port |
| `provar.py` | Bateria de proves de formulari, amb un remitent simulat |
| `serve.py` | Executa el mòdul en local, per desenvolupar |

## 8. Virtuts

**Tecnològiques**

- **Cap dependència de tercers als mòduls**: Python de biblioteca estàndard i
  SQLite. No hi ha `pip install`, ni dependències que es trenin ni que calgui
  actualitzar amb urgència. Un col·lectiu pot allotjar-lo en un servei econòmic i
  oblidar que hi ha un marc de programari sota.
- **Un lloc estàtic és ràpid, barat i difícil d'atacar**: HTML generat, sense base de
  dades, sense PHP, sense superfície d'atac en execució.
- **El contingut és versió, i versió és memòria**: cada article és un fitxer amb
  autor, data i historial. Es pot buscar, revisar, corregir i revertir. Cap contingut
  viu dins d'un algoritme d'alguna plataforma.
- **Autohospedatge**: web, gestor, votació i correu es poden servir des del mateix
  equipament, amb un procés i un registre.
- **Sense traçament innecessari**: estadístiques sense galetes i sense publicitat.
- **Sense marcs de tercers per a la gestió**: el gestor és nostre i es publica
  des del nostre web.

**Socials i de missió**

- **Cap barrer**: un article es publica, es corregeix o s'esborra sense dependre de
  ningú.
- **Autonomia de les dades**: el patrimoni documental de 24 anys de col·lectiu és
  fitxers llegibles, no una base de dades d'algú altre.
- **Aprenentatge accessible**: HTML, Markdown, Git i Python són eines conegudes per
  moltíssima gent, i tot el projecte és llegible i copiable.

**I, sobretot, la virtut que interessa a LinuxBCN**

Un sistema **real i en producció, no un prototip**. Un col·lectiu sense ànim de lucre
l'ha fet servir per publicar 3.008 articles, exposar fotografies i posar en marxa la
votació del públic d'una exposició. El valor de Taro no és la tecnologia, sinó que
**aquest model ja s'ha provat** i està documentat per poder reutilitzar-se.

## 9. Què encara no existeix (i per tant no es pot prometre)

Aquest apartat és tan important com els anteriors. El que segueix és **el que
hi ha de veritat a 27 de setembre de 2026**, després de la tanda de treball
d'aquest dia.

**Resolt en aquesta sessió.** Un apartat de «no existeix» que ja no és cert
seria una mentida, així que el que s'ha fet surt de la llista:

1. **Llicència.** Hi ha el fitxer `LICENSE` amb el text oficial de l'AGPL-3.0,
   capçaleres SPDX als fitxers de codi i la carpeta `LICENSES/` amb els textos
   de les llicències dels components de tercers (PaperMod, Sveltia, React,
   Gillius ADF, Montserrat). Sense això, convidar algú a reutilitzar el
   programari era una incoherència.
2. **Actes amb contingut real.** Les actes ja tenen camps per a les decisions
   i les votacions, a més de l'ordre del dia, i la documentació ho explica.
3. **Assemblees.** Hi ha vocabulari propi («Reunions (assemblees)») amb data,
   lloc, assistents, ordre del dia, decisions i votacions.
4. **Paquet distribuïble.** `modules/taro/` està al dia i funciona: un router
   que munta els tres mòduls, cap dada ni configuració de 9 Barris Imatge a
   dins, documentació de cada mòdul i un manual del bundle. Les proves de
   formulari i de votació s'executen i acaben amb `RESULTAT: OK`. Des del
   2026-10-04 es publica a Codeberg (`linuxbcn/taro-photo-app`) amb un
   `INSTALL.md` i historial de versions.
5. **Filtratge del gestor.** El gestor té un rail propi que filtra els
   articles per any i amaga la llista de col·leccions. És ordre de la
   interfície, no seguretat: la frontera real és qui té accés d'escriptura.

**El que encara no existeix, i per tant no es pot prometre:**

1. **No hi ha aïllament d'usuaris.** Cada article té autor i cada membre té la
   seva pàgina, però al gestor qualsevol persona amb accés d'escriptura veu i
   pot editar **tots** els articles. El gestor actual tampoc té rols propis,
   de manera que la separació real només es pot fer donant compte i permisos
   diferents, o construint un gestor amb permisos. Per a un col·lectiu gran,
   és la manca més seriosa.
2. **Les exposicions no es gestionen des del gestor.** Hi ha la votació en
   producció i cada edició pot tenir els seus resultats, les seves dates i les
   seves obres, però les obres viuen en un fitxer de configuració del servidor
   i s'han d'editar a mà. La gestió d'exposicions, obres i resultats des del
   gestor no existeix.
3. **No hi ha instal·lador.** Hi ha un manual i unes plantilles de
   configuració que funcionen sense tocar res, però cap assistent que faci les
   preguntes i deixi el servei en marxa.
4. **El gestor de continguts continua sent específic d'aquest col·lectiu.** Té
   32 col·leccions fetes a mida per als 3.008 articles i els 19 anys del 9bi.
   Un col·lectiu nou ha de retallar i renomenar la configuració del gestor; no
   hi ha un gestor genèric de col·leccions (articles, pàgines, membres, actes,
   exposicions).
5. **`autopublica` no fa encara el que promet el nom** (vegeu el 6.3) i no
   s'ha activat enlloc: la publicació real la fa GitHub Actions.

## 10. Com seria la instal·lació en un altre col·lectiu

El camí, tal com està avui, seria: tenir un allotjament amb Python 3 i un
domini; baixar la carpeta `modules/taro/`; llegir-ne el manual
(`modules/taro/README.txt`); triar els mòduls que es vulguin (cadascun es
pot instal·lar sol o tots junts sota `/taro/`); i omplir la seva
`config.example.ini`, que té valors d'exemple per llegir i cap dada nostra a
dins. En altres paraules: feina de configuració, no de programació, i ara amb
guia.

Un distribuible del tot acabat hauria d'ajustar cinc coses, i quatre ja
estan fetes:

1. ~~Fitxer de llicència AGPL-3.0 i documentació~~ — **fet** (`LICENSE`,
   `LICENSES/`, capçaleres SPDX).
2. ~~Documentació d'instal·lació pas a pas~~ — **fet** (manual del bundle i un
   document per mòdul, amb les dues variants d'allotjament: Passenger i procés
   d'usuari amb proxy).
3. ~~Decidir què és el paquet publicable i posar-lo al dia~~ — **fet**
   (`modules/taro/`, tres mòduls i router, sense dades nostres).
4. ~~Separar el codi real del codi distribuible~~ — **fet** (els mòduls en
   producció i la còpia distribuïble són directoris separats; per pujar una
   millora als dos cal sincronitzar-los).
5. **Gestor amb col·leccions genèriques** (articles, pàgines, membres, actes,
   exposicions) en lloc de la llista de 32 col·leccions d'aquest col·lectiu.
   **Pendents**, i són els dos punts que realment costarien feina: aquest i
   els permisos reals per membre.


## 11. Invitació

Aquestes línies són la part que ens interessa escriure: **el programa és vostre**.

- **Si teniu un col·lectiu, associació o grup fotogràfic**, podeu instal·lar-lo i
  tenir el vostre web, el vostre gestor i, si en feu falta, la votació del públic i els
formularis. No cal saber programar: publicar és escriure i pujar una imatge.
- **Si voleu adaptar-lo**, feu-ho. L'AGPL-3.0 us deixa (i us obliga, si ho publiqueu)
  a compartir les millores, i la idea és que el que millori el 9bi torni al col·lectiu.
- **Si hi ha una funcionalitat que us falta**, digueu-la. Cada mòdul de Taro va
  néixer d'una necessitat real d'un col·lectiu, no d'una idea: la votació va néixer
  del concurs de fotografia, els formularis, de no dependre de serveis de tercers.
- **Si voleu el programari i no teniu Hosting, parlem.** A LinuxBCN podem oferir l'allotjament, el correu i el manteniment amb tarifes de col·lectiu, i
  si esteu lluny, amb un contracte de manteniment, perquè la garantia de que el
  lloc continuï en marxa no quedi només en mans de voluntaris.
- **Si voleu llegir-ne el codi, useu-lo o millorar-lo**, el repositori és
  obert: [codeberg.org/linuxbcn/taro-photo-app](https://codeberg.org/linuxbcn/taro-photo-app).

## Annex: referències tècniques

Dades verificades el 2026-09-27 sobre el repositori i el web en producció.

**Volum del projecte**: 3.008 articles (2008–2026, 3.006 migrats de Blogger, 0
errors) · 24 fitxes de membres (12 actius i 12 amb l'actiu desactivat, entre ells el
fundador honorífic) · 14 pàgines fixes · 32 col·leccions al gestor · més de 8.700 pàgines HTML
generades · construcció local en menys de mig minut.

**Tecnologies**: Hugo 0.164.0 *extended* · PaperMod (tema, amb el peu i la capçalera
reescrits pel projecte) · Sveltia CMS 0.217.0 autoallotjat · Python 3
(biblioteca estàndard) · SQLite (només la votació) · GitHub Actions per a la
publicació amb accions ancorades a SHA · GoatCounter per a les estadístiques.

**Allotjament**: el web i el gestor de continguts els serveix GitHub Pages; la
votació i els formularis es serveixen des de l'hosting que ofereix
LinuxBCN, amb procés propi, proxy i vigilant automàtic. `autopublica` no
s'ha activat enlloc (vegeu el 6.3).

**Repositoris**: el **programari distribuïble** és a Codeberg
(`linuxbcn/taro-photo-app`, v1.0.1, 2026-10-04): un repositori net amb el web,
els mòduls i la documentació d'instal·lació (`INSTALL.md`), sense cap dada del
9bi. El **web de referència** (9barrisimatge.org) es desenvolupa a GitHub
(`112books/9bi`), que és d'on es publica. El programari està llicenciat amb
AGPL-3.0 (`LICENSE`).

**Fitxers que expliquen el funcionament**: `content/credits.md` (crèdits del web,
amb l'explicació de la decisió sobre Blogger i sobre el nom Taro) ·
`modules/taro/README.txt` (manual del paquet distribuible) ·
`modules/votacio/README.md`, `modules/formularis/README.txt` i
`modules/autopublica/README.md` (posada en marxa, seguretat i proves de cada
mòdul) · `content/documentacio/concurs/sistema-votacio.md` (el sistema de votació
del concurs) · `drafts/2026-09-25-auditoria-seo-quick.md` (revisió de SEO) ·
`drafts/2026-09-19-apps-modulars-votacio-albums.md` (pla de la suite, amb els
mòduls previstos).

QUÈ ÉS
-------
Programes en Python per mantenir el lloc i les estadístiques. S'executen
a mà (o des del servidor de GitHub Actions); cap d'ells s'executa quan un
visitant obre el web.

Què hi ha
---------
migrate_blogger.py   Converteix una exportació XML de Blogger en articles
                     de Markdown amb Hugo. Fa la conversió d'imatges,
                     detecta l'enllaç de l'àlbum de fotos i neteja el HTML.
migrate_live.py      El mateix, però llegint directament del feed del blog
                     en directe. Va ser el que es va fer servir per
                     migrar els 3.006 articles originals. Reassigna
                     autors i proposa etiquetes.
recupera_autors_blogger.py
                     Recupera l'autor d'un article a partir de les dades
                     del blog antic. Hi ha autors que no s'han pogut
                     resoldre i que consten com "9 Barris Imatge"
                     (llista a drafts/autors-no-resolts.md).
goatcounter_popular.py
                     Consulta GoatCounter i genera data/popular.json, la
                     llista d'articles més visitats que mostra /mes-visitats/.
                     Cal la variable GOATCOUNTER_API_KEY.
fetch_9bi_analytics.py
                     El mateix idea per al tauler /stats/. El servidor
                     GitHub Actions l'executa a cada desplegament.
add_year.py          Va afegir el camp year al front matter dels articles,
                     necessari per a les col·leccions per any del CMS.

Nota
----
Aquest directori NO s'ha d'executar sense mirar abans què fa el script
(opció --help) i sobre quins fitxers actua.

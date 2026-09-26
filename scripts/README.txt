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

auto_tags.py         Genera etiquetes automàtiques per als posts que
                     tenen el comentari <!-- tags auto-generades... -->.
                     Utilitza Claude Haiku (API d'Anthropic, model barat).
                     Requisit: pip install anthropic
                               export ANTHROPIC_API_KEY=sk-ant-...
                     1.697 posts a processar (juny 2026).

                     INSTRUCCIONS PER EXECUTAR (amb OpenCode o manualment):
                     ---------------------------------------------------------
                     # 0. Instal·la la llibreria si no la tens:
                     pip install anthropic

                     # 1. Prova amb els primers 5 posts (dry-run, no escriu):
                     python3 scripts/auto_tags.py --dry-run --limit 5

                     # 2. Prova real amb còpia de seguretat (escriu .bak):
                     python3 scripts/auto_tags.py --limit 20

                     # 3. Si el resultat és bo, processa tots:
                     python3 scripts/auto_tags.py

                     # 4. Revisa l'informe generat:
                     cat auto_tags_report.txt

                     # 5. Si algun post ha quedat malament, restaura el .bak:
                     cp content/posts/2013/post-exemple.md.bak \
                        content/posts/2013/post-exemple.md

                     # 6. Esborra els .bak un cop satisfet:
                     find content/posts -name "*.bak" -delete

                     # 7. Comprova el build:
                     hugo --minify

                     # 8. Commit i push:
                     git add content/posts/
                     git commit -m "Tags: etiquetes auto-generades revisades (Claude Haiku)"
                     git push github main

Nota
----
Aquest directori NO s'ha d'executar sense mirar abans què fa el script
(opció --help) i sobre quins fitxers actua.

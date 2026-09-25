QUÈ ÉS
-------
Dades que Hugo llegeix com a dades i que no són articles: en paraules
simples, "contingut estructurat" que el web consulta per generar les
taules, els llistats i les estadístiques.

Què hi ha dins
--------------
membres/         Un fitxer .yml per cada persona del col·lectiu (24 fitxers).
                 Es crea i s'edita des del CMS, a la col·lecció «Membres».
                 Camps: autor (clau d'atribució dels articles, no es canvia),
                 nom real, malnom (el que es mostra, si en hi ha), web,
                 instagram i actiu (true = membre actual, false = històric).
                 Dades reals, verificades amb la persona; no s'han d'omplir
                 a invents. La llista de membres actius es mostra a
                 /qui-som/ i la taula de tot el col·lectiu surt d'aquí.
popular.json     Llista d'articles més visitats (la pàgina /mes-visitats/).
                 La genera scripts/goatcounter_popular.py amb l'API de
                 GoatCounter i s'actualitza a mà; automatitzar-ho és una
                 tasca pendent.
picasa-broken.json i links-nous.json
                 Llistes de treball sobre enllaços d'àlbums: quins enllaços
                 de Picasa van morir i quins caldria refer. Són material
                 de feina, no es publiquen.

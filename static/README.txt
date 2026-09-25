QUÈ ÉS
-------
Fitxers que es publiquen al web tal qual, sense processar (a diferència
d'assets/, on Hugo els processa). Aquí hi viu el gestor de continguts,
les imatges, el dashboard d'estadístiques i les tipografies.

Què hi ha dins
--------------
admin/     Gestor de continguts (Sveltia CMS) autoallotjat. S'obre a
           /admin/ i funciona amb el compte de GitHub de cada editor.
           NO S'ESBORRI: és l'eina amb què escriu el col·lectiu.
           Vegeu admin/README.txt.
images/    Portades dels articles, miniatures, logotips, icones i imatges
           del concurs i de les exposicions.
fonts/     Tipografies pròpies del lloc (Montserrat per al text, Gillius
           ADF per als títols), en fitxers locals, sense cap servei
           extern de tipografies.
stats/     Tauler d'estadístiques de visites (Gràfics amb Chart.js) que
           alimenta el script de GoatCounter a cada desplegament. Té
           noindex: no s'ha de indexar.
sveltia...  Altres recursos del CMS.

També hi ha els icones del lloc (favicon, apple-touch-icon) i els
robots.txt, que s'ha de mantenir apuntant al sitemap.

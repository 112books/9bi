QUÈ ÉS
-------
Un fitxer per cada persona del col·lectiu (24 fitxers), amb les dades
reals que necessita el web: com es diu, com se l'anomena, on té el web i
si és membre actual o històric.

Què hi ha dins
--------------
autor       Clau interna. Ha de coincidir exactament amb el camp author
            dels articles, i per això NO s'ha de canviar. Si cal canviar
            el nom, es fa en un article nou; en elsantics caldria
            actualitzar-los tots.
nom         Nom i cognoms reals.
malnom      El nom amb què la gent el coneix («Linux», «Ulls»,
            «Casal»...). Si és buit, el web mostra el nom real.
web         Adreça del seu web o perfil. Si no en té, el web hi posa
            enllaç als seus articles.
instagram   Perfil d'Instagram. Hi ha alguns membres que encara no en
            tenen enllocat: és una tasca pendent, no un error.
actiu       true = membre actual (surt a la llista de membres actius de
            /qui-som/ amb el seu enllaç); false = membre històric
            (surt a sota, al grup de membres veterans).

On s'editar
------------
Des del gestor de continguts (CMS), a la col·lecció «Membres». A mà, es
poden editar els .yml, però cal respectar el format (dos espais, cometes
opcionals) i no tocar el camp autor.

Per què és aquí i no al CMS sol
-------------------------------
Aquestes dades apareixen a la portada, a «Qui som», a la pàgina de cada
autor i al peu del web (la xifra de membres). Venen del fitxer i no de
l'activitat recent, perquè el peu ha de dir sempre 24 membres encara que
aquest mes publiqui poc.

Es pot esborrar? Un fitxer, sí, però la persona deixarà d'aparèixer a la
llista de membres del web. Cal preguntar-li abans.

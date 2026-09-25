QUÈ ÉS
-------
Plantilles pròpies del lloc: aquí hi viu la part del disseny i de la
maquetació que no és el tema PaperMod. Tot el que hi ha aquí substitueix
o afegeix el que faria el tema.

Si un dia s'actualitza PaperMod, cal revisar aquests fitxers, perquè
algunos sobreescriuen directament els del tema.

Què hi ha
---------
baseof.html          Esquelet de la pàgina. SOBREESCRIT: la clau de memòria
                     del peu inclou una condició de "números" perquè la
                     portada i «Qui som» no comparteixin peu amb els articles.
404.html             Pàgina d'error pròpia: "Aquesta pàgina no s'ha trobat",
                     motius habituals, cerca directa i enllaços a Portada,
                     Arxiu i Contacte. Retorna HTTP 404 real i noindex.
index.html           Portada en mosaic de fotografies, paginada.
single.html          Article i pàgina. Admet visualTitle (títol amb salt de
                     línia) i visualDescription, i el bloc de fotografia de
                     capçalera (header_image).
archives.html        Arxiu + índex d'anys a la dreta.
taxonomy.html        Núvol d'etiquetes (/tags/).
search.html          Cerca immediata amb índex Fuse.
author/term.html     Articles d'un autor, en mosaic, paginat. Llegiràs les
                     dades reals de la persona a data/membres/.
_default/popular.html Llista de més visitats (llegeix data/popular.json).
_partials/           header (icones i capçalera sticky), footer (banda
                     vermella i 5 columnes), extend_head (tipografies i
                     GoatCounter), avís del concurs, autor al final de
                     l'article, botó "Veure tot l'àlbum de fotos".
_shortcodes/         membres (taula de membres), rel (adreça relativa per a
                     HTML escrit a mà), guia-tabs (pestanyes de la guia).
_markup/             render-image (adreces d'imatge base-aware).
aviso del concurs     Avís flotant del termini de participació i de la votació.

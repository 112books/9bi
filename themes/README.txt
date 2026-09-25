QUÈ ÉS
-------
El tema gràfic del lloc: PaperMod, copiat dins del repositori perquè el
web no depengui de res extern i per poder-lo modificar.

ATENCIÓ
-------
Aquí NO hi ha tot nostre. En una banda, els fitxers originals del tema
PaperMod (amb la seva llicència, que cal conservar). En l'altra, pocs
fitxers que hem modificat nosaltres, que es poden perdre en actualitzar
el tema:

themes/PaperMod/layouts/baseof.html             (nosaltre: clau del peu)
themes/PaperMod/layouts/_partials/footer.html   (nosaltre: peu de 5 columnes)
themes/PaperMod/layouts/_partials/head.html     (nosaltre: SEO, meta, cerca)
themes/PaperMod/assets/js/fastsearch.js         (nosaltre: cerca amb Fuse)

Abans d'actualitzar el tema, un "git log -- themes/PaperMod" indica quins
fitxers s'han tocat de debò.

Si s'actualitza PaperMod, cal:
1. fer una còpia d'aquests fitxers abans de substituir-los,
2. tornar-los a posar després,
3. comprovar capçalera, peu, cerca i metadades del web en directe.

Alternativa a actualitzar el tema: les versions pròpies del lloc ja viuen
a layouts/ i a assets/, que tenen prioritat sobre les del tema i no es
perden en una actualització.

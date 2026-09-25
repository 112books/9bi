QUÈ ÉS
-------
Els articles del col·lectiu, agrupats en una carpeta per any (2008-2026).
Són uns 3.000 fitxers i el cor del web: el que hi ha aquí és el que la
gent llegeix a https://9barrisimatge.org/

Què hi ha dins cada article
---------------------------
Front matter (entre --- i ---):
  title       títol de l'article
  date        data de publicació (YYYY-MM-DD)
  year        any, redundància que permet al gestor agrupar per any
  author      qui l'ha escrit (la clau ha de coincidir amb un fitxer de
              data/membres/)
  slug        nom curt de l'URL
  tags        etiquetes
  cover       imatge principal (opcional)
  album_url   enllaç de l'àlbum de fotos de Google Photos (opcional)
  description text per als cercadors (opcional)
Després, el cos de l'article en Markdown (també hi ha HTML antic que ve
del blog de Blogger i no s'ha tocat).

Advertiments
------------
- L'adreça web de cada article (/AAAA/MM/titol.html) surt de la data i del
  slug, NO del nom del fitxer. Es pot moure o reanomenar un fitxer sense
  canviar la seva URL, però NO es pot canviar el slug ni la data d'un
  article ja publicat: es perdria l'enllaç.
- Els articles tenen enllaços cap a àlbums de fotos que en alguns casos van
  morir quan Google va tancar Picasa. La llista de refer s'ha de demanar,
  és a recuperacio/.
- Editar un article des del gestor (CMS) és la via habitual; si es fa a
  mà, cal respectar el format del front matter.

Es pot esborrar? No sense esborrar l'article del web. Si un article ja
no es vol publicar, deixar-lo amb draft: true.

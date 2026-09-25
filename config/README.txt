QUÈ ÉS
-------
Configuració del lloc en format TOML, separada per entorn:

_default/hugo.toml      Valors comuns: títol, idioma (ca), zona horària,
                        permalinks (/YYYY/MM/slug), taxonomies, menús,
                        paràmetres del tema PaperMod i del CMS.
development/hugo.toml   Servidor local (hugo server). baseURL local.
production/hugo.toml    Producció: https://9barrisimatge.org/
staging/hugo.toml       Previsualització al servidor de Codeberg Pages.

Què hi ha de conservador
------------------------
- uglyURLs = true: manté les URL antigues acabades en .html del blog de
  Blogger, per no trencar els enllaços publicats ni el posicionament.
- [permalinks] posts = "/:year/:month/:slug": les URL surten de la data i
  del slug de l'article, no de la carpeta on viu el fitxer. Per això els
  articles es poden moure de carpeta sense canviar la seva adreça.
- showShareButtons / comments: desats perquè el col·lectiu no fa xarxes
  socials des del web.
- defaultTheme = "dark": el web s'obre en mode fosc.

Es pot esborrar? No sense perdre el web. Si es perden, el lloc es
construirà amb els valors per defecte de PaperMod i es perdrà el menú, el
títol i els permalinks.

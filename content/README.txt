QUÈ ÉS
-------
Tot el contingut publicable del web: articles, pàgines fixes, la guia
d'editors i la documentació interna. És la part del repositori que es
pot modificar des del gestor de continguts (CMS) de l'usuari editor.

Estructura
----------
posts/AAAA/    Els articles, agrupats per any (2008-2026, uns 3.000).
               Els fitxers d'un mateix any comparteixen carpeta, però
               l'adreça web NO depèn de la carpeta: surt de la data i del
               slug del front matter (/AAAA/MM/titol.html). Per això es
               poden moure de carpeta sense trencar cap enllaç.
               Camps habituals del front matter: title, date, year,
               author, slug, tags, cover.image, album_url, description.
               body: el text de l'article, en Markdown (també s'accepta
               HTML antic de Blogger).
guia/          Guia d'editors (8 pàgines). Publicada a /guia/ però
               robotsNoIndex, fora del menú i fora del sitemap: no és per
               visitants, és per a qui escriu al web.
documentacio/  Actes de reunió i documentació del concurs. Marcats com
               draft: existeixen al repositori però no es publiquen.
*.md a l'arrel Pàgines fixes: qui-som.md, concurs.md, contacte.md,
               privacitat.md, avis-legal.md, cookies.md, credits.md,
               subvencions.md, search.md, archive.md, mes-visitats.md,
               incorpora-te.md.

Camps especials que cal respectar
---------------------------------
- url: ruta final explícita de les pàgines fixes (per exemple /contacte/).
- visualTitle / visualDescription: títol i subtítol visuals amb salt de
  línia, quan el títol real és massa llarg.
- robotsNoIndex, hiddenInRss, sitemap.disable: s'usen per a la guia.
- layout: search, archives o popular per a les pàgines especials.

Es pot esborrar? No. El directori posts/ és el blog sencer del col·lectiu
i no hi ha cap còpia dels articles fora del repositori. Si un article
s'ha d'esborrar, millor és deixar-lo amb draft: true; i el repositori
es publica a GitHub (producció) i es conserva a Codeberg com a
reserva, encara que de moment no s'hi pugui enviar res (quota).

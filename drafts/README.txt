QUÈ ÉS
-------
Documentació de feina: informes, plans, researches i registres de les
tasques en curs. Són documents en text pla, per a consultar i revisar
nosaltres mateixos. NO es publiquen al web (Hugo no els llegeix, perquè
no són a content/).

Què hi ha
---------
2026-09-25-auditoria-seo-quick.md
                 Revisió ràpida de SEO, GEO (cercadors amb IA) i AEO
                 (respostes a preguntes) del web, amb punuació i
                 recomanacions. Inclou una correcció de dades.
2026-09-25-smtp-propi-dns.md
                 Com s'ha de deixar el correu del domini ben configurat
                 (SPF, DKIM, DMARC) i com passar els formularis del web
                 del servei FormSubmit al nostre propi servidor de correu.
2026-09-19-*      Pla de la votació per QR i dels programes del col·lectiu.
2026-09-18-*      Pla de recuperació dels àlbums de fotos perduts.
altres            Actes, correus, llistes de treball i notes d'infraestructura.

Documentació de directoris que no pot quedar dins la seva carpeta
-----------------------------------------------------------------
Hi ha un README.txt a gairebé tots els directoris del repositori, però els
de la carpeta static/ no poden-hi ser: Hugo copia tot el que hi ha dins
static/ al domini públic i el document acabaria visible a Internet. Per això
aquí, amb el nom del directori que descriuen:

README-static.txt            → static/
README-static-admin.txt      → static/admin/       (gestor de continguts)
README-static-images.txt     → static/images/      (fotografies i logotips)
README-static-fonts.txt      → static/fonts/       (tipografies del web)
README-static-stats.txt      → static/stats/       (tauler de visites)

Els README.txt que sí que estan dins la seva carpeta no es publiquen: la
configuració de Hugo els ignora (vegeu ignoreFiles a config/_default/hugo.toml,
que cal conservar si mai es treu de contextual).

Per què serveix
---------------
Deixa escrit per què es prenen les decisions i on quedava cada cosa, per
evitar haver de reconstruir la memòria del projecte. El document més
complet del projecte és CLAUDE.md, a l/arrel del repositori.

Es pot esborrar? Sí, sense afecta el web publicat, però es perden les
decisions i l'estat de les tasques pendents. Convé llegir-los abans de
proposar canvis al lloc.

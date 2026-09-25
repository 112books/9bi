Aquest document descriu el directori static/admin/ del repositori. És aquí perquè Hugo copia tot el que hi ha dins de static/ al domini públic i no hi pot haver cap documentació dins.

QUÈ ÉS
-------
El gestor de continguts (CMS) del web: l'eina amb què els membres del
col·lectiu publiquen articles sense tocar el codi. S'autoallotja al
repositori (no depèn de cap servei de tercers) i s'obre a:

    https://9barrisimatge.org/admin/

Què hi ha dins
--------------
index.html      Capçalera i peu propis del gestor (logo, «Llegir la guia»,
                «Torna al web») i el rail lateral d'articles per any.
                També amaga la llista de col·leccions nativa del Sveltia
                amb CSS i JavaScript, perquè el contingut ocupi tota
                l'amplada. Té noindex.
config.yml      Definició de les col·leccions: 19 col·leccions d'articles
                (una per any, 2008-2026), pàgines fixes, membres, guia,
                actes, concurs i els llistats d'àlbums per recuperar.
                Indica el backend (GitHub, repositori 112books/9bi,
                branca main) i els camps de cada col·lecció.
sveltia-cms.js  Còpia local del programa Sveltia CMS (0.217.0), perquè el
                gestor funcioni sense descarregar res de fora.

Com s'hi entra
--------------
Cada editor entra amb el seu propi compte de GitHub i un token personal
(àmbit repo), a «Sign In with Token». Els tokens no es comparteixen ni es
guarden al repositori: si un es filtra, cal revocar-lo de seguida.

Què NO fa (limita coneguda)
---------------------------
El gestor no té rols per usuari: qui tingui accés d'escriptura al
repositori pot editar qualsevol article del web. La llista d'àlbums
per arreglar només es mostra al login que figuri al codi del gestor
(CMS_ALBUMS a index.html).

Es pot esborrar? NO. Sense aquesta carpeta, el col·lectiu es queda sense
manera de publicar articles. Si es vol desinstalar, cal deixar la web
enlloc i buscar una altra manera de publicar.

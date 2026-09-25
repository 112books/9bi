DIRECTORI IMPORTANT: NO L'ESBORRIU
====================================

QUÈ ÉS
------
La configuració del desplegament automàtic del web. GitHub Actions
(consta al directori .github/workflows/) construeix el lloc i el publica
cada cop que es puja una versió nova a la branca main.

Per què serveix
---------------
Publicar el web és una acció que ha de fer el servidor automàticament, no
algú que s'hi recordi. Sense aquest fitxer, les correccions que fem es
queden al repositori però el web publicat no canvia.

Què hi ha dins
--------------
workflows/deploy.yml   El procés sencer:
                       1. baixa el codi
                       2. prepara Hugo 0.164.0 (la versió exacta amb què es
                          fa el web, perquè el resultat sigui sempre igual)
                       3. si hi ha el secret GOATCOUNTER_API_KEY, actualitza
                          les estadístiques de visites
                       4. construeix el lloc
                       5. el publica a https://9barrisimatge.org/
                       S'activa en cada "git push" a main, i també es pot
                       llançar a mà des de la pestanya Actions de GitHub.
                       Les versions de les accions de GitHub estan fixades
                       amb el codi SHA exacte de cada versió, no amb
                       "latest", perquè mai no s'executi una versió nova
                       sense adeu-nos-en (seguretat, agost de 2026).

Què cal saber
-------------
- Per publicar: git push github main. Després cal mirar la pestanya
  Actions del repositori per veure que s'ha publicat bé.
- El secret GOATCOUNTER_API_KEY només el veu el servidor, no el
  repositori. Si el treuen, el web es publica igual però /stats/ deixa
  d'actualitzar-se.
- El codi i els fitxers de configuració del lloc (hugo.toml) són
  l'entrada: aquest directori només orquestra la construcció.

Es pot esborrar? No. El web continuarà publicat a l'última versió
desplegada, però es perdrà tota actualització automàtica i caldrà
publicar a mà. Cal vigilar-ho, sobretot abans d'ajornar res del
repositori.

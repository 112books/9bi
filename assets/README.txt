QUÈ ÉS
-------
Recursos que Hugo processa en construir el web (els comprimeix i els
concatena abans de publicar-los).

El més important:
assets/css/extended/custom.css   Tots els estilos propis del lloc: mosaic
                                de la portada, capçalera amb icones, peu
                                de 5 columnes, pestanyes de la guia i
                                del concurs, mosaic de fotos, formularis,
                                pàgina d'error 404, tipografies pròpies.

Per què no és a static/: el que hi ha a static/ es publica tal qual, sense
processar; a assets/ el material passa pel processament de Hugo, cosa que
permet compressió i generació automàtica de les rutes.

Es pot esborrar? No sense perdre el disseny del lloc.

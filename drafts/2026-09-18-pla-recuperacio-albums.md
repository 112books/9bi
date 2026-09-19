# Pla d'acció — Recuperació dels enllaços d'àlbums trencats (Picasa → Google Photos)

Data: 2026-09-18. Estat: **proposta per aprovar**. Autor: sessió 9 Barris Imatge (OpenCode).
Objectiu: recuperar els enllaços d'àlbum morts dels 3.006 posts migrats, amb el mínim esforç humà possible i amb tots els fets verificats.

---

## 1. L'estat de la qüestió (verificat)

Resum de l'anàlisi feta (vegeu `drafts/informe-links-trencats.md`):

| Estat | Quantitat | Motiu |
|---|---|---|
| 404 | 1.333 | Picasa Web tancat (redirecció a `get.google.com/albumarchive`, mort el 19/07/2023) o link compartit de Google Photos eliminat |
| 000 | 10 | URL malformada per l'import o domini mort (posterous, cybercasal9b, gallery.me, homeip, ulls.info) |
| 403 | 3 | Àlbum de Flickr privat / restringit |

Del total d'URL `picasaweb.*` úniques (1.412, comptades al cos i al front matter):

| Franja de la URL | Quantitat | Significat |
|---|---|---|
| **ID numèric de 21 dígits** | 1.011 | El format que Google va dir oficialment que "continuaria funcionant" |
| **Nom d'usuari** | 361 | Format que Google va declarar "deixarà de funcionar" (`linuxbcn`, `ulls2006`, `Perdo.Garcia`, `pedro.cervera`, `nico9barrisimarge`…) |
| `/lh/photo/…` | 40 | Fotos individuals d'àlbum, no àlbums |

**Totes**, també les d'ID numèric, redirigeixen avui a l'Album Archive → 404. La promesa oficial de Google (2016) estava materialitzada en l'Album Archive; quan Google el va apagar el **19 de juliol de 2023**, tota la resta va quedar morta.

## 2. Veredicte crític: l'automatització OAuth és inviable (fet nou, decisiu)

L'enfocament "script amb l'API de Google Photos que llista els àlbums de cada autor i regenera els links" era la via que semblava viable, però l'hem de **descartar**: Google va retirar els scopes que ho permetien.

- El **31 de març de 2025** Google va treure els scopes `photoslibrary.readonly`, `photoslibrary.sharing` i `photoslibrary` de la Library API (fonts: *Updates to the Google Photos APIs* a developers.google.com, blog oficial *Google Photos Picker API launch and Library API updates*, release notes 2025-04-01).
- Des d'aleshores, les trucades amb aquests scopes retornen **403 PERMISSION_DENIED**, encara que el token sigui vàlid i contingui l'scope (verificat per tercers: Issue Tracker de Google #466163472, projecte Nextcloud #357 amb l'evidència de 2026).
- L'API actual **només** permet accedir/crear contingut de la mateixa app (`photoslibrary.appendonly`, `photolibrary.readonly.appcreateddata`, `photoslibrary.edit.appcreateddata`). Els mètodes de *sharing* (`sharedAlbums.*`, `albums:share`) estan **deprecats**: per "compartir", Google adreça l'usuari **a fer-ho des de la interfície de Google Photos**.
- La **Picker API** (nou règim) permet a un usuari *seleccionar* fotos/àlbums interactivament, però no llista àlbums en background ni genera enllaços compartits persistents: no substitueix el que cal per a aquesta tasca.

**Conseqüència**: cap script —nostre ni de tercers— pot, avui, llistar la biblioteca d'un usuari ni activar un enllaç compartit. L'única manera de crear l'enllaç nou és que **el propietari** ho faci des de Google Photos (UI) i el passi a l'equip.

### 2bis. Recerca "ja ho ha fet algú?" (fet)

No existeix cap eina pública que faci "URL Picasa trencada → cercar l'àlbum equivalent a Google Photos → generar el link nou". Resultats revisats i per què no serveixen:

- `esteban-uo/picasa` (Node) i `morgoth/picasa` (Ruby): clients de l'**API de Picasa** per crear/llistar àlbums; l'API de Picasa va morir (deprecada 2016, API tancada gen 2019) i no parlen amb Google Photos.
- `upicasa` (PyPI): pujador CLI a PicasaWeb, obsolet.
- `jaimetur/PhotoMigrator` (GPL-3, 248★): migra entre serveis de fotos (Google Photos, Immich, Synology, Takeout…) per moure **contingut**, no regenera enllaços de cap àlbum existent.
- `immich-go` (`from-picasa`): llegeix fitxers locals `.picasa.ini` per restaurar àlbums a Immich — no toca Google Photos ni enllaços.
- `simonmiddleton/download-google-photos`: descarrega àlbums **ja compartits** (cal l'enllaç) fent scraping de la pàgina pública, sense sessió. Útil només *després* de tenir l'enllaç nou (per validar títol/contingut).
- Altres (downloaders generals per compte propi): descarregar fotos, no enllaços.

Tampoc Google va oferir mai cap eina de conversió de URLs: era el redirect propi + Album Archive, tot mort. Pel que fa a scraping amb la *sessió* del compte de l'usuari (APIs internes de `photos.google.com`): funciona de manera informal però és **fràgil i contravé les condicions d'ús de Google**; no el contemplo com a via a desenvolupar, només com a últim recurs documentat.

## 3. Enfocament viable: recuperació assistida per autor

La divisió de tasques realista entre màquina i humà:

| Pas | Qui | Com |
|---|---|---|
| 1. Corpus dels àlbums trencats | **Màquina (IA)** | Ja fet (`drafts/informe-links-trencats.md` + anàlisi de 1.412 URL). |
| 2. Material per autor | **Màquina (IA)** | Per cada membre: llista de candidats (nom de l'àlbum llegible, data aproximada, posts on surt, nº de cops). |
| 3. Compartir l'àlbum i obtenir el link nou | **Autor (humà)** | Al seu Google Photos: cerca pel nom → Comparteix → Crea enllaç → envia el link (`photos.app.goo.gl/...`). |
| 4. Validar els links rebuts | **Màquina (IA)** | Obre cada URL pública: status 200 + títol de l'àlbum que apareix = el que tocava. |
| 5. Substituir als posts | **Màquina (IA)** | Reemplaça l'`album_url` (i els enllaços del cos) pel link nou, a tots els posts del corpus. |
| 6. Build + verificar | **Màquina** | `hugo --minify`, revisió de la URL envaïda. |
| 7. No recuperables | **Editorial** | Decidir com queden (veure §7). |

És la mateixa conclusió a què ja arribava l'informe del 18/09: "automàtic no possible, cal acció de cada autor" — però ara amb el veredicte definitiu del **per què** (API morta), i amb la part d'IA aprofitada al màxim per reduir la feina humana al pas imprescindible.

## 4. Fases d'execució

### Fase 0 — Aprovació d'aquest pla
Revisar i validar aquest document. *Sense aprovació explícita, no es toca cap fitxer del web ni s'envia res als autors.*

### Fase 1 — Corpus i material per autor
- Consolidar en `data/` el corpus `picasa-broken.json` (per compte Picasa: ID numèric i username) amb: `owner`, `album`, primera URL font, posts associats i dates.
- Generar per cada membre un **full de treball** (`drafts/candidats/<autor>.md` o CSV): per cada àlbum seu, el nom llegible suggerit (normalitzat), la data probable (del primer post), quants posts hi apunten i un enllaç d'exemple al web.
- Separar els casos que **no** són àlbums Picasa (3×403 Flickr, 10×000 dominis morts, els `photos.google.com/share` eliminats) per tractar-los en una llista editorial a banda.

### Fase 2 — Prova pilot amb 1 autor (Joan "Linux")
- Escollir un subconjunt (p.ex. els àlbums de 2011–2012 de `linuxbcn` / `103138221614479310970`) per validar el flux complet: full de treball → Joan comparteix → validació → substitució → build.
- Ajustar les plantilles i el guió amb el que s'aprengui.

### Fase 3 — Repartir als autors
- Cada membre actiu rep el seu full de treball (per correu) i retorna els links nous (o "no el trobo / no existeix").
- Recollida i integració dels resultats a la mesura que arribin; no cal esperar-ho tot.

### Fase 4 — Validació automàtica
- Script/IA sobre cada link rebut: resposta diferent de 404 + títol de l'àlbum visible que coincideixi (no login).
- Ambigüitats (2 àlbums semblants) resoltes amb preguntes al propietari.

### Fase 5 — Substitució i desplegament
- Reemplaçaments a `content/posts/` (només els validats), sense canviar res més.
- Build local net, revisió d'una mostra, commit i desplegament (branca `pages` + webhook, com sempre).

### Fase 6 — Casos sense solució
- Decisió editorial per cada categoria: borrar `album_url`, deixar l'àlbum sense enllaç, o afegir nota. (Vegeu §7.)

## 5. Eines (scripts) que caldran

Resta per construir (a proposta, no tocat res encara):

1. `scripts/picasa_to_photos.py` — **descartat el mòdul OAuth** (API morta). Es pot aprofitar només la part de *collect* (scanning de posts → corpus per compte). Decidir si queda com a `collect_albums.py` o es refà directament la Fase 1 amb l'anàlisi ja feta.
2. `scripts/valida_links.py` — donat un fitxer `<autor> → [urls]`, comprova status i títol públic de cada link.
3. `scripts/aplica_substitucions.py` — donat un mapa "URL antiga → URL nova", reemplaça al front matter i al cos dels posts i reporta el nombre de canvis.

Tot ells sota `scripts/`, sense noves dependències (stdlib), d'acord amb el projecte.

## 6. Riscos i consideracions

- **Pèrdua permanent**: els àlbums que el propietari no tingui a Google Photos (perquè no s'hi van migrar mai o es van esborrar amb l'Album Archive) són **irrecuperables**: no queden a enlloc. Això pot ser més o menys important segons l'autor; la Fase 1 ho ha de quantificar per compte.
- **Enllaços compartits nous són públics**: qui els retorna dona consentiment a publicar-los al web. Assegurar-ho al full de treball.
- **L'autor sense accés al seu compte antic**: opció de deixar-ho pendent o mirar de veure si l'àlbum s'ha recreat amb un altre nom.
- **Doble tipus d'aparició**: un mateix àlbum pot estar enllacat com a `album_url` i també dins del cos del post; la substitució ha de cobrir els dos (l'anàlisi actual compta cos i front matter).
- **Privacitat**: no hi ha cap dada personal de tercers al corpus; els enllaços són àlbums públics de cada autor.

## 7. Decisions editorials pendents (per als casos sense recuperació)

Per definir amb el propietari / equip:
- Posts amb enllaç mort i sense còpia accessible: (a) eliminar el camp `album_url` i el botó "Veure tot l'àlbum", (b) mantenir l'enllaç (deixa de funcionar), (c) nota "(àlbum ja no disponible)".
- Els 3 de Flickr (403, privats): idem.
- Els 10 malformats/dominis morts (000): normalment (a).
- Marcadors temporals: un lloc al web (p.ex. nota del peu o pàgina d'estat del concurs) on consti que es treballa a recuperar els àlbums històrics?

## 8. Acceptació

- [ ] Aprovat el pla general (aquesta secció amb el "sí" de l'usuari).
- [ ] Aprovat que cada autor rebi el seu full de treball (correu).
- [ ] Aprovada l'estratègia per als casos no recuperables (§7).
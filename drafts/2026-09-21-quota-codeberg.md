# Quota de Codeberg: diagnòstic, petició i solució definitiva

> Data: 2026-09-21. Investigació verificada des de l'API de Codeberg i la documentació
> oficial (blog.codeberg.org i docs.codeberg.org). Resum de la sessió.

## 🚨 COM ES PODRIA DEMANA: 1 clic

1. Obre `https://codeberg.org/Codeberg-e.V./requests/issues/new?template=storage-quota.yaml`.
   Si el template no es prefereix, tria «Increase storage quota(s)» del menú de templates.
2. Omple els camps amb el text de la secció «Text de la petició» d'aquest document.
3. Envia. Normalment l'owner (fnetX) aprova amb un "lgtm" (casos reals: 2103, 2026, 2109).

(Cal estar loguejat a Codeberg amb l'usuari `linuxbcn`.)

## Què ha passat

El `git push` al repositori `linuxbcn/9bi` falla amb:

```
remote: Forgejo: Quota exceeded ... pre-receive hook declined
```

És el **límit d'emmagatzematge git** de Codeberg, que s'aplica **per usuari/organització**
(namespace), NO per repositori.

## La quota (font: blog.codeberg.org, "New storage limits on Codeberg", 2025-05-14)

- **Git repository storage: 750 MiB** per usuari o organització.
- LFS / Packages / Releases / Attachments: 1,5 GiB addicionals (no ho usem).
- Les excepcions es demanen al repo **`Codeberg-e.V./requests`** amb un template
  (`ISSUE_TEMPLATE/storage-quota.yaml`), obrint una issue `[STORAGE]`.
- Clar en la política: *"There is no intention of monetizing you based on limits and
  quotas! So there is no quota for valid use-cases!"* (FAQ oficial). Els augments per
  ús legítim s'aproven gratuïtament (casos reals: issues 2103, 2109, 2026...).
- No volen pas que la gent es vagi a GitHub: són una associació sense ànim de lucre i
  els casos legítims s'aproven amb un simple "lgtm" del propietari.

## Quin ús tenim (verificat via API)

```
linuxbcn/9bi          size = 767549  → ≈ 749,6 MiB   (repo del web)
linuxbcn/konsento     size = 6515    → ≈   6,4 MiB   (app interna)
linuxbcn/gestor-hores size = 9       → ≈   0,01 MiB  (gestió d'hores)
─────────────────────────────────────────────────────────────
TOTAL compte ≈ 756 MiB  >  límit 750 MiB  (sobrepas ≈ 6 MiB)
```

La mida que reporta l'API és el directori `.git` del servidor i està en **KiB**.

Per què 9bi pesa tant si les **fotografies reals són externes** (àlbums de Google
Photos enllaçats des del camp `album_url`, covers i miniatures petites a
`static/images/`)? Perquè **cada deploy** amb el mecanisme antic feia:

1. `git init -b pages` en un directori temporal net (raó senzilla: cap dependència del
   repo local).
2. `git add -A` de TOTS els fitxers del build (≈164 MiB).
3. `git push -f HEAD:pages`.

Cada force-push deixava al servidor l'snapshot sencer anterior com a **objectes orfes**
(unreachable) que cap ref no referència. Aquests objectes **continuen contant per a la
quota** fins que el servidor fa un garbage collection. Amb molts deploys de ~160 MiB
cadascun, s'acumulen centenars de MiB. El repo local comprimit només fa ~254 MiB
(pack 229 MiB), que és la mida *honesta*.

## La solució (3 potes)

1. **Demanar un augment modest de quota** (això desbloqueja el push avui):
   - Repo: `https://codeberg.org/Codeberg-e.V./requests/issues/new`
   - Template: **"Increase storage quota(s)"** → títol `[STORAGE] ...`, etiqueta
     `resources/storage`.
   - Git Repositories: **1500 MiB** (opció de menú del formulari), suficient per a la
     història actual + el que vingui amb el deploy incremental. LFS: 1500 MiB (default,
     no usem LFS).
   - Argumentació: associació fotogràfica **sense ànim de lucre** de Nou Barris
     (Barcelona), arxiu cultural municipal, lloc públic, preferim **programari lliure**
     (no anar-nos-en a GitHub), les fotos originals són enllaços externs (no
     emmagatzemem gaire res), ús eficient garantit amb el deploy incremental.
   - Text llest per enganxar: vegeu el bloc "Text de la petició" més avall.

2. **Deploy incremental** (causa arrel; implementat a `sync-9bi.sh` 2026-09-21):
   - En lloc de `git init` + `force-push` del build sencer, mantenim un clon persistent
     de la branca `pages` a `.pages-deploy/`, hi sincronitzem el build i fem un
     **push normal (fast-forward)**: només es pugen els fitxers que canvien.
   - Això deixa de crear objectes orfes → el repo no tornaria a créixer per si sol.

3. **Garbage collection al servidor** (opcional, per quan l'augment no fos necessari):
   - L'única via és que Codeberg el faci (no ho podem forçar nosaltres). Hi ha issues
     prèvies demanant-ho. Un cop desbloquejat el push, amb el deploy incremental el
     creixement s'atura; amb un GC el repo baixaria cap als ~254 MiB reals.

## Text de la petició (per omplir el formulari `[STORAGE]`)

**Títol de la issue:**

```
[STORAGE] Augment modest de quota per a linuxbcn — lloc web d'associació fotogràfica sense ànim de lucre
```

**Description (camp lliure del formulari):**

```
Hello, and thank you for maintaining Codeberg.

I am the maintainer of the public repository `linuxbcn/9bi` (https://codeberg.org/linuxbcn/9bi),
the new website of a non-profit photography association from Nou Barris (Barcelona): 9 Barris Imatge.
We have migrated our blog (3.006 posts documenting the district since 2002) from Blogger to Hugo
and moved it to Codeberg precisely because we prefer free/libre software and do not want to depend
on proprietary services such as GitHub.

The account `linuxbcn` is currently just above the default 750 MiB git quota (usage ≈ 756 MiB;
repo 9bi ≈ 749.6 MiB). The size is not caused by storing photos: our albums are external links
(Google Photos) referenced from the posts, and only small cover images are kept in the repository.
The bloat comes from our previous deploy method, which force-pushed a full ~160 MB snapshot of the
site on every release, leaving orphaned objects on the server. We have already fixed this by moving
to an incremental deploy (only changed files are pushed), so the repository will not keep growing
by itself.

Since we are a non-profit association with a modest, mostly-text footprint, a small increase of the
git quota to 1500 MiB is more than enough. We want to be good users of the platform, not a burden,
and we are happy to work as efficiently as possible.

Thank you for your time.
```

**For organizations:** (deixar buit — és un compte personal)

**Git Repositories:** `1500 MiB`

**Git LFS, Packages, Releases and Attachments:** `1500 MiB` (default; no en fem ús)

## Estat després de la petició

- **2026-09-22 — RESOLT sense augment**: Codeberg va respondre que han fet
  garbage collection del repo i ara ocupa **22 MiB**: *"I triggered GC for the
  mentioned repository and it's now 22MiB. As such I don't believe you would
  need a quota raise for now."* → **no cal augment de quota**, el push queda
  desbloquejat. T-008 queda desbloquejat.
- Mentre la quota estava excedida, cap push (ni a `main` ni a `pages`).
- Els commits locals queden fets i nets (no es perden).
- Ara cal pujar: els commits de main pendents + un deploy per publicar.
- Si mai Codeberg cobrès l'augment (no és la política), pla B documentat: migrar a
  GitHub (github.com) — però hi voldríem arribar mai, preferim 100% programari lliure.

## Registre de verificacions (per a l'auditoria)

- 2026-09-21: API `codeberg.org/api/v1/repos/linuxbcn/<repo>` → sizes precedents.
- 2026-09-21: blog oficial quota → límits i procediment `Codeberg-e.V./requests`.
- 2026-09-21: FAQ oficial → "no quota for valid use-cases"; más per sines a GitHub
  (mirroring de repos de GitHub no permès).
- 2026-09-21: issues reals aprovades gratuïtament a `Codeberg-e.V./requests`
  (#2103, #2026, #2109) i la "request-bot" que tanca amb lgtm.
- 2026-09-21: template literal `storage-quota.yaml` recuperat.
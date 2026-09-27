# Reobrir l'issue #2522 de Codeberg (quota) — text preparat

> Data: 2026-09-27. Text redactat i **NO enviat** (cal enviar-lo des del navegador,
> logged in com a `linuxbcn`). Dades verificant l'API pública de Codeberg el mateix dia.

## Situació real (verificada el 2026-09-27)

- **Issue #2522**: tancada el 2026-09-23 per Gusted (*«I triggered GC for the mentioned
  repository and it's now 22MiB. As such I don't believe you would need a quota raise
  for now.»*). El 2026-09-24 vam respondre explicant que el GC no aguantava perquè el
  deploy tornava a omplir el repo, i demanant l'augment. **Des de llavors: cap resposta**
  i el títol continua marked "closed" (Codeberg no el va reobrir).
- **Canvi de fons (el que fa que el text canvii)**: la producció del web **ja és GitHub
  Pages** (des del 2026-09-24). Codeberg **ja no publica res**: el `pages` branch és el
  darrer deploy fet des de Codeberg i no el tornarem a pujar. Volem conservar `main`
  només com a **còpia de seguretat** del codi i del seu historial.
- **Mida actual del compte** (API, KiB → MiB):

  | repositori | mida |
  |---|---|
  | `linuxbcn/9bi` | 770.790 KiB = **752,7 MiB** |
  | `linuxbcn/konsento` | 6.515 KiB = 6,4 MiB |
  | `linuxbcn/gestor-hores` | 9 KiB ≈ 0,0 MiB |
  | **total** | **≈ 759,1 MiB** (límit 750 MiB → **9 MiB per sobre**) |

- **Branches a Codeberg**: `pages` → `60688d207` (2026-09-24 08:52, l'últim build) ·
  `main` → `e9b8ab5bc` (2026-09-24 01:27).
- La causa de la mida és **la branca `pages`**: el mètode de deploy antic feia
  `git init` + `push -f` del build sencer (~164 MiB) a cada publicació, deixant
  objectes orfes. Ja no ho fem (el 2026-09-21 vam passar a un deploy incremental i el
  2026-09-24 ens vam traslladar a GitHub Pages).

## Què demanem (en aquest ordre)

1. **Cap excepció de quota**: esborrem nosaltres mateixos la branca `pages`
   (`git push codeberg --delete pages`) i demanem un GC. `main` (codi, configuració del
   CMS i historial complet) **no es toca**.
2. Si a ells els resulta més còmode, **augment modest de quota** (1500 MiB) per a
   `linuxbcn`, ja que no publiquem aquí i el repo no creixerà sol.

## Com enviar-lo

1. Obre <https://codeberg.org/Codeberg-e.V./requests/issues/2522> loguejat com a `linuxbcn`.
2. Prem el botó **«Reopen issue»** del timeline (si no apareix perquè l'issue és d'un
   altre usuari, no cal: **fes igualment el comentari**; el que importa és que quedi
   registrat).
3. Enganxa el text de l'apartat següent al comentari i envia.

## Text del comentari (anglès, per enviar)

```text
Hello,

Thank you for the GC on Sep 23, and for replying to me on Sep 24. Since then the
situation has changed, and I think there is now a fix that does not need any quota
exception at all.

Where we stand now (2026-09-27)

- The website is no longer published from Codeberg. On Sep 24 we moved production to
  GitHub Pages, so linuxbcn/9bi is now only a backup mirror of the source and its
  history. We do not push any build to Codeberg any more.
- Current usage of the account linuxbcn: 9bi = 752.7 MiB, konsento = 6.4 MiB,
  gestor-hores = 0.01 MiB, total ~759.1 MiB, which is about 9 MiB above the 750 MiB
  limit, so pushes are declined.
- Almost all of that 752.7 MiB is the old pages branch: until Sep 21 our deploy
  method force-pushed a full generated snapshot of the site (~160 MB) on every
  release, which left orphaned objects on the server. That branch is frozen at
  60688d207 (Sep 24) and we have no use for it any more. The repository is not
  photographs either: the albums are external links (Google Photos) and only small
  cover images are stored.

What we would like to ask

The simplest option needs nothing from you: we are happy to delete the pages branch
ourselves (git push codeberg --delete pages), which should bring the account back
below the limit; a GC afterwards would settle the space. main - source, CMS
configuration and the full commit history - would stay untouched, and from now on we
would only push source changes of a few MB per month. Just say the word and we do it,
or you are welcome to remove the branch directly.

Alternatively, if that is simpler for you, a modest increase of the git quota for
linuxbcn (1500 MiB) would also solve it, now that we publish elsewhere and the
repository will not grow on its own.

We do want to keep Codeberg as our backup; we only need a few MB of headroom, and we
prefer to fix this ourselves whenever possible.

Thank you for your time, and for maintaining Codeberg.
```

## Alternativa ràpida (si es vols intentar primer el de la via 1)

Si prefereixes no esperar resposta, **esborra tu mateix la branca `pages`** des del
panell de Codeberg (repo `linuxbcn/9bi` → *Branches* → `pages` → *Delete*), o bé:

```bash
git push codeberg --delete pages
```

Això hauria de deixar el compte per sota del límit i el torn següent es podrà pujar
amb normalitat. **Avís**: perdries l'historial del build publicat a Codeberg, però
`main` (codi + historial) es conserva. No ho facis sense decidir-ho: Codeberg és el
nostre backup.

## Registre de verificacions (per a l'auditoria)

- 2026-09-27: `GET /api/v1/repos/Codeberg-e.V./requests/issues/2522` → `state: closed`,
  `closed_at: 2026-09-23T14:11:38+02:00`, 2 comentaris.
- 2026-09-27: `GET .../issues/2522/comments` → Gusted (2026-09-23) + linuxbcn (2026-09-24).
  Cap resposta després.
- 2026-09-27: `GET /api/v1/users/linuxbcn/repos` → mides de la taula de dalt.
- 2026-09-27: `GET /api/v1/repos/linuxbcn/9bi/branches` → `pages` (60688d207),
  `main` (e9b8ab5bc).

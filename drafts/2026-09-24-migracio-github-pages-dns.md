# Migració a GitHub Pages — canvis DNS de 9barrisimatge.org (2026-09-24)

> Producció ara construeix i publica GitHub Actions (`112books/9bi`). Un cop fets
> aquests canvis de DNS, el domini l'ha de servir GitHub Pages. Codeberg queda com
> a backup (repo `linuxbcn/9bi`) — no esborrar res.

## Objectiu dels registres

GitHub Pages serveix el domini **sols amb A records** (apex), i el `www` ha
d'apuntar per CNAME a `112books.github.io` (GitHub redirigeix www → apex automàticament).

## Registres a canviar

### 1. Apex `9barrisimatge.org` — registres A

| Tipus | Nom | Valor | TTL |
|---|---|---|---|
| A | `@` | **185.199.108.153** | 3600 |
| A | `@` | **185.199.109.153** | 3600 |
| A | `@` | **185.199.110.153** | 3600 |
| A | `@` | **185.199.111.153** | 3600 |

- **ELIMINAR** el registre A antic de Codeberg: `217.197.84.141`
- **ELIMINAR** la AAAA (`AAAA` no es fan servir): `2a0a:4580:103f:c0de::2`
  (GitHub Pages **no** té suport IPv6 per a domini custom; sense AAAA el navegador
  cau a IPv4, que és el que volem.)

### 2. `www.9barrisimatge.org` — registre CNAME

| Tipus | Nom | Valor | TTL |
|---|---|---|---|
| CNAME | www | **112books.github.io** | 3600 |

- **ELIMINAR** el CNAME antic a Codeberg: `codeberg.page`
- **ELIMINAR** el registre A de `www` si n'hi ha (`217.197.84.141`)

### 3. Registres TXT — es poden DEIXAR (no interfereixen)

- `_git-pages-repository.9barrisimatge.org` = `"https://codeberg.org/linuxbcn/9bi.git"`
- `_git-pages-repository.www.9barrisimatge.org` = `"https://codeberg.org/linuxbcn/9bi.git"`
- `v=spf1 a mx include:formsubmit.co ~all` (correu del formulari — **conservar**)
- `google-site-verification=...` (**conservar**)

## Propietats per canviar de lloc

| Propietat | Codeberg (abans) | GitHub (ara) |
|---|---|---|
| Definis el domini custom | al repo Pages/domini | `repo → Settings → Pages → Custom domain` (ja fet: `9barrisimatge.org`) |
| TLS | automàtic per Let's Encrypt | automàtic (GitHub emet el certificat als pocs minuts d'apuntar la DNS) |
| Webhooks del domini | repos Codeberg (els 4) | no cal cap: GitHub Pages es publica sol |

## Verificació després del canvi (5–60 min de propagació)

1. `dig +short 9barrisimatge.org A` → ha de tornar les 4 IP (185.199.x.x)
2. `curl -sI "https://9barrisimatge.org/?v=$RANDOM" | grep -i last-modified`
   → data = build de GitHub (fresc a cada push a `main`)
3. `curl -s -o /dev/null -w "%{http_code}" https://9barrisimatge.org/stats/` → 200

## Com tornar a Codeberg si mai calgués (backup)

- Repos: `linuxbcn/9bi` i `112books/9bi` estan sincronitzats a `main`.
- La DNS es pot revertir posant altra vegada els A records de Codeberg
  (`217.197.84.141`) i el CNAME de `www` a `codeberg.page`.
- El desplegament de Codeberg continua disponible via `sync-9bi.sh deploy
  production` (webhooks encara configurats al repo Codeberg).
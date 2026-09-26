---
title: "Sistema de votació del públic"
tipo: Documentació tècnica
date: 2026-09-26T00:00:00
draft: true
---

El sistema de votació és una aplicació web pròpia (mòdul `votacio` de la suite Taro), allotjada al servidor de LinuxBCN. Funciona sense dependències externes: Python estàndard + SQLite.

## Com funciona per al visitant

1. El visitant escaneja el codi QR de l'exposició (o entra la URL manualment).
2. El navegador demana permís de geolocalització. Cal acceptar-ho per poder votar.
3. El sistema comprova que el dispositiu és dins el radi del Casal de Barri de Prosperitat (500 m). Si és fora, rebutja el vot.
4. El visitant escriu el número de l'obra que vol votar.
5. El sistema registra el vot de forma anònima. Des del mateix dispositiu, **un sol vot per obra**.

## Fitxers al servidor

```
~/apps/vots-cordoncillo/       ← codi de l'aplicació (fora del docroot)
    app.py                     ← aplicació principal
    config.ini                 ← CONFIGURACIÓ (secrets, dates, obres)
    data.db                    ← base de dades SQLite (vots)
    deploy/
        start.sh               ← arrenca el procés (port 8301)
        stop.sh                ← atura el procés
        watchdog.sh            ← reinicia si el procés ha caigut

~/www/vots-cordoncillo/        ← docroot (proxy cap a l'aplicació)
    .htaccess                  ← redirect http→https + proxy
```

## Paràmetres de `config.ini`

Els paràmetres més importants de l'edició, a la secció `[edicio]`:

| Paràmetre | Valor actual | Descripció |
|---|---|---|
| `data_inici` | `2026-09-25T00:00:00` | Inici de la finestra de votació |
| `data_fi` | `2026-10-31T23:59:59` | Fi de la finestra de votació |
| `vot_limit` | `0` (mode proves) | `0` = sense límit; `1` = un vot per obra per dispositiu (producció) |
| `revote_minutes` | `10` | Minuts per tornar a votar la mateixa obra (0 = mai) |
| `mode_geo` | `hard` | `off` / `soft` (avisa) / `hard` (bloqueja si fora del radi) |
| `lat` | `41.441623` | Latitud del punt del concurs (Casal Prosperitat) |
| `lon` | `2.179794` | Longitud del punt del concurs |
| `radi` | `500` | Radi en metres per al geofencing |

A la secció `[obres]`, les obres en format `N = Títol · Autor · Categoria` (una per línia).

**Important:** els canvis a `config.ini` no es propaguen fins a reiniciar el servei. Els canvis de les obres requereixen esborrar `data.db` (vegeu procediments).

## Gestió del servei (SSH)

Connectar-se al servidor:
```bash
ssh linuxbcn0@vl28359.dinaserver.com
```

Anar a la carpeta de l'aplicació:
```bash
cd ~/apps/vots-cordoncillo
```

Reiniciar el servei (per aplicar canvis de `config.ini`):
```bash
deploy/stop.sh && deploy/start.sh
```

Comprovar que funciona:
```bash
curl https://vots-cordoncillo.linuxbcn.com/health
# Ha de respondre: ok
```

Veure el log en directe:
```bash
tail -f ~/logs/vots-cordoncillo.log
```

## Canviar les obres de l'exposició

Les obres es carreguen a la base de dades **en crear-se per primera vegada**. Per canviar-les:

1. Editar `config.ini` → secció `[obres]`: afegir/modificar les línies `N = Títol · Autor · Categoria`.
2. Aturar el servei: `deploy/stop.sh`
3. **Esborrar la base de dades:** `rm data.db`  
   ⚠️ Això esborra tots els vots registrats fins al moment.
4. Tornar a arrencar: `deploy/start.sh`

Per tant, cal definir les obres definitives **abans** d'obrir la votació real.

## Panell d'administració

URL: `https://vots-cordoncillo.linuxbcn.com/admin/`

Des del panell es pot:
- Veure el **recompte de vots** per obra en temps real
- Descarregar l'**export CSV signat** (per al recompte oficial)
- **Tancar la votació** (acció irreversible — fer-ho només el dia del lliurament de premis)

La contrasenya és el camp `admin_secret` de `config.ini`.

## Seguretat

- Els vots s'emmagatzemen de forma **anònima**: no es guarden nom, correu ni coordenades exactes.
- Cada dispositiu s'identifica per una cookie `vid` (codi aleatori, HttpOnly), no per empremta digital.
- El sistema comprova que la votació s'ha fet **dins del radi del Casal** (geofencing `hard`).
- Hi ha protecció CSRF, rate limit per IP i límit de mida del cos de les peticions.

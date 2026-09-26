---
title: "Procediments del concurs"
tipo: Documentació tècnica
date: 2026-09-26T00:00:00
draft: true
---

Procediments pas a pas per a cada fase del concurs. Seguir aquest ordre evita errors el dia de l'exposició.

## Abans de l'exposició (setmana prèvia)

### 1. Definir les obres finalistes

Preparar la llista definitiva d'obres: número, títol, autor i categoria. Format per a `config.ini`:

```ini
[obres]
1 = Títol de l'obra · Nom Autor · A
2 = Títol de l'obra · Nom Autor · B
3 = Títol de l'obra · Nom Autor · C
```

Les categories habituals: **A** (color, tema lliure), **B** (blanc i negre, tema lliure), **C** (Josep Antón Cordoncillo, tema específic).

### 2. Configurar el servidor per a producció

Connectar al servidor:
```bash
ssh linuxbcn0@vl28359.dinaserver.com
cd ~/apps/vots-cordoncillo
nano config.ini
```

Canvis obligatoris a `[edicio]`:
- `data_inici` → data i hora d'inici de l'exposició (ex: `2026-12-01T00:00:00`)
- `data_fi` → data i hora de tancament (ex: `2026-12-15T23:59:59`)
- `vot_limit = 1` → un sol vot per obra i dispositiu
- `revote_minutes = 0` → desactivar el re-vot de proves

I a `[obres]`: substituir les obres de prova per les definitives.

### 3. Esborrar la base de dades i reiniciar

⚠️ Aquest pas esborra tots els vots de proves. Fer-ho **abans** d'obrir al públic.

```bash
deploy/stop.sh
rm data.db
deploy/start.sh
```

Verificar que tot funciona:
```bash
curl https://vots-cordoncillo.linuxbcn.com/health
# Ha de respondre: ok
```

Fer una prova de vot real des del mòbil, dins del Casal, per confirmar que el geofencing funciona.

### 4. Actualitzar el cartell QR

Verificar que la pàgina `https://9barrisimatge.org/concurs/votacio/` mostra el QR correcte i les instruccions actualitzades. Imprimir el cartell des del botó «Imprimir» de la pàgina.

### 5. Verificar el certificat SSL

El certificat del subdomini `vots-cordoncillo.linuxbcn.com` venç el **2026-12-24**. Verificar que Dinahosting el renova automàticament abans de l'exposició (1–15 desembre). Si no s'ha renovat, renovar-lo manualment des del panell de Dinahosting.

---

## El dia de la votació (durant l'exposició)

- Penjar el **cartell QR imprès** en un lloc visible de l'exposició.
- Cada obra ha de tenir el seu **número** visible al costat.
- Comprovar periòdicament el panell d'administració per veure que arriben vots: `https://vots-cordoncillo.linuxbcn.com/admin/`
- Si hi ha problemes tècnics (el QR no funciona, la pàgina no carrega), comprovar:
  1. `curl https://vots-cordoncillo.linuxbcn.com/health` → ha de respondre `ok`
  2. Si no respon, reconectar per SSH i reiniciar: `deploy/stop.sh && deploy/start.sh`

---

## Tancament de la votació i recompte final

### 1. Descarregar l'export CSV

Abans de tancar, descarregar l'export des del panell d'administració. L'arxiu CSV conté tots els vots amb signatura HMAC per verificar-ne l'autenticitat.

### 2. Tancar la votació

Des del panell d'administració (`/admin/`), prémer el botó «Tancar la votació». Aquesta acció és **irreversible**: el formulari de vot deixa d'acceptar vots nous.

Fer-ho **el dia del lliurament de premis** (18 de desembre), just abans de l'acte, un cop acabat el període d'exposició.

### 3. Anunciar el guanyador

La fotografia amb més vots al recompte final del CSV és el **Premi del Públic**. Anunciar-lo a l'acte de lliurament de premis (18 de desembre, ~19h al Casal de Barri de Prosperitat).

### 4. Publicar els resultats

Publicar un article al web amb els guanyadors de totes les categories, incloent el Premi del Públic. Afegir les etiquetes habituals del concurs.

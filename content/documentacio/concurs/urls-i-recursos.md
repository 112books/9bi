---
title: "URLs i recursos del concurs"
tipo: Documentació tècnica
date: 2026-09-26T00:00:00
draft: true
---

Recull de totes les adreces i recursos necessaris per administrar el concurs. No cal recordar-les: consulta aquí.

## Web públic

| Recurs | URL |
|---|---|
| Pàgina del concurs | `https://9barrisimatge.org/concurs/` |
| Cartell QR per imprimir | `https://9barrisimatge.org/concurs/votacio/` |
| Etiquetes del concurs | `https://9barrisimatge.org/tags/concurs-fotogr%C3%A0fic-josep-ant%C3%B3n-cordoncillo/` |

El **cartell QR** (`/concurs/votacio/`) és la pàgina pensada per imprimir i penjar a l'exposició. Conté el codi QR i les instruccions per votar. Quan s'imprimeixi, verificar que el QR apunta a la URL correcta del formulari de vot.

## Sistema de votació

| Recurs | URL |
|---|---|
| Formulari de vot (públic) | `https://vots-cordoncillo.linuxbcn.com/v/cordoncillo-2026` |
| Panell d'administració | `https://vots-cordoncillo.linuxbcn.com/admin/` |
| Comprovació de salut | `https://vots-cordoncillo.linuxbcn.com/health` |

El **panell d'administració** (`/admin/`) permet:
- Veure el recompte de vots en temps real
- Descarregar l'export CSV signat (per al recompte final)
- Tancar la votació

La contrasenya d'administrador és al fitxer `~/apps/vots-cordoncillo/config.ini` al servidor, camp `admin_secret`.

## Infraestructura

| Recurs | Dades |
|---|---|
| Servidor | `vl28359.dinaserver.com` (IP: 82.98.166.123) |
| Usuari SSH | `linuxbcn0` |
| Clau SSH | `id_ed25519` (ja autoritzada) |
| Port SSH | 22 (estàndard) |
| Certificat SSL | vàlid fins al 2026-12-24 (cobreix el període de l'exposició) |

Connexió SSH:
```
ssh linuxbcn0@vl28359.dinaserver.com
```

## CMS i repositori

| Recurs | URL |
|---|---|
| CMS (Sveltia) | `https://9barrisimatge.org/admin/` |
| Repositori GitHub | `https://github.com/112books/9bi` |
| GitHub Actions (deploys) | `https://github.com/112books/9bi/actions` |
| Estadístiques (GoatCounter) | `https://9bi.goatcounter.com` |
| Dashboard d'estadístiques | `https://9barrisimatge.org/stats/` |

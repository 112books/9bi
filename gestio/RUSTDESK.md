# RustDesk — suport remot per als editors

> Documentat el 2026-11-15, per indicació de l'usuari. Eina que fa servir el
> col·lectiu per acompanyar editors que no són tècnics (alta al gestor, token,
> primera publicació) veient-ne la pantalla i, si cal, controlant-la.

## Què és

**RustDesk** és programari lliure (**GPLv3**) de control remot d'escriptori:
Windows, macOS i Linux, amb client i servidor al mateix paquet. Es pot fer
servir amb els **relés públics** de la comunitat o autoallotjar-lo.

- **Instal·lat**: al Mac del col·lectiu, versió **1.4.9** (`/Applications/RustDesk.app`, comprovat el 2026-11-15).
- **A Windows**: el company descarrega el `.exe` de `https://rustdesk.com`; la versió **portable** no s'instal·la. Si Windows mostra l'avís de SmartScreen: *Més informació → Executa igualment*.

## Com es fa una sessió

1. La persona que necessita ajuda obre RustDesk i passa el seu **ID de 9 xifres** i la **contrasenya temporal**.
2. Qui ajuda obre RustDesk al seu ordinador, introdueix l'ID i la contrasenya.
3. La persona que rep la connexió l'ha d'acceptar; a partir d'aquí veu la pantalla i, si vol, la controla.
4. En acabar, es tanca la sessió.

## Regles de la casa

- **Consentiment explícit**: la sessió s'obre per ajudar i s'ha de tancar en acabar. Qui rep la connexió ha de veure la pantalla mentre la sessió és oberta.
- **Contrasenya temporal, mai permanent**: no s'activa l'accés desatès. Si algú el necessita per a una feina recurrent, es decideix a part.
- **No es grava** la pantalla ni s'envien captures amb dades de tercers.
- **L'ID i la contrasenya no es publiquen** en canals públics (Telegram obert, xarxes): només per correu, telèfon o el grup privat.
- La pantalla pot mostrar **dades personals** (correu, fitxes de membres, formularis): val la mateixa cura que amb qualsevol accés a dades del col·lectiu.

## Limitacions conegudes

- Els **relés públics** de RustDesk els finança la comunitat: de vegades van lents o cauen. Si passa, es pot reintentar més tard.
- **Autoallotjar-lo** (l'opció bona per a un col·lectiu, sense dependre de tercers) demana un servidor amb ports propis; l'allotjament compartit actual no ho permet, així que de moment es fa servir el relé públic.

## Alternatives valorades i per què no

| Eina | Motiu |
|---|---|
| **Jitsi Meet** | Lliure i sense compte, però **només comparteix pantalla**, no permet controlar-la. Serveix si n'hi ha prou de dictar on s'ha de clicar |
| **Zoom** | Privatiu, i la versió gratuïta limita les sessions a 40 minuts |
| **AnyDesk, TeamViewer, Chrome Remote Desktop** | Privatius: descartats per coherència amb el projecte |

## Manteniment

- Si es fa servir sovint, val la pena revisar la versió del client (RustDesk publica versions noves sovint) i, si algun dia hi ha servidor propi, canviar els relés.
- Aquest document és intern però viu al repositori públic: **no hi ha d'haver mai** IDs, contrasenyes ni dades de persones.

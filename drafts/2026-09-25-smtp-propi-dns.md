# SMTP propi: correu de 9barrisimatge.org i formularis sense FormSubmit

> Diagnòstic verificat el 2026-09-25 amb consultes DNS i SMTP directes. Els articles d'ajuda de Dinahosting només expliquen **per què** cal SPF/DKIM/DMARC, no donen els registres ni el selector DKIM. Per tant, els registres finals s'han d'activar des del **panell `gestiondecorreo.com`** del compte Dinahosting que allotja el correu de 9barrisimatge.org.

## 1. Diagnòstic del correu actual (verificat)

| Comprovació | Estat |
|---|---|
| Servidor MX | `10 mail.9barrisimatge.org` |
| Adreça A de `mail.9barrisimatge.org` | `82.98.166.123` (Dinahosting) |
| PTR invers (`82.98.166.123`) | `vl28359.dinaserver.com` |
| SPF | `v=spf1 a mx include:formsubmit.co ~all` — funcional via `mx` |
| DKIM | **Cap registre publicat** (s'han provat 22 selectors habituals). L'usuari generarà el registre des del panell; cal el selector i el valor TXT |
| DMARC | `v=DMARC1; p=none; rua=mailto:info@9barrisimatge.org` |
| MTA-STS / TLS-RPT / BIMI | **No publicats** (baixa prioritat: el web és a GitHub Pages i no hi pot penjar el fitxer `.well-known/mta-sts.txt`) |
| SMTP port 465 (TLS implícit) | Connecta. Certificat `CN=*.correoseguro.dinaserver.com` (GlobalSign), vàlid 07/08/2026–22/02/2027 |
| SMTP port 587 (STARTTLS) | Connecta. Autenticació `AUTH PLAIN LOGIN` oferta |

**FCrDNS correcte**: la IP resolve a `mail.9barrisimatge.org` i a l'inrevés.

## 2. Registres DNS finals (a aplicar des del panell, NO a mà)

### 2.1 SPF — netejar quan el formulari passi al servidor propi

Actualment inclou `include:formsubmit.co`, que autoritza FormSubmit a enviar en nom del domini. Quan els formularis deixin d'usar FormSubmit, aquesta autorització ja no cal:

```
v=spf1 mx ~all
```

Es manté `mx` perquè `mail.9barrisimatge.org` és l'únic servidor autoritzat a enviar. El `~all` (soft fail) és preferible a `-all` fins que hi hagi DKIM publicat; quan el DKIM sigui actiu, passar a `-all` perquè qualsevol altre servidor que intenti enviar quedi rebutjat.

### 2.2 DKIM — **pendent del selector**

Dinahosting genera el selector i el valor TXT al panell. Cal:

1. Obrir el panell `gestiondecorreo.com` del compte que allotja `@9barrisimatge.org`.
2. Secció **DKIM**: generar/activar la clau per al domini `9barrisimatge.org`.
3. El panell mostra el **selector** (normalment una cadena hexadecimal) i el **valor** complet.
4. Publicar a DNS com a TXT: `selector._domainkey.9barrisimatge.org` amb el valor que doni el panell.
5. Guardar el selector: és el que caldrà posar a la configuració del client SMTP (capçalera `DKIM-Signature: d=9barrisimatge.org, s=<selector>` — si el servidor de correu de Dinahosting el signa automàticament en enviar, no cal generar la signatura a mà).

### 2.3 DMARC — mantenir i endureix progressivament

Actualment `p=none` (només monitoritza). Després que SPF i DKIM estiguin verificats:

1. Setmana 1-2: `v=DMARC1; p=none; rua=mailto:info@9barrisimatge.org` (es manté).
2. Quan els correus s'enviïn realment amb DKIM signat: pujar a `p=quarantine`.
3. Un cop cap correu legítim arriba a spam: pujar a `p=reject`.

### 2.4 Opcionals per a lliurabilitat

- **MTA-STS** (`mta-sts.9barrisimatge.org` TXT + fitxer `/.well-known/mta-sts.txt` publicat pel web) i **TLS-RPT** (`_smtp._tls.9barrisimatge.org` TXT). El web és GitHub Pages, on no es pot penjar el fitxer `.well-known`; es pot fer amb un servei de host estàtic o no fer-ho. Prioritat baixa: no és necessari per resoldre l'actualitat.
- **BIMI** (`default._bimi.9barrisimatge.org`): requereix DMARC `p=quarantine` o `p=reject` i un VMC valid. Fora d'abast ara.

## 3. Enviament SMTP propi amb Python (sense dependències)

Per als formularis de la web (contacte, incorporació de socis), en lloc de FormSubmit:

- Servidor: `mail.9barrisimatge.org` (port 465 TLS implícit, o 587 STARTTLS).
- Autenticació: `AUTH LOGIN` amb l'usuari complet (`info@9barrisimatge.org`).
- Sense biblioteques: `smtplib` + `email.message` de la biblioteca estàndria.
- `EmailMessage` permet construir correus amb capçaleres correctes (`From`, `To`, `Subject`, `Reply-To`) perquè es visualitzin bé a Gmail i no acabin a spam per manca de capçaleres mínimes.
- L'enviament ha d'incloure un text pla i una versió HTML opcional; una `multipart/alternative` és el patró correcte.

### Fitxers de configuració (mai al repositori)

- `config.ini` al servidor (gitignored): servidor SMTP, port, usuari, contrasenya, remitent.
- Alternativa: variables d'entorn `FORMULARIS_SMTP_USER` / `FORMULARIS_SMTP_PASSWORD`.
- La contrasenha **mai** dins del codi ni del repositori.

## 4. Subdomini per als formularis (`linuxbcn.com`)

`9barrisimatge.org` és allotjat a GitHub Pages (sense allotjament PHP/Python). Per tant els formularis s'han de servir des del hosting Dinahosting, al domini `linuxbcn.com`:

| Comprovació | Estat |
|---|---|
| `linuxbcn.com` i `www.linuxbcn.com` | resolen a `82.98.166.123` (servidor HTTP de Dinahosting) |
| `formularis.linuxbcn.com` | **Creat el 2026-09-25** a la carpeta `www/formularis`; resol a `82.98.166.123` |
| `vot-cordoncillo.linuxbcn.com` | **NXDOMAIN** — encara no creat |

Passos per deixar el servei engegant (els ha de fer la persona a la que correspon el panell):

1. Pujar el contingut de `modules/formularis/` a la carpeta `www/formularis` del servidor (README.txt, app.py, passenger_wsgi.py, config.example.ini, i18n/).
2. Activar el certificat Let's Encrypt del subdomini. Requisit: `linuxbcn.com` ja ha de tenir un certificat Let's Encrypt activat, altrament el subdomini no el podrà obtenir.
3. Crear `config.ini` al servidor a partir de `config.example.ini`, amb `[smtp] user`, `[smtp] password` i, **obligatori**, `[general] allowed_origins = https://9barrisimatge.org`. Sense aquesta línia el servei rebutja tots els enviaments amb 403.
4. Registrar l'aplicació Python al panell (**Servidores → Otras aplicaciones**, només en Hosting Avanzado): versió de Python, arrel de l'aplicació (per exemple `www`) i ruta de l'executable WSGI (`www/formularis/passenger_wsgi.py`).
5. Comprovar `https://formularis.linuxbcn.com/health` → ha de retornar `ok`.
6. Provar un enviament real (vegeu `modules/formularis/README.txt`) i confirmar que arriba a `info@9barrisimatge.org`.
7. **Només quan el servei funcioni**, canviar els dos formularis del web (`content/contacte.md` i `content/incorpora-te.md`) perquè enviïn al servei, i corregir els textos legals que esmenten FormSubmit.

Si el pla de hosting no té la secció d'aplicacions Python, l'alternativa és un script PHP amb `fsockopen` (STARTTLS + AUTH LOGIN) servit des de la mateixa carpeta del subdomini.

## 5. Decisions preses (2026-09-25)

1. **Subdomini**: `formularis.linuxbcn.com` → carpeta `www/formularis`. Creat.
2. **Protecció dels enviaments**: en lloc del token CSRF signat (que un formulari estàtic de Hugo no pot calcular), es valida la capçalera `Origin` (i, si no hi és, el `Referer`) contra la llista `allowed_origins`, a més del honeypot i el límit de peticions per IP. **Decidit per l'usuari.**
3. **Textos legals**: autoritzat corregir els tres blocs que esmenten FormSubmit (`content/contacte.md`, `content/incorpora-te.md`, `content/privacitat.md`). **Decidit per l'usuari; pendent d'executar un cop el servei funcioni.**
4. **Contrasenya**: a `config.ini` al servidor (mai al repositori, `.gitignore` a `modules/formularis/`), amb la variable d'entorn `FORMULARIS_SMTP_PASSWORD` com a alternativa. Cap opció exposa el secret al repositori.
5. **Pla Dinahosting**: cal confirmar si el compte `linuxbcn.com` té la secció **Servidores → Otras aplicaciones** (Python/Passenger). Si no, alternativa PHP.

Altres decisions tècniques aplicades al mòdul:

- Els errors de SMTP no es mostren al navegador (abans es mostrava el detall tècnic): van al registre del servidor i al navegador li torna un 503 genèric.
- El `Reply-To` només s'afegeix si l'adreça és vàlida, i tots els camps es netegen de caràcters de control perquè no es puguin injectar capçaleres de correu.
- `allowed_origins` buit = rebutja tot (per seguretat), en lloc d'admetre-ho tot.

## 6. Registres DNS: resum operatiu

| Host | Tipus | Valor | Estat |
|---|---|---|---|
| `@` | SPF | `v=spf1 mx ~all` (netejar `a` i `include:formsubmit.co` quan els formularis deixin FormSubmit) | Pendent d'aplicar |
| `selector._domainkey` | TXT | Valor DKIM que generi el panell | Pendent d'activar al panell |
| `_dmarc` | TXT | `v=DMARC1; p=none; rua=mailto:info@9barrisimatge.org` | Actiu ✓ |

La ordre recomanada és: (1) generar DKIM al panell i publicar-lo, (2) verificar SPF+DKIM amb l'enviament d'un correu de prova a `mail-tester.com`, (3) si arriba amb puntuació alta, netejar SPF, (4) pujar DMARC a `p=quarantine` després de 2 setmanes de correu estable.

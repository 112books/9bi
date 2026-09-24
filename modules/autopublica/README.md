# autopublica — publica el web sol quan el CMS puja un post nou

Mòdul M2 de la suite. App WSGI (només stdlib) que rep el **webhook de push
de Codeberg** quan el CMS (Decap) fa commit+push a `main`, i executa el
desplegament: `git pull` → build Hugo → `push` a la branca `pages`
(la que publica Codeberg Pages). Així ningú no ha de fer res a mà: escriure
al CMS i publicar ja deixa el post al web.

## Desplegament

1. `cp config.example.ini config.ini` i omple `secret` (HMAC compartit amb
   el webhook) i `workdir` (paths reals).
2. Puja `modules/autopublica/` al panell (Passenger, patró de `votacio`).
3. A Codeberg: repo → Settings → Webhooks → **Add Webhook**:
   - URL: `<https://el-teu-domini>/hook`
   - Secret: el mateix de `config.ini`
   - Event: **Push** (branca `main`)
4. La primera vegada, confirma que el clon del repo (branca `main`) sigui al
   `workdir` i que l'usuari del procés tingui permís de push a `pages`.

## Prova sense webhook

    curl -X POST -H "Content-Type: application/json" \
      -H "X-Codeberg-Signature: <hmac-sha256-hex(cos, secret)>" \
      -d '{"ref":"refs/heads/main"}' http://localhost:8000/hook

## Endpoints

- `GET /health` — monitor
- `POST /hook` — webhook (verifica HMAC; ignora push que no sigui a `main`)

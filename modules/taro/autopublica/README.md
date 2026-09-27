# autopublica — publica el web sol quan hi ha un push al repositori

App WSGI (només stdlib) que rep el **webhook de push** del repositori i
executa el desplegament: `git pull` → build → `push` del build. Així ningú
no ha de fer res a mà: escriure al CMS i publicar ja deixa el contingut al
web.

**Si el teu web es publica amb integració contínua (GitHub Actions, GitLab
CI, Drone…), no necessites aquest mòdul:** engega el push a la branca del
web i deixa que el CI publiqui. Aquest mòdul és per a hosting on el build
s'ha de pujar directament des del servidor.

## Desplegament

1. `cp config.example.ini config.ini` i omple `secret` (el HMAC compartit
   amb el webhook) i `workdir` (el clon del repositori, a la branca del
   web).
2. Puja la carpeta al servidor. Amb Passenger, apunta-hi. Sense Passenger,
   usa un procés d'usuari darrere d'un proxy, com la resta de mòduls.
3. Crea el webhook al repositori: URL `https://el-teu-domini/hook`, el
   mateix secret, esdeveniment **Push** i la branca del web.
4. La primera vegada, comprova que el clon del `workdir` existeix i que
   l'usuari del procés hi pot fer push de la branca de build.

Variables d'entorn del `tools/deploy.sh`:

| Variable                        | Per defecte | Què fa                          |
|---------------------------------|-------------|---------------------------------|
| `AUTOPUBLICA_REPO`              | on ets      | clon del repositori              |
| `AUTOPUBLICA_DEPLOY_BRANCH`     | `main`      | branca del web                   |
| `AUTOPUBLICA_PAGES_BRANCH`      | `pages`     | branca on es puja el build       |
| `AUTOPUBLICA_PUSH_URL`          | **cap**     | on es puja (**obligatori**)     |
| `HUGO_BASEURL`                  | —           | `--baseURL` del build            |

`AUTOPUBLICA_PUSH_URL` no té valor per defecte a propòsit: el mòdul no ha de
saber on publica el teu web. Tampoc accepta credencials dins la URL
(ho rebutja); el desplegament ha d'anar amb clau SSH o amb un agent que no
l exposi.

## Prova sense webhook

Calcula la signatura del cos i envia'l:

    python3 - <<'EOF'
    import hashlib, hmac, pathlib, sys
    secret = pathlib.Path("config.ini").read_text()  # o el secret directament
    body = b'{"ref":"refs/heads/main"}'
    print(hmac.new(b"EL-TEU-SECRET", body, hashlib.sha256).hexdigest())
    EOF

    curl -X POST -H "Content-Type: application/json" \
      -H "X-Forgejo-Signature: <el-hex>  " \
      -d '{"ref":"refs/heads/main"}' http://localhost:8000/hook

## Endpoints

- `GET /health` — monitor
- `POST /hook` — webhook (verifica el HMAC; ignora els push que no siguin a
  la branca configurada)

## Capçaleres acceptades

`X-Forgejo-Signature`, `X-Gitea-Signature` i `X-Codeberg-Signature` (que és el
mateix protocol). GitLab envia un token pla en comptes d'una signatura: això
no és el mateix protocol i no es pot reutilitzar sense adaptar el codi.

## Llicència

AGPL-3.0-or-later. Vegeu `LICENSE` a l'arrel del repositori.

#!/usr/bin/env python3
"""
Genera etiquetes automàtiques per als posts marcats amb el comentari
'<!-- tags auto-generades a partir del vocabulari del blog, revisar -->'.

Utilitza Claude Haiku (model barat) per generar 4 etiquetes rellevants
a partir del títol i el contingut de cada post, escollint del vocabulari
d'etiquetes existents al blog.

Ús:
    # Primer: simular (dry-run, no escriu res)
    python3 scripts/auto_tags.py --dry-run

    # Processar tots els posts amb el comentari
    python3 scripts/auto_tags.py

    # Processar només els primers N posts (per provar)
    python3 scripts/auto_tags.py --limit 10

    # Processar un fitxer concret
    python3 scripts/auto_tags.py --file content/posts/2013/2013-09-22-11-de-septiembre-cadena-human.md

Requisit:
    Variable d'entorn ANTHROPIC_API_KEY amb una clau vàlida de l'API d'Anthropic.
    pip install anthropic   (o: pip3 install anthropic)

Seguretat:
    - El mode --dry-run no toca cap fitxer.
    - Fa còpia de seguretat del fitxer original a <fitxer>.bak abans de modificar-lo
      (es pot desactivar amb --no-backup).
    - Genera un informe a auto_tags_report.txt amb tots els canvis aplicats.
"""
import argparse
import glob
import os
import re
import sys
import time
from collections import Counter

# ---------------------------------------------------------------------------
# Configuració
# ---------------------------------------------------------------------------

MODEL = "claude-haiku-4-5-20251001"   # model barat: ~0,001 $/1k tokens entrada
MAX_TAGS = 4                           # etiquetes a generar per post
COMMENT_MARKER = "<!-- tags auto-generades"
RATE_LIMIT_SLEEP = 0.3                 # segons entre peticions (evitar throttle)

SYSTEM_PROMPT = """\
Ets un etiquetador expert del blog fotogràfic 9 Barris Imatge (Barcelona, des del 2002).
El blog documenta la vida al districte de Nou Barris: cultura, festes, fotografia, política veïnal, música, activisme, etc.

Tasca: donats el títol i el cos d'un article, genera exactament {max_tags} etiquetes rellevants en català o castellà (segons l'idioma del post).

Regles estrictes:
1. Prioritza etiquetes de la llista de vocabulari que se't proporciona.
2. Si cap etiqueta del vocabulari és prou rellevant, pots crear-ne de noves (en minúscules).
3. Retorna NOMÉS les etiquetes, una per línia, sense numerar, sense explicacions.
4. Màxim {max_tags} etiquetes. Mínim 2.
5. Etiquetes en minúscules excepte noms propis.
""".format(max_tags=MAX_TAGS)


# ---------------------------------------------------------------------------
# Helpers de front matter
# ---------------------------------------------------------------------------

def parse_post(path):
    """Retorna (front_matter_str, body_str) o (None, None) si no és vàlid."""
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    m = re.match(r'^---\n(.*?)\n---\n?(.*)', txt, re.DOTALL)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def has_marker(body):
    return COMMENT_MARKER in body


def extract_tags_from_fm(fm_str):
    """Extreu la llista de tags del front matter (format YAML llista)."""
    tags = re.findall(r'^- (.+)', fm_str, re.MULTILINE)
    return [t.strip() for t in tags if t.strip()]


def replace_tags_in_fm(fm_str, new_tags):
    """Substitueix el bloc tags: del front matter per les noves etiquetes."""
    new_block = "tags:\n" + "\n".join(f"- {t}" for t in new_tags)
    # substitueix tags: ... (fins al pròxim camp o final)
    result = re.sub(
        r'^tags\s*:.*?(?=^\w|\Z)',
        new_block + "\n",
        fm_str,
        flags=re.MULTILINE | re.DOTALL
    )
    return result


def remove_marker_from_body(body):
    """Elimina la línia del comentari marcador."""
    lines = body.split("\n")
    lines = [l for l in lines if COMMENT_MARKER not in l]
    # elimina línia buida addicional al principi si n'hi ha dues seguides
    result = "\n".join(lines)
    result = re.sub(r'^\n+', '\n', result)
    return result


# ---------------------------------------------------------------------------
# Recollida del vocabulari d'etiquetes existent
# ---------------------------------------------------------------------------

def build_tag_vocabulary(posts_dir="content/posts"):
    """Retorna un Counter de totes les etiquetes existents al blog."""
    counter = Counter()
    for path in glob.glob(f"{posts_dir}/**/*.md", recursive=True):
        fm, _ = parse_post(path)
        if fm:
            for tag in extract_tags_from_fm(fm):
                counter[tag] += 1
    return counter


# ---------------------------------------------------------------------------
# Crida a l'API d'Anthropic
# ---------------------------------------------------------------------------

def suggest_tags(client, title, body_text, vocab_sample):
    """Crida Claude Haiku i retorna una llista d'etiquetes suggerides."""
    # trunca el cos a ~800 paraules per estalviar tokens
    words = body_text.split()
    if len(words) > 800:
        body_text = " ".join(words[:800]) + " [...]"

    vocab_str = ", ".join(vocab_sample[:120])  # mostra les 120 etiquetes més freqüents

    user_msg = f"""\
Vocabulari d'etiquetes existents (les més usades al blog):
{vocab_str}

Títol: {title}

Contingut:
{body_text}
"""
    resp = client.messages.create(
        model=MODEL,
        max_tokens=150,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    raw = resp.content[0].text.strip()
    tags = [line.strip("- •·").strip() for line in raw.splitlines() if line.strip()]
    tags = [t for t in tags if t]
    return tags[:MAX_TAGS]


# ---------------------------------------------------------------------------
# Processament d'un sol fitxer
# ---------------------------------------------------------------------------

def process_file(path, client, vocab_sample, dry_run=False, no_backup=False):
    fm, body = parse_post(path)
    if fm is None:
        return None

    if not has_marker(body):
        return None  # no té el comentari → saltar

    # extreu títol
    title_m = re.search(r'^title\s*:\s*"?(.+?)"?\s*$', fm, re.MULTILINE)
    title = title_m.group(1) if title_m else os.path.basename(path)

    # text net del cos (sense HTML)
    body_text = re.sub(r'<[^>]+>', ' ', body)
    body_text = re.sub(r'\s+', ' ', body_text).strip()

    new_tags = suggest_tags(client, title, body_text, vocab_sample)
    if not new_tags:
        return {"path": path, "status": "error", "detail": "API no ha retornat tags"}

    if dry_run:
        return {"path": path, "status": "dry-run", "tags": new_tags}

    # modifica el fitxer
    if not no_backup:
        with open(path, encoding="utf-8") as f:
            original = f.read()
        with open(path + ".bak", "w", encoding="utf-8") as f:
            f.write(original)

    new_fm = replace_tags_in_fm(fm, new_tags)
    new_body = remove_marker_from_body(body)
    new_content = f"---\n{new_fm}---\n{new_body}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return {"path": path, "status": "ok", "tags": new_tags}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Genera etiquetes automàtiques per als posts marcats.")
    parser.add_argument("--dry-run", action="store_true", help="Simula sense escriure fitxers.")
    parser.add_argument("--limit", type=int, default=0, help="Processa només els primers N posts (0 = tots).")
    parser.add_argument("--file", help="Processa un fitxer concret.")
    parser.add_argument("--no-backup", action="store_true", help="No crea fitxers .bak.")
    parser.add_argument("--posts-dir", default="content/posts", help="Directori de posts (default: content/posts).")
    parser.add_argument("--report", default="auto_tags_report.txt", help="Fitxer d'informe (default: auto_tags_report.txt).")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: cal definir la variable d'entorn ANTHROPIC_API_KEY", file=sys.stderr)
        sys.exit(1)

    try:
        import anthropic
    except ImportError:
        print("ERROR: cal instal·lar la llibreria: pip install anthropic", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # vocabulari
    print("Construint vocabulari d'etiquetes...", flush=True)
    vocab_counter = build_tag_vocabulary(args.posts_dir)
    vocab_sample = [tag for tag, _ in vocab_counter.most_common(200)]
    print(f"  {len(vocab_counter)} etiquetes úniques al vocabulari.", flush=True)

    # llista de fitxers a processar
    if args.file:
        candidates = [args.file]
    else:
        all_posts = sorted(glob.glob(f"{args.posts_dir}/**/*.md", recursive=True))
        candidates = []
        for p in all_posts:
            _, body = parse_post(p)
            if body and has_marker(body):
                candidates.append(p)

    total = len(candidates)
    if args.limit:
        candidates = candidates[:args.limit]

    print(f"Posts amb el marcador: {total}. A processar: {len(candidates)}.", flush=True)
    if args.dry_run:
        print("MODE DRY-RUN: no s'escriurà cap fitxer.", flush=True)

    results = []
    ok = errors = skipped = 0

    for i, path in enumerate(candidates, 1):
        print(f"  [{i}/{len(candidates)}] {path}", end=" ", flush=True)
        try:
            res = process_file(path, client, vocab_sample, dry_run=args.dry_run, no_backup=args.no_backup)
            if res is None:
                print("→ saltat")
                skipped += 1
            elif res["status"] == "error":
                print(f"→ ERROR: {res['detail']}")
                errors += 1
                results.append(res)
            else:
                tags_str = ", ".join(res["tags"])
                print(f"→ {tags_str}")
                ok += 1
                results.append(res)
        except Exception as e:
            print(f"→ EXCEPCIÓ: {e}")
            errors += 1
            results.append({"path": path, "status": "exception", "detail": str(e)})

        time.sleep(RATE_LIMIT_SLEEP)

    # informe
    with open(args.report, "w", encoding="utf-8") as rpt:
        rpt.write(f"auto_tags.py — informe\n")
        rpt.write(f"Model: {MODEL} | Max tags: {MAX_TAGS}\n")
        rpt.write(f"OK: {ok} | Errors: {errors} | Saltats: {skipped}\n\n")
        for r in results:
            if r["status"] in ("ok", "dry-run"):
                rpt.write(f"OK  {r['path']}\n")
                rpt.write(f"    tags: {', '.join(r['tags'])}\n")
            else:
                rpt.write(f"ERR {r['path']}: {r.get('detail', '')}\n")

    print(f"\nFet. OK: {ok} | Errors: {errors} | Saltats: {skipped}")
    print(f"Informe a: {args.report}")


if __name__ == "__main__":
    main()

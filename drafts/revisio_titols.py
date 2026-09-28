#!/usr/bin/env python3
"""Genera drafts/revisio-titols-2026-09-28.html per revisar la tasca T-08.

Ús: python3 drafts/revisio_titols.py
"""
import glob, os, re, html
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "drafts", "revisio-titols-2026-09-28.html")


def parse(path):
    txt = open(path, encoding="utf-8", errors="ignore").read()
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)$", txt, re.S)
    if not m:
        return None
    front, body = m.group(1), m.group(2)
    data = {}
    for ln in front.splitlines():
        if ln and not ln.startswith((" ", "\t")) and ":" in ln:
            k, v = ln.split(":", 1)
            v = v.strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in (chr(34), chr(39)):
                v = v[1:-1]
            data[k.strip()] = v.strip()
    data["file"] = os.path.relpath(path, ROOT)
    data["body"] = body
    return data


def body_lines(body):
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", body)
    body = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", body)
    out = []
    for ln in body.splitlines():
        ln = re.sub(r"^[#>*\-\s]+", "", ln.strip())
        ln = re.sub(r"[*_`]", "", ln).strip()
        if len(ln) >= 12 and not ln.lower().startswith(("http", "de [")):
            out.append(ln)
    return out


def excerpt(body, n=240):
    return html.escape(" ".join(body_lines(body))[:n])


def suggest(body, fallback):
    lines = body_lines(body)
    return html.escape((lines[0] if lines else fallback)[:90])


def url_of(d):
    date = d.get("date", "")
    m = re.match(r"(\d{4})-(\d{2})", date)
    if not m:
        return ""
    y, mo = m.group(1), m.group(2)
    slug = d.get("slug", "")
    return "https://9barrisimatge.org/" + y + "/" + mo + "/" + slug + ".html"


def esc(s):
    return html.escape(s or "", quote=True)


def inp(file, value, orig):
    return ("<input class=\"t\" data-file=\"" + esc(file) + "\" data-orig=\"" + esc(orig)
            + "\" value=\"" + esc(value) + "\">")


def main():
    posts = []
    for p in sorted(glob.glob(os.path.join(ROOT, "content/posts/*/*.md"))):
        d = parse(p)
        if d:
            posts.append(d)
    sense = [d for d in posts if (d.get("title") or "").strip().lower() in ("sense títol", "sense titol", "")]
    groups = defaultdict(list)
    for d in posts:
        t = (d.get("title") or "").strip()
        if t and t.lower() not in ("sense títol", "sense titol"):
            groups[t].append(d)
    dups = [(t, v) for t, v in groups.items() if len(v) > 1]
    dups.sort(key=lambda x: -len(x[1]))

    out = []
    out.append("<!doctype html><html lang=\"ca\"><head><meta charset=\"utf-8\">")
    out.append("<title>Revisió de títols — T-08</title>")
    out.append("<style>body{font:15px/1.5 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;background:#111;color:#eee}")
    out.append("h1{color:#e03131}h2{border-top:1px solid #444;padding-top:1rem;margin-top:2rem}")
    out.append(".case{background:#1c1f26;border:1px solid #333;border-radius:8px;padding:.7rem .9rem;margin:.6rem 0}")
    out.append(".meta{font-size:.8rem;color:#9aa}.meta a{color:#6ea8fe}")
    out.append("input.t{width:100%;margin-top:.4rem;padding:.35rem;background:#0d0f13;color:#eee;border:1px solid #444;border-radius:5px;font-size:.95rem}")
    out.append("button{position:sticky;top:.5rem;float:right;background:#e03131;color:#fff;border:0;padding:.6rem 1rem;border-radius:6px;cursor:pointer;font-weight:700}")
    out.append(".ex{font-size:.85rem;color:#bbb;margin-top:.3rem}.grp{margin:.4rem 0;color:#ffd;font-weight:700}")
    out.append("</style></head><body>")
    out.append("<button onclick=\"exportJSON()\">⬇ Exporta el JSON</button>")
    out.append("<h1>Revisió de títols — T-08</h1>")
    out.append("<p>Cada camp és editable. Deixa’l igual si no el vols canviar. En acabar, prem <b>Exporta el JSON</b> i envia’m el fitxer.</p>")
    out.append("<p><b>Sense títol: " + str(len(sense)) + "</b> · <b>Grups repetits: " + str(len(dups)) + " (" + str(sum(len(v) for _, v in dups)) + " posts)</b></p>")
    out.append("<h2>1. Posts sense títol (" + str(len(sense)) + ")</h2>")
    for d in sense:
        out.append("<div class=\"case\">")
        out.append("<div class=\"meta\">" + esc(d["file"]) + " · " + esc(d.get("date", "")) + " · " + esc(d.get("author", "")) + "</div>")
        out.append("<div class=\"ex\">" + excerpt(d["body"]) + "</div>")
        out.append(inp(d["file"], suggest(d["body"], "Sense títol"), "Sense títol"))
        out.append("</div>")
    out.append("<h2>2. Grups amb títol repetit (" + str(len(dups)) + ")</h2>")
    for t, members in dups:
        members = sorted(members, key=lambda d: d.get("date", ""))
        out.append("<div class=\"case\">")
        out.append("<div class=\"grp\">" + esc(t) + " · " + str(len(members)) + " posts</div>")
        for i, d in enumerate(members):
            out.append("<div class=\"meta\">" + esc(d["file"]) + " · " + esc(d.get("date", "")) + " · <a href=\"" + esc(url_of(d)) + "\" target=\"_blank\">veure</a></div>")
            out.append("<div class=\"ex\">" + excerpt(d["body"]) + "</div>")
            val = t  # per defecte es deixen igual (la URL no canvia encara que es canviï el títol)
            out.append(inp(d["file"], val, t))
        out.append("</div>")
    js = "function exportJSON(){var o={};document.querySelectorAll(\"input.t\").forEach(function(e){var v=e.value.trim();if(v&&v!==e.dataset.orig)o[e.dataset.file]=v;});var b=new Blob([JSON.stringify(o,null,2)],{type:\"application/json\"});var a=document.createElement(\"a\");a.href=URL.createObjectURL(b);a.download=\"titols.json\";a.click();}"
    out.append("<script>" + js + "</script></body></html>")
    open(OUT, "w", encoding="utf-8").write("\n".join(out))
    print("Escrit:", OUT)
    print("Sense títol:", len(sense), "| Grups:", len(dups), "| Posts en grups:", sum(len(v) for _, v in dups))


if __name__ == "__main__":
    main()

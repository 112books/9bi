#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ANÀLISI FINAL dels 469 'Unknown' del feed de Blogger — busca SI hi ha
qualsevol forma de recuperar l'autor real (uri de perfil, email, geo, ...).
Només llegeix la cache. No toca res."""
import json, re, sys

PUB = re.compile(r"^(\d{4}-\d\d-\d\d)T")
def d8(s): 
    m = PUB.match(s or "")
    return m.group(1) if m else ""
def T(e): return (e.get("title") or {}).get("$t", "")
def A(e):
    a = e.get("author") or []
    if isinstance(a, dict): a = [a]
    return a
def a_name(a0): 
    n = a0.get("name") or {}
    return (n.get("$t","") if isinstance(n,dict) else str(n))
def a_uri(a0):
    u = a0.get("uri") or {}
    return (u.get("$t","") if isinstance(u,dict) else str(u))
def a_uri_broken(o):
    d = e.get("custom_author") if isinstance(e,dict) and False else o

cache = "/tmp/blogger_feed_9bi_full.json"
d = json.load(open(cache, encoding="utf-8"))
print(f"cache: {cache} · entrades: {len(d)}")

unknown = [e for e in d if A(e) and a_name(A(e)[0]) == "Unknown"]
print(f"entrades amb autor 'Unknown': {len(unknown)}")

# 1) uri de perfil present?
amb_uri = [e for e in unknown if a_uri(A(e)[0])]
print(f"   amb <author><uri> NO BUIT: {len(amb_uri)}")
for e in amb_uri[:5]:
    print(f"      uri={a_uri(A(e)[0])[:70]}  «{T(e)[:40]}»")

# 2) email present? domini?
from collections import Counter
cnt = Counter()
for e in unknown:
    a0 = A(e)[0]
    m = a0.get("email") or {}
    em = (m.get("$t","") if isinstance(m,dict) else str(m))
    dom = em.split("@")[-1] if "@" in em else em or "(sense email)"
    cnt[dom] += 1
print("\n   dominis d'email dels Unknown:")
for k,v in cnt.most_common():
    print(f"      {v:5d}  {k!r}")

# 3) quants posts locals genèrics (473) quadren amb data única per dia?
print("\n   (la segona font que podria desempatar: data sola + 1 únic feed entry i 1 únic local)")

"""Do DS21's attributions name the graph the cited paper is about?

A survey must paraphrase a source's scope; the checkable shadow of that is
whether the reference's TITLE names the graph the formula is attributed for.
This is one-sided and weak -- a matching title does not prove the paper contains
the stated formula, and a non-matching title is often legitimate (general
results, theses, collected papers).  So it is a CANDIDATE GENERATOR, not a
verdict, and every flag has to be read by hand.
"""
import re, sys
t = open('ds21.txt', encoding='utf-8', errors='replace').read()
t = re.sub(r'\s+', ' ', t)

# bibliography: [n] Author. Title. In: ...
bib = {}
for m in re.finditer(r'\[(\d+)\]\s*[▶]?\s*([^\[]{10,300}?)\.\s*In\s*:', t):
    bib[m.group(1)] = m.group(2)

def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

# claims of the form cr(K_...) <rel> ... [refs]
claim = re.compile(r'cr\(\s*K\s*([0-9,mnpq\s]{1,22}?)\)\s*[=⩾⩽≥≤]([^\[]{1,80})\[([\d,\s]+)\]')
rows, flagged = [], []
for m in claim.finditer(t):
    parts = re.sub(r'\s+', '', m.group(1)).strip(',')
    refs = [r.strip() for r in m.group(3).split(',') if r.strip().isdigit()]
    if not parts or not refs:
        continue
    key = norm('K' + parts)
    titles = {r: bib.get(r, '') for r in refs}
    hit = any(norm('K' + parts) in norm(v) or
              norm(parts) in norm(v) for v in titles.values())
    rows.append((parts, refs, hit))
    if not hit:
        flagged.append((parts, refs, titles))

print(f"attribution pairings extracted: {len(rows)}")
print(f"cited title names the same graph: {sum(1 for _,_,h in rows if h)}")
print(f"flagged for hand reading: {len(flagged)}\n")
seen = set()
for parts, refs, titles in flagged:
    k = (parts, tuple(refs))
    if k in seen: continue
    seen.add(k)
    print(f"K_{parts}  ->  {refs}")
    for r, v in titles.items():
        print(f"    [{r}] {v[:120]}")
    print()

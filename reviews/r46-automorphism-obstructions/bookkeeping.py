"""reviewer-1: certs.json bookkeeping. Enumerates every cycle type 1^f p^k (p prime, k >= 1,
f + p k = n) for n = 36..39 and checks that certified / excluded_by_lemma / open_p_ge_5 /
not_attempted_p_2_3 partition them, and that each exclusion reason is valid."""
import json, sys
J = json.load(open(sys.argv[1]))
def isprime(p): return p > 1 and all(p % d for d in range(2, int(p ** .5) + 1))
window = set()
for n in range(36, 40):
    for p in range(2, n + 1):
        if isprime(p):
            for k in range(1, n // p + 1):
                window.add((n, n - p * k, p, k))
print("prime cycle types in the window:", len(window))
key = lambda e: (e['n'], e['f'], e['p'], e['k'])
cert = {key(e) for e in J['certificates']}
exc = {key(e) for e in J['excluded_by_lemma']}
opn = {key(e) for e in J['open_p_ge_5']}
na = {key(e) for e in J['not_attempted_p_2_3']}
print("sample excluded entry:", J['excluded_by_lemma'][0])
print("sample open entry:", J['open_p_ge_5'][0])
print("sample not-attempted:", J['not_attempted_p_2_3'][0])
print("certified", len(cert), "excluded", len(exc), "open", len(opn), "not attempted", len(na))
print("types in window not covered:", sorted(window - (cert | exc | opn | na)))
print("covered but not a prime type in window:", sorted((cert | exc | opn | na) - window))
sets = [cert, exc, opn, na]
print("overlaps:", [sorted(a & b) for i, a in enumerate(sets) for b in sets[i + 1:] if a & b])
print("p=2,3 types count:", sum(1 for (n, f, p, k) in window if p in (2, 3)))
bad = []
for e in J['excluded_by_lemma']:
    r = e['reason']
    ok = (r == 'Theorem 4' and e['p'] >= 18 and e['f'] >= 1) or (r.startswith('Corollary 3') and e['p'] >= 6 and e['f'] > 22)
    if not ok: bad.append(e)
print("invalid exclusion reasons:", bad)
print("open entries with p < 5:", [e for e in J['open_p_ge_5'] if e['p'] < 5],
      " not-attempted with p not in {2,3}:", [e for e in J['not_attempted_p_2_3'] if e['p'] not in (2, 3)])

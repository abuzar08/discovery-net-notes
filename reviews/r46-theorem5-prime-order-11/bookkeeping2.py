"""reviewer-1: certs.json bookkeeping for Theorem 5 (h2675). Same partition check as
bookkeeping.py, plus: every prime type with p >= 11 is certified (stored, hash-only or
cube) or excluded; lists which Theorem-5 types rest on unstored proofs."""
import json, sys
J = json.load(open(sys.argv[1]))
def isprime(p): return p > 1 and all(p % d for d in range(2, int(p ** .5) + 1))
window = {(n, n - p * k, p, k) for n in range(36, 40) for p in range(2, n + 1) if isprime(p) for k in range(1, n // p + 1)}
key = lambda e: (e['n'], e['f'], e['p'], e['k'])
cert = {key(e): e for e in J['certificates']}
exc = {key(e): e for e in J['excluded_by_lemma']}
opn = {key(e) for e in J['open_p_ge_5']}
na = {key(e) for e in J['not_attempted_p_2_3']}
sets = [set(cert), set(exc), opn, na]
print("prime types:", len(window), "| certified", len(cert), "(prime:", len(set(cert) & window), ") excluded", len(exc), "open", len(opn), "not attempted", len(na))
print("uncovered:", sorted(window - set().union(*sets)), " extra:", sorted(set().union(*sets) - window))
print("overlaps:", [sorted(a & b) for i, a in enumerate(sets) for b in sets[i+1:] if a & b])
bad = [e for e in exc.values() if not ((e['reason'].startswith('Theorem 4') and e['p'] >= 18 and e['f'] >= 1) or (e['reason'].startswith('Corollary 3') and e['p'] >= 6 and e['f'] > 22))]
print("invalid exclusion reasons:", bad)
print("open with p<5:", [t for t in opn if t[2] < 5], " open with p>=11:", sorted(t for t in opn if t[2] >= 11), " not-attempted p not in {2,3}:", [t for t in na if t[2] not in (2, 3)])
t5 = sorted(t for t in window if t[2] >= 11)
print("Theorem 5 types (p>=11):", len(t5))
for t in t5:
    if t in cert:
        e = cert[t]; how = "stored" if e.get('stored') else ("CUBES (not stored)" if e.get('cube_and_conquer') else "HASH ONLY (proof deleted)")
    elif t in exc: how = "excluded: " + exc[t]['reason']
    else: how = "*** NOT SETTLED ***"
    if not (t in cert and cert[t].get('stored')): print("  n=%d 1^%d %d^%d: %s" % (t[0], t[1], t[2], t[3], how))
print("stored-certificate count among Theorem-5 types:", sum(1 for t in t5 if t in cert and cert[t].get('stored')))
print("open p=7:", sorted(t for t in opn if t[2] == 7), "\nopen p=5:", sorted(t for t in opn if t[2] == 5))
print("cube_certificates:", {k: (v if not isinstance(v, list) else f"list[{len(v)}]") for k, v in J['cube_certificates'][0].items()} if isinstance(J['cube_certificates'], list) else list(J['cube_certificates'].keys()))

"""reviewer-1: independent regeneration of the orbit CNF for cycle type 1^f p^k.

usage: python indep_orbit_encode.py N S T F P K TARGET.cnf
Builds the clause set "no K_S, no independent T-set" over one Boolean per
orbit of unordered pairs under the permutation sigma (fixed 0..F-1, then K
cycles of length P), using union-find over pairs (a third method, different
from both encode.py and verify.py), and compares it as a *set of clauses*
with TARGET.cnf.  Also checks that the variable numbering agrees (lexico-
graphically least pair of each orbit, orbits numbered in that order), since
the LRAT proof refers to variables by number.
"""
import itertools, sys


def build(n, s, t, f, p, k):
    assert f + p * k == n
    def sig(x):
        if x < f:
            return x
        j, i = divmod(x - f, p)
        return f + j * p + (i + 1) % p
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    idx = {pr: i for i, pr in enumerate(pairs)}
    parent = list(range(len(pairs)))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for (u, v) in pairs:
        a, b = sig(u), sig(v)
        ra, rb = find(idx[(u, v)]), find(idx[(min(a, b), max(a, b))])
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)   # keep the lexicographically least pair as root
    roots = sorted({find(i) for i in range(len(pairs))})
    num = {r: j + 1 for j, r in enumerate(roots)}
    var = {pr: num[find(idx[pr])] for pr in pairs}
    C = set()
    for S in itertools.combinations(range(n), s):
        C.add(frozenset(-var[e] for e in itertools.combinations(S, 2)))
    for T in itertools.combinations(range(n), t):
        C.add(frozenset(var[e] for e in itertools.combinations(T, 2)))
    return len(roots), C


def read_cnf(path):
    nv, cls = None, []
    for line in open(path):
        if line[0] in 'c%':
            continue
        if line[0] == 'p':
            nv = int(line.split()[2]); continue
        toks = [int(x) for x in line.split()]
        assert toks and toks[-1] == 0
        cls.append(frozenset(toks[:-1]))
    return nv, cls


if __name__ == '__main__':
    n, s, t, f, p, k = map(int, sys.argv[1:7])
    nv, C = build(n, s, t, f, p, k)
    tnv, tcls = read_cnf(sys.argv[7])
    same = (nv == tnv) and (set(tcls) == C) and (len(tcls) == len(C))
    print(f"1^{f} {p}^{k} n={n}: own vars={nv} clauses={len(C)}  target vars={tnv} "
          f"clauses={len(tcls)} (distinct {len(set(tcls))})  SAME={same}")
    sys.exit(0 if same else 1)

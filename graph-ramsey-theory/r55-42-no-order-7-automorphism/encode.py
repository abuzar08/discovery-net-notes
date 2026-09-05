"""Orbit CNF for a (5,5)-good graph on n vertices invariant under a permutation
of cycle type 1^f p^k (f + p*k = n).

Vertices 0..f-1 are fixed; cycle j (0<=j<k) is {f + j*p + i : i in Z_p},
sigma(f+j*p+i) = f+j*p+((i+1) mod p).  One Boolean variable per orbit of
unordered pairs under <sigma>; x=1 means edge (red).  For every 5-set S the two
clauses (OR_{o in M(S)} not x_o) and (OR_{o in M(S)} x_o), M(S) = set of pair
orbits met by S, forbid a red K5 and a blue K5 (independent 5-set).
Duplicate clauses (5-sets in the same orbit, or with the same M) are emitted once.
"""
import sys
from itertools import combinations

def sigma_of(n, f, p, k):
    s = list(range(n))
    for j in range(k):
        base = f + j * p
        for i in range(p):
            s[base + i] = base + (i + 1) % p
    return s

def pair_orbits(n, sig):
    """Map each unordered pair to an orbit index; orbits numbered in order of
    their lexicographically least pair (u<v)."""
    var = {}
    nxt = 0
    for u in range(n):
        for v in range(u + 1, n):
            if (u, v) in var:
                continue
            nxt += 1
            a, b = u, v
            while True:
                key = (a, b) if a < b else (b, a)
                if key in var:
                    break
                var[key] = nxt
                a, b = sig[a], sig[b]
    return var, nxt

def clauses_for(n, var):
    seen = set()
    cls = []
    for S in combinations(range(n), 5):
        M = frozenset(var[e] for e in combinations(S, 2))
        if M in seen:
            continue
        seen.add(M)
        m = sorted(M)
        cls.append([-x for x in m])
        cls.append(m)
    return cls

def encode(n, f, p, k):
    assert f + p * k == n
    sig = sigma_of(n, f, p, k)
    var, nv = pair_orbits(n, sig)
    cls = clauses_for(n, var)
    return sig, var, nv, cls

def write_dimacs(path, nv, cls, comment):
    with open(path, 'w') as fh:
        fh.write(f"c {comment}\n")
        fh.write(f"p cnf {nv} {len(cls)}\n")
        for c in cls:
            fh.write(' '.join(map(str, c)) + ' 0\n')

if __name__ == '__main__':
    n, f, p, k = map(int, sys.argv[1:5])
    out = sys.argv[5]
    sig, var, nv, cls = encode(n, f, p, k)
    write_dimacs(out, nv, cls, f"R(5,5) n={n} automorphism type 1^{f} {p}^{k}; vars=pair orbits")
    print(f"type 1^{f} {p}^{k}: {nv} variables, {len(cls)} clauses")

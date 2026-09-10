"""Orbit CNF for a (5,5)-good graph on 42 vertices invariant under a permutation
of an arbitrary cycle type.

encode.py covers the types 1^f p^k that a single prime order produces. An
automorphism of composite order has several cycle lengths at once -- an element
of order 9 can have fixed points, 3-cycles and 9-cycles together -- so the
permutation is given here as an explicit list of cycle lengths.

Vertices are laid out in the order the cycle lengths are given: the cycles
occupy consecutive blocks, and sigma rotates each block by one. One Boolean per
orbit of unordered pairs under <sigma>, numbered by lexicographically least
pair; for every 5-set S the two clauses (OR_{o in M(S)} not x_o) and
(OR_{o in M(S)} x_o), M(S) the set of pair orbits met by S, forbid a red K5 and
a blue K5. Clauses with the same M are emitted once.

usage: python3 cyctype.py out.cnf len,len,...      (lengths summing to 42)
"""
import sys
from itertools import combinations

def sigma_of_type(lengths):
    """Permutation of sum(lengths) points with one cycle per entry."""
    s = []
    base = 0
    for L in lengths:
        s += [base + (i + 1) % L for i in range(L)]
        base += L
    return s

def pair_orbits(n, sig):
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
    seen, cls = set(), []
    for S in combinations(range(n), 5):
        M = frozenset(var[e] for e in combinations(S, 2))
        if M in seen:
            continue
        seen.add(M)
        m = sorted(M)
        cls.append([-x for x in m])
        cls.append(m)
    return cls

def build(lengths):
    n = sum(lengths)
    sig = sigma_of_type(lengths)
    assert sorted(sig) == list(range(n)), 'not a permutation'
    var, nv = pair_orbits(n, sig)
    return sig, var, nv, clauses_for(n, var)

if __name__ == '__main__':
    out = sys.argv[1]
    lengths = [int(x) for x in sys.argv[2].split(',')]
    sig, var, nv, cls = build(lengths)
    with open(out, 'w') as fh:
        fh.write(f'p cnf {nv} {len(cls)}\n')
        for c in cls:
            fh.write(' '.join(map(str, c)) + ' 0\n')
    print(f'cycle type {lengths}: {nv} orbit vars, {len(cls)} clauses -> {out}')

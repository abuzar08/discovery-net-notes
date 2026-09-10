"""Orbit CNF for a (5,5)-good graph on 42 vertices invariant under an action of
G = Z_3 x Z_3.

cyctype.py handles a graph invariant under one permutation. The same lemma holds
for any group G of automorphisms: the edge relation of a G-invariant graph is
constant on the G-orbits of unordered pairs, so such graphs correspond bijectively
to assignments of one Boolean per pair orbit, and for every 5-set S the two
clauses over M(S), the pair orbits met by S, forbid a clique and an independent
set. A larger group collapses more pairs, so the formula is smaller.

The action is given by its orbit data (a; b_1,b_2,b_3,b_4; c) in the sense of
z3sq_types.py: a fixed points, b_i orbits of size 3 with stabilizer the i-th
subgroup of order 3, and c regular orbits of size 9. For an abelian group the
multiset of point stabilizers determines the action up to isomorphism, so this
data determines the permutation group up to conjugacy in S_42, and refuting one
representative refutes every action with that data.

usage: python3 groupenc.py out.cnf a b1,b2,b3,b4 c
"""
import sys
from itertools import combinations

ELS = [(x, y) for x in range(3) for y in range(3)]
SUBGENS = [(1, 0), (0, 1), (1, 1), (1, 2)]      # generators of the four order-3 subgroups

def add(u, v):
    return ((u[0] + v[0]) % 3, (u[1] + v[1]) % 3)

def subgroup(h):
    return frozenset([(0, 0), h, add(h, h)])

def build_action(a, b, c):
    """Return (n, sigma, tau): the two generators of G as permutations of 0..n-1."""
    blocks = []                                  # each block is a list of cosets (frozensets)
    for _ in range(a):
        blocks.append([frozenset(ELS)])          # one point, stabiliser G
    for i, bi in enumerate(b):
        H = subgroup(SUBGENS[i])
        cosets = sorted({frozenset(add(g, h) for h in H) for g in ELS}, key=sorted)
        for _ in range(bi):
            blocks.append(list(cosets))          # three points, stabiliser H_i
    for _ in range(c):
        blocks.append([frozenset([g]) for g in ELS])   # nine points, trivial stabiliser
    index, pts = {}, 0
    for bi, blk in enumerate(blocks):
        for j, C in enumerate(blk):
            index[(bi, C)] = pts
            pts += 1
    def perm(g):
        p = [0] * pts
        for bi, blk in enumerate(blocks):
            for C in blk:
                img = frozenset(add(g, x) for x in C)
                p[index[(bi, C)]] = index[(bi, img)]
        return p
    return pts, perm((1, 0)), perm((0, 1))

def pair_orbits(n, gens):
    """One variable per orbit of unordered pairs under the group the gens generate,
    numbered by lexicographically least pair."""
    var, nxt = {}, 0
    for u in range(n):
        for v in range(u + 1, n):
            if (u, v) in var:
                continue
            nxt += 1
            stack = [(u, v)]
            while stack:                          # closure under both generators
                a1, b1 = stack.pop()
                key = (a1, b1) if a1 < b1 else (b1, a1)
                if key in var:
                    continue
                var[key] = nxt
                for p in gens:
                    stack.append((p[key[0]], p[key[1]]))
    return var, nxt

def supports(n, var, k):
    """The distinct sets M(S) of pair orbits met by a k-subset S."""
    return {frozenset(var[e] for e in combinations(S, 2)) for S in combinations(range(n), k)}

def clauses_for(n, var, s=5, t=None):
    """No clique of size s and no independent set of size t.

    One clause per distinct support: an s-set is not a clique iff some pair orbit
    it meets is false, a t-set is not independent iff some pair orbit it meets is
    true. Distinct subsets with the same support give literally the same clause,
    so each support is emitted once.
    """
    t = s if t is None else t
    cls = [[-x for x in sorted(M)] for M in supports(n, var, s)]
    cls += [sorted(M) for M in supports(n, var, t)]
    return cls

def build(a, b, c):
    n, sig, tau = build_action(a, b, c)
    assert n == 42, f'action has {n} points, not 42'
    for p in (sig, tau):
        assert sorted(p) == list(range(n)), 'not a permutation'
    var, nv = pair_orbits(n, [sig, tau])
    return n, sig, tau, var, nv, clauses_for(n, var)

if __name__ == '__main__':
    out = sys.argv[1]
    a = int(sys.argv[2]); b = [int(x) for x in sys.argv[3].split(',')]; c = int(sys.argv[4])
    n, sig, tau, var, nv, cls = build(a, b, c)
    with open(out, 'w') as fh:
        fh.write(f'p cnf {nv} {len(cls)}\n')
        for cl in cls:
            fh.write(' '.join(map(str, cl)) + ' 0\n')
    print(f'a={a} b={tuple(b)} c={c}: {nv} orbit vars, {len(cls)} clauses -> {out}')

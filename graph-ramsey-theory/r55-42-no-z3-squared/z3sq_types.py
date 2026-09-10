"""Enumerate the faithful actions of Z_3 x Z_3 on 42 points that survive the
published bound on the fixed points of an order-3 automorphism.

An action of an abelian group G on a set is determined up to isomorphism by the
multiset of point stabilizers, one per orbit. For G = Z_3 x Z_3 the stabilizers
are G itself (a fixed point), one of the four subgroups H_1..H_4 of order 3 (an
orbit of size 3), or the trivial group (an orbit of size 9). So an action is the
data (a; b_1,b_2,b_3,b_4; c) with

    a + 3(b_1 + b_2 + b_3 + b_4) + 9c = 42,

a the number of fixed points, b_i the number of size-3 orbits with stabilizer
H_i, and c the number of regular orbits. A non-identity g with <g> = H_i fixes
exactly the a fixed points and the 3b_i points of the orbits it stabilizes:

    |Fix(g)| = a + 3 b_i.

Every such g is an order-3 automorphism of the graph, so |Fix(g)| <= FMAX, the
published bound. Aut(Z_3 x Z_3) permutes H_1..H_4 as the full symmetric group,
so the b_i may be sorted.

usage: python3 z3sq_types.py [fmax]
"""
import sys, itertools

FMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12

out = []
for a in range(0, FMAX + 1, 3):
    bmax = (FMAX - a) // 3
    for b in itertools.combinations_with_replacement(range(bmax, -1, -1), 4):
        rest = 42 - a - 3 * sum(b)
        if rest < 0 or rest % 9:
            continue
        out.append((a, tuple(sorted(b, reverse=True)), rest // 9))
out.sort()
for a, b, c in out:
    fixes = sorted({a + 3 * x for x in b})
    print(f'a={a:2d}  b={b}  c={c}   orbit sizes 1^{a} 3^{sum(b)} 9^{c}   '
          f'|Fix| of the four subgroups: {[a + 3*x for x in b]}')
print(f'\n{len(out)} actions with fmax={FMAX}')

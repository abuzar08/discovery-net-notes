"""For any (n, q): the incumbent sampling bound, an explicit ceiling, and the gap.

Any lower bound that reads only the vertex and edge counts must hold for every
graph with those counts, so it is at most

    C(n,q) = min { cr(G) : |V(G)| = n, |E(G)| = q },

and exhibiting one graph with one drawing caps the entire family.  The ceiling
here comes from a 2-page drawing -- vertices in convex position, each edge drawn
inside or outside, two edges crossing exactly when they interleave on the same
page -- optimised for K_n and then thinned by greedy deletion to q edges, with
the pages re-optimised for what survives.  Every configuration is an explicit
drawing, so the number reported is rigorous.

Usage:  python3 bound_report.py N Q [TARGET]
"""
import sys
from fractions import Fraction as F
from math import comb

import recursive_sampling as RS


def interleavings(n):
    E = [(i, j) for i in range(n) for j in range(i + 1, n)]
    inter = [[] for _ in E]
    for i in range(len(E)):
        a, b = E[i]
        for j in range(i + 1, len(E)):
            c, d = E[j]
            if len({a, b, c, d}) < 4:
                continue
            if (a < c < b < d) or (c < a < d < b):
                inter[i].append(j)
                inter[j].append(i)
    return E, inter


def ceiling(n, q, restarts=6, seed=1):
    import random
    E, inter = interleavings(n)
    rnd = random.Random(seed)
    best = None
    for _ in range(restarts):
        page = [rnd.randrange(2) for _ in E]
        improved = True
        while improved:
            improved = False
            for i in range(len(E)):
                same = sum(1 for j in inter[i] if page[j] == page[i])
                if len(inter[i]) - same < same:
                    page[i] ^= 1
                    improved = True
        c = sum(1 for i in range(len(E)) for j in inter[i]
                if j > i and page[i] == page[j])
        if best is None or c < best[0]:
            best = (c, page[:])
    full, page = best
    k = len(E) - q
    alive = [True] * len(E)
    load = [sum(1 for j in inter[i] if page[j] == page[i]) for i in range(len(E))]
    tot = sum(load) // 2
    for _ in range(k):
        i = max((x for x in range(len(E)) if alive[x]), key=lambda x: load[x])
        alive[i] = False
        tot -= load[i]
        for j in inter[i]:
            if alive[j] and page[j] == page[i]:
                load[j] -= 1
        load[i] = 0
    keep = {i for i in range(len(E)) if alive[i]}
    improved = True
    while improved:
        improved = False
        for i in keep:
            same = sum(1 for j in inter[i] if j in keep and page[j] == page[i])
            if sum(1 for j in inter[i] if j in keep) - same < same:
                page[i] ^= 1
                improved = True
    return full, sum(1 for i in keep for j in inter[i]
                     if j > i and j in keep and page[j] == page[i])


def report(n, q, target=None, L=None):
    L = L or RS.build(n)
    env = {s: RS.Envelope(L[s]) for s in L}
    cur = L[n][q]
    full, cap = ceiling(n, q)
    Z = (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4
    print(f"n = {n}, q = {q}   (K_n has {comb(n,2)} edges; missing {comb(n,2)-q})")
    print(f"  incumbent sampling bound L(n,q) = {cur:,}")
    print(f"  2-page drawing of K_n found {full:,} crossings   (Z(n) = {Z:,})")
    print(f"  ceiling on ANY (n,q)-only bound  = {cap:,}"
          f"   [incumbent is {cur/cap:.0%} of it]")
    if target:
        print(f"  target {target:,}: "
              f"{'BELOW the ceiling, so not excluded' if target <= cap else 'ABOVE the ceiling -- UNREACHABLE by any (n,q)-only bound'}")
        fs = []
        for s in range(max(8, n // 2), n):
            cnk, cn4, cn2 = comb(n, s), comb(n - 4, s - 4), comb(n - 2, s - 2)
            m = F(q * cn2, cnk)
            c = env[s](m)
            if c > 0:
                fs.append((float(F(target * cn4, cnk) / c), s))
        if fs:
            fs.sort()
            print(f"  required improvement factor in the sample-size bound: "
                  f"{fs[0][0]:.4f} (at s={fs[0][1]}) to {fs[-1][0]:.4f}")
    return cur, cap


if __name__ == '__main__':
    n, q = int(sys.argv[1]), int(sys.argv[2])
    t = int(sys.argv[3]) if len(sys.argv) > 3 else None
    report(n, q, t)

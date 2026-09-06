"""A ceiling on any lower bound that depends only on (n, q).

Any valid bound L(n,q) <= cr(G) for EVERY n-vertex q-edge graph is at most the
minimum of cr over that family.  Exhibiting one graph with a good drawing
therefore caps what the whole sampling family can ever prove.

Construction: take a 2-page drawing of K_32 (vertices in convex position, each
edge drawn inside or outside; two edges cross exactly when they interleave and
share a page), optimise the page assignment by local search, then delete 113
edges to remove as many crossings as possible.  Every step only ever exhibits a
drawing, so the resulting count is a rigorous upper bound on the crossing number
of the surviving 383-edge graph.
"""
import itertools
import random
import sys


def interleave(e, f):
    (a, b), (c, d) = e, f
    if len({a, b, c, d}) < 4:
        return False
    return (a < c < b < d) or (c < a < d < b)


def build(n):
    E = [(i, j) for i in range(n) for j in range(i + 1, n)]
    idx = {e: k for k, e in enumerate(E)}
    inter = [[] for _ in E]
    for i in range(len(E)):
        for j in range(i + 1, len(E)):
            if interleave(E[i], E[j]):
                inter[i].append(j)
                inter[j].append(i)
    return E, idx, inter


def crossings(page, inter):
    return sum(1 for i in range(len(page)) for j in inter[i]
               if j > i and page[i] == page[j]) 


def optimise(E, inter, iters=60, seed=1):
    rnd = random.Random(seed)
    best = None
    for t in range(iters):
        page = [rnd.randrange(2) for _ in E]
        improved = True
        while improved:
            improved = False
            for i in range(len(E)):
                same = sum(1 for j in inter[i] if page[j] == page[i])
                other = len(inter[i]) - same
                if other < same:
                    page[i] ^= 1
                    improved = True
        c = crossings(page, inter)
        if best is None or c < best[0]:
            best = (c, page[:])
    return best


def greedy_delete(E, inter, page, k):
    """Delete k edges, each time removing the one carrying the most crossings."""
    alive = [True] * len(E)
    load = [sum(1 for j in inter[i] if page[j] == page[i]) for i in range(len(E))]
    total = sum(load) // 2
    removed = []
    for _ in range(k):
        i = max((x for x in range(len(E)) if alive[x]), key=lambda x: load[x])
        alive[i] = False
        removed.append(E[i])
        total -= load[i]
        for j in inter[i]:
            if alive[j] and page[j] == page[i]:
                load[j] -= 1
        load[i] = 0
    return total, removed, alive


if __name__ == '__main__':
    n = 32
    E, idx, inter = build(n)
    print(f"K_{n}: {len(E)} edges, "
          f"{sum(len(x) for x in inter)//2:,} interleaving pairs")
    c, page = optimise(E, inter)
    Z = (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4
    print(f"best 2-page drawing found: {c:,} crossings   (Z({n}) = {Z:,})")
    tot, rem, alive = greedy_delete(E, inter, page, 113)
    print(f"after deleting 113 edges greedily: {sum(alive)} edges, "
          f"{tot:,} crossings")
    print(f"\nceiling on any (n,q)-only bound at (32,383): cr <= {tot:,}")
    print(f"target 3557 is {'ABOVE' if 3557 > tot else 'below'} this ceiling")

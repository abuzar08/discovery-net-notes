"""Ceilings at every sample scale, to test whether sampling can reach 3557.

The recursion needs Lhat(s, mean q_S) to reach a value computed from the target.
But L(s,q) can never exceed C(s,q) = min{cr(H) : s vertices, q edges}, and an
explicit drawing upper-bounds C.  If the required value exceeds that ceiling at
every sample size, no bound in this family -- however the base bounds are
improved -- can prove the target.
"""
from fractions import Fraction as F
from math import comb
import sys

from ceiling import build, optimise, greedy_delete
import recursive_sampling as RS


def ceiling_at(s, q, restarts=8):
    E, idx, inter = build(s)
    c, page = optimise(E, inter, iters=restarts)
    k = len(E) - q
    if k <= 0:
        return c
    tot, rem, alive = greedy_delete(E, inter, page, k)
    # one page re-optimisation for the surviving graph
    keep = {i for i in range(len(E)) if alive[i]}
    improved = True
    while improved:
        improved = False
        for i in keep:
            same = sum(1 for j in inter[i] if j in keep and page[j] == page[i])
            if sum(1 for j in inter[i] if j in keep) - same < same:
                page[i] ^= 1
                improved = True
    return sum(1 for i in keep for j in inter[i]
               if j > i and j in keep and page[j] == page[i])


if __name__ == '__main__':
    n, q, TGT = 32, 383, 3557
    L = RS.build(n)
    env = {s: RS.Envelope(L[s]) for s in L}
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 31
    print(f"{'s':>3} {'mean q_S':>9} {'Lhat now':>9} {'needed':>9} "
          f"{'ceiling':>9} {'verdict':>12}")
    for s in range(lo, hi + 1):
        cnk, cn4, cn2 = comb(n, s), comb(n - 4, s - 4), comb(n - 2, s - 2)
        mean = F(q * cn2, cnk)
        cur = env[s](mean)
        need = F(TGT * cn4, cnk)
        # ceiling at the two integers bracketing the mean, convexly combined
        a, b = int(mean), int(mean) + 1
        ca, cb = ceiling_at(s, a), ceiling_at(s, b)
        w = mean - a
        cap = (1 - w) * ca + w * cb
        verdict = 'IMPOSSIBLE' if need > cap else 'possible'
        print(f"{s:>3} {float(mean):>9.2f} {float(cur):>9.1f} "
              f"{float(need):>9.1f} {float(cap):>9.1f} {verdict:>12}",
              flush=True)

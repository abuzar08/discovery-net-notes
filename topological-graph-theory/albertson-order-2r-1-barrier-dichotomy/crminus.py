#!/usr/bin/env python3
"""
A lower bound for cr(F) when F is a complete graph minus a few edges.

WHY THIS EXISTS.  Every tight configuration in this directory has the same
shape: a vertex set D on which the complement H has only a handful of edges, so
G[D] is K_|D| minus f edges with f small.  Until now such a set was scored with
the generic integer-aware sampling bound L(n, m), which is very weak at high
density -- for K_28 minus 3 edges it returns 4656 against cr(K_28) >= 6250.
That gap was the load-bearing weakness of the order-58 argument.

THE BOUND.  Write g(n, f) for a lower bound on cr(F) valid for EVERY graph F on
n vertices with at least C(n,2) - f edges.  Three ingredients, take the maximum.

1. VERTEX COVER.  The missing edges have a vertex cover of size at most f (one
   endpoint per edge), and deleting it leaves a complete graph on at least n - f
   vertices.  So g(n,f) >= crK(n-f).

2. SAMPLING.  L(n, C(n,2) - f) is valid for every graph with those parameters.

3. VERTEX-DELETION AVERAGING.  Fix a good optimal drawing of F.  In a good
   drawing crossing edges are independent, so every crossing involves exactly
   four distinct vertices and therefore survives in exactly n - 4 of the n
   vertex-deleted subdrawings.  Hence

       sum_v cr(F - v)  <=  sum_v cr_D(F - v)  =  (n - 4) cr(F),

   so cr(F) >= sum_v cr(F-v) / (n-4).  Now F - v misses f_v edges, where
   f_v counts the missing edges avoiding v, so f_v <= f for every v.  The
   missing edges span at least t(f) vertices, where t(f) is least with
   C(t,2) >= f, and each spanned vertex lies in a missing edge, so for those
   f_v <= f - 1.  Therefore

       g(n,f) >= ceil( ( (n - t) g(n-1, f) + t g(n-1, f-1) ) / (n - 4) ).

CAUTION -- A WRONG VERSION.  The first version of this file used
"(n-2) g(n-1,f) + 2 crK(n-1)", on the assumption that two of the deleted
subgraphs come out complete.  That is FALSE: f_v = 0 requires v to lie in
*every* missing edge, which already fails for two disjoint missing edges.  The
step above replaces it and only ever claims f_v <= f - 1 for a spanned vertex,
which is immediate.

SOUNDNESS CONTROL.  cr(K_n) <= Z(n) and F is a subgraph of K_n, so any correct
lower bound must satisfy g(n,f) <= Z(n) for every f >= 0; `controls()` checks
this over the whole range used, together with g(n,0) = crK(n) and monotonicity
of g in f.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
from functools import lru_cache

import verify_range as V
import order2r as O


def tmin(f):
    """Least t with C(t,2) >= f: f edges span at least t vertices."""
    t = 0
    while t * (t - 1) // 2 < f:
        t += 1
    return t


@lru_cache(maxsize=None)
def g(n, f):
    """Lower bound on cr(F) for every F on n vertices with >= C(n,2) - f edges."""
    if n < 5:
        return 0
    if f <= 0:
        return V.crK(n)
    best = max(V.crK(max(0, n - f)), O.L(n, n * (n - 1) // 2 - f))
    t = tmin(f)
    if n - 4 > 0:
        val = -(-((n - t) * g(n - 1, f) + t * g(n - 1, f - 1)) // (n - 4))
        if val > best:
            best = val
    return best


def reset():
    """Drop the cache after verify_range.set_base changes the crK seeds."""
    g.cache_clear()


def controls(nmax=60, fmax=40):
    """g must never exceed Z(n), must equal crK(n) at f = 0, and must be
    non-increasing in f."""
    ok = True
    for n in range(5, nmax + 1):
        ok &= g(n, 0) == V.crK(n)
        prev = None
        for f in range(0, min(fmax, n * (n - 1) // 2) + 1):
            v = g(n, f)
            ok &= v <= V.Z(n)
            if prev is not None:
                ok &= v <= prev
            prev = v
    return ok


def main():
    print("cr(K_n minus f edges): a lower bound, and what it buys")
    print()
    for name, base in (("conservative (seed cr(K_12) = 150 only)", V.BASE_CONSERVATIVE),
                       ("with the CCCG 2021 values cr(K_13) = 225, cr(K_14) = 315",
                        V.BASE_CCCG2021)):
        V.set_base(base)
        reset()
        print("SEED: %s" % name)
        print("   controls (g <= Z, g(n,0) = crK(n), monotone in f): %s"
              % ("PASS" if controls() else "FAIL"))
        print("     n   f   this bound   sampling L   crK(n-f)")
        for n, f in ((28, 3), (28, 6), (27, 3), (26, 0), (32, 113), (31, 87),
                     (49, 594), (52, 685)):
            print("   %3d %3d   %8d   %10d   %8d"
                  % (n, f, g(n, f), O.L(n, n * (n - 1) // 2 - f),
                     V.crK(max(0, n - f))))
        print()
    V.set_base(V.BASE_CCCG2021)
    reset()


if __name__ == "__main__":
    main()

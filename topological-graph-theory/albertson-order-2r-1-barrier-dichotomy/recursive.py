#!/usr/bin/env python3
"""
Independent recursive integer-aware sampling bound L(n,q) on cr over all simple
graphs with n vertices and q edges, built from published base bounds only.

Base (all published, all valid for every simple graph):
  Euler          cr >= q - (3n-6)
  PRTT           cr >= (7/3)q - (25/3)(n-2)
  PRTT           cr >= 4q - (103/6)(n-2)
  Buengener-Kaufmann / Sadhu Lemma 2.1   cr >= 5q - (203/9)(n-2)
Each is rounded up, since cr is an integer.

Recursion (Sadhu Lemma 2.2 double count): for a uniform random s-subset S,
  E[cr(G[S])] <= cr(G) * (s)_4/(n)_4     (a crossing has 4 distinct vertices)
  E[e(G[S])]   = q * s(s-1)/(n(n-1))
so with f = lower convex envelope of q' -> L(s,q'),
  cr(G) >= ceil( f( q s(s-1)/(n(n-1)) ) * (n)_4/(s)_4 ).
The envelope is needed for Jensen; the ceiling at every level is what makes the
recursion gain -- without it the binomial factors telescope exactly and a
two-level bound equals the direct one.

This reproduces, independently, the mechanism recorded on Discovery Net at
ledger height 2617.
"""
from fractions import Fraction as F


def falling(n, k):
    p = 1
    for i in range(k):
        p *= (n - i)
    return p


def base_bound(n, q):
    """max of the published linear bounds, rounded up; 0 if none is positive."""
    if n < 3 or q <= 0:
        return 0
    cands = [q - (3 * n - 6),
             -(-(7 * q * 2 - 50 * (n - 2)) // 6),          # ceil((7/3)q-(25/3)(n-2))
             -(-(4 * q * 6 - 103 * (n - 2)) // 6),         # ceil(4q-(103/6)(n-2))
             -(-(5 * q * 9 - 203 * (n - 2)) // 9)]         # ceil(5q-(203/9)(n-2))
    return max(0, max(cands))


def lower_convex_envelope(vals):
    """Lower convex hull of the points (i, vals[i]).  Returns the hull vertices."""
    hull = []
    for i, y in enumerate(vals):
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            # drop (x2,y2) if it lies on or above the segment (x1,y1)-(i,y)
            if (y2 - y1) * (i - x1) >= (y - y1) * (x2 - x1):
                hull.pop()
            else:
                break
        hull.append((i, y))
    return hull


def env_value(hull, x):
    """Evaluate the piecewise-linear hull at a Fraction x (0 <= x <= last vertex)."""
    lo, hi = 0, len(hull) - 1
    while lo < hi - 1:
        mid = (lo + hi) // 2
        if hull[mid][0] <= x:
            lo = mid
        else:
            hi = mid
    (x1, y1), (x2, y2) = hull[lo], hull[hi]
    if x2 == x1:
        return F(y1)
    return F(y1) + F((y2 - y1) * (x - x1), (x2 - x1))


def build(N, rounds=3):
    """L[n] is a list of integer lower bounds indexed by edge count."""
    L = {n: [base_bound(n, q) for q in range(n * (n - 1) // 2 + 1)]
         for n in range(3, N + 1)}
    for _ in range(rounds):
        changed = False
        for n in range(5, N + 1):
            fn4 = falling(n, 4)
            best = list(L[n])
            for s in range(4, n):
                hull = lower_convex_envelope(L[s])
                fs4 = falling(s, 4)
                scale = F(fn4, fs4)
                for q in range(len(L[n])):
                    x = F(q * s * (s - 1), n * (n - 1))
                    v = env_value(hull, x) * scale
                    b = -((-v.numerator) // v.denominator)      # ceil
                    if b > best[q]:
                        best[q] = b
                        changed = True
            L[n] = best
        if not changed:
            break
    return L


def Z(n):
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4


if __name__ == "__main__":
    N = 59
    L = build(N)
    print("Independent recursive integer-aware sampling, base = Euler + PRTT + BK/Sadhu")
    print()
    print("soundness controls (every bound must stay below a known upper bound):")
    bad = [(n, L[n][n * (n - 1) // 2], Z(n)) for n in range(5, N + 1)
           if L[n][n * (n - 1) // 2] > Z(n)]
    print("   L(n, C(n,2)) <= Z(n):", bad[:4] if bad else "ALL OK")

    def Zb(a, b):
        return (a // 2) * ((a - 1) // 2) * (b // 2) * ((b - 1) // 2)
    bad2 = [(a, b) for a in range(3, 30) for b in range(3, 30)
            if a + b <= N and L[a + b][a * b] > Zb(a, b)]
    print("   bipartite <= Z(a,b):", bad2[:4] if bad2 else "ALL OK")
    bad3 = [(n, q) for n in range(5, N + 1) for q in range(1, 3 * n - 6)
            if L[n][q] > 0]
    print("   vanishes for q <= 3n-7:", bad3[:4] if bad3 else "ALL OK")
    for n, q, tr in ((11, 55, 100), (12, 66, 150), (13, 78, 225), (14, 91, 315)):
        print("   K_%d: L=%d true=%d %s" % (n, L[n][q], tr,
                                            "OK" if L[n][q] <= tr else "VIOLATION"))
    print()
    print("the four r=27 frontier rows:")
    for n, q in ((53, 713), (53, 714), (53, 715), (54, 726)):
        print("   (%d,%d): recursive %5d   Z(27)=%d   %s"
              % (n, q, L[n][q], Z(27),
                 "CLOSED" if L[n][q] >= Z(27) else "open, gap %d" % (Z(27) - L[n][q])))
    print()
    print("ceilings (largest q with L(n,q) < Z(r)):")
    for r, n in ((27, 53), (27, 54), (28, 55), (29, 57), (30, 59)):
        hi = max([q for q in range(len(L[n])) if L[n][q] < Z(r)], default=-1)
        print("   r=%d n=%d: ceiling %d" % (r, n, hi))

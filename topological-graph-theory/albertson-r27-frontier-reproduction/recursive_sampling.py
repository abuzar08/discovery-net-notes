"""Recursive integer-aware sampling bounds for the crossing number.

Builds, for every n and every edge count q, an integer lower bound L(n,q) on
cr(H) over all n-vertex q-edge simple graphs, from published base bounds plus
the induced-sampling double count, rounding to an integer at every level.

Base bounds (all published):
  Euler                cr >= q - (3n-6)
  density sum          2 cr >= sum_j max(0, q - e_{j-1}(n)) with
                       e_0 = 3n-6, e_1 = 4n-8, e_2 = 5n-10,
                       e_3 = floor(5.5n-11.5), e_4 = 6n-12   (Ackerman)
  Buengener-Kaufmann   cr >= 5q - (203/9)(n-2)
                       cr >= (37/9)q - (155/9)(n-2)

Recursion (Sadhu Lemma 2.2's double count, applied with any valid bound at the
sample size):  in a crossing-minimal good drawing of an n-vertex q-edge graph,
each edge lies in C(n-2,s-2) of the induced s-subgraphs and each crossing in
C(n-4,s-4), so

    cr(G) * C(n-4,s-4)  >=  sum over the C(n,s) samples of  L(s, q_S).

Since sum q_S = q C(n-2,s-2), and the lower convex envelope Lhat(s, .) of
L(s, .) is convex and under-estimates L(s, .) at integers, Jensen gives

    cr(G) >= ceil( C(n,s) * Lhat(s, q C(n-2,s-2)/C(n,s)) / C(n-4,s-4) ).

Rounding up at every level is what makes the recursion gain: plain (unrounded)
recursive sampling telescopes exactly to single-level sampling, because
C(n,s1)C(s1,s2)/(C(n-4,s1-4)C(s1-4,s2-4)) = C(n,s2)/C(n-4,s2-4).

Standard library only; exact rational arithmetic.
"""
from fractions import Fraction as F
from math import comb


def ceil_frac(x):
    x = F(x)
    return -((-x.numerator) // x.denominator)


def base_bound(n, q):
    """Max of the published base bounds, as an integer."""
    if n < 3:
        return 0
    b = [0, q - (3 * n - 6)]
    # density sum
    e = [3 * n - 6, 4 * n - 8, 5 * n - 10, (11 * n - 23) // 2, 6 * n - 12]
    s = sum(max(0, q - x) for x in e)
    b.append(ceil_frac(F(s, 2)))
    # Buengener-Kaufmann
    b.append(ceil_frac(5 * F(q) - F(203, 9) * (n - 2)))
    b.append(ceil_frac(F(37, 9) * q - F(155, 9) * (n - 2)))
    return max(b)


def lower_hull(pts):
    """Lower convex hull of (x, y) points sorted by x; returns hull vertices."""
    h = []
    for p in pts:
        while len(h) >= 2:
            (x1, y1), (x2, y2) = h[-2], h[-1]
            # drop h[-1] if it is on or above the segment h[-2] -> p
            if (y2 - y1) * (p[0] - x1) >= (p[1] - y1) * (x2 - x1):
                h.pop()
            else:
                break
        h.append(p)
    return h


class Envelope:
    """Lower convex envelope of an integer-indexed sequence, evaluable at
    rational points."""

    def __init__(self, values):
        self.h = lower_hull(list(enumerate(values)))

    def __call__(self, x):
        h = self.h
        if x <= h[0][0]:
            return F(h[0][1])
        if x >= h[-1][0]:
            return F(h[-1][1])
        lo, hi = 0, len(h) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if h[mid][0] <= x:
                lo = mid
            else:
                hi = mid
        (x1, y1), (x2, y2) = h[lo], h[hi]
        return F(y1) + F(y2 - y1) * (F(x) - x1) / (x2 - x1)


def build(nmax, verbose=False):
    """L[n] is the list of integer bounds for q = 0 .. C(n,2)."""
    L = {}
    env = {}
    for n in range(3, nmax + 1):
        qmax = comb(n, 2)
        vals = [base_bound(n, q) for q in range(qmax + 1)]
        for s in range(4, n):
            if n - 4 < s - 4:
                continue
            cnk = comb(n, s)
            cn4 = comb(n - 4, s - 4)
            cn2 = comb(n - 2, s - 2)
            E = env[s]
            for q in range(qmax + 1):
                mean = F(q * cn2, cnk)
                v = ceil_frac(F(cnk) * E(mean) / cn4)
                if v > vals[q]:
                    vals[q] = v
        L[n] = vals
        env[n] = Envelope(vals)
        if verbose and n % 10 == 0:
            print(f"  built n={n}")
    return L


if __name__ == "__main__":
    import sys
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    L = build(nmax, verbose=True)

    print()
    print("Claim (b) of the Albertson r=27 chain (height 1813):")
    print("    cr(H) >= 26q - 11706 for every 50-vertex q-edge simple graph H")
    print()
    print(f"{'q':>5} {'claim 26q-11706':>16} {'recursive bound':>16} {'ok?':>5}")
    bad = []
    for q in range(0, comb(50, 2) + 1):
        claim = 26 * q - 11706
        got = L[50][q]
        if claim > got:
            bad.append((q, claim, got))
    for q in (500, 600, 634, 635, 650, 700, 800, 900, 1000, 1225):
        print(f"{q:>5} {26*q-11706:>16} {L[50][q]:>16} "
              f"{'ok' if L[50][q] >= 26*q-11706 else 'SHORT':>5}")
    print()
    if bad:
        print(f"claim (b) NOT reproduced at {len(bad)} edge counts; "
              f"worst deficits:")
        for q, c, g in sorted(bad, key=lambda t: g - t[1])[:6]:
            print(f"    q={q}: claim {c}, recursive bound {g} (short by {c-g})")
    else:
        print("claim (b) is implied by the recursive bound at every q: REPRODUCED")

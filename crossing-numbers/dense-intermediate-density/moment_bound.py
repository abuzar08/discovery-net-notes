"""A second-moment strengthening of the recursive sampling bound.

The sampling identity gives cr(G) C(n-4,s-4) >= sum_S cr(G[S]) >= sum_S L(s,q_S).
The published bound then applies Jensen to the lower convex envelope, which uses
only the MEAN of q_S.  But for G = K_n minus a set F of t edges, writing t_S for
the number of F-edges inside S, the SECOND moment of t_S is also pinned down:

    sum_S t_S            = t * C(n-2,s-2)
    sum_S C(t_S,2)       = P3 * C(n-3,s-3) + (C(t,2) - P3) * C(n-4,s-4)

where P3 = sum_v C(d_v,2) counts pairs of F-edges sharing a vertex.  P3 is not
known, but it is bounded on both sides over all F with t edges: below by making
the degrees as equal as possible, above by the colex (threshold) graph.  Since
C(n-3,s-3) > C(n-4,s-4), those give M2min and M2max.

Duality makes this certifiable.  For any reals (a, b, g) with

    a + b*t + g*C(t,2)  <=  L(s, C(s,2) - t)      for every feasible t,

summing over the C(n,s) samples gives

    sum_S L(s,q_S) >= a*C(n,s) + b*M1 + g*M2,

and M2 may be replaced by M2min when g >= 0, or by M2max when g <= 0.  Jensen is
the special case g = 0, so this can only help; the gain comes from g < 0, which
exploits that q_S is CONCENTRATED while the envelope's optimal mixture is spread
across two far-apart hull vertices.
"""
from fractions import Fraction as F
from math import comb

import recursive_sampling as RS


def P3_min(n, t):
    """Minimum of sum_v C(d_v,2) over graphs with n vertices and t edges."""
    s = 2 * t
    base, extra = divmod(s, n)
    return extra * comb(base + 1, 2) + (n - extra) * comb(base, 2)


def P3_max(n, t):
    """Maximum of sum_v C(d_v,2): the colex (threshold) graph on t edges."""
    deg = [0] * n
    left = t
    j = 1
    while left > 0 and j < n:
        take = min(left, j)
        for i in range(take):
            deg[i] += 1
            deg[j] += 1
        left -= take
        j += 1
    return sum(comb(d, 2) for d in deg)


def moments(n, s, t, P3):
    M1 = t * comb(n - 2, s - 2)
    M2 = P3 * comb(n - 3, s - 3) + (comb(t, 2) - P3) * comb(n - 4, s - 4)
    return M1, M2


def certify(n, q, s, L):
    """Best bound from a dual certificate (a,b,g), searched over b and g."""
    t = comb(n, 2) - q
    N = comb(n, s)
    M1, M2lo = moments(n, s, t, P3_min(n, t))
    _, M2hi = moments(n, s, t, P3_max(n, t))
    S2 = comb(s, 2)
    tmax = min(t, S2)
    vals = {tt: L[s][S2 - tt] for tt in range(tmax + 1)}
    best = (0, None)
    # coarse-to-fine search over the two multipliers
    bs = [F(x, 4) for x in range(-4 * 60, 1)]
    for b in bs:
        for gnum in range(-40, 41):
            g = F(gnum, 400)
            a = min(vals[tt] - b * tt - g * comb(tt, 2) for tt in range(tmax + 1))
            M2 = M2lo if g >= 0 else M2hi
            val = a * N + b * M1 + g * M2
            if val > best[0]:
                best = (val, (a, b, g, M2))
    return best, comb(n - 4, s - 4)


if __name__ == "__main__":
    n, q = 32, 383
    L = RS.build(n)
    print(f"published bound L({n},{q}) = {L[n][q]}")
    t = comb(n, 2) - q
    print(f"complement has t = {t} edges; "
          f"P3 in [{P3_min(n,t)}, {P3_max(n,t)}]")
    best = 0
    for s in range(6, n):
        (val, cert), den = certify(n, q, s, L)
        b = RS.ceil_frac(F(val) / den)
        if b > best:
            best = b
            print(f"  s={s:>3}: moment bound {b}   (g={cert[2]})", flush=True)
    print(f"\nsecond-moment bound at (32,383): {best}")
    print(f"published: {L[n][q]};  target 3557;  ceiling 4644")

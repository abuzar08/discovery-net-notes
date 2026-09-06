#!/usr/bin/env python3
"""
Playing a large block against itself: defect Hall, and one-sided high vertices.

STATE BEFORE THIS FILE.  At r = 29 two cases are open:

    order 57, row (57,828), four (|R|, multiset) combinations;
    order 58, class b = 6, c = (51,1) at |R| >= 11.

The absorption argument needs t := chi(G[L]) + |R| - 28 - nu absorptions, and
chi(G[L]) is the largest block order q_1.  So a LARGE largest block makes t large
and the argument harder.  But a large block is also a large clique of G, which
makes the crossing bound easier.  Nothing so far played those two against each
other in one argument.  This file does, through the count of "one-sided" high
vertices, and sharpens the matching bound at the same time.

==============================================================================
ONE-SIDED HIGH VERTICES.  For z in Z (the high vertices other than the
singletons w) put a_z := |N_H(z) ^ Q_1| and b_z := |N_H(z) ^ (Q_2 - Q_1)|, and
let k_1, k_2 count the z with a_z = 0, resp. b_z = 0.

  * a_z = 0 means z is G-adjacent to EVERY vertex of Q_1, so Q_1 together with
    those k_1 vertices is a clique -- less at most e(H[R]) of them, since a set
    of k_1 vertices of R spans at most e(H[R]) non-edges of G and dropping one
    endpoint of each leaves a clique.  Likewise for Q_2 and k_2.
  * A z cannot be one-sided on both sides: it would have no H-neighbour at all
    in L, so d_H(z) <= |R| - 1 and x_z >= 29 - |R|, which the excess budget
    forbids in the range considered.
  * The |R| - k_1 - k_2 remaining vertices of R give a third disjoint clique, of
    order at least |R| - k_1 - k_2 - e(H[R]).

So for each (k_1, k_2) there is a crossing bound
cr(K_{q_1+c_1}) + cr(K_{q_2+c_2}) + cr(K_{rest}) with c_i = max(0, k_i - e(H[R])).

Conversely the k_1 one-sided vertices can NEVER be absorbed -- every colour class
contains a vertex of Q_1, and absorbing z needs z to be H-adjacent to it -- so at
most |Z| - k_1 absorptions are available.

==============================================================================
DEFECT HALL, WHICH IS SHARPER THAN THE COVER BOUND.  Both are lower bounds on
mu_1, but they use different information.  If a set S of z has deficiency
d = |S| - |N(S)| >= 1, then every z in S has N(z) inside N(S), so a_z <= |S| - d,
and therefore

        sum_z a_z  <=  |S|(|S| - d) + (|Z| - |S|) q_1 .

If no |S| makes that at least the known lower bound on sum_z a_z, deficiency d is
impossible.  Hence mu_1 >= |Z| - (largest feasible d).  Knowing k_1 = 0 supplies
a_z >= 1 for every z, which forces |S| >= d + 1 and rules out the |S| = 1 escape.

At (26,20) with |R| = 11 this is decisive: sum_z a_z >= 203 over |Z| = 9 vertices
of a 26-set, and |S|(|S|-d) + (9-|S|) 26 >= 203 fails for every |S| >= 2 at
d >= 1.  So with k_1 = 0 the matching is PERFECT, mu_1 = 9, where the cover bound
gave only 8.

==============================================================================
RESULT.  The combination cuts row (57,828) from its four multisets, each with
many (k_1, k_2), down to NINE fully explicit sub-cases -- and every surviving one
has k_1 at its maximum, which pins the structure hard: there
sum_z a_z is within a few of (|Z| - k_1) q_1, so every z that is not one-sided is
H-adjacent to almost all of Q_1 and G-adjacent to only a handful of it.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import mu58 as MU
from order2r import RCHI, Z

r = RCHI
DEG = r - 1
crK = V.crK


def defect_mu(S, side, nz, amin):
    """mu >= nz - (largest feasible deficiency), given sum >= S, each value at
    most `side`, and each at least `amin`."""
    best = 0
    for d in range(1, nz + 1):
        for sg in range(max(1, d + amin), nz + 1):
            if sg * (sg - d) + (nz - sg) * side >= S:
                best = d
                break
    return nz - best


def singletons(NL, mult, d0):
    q1 = mult[0]
    keff = sum(1 for q in mult if q - 1 >= d0)
    if keff < 2:
        return 0
    return max(0, q1 - -(-(NL - q1) // (keff - 1)))


def survivors(nn, m, RSZ, mult, eL, nw, cw):
    """nw = number of singleton components w (2 at order 57, 1 at order 58)."""
    NL = nn - RSZ
    NZ = RSZ - nw
    d0 = DEG - RSZ
    X = 2 * m - nn * DEG
    base = m - DEG * RSZ - X
    eGR = eL - base
    eHR = RSZ * (RSZ - 1) // 2 - eGR
    if eGR < 0 or eHR < 0 or NZ <= 0:
        return None
    q1 = mult[0]
    q2 = mult[1] if len(mult) > 1 else 1
    nu = min(eHR, RSZ // 2)
    t = q1 + RSZ - 28 - nu
    if t <= 0:
        return []
    s = singletons(NL, mult, d0)
    e1 = q1 * (q1 + RSZ - 29)
    e2 = (q2 - 1) * (q2 + RSZ - 29)
    Sa, Sb = e1 - cw, e2 - cw
    k1max = NZ - -(-max(Sa, 0) // q1)
    k2max = NZ - -(-max(Sb, 0) // max(q2 - 1, 1))
    bad = []
    for k1 in range(0, max(k1max, 0) + 1):
        for k2 in range(0, max(k2max, 0) + 1):
            if k1 + k2 > NZ:
                continue
            c1 = max(0, k1 - eHR)
            c2 = max(0, k2 - eHR)
            rest = max(0, RSZ - k1 - k2 - eHR)
            cross = crK(q1 + c1) + crK(q2 + c2) + crK(rest)
            Za, Zb = NZ - k1, NZ - k2
            mu1 = max(MU.koenig(Sa, q1, Za), defect_mu(Sa, q1, Za, 1)) if Za > 0 else 0
            mu2 = (max(MU.koenig(Sb, max(q2 - 1, 1), Zb),
                       defect_mu(Sb, max(q2 - 1, 1), Zb, 1)) if Zb > 0 else 0)
            ok = cross >= Z or (Za >= t and mu1 >= t
                                and mu1 + mu2 >= NZ + max(0, t - s))
            if not ok:
                bad.append((k1, k2, cross, mu1, mu2))
    return bad


def main():
    print("Playing a large block against itself, at r = %d" % r)
    print("Z(29) = %d" % Z)
    print()

    print("PART 1   order 57, row (57,828)")
    N57 = 2 * r - 1
    tot = 0
    for RSZ, mult in ((10, (24, 23, 2)), (10, (25, 22)), (10, (25, 22, 2)),
                      (11, (26, 20))):
        eL = sum(q * (q - 1) // 2 for q in mult)
        bad = survivors(N57, 828, RSZ, mult, eL, 2, 5)
        tot += len(bad)
        print("   |R|=%2d %-12s -> %s"
              % (RSZ, str(mult),
                 "IMPOSSIBLE" if not bad else
                 "%d sub-cases: %s" % (len(bad), [(b[0], b[1]) for b in bad])))
    print("   order 57 now has %d fully explicit sub-cases, each pinned by"
          " (|R|, multiset, k_1, k_2)." % tot)
    print()

    print("PART 2   order 58, class b = 6, c = (51,1)")
    N58 = 2 * r
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        Rmax = 1 + max(0, X - (r + 2 - 6))
        alive = 0
        rs = set()
        for RSZ in range(11, Rmax + 1):
            NL = N58 - RSZ
            d0 = DEG - RSZ
            base = m - DEG * RSZ - X
            for mult, eL in MU.multisets(NL, max(base, 0),
                                         base + RSZ * (RSZ - 1) // 2, d0, r):
                if sum(crK(q) for q in mult) >= Z:
                    continue
                bad = survivors(N58, m, RSZ, mult, eL, 1, 4)
                if bad:
                    alive += 1
                    rs.add(RSZ)
        print("   m = %d : %d (|R|, multiset) survive, |R| in %s"
              % (m, alive, "-" if not rs else "%d..%d" % (min(rs), max(rs))))
    print()
    print("CONCLUSION")
    print("   Order 57 is down to nine explicit sub-cases; order 58's single")
    print("   class is reduced but not closed.  Neither frontier closes.")


if __name__ == "__main__":
    main()

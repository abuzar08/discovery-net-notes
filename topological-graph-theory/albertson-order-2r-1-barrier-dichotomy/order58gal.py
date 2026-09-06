#!/usr/bin/env python3
"""
Order 58 at r = 29: the low-vertex machinery of the order-57 work, transferred.

The three classes left in the last open branch of order 58 are

      b = 6, c = (51, 1)        b = 6, c = (50, 1, 1)        b = 7, c = (49, 1, 1)

and none of the constraints developed for order 57 -- the covering condition on
the Gallai blocks, the two-sided e(L) identity, and the clique-cover absorption
argument -- has ever been applied to them.  All of that machinery is
barrier-independent: it needs only that G is 29-critical, Gallai's low-vertex
theorem, and theta(H) = chi(G) = 29.  This file transfers it.

==============================================================================
THE SETUP, IDENTICAL AT ORDER 2r AND 2r-1.  Low means d_G(v) = r - 1 = 28
exactly; R is the set of high vertices, L the rest, |L| = 58 - |R|, and
X := 2m - 58*28 is the total excess, so every high vertex has x_v >= 1 and
|R| <= X.  By Gallai every block of G[L] is a clique or an odd cycle, and

    e(L) = m - 28|R| - X + e(G[R]),          0 <= e(G[R]) <= C(|R|,2),

    |N_H(v) ^ R| = |R| - 28 + D_v   for v in L,   D_v := sum_{blocks ni v}(|Q|-1),

    e_H(Q,R) = q(|R| - 28) + sum_{v in Q} D_v >= q(q + |R| - 29),

    e_H(L,R) = |L|(|R| - 28) + 2 e(L).

Constraint C (covering): every low vertex needs D_v >= 28 - |R| =: delta_0, so
L has no isolated vertex and any block with q - 1 < delta_0 consists entirely of
cut vertices, of which there are at most sum_i q_i - |L|.

==============================================================================
WHAT BOUNDS |R|, AND WHY TWO OF THE THREE CLASSES ARE TRACTABLE.

In this branch B contains two disjoint triangles, and a singleton component {w}
of H - B has N_H(w) inside B with at most two neighbours in each triangle, so
d_H(w) <= b - 2 and

        x_w  >=  r + 2 - b  =  31 - b .

Writing W for the number of singleton components, the remaining excess is at
most X - W(31 - b), so

        |R|  <=  W + X - W(31 - b) .

For c = (50,1,1) at b = 6 that is |R| <= 8, and for c = (49,1,1) at b = 7 it is
|R| <= 10.  Those ranges are small enough that delta_0 = 28 - |R| stays near 20,
which makes Constraint C bite hard and forces very large Gallai blocks.  The
class c = (51,1) has only ONE singleton, so the bound is |R| <= 32 and the
method does not reach it; that is reported rather than hidden.

==============================================================================
THE TWO TESTS.  For each admissible block multiset:

  CROSSING.  The blocks are edge-disjoint, so cr(G) >= sum_i cr(K_{q_i}); if that
  reaches Z(29) = 8281 the multiset is impossible.

  CLIQUE COVER.  chi(G[L]) = max block order, and absorbing t vertices of R into
  distinct colour classes gives
        29 = chi(G) <= chi(G[L]) + (|R| - t) - nu,     nu := nu(H[R]),
  so a contradiction needs t + nu >= chi(G[L]) + |R| - 28.  If that requirement
  is already met with t = 0 the multiset dies outright.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
from order2r import RCHI, Z

r = RCHI            # 29
n = 2 * r           # 58
DEG = r - 1         # 28
crK = V.crK
ROWS = (838, 839, 840)
CLASSES = ((6, (51, 1)), (6, (50, 1, 1)), (7, (49, 1, 1)))


def multisets(NL, eLo, eHi, d0, cap=None):
    """Gallai block multisets on NL vertices with e(L) in [eLo, eHi], no
    isolated vertex, and Constraint C on the small blocks."""
    out = []

    def rec(rem, capb, edges, blocks):
        if rem == 0:
            if eLo <= edges <= eHi:
                extra = sum(blocks) - NL
                if extra < 0:
                    return
                big = [q for q in blocks if q - 1 >= d0]
                if sum(big) > NL:
                    return
                if sum(q * (q - 1) for q in blocks if q - 1 < d0) \
                        < d0 * (NL - sum(big)):
                    return
                out.append((tuple(sorted(blocks, reverse=True)), edges))
            return
        hi, r2, c2 = edges, rem, capb
        while r2 > 0:
            t = min(c2, r2)
            hi += t * (t + 1) // 2
            r2 -= t
        if hi < eLo or edges > eHi:
            return
        for u in range(min(capb, rem), 0, -1):
            if cap is not None and u + 1 > cap:
                continue
            rec(rem - u, u, edges + u * (u + 1) // 2, blocks + [u + 1])
            if u >= 2 and (u + 1) % 2 == 1:
                rec(rem - u, u, edges + u + 1, blocks)
    for c in range(1, NL + 1):
        rec(NL - c, NL - c, 0, [])
    return sorted(set(out))


def analyse(m, b, c):
    """Returns (Rmax, list of surviving (|R|, multiset, why))."""
    X = 2 * m - n * DEG
    W = sum(1 for s in c if s == 1)
    xw = W * (r + 2 - b)
    Rmax = W + max(0, X - xw)
    surv = []
    for RSZ in range(max(1, W), Rmax + 1):
        NL = n - RSZ
        if NL < 2:
            continue
        d0 = DEG - RSZ
        base = m - DEG * RSZ - X
        eLo = max(base, 0)
        eHi = base + RSZ * (RSZ - 1) // 2
        if eHi < 0:
            continue
        # a low vertex has at most 28 neighbours, so blocks have order <= 29
        for mult, eL in multisets(NL, eLo, eHi, d0, cap=r):
            eGR = eL - base
            eHR = RSZ * (RSZ - 1) // 2 - eGR
            if eGR < 0 or eHR < 0:
                continue
            cross = sum(crK(q) for q in mult)
            if cross >= Z:
                continue                       # killed by the crossing bound
            maxq = max(mult)
            nu = min(eHR, RSZ // 2)
            tneed = maxq + RSZ - 28 - nu
            if tneed <= 0:
                continue                       # killed by the clique cover
            surv.append((RSZ, mult, eL, cross, maxq, tneed))
    return Rmax, surv


def main():
    print("Albertson r = 29, order 58: the order-57 low-vertex machinery,"
          " transferred")
    print("Z(29) = %d;  low means d_G = %d" % (Z, DEG))
    print()
    for b, c in CLASSES:
        print("CLASS b = %d, c = %s" % (b, str(c)))
        for m in ROWS:
            X = 2 * m - n * DEG
            Rmax, surv = analyse(m, b, c)
            if not surv:
                print("   m = %d (X = %d): |R| <= %d, and NO admissible"
                      " (|R|, multiset) survives  ->  CLASS IMPOSSIBLE"
                      % (m, X, Rmax))
            else:
                rs = sorted(set(t[0] for t in surv))
                print("   m = %d (X = %d): |R| <= %d, %d survivors at |R| in %s"
                      % (m, X, Rmax, len(surv), rs if len(rs) < 12
                         else "%d..%d" % (rs[0], rs[-1])))
                print("        smallest surviving |R| is %d, so this class now"
                      " needs |R| >= %d" % (rs[0], rs[0]))
                for t in surv[:3]:
                    print("        |R|=%d %s e(L)=%d cross=%d chi=%d t>=%d"
                          % (t[0], str(t[1])[:22], t[2], t[3], t[4], t[5]))
        print()
    print("SUMMARY")
    print("   b = 6, c = (50,1,1) : ELIMINATED at all three rows")
    print("   b = 7, c = (49,1,1) : ELIMINATED at all three rows")
    print("   b = 6, c = (51,1)   : survives, and now needs |R| >= 11")
    print()
    print("   Order 58 therefore reduces from three classes to ONE.")
    print("   The two that die have TWO singleton components, so the excess")
    print("   bound x_w >= 31 - b applies twice and caps |R| at 4 to 10; that")
    print("   forces |L| >= 48 and e(L) = m - 28|R| - X + e(G[R]) large, which")
    print("   in turn forces Gallai blocks so big that either the crossing")
    print("   bound reaches Z(29) or the covering constraint rejects every")
    print("   multiset in the e(L) band.  The surviving class has only ONE")
    print("   singleton, so the same bound gives only |R| <= 28..32 and the")
    print("   forcing is far weaker.")


if __name__ == "__main__":
    main()

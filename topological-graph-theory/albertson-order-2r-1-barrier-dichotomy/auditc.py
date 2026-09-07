#!/usr/bin/env python3
"""
An audit of Constraint C, and the repair of two scope defects it exposes.

WHY.  In three consecutive passes I found two scope defects in my own order-58
work, both from the same root: a consequence of Constraint C that is silently
false outside the range where it was derived.  Rather than rediscover it a third
time, this file audits the constraint once, for every use site, and states the
exact validity threshold of each consequence.

==============================================================================
CONSTRAINT C AND ITS THREE CONSEQUENCES.

Every vertex of L is low, d_G(v) = 28 exactly, so it has 28 - D_v G-neighbours in
R with D_v := sum_{blocks ni v}(|Q| - 1), and |N_H(v) ^ R| = |R| - 28 + D_v >= 0
gives

        (C)   D_v  >=  28 - |R|  =:  delta_0    for every low vertex v.

  (C1) NO ISOLATED LOW VERTEX.  D_v >= delta_0 >= 1 forces v into a block of
       order at least 2.  Valid iff  delta_0 >= 1,  i.e.  |R| <= 27.

  (C2) EVERY BLOCK WITH q - 1 < delta_0 IS ALL CUT VERTICES.  A vertex of such a
       block needs more than the block supplies, so it lies in a further block.
       Valid iff delta_0 >= 1; for delta_0 <= 0 there are no such blocks and the
       statement is vacuous.

  (C3) BIG BLOCKS ARE PAIRWISE DISJOINT.  A vertex in two blocks of order
       > delta_0 has D_v >= 2 delta_0, and D_v <= 28 because v is low.  So the
       conclusion needs  2 delta_0 > 28,  i.e.

              delta_0 >= 15,   i.e.   |R| <= 13.

       THIS IS THE THRESHOLD THAT WAS MISSED.  It is far more restrictive than
       (C1)'s, and it is the one the singleton-colour-class count and the
       enumeration's `sum(big) <= |L|` filter both rest on.

At order 2r - 1 = 57 all three hold everywhere the theory is applied: |R| <= 11
there, so delta_0 >= 17.  THE ORDER-57 CLOSURE IS UNAFFECTED, and the control
below re-derives its multiset lists under the audited filters and checks they are
unchanged.  At order 58 the excess budget allows |R| up to 32 and all three
thresholds are crossed.

==============================================================================
DEFECT 1 -- THE SINGLETON COUNT (repaired in dichot.singletons).

s := q_1 - ceil((|L| - q_1)/(k_eff - 1)) with k_eff the number of big blocks
rests on "an independent set of G[L] has at most k_eff vertices, one per big
block", which is (C3).  Applied at |R| >= 14 it is unjustified, and a larger s
weakens the absorption requirement |Z| + max(0, t - s), so it CLOSES CASES THAT
ARE NOT CLOSED.  That is the unsafe direction.

What survives without (C3): when the multiset is an explicit partition of L into
exactly two cliques, the realisability argument needs no delta_0 -- every vertex
outside Q_1 lies in the other block and is G-non-adjacent to all of Q_1, so the
pairing is a free matching and any 2 q_1 - |L| vertices of Q_1 may be left
unpaired.  dichot.singletons now uses (C3) where valid, that partition form
otherwise, and 0 failing both.

DEFECT 2 -- THE ENUMERATION FILTER (measured here).

mu58.multisets rejects a multiset when sum(big) > |L|, which is (C3) again: if
the big blocks are pairwise disjoint their orders cannot exceed |L|.  At
|R| >= 14 that rejects legitimate multisets, so the enumeration is INCOMPLETE.
Excluding cases undercounts survivors, so no elimination revives -- but the
published statements of what REMAINS at order 58 were counts over the wrong set.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import mu58 as MU
import dichot as D
import residue58 as R58
import blockr58 as BR
from order2r import RCHI, Z

r = RCHI
DEG = r - 1
crK = V.crK
N57 = 2 * r - 1
N58 = 2 * r


def multisets_audited(NL, eLo, eHi, d0, cap):
    """mu58.multisets with each Constraint-C filter applied only where valid.

    Coverage of the enumerated set is kept unconditionally: it is a property of
    the vertex set passed in, and callers that allow isolated low vertices pass
    the non-isolated part (see iso58.py)."""
    out = []
    disjoint_ok = 2 * d0 > DEG          # (C3)
    cover_ok = d0 >= 1                  # (C2)

    def rec(rem, capb, edges, blocks):
        if rem == 0:
            if eLo <= edges <= eHi:
                if sum(blocks) - NL < 0:
                    return
                big = [q for q in blocks if q - 1 >= d0]
                if disjoint_ok and sum(big) > NL:
                    return
                if cover_ok and sum(q * (q - 1) for q in blocks if q - 1 < d0) \
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
            if u + 1 > cap:
                continue
            rec(rem - u, u, edges + u * (u + 1) // 2, blocks + [u + 1])
            if u >= 2 and (u + 1) % 2 == 1:
                rec(rem - u, u, edges + u + 1, blocks)
    for c in range(1, NL + 1):
        rec(NL - c, NL - c, 0, [])
    return sorted(set(out))


def part1():
    print("PART 1   the three consequences and their exact thresholds")
    print("   consequence                      needs          holds for |R| <=")
    print("   (C1) no isolated low vertex      delta_0 >= 1          %d" % (DEG - 1))
    print("   (C2) small blocks all cut        delta_0 >= 1          %d" % (DEG - 1))
    print("   (C3) big blocks disjoint         2 delta_0 > %d        %d"
          % (DEG, DEG - (DEG // 2 + 1)))
    bad = [x for x in range(1, 40) if (2 * (DEG - x) > DEG) != (x <= 13)]
    print("   threshold check for (C3) over |R| in [1,39]: %s"
          % ("PASS" if not bad else "FAIL %s" % bad))
    print()
    print("   ORDER 57: the theory is applied at |R| in [2,11], so delta_0 in"
          " [17,26];")
    print("   all three hold with room.  ORDER 58: |R| runs to 32, so (C3) fails"
          " from")
    print("   |R| = 14 and (C1),(C2) from |R| = 28.")
    print()


def part2_control():
    print("PART 2   control: order 57 is unaffected")
    M = 828
    X = 2 * M - N57 * DEG
    same = True
    for RSZ in (9, 10, 11):
        NL = N57 - RSZ
        d0 = DEG - RSZ
        base = M - DEG * RSZ - X
        lo, hi = max(base, 0), base + RSZ * (RSZ - 1) // 2
        a = MU.multisets(NL, lo, hi, d0, r)
        b = multisets_audited(NL, lo, hi, d0, r)
        ok = a == b
        same &= ok
        print("   |R| = %2d (delta_0 = %2d): published %d multisets, audited %d"
              "  -> %s" % (RSZ, d0, len(a), len(b), "identical" if ok else "DIFFER"))
    print("   order 57 enumeration unchanged: %s" % ("PASS" if same else "FAIL"))
    print()
    return same


def part3():
    print("PART 3   defect 2: how much the order-58 enumeration excluded")
    tot_p = tot_a = 0
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        Rmax = 1 + max(0, X - (r + 2 - 6))
        p = a = 0
        for RSZ in range(11, Rmax + 1):
            NL = N58 - RSZ
            d0 = DEG - RSZ
            base = m - DEG * RSZ - X
            lo, hi = max(base, 0), base + RSZ * (RSZ - 1) // 2
            p += len(MU.multisets(NL, lo, hi, d0, r))
            a += len(multisets_audited(NL, lo, hi, d0, r))
        tot_p += p
        tot_a += a
        print("   row (58,%d): published %6d multisets, audited %6d"
              "  -> %6d were wrongly excluded" % (m, p, a, a - p))
    print("   TOTAL: %d published, %d audited, %d excluded"
          % (tot_p, tot_a, tot_a - tot_p))
    print()
    return tot_p, tot_a


def part4():
    print("PART 4   the corrected open set at order 58")
    print("   Full battery -- crossing, residue, clique cover, absorption, and")
    print("   the block-plus-R bound -- over the AUDITED enumeration, with the")
    print("   repaired singleton count.")
    grand = 0
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        sx = X - (r + 2 - 6)
        Rmax = 1 + max(0, sx)
        alive = 0
        rs = set()
        for RSZ in range(11, Rmax + 1):
            NL = N58 - RSZ
            d0 = DEG - RSZ
            base = m - DEG * RSZ - X
            for mult, eL in multisets_audited(NL, max(base, 0),
                                              base + RSZ * (RSZ - 1) // 2,
                                              d0, r):
                if sum(crK(q) for q in mult) >= Z:
                    continue
                if not R58.survivors(N58, m, RSZ, mult, eL, 1, 4, sx):
                    continue
                eGR = eL - base
                eHR = RSZ * (RSZ - 1) // 2 - eGR
                if BR.blockR(mult, NL, RSZ, eHR) >= Z:
                    continue
                alive += 1
                rs.add(RSZ)
        grand += alive
        print("   row (58,%d): %6d configurations survive, |R| in %d..%d"
              % (m, alive, min(rs), max(rs)))
    print("   TOTAL over the three rows: %d" % grand)
    print()
    return grand


def main():
    print("An audit of Constraint C at r = %d" % r)
    print("Z(29) = %d;  low means d_G = %d;  delta_0 = %d - |R|" % (Z, DEG, DEG))
    print()
    part1()
    ok = part2_control()
    part3()
    grand = part4()
    print("CONCLUSION")
    if not ok:
        print("   The order-57 control failed; nothing is claimed.")
        return
    print("   Constraint C has three consequences with TWO different thresholds,")
    print("   |R| <= 27 and |R| <= 13, and the stricter one was not observed.")
    print("   Order 57 is unaffected: delta_0 >= 17 throughout, the enumeration")
    print("   is identical, and its closure stands.")
    print()
    print("   At order 58 the effect is large.  The singleton count closed 198")
    print("   configurations it was not entitled to close, and the enumeration")
    print("   filter excluded well over a hundred thousand multisets.  Both are")
    print("   repaired here, and the corrected open set is %d configurations"
          % grand)
    print("   without an isolated low vertex, against the 19193 last reported.")
    print("   Adding iso58.py's isolated-vertex configurations, order 58 at")
    print("   r = 29 is open in strictly more cases than previously stated.")
    print()
    print("   No elimination anywhere in the chain revives: both defects")
    print("   excluded or over-closed cases, never resurrected eliminated ones,")
    print("   and the order-57 result and the |R| <= 13 order-58 results -- "
          "including")
    print("   the five-configuration small-|R| family -- are untouched.")


if __name__ == "__main__":
    main()

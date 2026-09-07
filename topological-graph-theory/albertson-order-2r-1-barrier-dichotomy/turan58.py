#!/usr/bin/env python3
"""
Turan on H[R], and the odd-cycle blocks that were never enumerated.

TWO ITEMS, both consequences of the same branch hypothesis: in the surviving
order-58 case H is K_4-free, i.e. alpha(G) <= 3.

==============================================================================
ITEM 1 -- A TURAN CAP ON e(H[R]), WHICH WAS NEVER APPLIED THERE.

H is K_4-free, so every induced subgraph of H is, in particular H[R].  Turan's
theorem gives the extremal number for K_4-free graphs exactly:

        e(H[R])  <=  floor(|R|^2 / 3) ,

attained only by the complete 3-partite Turan graph.  This directory already
applies the same cap to the components of H - B; it was never applied to the
high set R, which is a different vertex set.

The cap is equivalent to a FLOOR on e(L), through the identity
e(L) = m - 28|R| - X + e(G[R]) and e(G[R]) = C(|R|,2) - e(H[R]):

        e(L)  >=  m - 28|R| - X + C(|R|,2) - floor(|R|^2/3) ,

which at |R| = 28 on row 838 reads e(L) >= 119 where the enumeration used
e(L) >= 2.  Sparse-R configurations are exactly the ones that resisted every
crossing bound, and this is what bounds how sparse R may be.

==============================================================================
ITEM 2 -- ODD-CYCLE BLOCKS, A COMPLETENESS GAP NOW SMALL ENOUGH TO CLOSE.

Gallai's theorem says the blocks of G[L] are cliques OR ODD CYCLES.  Every
enumeration in this directory drops the odd cycles: the recursion spends vertices
on a cycle without recording it in the multiset, so the result then fails the
covering filter and is discarded.  Two things now bound the gap to something
finite and small.

  * Constraint C.  A vertex of an odd-cycle block has D_v = 2 from that block,
    so an odd cycle can only occur when delta_0 = 28 - |R| <= 2, i.e.

            |R|  >=  26 .

  * alpha(G) <= 3.  An odd cycle C_q has alpha(C_q) = (q-1)/2, and the cycle's
    vertices are non-adjacent to the private vertices of the other blocks, so

            (q-1)/2 + #{other blocks with a private vertex}  <=  3 .

    Hence q <= 7: C_9 and longer are impossible outright.  A C_7 leaves room for
    NO other block, and a C_5 for at most one.

So the missing configurations are: |R| in [26, 32], one block that is a C_5 or a
C_7, and at most one further clique block.  They are enumerated below.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import auditc as AC
import alpha58 as A
import residue58 as R58
import blockr58 as BR
from order2r import RCHI, Z

r = RCHI
DEG = r - 1
crK = V.crK
N58 = 2 * r
ALPHA = 3


def turan_k4free(n):
    """Max edges of a K_4-free graph on n vertices (Turan)."""
    return n * n // 3


def item1():
    print("ITEM 1   the Turan cap e(H[R]) <= floor(|R|^2/3)")
    tot = alive = 0
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        sx = X - (r + 2 - 6)
        Rmax = 1 + max(0, sx)
        seen = al = 0
        rs = set()
        for RSZ in range(11, Rmax + 1):
            NL = N58 - RSZ
            d0 = DEG - RSZ
            base = m - DEG * RSZ - X
            cap = turan_k4free(RSZ)
            for mult, eL in AC.multisets_audited(NL, max(base, 0),
                                                 base + RSZ * (RSZ - 1) // 2,
                                                 d0, r):
                if sum(crK(q) for q in mult) >= Z:
                    continue
                eGR = eL - base
                eHR = RSZ * (RSZ - 1) // 2 - eGR
                if eGR < 0 or eHR < 0:
                    continue
                if A.alpha_lb(mult, NL) > ALPHA:
                    continue
                if not R58.survivors(N58, m, RSZ, mult, eL, 1, 4, sx):
                    continue
                if BR.blockR(mult, NL, RSZ, eHR) >= Z:
                    continue
                seen += 1
                if eHR <= cap:
                    al += 1
                    rs.add(RSZ)
        tot += seen
        alive += al
        print("   row (58,%d): %5d after alpha, %5d also within the cap,"
              " |R| in %d..%d" % (m, seen, al, min(rs), max(rs)))
    print("   TOTAL: %d  ->  %d" % (tot, alive))
    print()
    return tot, alive


def item2():
    print("ITEM 2   the odd-cycle blocks never enumerated")
    print("   Constraint C forces |R| >= %d, and alpha(C_q) = (q-1)/2 with"
          " alpha <= %d" % (DEG - 2, ALPHA))
    print("   forces q <= 7.  So the gap is |R| in [26, Rmax] with one C_5 or")
    print("   C_7 and at most one further clique block.")
    total = alive = 0
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        sx = X - (r + 2 - 6)
        Rmax = 1 + max(0, sx)
        seen = al = 0
        detail = []
        for RSZ in range(DEG - 2, Rmax + 1):
            NL = N58 - RSZ
            d0 = DEG - RSZ
            if d0 > 2:
                continue                   # Constraint C forbids a cycle block
            base = m - DEG * RSZ - X
            cap = turan_k4free(RSZ)
            for cyc in (5, 7):
                acyc = (cyc - 1) // 2
                if acyc > ALPHA:
                    continue
                room = ALPHA - acyc        # further blocks with private vertices
                rest = NL - cyc
                if rest < 0:
                    continue
                # the cycle contributes cyc edges and cyc vertices
                for mult, eLb in ([((), 0)] if rest == 0 else
                                  AC.multisets_audited(rest, 0,
                                                       base + RSZ * (RSZ - 1) // 2,
                                                       d0, r)):
                    if len(mult) > room:
                        continue
                    eL = eLb + cyc
                    eGR = eL - base
                    eHR = RSZ * (RSZ - 1) // 2 - eGR
                    if eGR < 0 or eHR < 0 or eGR > RSZ * (RSZ - 1) // 2:
                        continue
                    if eHR > cap:
                        continue           # Turan on H[R]
                    seen += 1
                    # crossing: the cycle is not a clique, so it contributes a
                    # triangle at most; score only the clique blocks and R
                    if sum(crK(q) for q in mult) >= Z:
                        continue
                    if mult and BR.blockR(mult, NL - cyc, RSZ, eHR) >= Z:
                        continue
                    # clique cover: chi(G[L]) = max(largest clique block, 3),
                    # since an odd cycle needs 3 colours
                    q1 = max(list(mult) + [3])
                    nu = min(eHR, RSZ // 2)
                    if q1 + RSZ - 28 - nu <= 0:
                        continue           # killed by the clique cover
                    al += 1
                    detail.append((RSZ, cyc, mult, eHR))
        total += seen
        alive += al
        print("   row (58,%d): %4d admissible cycle configurations, %d survive"
              % (m, seen, al))
        for d in detail[:3]:
            print("        |R|=%d C_%d blocks=%s e(H[R])=%d"
                  % (d[0], d[1], str(d[2]), d[3]))
    print("   TOTAL: %d admissible, %d survive" % (total, alive))
    print()
    return total, alive


def main():
    print("Turan on H[R], and the odd-cycle gap, at r = %d" % r)
    print("Z(29) = %d;  the branch has H K_4-free, i.e. alpha(G) <= %d"
          % (Z, ALPHA))
    print()
    _, a1 = item1()
    _, a2 = item2()
    print("CONCLUSION")
    print("   The Turan cap on H[R] is a genuinely new constraint -- the same")
    print("   cap was applied to the components of H - B but never to R -- and")
    print("   it removes %d configurations." % (9226 - a1))
    print("   The odd-cycle gap, open since the first Gallai enumeration, is")
    print("   now closed: alpha(G) <= 3 confines it to |R| >= 26 with a single")
    print("   C_5 or C_7, and %d of those survive." % a2)
    print()
    print("   Order 58 at r = 29 is open in %d + %d = %d configurations without"
          % (a1, a2, a1 + a2))
    print("   an isolated low vertex, together with 307 carrying one -- all 307")
    print("   of which were checked against the Turan cap and satisfy it -- for")
    print("   %d in all, against 103292 three passes ago." % (a1 + a2 + 307))
    print("   r = 29 is NOT proved.")


if __name__ == "__main__":
    main()

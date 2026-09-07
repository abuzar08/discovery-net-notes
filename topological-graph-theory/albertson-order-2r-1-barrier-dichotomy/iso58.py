#!/usr/bin/env python3
"""
A completeness gap at |R| >= 28, found and repaired: isolated low vertices.

WHAT WAS ASSUMED.  Every block-multiset enumeration in this directory requires
the Gallai blocks of G[L] to COVER L -- the filter is `sum(mult) >= |L|`, and no
block of order 1 is ever emitted.  That is Constraint C: a low vertex needs

        D_v  >=  28 - |R|  =:  delta_0 ,

so when delta_0 >= 1 it lies in a block of order at least 2 and L has no vertex
isolated in G[L].  The justification FAILS when delta_0 <= 0.

At order 2r - 1 = 57 that never happened: |R| <= 11 there, so delta_0 >= 17.  At
order 58 it does.  The excess budget allows |R| <= X - 24, which is 28, 30 and 32
on the three rows, and delta_0 = 28 - |R| <= 0 exactly when |R| >= 28.  So the
published order-58 enumeration is COMPLETE for |R| <= 27 and INCOMPLETE for
|R| >= 28: configurations in which some low vertex lies in no block at all were
silently excluded.  This file enumerates them.

The gap direction matters.  Excluding cases makes a survivor COUNT too small,
not too large, so nothing previously reported as eliminated becomes alive again;
what was at risk was the claim that the listed survivors are all of them.

==============================================================================
WHAT AN ISOLATED LOW VERTEX FORCES.

Let v in L have D_v = 0.  Then v has no G-neighbour in L, so all 28 of them lie
in R and |R| >= 28; and the per-block identity gives

        |N_H(v) ^ R|  =  |R| - 28 + D_v  =  |R| - 28 .

Hence {v} u R spans |R| + 1 vertices and misses exactly (|R| - 28) + e(H[R])
edges: v's own H-edges to R, and the H-edges inside R.  It is a near-complete
graph, scored by crminus.g.

ALL the isolated vertices go in at once.  They are pairwise non-adjacent in G,
which costs C(iso,2) further missing edges, but that is far cheaper than leaving
them out, since g grows superlinearly in the number of vertices.  So with iso of
them, R u Iso spans |R| + iso vertices missing at most
e(H[R]) + C(iso,2) + iso(|R| - 28), and it is vertex-disjoint from every block:

    cr(G) >= g(|R| + iso, e(H[R]) + C(iso,2) + iso(|R|-28)) + sum_i cr(K_{q_i}).

This does NOT close by itself.  g(29,0) = 7507 is below Z(29) = 8281 -- the
machinery's own lower bound for cr(K_29) is not yet 8281 -- so at |R| = 28 with
e(H[R]) = 0 the near-clique alone is not a contradiction.  It is one when the
missing count is zero, since then K_29 is a subgraph of G outright and
cr(G) >= cr(K_29) with no numbers at all; that needs |R| = 28 and e(H[R]) = 0.

==============================================================================
DEFECT 2 OF THE CONSTRAINT C AUDIT APPLIES HERE TOO.  This file enumerates the
block multisets on the NON-isolated part of L, and it did so through
mu58.multisets, which rejects sum(big) > |L| -- consequence (C3), valid only for
|R| <= 13.  Every |R| in this file is at least 28, where (C3) is maximally false,
so the counts below were themselves under-counts.  The enumeration now goes
through auditc.multisets_audited, which applies each Constraint C filter only in
the range where it is justified.

==============================================================================
THE TEST.  For every row, every |R| >= 28, every number iso >= 1 of isolated low
vertices and every block multiset on the remaining |L| - iso vertices, take the
maximum of the near-clique bound above and the block-plus-R bound of blockr58,
and ask whether it reaches Z(29).

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import crminus as C
import auditc as AC
import blockr58 as BR
import residue58 as R58
from order2r import RCHI, Z

r = RCHI
DEG = r - 1
crK = V.crK
N58 = 2 * r


def iso_bound(mult, RSZ, eHR, iso):
    """Merge ALL the isolated low vertices with R, not just one.

    The iso isolated vertices are pairwise non-adjacent in G, so they contribute
    C(iso,2) missing edges among themselves; each has |R| - 28 H-neighbours in
    R; and R itself misses e(H[R]).  So R u Iso spans |R| + iso vertices and
    misses at most e(H[R]) + C(iso,2) + iso(|R| - 28).  It is vertex-disjoint
    from every block of G[L]."""
    f = eHR + iso * (iso - 1) // 2 + iso * (RSZ - DEG)
    if f < 0:
        return 0
    return C.g(RSZ + iso, f) + sum(crK(q) for q in mult)


def forced_K29(RSZ, eHR):
    """{v} u R contains K_29 outright: no crossing number is needed."""
    return RSZ - DEG + eHR == 0 and RSZ + 1 >= r


def run():
    print("Isolated low vertices at order 58: the range delta_0 <= 0")
    print("Z(29) = %d;  an isolated low vertex needs |R| >= %d" % (Z, DEG))
    print()
    grand_alive = 0
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        sx = X - (r + 2 - 6)
        Rmax = 1 + max(0, sx)
        print("ROW (58,%d):  X = %d, |R| <= %d, so delta_0 <= 0 for |R| in [%d,%d]"
              % (m, X, Rmax, DEG, Rmax))
        if Rmax < DEG:
            print("   no such |R| on this row")
            print()
            continue
        for RSZ in range(DEG, Rmax + 1):
            NL = N58 - RSZ
            d0 = DEG - RSZ
            base = m - DEG * RSZ - X
            seen = alive = kfree = 0
            worst = None
            # The degenerate tail: fewer than two vertices left for blocks, so
            # G[L] has no block at all and chi(G[L]) = 1.  Then the clique cover
            # gives 29 <= 1 + |R| - t - nu with t <= |Z|, and it is checked here
            # rather than left out of the enumeration.
            for NB in (0, 1):
                iso = NL - NB
                if iso < 1:
                    continue
                eL = 0
                eGR = eL - base
                eHR = RSZ * (RSZ - 1) // 2 - eGR
                if eGR < 0 or eHR < 0:
                    continue
                seen += 1
                nu = min(eHR, RSZ // 2)
                if 1 + RSZ - 28 - nu <= 0:
                    continue               # killed by the clique cover outright
                if forced_K29(RSZ, eHR):
                    kfree += 1
                    continue
                if iso_bound((), RSZ, eHR, iso) >= Z:
                    continue
                alive += 1
                if worst is None:
                    worst = (iso_bound((), RSZ, eHR, iso), iso, (), eHR)

            for iso in range(1, NL - 1):
                NB = NL - iso              # vertices actually inside blocks
                if NB < 2:
                    break
                for mult, eL in AC.multisets_audited(NB, max(base, 0),
                                             base + RSZ * (RSZ - 1) // 2,
                                             d0, r):
                    eGR = eL - base
                    eHR = RSZ * (RSZ - 1) // 2 - eGR
                    if eGR < 0 or eHR < 0:
                        continue
                    seen += 1
                    if forced_K29(RSZ, eHR):
                        kfree += 1
                        continue           # K_29 is a subgraph of G outright
                    v = max(iso_bound(mult, RSZ, eHR, iso),
                            BR.blockR(mult, NL, RSZ, eHR))
                    if v >= Z:
                        continue
                    # The clique-cover and absorption battery.  chi(G[L]) is
                    # still the largest block order, since G[L] is a disjoint
                    # union of cliques and isolated vertices; and an isolated
                    # vertex only ENLARGES the independent sets, so the count s
                    # of singleton colour classes computed from the blocks alone
                    # is an under-estimate, which is the safe direction.
                    if not R58.survivors(N58, m, RSZ, mult, eL, 1, 4, sx):
                        continue
                    alive += 1
                    if worst is None or v < worst[0]:
                        worst = (v, iso, mult, eHR)
            grand_alive += alive
            print("   |R| = %2d (delta_0 = %3d, |L| = %2d): %6d configurations"
                  " with an isolated low vertex; %d killed by a forced K_29,"
                  " %d survive" % (RSZ, d0, NL, seen, kfree, alive))
            if worst:
                print("        weakest: iso=%d %s e(H[R])=%d bound %d, short %d"
                      % (worst[1], str(worst[2])[:30], worst[3], worst[0],
                         Z - worst[0]))
        print()
    return grand_alive


def main():
    alive = run()
    print("CONCLUSION")
    print("   The published order-58 enumeration is COMPLETE for |R| <= 27,")
    print("   where Constraint C forbids an isolated low vertex, and was")
    print("   INCOMPLETE for |R| >= 28.  The missing configurations are")
    print("   enumerated above.")
    if alive == 0:
        print("   Every one of them is impossible, so the gap is closed and the")
        print("   previously reported survivor sets are complete after all.")
    else:
        print("   %d of them survive, so they are a genuine addition to the"
              % alive)
        print("   open set: order 58 at r = 29 is open in the configurations")
        print("   previously listed TOGETHER WITH these.  Reported, not hidden.")
    print()
    print("   Order 58 at r = 29 remains open; r = 29 is not proved.")


if __name__ == "__main__":
    main()

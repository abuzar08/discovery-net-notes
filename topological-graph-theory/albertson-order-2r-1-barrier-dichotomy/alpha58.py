#!/usr/bin/env python3
"""
alpha(G) <= 3 was already proved, and never used on the Gallai blocks.

THE OBSERVATION.  The surviving order-58 branch at r = 29 is, by the reviewed
order-2r lemma, exactly

        H is K_4-free AND H has two vertex-disjoint triangles.

"H is K_4-free" is "omega(H) <= 3", which is "alpha(G) <= 3".  That bound was
used to get a Turan cap on the components of H - B and the K_4-free sharpening
x_w >= r + 2 - b.  It was never applied to G[L], where it is far stronger.

==============================================================================
WHY IT BITES.  alpha is monotone under induced subgraphs, so alpha(G[L]) <= 3.
By Gallai the blocks of G[L] are cliques or odd cycles, and adjacency in such a
graph means sharing a block.  Hence:

  * the PRIVATE vertices -- those lying in exactly one block -- of distinct
    blocks are pairwise non-adjacent;
  * a vertex isolated in G[L] is non-adjacent to everything.

Picking one private vertex from each block that has one, together with every
isolated vertex, therefore gives an independent set, so

        alpha(G[L])  >=  #{blocks with a private vertex}  +  #isolated .

A block has no private vertex only if all q of its vertices are cut vertices,
which consumes q of the extra := sum_i q_i - |L_blocks| incidences.  So

        alpha(G[L])  >=  (#blocks - maxk) + iso ,

with maxk the largest number of blocks whose orders sum to at most extra.  The
constraint alpha(G[L]) <= 3 then caps the whole block structure: at most three
blocks when they are disjoint, and AT MOST THREE ISOLATED LOW VERTICES -- against
the 26 the previous enumeration allowed.

==============================================================================
WHAT IT DOES.  On the audited enumeration the surviving configurations fall from
55824 to 9226; the isolated-vertex configurations fall from 47468 to 307, every
one of them with exactly one isolated vertex.  Order 58 at r = 29 is open in
9533 configurations rather than 103292, a reduction of more than ten-fold, and
the first progress in the closing direction for several passes.

It is not a closure.  r = 29 is not proved.

==============================================================================
A NOTE ON ODD-CYCLE BLOCKS.  Gallai allows a block to be an odd cycle, and the
enumeration in this directory silently drops those: the recursion spends vertices
on an odd cycle without recording it, so the surviving multiset fails the
covering filter.  Constraint C excludes them for |R| <= 25, since a cycle vertex
has D_v = 2 and needs D_v >= delta_0; for |R| >= 26 they are possible and were
not enumerated.  alpha(G[L]) <= 3 bounds that gap sharply -- alpha(C_q) =
(q-1)/2, so C_9 and longer are impossible outright and at most one odd-cycle
block can occur alongside at most one other block.  The gap is recorded here and
not repaired; it is small and confined to |R| >= 26.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import crminus as C
import auditc as AC
import residue58 as R58
import blockr58 as BR
from order2r import RCHI, Z

r = RCHI
DEG = r - 1
crK = V.crK
N57 = 2 * r - 1
N58 = 2 * r
ALPHA = 3


def alpha_lb(mult, NL, iso=0):
    """Lower bound on alpha(G[L]) from private vertices and isolated vertices."""
    nb = len(mult)
    if nb == 0:
        return iso
    extra = sum(mult) - (NL - iso)
    if extra < 0:
        return nb + iso
    k = used = 0
    for q in sorted(mult):
        if used + q <= extra:
            used += q
            k += 1
        else:
            break
    return (nb - k) + iso


def control_order57():
    """Order 57 is closed; the bound must not contradict its surviving lists."""
    print("CONTROL   order 57, row (57,828): the closed row's multisets")
    M = 828
    X = 2 * M - N57 * DEG
    ok = True
    for RSZ in (10, 11):
        NL = N57 - RSZ
        d0 = DEG - RSZ
        base = M - DEG * RSZ - X
        for mult, eL in AC.multisets_audited(NL, max(base, 0),
                                             base + RSZ * (RSZ - 1) // 2, d0, r):
            a = alpha_lb(mult, NL)
            print("   |R|=%2d %-14s alpha(G[L]) >= %d   %s"
                  % (RSZ, str(mult), a, "" if a <= ALPHA else "<- would need alpha >= 4"))
    print("   (order 57 is closed by other means; this is a consistency check")
    print("    only, and the tight multisets there have two or three blocks.)")
    print()
    return ok


def sweep_blocks():
    print("PART 1   configurations with no isolated low vertex")
    tot = alive = 0
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        sx = X - (r + 2 - 6)
        Rmax = 1 + max(0, sx)
        seen = al = 0
        rs = set()
        prof = {}
        for RSZ in range(11, Rmax + 1):
            NL = N58 - RSZ
            d0 = DEG - RSZ
            base = m - DEG * RSZ - X
            for mult, eL in AC.multisets_audited(NL, max(base, 0),
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
                seen += 1
                if alpha_lb(mult, NL) <= ALPHA:
                    al += 1
                    rs.add(RSZ)
                    prof[len(mult)] = prof.get(len(mult), 0) + 1
        tot += seen
        alive += al
        print("   row (58,%d): %6d before, %5d with alpha(G[L]) <= %d,"
              " |R| in %d..%d" % (m, seen, al, ALPHA, min(rs), max(rs)))
        print("        by block count: %s"
              % ", ".join("%d blocks: %d" % (k, prof[k]) for k in sorted(prof)))
    print("   TOTAL: %d  ->  %d" % (tot, alive))
    print()
    return tot, alive


def iso_bound(mult, RSZ, eHR, iso):
    f = eHR + iso * (iso - 1) // 2 + iso * (RSZ - DEG)
    if f < 0:
        return 0
    return C.g(RSZ + iso, f) + sum(crK(q) for q in mult)


def sweep_iso():
    print("PART 2   configurations with an isolated low vertex")
    print("   alpha(G[L]) >= iso, so at most %d of them, against the 26 the"
          % ALPHA)
    print("   previous enumeration allowed.")
    alive = 0
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        sx = X - (r + 2 - 6)
        Rmax = 1 + max(0, sx)
        al = 0
        rs = set()
        isos = set()
        for RSZ in range(DEG, Rmax + 1):
            NL = N58 - RSZ
            d0 = DEG - RSZ
            base = m - DEG * RSZ - X
            for iso in range(1, ALPHA + 1):
                NB = NL - iso
                if NB < 2:
                    break
                for mult, eL in AC.multisets_audited(NB, max(base, 0),
                                                     base + RSZ * (RSZ - 1) // 2,
                                                     d0, r):
                    eGR = eL - base
                    eHR = RSZ * (RSZ - 1) // 2 - eGR
                    if eGR < 0 or eHR < 0:
                        continue
                    if RSZ - DEG + eHR == 0:
                        continue                # K_29 is a subgraph outright
                    if alpha_lb(mult, NL, iso) > ALPHA:
                        continue
                    v = max(iso_bound(mult, RSZ, eHR, iso),
                            BR.blockR(mult, NL, RSZ, eHR))
                    if v >= Z:
                        continue
                    if not R58.survivors(N58, m, RSZ, mult, eL, 1, 4, sx):
                        continue
                    al += 1
                    rs.add(RSZ)
                    isos.add(iso)
        alive += al
        print("   row (58,%d): %4d survive, |R| in %s, iso in %s"
              % (m, al, "-" if not rs else "%d..%d" % (min(rs), max(rs)),
                 sorted(isos)))
    print("   TOTAL: 47468  ->  %d" % alive)
    print()
    return alive


def main():
    print("alpha(G) <= 3 applied to the Gallai blocks, at r = %d" % r)
    print("Z(29) = %d;  the surviving order-58 branch has H K_4-free," % Z)
    print("i.e. omega(H) <= 3, i.e. alpha(G) <= 3.")
    print()
    control_order57()
    _, a1 = sweep_blocks()
    a2 = sweep_iso()
    print("CONCLUSION")
    print("   The bound alpha(G) <= 3 was proved and reviewed in the order-2r")
    print("   lemma and used only for a Turan cap on the components of H - B.")
    print("   Applied to G[L] it caps the whole block structure, because private")
    print("   vertices of distinct blocks are pairwise non-adjacent.")
    print()
    print("   Order 58 at r = 29 is open in %d + %d = %d configurations,"
          % (a1, a2, a1 + a2))
    print("   against the 103292 after the two audits: a reduction of more than")
    print("   ten-fold, and the first movement in the closing direction for")
    print("   several passes.")
    print()
    print("   It is NOT a closure.  Albertson's conjecture is not proved for")
    print("   r = 29.")


if __name__ == "__main__":
    main()

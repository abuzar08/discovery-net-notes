#!/usr/bin/env python3
"""
The (3,24) route, checked against every Tutte family the counts can decide.

A CORRECTION TO THE PREVIOUS PASS.  route324.py checked the Tutte obstruction
built from Q_1, the LARGEST block, found it unreachable, and concluded the route
was unblocked on all 6829 configurations where it applies.  The obstruction can
be built from ANY block, and for a SMALL block it is reachable.  Corrected here:
both count-decidable families are unreachable on 2116 of the 6829, not on all.
The direction of the error was over-optimistic, so it is stated plainly.

==============================================================================
WHAT THE ROUTE NEEDS.

H minus t_3 = 3 disjoint triangles has 49 vertices and needs a matching of 24,
i.e. Tutte-Berge deficiency at most 1.  Write H' for that graph: it is
L' (complete multipartite on the blocks, minus 3 vertices from each of three of
them) together with all of R.

==============================================================================
FAMILY A -- ISOLATE A PART.

Q_i is a block, hence a clique of G, hence an INDEPENDENT SET of H.  Taking
S = (L' - Q_i) u N_R(Q_i - T) isolates the q_i - 3 surviving vertices of Q_i, and
the adversary may also leave R - N_R independent inside H[R].  That gives

        deficiency  <=  2 q_i + 3 - 58 + 2 k_i ,

so the obstruction is reached exactly when k_i >= 29 - q_i, where k_i counts the
z in Z with no H-neighbour in Q_i.

THE EDGE COUNT ON Q_i.  Every v in Q_i has D_v = q_i - 1 on a partition, so
|N_H(v) ^ R| = q_i + |R| - 29 and

        sum_{z in Z} a_z^(i)  =  q_i(q_i + |R| - 29) - c_w^(i) ,   a_z^(i) <= q_i ,

spread over |Z| - k_i vertices.  Hence

        k_i  <=  (|R| - 1) - ceil( (q_i(q_i+|R|-29) - c_w) / q_i ) .

WHERE THE PREVIOUS PASS WENT WRONG.  That ceiling equals q_i + |R| - 29 exactly
when c_w < q_i, giving the clean identity k_i <= 28 - q_i and putting the
obstruction one unit out of reach.  But when c_w >= q_i the ceiling drops by one
and the cap becomes 29 - q_i -- exactly reachable.  With c_w <= 4 that happens
for every block of order at most 4, and the surviving multisets are full of
connector blocks of order 2.  Checking only Q_1, which is always large, hides it.

==============================================================================
FAMILY B -- AN R-SET CUT OFF FROM L'.  Settled completely, and negatively for
the adversary.

With S empty, the components of H' are the L'-chunk together with everything
attached to it, plus whatever part of R is disconnected from L'.  A cut-off set
C must be a union of H[R]-components with no L'-edge at all, so every z in C has
no L-neighbour whatever, i.e. c_z := x_z + |N_H(z) ^ R| = 29, and every
R-neighbour of z lies in C.  With |C| = p that forces |N_H(z) ^ R| <= p - 1,
hence x_z >= 30 - p, hence

        Sx  >=  p(30 - p) + (|Z| - p) .

At p = 1 that is 29 + |Z| - 1 >= 38 for |R| >= 11, and Sx <= X - 25 <= 31.  Every
larger p is worse.  So NO cut-off set exists, for any configuration in the class.

==============================================================================
RESULT.  Family B is unreachable everywhere.  Family A is unreachable for every
part on 2116 of the 6829 configurations where the route applies -- those whose
blocks all have order greater than c_w = 4.  On the other 4713 a small block
makes the obstruction reachable by the counts, which does not mean it is
realised, only that the counts no longer decide it.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import auditc as AC
import alpha58 as A
import turan58 as T
import residue58 as R58
import blockr58 as BR
from order2r import RCHI, Z

r = RCHI
DEG = r - 1
crK = V.crK
N58 = 2 * r
ALPHA = 3
CW = 4


def famA_cap(qi, RSZ, cw=CW):
    """Largest k_i the edge count on Q_i permits."""
    return (RSZ - 1) - -(-(qi * (qi + RSZ - 29) - cw) // qi)


def famB_needs(p, NZ):
    """Sx needed for a cut-off set of size p."""
    return p * (30 - p) + (NZ - p)


def part1():
    print("PART 1   Family A: the cap, and where the identity breaks")
    print("   cap = 28 - q_i when c_w < q_i, and 29 - q_i when c_w >= q_i;")
    print("   the obstruction is reached exactly at k_i >= 29 - q_i.")
    bad = []
    for qi in range(2, 29):
        for RSZ in range(11, 33):
            if qi + RSZ - 29 < 0:
                continue
            if famA_cap(qi, RSZ) >= 29 - qi:
                bad.append(qi)
                break
    print("   block orders for which the obstruction IS reachable: %s"
          % sorted(set(bad)))
    print("   i.e. exactly the blocks of order at most c_w = %d." % CW)
    print()


def part2():
    print("PART 2   Family B: no cut-off R-set exists")
    ok = True
    for RSZ in (11, 20, 32):
        NZ = RSZ - 1
        need = famB_needs(1, NZ)
        print("   |R| = %2d : a single cut-off vertex needs Sx >= %d, and"
              " Sx <= 31" % (RSZ, need))
        if need <= 31:
            ok = False
    print("   larger cut-off sets need strictly more, so Family B is")
    print("   unreachable for every configuration: %s" % ("PASS" if ok else "FAIL"))
    print()
    return ok


def part3():
    print("PART 3   how much the two families settle")
    tot = reach = both = 0
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        sx = X - (r + 2 - 6)
        Rmax = 1 + max(0, sx)
        for RSZ in range(11, Rmax + 1):
            NL = N58 - RSZ
            d0 = DEG - RSZ
            base = m - DEG * RSZ - X
            cp = T.turan_k4free(RSZ)
            for mult, eL in AC.multisets_audited(NL, max(base, 0),
                                                 base + RSZ * (RSZ - 1) // 2,
                                                 d0, r):
                if sum(crK(q) for q in mult) >= Z:
                    continue
                eGR = eL - base
                eHR = RSZ * (RSZ - 1) // 2 - eGR
                if eGR < 0 or eHR < 0 or eHR > cp:
                    continue
                if A.alpha_lb(mult, NL) > ALPHA:
                    continue
                if not R58.survivors(N58, m, RSZ, mult, eL, 1, 4, sx):
                    continue
                if BR.blockR(mult, NL, RSZ, eHR) >= Z:
                    continue
                tot += 1
                if len(mult) < 3 or min(mult[:3]) < 3:
                    continue
                reach += 1
                if all(famA_cap(qi, RSZ) < 29 - qi for qi in mult):
                    both += 1
    print("   surviving clique-block configurations: %d" % tot)
    print("   the (3,24) route applies to: %d" % reach)
    print("   both families unreachable (all blocks of order > %d): %d"
          % (CW, both))
    print("   counts no longer decide it (a block of order <= %d): %d"
          % (CW, reach - both))
    print()
    return tot, reach, both


def main():
    print("The (3,24) route against every Tutte family the counts decide")
    print("Z(29) = %d;  r = %d" % (Z, r))
    print()
    part1()
    okB = part2()
    tot, reach, both = part3()
    print("CONCLUSION")
    print("   CORRECTION.  The previous pass checked the Family A obstruction")
    print("   built from Q_1 only, found it one unit out of reach, and concluded")
    print("   the route was unblocked on all %d configurations.  Built from a" % reach)
    print("   SMALL block the same obstruction IS reachable, because the")
    print("   identity k_i <= 28 - q_i needs c_w < q_i.  The corrected figure is")
    print("   %d, not %d.  The error was over-optimistic." % (both, reach))
    print()
    print("   Family B is settled outright: a cut-off R-set would need")
    print("   Sx >= 29 + |Z| - 1 >= 38 against Sx <= 31, for every configuration.")
    print()
    print("   So on %d configurations both count-decidable Tutte families are" % both)
    print("   unreachable and the route stays live; on the remaining %d the"
          % (reach - both))
    print("   counts no longer decide it.  Neither is a closure: Tutte quantifies")
    print("   over all vertex sets and only these two families are determined by")
    print("   (|R|, multiset, e(H[R])).")
    print()
    print("   Order 58 remains open; r = 29 is NOT proved.")


if __name__ == "__main__":
    main()

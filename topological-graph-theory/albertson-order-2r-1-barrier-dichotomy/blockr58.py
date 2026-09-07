#!/usr/bin/env python3
"""
A Gallai block and the high set are almost a complete graph: order 58 at r = 29.

STATE BEFORE THIS FILE.  Order 57 at r = 29 is closed; what remains is order 58
in one class, b = 6, c = (51,1), on rows m = 838, 839, 840.  Every crossing bound
used on it so far scores three cliques that are pairwise VERTEX-disjoint,

        cr(G)  >=  cr(K_{q_1+c_1}) + cr(K_{q_2+c_2}) + cr(K_{rest}) ,

where c_i counts the high vertices adjacent to all of Q_i.  That throws away the
edges BETWEEN a block and R, and those edges are the densest part of the graph.

==============================================================================
WHY Q u R IS NEARLY COMPLETE.

Every vertex of L is low, d_G(v) = 28 exactly, and its G-neighbours inside L are
the union of its blocks minus itself, D_v := sum_{blocks ni v}(|Q'| - 1).  So v
has 28 - D_v G-neighbours in R and

        |N_H(v) ^ R|  =  |R| - 28 + D_v .

For a block Q of order q whose vertices lie in no other block, D_v = q - 1 and
each vertex of Q has exactly q + |R| - 29 non-neighbours in R.  That number is
TINY in every surviving configuration -- 2 at (27,15) with |R| = 16 -- because
the block orders and |R| are pinned near 29 from below.  Hence

        e_H(Q, R)  =  q(q + |R| - 29)          (blocks partitioning L)

and in general, since two blocks meet in at most one vertex and Constraint C
pins which blocks can share at all (see fmiss),

        e_H(Q, R)  <=  q(q + |R| - 29) + pen(Q) ,

with pen(Q) usually 0 or 1 rather than the extra (q_1 - 1) of the first draft.

Q is a clique of G and R misses only e(H[R]) edges, so G[Q u R] is a complete
graph on q + |R| vertices minus at most

        f(Q)  :=  e(H[R]) + q(q + |R| - 29) + extra (q_1 - 1)

edges, and crminus.g(q + |R|, f(Q)) is a lower bound for cr(G[Q u R]).  The other
blocks are vertex-disjoint from Q u R, so their crossings are counted in neither
and

        cr(G)  >=  g(q + |R|, f(Q))  +  sum_{i : Q_i =/= Q} cr(K_{q_i}) ,

maximised over which block is merged with R.

==============================================================================
WHAT IT BUYS.  At (27,15) with |R| = 16 and e(H[R]) = 0 the second block gives
f = 30 on 31 vertices, so g(31,30) = 5417, and the disjoint K_27 adds 5546:
10963 against Z(29) = 8281.  The old three-clique bound gave 6550 there.  The
mechanism is strongest exactly where the old one was weakest, because a small
second block is what makes q_2 + |R| - 29 small.

It is NOT a closure.  It clears almost all of the small-|R| regime and almost
none of |R| >= 17, where e(H[R]) runs to 268 and swamps f.  Reported as it is.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import crminus as C
import mu58 as MU
import residue58 as R58
from order2r import RCHI, Z

r = RCHI
DEG = r - 1
crK = V.crK
N57 = 2 * r - 1
N58 = 2 * r


def fmiss(mult, i, NL, RSZ, eHR):
    """Upper bound on the edges missing from G[Q_i u R].

    The shared-vertex penalty.  For v in Q, D_v = (q-1) + sum over the OTHER
    blocks containing v of (q'-1), and two blocks of a graph meet in at most one
    vertex, so each other block contributes at most (q'-1) once.  The number of
    (vertex, extra-block) incidences in all of L is exactly
    extra := sum_i q_i - |L|.  Constraint C forces every block with q' - 1 < d_0
    to consist entirely of cut vertices, so those blocks alone already consume
    sum q' of the incidences; what is left can be spent on big-big sharing.

    Charging every incidence at the largest block order, as the first version of
    this file did, over-penalises badly: at (24,23,2) with |R| = 11 it charges
    2 x 23 = 46 where the true maximum is 1."""
    q = mult[i]
    d0 = DEG - RSZ
    extra = sum(mult) - NL
    small = [mult[j] for j in range(len(mult)) if j != i and mult[j] - 1 < d0]
    big = sorted((mult[j] for j in range(len(mult))
                  if j != i and mult[j] - 1 >= d0), reverse=True)
    slots_big = max(0, extra - sum(q2 for q2 in mult if q2 - 1 < d0))
    pen = sum(q2 - 1 for q2 in small)
    for q2 in big[:slots_big]:
        pen += q2 - 1
    return eHR + q * (q + RSZ - 29) + pen


def blockR(mult, NL, RSZ, eHR):
    """Best bound over the choice of which block is merged with R."""
    best = 0
    for i, q in enumerate(mult):
        f = fmiss(mult, i, NL, RSZ, eHR)
        if f < 0:
            continue
        v = C.g(q + RSZ, f) + sum(crK(mult[j])
                                  for j in range(len(mult)) if j != i)
        if v > best:
            best = v
    return best


def control_order57():
    """The bound must never exceed Z(58-vertex) style upper bounds, and it must
    agree with the closed order-57 verdict rather than contradict it."""
    print("CONTROL   order 57, row (57,828): the bound on the already-closed row")
    M = 828
    X = 2 * M - N57 * DEG
    ok = True
    for RSZ in (10, 11):
        NL = N57 - RSZ
        d0 = DEG - RSZ
        base = M - DEG * RSZ - X
        for mult, eL in MU.multisets(NL, max(base, 0),
                                     base + RSZ * (RSZ - 1) // 2, d0, r):
            eGR = eL - base
            eHR = RSZ * (RSZ - 1) // 2 - eGR
            v = blockR(mult, NL, RSZ, eHR)
            # soundness: the bound may not exceed Z(q+|R|) for the merged piece
            for i, q in enumerate(mult):
                f = fmiss(mult, i, NL, RSZ, eHR)
                if f >= 0 and C.g(q + RSZ, f) > V.Z(q + RSZ):
                    ok = False
            print("   |R|=%2d %-14s e(H[R])=%2d  block+R bound %6d   %s"
                  % (RSZ, str(mult), eHR, v, "kills" if v >= Z else "-"))
    print("   soundness (every merged bound <= Z of its own order): %s"
          % ("PASS" if ok else "FAIL"))
    return ok


def order58():
    print("ORDER 58, class b = 6, c = (51,1)")
    print("   Applied to the configurations that survive residue58.py.")
    total = kills = 0
    left = []
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        sx = X - (r + 2 - 6)
        Rmax = 1 + max(0, sx)
        seen = k = 0
        lo = hi = 0
        rs = set()
        for RSZ in range(11, Rmax + 1):
            NL = N58 - RSZ
            d0 = DEG - RSZ
            base = m - DEG * RSZ - X
            for mult, eL in MU.multisets(NL, max(base, 0),
                                         base + RSZ * (RSZ - 1) // 2, d0, r):
                if sum(crK(q) for q in mult) >= Z:
                    continue
                if not R58.survivors(N58, m, RSZ, mult, eL, 1, 4, sx):
                    continue
                seen += 1
                eGR = eL - base
                eHR = RSZ * (RSZ - 1) // 2 - eGR
                if blockR(mult, NL, RSZ, eHR) >= Z:
                    k += 1
                else:
                    rs.add(RSZ)
                    if RSZ <= 16:
                        lo += 1
                        left.append((m, RSZ, mult, eHR,
                                     blockR(mult, NL, RSZ, eHR)))
                    else:
                        hi += 1
        total += seen
        kills += k
        print("   m = %d : %d survivors of residue58; block+R kills %d,"
              " %d remain (|R| <= 16: %d, |R| >= 17: %d), |R| in %s"
              % (m, seen, k, seen - k, lo, hi,
                 "-" if not rs else "%d..%d" % (min(rs), max(rs))))
    print()
    print("   THE SMALL-|R| REGIME is now %d configurations:" % len(left))
    for (m, RSZ, mult, eHR, v) in left:
        print("      m=%d |R|=%2d %-16s e(H[R])=%d  bound %6d, short %d"
              % (m, RSZ, str(mult), eHR, v, Z - v))
    return total, kills, left


def main():
    print("A Gallai block and the high set are almost complete, at r = %d" % r)
    print("Z(29) = %d;  low means d_G = %d" % (Z, DEG))
    print()
    ok = control_order57()
    print()
    total, kills, left = order58()
    print()
    print("CONCLUSION")
    if not ok:
        print("   A soundness control failed; nothing is claimed.")
        return
    print("   Merging one Gallai block with the whole high set, and scoring the")
    print("   result as a near-complete graph, is strictly stronger than the")
    print("   three-clique split wherever the second block is small.  It kills")
    print("   %d of the %d configurations that survive the residue." % (kills, total))
    print("   The small-|R| regime falls from 20 configurations to %d."
          % len(left))
    print("   It does NOT close order 58: the |R| >= 17 regime is untouched,")
    print("   because there e(H[R]) reaches 268 and dominates f(Q).  Order 58")
    print("   at r = 29 remains open, and r = 29 is not proved.")


if __name__ == "__main__":
    main()

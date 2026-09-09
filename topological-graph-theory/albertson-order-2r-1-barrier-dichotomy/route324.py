#!/usr/bin/env python3
"""
The route the branch hypothesis never imposed is LIVE, by exactly one unit.

WHY THIS EXISTS.  routes58.py showed that theta(H) <= 28 follows from any of
SEVENTY (t_3, t_2) packing families, and that the branch hypothesis (TT) excludes
only the first, (2,26).  The natural next one is (3,24) -- three disjoint
triangles plus a matching of 24 -- and it is available on 6829 of the surviving
configurations, because three or more Gallai blocks put a complete multipartite
graph inside H[L].

The obvious worry is that the (3,24) route hits the same wall as everything else.
It does not.  The natural obstruction to it is provably UNREACHABLE, and by
exactly one unit.

==============================================================================
WHAT THE (t_3, t_2) FAMILY NEEDS.

H minus t_3 disjoint triangles has 58 - 3 t_3 vertices and needs a matching of
t_2 = 30 - 2 t_3.  A matching of size t_2 exists iff the Tutte-Berge deficiency
is at most (58 - 3 t_3) - 2 t_2 = t_3 - 2.

==============================================================================
THE NATURAL OBSTRUCTION, AND WHY IT IS NEVER AVAILABLE.

Q_1 is a block, hence a clique of G, hence an INDEPENDENT SET of H.  So the
obvious Tutte set is S = (L' - Q_1) u N_R(Q_1 - T): removing it isolates the
q_1 - t_3 surviving vertices of Q_1, and the adversary may additionally leave
R - N_R independent inside H[R], contributing |R| - |N_R| further odd components.
With |L'| = |L| - 3 t_3 that gives

    deficiency  >=  2(q_1 - t_3) - |L'| + o_R - |N_R|
                 =  2 q_1 + t_3 - |L| + o_R - |N_R| ,

and with o_R <= k_1 and |N_R| >= |R| - k_1, where k_1 counts the z in Z having
no H-neighbour in Q_1,

    deficiency  <=  2 q_1 + t_3 - 58 + 2 k_1 .

For this to block the route it must reach t_3 - 1, i.e.

    2 k_1  >=  57 - 2 q_1 ,      that is     k_1  >=  29 - q_1 .

BUT THE EDGE COUNT FORBIDS EXACTLY THAT.  On a partition every v in Q_1 has
D_v = q_1 - 1, so |N_H(v) ^ R| = q_1 + |R| - 29 and

    sum_{z in Z} a_z  =  q_1(q_1 + |R| - 29) - c_w ,     a_z <= q_1 ,

spread over |Z| - k_1 = |R| - 1 - k_1 vertices.  Hence

    (|R| - 1 - k_1) q_1  >=  q_1(q_1 + |R| - 29) - c_w ,

which gives k_1 <= 28 - q_1 for every c_w in [0,4] and every |R| -- an identity,
checked below, independent of |R| and of c_w.

So the obstruction needs k_1 >= 29 - q_1 and the count permits at most
k_1 = 28 - q_1.  IT IS SHORT BY EXACTLY ONE, ALWAYS.

==============================================================================
WHAT THIS DOES AND DOES NOT SHOW.

It shows the (3,24) route is not blocked by the obstruction its own structure
suggests, on every configuration where three disjoint triangles sit inside L.
That is 6829 of the 8623 survivors.

It does NOT show nu(H - T_1 - T_2 - T_3) >= 24.  Tutte's condition quantifies
over ALL vertex sets, and this rules out one family of them -- the family built
from the block structure, which is the only one the parameters determine.  The
remaining sets depend on the placement of the L-R and R-R edges of H, which the
enumeration in this directory does not pin down.

That is the precise open question, and it is the first one in this lane that is
a question about H as a graph rather than about (|R|, multiset, e(H[R])).

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


def k1_cap(q1, RSZ, cw):
    """Largest k_1 the edge count permits: (|R|-1-k_1) q_1 >= e_1 - c_w."""
    e1 = q1 * (q1 + RSZ - 29)
    return (RSZ - 1) - -(-(e1 - cw) // q1)


def identity_check():
    print("PART 1   k_1 <= 28 - q_1 is an identity")
    ok = True
    for q1 in range(10, 29):
        for RSZ in range(11, 33):
            if q1 + RSZ - 29 < 0:
                continue
            for cw in range(0, 5):
                if k1_cap(q1, RSZ, cw) != 28 - q1:
                    ok = False
    print("   checked q_1 in [10,28], |R| in [11,32], c_w in [0,4]: %s"
          % ("the cap is 28 - q_1 in every case" if ok else "FAILS"))
    print("   the obstruction needs k_1 >= 29 - q_1, so it is short by ONE.")
    print()
    return ok


def main():
    print("Is the (3,24) route blocked?  Albertson r = %d, order 58" % r)
    print("Z(29) = %d" % Z)
    print()
    ok = identity_check()

    print("PART 2   where the route applies, and whether the obstruction bites")
    tot = reach = blocked = 0
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
                bad = R58.survivors(N58, m, RSZ, mult, eL, 1, 4, sx)
                if not bad:
                    continue
                if BR.blockR(mult, NL, RSZ, eHR) >= Z:
                    continue
                tot += 1
                if len(mult) < 3 or min(mult[:3]) < 3:
                    continue           # need three disjoint triangles inside L
                reach += 1
                q1 = mult[0]
                if max(b[0] for b in bad) >= 29 - q1:
                    blocked += 1
    print("   surviving clique-block configurations: %d" % tot)
    print("   with three blocks of order >= 3, so three disjoint triangles sit")
    print("   inside L and the (3,24) route applies: %d" % reach)
    print("   of those, the obstruction is REACHABLE (route blocked): %d" % blocked)
    print()
    print("CONCLUSION")
    if not ok:
        print("   The identity check failed; nothing is claimed.")
        return
    print("   The obstruction to the (3,24) route needs k_1 >= 29 - q_1, and the")
    print("   edge count on Q_1 permits at most k_1 = 28 - q_1.  Short by one,")
    print("   always, so the route is NOT blocked on any of the %d" % reach)
    print("   configurations where it applies -- %d%% of what remains."
          % ((100 * reach) // tot))
    print()
    print("   This is NOT a closure.  Tutte's condition quantifies over all")
    print("   vertex sets; this rules out the family the block structure")
    print("   determines, and the rest depend on where H puts its L-R and R-R")
    print("   edges, which the enumeration here does not pin down.  Deciding")
    print("   nu(H - T_1 - T_2 - T_3) >= 24 is the precise open question, and it")
    print("   is a question about H as a graph.")
    print()
    print("   Order 58 remains open; r = 29 is NOT proved.")


if __name__ == "__main__":
    main()

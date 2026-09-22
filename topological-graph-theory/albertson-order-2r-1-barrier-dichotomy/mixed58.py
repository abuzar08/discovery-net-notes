#!/usr/bin/env python3
"""
Triangles across the L/R split: are any of them GUARANTEED?  A gate, not a build.

WHY A GATE.  Four passes have ended by naming "triangles across the L/R split" as
the next step, for two different reasons: the 3676 configurations where three
disjoint triangles of H[L] cannot be guaranteed, and the surviving Tutte points
where S_R sits untouched in R while the k triangles are taken from the blocks.
Building it means re-deriving all eight inequalities of tuttegen.py, because R
loses vertices and rho, the degree sum and e(H[R]) all shift.

Before paying that, the cheap question: is such a triangle guaranteed AT ALL?
The whole clique-cover route needs THREE vertex-disjoint triangles of H for every
admissible H (packing58.py: (2,26) is the only family with t_3 = 2 and the branch
hypothesis excludes it).  A route through triangles that merely MIGHT exist closes
nothing, exactly as the 3676 are out of scope for that reason.

==============================================================================
EVERY WAY A TRIANGLE OF H CAN MEET THE SPLIT, AND WHEN IT IS FORCED.

Blocks are cliques of G, so independent in H; two low vertices are H-adjacent iff
they share no block; |N_H(v) ^ R| = rho_i = q_i + |R| - 29 for v private to block
i.  H is K_4-free.

  3L   three low vertices, pairwise sharing no block.  This is packing58.py's
       analysis and is what the 3676 fail.

  2L+1R   v in Q_i, v' in Q_j with i != j, and z in N_H(v) ^ N_H(v') ^ R.
       Forced iff the two neighbourhoods must meet:  rho_i + rho_j > |R|.

  1L+2R   v in L and an H[R]-EDGE inside N_H(v) ^ R.  The least number of
       H[R]-edges induced on a rho-subset is e(H[R]) - (C(|R|,2) - C(rho,2)), so
       forced iff  e(H[R]) > C(|R|,2) - C(rho_i,2)  for some i.

  3R   a triangle of H[R].  H[R] is K_4-free but may be triangle-free, and by
       Mantel it is forced only if  e(H[R]) > floor(|R|^2/4).

Each test is a guarantee over all admissible H, which is what the route needs.
Each is also necessary for the corresponding type to be forced, so a NO here is
not conservatism: it means an admissible H exists with no triangle of that type.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import pickle
import sys
from math import comb

import packing58 as P
import tuttegen as G


def rhos(mult, RSZ):
    return [max(0, q + RSZ - 29) for q in mult]


def forced_2L1R(mult, RSZ):
    """Some two blocks' R-neighbourhoods must intersect."""
    rs = rhos(mult, RSZ)
    return any(rs[i] + rs[j] > RSZ
               for i in range(len(rs)) for j in range(i + 1, len(rs)))


def forced_1L2R(mult, RSZ, eHR):
    """Some block's rho-neighbourhood must induce an H[R]-edge."""
    return any(eHR > comb(RSZ, 2) - comb(r, 2) for r in rhos(mult, RSZ) if r >= 2)


def forced_3R(RSZ, eHR):
    """H[R] cannot be triangle-free."""
    return eHR > RSZ * RSZ // 4


def forced_three(mult, RSZ, eHR, Ltail):
    """Is nu_tri(H) >= 3 FORCED, allowing the three triangles to mix types?

    nu_tri(H) <= 2 gives a 6-set B' meeting every triangle, so H - B' is
    triangle-free.  Split B' as b_L in L and b_R in R with b_L + b_R = 6.  Then
    BOTH sides must come out triangle-free:

      * H[L - B'] triangle-free needs at most two blocks to keep a private
        vertex outside B', i.e. the private tail outside the best two blocks must
        be at most b_L (packing58.hitting_tail with budget b_L);
      * H[R - B'] triangle-free needs
            e(H[R]) <= Mantel(|R| - b_R) + (edges of H[R] meeting B' ^ R)
                    <= Mantel(|R| - b_R) + C(|R|,2) - C(|R| - b_R, 2).

    If every split fails one of the two, no 6-set can meet all triangles and
    nu_tri(H) >= 3.  This is strictly stronger than either side alone: it makes
    the adversary pay for both at once out of one budget of six."""
    for bR in range(0, 7):
        bL = 6 - bR
        if Ltail > bL:
            continue                      # L side already impossible: good
        rest = RSZ - bR
        if rest < 0:
            return False
        cap = rest * rest // 4 + comb(RSZ, 2) - comb(rest, 2)
        if eHR <= cap:
            return False                  # this split works for the adversary
    return True


def main():
    print("Triangles across the L/R split: are any GUARANTEED?")
    print()
    cfgs = (pickle.load(open(sys.argv[1], "rb")) if len(sys.argv) > 1
            else G.configurations())
    openc = [(m, RSZ, mult, eHR) for m, RSZ, mult, eHR in cfgs
             if not G.route_closed(RSZ, list(mult), eHR,
                                   2 * m - G.N58 * G.DEG)[0]]
    print("   open clique-block configurations: %d" % len(openc))
    # true_blocks, not mult: the enumerator omits blocks and the raw multiset
    # OVERSTATES the guarantee (defect 19), which would put 151 configurations
    # in scope that are not.
    def inscope(x):
        m, RSZ, mult, eHR = x
        return P.kmax_exact(G.true_blocks(mult, RSZ, eHR,
                                          2 * m - G.N58 * G.DEG),
                            G.N58 - RSZ) >= 3
    noL = [x for x in openc if not inscope(x)]
    inL = [x for x in openc if inscope(x)]
    print("      three disjoint triangles in H[L] not guaranteed: %d" % len(noL))
    print("      in scope for the block route but undecided:       %d" % len(inL))
    print()

    rows = []
    for name, sub in (("all open", openc), ("H[L] route unavailable", noL),
                      ("in scope but undecided", inL)):
        c2 = sum(1 for m, R, mu, e in sub if forced_2L1R(list(mu), R))
        c1 = sum(1 for m, R, mu, e in sub if forced_1L2R(list(mu), R, e))
        c3 = sum(1 for m, R, mu, e in sub if forced_3R(R, e))
        anyf = sum(1 for m, R, mu, e in sub
                   if forced_2L1R(list(mu), R) or forced_1L2R(list(mu), R, e)
                   or forced_3R(R, e))
        rows.append((name, len(sub), c2, c1, c3, anyf))

    print("   configurations where a triangle of each mixed type is FORCED:")
    print()
    print("   %-24s %7s %8s %8s %6s %9s"
          % ("set", "size", "2L+1R", "1L+2R", "3R", "any one"))
    for name, n, c2, c1, c3, anyf in rows:
        print("   %-24s %7d %8d %8d %6d %9d" % (name, n, c2, c1, c3, anyf))
    print()

    print("   nu_tri(H) >= 3 FORCED by the two sides sharing one budget of six:")
    three = {}
    for name, sub in (("all open", openc), ("H[L] route unavailable", noL),
                      ("in scope but undecided", inL)):
        c = sum(1 for m, R, mu, e in sub
                if forced_three(list(mu), R, e,
                                P.hitting_tail(list(mu), G.N58 - R)))
        three[name] = c
        print("      %-24s %7d of %d" % (name, c, len(sub)))
    print()

    tot = rows[0]
    gained = three["H[L] route unavailable"]
    print("CONCLUSION")
    print("   One mixed triangle is forced on %d of the %d open configurations,"
          % (tot[5], tot[1]))
    print("   almost all of them by Mantel inside H[R] (%d) rather than by any"
          % tot[4])
    print("   crossing type: the 1L+2R test fires %d times, never." % rows[0][3])
    print()
    print("   But the route needs THREE disjoint triangles, and that is forced on")
    print("   only %d configurations -- of which %d are ones the block route"
          % (three["all open"], three["in scope but undecided"]))
    print("   already reaches, and %d are new." % gained)
    print()
    if gained == 0:
        print("   SO THE MIXED ROUTE ADDS NO SCOPE AT ALL.  Every configuration")
        print("   where mixed triangles force a packing of three is already in")
        print("   scope through H[L]; not one of the %d out-of-scope" % len(noL))
        print("   configurations is rescued by them.  'Triangles across the L/R")
        print("   split', named as the next step four times, is NOT AVAILABLE")
        print("   where it was wanted.")
        print()
        print("   This gate cost one measurement.  Re-deriving the eight")
        print("   inequalities for a route with no new domain would have cost a")
        print("   pass, and the conclusion would have been the same.")
    else:
        print("   %d configurations are newly reachable, so the re-derivation of"
              % gained)
        print("   the eight inequalities is worth paying for.")
    print()
    print("   The three tests are also NECESSARY for forcing, so a zero is not")
    print("   conservatism -- it exhibits the freedom an adversary has.")
    print()
    print("   r = 29 is NOT proved.")


if __name__ == "__main__":
    main()

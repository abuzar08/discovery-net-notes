#!/usr/bin/env python3
"""
The absorption route at order 58 is exhausted: a component-by-component check.

WHY.  The shortfall map (profile58.py) showed that the near obstruction at order
58 is the absorption inequality, not the crossing bound: 3182 of the 8623
surviving configurations are ONE unit short of

        mu_1 + mu_2  >=  |Z| + max(0, t - s) ,       mu_1 >= t .

One unit is all that is needed anywhere.  This file asks, for each of the four
places a unit could come from, whether anything is left, and answers no.

==============================================================================
THE FOUR COMPONENTS, AND WHERE EACH STANDS.

(1) THE EDGE TOTAL FOR mu_1.  e_H(Q_1,R) = q_1(|R| - 28) + sum_{v in Q_1} D_v,
    and on a partition D_v = q_1 - 1 for every v in Q_1, so

        e_H(Q_1, R)  =  q_1(q_1 + |R| - 29)     EXACTLY.

    Nothing is recoverable: the bound already is the value.

(2) THE SECOND SIDE FOR mu_2.  Widened in the previous pass from Q_2 - Q_1 to
    all of L - Q_1, which is what the absorption actually permits, with

        e_H(L - Q_1, R) = (|L| - q_1)(|R| - 28) + sum_{i>=2} q_i(q_i - 1)

    again exact on a partition.  mu_2 strictly improved for 641 of the 1843
    partition multisets among the survivors and closed NONE of them.  The side is
    now as wide as the argument permits.

(3) THE SINGLETON COUNT s.  Measured out two passes ago: making the Hall
    condition explicit -- a colour class of G[L - Q_1] is forbidden only from
    those cut vertices of Q_1 whose block it meets, hence from at most
    min(extra, k-1) of them -- changes nothing at all, because among the
    survivors either extra = 0, so nothing was being paid, or the condition
    fails anyway.

(4) THE STEP FROM mu_1, mu_2 TO THE TRIANGLES.  This is the one thing that had
    never been examined, and it is what this file computes.

==============================================================================
COMPONENT (4): THE INCLUSION-EXCLUSION STEP IS NOT THE BOTTLENECK.

What the argument needs is t vertex-disjoint triangles {z, u, v} of H with
z in Z, u in Q_1, v in L - Q_1.  Since u and v lie in different blocks they are
automatically H-adjacent, so the condition is only that z be H-adjacent to both:
t vertices of Z simultaneously saturated by a matching into Q_1 and by one into
L - Q_1.  The chain bounds that by inclusion-exclusion,

        #{z saturated by both}  >=  mu_1 + mu_2 - |Z| ,

which is exactly the requirement above.  The sets matchable into Q_1 and into
L - Q_1 are transversal matroids on Z, so the truth is their matroid
intersection, and by Edmonds

        max  =  min_{A subset of Z} [ r_1(A) + r_2(Z - A) ] ,

which the inclusion-exclusion bound underestimates whenever the two deficiency
sets cannot sit on complementary parts.  Here they are coupled: on a partition

        a_z + b_z  =  |N_H(z) ^ L|  =  dh - c_z  EXACTLY,

so a vertex whose a_z is small has b_z large.  Concretely, if S_1 realises the
deficiency d_1 then every z in S_1 has a_z <= A := |S_1| - d_1, and likewise
b_z <= B on S_2, so every z in the overlap has c_z >= dh - A - B, and summing
against sum_z c_z <= budget caps the overlap:

        |S_1 ^ S_2| (dh - A - B)  <=  budget .

Maximising d_1 + d_2 = |S_1| + |S_2| - A - B under that cap and under the two
sum constraints is a small search, done below for every surviving partition
multiset and every (k_1, k_2) sub-case and every split of the w-deduction.

THE ANSWER: it closes ONE configuration out of 1843.  The cap does not bite,
because at the maximising A = B = 1 the sum constraints already force
|S_1| + |S_2| well below |Z| + budget/(dh - 2).  The inclusion-exclusion step was
never where the slack was.

==============================================================================
CONCLUSION.  All four components of the absorption inequality are at their
limit, so the 3182 configurations that are one unit short will not be closed by
sharpening it.  Order 58 needs a different argument.  Reported as a negative.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import auditc as AC
import alpha58 as A
import turan58 as T
import residue58 as R58
import blockr58 as BR
import dichot as D
from order2r import RCHI, Z

r = RCHI
DEG = r - 1
crK = V.crK
N58 = 2 * r
ALPHA = 3


def maxsig(NZ, cs, side, S):
    """Largest sigma with sigma*cs + (NZ - sigma)*side >= S."""
    b = -1
    for s in range(0, NZ + 1):
        if s * cs + (NZ - s) * side >= S:
            b = s
    return b


def joint_d(Za, Zb, NZ, q1, side2, Sa, Sb, budget, dh):
    """Largest feasible d_1 + d_2 under the residue coupling."""
    best = 0
    for Aa in range(1, q1 + 1):
        s1 = min(maxsig(Za, Aa, q1, Sa), Za)
        if s1 < Aa:
            continue
        for Bb in range(1, side2 + 1):
            s2 = min(maxsig(Zb, Bb, side2, Sb), Zb)
            if s2 < Bb:
                continue
            gap = dh - Aa - Bb
            cap = NZ if gap <= 0 else budget // gap
            tot = min(s1 + s2, NZ + cap) - Aa - Bb
            if tot > best:
                best = tot
    return best


def closes(nn, m, RSZ, mult, eL, sx):
    """True when every (k_1,k_2) and every w-split is killed by the joint test."""
    NL = nn - RSZ
    NZ = RSZ - 1
    X = 2 * m - nn * DEG
    base = m - DEG * RSZ - X
    eGR = eL - base
    eHR = RSZ * (RSZ - 1) // 2 - eGR
    q1 = mult[0]
    side2 = R58.second_side(NL, mult)
    nu = min(eHR, RSZ // 2)
    t = q1 + RSZ - 28 - nu
    if t <= 0:
        return True
    d0 = DEG - RSZ
    s = D.singletons(NL, mult, d0)
    need = max(0, t - s)
    e1 = q1 * (q1 + RSZ - 29)
    e2 = R58.second_edges(NL, mult, RSZ)
    budget = sx + 2 * eHR
    dh = nn - 1 - DEG
    thr1, thr2 = R58.thresholds(nn, NL, mult)
    for k1 in range(0, NZ + 1):
        for k2 in range(0, NZ + 1):
            if R58.residue(NZ, budget, thr1, thr2, k1, k2) is None:
                continue
            Za, Zb = NZ - k1, NZ - k2
            if Za < t:
                continue                       # already impossible
            for cw1 in range(0, 5):
                Sa = max(e1 - cw1, 0)
                Sb = max(e2 - (4 - cw1), 0)
                if joint_d(Za, Zb, NZ, q1, side2, Sa, Sb,
                           budget, dh) > NZ - k1 - k2 - need:
                    return False               # this split escapes
    return True


def main():
    print("Is the absorption route at order 58 exhausted?  r = %d" % r)
    print("Z(29) = %d" % Z)
    print()
    print("COMPONENTS (1)-(3) are settled in earlier files:")
    print("   (1) e_H(Q_1,R) = q_1(q_1 + |R| - 29) EXACTLY on a partition;")
    print("       the bound already is the value.")
    print("   (2) the second side is now all of L - Q_1, which is what the")
    print("       absorption permits; it improved mu_2 for 641 of 1843 and")
    print("       closed none.")
    print("   (3) the singleton count: the explicit Hall condition changes")
    print("       nothing, 8623 to 8623.")
    print()
    print("COMPONENT (4)   the inclusion-exclusion step, computed here")
    n_part = n_close = 0
    for m in (838, 839, 840):
        X = 2 * m - N58 * DEG
        sx = X - (r + 2 - 6)
        Rmax = 1 + max(0, sx)
        p = c = 0
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
                if sum(mult) != NL or len(mult) < 2:
                    continue                   # the coupling needs a partition
                p += 1
                if closes(N58, m, RSZ, mult, eL, sx):
                    c += 1
        n_part += p
        n_close += c
        print("   row (58,%d): %4d partition survivors, %d closed by the joint"
              " deficiency bound" % (m, p, c))
    print("   TOTAL: %d partition survivors, %d closed" % (n_part, n_close))
    print()
    print("CONCLUSION")
    print("   The matroid-intersection view of the absorption step, with the")
    print("   residue coupling the two deficiency sets, closes %d of %d."
          % (n_close, n_part))
    print("   The cap on the overlap does not bite: at the maximising A = B = 1")
    print("   the two sum constraints already hold |S_1| + |S_2| well below")
    print("   |Z| + budget/(dh - 2), so inclusion-exclusion was never where the")
    print("   slack was.")
    print()
    print("   All four components of the absorption inequality are therefore at")
    print("   their limit.  The 3182 configurations that are one unit short will")
    print("   NOT be closed by sharpening it, and order 58 needs a different")
    print("   argument.  r = 29 is not proved.")


if __name__ == "__main__":
    main()

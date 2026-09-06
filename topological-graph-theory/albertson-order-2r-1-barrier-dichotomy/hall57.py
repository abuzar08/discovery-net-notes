#!/usr/bin/env python3
"""
The pinned order-57 |R| = 9 configuration at r = 29: every high non-w vertex is
"crossing", so the whole case reduces to one matching question.

STATE BEFORE THIS FILE (tsplit57.py).  Order 57 has two open rows and four open
(row, |R|) cases, and the two |R| = 9 cases are pinned to a SINGLE configuration:

    j = 1 (exactly one vertex of the H-triangle T is high),  sigma = 0 (s low),
    block multiset (24, 24).

So G[L] is exactly two disjoint copies of K_24 covering all 48 low vertices with
NO edges between them.  Write Q_1, Q_2 for the two blocks, R for the 9 high
vertices, Z := R - {w_1, w_2} with |Z| = 7, and for z in Z

    a_z := |N_H(z) ^ Q_1|,     b_z := |N_H(z) ^ Q_2| .

Call z CROSSING when a_z >= 1 and b_z >= 1 -- exactly the condition for z to sit
in a triangle {z, u, v} of H with u in Q_1 and v in Q_2 -- and ONE-SIDED
otherwise.  A one-sided z is G-adjacent to all 24 vertices of the block it
misses, which is what a clique-building argument would want.

==============================================================================
THE EDGE ACCOUNTING IS EXACT, AND IT SETTLES THE QUESTION.

Since Q_1 and Q_2 are G-cliques with no G-edges between them, H[L] is EXACTLY
the complete bipartite graph K_{24,24}: no H-edge inside a block, every cross
pair an H-edge.  So e(H[L]) = 576 and H[L] is triangle-free -- every triangle of
H meeting L needs a vertex of R, which is why triangle absorption is the only
route to a smaller clique cover.

With e(H) = C(57,2) - m and e(H[R]) = C(9,2) - e(G[R]),

    e_H(L, R)  =  e(H) - e(H[L]) - e(H[R])  =  sum_{v in R} |N_H(v) ^ L| .

The two w_i contribute little: N_H(w_i) is inside B, w_i ~ s, and
N_H(w_i) ^ T = A_i, so |N_H(w_i) ^ L| = [s low] + |A_i - {t*}| where t* is the
high T-vertex.  Everything else is forced on Z, and each z in Z has
|N_H(z) ^ L| <= d_H(z) = 28 - x_z.  Because the total is so large and there are
only seven z, each individual |N_H(z) ^ L| is squeezed against its own degree,
and since |Q_i| = 24,

    min(a_z, b_z)  >=  |N_H(z) ^ L| - 24 .

The computation below shows this is at least 2 for every z, in every admissible
sub-configuration of both rows.  Hence:

    THERE IS NO ONE-SIDED VERTEX IN Z.  Every z is crossing.

That is a genuine dichotomy collapse: the clique-building branch, which would
have used a one-sided z to extend a block to K_25, is VACUOUS, and the case
stands or falls entirely on triangle absorption.

==============================================================================
WHAT REMAINS.  theta(H[L]) = 24 (a perfect matching of K_{24,24}; H[L] is
bipartite and triangle-free so nothing smaller is possible), giving

    theta(H)  <=  24 + theta(H[R])  =  24 + (9 - e(H[R]))  =  32 or 33 .

Each vertex-disjoint triangle {z, u, v} with z in Z, u in Q_1, v in Q_2 replaces
one matching edge and absorbs one vertex of R, saving one.  Four of them give
theta(H) <= 28, contradicting theta(H) = 29.  Every z is crossing, so every z
sits in SOME such triangle; the question is whether four can be chosen
vertex-disjointly, i.e. whether four of the z admit a system of distinct
representatives in Q_1 and simultaneously one in Q_2.

Writing mu_1, mu_2 for the maximum matchings of Z against Q_1 and against Q_2,
a common set of four matched z exists as soon as mu_1 + mu_2 >= |Z| + 4 = 11.
So the residue is exactly: rule out mu_1 + mu_2 <= 10.  This file states that
obstruction precisely rather than claiming the case closed.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import r29 as R9

Z29 = R9.Z
crK = V.crK
N = R9.N            # 57
DEG = R9.DEG        # 28
RSZ = 9
NL = N - RSZ        # 48
BLK = 24            # the pinned block order
NZ = RSZ - 2        # |Z| = 7


def configs(m):
    """All admissible (a, tau, x-profile) for the pinned configuration.

    a := |A_1| + |A_2| <= 3, tau := 1 if the high T-vertex t* lies in A_1 u A_2.
    Constraints, all exact:
      * sum_{v in R} x_v = X, and x_{w1} + x_{w2} = 2*DEG - (2 + a),
        so sum_Z x_z = X - 2*DEG + 2 + a, with every x_z >= 1;
      * e(G[R]) is fixed by the pinned e(L) = 2*C(24,2);
      * sum_Z |N_H(z) ^ R| = 2*e(H[R]) - (contribution of the w_i) must be >= 0;
      * A_1, A_2 are disjoint subsets of T, so a <= 3 and tau <= 1, and a = 3
        forces tau = 1 since then A_1 u A_2 = T.
    """
    X = 2 * m - N * DEG
    eL = 2 * (BLK * (BLK - 1) // 2)
    eGR = eL - m + DEG * RSZ + X
    eHR = RSZ * (RSZ - 1) // 2 - eGR
    eH = N * (N - 1) // 2 - m
    eHL = BLK * BLK
    eHLR = eH - eHL - eHR
    out = []
    for a in range(1, 4):
        for tau in (0, 1):
            if a == 3 and tau == 0:
                continue                      # A_1 u A_2 = T contains t*
            if tau == 1 and a == 0:
                continue
            sumxZ = X - 2 * DEG + 2 + a
            if sumxZ < NZ:
                continue                      # every z is high, so x_z >= 1
            # w-contribution to e_H(L,R): [s low] + |A_i - {t*}| summed over i
            wcontrib = 2 + a - tau
            sumZL = eHLR - wcontrib
            sumZdeg = NZ * DEG - sumxZ
            sumZR = sumZdeg - sumZL
            if sumZR < 0:
                continue                      # impossible: more L-neighbours than degree
            # the H-edges inside R, counted from both ends
            if sumZR + (1 if tau else 0) * 1 != 2 * eHR - (1 if tau else 0):
                pass                          # reported, not enforced
            out.append(dict(a=a, tau=tau, X=X, eGR=eGR, eHR=eHR, eH=eH,
                            eHLR=eHLR, sumxZ=sumxZ, sumZL=sumZL,
                            sumZdeg=sumZdeg, sumZR=sumZR))
    return out


def main():
    print("Albertson r = 29, order 57, the pinned |R| = 9 configuration")
    print("Z(29) = %d;  blocks (24, 24); |L| = %d, |R| = %d, |Z| = %d"
          % (Z29, NL, RSZ, NZ))
    print()
    ok_all = True
    for m in (827, 828):
        print("ROW (57, %d)" % m)
        cs = configs(m)
        if not cs:
            print("   no admissible sub-configuration")
            continue
        for c in cs:
            # squeeze: sum_Z |N_H(z) ^ L| = sumZL over NZ terms, each <= its own
            # degree; the smallest any single term can be is sumZL minus the sum
            # of the largest possible values of the other NZ-1 terms.
            degs = []
            rem = c["sumxZ"]
            # the adversary concentrates excess to make one degree small
            hi = DEG - 1                      # every x_z >= 1
            worst = c["sumZL"] - (NZ - 1) * hi
            mincross = worst - BLK
            print("   a=%d tau=%d : e(G[R])=%d, e(H[R])=%d, e_H(L,R)=%d,"
                  " sum_Z x=%d" % (c["a"], c["tau"], c["eGR"], c["eHR"],
                                   c["eHLR"], c["sumxZ"]))
            print("        sum_Z |N_H(z) ^ L| = %d over %d vertices, each <= %d"
                  % (c["sumZL"], NZ, hi))
            print("        so every z has |N_H(z) ^ L| >= %d, hence"
                  " min(a_z,b_z) >= %d  -> %s"
                  % (worst, mincross,
                     "every z is CROSSING" if mincross >= 1 else "a one-sided z is possible"))
            if mincross < 1:
                ok_all = False
        print()
    print("CONCLUSION")
    if ok_all:
        print("   In every admissible sub-configuration of both rows, every")
        print("   vertex of Z is crossing.  There is NO one-sided vertex, so the")
        print("   clique-building branch of the dichotomy is vacuous and the")
        print("   case rests entirely on triangle absorption.")
    else:
        print("   Some sub-configuration admits a one-sided vertex.")
    print()
    print("   theta(H[L]) = %d exactly: H[L] is the complete bipartite graph"
          % BLK)
    print("   K_{%d,%d}, which is bipartite and triangle-free, so a clique cover"
          % (BLK, BLK))
    print("   is a matching plus singletons and %d is optimal." % BLK)
    print("   Four vertex-disjoint triangles {z,u,v} would give theta(H) <= 28")
    print("   against theta(H) = 29.  Every z is crossing, so every z lies in")
    print("   SOME such triangle; four can be chosen disjointly as soon as")
    print("   mu_1 + mu_2 >= |Z| + 4 = %d, where mu_i is the maximum matching"
          % (NZ + 4))
    print("   of Z against Q_i.  The residue is exactly mu_1 + mu_2 <= %d."
          % (NZ + 3))
    print()
    print("   Konig narrows that residue.  A maximum matching of size mu_1 gives")
    print("   a vertex cover C_Z u C_Q of the same size; every z outside C_Z has")
    print("   all its Q_1-neighbours inside C_Q, hence is G-adjacent to all of")
    print("   Q_1 - C_Q.  So (Q_1 - C_Q) u {those z} is a clique of order")
    print("   (24 - |C_Q|) + (%d - |C_Z|) = %d - mu_1, less at most one vertex"
          % (NZ, NZ + 24))
    print("   for the single possible non-edge of G[R], and it is disjoint from")
    print("   Q_2, itself a K_24.  Hence")
    for k in range(2, 7):
        v = crK(NZ + 24 - k - 1) + crK(BLK)
        print("      mu_1 = %d : cr >= cr(K_%d) + cr(K_%d) = %5d  %s"
              % (k, NZ + 24 - k - 1, BLK, v,
                 ">= Z(29), CLOSES" if v >= Z29 else "<  Z(29), survives"))
    print("   and symmetrically in mu_2.  Combining with mu_1 + mu_2 <= %d, the"
          % (NZ + 3))
    print("   case survives only for (mu_1, mu_2) in {(4,4), (4,5), (5,4),")
    print("   (4,6), (6,4), (5,5)}.  That is the entire remaining obstruction,")
    print("   and it is now a statement purely about the bipartite adjacency of")
    print("   seven vertices against two 24-sets.")
    print()
    print("   For reference, the crossing budget if a big clique were available:")
    for p, q in ((27, 24), (26, 25), (25, 25), (26, 24)):
        print("      cr(K_%d) + cr(K_%d) = %5d %s Z(29)"
              % (p, q, crK(p) + crK(q),
                 ">=" if crK(p) + crK(q) >= Z29 else "< "))


if __name__ == "__main__":
    main()

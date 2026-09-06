#!/usr/bin/env python3
"""
The pinned order-57 |R| = 9 cases at r = 29 are IMPOSSIBLE.

Consequently row (57, 827) is eliminated outright and row (57, 828) reduces to
|R| in [10, 11].

STATE BEFORE THIS FILE.  tsplit57.py pins the two |R| = 9 cases to a single
configuration -- j = 1, sigma = 0, block multiset (24, 24) -- and hall57.py shows
that every z in Z := R - {w_1, w_2} is CROSSING, with min(a_z, b_z) >= 2, where
a_z := |N_H(z) ^ Q_1| and b_z := |N_H(z) ^ Q_2|.  What was left was to rule out
mu_1 + mu_2 <= 10, where mu_i is the maximum matching of Z against Q_i.

Two facts that were sitting unused close it.

==============================================================================
FACT 1 -- Z IS A CLIQUE OF G, so the block-plus-Z cliques lose nothing.

The block multiset is exactly (24, 24) with sum of orders 48 = |L|, so the two
blocks PARTITION L: no vertex lies in two blocks and there is no third block.

For m = 827 the pinned configuration has e(H[R]) = 1, and the accounting of
hall57.py gives sum_{z in Z} |N_H(z) ^ R| = 1: exactly one endpoint of that
single H-edge lies in Z.  So the edge runs between Z and {w_1, w_2} -- it is the
pair (t*, w_i) forced by tau = 1 -- and NO pair inside Z is an H-edge.  For
m = 828, e(H[R]) = 0 and R is a G-clique outright.  Either way

        Z is a clique of G.

Earlier bounds subtracted one vertex from every block-plus-Z clique to allow for
a possible non-edge.  That subtraction is unnecessary, and it is worth a whole
crossing step: a Koenig clique of order 31 - mu_1 rather than 30 - mu_1.

==============================================================================
FACT 2 -- EVERY LOW VERTEX HAS EXACTLY FOUR H-NEIGHBOURS IN R.

A low vertex has d_G = 28 exactly.  Since the blocks partition L and each has
order 24, v has exactly 23 G-neighbours inside L, hence 28 - 23 = 5 inside R,
hence |R| - 5 = 4 H-neighbours inside R.  Summing over a block,

        e_H(Q_i, R) = 24 * 4 = 96,

and the two together give 192, which matches e_H(L, R) exactly.  Subtracting the
small contribution of w_1, w_2 leaves

        sum_{z in Z} a_z  >=  96 - (w-contribution)  and likewise for b_z,
        sum_{z in Z} a_z  >=  92   in every admissible sub-configuration.

==============================================================================
THE CLOSURE.  By Koenig, mu_1 is the size of a minimum vertex cover C_Z u C_Q of
the bipartite graph of H-edges between Z and Q_1.  Every z outside C_Z has all
its Q_1-neighbours inside C_Q, so a_z <= |C_Q|, while a z inside C_Z has only the
trivial bound a_z <= 24.  Hence

        sum_z a_z  <=  24 |C_Z| + (7 - |C_Z|) |C_Q| .

Every z is crossing, so a_z >= 2, which forces |C_Q| >= 2 whenever some z lies
outside C_Z.  Maximising the right-hand side over the admissible splits of
mu_1 = k shows it stays below 92 for every k <= 5.  Therefore

        mu_1 >= 6,   and symmetrically   mu_2 >= 6,   so   mu_1 + mu_2 >= 12.

A maximum matching of Z against Q_1 saturates mu_1 vertices of Z and one against
Q_2 saturates mu_2, so at least mu_1 + mu_2 - 7 >= 5 vertices of Z are saturated
in both.  Take t of them: their Q_1-representatives are distinct, their
Q_2-representatives are distinct, and Q_1, Q_2, Z are pairwise disjoint, so we
get t vertex-disjoint triangles {z, u, v} of H.

Each triangle absorbs one vertex of R and two of L, and what remains of H[L] is
a complete bipartite graph K_{24-t, 24-t}, covered by 24 - t edges.  So

        theta(H)  <=  t + (24 - t) + theta(H[R minus those t])
                  =  24 + (9 - t) - (surviving H-edges inside R)
                  =  33 - t - e(H[R]) .

For m = 827 (e(H[R]) = 1) that is 32 - t, and t = 4 gives 28; five vertices are
available, so the four can be chosen to avoid t*, keeping the H-edge alive.  For
m = 828 (e(H[R]) = 0) it is 33 - t, and t = 5 gives 28.  Both contradict
theta(H) = 29.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import r29 as R9

Z29 = R9.Z
N = R9.N            # 57
DEG = R9.DEG        # 28
RSZ = 9
NL = N - RSZ        # 48
BLK = 24
NZ = RSZ - 2        # 7


def subcases(m):
    """The admissible (a, tau) for the pinned configuration, with the exact
    edge accounting."""
    X = 2 * m - N * DEG
    eL = 2 * (BLK * (BLK - 1) // 2)
    eGR = eL - m + DEG * RSZ + X
    eHR = RSZ * (RSZ - 1) // 2 - eGR
    eH = N * (N - 1) // 2 - m
    eHLR = eH - BLK * BLK - eHR
    out = []
    for a in range(1, 4):
        for tau in (0, 1):
            if a == 3 and tau == 0:
                continue
            sumxZ = X - 2 * DEG + 2 + a
            if sumxZ < NZ:
                continue
            wc = 2 + a - tau
            sumZL = eHLR - wc
            sumZR = (NZ * DEG - sumxZ) - sumZL
            if sumZR < 0:
                continue
            # the H-edges inside R, seen from Z, must match e(H[R]) and tau
            if sumZR != tau:
                continue
            out.append((a, tau, X, eGR, eHR, eHLR, sumZL, sumxZ))
    return out


def max_sum_a(k):
    """Largest possible sum_z a_z compatible with a vertex cover of size k,
    given that every a_z >= 2 (so |C_Q| >= 2 whenever some z is uncovered)."""
    best = -1
    for cz in range(0, min(k, NZ) + 1):
        cq = k - cz
        if cz < NZ and cq < 2:
            continue                       # an uncovered z would have a_z <= 1
        best = max(best, BLK * cz + (NZ - cz) * min(cq, BLK))
    return best


def main():
    print("Albertson r = 29, order 57: the pinned |R| = 9 cases are impossible")
    print("Z(29) = %d;  |L| = %d, blocks (24,24), |R| = %d, |Z| = %d"
          % (Z29, NL, RSZ, NZ))
    print()

    gL = BLK - 1
    gR = DEG - gL
    hR = RSZ - gR
    perQ = BLK * hR
    print("FACT 2   every low vertex has exactly %d H-neighbours in R" % hR)
    print("   The blocks partition L, so a low vertex has %d G-neighbours in L,"
          % gL)
    print("   hence %d in R, hence %d H-neighbours in R.  So e_H(Q_i,R) = %d."
          % (gR, hR, perQ))
    print()

    print("KOENIG BOUND   largest sum_z a_z admitted by a cover of size k")
    for k in range(2, 9):
        print("      k = %d :  sum_z a_z <= %3d" % (k, max_sum_a(k)))
    print()

    allclosed = True
    for m in (827, 828):
        print("ROW (57, %d)" % m)
        cs = subcases(m)
        if not cs:
            print("   no admissible sub-configuration")
            continue
        for (a, tau, X, eGR, eHR, eHLR, sumZL, sumxZ) in cs:
            need = sumZL - perQ                    # sum_z a_z >= need
            kmin = min(k for k in range(2, 9) if max_sum_a(k) >= need)
            tmin = 33 - eHR - 28                   # smallest t with theta <= 28
            avail = 2 * kmin - NZ                  # z saturated on both sides
            ok = avail >= tmin
            print("   a=%d tau=%d : e(H[R])=%d, sum_Z|N^L|=%d" % (a, tau, eHR, sumZL))
            print("        sum_z a_z >= %d and sum_z b_z >= %d, so mu_1, mu_2 >= %d"
                  % (need, need, kmin))
            print("        hence mu_1 + mu_2 >= %d and at least %d vertices of Z"
                  % (2 * kmin, avail))
            print("        are saturated on both sides; t = %d triangles are"
                  " needed (theta <= 33 - t - %d)" % (tmin, eHR))
            print("        %d available >= %d needed  ->  %s"
                  % (avail, tmin, "IMPOSSIBLE" if ok else "not closed"))
            if eHR:
                print("        (the surviving H-edge of R runs from t* to a w_i,"
                      " and w_i is")
                print("         never absorbed; %d candidates for %d slots let us"
                      " avoid t*,"  % (avail, tmin))
                print("         so theta(H[R']) = %d - 1 = %d as used above.)"
                      % (RSZ - tmin, RSZ - tmin - 1))
            if not ok:
                allclosed = False
        print()

    print("CONCLUSION")
    if allclosed:
        print("   Both pinned |R| = 9 cases are impossible.")
        print("   Row (57, 827) had |R| = 9 as its only open case, so it is")
        print("   ELIMINATED.  Row (57, 828) reduces to |R| in [10, 11].")
        print("   Order 57 open (row, |R|) cases: 2, down from 4.")
    else:
        print("   Some sub-configuration is not closed; see above.")


if __name__ == "__main__":
    main()

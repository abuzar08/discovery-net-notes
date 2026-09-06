#!/usr/bin/env python3
"""
Two more exact constraints on the order-57 frontier at r = 29.

STATE BEFORE THIS FILE (cover57.py): order 57 has two open rows and four open
(row, |R|) cases, (57,827) at |R| = 9 and (57,828) at |R| in [9,10,11], each
scoring 7354 or less against Z(29) = 8281.

Setting, from r29.py: H := complement(G) is factor-critical with theta(H) = 29;
the barrier is B = T u {s} with T an H-triangle; H - B = C u {w1} u {w2} with
N_H(w_i) inside B.  Low means d_G(v) = 28 EXACTLY, R is the high set, L the rest,
p := |L| = 57 - |R|, delta_0 := 28 - |R|, and X := 2m - 57*28.  Write
R = {w1, w2} u Z, and let

    j := |T ^ R|   (T-vertices that are high),     sigma := 1 if s is high.

==============================================================================
CONSTRAINT E -- T-VERTICES OF L NEED PAIRWISE DISTINCT BLOCKS.

T is an H-triangle, so its three vertices are pairwise NON-adjacent in G.  Two of
them therefore cannot lie in a common clique block.  The 3 - j T-vertices that
are low must consequently occupy pairwise distinct blocks.

Counting the available slots: the BIG blocks (q - 1 >= delta_0) are pairwise
disjoint, so a vertex lies in at most one of them, giving nbig slots; every other
vertex lies outside all BIG blocks, and there are p - sum_{BIG} q of those.
Hence

        3 - j  <=  nbig + ( p - sum_{BIG} q ) .

This is what kills the (24,24,2) minimiser at |R| = 9 when j = 0: there the two
K_24 blocks are BIG, disjoint and cover all 48 vertices, so nbig + 0 = 2 < 3.

==============================================================================
CONSTRAINT F -- FORCED NON-EDGES INSIDE R SHARPEN THE e(L) BAND.

cover57.py used e(G[R]) <= C(|R|,2).  Some pairs inside R are forced NON-edges of
G, because they are edges of H:

  * the j high T-vertices are pairwise H-adjacent            C(j,2) pairs;
  * each high T-vertex lying in A_1 u A_2 is H-adjacent to the
    corresponding w_i.  Writing a := |A_1| + |A_2| <= 3, exactly
    3 - a of the T-vertices lie outside A_1 u A_2 and force
    nothing, so this contributes             max(0, j - (3 - a)) pairs;
  * if s is high then s is H-adjacent to both w_1 and w_2    2 sigma pairs.

(These are distinct pairs.  Note s is H-adjacent to NO vertex of A_1 u A_2 by
non-domination, so s-T pairs are G-edges and are not subtracted; and w_1 w_2 is
a G-edge.)  Hence

        e(G[R])  <=  C(|R|,2) - C(j,2) - max(0, j - 3 + a) - 2 sigma ,

where a is bounded below by the excess budget: every z in Z is high, so
x_z >= 1 and sum_{z in Z} x_z = X - (54 - a) >= |Z| = |R| - 2, giving

        a  >=  a_min  :=  max(0, |R| + 52 - X).

The adversary takes a = a_min to leave as many T-vertices as possible outside
A_1 u A_2, so a_min is what enters the bound.

which tightens the upper end of the band e(L) = m - 28|R| - X + e(G[R]).

The two constraints pull against each other: j = 0 gives the weakest band but
the strongest block condition, while j >= 1 relaxes the block condition and pays
in the band.  A case dies only if EVERY (j, sigma) is infeasible.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import r29 as R9
from aug57 import adversary_gain

Z = R9.Z
crK = V.crK
OPEN = ((827, [9]), (828, [9, 10, 11]))


def solve(NL, eL_lo, eL_hi, Rsz, j):
    d0 = R9.DEG - Rsz
    best = [None, None]

    def rec(rem, capb, edges, blocks):
        if rem == 0:
            if eL_lo <= edges <= eL_hi:
                if sum(blocks) - NL < 0:
                    return
                big = [q for q in blocks if q - 1 >= d0]
                sb = sum(big)
                if sb > NL:
                    return
                if sum(q * (q - 1) for q in blocks if q - 1 < d0) < d0 * (NL - sb):
                    return
                if 3 - j > len(big) + (NL - sb):          # Constraint E
                    return
                tot = sum(crK(b) for b in blocks)
                if blocks:
                    tot += adversary_gain(sorted(blocks, reverse=True))
                if best[0] is None or tot < best[0]:
                    best[0], best[1] = tot, tuple(sorted(blocks, reverse=True))
            return
        hi, r2, c2 = edges, rem, capb
        while r2 > 0:
            t = min(c2, r2)
            hi += t * (t + 1) // 2
            r2 -= t
        if hi < eL_lo or edges > eL_hi:
            return
        for u in range(min(capb, rem), 0, -1):
            rec(rem - u, u, edges + u * (u + 1) // 2, blocks + [u + 1])
            if u >= 2 and (u + 1) % 2 == 1:
                rec(rem - u, u, edges + u + 1, blocks)
    for c in range(1, NL):
        rec(NL - c, NL - c, 0, [])
    return best


def main():
    print("Albertson r = 29, order 57: the last four cases")
    print("Z(29) = %d;  a counterexample has cr(G) <= %d" % (Z, Z - 1))
    print()
    print("  row  |R|   j  sig   e(L) range    score   minimiser      verdict")
    surv = {}
    for m, Rs in OPEN:
        X = 2 * m - R9.N * R9.DEG
        for Rsz in Rs:
            VL = R9.N - Rsz
            nZ = Rsz - 2
            base = m - (R9.DEG * Rsz + X)
            eLo = base + R9.eGR_min(Rsz)
            alive = []
            for j in range(0, 4):
                for sig in (0, 1):
                    if j + sig > nZ:
                        continue
                    amin = max(0, Rsz + 52 - X)
                    cap = (Rsz * (Rsz - 1) // 2 - j * (j - 1) // 2
                           - max(0, j - 3 + amin) - 2 * sig)
                    eHi = base + cap
                    if eHi < eLo:
                        print("  %3d   %2d   %d   %d    [%3d,%3d]   %6s   %-13s %s"
                              % (m, Rsz, j, sig, eLo, eHi, "-", "-", "band empty"))
                        continue
                    sc, w = solve(VL, eLo, eHi, Rsz, j)
                    dead = sc is None or sc >= Z
                    if not dead:
                        alive.append((j, sig, sc))
                    print("  %3d   %2d   %d   %d    [%3d,%3d]   %6s   %-13s %s"
                          % (m, Rsz, j, sig, eLo, eHi,
                             "none" if sc is None else sc,
                             "none" if w is None else str(w)[:13],
                             "impossible" if dead else "SURVIVES"))
            if alive:
                surv.setdefault(m, []).append((Rsz, alive))
    print()
    print("RESULT at order 57")
    for m, Rs in OPEN:
        left = surv.get(m, [])
        if not left:
            print("   row (57, %d) is ELIMINATED" % m)
        else:
            print("   row (57, %d) keeps |R| in %s" % (m, [t[0] for t in left]))
    print()
    tot = sum(len(v) for v in surv.values())
    print("   Open (row, |R|) cases at order 57: %d, unchanged." % tot)
    print()
    print("WHAT IS GAINED, since the case count does not move")
    print("   j = 0 is impossible in EVERY remaining case: at least one vertex")
    print("   of the H-triangle T must be high.  With j = 0 the three T-vertices")
    print("   of L need three pairwise distinct blocks (Constraint E), and no")
    print("   admissible multiset supplies them inside the e(L) band.")
    print()
    print("   The two |R| = 9 cases are pinned to a SINGLE configuration:")
    print("      j = 1, sigma = 0, block multiset (24, 24).")
    print("   So G[L] is exactly two disjoint copies of K_24 covering all 48 low")
    print("   vertices, with NO edges between them, and e(G[R]) = C(9,2) - 1 = 35.")
    print()
    print("   That rigidity is the opening for the next step.  No G-edges between")
    print("   the blocks means H contains the complete bipartite graph K_{24,24}")
    print("   between them, so H has a perfect matching on L using 24 edges, and")
    print("   theta(H) <= 24 + theta(H[R]) = 24 + 8 = 32.  Pushing to 28 needs")
    print("   four vertex-disjoint triangles {z, u, v} with z high, u and v in")
    print("   different blocks: each such triangle replaces an edge of the")
    print("   matching and absorbs one vertex of R, and 32 - 4 = 28 contradicts")
    print("   theta(H) = 29.  A high z fails to give one only if all of its")
    print("   H-neighbours in L lie in a single block, and then z is G-adjacent")
    print("   to all 24 vertices of the OTHER block, giving a K_25 of G.  With")
    print("   |Z| = 7 one of the two alternatives has at least four vertices;")
    print("   in the second, two of them attach to the same block (and are")
    print("   G-adjacent, since G[R] misses only one pair), giving a K_26 that")
    print("   is disjoint from the other block augmented by w_1, w_2:")
    print("      cr(K_26) + cr(K_25) = %d + %d = %d >= %d."
          % (V.crK(26), V.crK(25), V.crK(26) + V.crK(25), Z))
    print("   Making the first alternative rigorous needs a system of distinct")
    print("   representatives for the u and v; that is the open step.")


if __name__ == "__main__":
    main()

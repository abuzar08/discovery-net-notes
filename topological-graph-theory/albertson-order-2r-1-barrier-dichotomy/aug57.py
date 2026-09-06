#!/usr/bin/env python3
"""
Two new ingredients close row (57, 826) and narrow row (57, 827) at r = 29.

STATE BEFORE THIS FILE.  r29.py reduces the five order-57 rows of the r = 29
frontier (ledger height 2761) to three, with explicit high-vertex counts:

    (57, 824) eliminated        (57, 826) reduces to |R| in [7]
    (57, 825) eliminated        (57, 827) reduces to |R| in [7, 8, 9]
                                (57, 828) reduces to |R| in [7, ..., 11]

The surviving rows are scored by `min_split`, which minimises sum crK(|Q_i|)
over the clique blocks of the Gallai forest L induced by the low vertices.  Two
resources were being discarded, and this file recovers them.

Setting, from r29.py: G is 29-critical of order n = 2r-1 = 57 with
cr(G) < cr(K_29) <= Z(29) = 8281; H := complement(G) is factor-critical with
theta(H) = 29 and no conformal triangle; the barrier classification leaves
B = T u {s} with T an H-triangle, and

    H - B  =  C  u  {w1}  u  {w2},    |C| = 49,   N_H(w_i) inside B.

Low means d_G(v) = r - 1 = 28 exactly; R is the set of high vertices; L is the
rest, and by Gallai every block of G[L] is a clique or an odd cycle.

==============================================================================
INGREDIENT A -- AUGMENT ONE BLOCK BY w1 AND w2.

First, the scoring needs no vertex-disjointness at all.  Distinct blocks of a
graph are EDGE-disjoint, and in any drawing a crossing is between two edges; if
those edges lie in different blocks the crossing is counted in neither.  So

        sum_i cr(Q_i)  <=  cr(G)

immediately, and the restriction to blocks of order >= 15 that `min_split` uses
(justified there by disjointness) can be dropped.  That turns out to change no
number -- the minimiser never uses small blocks, because they are inefficient at
producing edges -- but it is what licenses the next step.

Now, N_H(w_i) lies inside B, so each w_i is G-adjacent to EVERY vertex of C, and
w1 w2 is a G-edge because w1 and w2 are different components of H - B.  Hence for
any block Q_j,

        (Q_j ^ C) u {w1, w2}   is a clique of G   of order  q_j - beta_j + 2,
        where beta_j := |Q_j ^ B| .

Its edges are those inside Q_j, plus edges at w1 or w2, and w1, w2 are high, so
they lie in no block of G[L].  So this clique is edge-disjoint from every other
block, and

        cr(G)  >=  cr(K_{q_j - beta_j + 2})  +  sum_{l != j} cr(Q_l).

WHAT THE ADVERSARY CAN DO.  B = T u {s} has four vertices.  T is an H-triangle,
so its three vertices are pairwise NON-adjacent in G and a G-clique contains at
most one of them.  A B-vertex lying in two blocks would be a cut vertex of
degree at least (q_1 - 1) + (q_2 - 1); it is low, so that is at most 28, and the
blocks that matter here have order at least 22 (Ingredient B), so a B-vertex
lies in at most one of them.  Therefore

        beta_j <= 2,   at most one beta_j = 2 (only one block can hold s),
        sum_j beta_j <= 4 .

The adversary chooses beta to minimise our best gain, and we take the maximum
over which block to augment.  For a target gain g, block j needs beta_j at least
the least b with crK(q_j - b + 2) - crK(q_j) <= g, so feasibility is a threshold
test and the adversary's optimum is found exactly by scanning the candidate
values of g.  (Blocks of order at most 2 have gain 0 for every beta, so the
adversary never spends there and they do not distort the count.)

==============================================================================
INGREDIENT B -- EVERY LOW VERTEX NEEDS ENOUGH BLOCK DEGREE.

A low vertex v has d_G(v) = 28 EXACTLY.  Its neighbours inside L are precisely
the union of its blocks minus itself, and distinct blocks through v meet only at
v, so that number is sum_{blocks ni v} (|Q| - 1).  Its remaining neighbours lie
in R.  Hence

        sum_{blocks ni v} (|Q| - 1)  >=  28 - |R|  =:  delta_0 .

Two consequences, both used below.

  (i) NO ISOLATED LOW VERTEX.  A vertex in no block would need 28 neighbours
      inside R, and |R| <= 11 here.  So every vertex of L lies in a block and
      sum_j q_j >= p, i.e. extra := sum_j q_j - p >= 0.

 (ii) SMALL BLOCKS MUST BE ALL CUT VERTICES.  If q - 1 < delta_0 then every
      vertex of that block lies in a second block.  The number of vertices lying
      in at least two blocks is sum_v (d(v) - 1) = sum_j q_j - p = extra.  So
      every block with q - 1 < delta_0 satisfies q <= extra.

At |R| = 7 this gives delta_0 = 21, so every block that contains a non-cut vertex
has order at least 22, and the connector blocks the minimiser wanted to use --
(26, 23, 3) with a K_3 joining two big cliques -- are ruled out unless they are
tiny enough to consist entirely of cut vertices.

==============================================================================
RESULT.  The `plain` column below reproduces r29.py exactly, which checks the
harness.  With both ingredients:

    row (57, 826), whose only open case was |R| = 7, is ELIMINATED;
    row (57, 827) loses |R| = 7 and reduces to |R| in [8, 9];
    row (57, 828) is unchanged, at |R| in [7, ..., 11].

So the order-57 frontier goes from three open rows to two.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import r29 as R9

Z = R9.Z
crK = V.crK


def adversary_gain(qs):
    """Minimum over the adversary's admissible beta of our best augmentation
    gain.  See INGREDIENT A for the constraints on beta."""
    cands = sorted({crK(q - b + 2) - crK(q) for q in qs for b in (0, 1, 2)} | {0})
    for g in cands:
        th, ok = [], True
        for q in qs:
            t = None
            for b in (0, 1, 2):
                if crK(q - b + 2) - crK(q) <= g:
                    t = b
                    break
            if t is None:
                ok = False
                break
            th.append(t)
        if ok and sum(th) <= 4 and sum(1 for t in th if t == 2) <= 1:
            return g
    return 0


def solve(NL, eL_lo, Rsz, use_deg, use_aug):
    """Minimise the block score over Gallai forests on NL vertices carrying at
    least eL_lo edges, optionally with each ingredient switched on."""
    d0 = R9.DEG - Rsz
    best = [None, None]

    def rec(rem, cap, edges, blocks):
        if rem == 0:
            if edges >= eL_lo:
                if use_deg:
                    extra = sum(blocks) - NL
                    if extra < 0:
                        return                       # an isolated low vertex
                    if any(q - 1 < d0 and q > extra for q in blocks):
                        return                       # a small block with a non-cut vertex
                tot = sum(crK(b) for b in blocks)
                if use_aug and blocks:
                    tot += adversary_gain(sorted(blocks, reverse=True))
                if best[0] is None or tot < best[0]:
                    best[0], best[1] = tot, tuple(sorted(blocks, reverse=True))
            return
        hi, r2, c2 = edges, rem, cap
        while r2 > 0:
            t = min(c2, r2)
            hi += t * (t + 1) // 2
            r2 -= t
        if hi < eL_lo:
            return
        for u in range(min(cap, rem), 0, -1):
            rec(rem - u, u, edges + u * (u + 1) // 2, blocks + [u + 1])
            if u >= 2 and (u + 1) % 2 == 1:
                rec(rem - u, u, edges + u + 1, blocks)
    for c in range(1, NL):
        rec(NL - c, NL - c, 0, [])
    return best


ROWS = ((826, [7]), (827, [7, 8, 9]), (828, [7, 8, 9, 10, 11]))


def main():
    print("Albertson r = 29, order 57: two discarded resources recovered")
    print("Z(29) = %d;  a counterexample has cr(G) <= %d" % (Z, Z - 1))
    print()
    print("The `plain` column must reproduce r29.py exactly.")
    print()
    print("  row  |R|  |V(L)|  e(L) >=   plain   +w1,w2   +degree   minimiser"
          "       verdict")
    surv = {}
    for m, Rs in ROWS:
        X = 2 * m - R9.N * R9.DEG
        for Rsz in Rs:
            VL = R9.N - Rsz
            eL = m - (R9.DEG * Rsz + X) + R9.eGR_min(Rsz)
            p, _ = solve(VL, eL, Rsz, False, False)
            a, _ = solve(VL, eL, Rsz, False, True)
            d, w = solve(VL, eL, Rsz, True, True)
            dead = d is None or d >= Z
            if not dead:
                surv.setdefault(m, []).append(Rsz)
            print("  %3d   %2d    %3d     %4d    %5s   %5s    %5s   %-14s %s"
                  % (m, Rsz, VL, eL, p, a, d, str(w)[:14],
                     "impossible" if dead else "SURVIVES"))
    print()
    print("RESULT at order 57")
    for m, Rs in ROWS:
        left = surv.get(m, [])
        if not left:
            print("   row (57, %d) is ELIMINATED" % m)
        else:
            print("   row (57, %d) reduces to |R| in %s   (was %s)" % (m, left, Rs))
    print()
    print("   Order-57 open rows: %d, down from 3." % len(surv))
    print("   Order 58 = 2r is not covered by this argument.")


if __name__ == "__main__":
    main()

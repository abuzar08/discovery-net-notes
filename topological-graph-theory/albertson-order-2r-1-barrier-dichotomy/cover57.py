#!/usr/bin/env python3
"""
Two exact constraints on the low-vertex Gallai forest narrow order 57 at r = 29
to two rows and three high-vertex counts.

STATE BEFORE THIS FILE.  aug57.py added block augmentation by w_1, w_2 and a
first, weak form of the low-vertex degree condition, leaving

    (57, 824) eliminated    (57, 826) eliminated
    (57, 825) eliminated    (57, 827) |R| in [8, 9]
                            (57, 828) |R| in [7, ..., 11]

Both ingredients here are exact statements about the block structure of the
Gallai forest L induced by the low vertices, and both were being under-used.
Everything aug57.py concluded remains valid: these filters only ever exclude
more, so nothing already closed is reopened.

Setting, from r29.py: G is 29-critical of order n = 2r-1 = 57 with
cr(G) < cr(K_29) <= Z(29) = 8281; H := complement(G) is factor-critical with
theta(H) = 29 and no conformal triangle; the barrier classification leaves
B = T u {s} with T an H-triangle, and H - B = C u {w1} u {w2} with |C| = 49 and
N_H(w_i) inside B.  Low means d_G(v) = r - 1 = 28 EXACTLY; R is the set of high
vertices, L the rest, p := |L| = 57 - |R|, and delta_0 := 28 - |R|.

==============================================================================
INGREDIENT C -- THE COVERING FORM OF THE LOW-VERTEX DEGREE CONDITION.

A low vertex v has d_G(v) = 28 exactly.  Its neighbours inside L are precisely
the union of its blocks minus itself, since distinct blocks through v meet only
at v.  Its remaining neighbours lie in R, so

        sum_{blocks ni v} (|Q| - 1)  >=  28 - |R|  =  delta_0 .

aug57.py used only the consequence "a block with q - 1 < delta_0 has all its
vertices in a second block, and there are at most sum_j q_j - p such vertices".
That is too weak: it accepts (25, 23, 2, 2) on p = 49 with delta_0 = 20, where
each K_2 has 2 <= extra = 3 vertices.  But the two large blocks cannot share a
vertex (its degree would be 24 + 22 = 46 > 28), so they cover 48 distinct
vertices, and the 49th vertex can reach block degree at most 1 + 1 = 2, far
below 20.  The configuration is impossible and the per-block test misses it.

The correct form is a covering count.  Call a block BIG when q - 1 >= delta_0.
Two BIG blocks cannot share a vertex: it would have degree at least 2 delta_0,
and 2 delta_0 > 28 for every |R| <= 13, which covers the whole range here.  So
the BIG blocks are pairwise disjoint and cover exactly sum_{BIG} q_j vertices,
all of which satisfy the condition automatically.  Every one of the remaining
p - sum_{BIG} q_j vertices must reach delta_0 from small blocks alone, and a
small block Q contributes q - 1 to each of its q vertices, so the total value the
small blocks can distribute is sum_{small} q_j (q_j - 1).  Hence

        sum_{small} q_j (q_j - 1)  >=  delta_0 * ( p - sum_{BIG} q_j ) .

(Some of that value is spent on vertices that are already in a BIG block, so
this is a relaxation and therefore safe.)

==============================================================================
INGREDIENT D -- e(L) IS BOUNDED ABOVE, NOT ONLY BELOW.

All the excess sits in R, since low means x_v = 0, so
sum_{v in R} d_G(v) = 28|R| + X with X := 2m - 57*28.  Counting the edges
incident to R once each,

        e(L)  =  m - ( sum_{v in R} d_G(v) - e(G[R]) )
              =  m - 28|R| - X + e(G[R]) ,

which is an IDENTITY.  The existing argument used only e(G[R]) >= eGR_min to
get a lower bound on e(L).  But equally e(G[R]) <= C(|R|,2), so

        m - 28|R| - X + eGR_min  <=  e(L)  <=  m - 28|R| - X + C(|R|,2),

and e(L) is exactly sum_j C(q_j, 2) over the clique blocks.  At |R| = 8 on row
827 this pins e(L) into [555, 573], and every way of covering 49 vertices by two
disjoint BIG blocks -- (26,23), (25,24), (27,22), (28,21) -- carries at least
576 edges.  Anything with fewer BIG blocks leaves vertices that Ingredient C
cannot supply.  So no admissible block multiset exists at all, and the case dies
structurally rather than by a crossing count.

==============================================================================
RESULT.

    (57, 826) eliminated          (57, 827) reduces to |R| = 9
    (57, 828) reduces to |R| in [9, 10, 11]

so order 57 keeps two open rows and three high-vertex counts, down from five
rows originally and from nine (row, |R|) cases before aug57.py.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import r29 as R9
from aug57 import adversary_gain

Z = R9.Z
crK = V.crK
ROWS = ((824, []), (825, []), (826, [7]), (827, [7, 8, 9]),
        (828, [7, 8, 9, 10, 11]))


def solve(NL, eL_lo, eL_hi, Rsz, cover=True, cap_hi=True):
    """Minimise the augmented block score over Gallai forests on NL vertices
    whose edge count lies in [eL_lo, eL_hi].  Returns (score, minimiser), with
    score None when no admissible block multiset exists at all."""
    d0 = R9.DEG - Rsz
    best = [None, None]

    def rec(rem, capb, edges, blocks):
        if rem == 0:
            if edges >= eL_lo and (not cap_hi or edges <= eL_hi):
                if sum(blocks) - NL < 0:
                    return                        # an isolated low vertex
                if cover:
                    big = [q for q in blocks if q - 1 >= d0]
                    sb = sum(big)
                    if sb > NL:
                        return                    # BIG blocks are disjoint
                    if sum(q * (q - 1) for q in blocks if q - 1 < d0) \
                            < d0 * (NL - sb):
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
        if hi < eL_lo:
            return
        if cap_hi and edges > eL_hi:
            return
        for u in range(min(capb, rem), 0, -1):
            rec(rem - u, u, edges + u * (u + 1) // 2, blocks + [u + 1])
            if u >= 2 and (u + 1) % 2 == 1:
                rec(rem - u, u, edges + u + 1, blocks)
    for c in range(1, NL):
        rec(NL - c, NL - c, 0, [])
    return best


def main():
    print("Albertson r = 29, order 57: covering and the two-sided e(L) identity")
    print("Z(29) = %d;  a counterexample has cr(G) <= %d" % (Z, Z - 1))
    print()
    print("  row  |R|  |V(L)|   e(L) range    aug57   +cover   +e(L) cap"
          "   minimiser     verdict")
    surv = {}
    for m, Rs in ROWS:
        X = 2 * m - R9.N * R9.DEG
        for Rsz in Rs:
            VL = R9.N - Rsz
            base = m - (R9.DEG * Rsz + X)
            eLo = base + R9.eGR_min(Rsz)
            eHi = base + Rsz * (Rsz - 1) // 2
            a, _ = solve(VL, eLo, eHi, Rsz, cover=False, cap_hi=False)
            b, _ = solve(VL, eLo, eHi, Rsz, cover=True, cap_hi=False)
            c, w = solve(VL, eLo, eHi, Rsz, cover=True, cap_hi=True)
            dead = c is None or c >= Z
            if not dead:
                surv.setdefault(m, []).append(Rsz)
            print("  %3d   %2d    %3d     [%3d,%3d]   %6s   %6s     %6s"
                  "   %-13s %s"
                  % (m, Rsz, VL, eLo, eHi, a, b,
                     "none" if c is None else c,
                     "none" if w is None else str(w)[:13],
                     "impossible" if dead else "SURVIVES"))
    print()
    print("   A score of `none` means no admissible block multiset exists at")
    print("   all: the case dies structurally, not by a crossing count.")
    print()
    print("RESULT at order 57")
    for m, Rs in ROWS:
        left = surv.get(m, [])
        if not Rs:
            print("   row (57, %d) was already eliminated" % m)
        elif not left:
            print("   row (57, %d) is ELIMINATED" % m)
        else:
            print("   row (57, %d) reduces to |R| in %s   (was %s)" % (m, left, Rs))
    print()
    print("   Open (row, |R|) cases at order 57: %d, down from 9 before aug57.py."
          % sum(len(v) for v in surv.values()))
    print("   Order 58 = 2r is not covered by this argument.")


if __name__ == "__main__":
    main()

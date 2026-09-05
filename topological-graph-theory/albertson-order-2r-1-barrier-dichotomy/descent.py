#!/usr/bin/env python3
"""
The three b <= 7 classes of the last open branch of Albertson order 58 at r = 29:
two structural reductions, and an honest account of what they do not close.

The branch: G is 29-critical of order 58 with cr(G) < cr(K_29) <= Z(29) = 8281,
H := complement(G) is K_4-free with two disjoint triangles T_1, T_2, and the
Tutte barrier B (which contains T_1 u T_2) satisfies o(H - B) >= |B| - 4.
k4free.py closes every class with b := |B| >= 8, using Gallai blocks inside B.
Three classes are left, all with B barely bigger than T_1 u T_2:

      b = 6, c = (51, 1)      split bound 4470 / 4447 / 4424
      b = 6, c = (50, 1, 1)   split bound 5027 / 5002 / 4977
      b = 7, c = (49, 1, 1)   split bound 4533 / 4509 / 4486     against 8281.

These are not near misses; the barrier is too small for a Gallai argument, so
any leverage has to come from inside the big component C.  This file establishes
two reductions and then reports, negatively, that they are not enough.

==============================================================================
REDUCTION 1 -- CLIQUE-COVER TRANSFER.  For any vertex set S, a clique cover of
H[S] together with one of H - S covers H, so theta(H) <= theta(H[S]) +
theta(H - S), i.e.

        theta(H[C]) >= 29 - theta(H - C).

An explicit cover of H - C is needed (an upper bound, not the K_4-free lower
bound ceil(|H-C|/3)).  For c = (51,1), H - C is B u {w} = 7 vertices, covered by
T_1, T_2 and {w}: three cliques.  Hence

        theta(H[C]) >= 26     with     |C| = 51 = 2*26 - 1.

A clique cover of H[C] with t triangles, e edges and s singletons has
3t + 2e + s = 51 and size 51 - 2t - e, so this says exactly

        2t + e <= 25   for every disjoint packing of t triangles and e edges.

Two consequences.  (i) A triangle-free graph on 51 vertices has at most
floor(51^2/4) = 650 edges (Mantel), so once e(H[C]) > 650 a triangle T exists.
(ii) NO CONFORMAL TRIANGLE: a perfect matching of H[C] - T would be 24 edges and
2*1 + 24 = 26 > 25.  So H[C] - T has no perfect matching, and by Tutte there is
S inside C - T with

        o(H[C] - T - S) >= |S| + 2

(parity: 48 - |S| and |S| agree mod 2, so the deficiency is at least two).

That is the SAME no-conformal-triangle condition that drives the order-2r-1
theory in this directory, reappearing one level down inside C, on 2*26 - 1
vertices.  PARITY IS ESSENTIAL: the argument needs |C| odd, since for even |C|
the set C - T is odd and has no perfect matching for trivial reasons.  So the
transfer reaches the (51,1) class ONLY.  For c = (50,1,1) the best explicit
cover of H - C = B u {w_1, w_2} has four cliques, giving theta(H[C]) >= 25 with
|C| = 50, and the forbidden packing becomes "two disjoint triangles plus a
perfect matching of the remaining 44", which removes six vertices instead of
three and is correspondingly weaker.  For b = 7, c = (49,1,1) the cover needs
five cliques and theta(H[C]) >= 24, which forbids nothing at all: a triangle
plus a matching of 23 gives 2 + 23 = 25 = 49 - 24, still allowed.

==============================================================================
REDUCTION 2 -- A K_4-FREE SHARPENING OF THE SINGLETON DEGREE.  Let {w} be a
singleton component of H - B, so N_H(w) is contained in B.  If w were H-adjacent
to all three vertices of T_i then {w} u T_i would induce a K_4, so

        |N_H(w) ^ T_i| <= 2   for i = 1, 2,   hence   d_H(w) <= b - 2.

Together with delta(H) >= 2 (the order-2r non-domination lemma at ledger height
2933: no vertex of N_H(w) is adjacent to all the others, which fails vacuously
when d_H(w) = 1) this gives, at b = 6,

        2 <= d_H(w) <= 4,   so   x_w := 29 - d_H(w) >= 25,

against the 23 the barrier alone gives.  In the (50,1,1) class the two
singletons then consume at least 50 of the excess budget X <= 56, leaving at
most 6 units for the other 56 vertices.  The same sharpening applies to every
vertex of every component and is fed back into k4free.py as x_v >= r + 3 - s - b.

==============================================================================
THE TWO FILTERS ON THE SECOND-LEVEL BARRIER, and what survives.

Write s := |S| and let the components of H[C] - T - S have sizes n_1, ..., n_k
summing to 48 - s, at least s + 2 of them odd.

EXCESS.  A vertex v of the component of size n_i has its H-neighbours inside
that component, S, T and B only -- not w, whose H-neighbours all lie in B.  At
most b - 2 = 4 of them lie in B, and at most 2 lie in T, since v adjacent to all
three of the triangle T would make {v} u T a K_4.  So
d_H(v) <= (n_i - 1) + s + 2 + 4 and

        x_v >= r + 1 - n_i - s - b = 24 - n_i - s,

giving   25 + sum_i n_i max(0, 24 - n_i - s) <= X.

BIPARTITION.  The components are pairwise non-adjacent in H, and so is w, so in
G the sets D_1, ..., D_k, {w} are pairwise completely joined: G contains that
complete multipartite graph, hence K_{a, 49-s-a} for every realisable sub-sum a,
and K_{k+1} by taking one vertex per part.  Both must stay below Z(29).

SECOND-LEVEL SPLIT (the filter that closes families B and C).  Put

        A := D_1 u ... u D_k u W        (W = the singletons of H - B)
        R := S u T u B.

These are disjoint and A u R = V(H), since |A| + |R| = (|C| - 3 - s) + |W| +
(s + 3 + b) = |C| + |W| + b = 58.  Inside A the only H-edges are those inside the
D_i (distinct components are non-adjacent, W is non-adjacent to D and to itself),
so writing P := sum_i e(H[D_i]),

        e(H) = P + e_H(A, R) + e(H[R]).

Every excess is non-negative and they total X, so sum_{v in A} x_v <= X, i.e.

        |A| r - (2P + e_H(A,R))  <=  X,      e_H(A,R) >= |A| r - 2P - X,

and substituting into the edge count gives the key inequality

        e(H[R])  <=  e(H) + P - |A| r + X,

hence   e(G[R]) >= C(|R|,2) - e(H) - P + |A| r - X.

P is capped by Turan (each D_i is K_4-free), and taking P at its cap is the
conservative choice: it lowers both e(G[R]) and e(G[A]) = C(|A|,2) - P.  Since A
and R are disjoint the crossing number is additive over them:

        cr(G) >= cr(G[A]) + cr(G[R]),
        cr(G[A]) >= max( crK(k + |W|), best_bipartition, L(|A|, C(|A|,2) - P) ),
        cr(G[R]) >= L(|R|, e(G[R])).

If the bound on e(H[R]) comes out negative the configuration is impossible
outright.

The filters pull against each other -- excess wants one huge component,
bipartition wants no two large ones -- and together with Reduction 2 they cut
the second-level barriers from 68 per row to FIVE, in three families.  But five is
not zero, and none of them is closed by anything in this directory; PART 2 lists
them and PART 3 says why each escapes.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import verify_range as V
import k4free as K
import crminus as CM
from order2r import L, RCHI, Z

r = RCHI
n = 2 * r


def partitions(total, nodd):
    """Multisets of positive parts summing to `total` with >= nodd odd parts."""
    out = []

    def rec(rem, maxsz, cur):
        if rem == 0:
            if sum(1 for v in cur if v % 2) >= nodd:
                out.append(tuple(cur))
            return
        for sz in range(min(maxsz, rem), 0, -1):
            rec(rem - sz, sz, cur + [sz])
    rec(total, total, [])
    return out


def level1(bsz, csizes, X, eH, verbose=False):
    """Second-level barriers of the (51,1) class surviving both filters."""
    C = max(csizes)
    others = [x for x in csizes if x != C]
    # x_w >= r + 2 - b for each singleton of H - B (K_4-free sharpening)
    xw = sum(sz * max(0, r + 3 - sz - bsz) for sz in others)
    surv = []
    for s in range(0, C - 3 + 1):
        rest = C - 3 - s
        if rest < s + 2:
            continue
        for sizes in partitions(rest, s + 2):
            cost = sum(ni * max(0, r + 1 - ni - s - bsz) for ni in sizes)
            if xw + cost > X:
                continue
            parts = list(sizes) + list(others)
            if V.best_bipartition(parts) >= Z:
                continue
            if V.crK(len(parts)) >= Z:
                continue
            # --- second-level split bound, with Gallai blocks inside R ---
            nA = sum(sizes) + len(others)
            nR = s + 3 + bsz
            CR = nR * (nR - 1) // 2
            Pmax = sum(min(ni * ni // 3, ni * (ni - 1) // 2) for ni in sizes)
            Pmin = sum(ni - 1 for ni in sizes)
            best = None
            for YA in range(xw + cost, X + 1):
                # e(H[R]) = eH + P - |A| r + YA must lie in [0, C(|R|,2)].
                # The bound decreases in P, so take P as large as feasible.
                P = min(Pmax, CR - eH + nA * r - YA)
                if P < max(Pmin, nA * r - eH - YA):
                    continue                  # no feasible P for this YA
                eHR = eH + P - nA * r + YA
                eGR = CR - eHR
                crA = max(V.crK(len(parts)), V.best_bipartition(parts),
                          L(nA, nA * (nA - 1) // 2 - P), CM.g(nA, P))
                crR = max(L(nR, eGR), CM.g(nR, eHR)) if eGR > 0 else 0
                # excess left on R is X - YA, so at least nR - (X - YA) of its
                # vertices are low and G[low(R)] is a Gallai forest
                pR = nR - (X - YA)
                eLR = eGR - (X - YA) * min(nR - 1, r)
                if pR >= 2:
                    qR = K.forced_clique(pR, eLR, r)
                    if qR is None:
                        continue              # no Gallai forest with that many edges
                    crR = max(crR, V.crK(qR))
                t = crA + crR
                if best is None or t < best:
                    best = t
            if best is None or best >= Z:
                continue
            surv.append((s, tuple(sizes), xw + cost, best))
    return surv


def main():
    print("Albertson order 58 at r = 29: the three b <= 7 classes")
    print("Z(%d) = %d;  a counterexample has cr(G) <= %d" % (r, Z, Z - 1))
    print()

    print("PART 1   which classes inherit a usable clique-cover bound")
    for bsz, c in ((6, (51, 1)), (6, (50, 1, 1)), (7, (49, 1, 1))):
        C = max(c)
        cover = 2 + (bsz - 6) + (len(c) - 1)
        theta = r - cover
        cap = C - theta                      # every packing has 2t + e <= cap
        # the packing "one triangle + a perfect matching of the rest"
        usable = (C % 2 == 1) and (2 + (C - 3) // 2 > cap)
        print("   b=%d c=%-11s |C|=%2d, H-C is %d vertices covered by %d cliques,"
              % (bsz, str(c) + ":", C, n - C, cover))
        print("        theta(H[C]) >= %d, so every packing has 2t + e <= %d;"
              % (theta, cap))
        if C % 2 == 1:
            print("        triangle + perfect matching of the rest costs %d  -> %s"
                  % (2 + (C - 3) // 2,
                     "FORBIDDEN, transfer usable" if usable else "allowed, no transfer"))
        else:
            print("        |C| is even, so C - T is odd and has no perfect")
            print("        matching for trivial reasons  -> no transfer")
    print()

    print("PART 2   the (51,1) class: second-level barriers surviving both filters")
    for m in (838, 839, 840):
        X = 2 * m - n * (r - 1)
        eH = n * (n - 1) // 2 - m
        surv = level1(6, (51, 1), X, eH)
        print("   m=%d (X=%d): %d survive%s" % (m, X, len(surv),
              "  -> CLASS IMPOSSIBLE" if not surv else ""))
        fams = {}
        for s, sizes, cost, cr in surv:
            fams.setdefault(s, []).append((sizes, cost, cr))
        for s in sorted(fams):
            ex = fams[s][0]
            print("        s=%2d : %3d barriers, e.g. sizes %s%s costing %d of %d,"
                  " split bound %d"
                  % (s, len(fams[s]),
                     str(ex[0][:3]),
                     "+1^%d" % (len(ex[0]) - 3) if len(ex[0]) > 3 else "",
                     ex[1], X, ex[2]))
    print()

    print("PART 3   why they still survive, and by how little")
    print("   Family A (s = 0, sizes (47,1)).  Here R = T u B is only 9 vertices,")
    print("   so the second-level split has almost nothing to work with: the")
    print("   feasibility cap e(H[R]) <= C(9,2) = 36 forces P up to 594 and A")
    print("   carries the whole bound, L(49, 582).  This is the self-similar")
    print("   descent case -- C shrinks by 4 while theta drops by 2, so the")
    print("   transfer reapplies verbatim on 47 = 2*24 - 1 vertices -- and it is")
    print("   still the furthest from Z.")
    print("   Families B (s = 22) and C (s = 23).  Now R is 31 or 32 vertices and")
    print("   the split is strong: A is a clique K_26 or K_27 of G worth %d,"
          % V.crK(26))
    print("   and R carries at most e(H) + P - |A| r + Y_A H-edges, so G[R] is")
    print("   nearly complete.  The bound is minimised at Y_A = 47 or 48, where")
    print("   the excess left on R is only 4 or 5, so 27 or 28 of its vertices")
    print("   are low and Gallai forces a clique block of order 23 or 24.")
    print("   The profile is a narrow dip in Y_A: it is above Z at both ends")
    print("   and only the middle survives.  Closing it needs a few hundred more,")
    print("   from the e_G(A,R) edges the split discards or from a still sharper")
    print("   crossing bound at high density.")
    print()
    print("   Kleitman bipartite bound on a 48-vertex split, for reference:")
    for a_ in (24, 20, 16, 14, 12, 8, 4, 1):
        v = V.kleitman_bipartite(a_, 48 - a_)
        print("      cr(K_{%2d,%2d}) >= %6d   %s"
              % (a_, 48 - a_, v, "kills" if v >= Z else "survives"))
    print()
    print("CONCLUSION")
    print("   The second-level split plus the dense-subgraph bound raise the")
    print("   three surviving second-level barriers of the (51,1) class well")
    print("   above cr(K_26) = %d, to the values listed in PART 2," % V.crK(26))
    print("   against Z(29) = %d.  Two of the three are now within 500, but" % Z)
    print("   none is closed, and the (50,1,1) and (49,1,1) classes do not even")
    print("   inherit the transfer.  Order 58 at r = 29 remains open.")


if __name__ == "__main__":
    main()

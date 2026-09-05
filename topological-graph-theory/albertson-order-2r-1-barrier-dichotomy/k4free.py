#!/usr/bin/env python3
"""
The last open branch of Albertson order 58 at r = 29, closed by Gallai blocks.

State of the order-58 case before this file:

  * height 2933 (order2r.py PART 2): impossible whenever H contains a K_4.
  * order2r.py PART 3: impossible whenever H has no two disjoint triangles.

Those two hypotheses are complementary, so exactly one branch was left:

      H is K_4-free AND H has two vertex-disjoint triangles T_1, T_2.

Setting.  G is 29-critical of order n = 2r = 58 with cr(G) < cr(K_29) <= Z(29) =
8281, H := complement(G), theta(H) = r = 29, Delta(H) <= r, and the row is one of
m = 838, 839, 840 (the r = 29 frontier at ledger height 2761), i.e.
e(H) = 815, 814, 813.

Why the barrier has deficiency four.  If H - (T_1 u T_2) had a perfect matching,
its 26 edges together with T_1 and T_2 would cover V(H) with 28 = r-1 cliques,
contradicting theta(H) = r.  So by Tutte there is a set B' inside
V(H) - (T_1 u T_2) with o(H - T_1 - T_2 - B') >= |B'| + 2 (parity forces +2, not
+1: 58 - 6 - |B'| = 52 - |B'| has the same parity as |B'|).  Put
B := B' u T_1 u T_2, b := |B| = |B'| + 6.  Then

      o(H - B)  >=  |B'| + 2  =  b - 4,        and  e(H[B]) >= 6.

That deficiency of four (against two in the K_4 route) is what kept this branch
alive: it lets b run up to 30 and destroys the packing constraints that closed
every other class.

------------------------------------------------------------------------------
THE NEW INGREDIENT: Gallai's low-vertex theorem, applied inside the barrier.

  Gallai, "Kritische Graphen II", Publ. Math. Inst. Hungar. Acad. Sci. 8 (1963)
  373-395:  in a k-critical graph the vertices of degree k-1 induce a subgraph
  whose every block is a complete graph or an odd cycle (a "Gallai forest").

Write x_v := d_G(v) - (r-1) >= 0 for the excess, so sum_v x_v = 2m - n(r-1) =: X
and x_v = r - d_H(v).  Call v LOW when x_v = 0, i.e. d_G(v) = r-1 = 28.  Split
the excess between the barrier and its complement:

      Y := sum_{v in D} x_v,      X - Y = sum_{v in B} x_v,      D := V(H) - B.

Every non-low vertex carries at least one unit of excess, so

      #(low vertices of B) >= b - (X - Y),   #(low vertices of D) >= |D| - Y.

G restricted to the low vertices of B is a Gallai forest, and likewise inside D.
Deleting the at most X-Y non-low vertices of B costs at most (X-Y)(b-1) edges:

      e(G[L_B]) >= e(G[B]) - (X-Y)(b-1),    e(G[L_D]) >= e(G[D]) - Y(|D|-1).

MAXIMUM EDGES OF A GALLAI FOREST.  Let F be a Gallai forest on p vertices with
every block of order <= q.  Each component is a block tree, so summing over
components sum_i (|Q_i| - 1) = p - #components <= p - 1.  An odd cycle of order
s has s <= C(s,2) edges, so cliques dominate, and t -> C(t+1,2) is convex, so the
edge count sum_i C(|Q_i|,2) is maximised by taking as many blocks of the maximum
order q as the budget s := p-1 allows:

      maxgallai(p, q) = k * C(q,2) + C(rem+1, 2),
      k = floor(s/(q-1)),  rem = s - k(q-1).

A low vertex has d_G = r-1 = 28, so it has at most 28 neighbours altogether and
any clique block containing it has order <= r = 29.  Hence if

      e(G[L_B]) > maxgallai(|L_B|, q-1)

then G[L_B] -- and therefore G -- contains a CLIQUE of order at least q, and if
e(G[L_B]) > maxgallai(|L_B|, r) the configuration is impossible outright.

The forced block lies inside B, the forced block inside D lies inside D, and
B and D are disjoint, so the crossing number is additive over them:

      cr(G) >= cr(K_{q_B}) + cr(K_{q_D}).

------------------------------------------------------------------------------
A K_4-FREE SHARPENING OF THE DEGREE BOUND.  B contains the two disjoint
triangles T_1 and T_2.  If a vertex v outside T_i were H-adjacent to all three
of its vertices, then {v} u T_i would induce a K_4 in H.  So every vertex
outside B has at most two H-neighbours in each T_i, hence at most

        2 + 2 + (b - 6)  =  b - 2

H-neighbours in B altogether.  A vertex v in a component of size s of H - B
therefore has d_H(v) <= (s-1) + (b-2), so its excess satisfies

        x_v = r - d_H(v) >= r + 3 - s - b,

one better than the r + 1 - s - b used before this branch was isolated.  For a
singleton component it says d_H(w) <= b - 2 and x_w >= r + 2 - b: at b = 6 that
is x_w >= 25 where the old bound gave 23.

------------------------------------------------------------------------------
WHAT THIS FILE COMPUTES.  Exactly the pass-10 classification of the branch (the
b-4 barrier with the Turan cap e(H[C]) <= floor(|C|^2/3) on every component of
H - B, valid because H is K_4-free), with the Gallai term added to both sides of
the split.  Exact integer arithmetic; no floating-point value enters a
comparison.  Z(29) = 8281 is Hill's number, an UPPER bound on cr(K_29) (Hill's drawing is
explicit), which is the direction needed here.

THE EXCLUSION THRESHOLD IS >=, NOT >.  A counterexample satisfies
cr(G) < cr(K_29) <= Z(29) = 8281, and both are integers, so cr(G) <= 8280.  A
lower bound of exactly 8281 is therefore already a contradiction, and a class is
excluded as soon as its split bound reaches Z, not only when it passes Z.  The
earlier files in this directory use the weaker test "excluded when > Z"; that is
conservative, so nothing closed there is reopened, but one class here (b = 30 at
m = 840) lands exactly on 8281 and needs the correct threshold.
"""
import recursive as R
import verify_range as V
from order2r import L, configs, RCHI, Z

r = RCHI
n = 2 * r


def maxgallai(p, q):
    """Max edges of a Gallai forest on p vertices with all blocks of order <= q."""
    if p <= 1 or q <= 1:
        return 0
    s = p - 1
    k = s // (q - 1)
    rem = s - k * (q - 1)
    return k * (q * (q - 1) // 2) + (rem + 1) * rem // 2


def forced_clique(p, e, qmax):
    """Smallest q with maxgallai(p,q) >= e, i.e. a Gallai forest on p vertices
    with e edges must contain a block of order >= q.  None if e exceeds
    maxgallai(p,qmax), which means no such Gallai forest exists at all."""
    if e <= 0:
        return 1
    for q in range(2, qmax + 1):
        if maxgallai(p, q) >= e:
            return q
    return None


def turan_cap(s):
    """Max edges of a K_4-free graph on s vertices (Turan)."""
    return s * s // 3


def branch_survivors(m, use_gallai=True, verbose_b=None):
    """Classify the K_4-free / two-disjoint-triangle branch at order 2r."""
    X = 2 * m - n * (r - 1)
    eH = n * (n - 1) // 2 - m
    live = []
    detail = []
    for b in range(6, n + 1):
        nodd = b - 4
        if n - b < nodd:
            continue
        free = r + 3 - b          # K_4-free sharpening, see the docstring
        for c in configs(n - b, nodd, free, X):
            D = sum(c)
            CB = b * (b - 1) // 2
            CD = D * (D - 1) // 2
            if V.best_bipartition(list(c)) > Z:
                continue
            if len(c) >= r:
                continue
            Ymin = sum(s * max(0, r + 3 - s - b) for s in c)
            Pmin = sum(s - 1 for s in c)
            # K_4-free Turan cap, never above the trivial complete-graph cap
            Pmax = sum(min(turan_cap(s), s * (s - 1) // 2) for s in c)
            if Pmax < Pmin:
                continue
            best, bestwit = None, None
            for Y in range(Ymin, X + 1):
                Q = min(CB, Pmax - D * r + Y + eH)
                if Q < 6:               # B contains two disjoint triangles
                    continue
                P = D * r - Y - eH + Q
                if not (Pmin <= P <= Pmax):
                    continue
                eB, eD = CB - Q, CD - P
                crD = max(V.crK(len(c)), L(D, eD), V.best_bipartition(list(c)))
                crB = L(b, eB) if eB > 0 else 0
                wit = None
                if use_gallai:
                    # low vertices and their guaranteed edges
                    pB, pD = b - (X - Y), D - Y
                    eLB = eB - (X - Y) * (b - 1)
                    eLD = eD - Y * (D - 1)
                    qB = forced_clique(pB, eLB, r) if pB >= 2 else 1
                    qD = forced_clique(pD, eLD, r) if pD >= 2 else 1
                    if qB is None or qD is None:
                        continue        # no Gallai forest with that many edges
                    crB = max(crB, V.crK(qB))
                    crD = max(crD, V.crK(qD))
                    wit = (Y, Q, P, pB, eLB, qB, pD, eLD, qD)
                t = crD + crB
                if best is None or t < best:
                    best, bestwit = t, (wit if wit else (Y, Q, P))
            if best is None:
                continue
            if b == verbose_b:
                detail.append((b, tuple(sorted(c, reverse=True)), best, bestwit))
            if best < Z:
                live.append((b, tuple(sorted(c, reverse=True)), best))
    return live, detail


def main():
    print("Albertson order 58 at r = 29: the last branch (H K_4-free with two")
    print("disjoint triangles), closed by Gallai low-vertex blocks.")
    print("Z(%d) = %d   (Hill's number, an upper bound on cr(K_%d))" % (r, Z, r))
    print()

    print("PART 1   maximum edges of a Gallai forest, and what 377 edges force")
    print("   A low vertex has d_G = r-1 = %d, so every clique block through it" % (r - 1))
    print("   has order <= r = %d." % r)
    for q in (15, 20, 25, 27, 28, 29):
        print("      maxgallai(30, %2d) = %3d" % (q, maxgallai(30, q)))
    print("   So a Gallai forest on 30 vertices with more than %d edges must"
          % maxgallai(30, 27))
    print("   contain a clique block of order >= 28, worth cr(K_28) = %d."
          % V.crK(28))
    print()

    print("PART 2   the branch WITHOUT the Gallai term (the pass-10 state)")
    for m in (838, 839, 840):
        live, _ = branch_survivors(m, use_gallai=False)
        print("   m=%d: %d surviving classes %s"
              % (m, len(live), [(b, c, v) for b, c, v in live]))
    print()

    print("PART 3   the same branch WITH the Gallai term")
    allclosed = True
    for m in (838, 839, 840):
        live, _ = branch_survivors(m, use_gallai=True)
        print("   m=%d: %d surviving classes %s"
              % (m, len(live), live if live else "-> BRANCH IMPOSSIBLE"))
        if live:
            allclosed = False
    print()

    print("PART 4   the b = 30 class in detail, at m = 838")
    _, det = branch_survivors(838, use_gallai=True, verbose_b=30)
    for b, c, best, wit in det:
        Y, Q, P, pB, eLB, qB, pD, eLD, qD = wit
        print("   c=%s  minimiser Y=%d, e(H[B])=%d, sum_C e(H[C])=%d"
              % (str(c[:3]) + ("+1^%d" % (len(c) - 3) if len(c) > 3 else ""),
                 Y, Q, P))
        print("      B: %d low vertices carry >= %d edges -> clique K_%d, cr = %d"
              % (pB, eLB, qB, V.crK(qB)))
        print("      D: %d low vertices carry >= %d edges -> clique K_%d, cr = %d"
              % (pD, eLD, qD, V.crK(qD)))
        print("      split bound %d against Z(29) = %d" % (best, Z))
    print()

    if allclosed:
        print("CONCLUSION")
        print("   The last branch of order 58 is impossible, so with height 2933")
        print("   (H has a K_4) and order2r.py PART 3 (H has no two disjoint")
        print("   triangles) ORDER 58 AT r = 29 IS IMPOSSIBLE OUTRIGHT.")
        print("   Remaining for r = 29: the three order-57 rows 826, 827, 828.")
    else:
        print("CONCLUSION")
        print("   The Gallai term does not close the branch; classes survive above.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Gallai low-vertex block packing at the surviving Albertson r=27 row (53,713).

Setting (from the preceding contribution, ledger height 2623).  G is 27-critical,
|G| = 53 = 2r-1, e(G) = 713, cr(G) < cr(K_27), H = complement(G) is connected and
factor-critical, and the unique surviving configuration is

    B = T u {s}   (|B| = 4, T a triangle of H),
    H - B = C  u  {w1}  u  {w2},   |C| = 47,

with N_H(wi) contained in B, d_H(wi) = 1 + |N_T(wi)| in {2,3,4}.

Write x_v = d_G(v) - (r-1) = 26 - d_H(v) >= 0, so sum_v x_v = 2m - n(r-1) = 48,
and x_{wi} = 26 - d_H(wi) in {22,23,24}.

Since H-edges from wi go only into B, each wi is G-adjacent to every vertex of C
and to the other wj.  Let L be the subgraph of G induced by the LOW vertices
(x_v = 0).  Gallai's low-vertex theorem: in a k-critical graph the vertices of
degree k-1 induce a Gallai forest, i.e. every block is a clique or an odd cycle.
  Gallai, Kritische Graphen II (1963); modern statement Thm 1.3 of
  Kostochka-Rabern-Stiebitz.

Facts used, all proved in README.md:
  (F1) w1, w2 are not low, so V(L) is inside C u B and |V(L)| = 53 - |R| where
       R is the set of high vertices (which contains w1 and w2).
  (F2) block sizes are at most 25: a block of size >= 5 meets C (|B| = 4), and a
       low vertex of C has 26 = d_G >= (|Q|-1) + |{w1,w2}|.
  (F3) at most one block of size 25: its >= 21 vertices in C are saturated, so
       every vertex outside the block and outside {w1,w2} is H-adjacent to all of
       them; two such blocks leave at least one vertex with d_H >= 42 > 26, and
       they cannot share a cut vertex (that vertex would have 48 neighbours in L).
  (F4) a size-25 block cannot lie wholly inside C: with w1, w2 it would be a K_27
       in G, giving cr(G) >= cr(K_27).
  (F5) the exact degree identity
           e(L) = m - sum_{v in R} d_G(v) + e(G[R]) = 665 - 26|R| + e(G[R]),
       with 1 <= e(G[R]) <= C(|R|,2), the 1 because w1w2 is a G-edge.

Exact integer arithmetic only.
"""

N, R_CHI, M = 53, 27, 713
X = 2 * M - N * (R_CHI - 1)          # 48
MAXBLK = 25                          # (F2)


def f(u):
    """Most edges a block with |Q| - 1 = u can have: a clique.  An odd cycle of
    length u+1 has only u+1 edges, which is smaller for u >= 2."""
    return u * (u + 1) // 2


def max_edges(U, cap, specials):
    """Maximum of sum f(u_i) over compositions of U into parts u_i >= 1 with
    u_i <= cap, where at most `specials` parts may equal cap and the rest are
    at most cap-1.  (U = |V(L)| - c, maximised at c = 1.)"""
    NEG = -1
    best = [[NEG] * (specials + 1) for _ in range(U + 1)]
    best[0][specials] = 0
    for tot in range(U + 1):
        for sp in range(specials + 1):
            if best[tot][sp] < 0:
                continue
            for u in range(1, min(cap, U - tot) + 1):
                if u == cap:
                    if sp == 0:
                        continue
                    ns = sp - 1
                else:
                    ns = sp
                v = best[tot][sp] + f(u)
                if v > best[tot + u][ns]:
                    best[tot + u][ns] = v
    return max(best[U])


def analyse():
    print("Gallai low-vertex block packing at (n, m) = (%d, %d), r = %d" % (N, M, R_CHI))
    print("sum_v x_v = %d ; x_{wi} in {22,23,24} ; |C| = 47, |B| = 4" % X)
    print()
    print(" |R|  |V(L)|   e(L) range      pack(<=25,one)  pack(<=24)  pack(25+<=23)  verdict")
    survivors = []
    for Rsz in range(2, 8):
        # feasibility: R = {w1,w2} u (other high vertices, each x >= 1);
        # x_{w1}+x_{w2} >= 44, so at most 4 other high vertices.
        others = Rsz - 2
        if others < 0 or others > X - 44:
            continue
        VL = N - Rsz
        U = VL - 1                                   # c = 1 maximises U
        eL_lo = 665 - 26 * Rsz + 1
        eL_hi = 665 - 26 * Rsz + Rsz * (Rsz - 1) // 2
        p_all = max_edges(U, MAXBLK - 1, 1)          # at most one part = 24
        p_no25 = max_edges(U, MAXBLK - 2, U)         # no part = 24  (no K_25)
        p_no24 = max_edges(U, MAXBLK - 1, 1)         # placeholder, refined below
        # "one K_25 but no K_24": one part = 24, all others <= 22
        NEG = -1
        best = [NEG] * (U + 1)
        best[0] = 0
        for tot in range(U + 1):
            if best[tot] < 0:
                continue
            for u in range(1, min(MAXBLK - 3, U - tot) + 1):   # u <= 22
                if best[tot] + f(u) > best[tot + u]:
                    best[tot + u] = best[tot] + f(u)
        p_25_no24 = max(best[t] + f(24) for t in range(U - 24 + 1) if best[t] >= 0) \
            if U >= 24 else -1

        verdict = None
        if eL_lo > p_all:
            verdict = "IMPOSSIBLE (packing)"
        elif eL_lo > p_no25 and eL_lo > p_25_no24 and eL_hi < f(24) + f(23):
            verdict = ("IMPOSSIBLE (K_25 and K_24 both forced, disjoint, "
                       "%d > %d)" % (f(24) + f(23), eL_hi))
        else:
            verdict = "survives"
            survivors.append(Rsz)
        print("  %2d    %3d    [%3d, %3d]      %6d        %6d      %6d       %s"
              % (Rsz, VL, eL_lo, eL_hi, p_all, p_no25, p_25_no24, verdict))
    print()
    print("surviving |R|: %s" % survivors)
    if survivors:
        print("=> at (53,713) the counterexample has at least %d high vertices"
              " besides w1 and w2." % (min(survivors) - 2))
    else:
        print("=> the row (53,713) is ELIMINATED.")
    return survivors


if __name__ == "__main__":
    analyse()

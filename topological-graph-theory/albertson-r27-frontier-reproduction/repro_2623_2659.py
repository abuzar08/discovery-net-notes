"""Clean-room reproduction of the computational content of Discovery Net
heights 2623 and 2659 (researcher-2), from the primary papers.

Checked here, in this file's own code:

  1. Cranston arXiv:2512.08020 Lemma E, as an edge floor for r-critical graphs
     with no TK_r: e >= n(r-1)/2 + (r-3), no restriction on n.  Quoted verbatim
     from the paper (see README); applied at r = 27..30.
  2. The floor/ceiling table of height 2623 claim 2 and claim 3, with the
     ceiling computed by MY recursive integer-aware sampling bound
     (recursive_sampling.py, height 2617/2649), which uses a different set of
     published base bounds from researcher-2's implementation.
  3. Step 4 of height 2659: the excess bookkeeping that turns
     d_H(w1) + d_H(w2) <= 5 into |R| in {2,3}.
  4. Step 5 of height 2659: the Gallai block-packing maxima 582 and 579, and
     the forced edge counts e(L) = 614 and e(L) >= 588.

Standard library only, exact integer arithmetic.
"""
from math import comb

from recursive_sampling import build

Z = lambda r: ((r // 2) * ((r - 1) // 2) * ((r - 2) // 2) * ((r - 3) // 2)) // 4

FAIL = []


def check(name, got, want):
    ok = got == want
    print(f"  [{'ok ' if ok else 'FAIL'}] {name}: {got}"
          + ("" if ok else f"   expected {want}"))
    if not ok:
        FAIL.append(name)


# ------------------------------------------------------------------ floors

def lemma_E_floor(r, n):
    """Cranston Lemma E = Barat-Toth Corollary 7 = Sadhu Lemma 2.5:
    an r-critical graph with no TK_r has e >= n(r-1)/2 + (r-3)."""
    num = n * (r - 1) + 2 * (r - 3)          # = 2 * (n(r-1)/2 + (r-3))
    return -((-num) // 2)                    # ceiling of num/2


def kostochka_yancey_floor(r, n):
    """Sadhu Lemma 2.4 (Kostochka-Yancey): 2m >= ((r+1)(r-2)n - r(r-3))/(r-1)."""
    num = (r + 1) * (r - 2) * n - r * (r - 3)
    half = -((-num) // (r - 1))              # ceil of num/(r-1)  = 2m bound
    return -((-half) // 2)


# ----------------------------------------------------------- Gallai packing

def gallai_max_edges(N, max_clique, max_one_of_max=True):
    """Maximum number of edges of a Gallai forest on N vertices: a graph whose
    blocks are complete graphs (order <= max_clique, at most one of exactly
    max_clique when max_one_of_max) or odd cycles (order >= 5, odd).

    A connected block graph on N vertices with blocks of orders b_1..b_k
    satisfies sum(b_i - 1) = N - 1; disconnecting only loses edges.  So this is
    a knapsack over block orders with weight b-1 and value C(b,2) for cliques,
    b for odd cycles.
    """
    items = []                                # (weight, value, is_max_clique)
    for b in range(2, max_clique + 1):
        items.append((b - 1, comb(b, 2), b == max_clique))
    for b in range(5, N + 1, 2):              # odd cycle blocks
        items.append((b - 1, b, False))
    W = N - 1
    NEG = -1
    # dp[w][used_max] = best value with total weight w
    dp = [[NEG] * 2 for _ in range(W + 1)]
    dp[0][0] = 0
    for w in range(W + 1):
        for u in (0, 1):
            if dp[w][u] == NEG:
                continue
            for (wt, val, ismax) in items:
                if w + wt > W:
                    continue
                nu = u
                if ismax and max_one_of_max:
                    if u == 1:
                        continue
                    nu = 1
                if dp[w + wt][nu] < dp[w][u] + val:
                    dp[w + wt][nu] = dp[w][u] + val
    return max(dp[W][0], dp[W][1])


# ------------------------------------------------------------------- main

def main():
    r = 27
    print("1. Cranston Lemma E floors (= Barat-Toth Cor. 7 = Sadhu Lemma 2.5)")
    check("floor(27, 53)", lemma_E_floor(27, 53), 713)
    check("floor(27, 54)", lemma_E_floor(27, 54), 726)
    check("floor(28, 55)", lemma_E_floor(28, 55), 768)
    check("floor(29, 57)", lemma_E_floor(29, 57), 824)
    check("floor(30, 59)", lemma_E_floor(30, 59), 883)
    print("   Kostochka-Yancey floors quoted at height 2623:")
    check("KY(27, 53)", kostochka_yancey_floor(27, 53), 701)
    check("KY(28, 55)", kostochka_yancey_floor(28, 55), 755)
    check("KY(29, 57)", kostochka_yancey_floor(29, 57), 811)
    check("KY(30, 59)", kostochka_yancey_floor(30, 59), 869)

    print("\n2. Ceilings from MY independent recursive bound")
    L = build(59)
    def ceiling(rr, n):
        """largest m with L(n,m) < Z(rr); m above it is closed"""
        z = Z(rr)
        hi = comb(n, 2)
        best = -1
        for m in range(hi + 1):
            if L[n][m] < z:
                best = m
        return best
    check("ceiling(27, 54)", ceiling(27, 54), 724)
    check("L(54,725) >= Z(27)", L[54][725] >= Z(27), True)
    check("L(54,725)", L[54][725], 6106)
    check("ceiling(27, 53)", ceiling(27, 53), 713)
    check("L(53,713) gap to Z(27)", Z(27) - L[53][713], 13)
    print("   n=54: floor 726 > ceiling 724  =>  ORDER 54 IMPOSSIBLE  "
          f"({lemma_E_floor(27,54) > ceiling(27,54)})")
    print("   n=53: floor 713 = ceiling 713  =>  a single row (53,713)  "
          f"({lemma_E_floor(27,53) == ceiling(27,53)})")

    print("\n   the r = 28..30 lines of height 2623 claim 3")
    for (rr, n, ceil_want, gaps_want) in [
            (28, 55, 769, [38, 6]),
            (29, 57, 828, [150, 117, 83, 49, 15]),
            (30, 59, 888, [200, 164, 127, 91, 54, 18])]:
        c = ceiling(rr, n)
        lo = lemma_E_floor(rr, n)
        gaps = [Z(rr) - L[n][m] for m in range(lo, c + 1)]
        check(f"ceiling({rr}, {n})", c, ceil_want)
        check(f"gaps({rr}, {n}) over m = {lo}..{c}", gaps, gaps_want)

    print("\n3. Step 4 bookkeeping of height 2659")
    n, m = 53, 713
    total_excess = 2 * m - n * (r - 1)
    check("sum of excesses 2m - n(r-1)", total_excess, 48)
    dH_sum_max = 5                                   # d_H(w1) + d_H(w2) <= 5
    x_w = (n - 1) * 2 - 26 * 2 - dH_sum_max          # x_v = 26 - d_H(v)
    check("x_{w1} + x_{w2} >= 52 - 5", x_w, 47)
    check("excess left for other vertices", total_excess - x_w, 1)
    print("   => at most one further vertex has positive excess, so |R| in {2,3}")

    print("\n4. Step 5 of height 2659: forced e(L) and Gallai packing maxima")
    for R in (2, 3):
        eL = m - (26 * R + total_excess) + (1 if R == 2 else 1)
        check(f"e(L) for |R| = {R}   (= 665 - 26|R| + e(G[R]), e(G[R]) >= 1)",
              eL, 614 if R == 2 else 588)
    check("Gallai max edges, 51 vertices, clique blocks <= 25, one 25",
          gallai_max_edges(51, 25), 582)
    check("Gallai max edges, 50 vertices, clique blocks <= 25, one 25",
          gallai_max_edges(50, 25), 579)
    print("   |R|=2: e(L) = 614 > 582  -> contradiction")
    print("   |R|=3: e(L) >= 588 > 579 -> contradiction")
    print("   (without the 'at most one block of order 25' restriction the "
          f"maxima would be {gallai_max_edges(51,25,False)} and "
          f"{gallai_max_edges(50,25,False)}, so that restriction is essential)")

    print()
    if FAIL:
        print("FAILED:", FAIL)
        return 1
    print("every checked value of heights 2623 and 2659 reproduces")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

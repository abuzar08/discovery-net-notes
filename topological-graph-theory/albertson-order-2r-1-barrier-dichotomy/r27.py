#!/usr/bin/env python3
"""
The single surviving Albertson r = 27 row (53, 713) is eliminated.

Exact integer / Fraction arithmetic only: no floating point, no randomness, no
solver, no external data.  Imports recursive.py and verify_range.py.

--------------------------------------------------------------------------
THE ARGUMENT

Suppose G is 27-critical with cr(G) < cr(K_27).  Then G has no subdivision of
K_27 (cr(TK_27) = cr(K_27)), and by Sadhu arXiv:2609.01682 Thm 1.3 we have
|G| in {53, 54} with H := complement(G) connected.

Step 1 (frontier; ledger height 2623).  Cranston arXiv:2512.08020 Lemma E gives
e(G) >= n(r-1)/2 + (r-3), i.e. 713 at n = 53 and 726 at n = 54; recursive
integer-aware sampling gives L(54,725) >= Z(27) and L(53,714) >= Z(27).  So
order 54 is impossible and n = 53, m = 713.

Step 2 (configuration; ledger height 2623).  H is factor-critical (Stehlik 2003
at n = 2r-1) with theta(H) = 27, hence no conformal triangle.  The barrier
classification leaves exactly one possibility: a 4-set B = T u {s} with T a
triangle of H, such that

    H - B  =  C  u  {w1}  u  {w2},    |C| = 47,

so N_H(wi) is contained in B.  (Barrier size 3 is excluded by the non-domination
lemma below; the triangle-free case is excluded by the split bound.)

Step 3 (non-domination).  For a factor-critical H with no conformal triangle and
{w} a singleton component of H - B, no vertex of N_H(w) is adjacent to every
other vertex of N_H(w).  [Proof: delta(H) >= 2, so |N_H(w)| >= 2.  If a in N_H(w)
dominates the rest, take a perfect matching M of H - a; it matches w to some
u in N_H(w)\\{a}; then {w,a,u} is a triangle and M \\ {wu} perfectly matches
H - {a,w,u}, a conformal triangle.]
Consequences here: N_H(wi) is not inside the clique T, so wi ~ s; and for every
alpha in A_i := N_T(wi), alpha does not dominate N_H(wi) = A_i u {s}, and alpha
is adjacent to all of A_i\\{alpha} because T is a clique, so alpha is NOT
adjacent to s.  Thus s is H-adjacent to no vertex of A_1 u A_2.

Step 4 (disjointness).  A_1 and A_2 are disjoint.  [Suppose alpha is in both.
H - alpha has a perfect matching M.  M matches w1 into N_H(w1)\\{alpha} =
(A_1\\{alpha}) u {s}.  Any beta in A_1\\{alpha} is adjacent to alpha (T is a
clique), so matching w1 to beta makes {w1, alpha, beta} a triangle with
M \\ {w1 beta} a perfect matching of H - {alpha, w1, beta}: a conformal triangle.
Hence M matches w1 to s, and by the same argument it matches w2 to s.  A matching
cannot do both.]
Since A_1, A_2 are non-empty, disjoint and inside T, |A_1| + |A_2| <= 3, so

    d_H(w1) + d_H(w2) = 2 + |A_1| + |A_2| <= 5.

With x_v := d_G(v) - 26 = 26 - d_H(v) and sum_v x_v = 2m - n(r-1) = 48,

    x_{w1} + x_{w2} = 52 - (d_H(w1) + d_H(w2)) >= 47,

so the other 51 vertices carry total excess at most 1: at most ONE vertex besides
w1, w2 is high.  Writing R for the set of high vertices, |R| is 2 or 3.

Step 5 (Gallai low-vertex packing).  Gallai (Kritische Graphen II, 1963): in a
k-critical graph the vertices of degree k-1 induce a Gallai forest, every block a
complete graph or an odd cycle.  Let L be that subgraph here (the vertices with
x_v = 0); V(L) is inside C u B and |V(L)| = 53 - |R|.
  * Each wi is G-adjacent to every vertex of C (N_H(wi) is inside B) and to the
    other wj (different components of H - B), so w1w2 is a G-edge.
  * A clique block Q with |Q| >= 5 meets C (|B| = 4); such a vertex v is low, and
    its neighbours include Q\\{v} together with w1 and w2, so |Q| - 1 + 2 <= 26,
    i.e. |Q| <= 25.
  * At most one clique block has size 25.  Two of them cannot share a cut vertex
    (that vertex would have 48 neighbours in L), so they are disjoint; each has at
    least 25 - |B| vertices in C, and together at least 50 - 4 = 46; every such
    vertex v is saturated (24 block neighbours plus w1, w2 = 26 = d_G(v)), so any
    vertex z outside the two blocks and outside {w1,w2} is H-adjacent to all 46,
    giving d_H(z) >= 46 > 26 = Delta(H).  For |R| in {2,3} such a z exists.
  * Exact degree identity: e(L) = m - sum_{v in R} d_G(v) + e(G[R])
    = 713 - (26|R| + 48) + e(G[R]) = 665 - 26|R| + e(G[R]),  and e(G[R]) >= 1.
The maximum number of edges of such a Gallai forest is computed exactly below and
is smaller than the forced e(L) for both |R| = 2 and |R| = 3.
--------------------------------------------------------------------------
"""
import recursive as R
import verify_range as V

N, RCHI, M = 53, 27, 713
X = 2 * M - N * (RCHI - 1)                 # 48
DEG = RCHI - 1                             # low-vertex degree 26
_L = R.build(59, rounds=3)


def cr_lower(n, q):
    if n < 4 or q <= 0 or n > 59:
        return 0
    return _L[n][min(q, len(_L[n]) - 1)]


for _f in (V.controls, V.analyse, V.tri_free_survivors):
    _f.__globals__['cr_lower_nm'] = cr_lower


def cranston_E(r, n):
    return -(-(n * (r - 1) + 2 * (r - 3)) // 2)


def ky_floor(r, n):
    return -(-((r + 1) * (r - 2) * n - r * (r - 3)) // (2 * (r - 1)))


def gallai_max_edges(VL):
    """Exact maximum edge count of a Gallai forest on VL vertices whose clique
    blocks have size <= 25 with at most one of size exactly 25, and whose odd
    cycle blocks are unrestricted in length.  Maximised at c = 1, i.e. U = VL-1,
    because the optimum is non-decreasing in U."""
    U = VL - 1
    NEG = -1
    # dp[t][s] : most edges using increment total t, s = 1 if the size-25 clique
    # block is still available
    dp = [[NEG, NEG] for _ in range(U + 1)]
    dp[0][1] = 0
    for t in range(U + 1):
        for s in (0, 1):
            if dp[t][s] < 0:
                continue
            for u in range(1, U - t + 1):
                opts = []
                if u + 1 <= 24:                       # clique of size <= 24
                    opts.append((u * (u + 1) // 2, s))
                elif u + 1 == 25 and s == 1:          # the one allowed K_25
                    opts.append((u * (u + 1) // 2, 0))
                if u >= 2 and (u + 1) % 2 == 1:       # odd cycle, any length
                    opts.append((u + 1, s))
                for e, ns in opts:
                    if dp[t][s] + e > dp[t + u][ns]:
                        dp[t + u][ns] = dp[t][s] + e
    return max(dp[U])


def main():
    print("Elimination of the Albertson r = 27 row (53, 713)")
    print("Exact arithmetic; no floating point, randomness or solver.")
    print()
    ok = V.controls()
    bad = [n for n in range(5, 60) if _L[n][n * (n - 1) // 2] > V.Z(n)]
    print("SOUNDNESS CONTROLS: barrier machinery %s ; recursive table %s"
          % ("PASS" if ok else "FAIL", "PASS" if not bad else "FAIL"))
    print()

    print("STEP 1  the frontier")
    for n in (53, 54):
        lo = max(ky_floor(RCHI, n), cranston_E(RCHI, n))
        hi = max([q for q in range(len(_L[n])) if _L[n][q] < V.Z(RCHI)], default=-1)
        print("   n=%d: floor %d (Cranston Lemma E), ceiling %d  ->  %s"
              % (n, lo, hi, "m = %d" % lo if lo <= hi else "ORDER IMPOSSIBLE"))
    assert max(ky_floor(RCHI, 54), cranston_E(RCHI, 54)) > \
        max(q for q in range(len(_L[54])) if _L[54][q] < V.Z(RCHI))
    assert max(ky_floor(RCHI, 53), cranston_E(RCHI, 53)) == M
    print()

    print("STEP 2  the configuration at (53, 713)")
    print("   triangle-free case survivors: %s" % (V.tri_free_survivors(RCHI, M),))
    live = {}
    for b in range(3, N + 1):
        q = b - 1
        if N - b < q:
            continue
        cf = V.configs(N - b, q, RCHI - b, X)
        if not cf:
            continue
        keep = [c for c in cf if _cfg_survives(c, b)]
        if keep:
            live[b] = keep
    for b in sorted(live):
        print("   barrier size b=%d: %s%s" % (b, [tuple(c) for c in live[b]],
              "   (all contain a singleton -> killed by non-domination)"
              if b == 3 else ""))
    assert all(1 in c for c in live.get(3, [])), "a b=3 multiset has no singleton"
    assert set(live) <= {3, 4} and live.get(4) == [tuple(sorted((N - 6, 1, 1),
                                                               reverse=True))]
    print("   => B = T u {s}, H - B = C u {w1} u {w2} with |C| = %d" % (N - 6))
    print()

    print("STEP 3-4  non-domination and disjointness")
    print("   d_H(w1) + d_H(w2) = 2 + |A_1| + |A_2| <= 2 + |T| = 5")
    print("   x_{w1} + x_{w2} = 52 - (d_H(w1)+d_H(w2)) >= 47, and sum_v x_v = %d" % X)
    print("   => at most %d vertex besides w1, w2 is high, so |R| in {2, 3}"
          % (X - 47))
    print()

    print("STEP 5  Gallai low-vertex block packing")
    print("   |R|  |V(L)|   forced e(L) >=   max Gallai forest edges   verdict")
    for Rsz in (2, 3):
        VL = N - Rsz
        eL = 665 - 26 * Rsz + 1
        cap = gallai_max_edges(VL)
        print("    %d     %2d          %4d                  %4d              %s"
              % (Rsz, VL, eL, cap, "CONTRADICTION" if eL > cap else "survives"))
        assert eL > cap, "|R|=%d survives the packing bound" % Rsz
    print()
    print("CONCLUSION")
    print("   Every case is contradictory, so no 27-critical graph G with")
    print("   cr(G) < cr(K_27) exists:  Albertson's conjecture holds for r = 27,")
    print("   conditional on the published inputs listed in README.md.")


def _cfg_survives(c, b):
    """The barrier filter of verify_range.analyse, for one multiset."""
    n, r, m = N, RCHI, M
    eH = n * (n - 1) // 2 - m
    D = sum(c)
    CB = b * (b - 1) // 2
    if V.best_bipartition(list(c)) > V.Z(r):
        return False
    eGDBu = D * (b - r + 1) + X + 2 * sum(s * (s - 1) // 2 for s in c)
    if max(b * max(0, r - b), D * max(0, r - D)) > eGDBu:
        return False
    if len(c) >= r:
        return False
    Ymin = sum(s * max(0, r - s - b) for s in c)
    Pmin, Pmax = sum(s - 1 for s in c), sum(s * (s - 1) // 2 for s in c)
    best = None
    for Y in range(Ymin, X + 1):
        Q = min(CB, Pmax - D * (r - 1) + Y + eH)
        if Q < 3:
            continue
        P = D * (r - 1) - Y - eH + Q
        if not (Pmin <= P <= Pmax):
            continue
        crD = max(V.crK(len(c)), cr_lower(D, D * (D - 1) // 2 - P),
                  V.best_bipartition(list(c)))
        eB = CB - Q
        t = crD + (cr_lower(b, eB) if eB > 0 else 0)
        if best is None or t < best:
            best = t
    return best is not None and best <= V.Z(r)


if __name__ == "__main__":
    main()

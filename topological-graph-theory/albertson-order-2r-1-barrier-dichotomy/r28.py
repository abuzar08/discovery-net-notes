#!/usr/bin/env python3
"""
Albertson's conjecture for r = 28.

Exact integer / Fraction arithmetic only.  Imports recursive.py and
verify_range.py.  This argument does NOT use the r = 27 result: it is
independent of it.

--------------------------------------------------------------------------
A graph with chi >= 28 contains a 28-critical subgraph, whose crossing number is
no larger, so it suffices to treat 28-critical G with cr(G) < cr(K_28).  Such a G
has no subdivision of K_28, since cr(TK_28) = cr(K_28).  Cranston's order bounds
are stated for a MINIMUM counterexample, so fix G of minimum order among the
28-critical counterexamples; ruling out every order rules out all of them.

PART A -- the order is 55.
  Orders <= r+4 = 32 carry a TK_r (Cranston Lemma C); orders 35..49 and >= 79 are
  excluded by Cranston; every remaining order whose edge floor exceeds its
  recursive-sampling ceiling is excluded here.  That leaves 33, 34, 50..55.
  For n <= 2r-2 = 54 the complement is disconnected (Gallai; Sadhu Lemma 2.8),
  so V(G) splits into the components V_1..V_t of the complement, distinct parts
  complete to each other, G[V_i] r_i-critical, sum r_i = 28, |V_i| >= 2 r_i - 1
  (Gallai, applicable since complement(G_i) is that component).  A part with
  r_i = 2 would be K_2, whose complement is disconnected, so every part has
  r_i = 1 with v_i = 1, or r_i >= 3 with v_i >= 2 r_i - 1.
    * Edge budget: e(G) = e(M) + sum_i e(G_i) with M the complete multipartite
      graph on the parts, so e(M) + sum_i (edge floor)_i <= m.
    * Subdivision transfer: if every G_i had a TK_{r_i}, joining them would give
      a TK_28 in G (branch vertices in different parts are adjacent, internal
      path vertices stay inside their part).  So some G_j has none, and Cranston
      Lemma E applies to it.  Parts with r_j <= 3 always have a TK_{r_j} (K_1;
      a 3-critical graph is an odd cycle, which is a TK_3), so r_j >= 4.
  No decomposition of any n <= 54 survives, so n = 55 = 2r-1 and m in {768,769}.

PART B -- both rows at n = 55 are impossible.
  At n = 2r-1 the complement H is factor-critical (Stehlik 2003) with
  theta(H) = 28, hence no conformal triangle.  The barrier classification leaves
  one configuration: B = T u {s} with T a triangle of H, and
  H - B = C u {w1} u {w2} with |C| = 49 and N_H(wi) inside B.
  Non-domination (no vertex of N_H(w) dominates the rest of N_H(w)) gives
  wi ~ s and s adjacent to no vertex of A_i := N_T(wi); disjointness of A_1, A_2
  gives d_H(w1) + d_H(w2) <= 5, so with x_v = d_G(v) - 27 = 27 - d_H(v) and
  sum_v x_v = 2m - 55*27,
      x_{w1} + x_{w2} >= 54 - 5 = 49,
  leaving at most 2 (m = 768) or 4 (m = 769) units of excess elsewhere, so the
  high-vertex set R has |R| <= 4 resp. 6.
  Gallai's low-vertex theorem then bounds e(L) for the Gallai forest L induced by
  the vertices with x_v = 0, against the exact identity
      e(L) = m - (27|R| + sum_v x_v) + e(G[R]).
  Each case falls either to the packing capacity or to the split bound
  cr(G) >= sum_i crK(|Q_i|) over the blocks of order >= 15, which are pairwise
  disjoint because a shared cut vertex would have >= 28 > 27 neighbours in L.
  The single tightest case (m = 769, |R| = 6) needs the exact count of e(G[R])
  recorded in eGR_min below.
--------------------------------------------------------------------------
"""
import recursive as R
import verify_range as V

RCHI = 28
N = 2 * RCHI - 1                 # 55
DEG = RCHI - 1                   # low-vertex degree 27
Z = V.Z(RCHI)
_L = R.build(79, rounds=3)


def L(n, q):
    if n < 4 or q <= 0 or n not in _L:
        return 0
    return _L[n][min(q, len(_L[n]) - 1)]


def ky(r, n):
    if r <= 1:
        return 0
    if r == 2:
        return 1
    return -(-((r + 1) * (r - 2) * n - r * (r - 3)) // (2 * (r - 1)))


def lemE(r, n):
    return -(-(n * (r - 1) + 2 * (r - 3)) // 2)


def floor_of(r, n):
    return max(ky(r, n), lemE(r, n))


def ceiling_of(n):
    return max([q for q in range(len(_L[n])) if _L[n][q] < Z], default=-1)


def open_orders():
    out = []
    for n in range(RCHI + 5, int(2.82 * RCHI) + 1):
        if 1.228 * RCHI <= n <= 1.768 * RCHI:
            continue
        lo, hi = floor_of(RCHI, n), ceiling_of(n)
        if lo <= hi:
            out.append((n, lo, hi))
    return out


def join_survivors(n, mhi):
    live = []

    def rec(rrem, vrem, minr, cur):
        if rrem == 0:
            if vrem != 0 or len(cur) < 2:
                return
            eM = (n * n - sum(v * v for _, v in cur)) // 2
            kys = sum(ky(ri, vi) for ri, vi in cur)
            deep = [(rj, vj) for rj, vj in cur if rj >= 4]
            if not deep:
                return                      # every part has a TK_{r_i}: TK_28 in G
            need = min(eM + kys - ky(rj, vj) + max(ky(rj, vj), lemE(rj, vj))
                       for rj, vj in deep)
            if need <= mhi:
                live.append((sorted(cur, reverse=True), eM, need))
            return
        for ri in range(minr, rrem + 1):
            if ri == 2:
                continue
            if ri == 1:
                if vrem >= 1:
                    rec(rrem - 1, vrem - 1, 1, cur + [(1, 1)])
                continue
            for vi in range(2 * ri - 1, vrem + 1):
                if ky(ri, vi) > mhi:
                    break
                rec(rrem - ri, vrem - vi, ri, cur + [(ri, vi)])
    rec(RCHI, n, 1, [])
    return live


def gallai_cap(VL, maxblk):
    """Most edges a Gallai forest on VL vertices can have when clique blocks have
    order <= maxblk with at most one of order exactly maxblk (odd cycle blocks
    unrestricted)."""
    U = VL - 1
    NEG = -1
    dp = [[NEG, NEG] for _ in range(U + 1)]
    dp[0][1] = 0
    for t in range(U + 1):
        for s in (0, 1):
            if dp[t][s] < 0:
                continue
            for u in range(1, U - t + 1):
                opts = []
                if u + 1 <= maxblk - 1:
                    opts.append((u * (u + 1) // 2, s))
                elif u + 1 == maxblk and s == 1:
                    opts.append((u * (u + 1) // 2, 0))
                if u >= 2 and (u + 1) % 2 == 1:
                    opts.append((u + 1, s))
                for e, ns in opts:
                    if dp[t][s] + e > dp[t + u][ns]:
                        dp[t + u][ns] = dp[t][s] + e
    return max(dp[U])


def min_split(NL, eL_lo):
    best = [None]

    def rec(rem, cap, edges, cliques):
        if rem == 0:
            if edges >= eL_lo:
                s = sum(V.crK(b) for b in cliques if b >= 15)
                if best[0] is None or s < best[0]:
                    best[0] = s
            return
        hi, r, c2 = edges, rem, cap
        while r > 0:
            t = min(c2, r)
            hi += t * (t + 1) // 2
            r -= t
        if hi < eL_lo:
            return
        for u in range(min(cap, rem), 0, -1):
            rec(rem - u, u, edges + u * (u + 1) // 2, cliques + [u + 1])
            if u >= 2 and (u + 1) % 2 == 1:
                rec(rem - u, u, edges + u + 1, cliques)
    for c in range(1, NL):
        rec(NL - c, NL - c, 0, [])
    return best[0]


def eGR_min(Rsz, tight):
    """Lower bound on e(G[R]) for the high-vertex set R = {w1,w2} u Z.

    Always: w1w2 is a G-edge.  A z in C is G-adjacent to both w1 and w2, because
    N_H(wi) lies inside B.  When `tight` (the case d_H(w1)+d_H(w2) = 5, so
    A_1 u A_2 = T and N_H(w1) u N_H(w2) = B), a z in T is H-adjacent to exactly
    one wi, hence G-adjacent to the other; z = s is H-adjacent to both, hence
    G-adjacent to neither; and s is G-adjacent to every vertex of T, since
    non-domination makes s H-adjacent to no vertex of T.  With sigma = 1 if s is
    one of the high vertices and tau the number of high vertices in T,
        e(G[R]) >= 1 + 2(|Z| - sigma - tau) + tau + sigma*tau.
    Minimising over sigma in {0,1} and tau in {0..3}."""
    nz = Rsz - 2
    if not tight:
        return 1
    best = None
    for sigma in (0, 1):
        for tau in range(0, min(3, nz - sigma) + 1):
            if sigma + tau > nz:
                continue
            v = 1 + 2 * (nz - sigma - tau) + tau + sigma * tau
            if best is None or v < best:
                best = v
    return best if best is not None else 1


def main():
    print("Albertson's conjecture for r = 28   (independent of the r = 27 result)")
    print("Exact arithmetic; Z(28) = %d >= cr(K_28)" % Z)
    print()
    print("SOUNDNESS CONTROLS: barrier machinery %s ; recursive table %s"
          % ("PASS" if V.controls() else "FAIL",
             "PASS" if not [n for n in range(5, 60)
                            if _L[n][n * (n - 1) // 2] > V.Z(n)] else "FAIL"))
    print()

    print("PART A   the order of a minimum counterexample")
    oo = open_orders()
    print("   orders left by Cranston's exclusions and the sampling ceiling:")
    for n, lo, hi in oo:
        print("      n=%2d   m in [%d, %d]" % (n, lo, hi))
    for n, lo, hi in oo:
        if n > 2 * RCHI - 2:
            continue
        live = join_survivors(n, hi)
        print("      n=%2d   Gallai join decompositions within the edge budget: %d %s"
              % (n, len(live), "-> ORDER IMPOSSIBLE" if not live else live))
        assert not live
    rows = [(n, lo, hi) for n, lo, hi in oo if n > 2 * RCHI - 2]
    assert len(rows) == 1 and rows[0][0] == N
    print("   => n = %d and m in [%d, %d]" % (N, rows[0][1], rows[0][2]))
    print()

    print("PART B   the rows at n = %d" % N)
    print("   m    |R|  |V(L)|  e(L) >=   Gallai cap   split bound   verdict")
    for m in range(rows[0][1], rows[0][2] + 1):
        X = 2 * m - N * DEG
        Rmax = 2 + (X - (2 * DEG - 5))
        for Rsz in range(2, Rmax + 1):
            tight = (X - (2 * DEG - 5)) == (Rsz - 2)   # all slack used by |Z| ones
            VL = N - Rsz
            eL = m - (DEG * Rsz + X) + eGR_min(Rsz, tight)
            cap = gallai_cap(VL, DEG - 1)
            sp = min_split(VL, eL)
            ok = eL > cap or (sp is not None and sp > Z)
            print("  %3d   %2d    %3d     %4d       %5d        %6s      %s"
                  % (m, Rsz, VL, eL, cap, sp, "impossible" if ok else "SURVIVES"))
            assert ok, "case m=%d |R|=%d survives" % (m, Rsz)
    print()
    print("CONCLUSION")
    print("   No 28-critical G has cr(G) < cr(K_28):  Albertson's conjecture")
    print("   holds for r = 28, conditional on the published inputs in README.md.")


if __name__ == "__main__":
    main()

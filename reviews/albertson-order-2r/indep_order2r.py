"""reviewer-1: independent recomputation of the order-58 table of h2933.

Rebuilt from the mathematics, not from order2r.py:

  n = 2r, G r-critical, cr(G) < cr(K_r), H = complement connected.
  d_G(v) + d_H(v) = n-1, delta(G) >= r-1 (Dirac), so x_v := d_G(v)-(r-1)
  = r - d_H(v) >= 0 and X := sum_v x_v = 2m - n(r-1).
  In the surviving barrier class, w1 and w2 satisfy d_H(w1)+d_H(w2) <= 6,
  so x_{w1}+x_{w2} >= 2r-6 and any further vertex of R (the set of vertices
  of positive excess) costs at least 1, giving |R| <= 2 + (X - (2r-6)).
  L = G - R is contained in the low vertices, so by Gallai every block of L
  is a clique or an odd cycle, and
      e(L) = m - sum_{v in R} d_G(v) + e(G[R]) >= m - ((r-1)|R| + X) + e(G[R]).

Two independent bounds are then recomputed here:
  * the Gallai cap: the maximum number of edges of a graph on |V(L)| vertices
    all of whose blocks are cliques of order <= B or odd cycles.  Computed in
    two variants — with at most one block of order exactly B (the target's
    assumption, inherited from its order-(2r-1) argument) and with NO such
    restriction (weaker, so a safer check);
  * the split bound: min over such block structures achieving e(L) of
    sum of cr(K_b) over the clique blocks, using my own cr(K_q) lower bound
    (exact values for q <= 12 and the counting recursion).  Crossing number is
    additive over blocks, so this is a lower bound on cr(G); if it exceeds
    Z(r) >= cr(K_r) the row is impossible.

usage: python3 indep_order2r.py [r] [eGR_min]
"""
import sys
from functools import lru_cache

CR_EXACT = {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 3, 7: 9, 8: 18, 9: 36, 10: 60, 11: 100, 12: 150}


@lru_cache(maxsize=None)
def crK(q):
    """lower bound for cr(K_q): exact to 12 (Guy; Pan-Richter), then
    cr(K_q) >= ceil(q * cr(K_{q-1}) / (q-4))"""
    if q in CR_EXACT:
        return CR_EXACT[q]
    return -(-q * crK(q - 1) // (q - 4))


def Z(n):
    """Hill's drawing: cr(K_n) <= Z(n); used only as an upper bound"""
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4


def gallai_cap(nv, maxblk, at_most_one_max=True):
    """max edges of a connected graph on nv vertices whose blocks are cliques of
    order <= maxblk or odd cycles (each block after the first adds u new vertices
    and is glued at one cut vertex)"""
    U = nv - 1
    NEG = -1
    dp = [[NEG, NEG] for _ in range(U + 1)]      # dp[vertices used][may still use a max block]
    dp[0][1] = 0
    for t in range(U + 1):
        for s in (0, 1):
            if dp[t][s] < 0:
                continue
            for u in range(1, U - t + 1):
                opts = []
                blk = u + 1                        # order of the block
                if blk <= maxblk - 1 or not at_most_one_max:
                    if blk <= maxblk:
                        opts.append((u * (u + 1) // 2, s))
                elif blk == maxblk and s == 1:
                    opts.append((u * (u + 1) // 2, 0))
                if u >= 2 and blk % 2 == 1:        # odd cycle block
                    opts.append((blk, s))
                for e, ns in opts:
                    if dp[t][s] + e > dp[t + u][ns]:
                        dp[t + u][ns] = dp[t][s] + e
    return max(dp[U])


def min_split(nv, e_lo, maxblk=None):
    """min sum of cr(K_b) over the clique blocks, over block structures on nv
    vertices with at least e_lo edges"""
    best = [None]

    def rec(rem, cap, edges, cliques):
        if rem == 0:
            if edges >= e_lo:
                s = sum(crK(b) for b in cliques if b >= 15)
                if best[0] is None or s < best[0]:
                    best[0] = s
            return
        hi, rr, c2 = edges, rem, cap
        while rr > 0:                              # optimistic completion
            t = min(c2, rr)
            hi += t * (t + 1) // 2
            rr -= t
        if hi < e_lo:
            return
        for u in range(min(cap, rem), 0, -1):
            if maxblk is None or u + 1 <= maxblk:
                rec(rem - u, u, edges + u * (u + 1) // 2, cliques + [u + 1])
            if u >= 2 and (u + 1) % 2 == 1:
                rec(rem - u, u, edges + u + 1, cliques)

    for c in range(1, nv):
        rec(nv - c, nv - c, 0, [])
    return best[0]


def main():
    r = int(sys.argv[1]) if len(sys.argv) > 1 else 29
    eGR = int(sys.argv[2]) if len(sys.argv) > 2 else 1     # conservative e(G[R]) >= 1
    n = 2 * r
    zz = Z(r)
    print(f'r = {r}, n = 2r = {n}, Z({r}) = {zz} (>= cr(K_{r}), Hill), e(G[R]) >= {eGR}')
    print(f'crK lower bounds: cr(K_15) >= {crK(15)}, cr(K_20) >= {crK(20)}, cr(K_29) >= {crK(29)}')
    print()
    print('   m    |R|  |V(L)|  e(L)>=   cap(<=1 max blk)  cap(unrestricted)   split    verdict')
    allok = True
    for m in (838, 839, 840):
        X = 2 * m - n * (r - 1)
        hi = 2 + (X - (2 * r - 6))
        for Rsz in range(2, hi + 1):
            VL = n - Rsz
            eL = m - ((r - 1) * Rsz + X) + eGR
            cap1 = gallai_cap(VL, r - 2, True)
            cap2 = gallai_cap(VL, r - 2, False)
            sp = min_split(VL, eL, r - 2)
            ok1 = eL > cap1 or (sp is not None and sp > zz)
            ok2 = eL > cap2 or (sp is not None and sp > zz)
            allok &= ok2
            print(f'  {m}   {Rsz:2d}    {VL:3d}    {eL:5d}        {cap1:5d}             {cap2:5d}      '
                  f'{sp if sp is not None else "-":>6}    '
                  f'{"impossible" if ok1 else "SURVIVES"} / {"impossible" if ok2 else "SURVIVES"}')
    print()
    print('every row closed even with the unrestricted Gallai cap: ' + ('YES' if allok else 'NO'))


if __name__ == '__main__':
    main()

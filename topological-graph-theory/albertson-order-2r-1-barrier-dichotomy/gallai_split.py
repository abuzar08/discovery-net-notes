#!/usr/bin/env python3
"""For each surviving |R| at (53,713), enumerate every admissible Gallai block
multiset of L and evaluate the split bound over its pairwise-disjoint clique
blocks.  Blocks of size >= 15 are pairwise disjoint: a shared cut vertex v would
have (|Q1|-1)+(|Q2|-1) >= 28 > 26 = d_G(v) neighbours inside L."""
import sys
import verify_range as V

N, R_CHI, M = 53, 27, 713
Z27 = V.Z(R_CHI)

def clique_edges(u): return u * (u + 1) // 2
def cycle_edges(u):  return u + 1 if (u + 1) >= 3 and (u + 1) % 2 == 1 else -1

def enumerate_packings(U, eL_lo, maxpart=24, one_max=True):
    """Yield (min split bound) over all block multisets with sum u_i = U,
    u_i <= maxpart, at most one u_i = maxpart, and total edges >= eL_lo."""
    best = [None]
    def rec(rem, cap, used_max, edges, cliques):
        if rem == 0:
            if edges >= eL_lo:
                s = sum(V.crK(c) for c in cliques if c >= 15)
                if best[0] is None or s < best[0]:
                    best[0] = s
            return
        # optimistic bound: even filling everything with the largest allowed part
        hi = edges
        r, c2 = rem, cap
        while r > 0:
            t = min(c2, r); hi += clique_edges(t); r -= t
        if hi < eL_lo:
            return
        for u in range(min(cap, rem), 0, -1):
            if u == maxpart and used_max and one_max:
                continue
            um = used_max or (u == maxpart)
            ce = clique_edges(u)
            rec(rem - u, u, um, edges + ce, cliques + [u + 1])
            cy = cycle_edges(u)
            if cy > 0 and cy != ce:
                rec(rem - u, u, um, edges + cy, cliques)
    rec(U, maxpart, False, 0, [])
    return best[0]

print("split bound over Gallai blocks at (53,713), Z(27) = %d" % Z27)
print(" |R|  |V(L)|   c    U    e(L)>=   min split bound over admissible packings")
overall = {}
for Rsz in (5, 6):
    VL = N - Rsz
    eL_lo = 665 - 26 * Rsz + 1
    worst = None
    for c in range(1, VL + 1):
        U = VL - c
        if U < 1:
            continue
        b = enumerate_packings(U, eL_lo)
        if b is None:
            continue                      # no admissible packing: that c is impossible
        if worst is None or b < worst:
            worst = b
        print("  %2d    %3d   %2d  %3d    %4d     %s" % (Rsz, VL, c, U, eL_lo, b))
        if c >= 2:
            break
    overall[Rsz] = worst
print()
for Rsz, w in overall.items():
    print("|R|=%d: min split bound %s vs Z(27)=%d -> %s"
          % (Rsz, w, Z27, "IMPOSSIBLE" if w is not None and w > Z27 else "survives"))

#!/usr/bin/env python3
"""Robustness of Step 5: the split bound over the Gallai blocks makes the
|R| = 2 and |R| = 3 contradictions independent of BOTH structural block claims
("clique blocks have order <= 25" and "at most one has order 25").

For any Gallai forest L on N_L vertices with c components,
sum over blocks of (order-1) = N_L - c.  A clique block of order b carries
C(b,2) edges, an odd cycle of order b carries b.  Two blocks of order >= 15
cannot share a cut vertex (it would have >= 28 > 26 neighbours in L), so all
such blocks are pairwise disjoint and the split bound
cr(G) >= sum_i cr(G[Q_i]) >= sum_i crK(|Q_i|) applies to them.

We enumerate EVERY block multiset with the forced edge total and take the
minimum of that split bound.  No cap on block order is imposed.
"""
import verify_range as V

Z27 = V.Z(27)

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
        while r > 0:                       # optimistic completion
            t = min(c2, r); hi += t * (t + 1) // 2; r -= t
        if hi < eL_lo:
            return
        for u in range(min(cap, rem), 0, -1):
            rec(rem - u, u, edges + u * (u + 1) // 2, cliques + [u + 1])   # clique
            if u >= 2 and (u + 1) % 2 == 1:                                # odd cycle
                rec(rem - u, u, edges + u + 1, cliques)
    for c in range(1, NL):
        rec(NL - c, NL - c, 0, [])
    return best[0]

print("Step 5 without any block-order restriction, via the split bound")
print("  |R|  |V(L)|  forced e(L)>=   min split bound   Z(27)   verdict")
for Rsz, NL, eL in ((2, 51, 614), (3, 50, 588)):
    b = min_split(NL, eL)
    print("   %d     %2d        %4d           %6s        %4d    %s"
          % (Rsz, NL, eL, b, Z27, "CONTRADICTION" if b is not None and b > Z27 else "survives"))
print()
print("crK reference:", {q: V.crK(q) for q in (15, 20, 24, 25, 26, 27)})

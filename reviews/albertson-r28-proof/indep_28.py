r"""reviewer-1: independent check of the r = 28 proof attempt (h2711), Part B.

My own crossing-number ladder, my own Gallai cap (maximum edges of a Gallai
forest with blocks of order at most r-2, by my own dynamic programme), my own
e(L) identity and my own split minima, at both seedings.
"""
import sys
from functools import lru_cache

R, N = 28, 55
BASE_CCCG = {5:1,6:3,7:9,8:18,9:36,10:60,11:100,12:150,13:225,14:315}
BASE_CONS = {5:1,6:3,7:9,8:18,9:36,10:60,11:100,12:150}


def Zh(n):
    return (n//2)*((n-1)//2)*((n-2)//2)*((n-3)//2)//4


def make_cr(base):
    @lru_cache(maxsize=None)
    def crK(q):
        if q in base: return base[q]
        if q < 5: return 0
        return -(-q*crK(q-1)//(q-4))
    return crK


@lru_cache(maxsize=None)
def maxgallai(p, q):
    """most edges of a Gallai forest on p vertices whose blocks are cliques of
    order at most q (blocks pairwise share at most a cut vertex): my own DP"""
    if p <= 1:
        return 0
    best = 0
    for b in range(2, min(q, p) + 1):
        best = max(best, b*(b-1)//2 + maxgallai(p - b + 1, q))
    return best


def eL_bound(m, RSZ, eGR):
    return m - 27*RSZ - (2*m - N*27) + eGR


def min_split(crK, NL, eLo, qmax=26):
    """least sum of cr(K_q) over block multisets covering NL vertices with at
    least eLo edges and blocks of order at most qmax"""
    best = [None]
    def rec(rem, cap, edges, score):
        if rem == 0:
            if edges >= eLo and (best[0] is None or score < best[0]):
                best[0] = score
            return
        hi = edges
        r2, c2 = rem, cap
        while r2 > 0:
            t = min(c2, r2); hi += t*(t+1)//2; r2 -= t
        if hi < eLo:
            return
        for u in range(min(cap, rem), 0, -1):
            if u + 1 > qmax: continue
            rec(rem - u, u, edges + (u+1)*u//2, score + crK(u+1))
    for c in range(1, NL + 1):
        rec(NL - c, NL - c, 0, 0)
    return best[0]


ROWS = [(768, 2, 1), (768, 3, 1), (768, 4, 3),
        (769, 2, 1), (769, 3, 1), (769, 4, 1), (769, 5, 3), (769, 6, 6)]

for name, base in (('CCCG 2021 seeding', BASE_CCCG),
                   ('conservative seeding', BASE_CONS)):
    crK = make_cr(base)
    print(f'{name}: cr(K13) >= {crK(13)}, Z(28) = {Zh(R)}')
    print('    m   |R|  |L|   e(L)>=   Gallai cap   split      verdict')
    margins = []
    for (m, RSZ, eGR) in ROWS:
        NL = N - RSZ
        lo = eL_bound(m, RSZ, eGR)
        cap = maxgallai(NL, R - 2)
        if lo > cap:
            print(f'  {m}  {RSZ:3d}  {NL:3d}  {lo:6d}  {cap:10d}       -    '
                  f'impossible (exceeds the Gallai cap)')
            continue
        sp = min_split(crK, NL, lo)
        margins.append(sp - Zh(R))
        print(f'  {m}  {RSZ:3d}  {NL:3d}  {lo:6d}  {cap:10d}  {sp:6d}    '
              f'{"impossible" if sp > Zh(R) else "SURVIVES"}')
    print(f'    tightest split margin over Z(28): {min(margins)}')
    print()

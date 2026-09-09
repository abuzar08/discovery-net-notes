r"""reviewer-1: independent check of the order-57 row-826 closure (h3285, r2).

My own crossing-number ladder, my own block-multiset enumeration and my own
implementation of the two ingredients:

  A: blocks are edge-disjoint so cr(G) >= sum_i cr(Q_i); and since each w_i is
     G-adjacent to all of C and w_1 w_2 is an edge, augmenting one block by
     w_1, w_2 gives cr(G) >= cr(K_{q_j - beta_j + 2}) + sum_{l != j} cr(Q_l),
     with the adversary choosing beta subject to beta_j <= 2, at most one
     beta_j = 2, and sum_j beta_j <= 4;
  B: every low vertex has sum over its blocks of (|Q| - 1) >= 28 - |R| =: d0,
     so a block with q - 1 < d0 has all its vertices in a second block and
     therefore q <= extra := sum_j q_j - |L|.
"""
import sys
from functools import lru_cache

BASE = {5: 1, 6: 3, 7: 9, 8: 18, 9: 36, 10: 60, 11: 100, 12: 150,
        13: 225, 14: 315}


@lru_cache(maxsize=None)
def crK(q):
    if q in BASE:
        return BASE[q]
    if q < 5:
        return 0
    return -(-q * crK(q - 1) // (q - 4))


ROWS = [(826, 7, 582), (827, 7, 581), (827, 8, 555), (827, 9, 529),
        (828, 7, 580), (828, 8, 554), (828, 9, 528), (828, 10, 502),
        (828, 11, 476)]
Z29 = 8281


def multisets(NL, eLo):
    """block multisets: orders >= 2, sum (q-1) = NL - c for some c >= 1,
    total edges at least eLo"""
    out = []
    def rec(rem, cap, edges, blocks):
        if rem == 0:
            if edges >= eLo and blocks:
                out.append(tuple(sorted(blocks, reverse=True)))
            return
        # optimistic completion: all remaining in one block
        hi = edges + (rem + 1) * rem // 2
        if hi < eLo:
            return
        for u in range(min(cap, rem), 0, -1):
            rec(rem - u, u, edges + (u + 1) * u // 2, blocks + [u + 1])
    for c in range(1, NL):
        rec(NL - c, NL - c, 0, [])
    return sorted(set(out))


def augmented_gain(mult):
    """the adversary picks beta to minimise our best gain"""
    best = None
    k = len(mult)
    import itertools
    for beta in itertools.product((0, 1, 2), repeat=k):
        if sum(beta) > 4 or sum(1 for b in beta if b == 2) > 1:
            continue
        gain = max(crK(q - b + 2) - crK(q) for q, b in zip(mult, beta))
        if best is None or gain < best:
            best = gain
    return best or 0


def degree_ok(mult, NL, RSZ):
    d0 = 28 - RSZ
    extra = sum(mult) - NL
    if extra < 0:
        return False
    return all(q <= extra for q in mult if q - 1 < d0)


def main():
    print('  row  |R|  |L|  e(L)>=   plain   +w1,w2  +degree   minimiser'
          '        verdict')
    for (m, RSZ, eLo) in ROWS:
        NL = 57 - RSZ
        ms = multisets(NL, eLo)
        plain = min((sum(crK(q) for q in mm), mm) for mm in ms)
        aug = min((sum(crK(q) for q in mm) + augmented_gain(mm), mm)
                  for mm in ms)
        msd = [mm for mm in ms if degree_ok(mm, NL, RSZ)]
        deg = min((sum(crK(q) for q in mm) + augmented_gain(mm), mm)
                  for mm in msd) if msd else (0, ())
        verdict = 'impossible' if deg[0] >= Z29 else 'SURVIVES'
        print(f'  {m}  {RSZ:3d}  {NL:3d}  {eLo:6d}  {plain[0]:6d}  '
              f'{aug[0]:6d}  {deg[0]:7d}   {str(deg[1])[:16]:16s} {verdict}')


if __name__ == '__main__':
    main()

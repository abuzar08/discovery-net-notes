r"""reviewer-1: independent check of the covering-count lemma (h3285, r2).

My own implementation of both ingredients:

  C: big blocks (q - 1 >= delta_0) are pairwise disjoint — valid because a
     shared vertex would have degree >= 2 delta_0 > 28 for |R| <= 13 — and every
     vertex outside the big blocks must reach delta_0 from small blocks alone,
     giving sum_small q(q-1) >= delta_0 (p - sum_big q);
  D: e(L) = m - 28|R| - X + e(G[R]) is an identity, so with
     e(G[R]) <= C(|R|,2) the value e(L) = sum_j C(q_j,2) is pinned into a band.

Scores use my own crossing-number ladder and the block augmentation of the
previous lemma (adversary chooses beta_j <= 2, at most one 2, sum <= 4).
"""
import itertools, sys
from functools import lru_cache

sys.path.insert(0, '/Users/abuzark/.discovery-research-team/workspaces/'
                   'reviewer-1/notes/topological-graph-theory/'
                   'albertson-order-2r-1-barrier-dichotomy')
import r29

BASE = {5: 1, 6: 3, 7: 9, 8: 18, 9: 36, 10: 60, 11: 100, 12: 150,
        13: 225, 14: 315}
N, DEG, Z29 = 57, 28, 8281


@lru_cache(maxsize=None)
def crK(q):
    if q in BASE:
        return BASE[q]
    if q < 5:
        return 0
    return -(-q * crK(q - 1) // (q - 4))


def band(m, RSZ):
    X = 2 * m - N * DEG
    base = m - DEG * RSZ - X
    return base + r29.eGR_min(RSZ), base + RSZ * (RSZ - 1) // 2


def multisets(NL, lo, hi):
    out = []
    def rec(rem, cap, edges, blocks):
        if edges > hi:
            return
        if rem == 0:
            if lo <= edges <= hi and blocks:
                out.append(tuple(sorted(blocks, reverse=True)))
            return
        for u in range(min(cap, rem), 0, -1):
            rec(rem - u, u, edges + (u + 1) * u // 2, blocks + [u + 1])
    for c in range(1, NL + 1):
        rec(NL - c, NL - c, 0, [])
    return sorted(set(out))


def covering_ok(mult, NL, RSZ):
    d0 = DEG - RSZ
    big = [q for q in mult if q - 1 >= d0]
    small = [q for q in mult if q - 1 < d0]
    if sum(big) > NL:                       # big blocks are pairwise disjoint
        return False
    return sum(q * (q - 1) for q in small) >= d0 * (NL - sum(big))


def per_block_only(mult, NL, RSZ):
    """the weaker filter the previous work used: a block with q-1 < d0 has all
    its vertices in a second block, so q <= extra"""
    d0 = DEG - RSZ
    extra = sum(mult) - NL
    if extra < 0:
        return False
    return all(q <= extra for q in mult if q - 1 < d0)


def aug_gain(mult):
    best = None
    for beta in itertools.product((0, 1, 2), repeat=len(mult)):
        if sum(beta) > 4 or sum(1 for b in beta if b == 2) > 1:
            continue
        g = max(crK(q - b + 2) - crK(q) for q, b in zip(mult, beta))
        if best is None or g < best:
            best = g
    return best or 0


ROWS = [(826, 7), (827, 7), (827, 8), (827, 9),
        (828, 7), (828, 8), (828, 9), (828, 10), (828, 11)]


def main():
    print('  row  |R|  |L|   e(L) band    +aug(perblock)   +C      verdict   '
          'minimiser')
    for (m, RSZ) in ROWS:
        NL = N - RSZ
        lo, hi = band(m, RSZ)
        ms = multisets(NL, lo, hi)
        old = [mm for mm in ms if per_block_only(mm, NL, RSZ)]
        new = [mm for mm in ms if covering_ok(mm, NL, RSZ)]
        s_old = min((sum(crK(q) for q in mm) + aug_gain(mm), mm) for mm in old) \
            if old else None
        s_new = min((sum(crK(q) for q in mm) + aug_gain(mm), mm) for mm in new) \
            if new else None
        verdict = ('impossible (no admissible multiset)' if s_new is None
                   else 'impossible' if s_new[0] >= Z29 else 'SURVIVES')
        print(f'  {m}  {RSZ:3d}  {NL:3d}  [{lo},{hi}]  '
              f'{(s_old[0] if s_old else "none"):>8}  '
              f'{(s_new[0] if s_new else "none"):>8}   {verdict:34s} '
              f'{s_new[1] if s_new else ""}')
    print()
    print('THE EXAMPLE THE BODY GIVES: (25,23,2,2) on p = 49, delta_0 = 20')
    mm = (25, 23, 2, 2)
    print(f'   per-block filter accepts it: {per_block_only(mm, 49, 8)}')
    print(f'   covering count accepts it:   {covering_ok(mm, 49, 8)}')
    print('   (two big blocks would need 25 + 23 = 48 distinct vertices, and '
          'the 49th\n    reaches block degree at most 1 + 1 = 2 against '
          'delta_0 = 20)')


if __name__ == '__main__':
    main()

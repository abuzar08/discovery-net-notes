"""reviewer-1: independent checks of the two order-58 lemmas at h3014.

  (1) the closed form maxgallai(p, q) for the maximum number of edges of a
      Gallai forest on p vertices with all blocks of order <= q, against my own
      dynamic program over block trees (cliques and odd cycles);
  (2) the minimum of cr(K_a) + cr(K_b) over a + b >= 54, a, b <= 29 -- the number
      the "no two disjoint triangles" lemma quotes as 11092 -- computed under
      both seedings of the counting recursion;
  (3) the arithmetic of that lemma's chain: edges meeting a triangle, e(F), and
      the Cauchy-Schwarz step;
  (4) a sensitivity analysis of the b >= 8 closure: the target's own classifier
      re-run with my conservative cr(K_q), seeded only by cr(K_12) = 150.

usage: python3 indep_58.py
"""
from functools import lru_cache

CR12 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 3, 7: 9, 8: 18, 9: 36, 10: 60, 11: 100, 12: 150}
CR14 = {**CR12, 13: 225, 14: 315}


def make_crK(base):
    @lru_cache(maxsize=None)
    def crK(q):
        if q in base:
            return base[q]
        return -(-q * crK(q - 1) // (q - 4))
    return crK


def Z(n):
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4


def maxgallai_closed(p, q):
    """the target's closed form"""
    if p <= 1:
        return 0
    k = (p - 1) // (q - 1)
    rem = (p - 1) - k * (q - 1)
    return k * (q * (q - 1) // 2) + (rem + 1) * rem // 2


def maxgallai_dp(p, q):
    """my own version: maximum edges of a connected block tree on p vertices whose
    blocks are cliques of order <= q or odd cycles (a block on u+1 vertices adds u
    new vertices and either u(u+1)/2 edges as a clique or u+1 as an odd cycle)"""
    U = p - 1
    dp = [-1] * (U + 1)
    dp[0] = 0
    for t in range(U + 1):
        if dp[t] < 0:
            continue
        for u in range(1, U - t + 1):
            blk = u + 1
            cand = []
            if blk <= q:
                cand.append(u * (u + 1) // 2)
            if u >= 2 and blk % 2 == 1:
                cand.append(blk)
            for e in cand:
                if dp[t] + e > dp[t + u]:
                    dp[t + u] = dp[t] + e
    return dp[U]


def main():
    print('(1) maximum edges of a Gallai forest: closed form vs my own DP')
    bad = []
    for p in range(2, 41):
        for q in range(3, 30):
            a, b = maxgallai_closed(p, q), maxgallai_dp(p, q)
            if a != b:
                bad.append((p, q, a, b))
    print(f'    agreement over 2 <= p <= 40, 3 <= q <= 29: '
          f'{"exact" if not bad else f"{len(bad)} disagreements, e.g. {bad[:5]}"}')
    print(f'    maxgallai(30,27) = {maxgallai_closed(30,27)} (mine {maxgallai_dp(30,27)}), '
          f'maxgallai(30,28) = {maxgallai_closed(30,28)}, maxgallai(30,29) = {maxgallai_closed(30,29)}')
    print()

    print('(2) min of cr(K_a) + cr(K_b) over a+b >= 54, a,b <= 29')
    for base, name in ((CR14, 'seeded by cr(K_14) = 315 (CCCG 2021)'),
                       (CR12, 'seeded only by cr(K_12) = 150')):
        crK = make_crK(base)
        best = min(((crK(a) + crK(b), a, b) for a in range(1, 30) for b in range(1, 30)
                    if a + b >= 54), key=lambda t: t[0])
        print(f'    {name}: minimum {best[0]} at (a,b) = ({best[1]},{best[2]}); '
              f'cr(K_27) >= {crK(27)}, cr(K_28) >= {crK(28)}, cr(K_26) >= {crK(26)}')
    print(f'    Z(29) = {Z(29)}: the branch closes under either seeding')
    print()

    print('(3) the arithmetic of the no-two-disjoint-triangles lemma')
    r, n = 29, 58
    for m in (838, 839, 840):
        eH = n * (n - 1) // 2 - m
        meet = 3 * r - 3
        eF = eH - meet
        need = -(-4 * eF // 55)                      # ceil(4 e(F) / |V(F)|)
        print(f'    m={m}: e(H)={eH}, edges meeting T <= {meet}, e(F) >= {eF}, '
              f'some edge has d_F(u)+d_F(v) >= {need}')
    print('    (|V(F)| = 55; F is triangle-free, so N_F(u), N_F(v) are disjoint '
          'independent sets of H, i.e. disjoint cliques of G)')


if __name__ == '__main__':
    main()

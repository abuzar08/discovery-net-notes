r"""reviewer-1: independent check of the crossing lemma (height 3285, researcher-2).

This is the lemma that my review of the order-57 closure showed carries that
closure, so every step is redone here from the pinned configuration alone:
\(j = 1\), \(\sigma = 0\), blocks \((24,24)\) partitioning the 48 low vertices,
\(\lvert R\rvert = 9\), \(\lvert Z\rvert = 7\).

  1. the edge counts and the two routes to \(e_H(L,R) = 192\);
  2. the per-vertex cap and the pigeonhole that makes every \(z\) crossing;
  3. \(\theta(H[L]) = 24\) and the triangle arithmetic PER ROW;
  4. the crossing-number table, under the seeding the lane uses and under the
     conservative seeding, since the numbers depend on which is taken.
"""
import math

N, DEG, RCHI, RSZ, BLK = 57, 28, 29, 9, 24
NL, NZ = N - RSZ, RSZ - 2


def Z_hill(n):
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4


def cr_lower(seed):
    """cr(K_q) lower bounds from the counting recursion
    cr(K_q) >= ceil(q * cr(K_{q-1}) / (q - 4)), from a seed dictionary"""
    cr = dict(seed)
    for q in range(max(seed) + 1, 30):
        cr[q] = -(-q * cr[q - 1] // (q - 4))
    return cr


def edge_counts(m):
    eL = 2 * (BLK * (BLK - 1) // 2)
    eHL = BLK * BLK                                   # H[L] = K_{24,24}
    assert eHL == NL * (NL - 1) // 2 - eL
    eGLR = DEG * NL - 2 * eL
    eGR = m - eL - eGLR
    eHR = RSZ * (RSZ - 1) // 2 - eGR
    eH = N * (N - 1) // 2 - m
    return dict(eL=eL, eHL=eHL, eGR=eGR, eHR=eHR,
                eHLR_a=eH - eHL - eHR,
                eHLR_b=NL * (RSZ - DEG) + 2 * eL)


def main():
    print('EDGE COUNTS, two routes to e_H(L,R)')
    for m in (827, 828):
        c = edge_counts(m)
        print(f'   m = {m}: e(L) = {c["eL"]}, e(H[L]) = {c["eHL"]} = 24 x 24, '
              f'e(G[R]) = {c["eGR"]}, e(H[R]) = {c["eHR"]}, '
              f'e_H(L,R) = {c["eHLR_a"]} (complement count) = {c["eHLR_b"]} '
              f'(degree identity)')
    print()

    print('THE CAP AND THE PIGEONHOLE')
    print('   for a high z, d_G(z) = 28 + x_z with x_z >= 1, and')
    print('   |N_H(z) ^ L| = 48 - (d_G(z) - (8 - h_z)) = 28 - x_z - h_z <= 27')
    for (m, a, tau) in [(827, 3, 1), (828, 1, 0), (828, 2, 0)]:
        c = edge_counts(m)
        w = 2 + a - tau
        sumZ = c['eHLR_a'] - w
        floor_each = sumZ - (NZ - 1) * 27
        print(f'   m = {m}, a = {a}, tau = {tau}: w-contribution {w}, '
              f'sum over Z = {sumZ}, so each |N_H(z) ^ L| >= '
              f'{sumZ} - 6*27 = {floor_each}, hence min(a_z,b_z) >= '
              f'{floor_each - BLK}')
    print()

    print('THETA ARITHMETIC, PER ROW  (t vertex-disjoint triangles)')
    for m in (827, 828):
        c = edge_counts(m)
        start = BLK + (RSZ - c['eHR'])
        tneed = start - (RCHI - 1)
        print(f'   m = {m}: theta(H) <= 24 + (9 - e(H[R])) = {start}; each '
              f'triangle saves one, so theta <= {start} - t, and t = {tneed} '
              f'is the least that gives <= 28 < 29')
        print(f'        t = 4 gives {start - 4}'
              f'{" — CONTRADICTION" if start - 4 < RCHI else " — NO contradiction"}'
              f'; the residue to rule out is mu_1 + mu_2 <= '
              f'{NZ + tneed - 1}')
    print()

    print('THE CROSSING-NUMBER TABLE')
    seeds = {'lane seeding (CCCG 2021: cr(K13)=225, cr(K14)=315)':
             {12: 150, 13: 225, 14: 315},
             'conservative seeding (cr(K12)=150 only)': {12: 150}}
    for name, seed in seeds.items():
        cr = cr_lower(seed)
        print(f'   {name}: cr(K24) >= {cr[24]}, cr(K28) >= {cr[28]}')
        for mu in range(2, 8):
            q = 30 - mu                       # 31 - mu, less one for the non-edge
            b = cr[q] + cr[BLK]
            print(f'      mu_1 = {mu}: clique K_{q} disjoint from a K_24  ->  '
                  f'cr >= {cr[q]} + {cr[BLK]} = {b}  '
                  f'{"CLOSES" if b >= Z_hill(RCHI) else "survives"} '
                  f'(Z(29) = {Z_hill(RCHI)})')
    print()

    print('SURVIVING (mu_1, mu_2) PAIRS, per row')
    cr = cr_lower({12: 150, 13: 225, 14: 315})
    lo = min(mu for mu in range(2, 8) if cr[30 - mu] + cr[BLK] < Z_hill(RCHI))
    print(f'   the table forces mu_i >= {lo}')
    for m in (827, 828):
        c = edge_counts(m)
        start = BLK + (RSZ - c['eHR'])
        tneed = start - (RCHI - 1)
        cap = NZ + tneed - 1
        pairs = [(x, y) for x in range(lo, NZ + 1) for y in range(lo, NZ + 1)
                 if x + y <= cap]
        print(f'   m = {m}: t = {tneed} needed, residue mu_1 + mu_2 <= {cap}, '
              f'surviving pairs {sorted(pairs)}')


if __name__ == '__main__':
    main()

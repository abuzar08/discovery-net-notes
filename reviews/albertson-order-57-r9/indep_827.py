r"""reviewer-1: independent check of the order-57 |R| = 9 closure (h3285, researcher-2).

This is a POSITIVE closure — it eliminates row (57,827) — so unlike the negative
finding h3293 every bound has to point the safe way.  Each step is recomputed
here from the pinned configuration alone (\(j = 1\), \(\sigma = 0\), blocks
\((24,24)\) partitioning \(L\), \(\lvert Z\rvert = 7\), every \(z\) crossing with
\(\min(a_z,b_z) \ge 2\)):

  1. the counting facts, from \(d_G(v) = 28\) and the block partition;
  2. the constrained Koenig maximum, computed by my own optimisation and
     validated by brute force over all small bipartite graphs;
  3. what happens WITHOUT the crossing hypothesis, to show where the closure
     actually rests;
  4. the saturation count, the triangle construction and the clique-cover
     arithmetic, including the two instantiations that reach 28 < 29.
"""
import itertools

N, DEG, RCHI, RSZ = 57, 28, 29, 9
NL, NZ, Q = N - RSZ, RSZ - 2, 24          # 48 low vertices, |Z| = 7, blocks 24


# ------------------------------------------------------------- the counting
def counts(M):
    eL = 2 * (Q * (Q - 1) // 2)                       # two disjoint K_24
    eGLR = DEG * NL - 2 * eL
    eGR = M - eL - eGLR
    eHR = RSZ * (RSZ - 1) // 2 - eGR
    eHLR = NL * RSZ - eGLR
    per_low = RSZ - (DEG - (Q - 1))                   # H-neighbours of v in R
    return dict(eL=eL, eGLR=eGLR, eGR=eGR, eHR=eHR, eHLR=eHLR,
                eHLR_id=NL * (RSZ - DEG) + 2 * eL, per_low=per_low,
                eHQR=Q * per_low)


# ------------------------------------------------------ constrained Koenig
def max_sum_a(k, nz=NZ, q=Q, amin=2):
    """largest sum_z a_z admitted by a vertex cover of size k, given every z has
    a_z >= amin: a cover splits as cz vertices of Z and k - cz of Q; a z outside
    the cover has all its neighbours inside the Q-part, so if cz < nz then
    k - cz >= amin is forced"""
    best = -1
    for cz in range(0, min(k, nz) + 1):
        cq = k - cz
        if cz < nz and cq < amin:
            continue
        best = max(best, q * cz + (nz - cz) * min(cq, q))
    return best


def brute_validate(nz, q, amin=2, kmax=None):
    """for small parts: over all bipartite graphs with every z of degree >= amin,
    the true maximum of sum_z a_z among those of matching number <= k must not
    exceed max_sum_a(k, nz, q, amin)"""
    cells = [(i, j) for i in range(nz) for j in range(q)]
    best = {}
    for mask in range(1 << len(cells)):
        es = [cells[i] for i in range(len(cells)) if mask >> i & 1]
        deg = [0] * nz
        for a, _ in es:
            deg[a] += 1
        if min(deg) < amin:
            continue
        mu = 0
        for r in range(min(nz, q), 0, -1):
            if any(len({a for a, _ in s}) == r and len({b for _, b in s}) == r
                   for s in itertools.combinations(es, r)):
                mu = r
                break
        best[mu] = max(best.get(mu, 0), len(es))
    out = []
    for k in sorted(best):
        true_max = max(v for mu, v in best.items() if mu <= k)
        out.append((k, true_max, max_sum_a(k, nz, q, amin)))
    return out


def main():
    print('FACTS, from d_G(v) = 28 and the block partition')
    for M in (827, 828):
        c = counts(M)
        assert c['eHLR'] == c['eHLR_id']
        print(f'   m = {M}: e(L) = {c["eL"]}, e_G(L,R) = {c["eGLR"]}, '
              f'e(G[R]) = {c["eGR"]} of {RSZ * (RSZ - 1) // 2}, '
              f'e(H[R]) = {c["eHR"]}; every low vertex has {c["per_low"]} '
              f'H-neighbours in R, so e_H(Q_i,R) = {c["eHQR"]} and '
              f'e_H(L,R) = {c["eHLR"]} = 2 x {c["eHQR"]}')
    print()

    print('THE w-CONTRIBUTION, cross-checked against the (a, j, sigma) formula')
    for (a, j, sig, want) in [(3, 1, 0, 188), (1, 1, 0, 189), (2, 1, 0, 188)]:
        jA = max(0, j + a - 3)
        c = 2 * (1 - sig) + a - jA
        print(f'   a={a} j={j} sigma={sig}: c = 2(1-sigma) + a - j_A = {c}, '
              f'so sum_z |N_H(z) ^ L| = 192 - {c} = {192 - c} '
              f'{"(matches the artifact)" if 192 - c == want else "MISMATCH"}'
              f'  ->  sum_z a_z >= {(192 - c) // 2 if (192 - c) % 2 == 0 else "?"}'
              f' per side, worst case {96 - c}')
    print()

    print('THE CONSTRAINED KOENIG MAXIMUM (mine)')
    for k in range(2, 9):
        print(f'   k = {k}: max sum_z a_z <= {max_sum_a(k)}')
    need = 92
    least = min(k for k in range(0, NZ + 1) if max_sum_a(k) >= need)
    print(f'   least k whose covers can carry {need} edges: {least}  ->  '
          f'mu_1, mu_2 >= {least}')
    print()

    print('WITHOUT THE CROSSING HYPOTHESIS (a_z >= 2 dropped)')
    for k in range(2, 7):
        print(f'   k = {k}: max sum_z a_z <= {max_sum_a(k, amin=0)}')
    least0 = min(k for k in range(0, NZ + 1) if max_sum_a(k, amin=0) >= need)
    print(f'   least k without the hypothesis: {least0} — so the closure really '
          f'does rest on every z being crossing')
    print()

    print('BRUTE-FORCE VALIDATION of the constrained maximum, small analogues')
    for nz, q in [(3, 3), (3, 4), (4, 4)]:
        rows = brute_validate(nz, q)
        ok = all(t <= f for _, t, f in rows)
        print(f'   |Z|={nz}, |Q|={q}: (k, true max, my bound) {rows}  '
              f'{"sound" if ok else "*** VIOLATED ***"}')
    print()

    print('SATURATION, TRIANGLES AND THE CLIQUE COVER')
    mu = least
    both = 2 * mu - NZ
    print(f'   mu_1 + mu_2 >= {2 * mu}, so at least {both} vertices of Z are '
          f'saturated on both sides')
    for M, t in ((827, 4), (828, 5)):
        c = counts(M)
        eHR = c['eHR']
        theta = t + (Q - t) + ((RSZ - t) - eHR)
        print(f'   m = {M}: t = {t} triangles cover t vertices of Z and 2t of L;'
              f' H[L] leaves K_{{{Q - t},{Q - t}}}, covered by {Q - t} cliques;'
              f' R keeps {RSZ - t} vertices with {eHR} H-edge(s), so'
              f' theta(H) <= {t} + {Q - t} + {RSZ - t - eHR} = {theta}'
              f'  {"< 29 = chi(G): IMPOSSIBLE" if theta < RCHI else "NO CONTRADICTION"}'
              f'   [{both} candidates available, {t} needed]')


if __name__ == '__main__':
    main()

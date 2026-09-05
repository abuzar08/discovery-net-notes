"""reviewer-1: independent check of symC, the cycle-sorting symmetry break of
h3014, and of its interaction with symF.

For a permutation tau of the cycle indices, Phi_tau fixes the f fixed vertices
pointwise and sends the i-th vertex of cycle j to the i-th vertex of cycle
tau(j).  The contribution claims (a) Phi_tau commutes with sigma, so it maps
type-1^f p^k graphs to type-1^f p^k graphs and preserves (s,t)-goodness, and
(b) it carries the internal orbit of cycle j at difference d to the internal
orbit of cycle tau(j) at the same d, so sorting the cycles by internal code
loses no isomorphism class.

Checked here with my own union-find orbit numbering (h2661 evidence):

  (1) for every tau in S_k: Phi_tau sigma Phi_tau^{-1} = sigma, the induced
      permutation of the orbit variables maps my base clause set onto itself,
      and internal(j, d) maps to internal(tau(j), d);
  (2) exhaustively over all sigma-invariant graphs for small (n, f, p, k):
      some image under Phi_tau alone satisfies the sorted-code condition, and
      some image under "Phi_tau first, then a permutation of the fixed vertices"
      satisfies sorted codes AND the symF lex condition simultaneously -- the
      order of operations the combination needs, since fixed-vertex permutations
      leave the cycles alone but cycle permutations move the symF columns.

usage: python3 symc_check.py n s t f p k
"""
import sys, itertools
from indep_symf import orbit_numbering, base_clauses


def main():
    n, s, t, f, p, k = map(int, sys.argv[1:7])
    assert p % 2 == 1, 'symC is defined for odd p'
    var, nv = orbit_numbering(n, f, p, k)
    base = base_clauses(n, s, t, var)
    x = lambda val, a, b: (val >> (var[(a, b) if a < b else (b, a)] - 1)) & 1
    half = (p - 1) // 2
    cyc = lambda j, i: f + p * j + i % p

    def phi(tau):
        """vertex map of Phi_tau"""
        m = list(range(n))
        for j in range(k):
            for i in range(p):
                m[cyc(j, i)] = cyc(tau[j], i)
        return m

    sigma = [v if v < f else cyc((v - f) // p, (v - f) % p + 1) for v in range(n)]

    # ---- (1) equivariance, over all tau
    bad = 0
    for tau in itertools.permutations(range(k)):
        m = phi(tau)
        inv = [0] * n
        for v in range(n):
            inv[m[v]] = v
        conj = [m[sigma[inv[v]]] for v in range(n)]
        if conj != sigma:
            bad += 1
            continue
        vmap = {}
        for (a, b), v in var.items():
            aa, bb = m[a], m[b]
            vmap[v] = var[(aa, bb) if aa < bb else (bb, aa)]
        img = {frozenset((vmap[l] if l > 0 else -vmap[-l]) for l in c) for c in base}
        if img != base:
            bad += 1
            continue
        for j in range(k):
            for d in range(1, half + 1):
                a, b = cyc(j, 0), cyc(j, d)
                a2, b2 = cyc(tau[j], 0), cyc(tau[j], d)
                if vmap[var[(min(a, b), max(a, b))]] != var[(min(a2, b2), max(a2, b2))]:
                    bad += 1
    print(f'(1) n={n} 1^{f} {p}^{k}: all {len(list(itertools.permutations(range(k))))} '
          f'cycle permutations commute with sigma, fix my ({s},{t}) clause set, and carry '
          f'internal(j,d) to internal(tau(j),d): {"OK" if bad == 0 else f"{bad} FAILURES"}')
    assert bad == 0

    # ---- (2) no solution lost, exhaustively
    assert nv <= 22, f'{nv} orbit variables is too many to enumerate'

    def relabel(val, m):
        out = 0
        for (a, b), v in var.items():
            if (val >> (v - 1)) & 1:
                aa, bb = m[a], m[b]
                out |= 1 << (var[(aa, bb) if aa < bb else (bb, aa)] - 1)
        return out

    def code(val, j):
        return tuple(x(val, cyc(j, 0), cyc(j, d)) for d in range(1, half + 1))

    def codes_sorted(val):
        return all(code(val, j) <= code(val, j + 1) for j in range(k - 1))

    cols = lambda u: [cyc(j, 0) for j in range(k)] + [w for w in range(f) if w not in (u, u + 1)]

    def rows_ok(val):
        for u in range(f - 1):
            c = cols(u)
            if [x(val, u, w) for w in c] > [x(val, u + 1, w) for w in c]:
                return False
        return True

    fperms = [list(pi) + list(range(f, n)) for pi in itertools.permutations(range(f))] or [list(range(n))]
    taus = list(itertools.permutations(range(k)))
    lost_c = lost_both = 0
    for val in range(1 << nv):
        imgs = [relabel(val, phi(tau)) for tau in taus]
        if not any(codes_sorted(w) for w in imgs):
            lost_c += 1
        if not any(codes_sorted(w) and rows_ok(relabel(w, pm))
                   and codes_sorted(relabel(w, pm))
                   for w in imgs for pm in fperms):
            lost_both += 1
    print(f'(2) n={n} 1^{f} {p}^{k}: {1 << nv} sigma-invariant graphs; without a sorted-code '
          f'image: {lost_c}; without an image satisfying sorted codes AND the symF rows '
          f'(cycles sorted first, then the fixed vertices permuted): {lost_both}')
    assert lost_c == 0 and lost_both == 0


if __name__ == '__main__':
    main()

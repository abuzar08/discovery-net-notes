r"""reviewer-1: an adversarial soundness family for h2713 that its own suite does
not contain — explicit two-page drawings at many \((n,q)\).

For each \((n,q)\) I build a drawing of *some* graph with those parameters
(optimal two-page drawing of \(K_n\), then greedy deletion with re-optimisation)
and count its crossings exactly. That number is an upper bound on
\(\min\{\mathrm{cr}(G)\}\) over the family, so a sound \((n,q)\)-only bound must
not exceed it.
"""
import random
import sys
sys.path.insert(0, '../dens1')

import indep_ceiling as P
import indep_2713 as B


def drawing_upper(n, q, rng, restarts=6):
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    cross = P.build(edges)
    page = [rng.randrange(2) for _ in edges]
    P.optimise(cross, page, rng)
    alive = [True] * len(edges)
    ndel = len(edges) - q
    for _ in range(ndel):
        loads = [(sum(1 for j in cross[i] if alive[j] and page[j] == page[i]), i)
                 for i in range(len(edges)) if alive[i]]
        loads.sort(reverse=True)
        alive[loads[0][1]] = False
    sub = [i for i in range(len(edges)) if alive[i]]
    se = [edges[i] for i in sub]
    sc = P.build(se)
    best = None
    for t in range(restarts):
        p = ([page[i] for i in sub] if t == 0 else [rng.randrange(2) for _ in se])
        v = P.optimise(sc, p, rng)
        best = v if best is None else min(best, v)
    return best


def main():
    rng = random.Random(4242)
    L = B.build(32)
    print('adversarial soundness: my own two-page drawings against L(n,q)')
    viol = []
    for n in (12, 16, 20, 24, 28, 32):
        M = n * (n - 1) // 2
        for frac in (0.55, 0.65, 0.75, 0.85, 0.95, 1.0):
            q = int(round(frac * M))
            up = drawing_upper(n, q, rng)
            lo = L[n][q]
            ok = lo <= up
            if not ok:
                viol.append((n, q, lo, up))
            print(f'   n={n:3d} q={q:4d}  L={lo:6d}  drawing={up:6d}  '
                  f'{"ok" if ok else "VIOLATION"}')
    print(f'   violations: {len(viol)}' + (f' {viol}' if viol else ''))


if __name__ == '__main__':
    main()

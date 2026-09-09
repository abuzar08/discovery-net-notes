r"""reviewer-1: the telescoping identity behind the scale-freeness claim, and a
harder search for a better (32,383) ceiling."""
import random
from math import comb

import indep_ceiling as C


def telescope():
    bad = []
    for n in range(8, 61):
        for s1 in range(6, n):
            for s2 in range(5, s1):
                lhs = comb(n, s1) * comb(s1, s2)
                rhs = comb(n - 4, s1 - 4) * comb(s1 - 4, s2 - 4)
                a = comb(n, s2) * rhs
                b = comb(n - 4, s2 - 4) * lhs
                if a != b:
                    bad.append((n, s1, s2))
    return bad


def harder():
    rng = random.Random(7)
    edges = [(i, j) for i in range(32) for j in range(i + 1, 32)]
    cross = C.build(edges)
    best = None
    for strat in ('greedy', 'matching', 'random', 'clique'):
        for rep in range(3):
            page = [rng.randrange(2) for _ in edges]
            C.optimise(cross, page, rng)
            alive = [True] * len(edges)
            if strat == 'greedy':
                for _ in range(113):
                    loads = [(sum(1 for j in cross[i] if alive[j] and
                                  page[j] == page[i]), i)
                             for i in range(len(edges)) if alive[i]]
                    loads.sort(reverse=True)
                    alive[loads[0][1]] = False
            elif strat == 'random':
                for i in rng.sample(range(len(edges)), 113):
                    alive[i] = False
            elif strat == 'matching':
                # delete the longest chords: they cross the most
                order = sorted(range(len(edges)),
                               key=lambda i: -min((edges[i][1] - edges[i][0]) % 32,
                                                  (edges[i][0] - edges[i][1]) % 32))
                for i in order[:113]:
                    alive[i] = False
            else:
                # delete all edges inside a 15-vertex window's near-clique
                cnt = 0
                for i, (a, b) in enumerate(edges):
                    if cnt < 113 and a < 16 and b < 16:
                        alive[i] = False
                        cnt += 1
            sub = [i for i in range(len(edges)) if alive[i]]
            se = [edges[i] for i in sub]
            sc = C.build(se)
            loc = None
            for t in range(6):
                p = ([page[i] for i in sub] if t == 0
                     else [rng.randrange(2) for _ in se])
                v = C.optimise(sc, p, rng)
                loc = v if loc is None else min(loc, v)
            if best is None or loc < best[0]:
                best = (loc, strat)
            print(f'   {strat} (rep {rep}): {loc} crossings')
    return best


if __name__ == '__main__':
    bad = telescope()
    print(f'telescoping identity C(n,s1)C(s1,s2)/(C(n-4,s1-4)C(s1-4,s2-4)) = '
          f'C(n,s2)/C(n-4,s2-4): failures over 8 <= n <= 60, '
          f'5 <= s2 < s1 < n: {len(bad)}')
    print('my own search for a better (32,383) two-page ceiling:')
    b = harder()
    print(f'   best over all strategies: {b[0]} ({b[1]}); published 4644')

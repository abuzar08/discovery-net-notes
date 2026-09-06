r"""reviewer-1: independent check of the bound \(g(n,f)\) introduced by h3068, and
of the repair it claims for the order-58 \(b \ge 8\) closure.

My own implementation of the three ingredients, from the statement rather than
from crminus.py:

  1. deleting a vertex cover of the missing edges (size at most f) leaves a
     complete graph on at least n-f vertices, so g(n,f) >= crK(n-f);
  2. the sampling bound L(n, C(n,2)-f), taken from the lane's recursive.py;
  3. vertex-deletion averaging: in a good drawing every crossing has four
     distinct vertices and so survives in exactly n-4 of the n vertex-deleted
     subdrawings, giving sum_v cr(F-v) <= (n-4) cr(F); at least t(f) vertices lie
     in a missing edge and for those f_v <= f-1, whence
     g(n,f) >= ceil( ((n-t) g(n-1,f) + t g(n-1,f-1)) / (n-4) ).

Controls of my own, beyond the ones crminus.py runs: g must not exceed the
crossing number of any actual drawing, so it is checked against the known values
cr(K_5 - e) = 0, cr(K_6 - e) = 2, cr(K_7 - e) = 6 and against Z(n).

usage: python3 indep_g.py
"""
from functools import lru_cache
import order2r as O          # only for the sampling bound L(n, m)

CR12 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 3, 7: 9, 8: 18, 9: 36, 10: 60, 11: 100, 12: 150}
SEEDS = {'bare counting recursion': {},
         'McQuillan-Pan-Richter 2015 (219)': {13: 219},
         'EuroCG 2015 (223)': {13: 223},
         'Aichholzer CCCG 2021 (225, 315)': {13: 225, 14: 315}}


def make(seed):
    base = {**CR12, **seed}

    @lru_cache(maxsize=None)
    def crK(q):
        if q in base:
            return base[q]
        if q < 1:
            return 0
        return -(-q * crK(q - 1) // (q - 4))

    @lru_cache(maxsize=None)
    def tmin(f):
        t = 0
        while t * (t - 1) // 2 < f:
            t += 1
        return t

    @lru_cache(maxsize=None)
    def g(n, f):
        if n < 5:
            return 0
        if f <= 0:
            return crK(n)
        best = max(crK(max(0, n - f)), O.L(n, n * (n - 1) // 2 - f))
        t = tmin(f)
        if n - 4 > 0:
            val = -(-((n - t) * g(n - 1, f) + t * g(n - 1, f - 1)) // (n - 4))
            best = max(best, val)
        return best

    return crK, g


def Z(n):
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4


def main():
    print('(1) my own g against the published values (conservative seed)')
    crK, g = make({})
    for n, f in ((28, 3), (28, 6), (27, 3), (26, 0), (32, 113), (31, 87), (49, 594), (52, 685)):
        print(f'    g({n},{f}) = {g(n, f)}   [crminus.py prints '
              f'{ {(28,3):5324,(28,6):4468,(27,3):4520,(26,0):4563,(32,113):2988,(31,87):3164,(49,594):3783,(52,685):4470}[(n,f)] }]')
    print()
    print('(2) my own soundness controls')
    known = {(5, 1): 0, (6, 1): 2, (7, 1): 6}
    for (n, f), v in known.items():
        print(f'    g({n},{f}) = {g(n, f)} must be <= cr(K_{n} - e) = {v}: {g(n, f) <= v}')
    bad = [(n, f) for n in range(5, 61) for f in range(0, 41) if g(n, f) > Z(n)]
    print(f'    g(n,f) <= Z(n) for 5 <= n <= 60, 0 <= f <= 40: {"yes" if not bad else bad[:4]}')
    mono = [(n, f) for n in range(5, 61) for f in range(1, 41) if g(n, f) > g(n, f - 1)]
    print(f'    g non-increasing in f over the same range: {"yes" if not mono else mono[:4]}')
    print(f'    g(n,0) = crK(n) for all n in range: '
          f'{all(g(n,0) == crK(n) for n in range(5, 61))}')
    print()
    print('(3) crK(28) and g(28,3) along the seed ladder')
    for name, seed in SEEDS.items():
        ck, gg = make(seed)
        print(f'    {name:34s} crK(13) = {ck(13):3d}  crK(28) = {ck(28):4d}  g(28,3) = {gg(28,3)}')


if __name__ == '__main__':
    main()

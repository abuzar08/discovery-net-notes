r"""reviewer-1: independent check of the seed-ladder audit (h3284, researcher-2).

The claim is that the order-58 reduction at \(r = 29\) needs nothing beyond
\(\mathrm{cr}(K_{12}) = 150\).  Since I am the reviewer who raised the seeding
dependency at h3034 and h3064, and who verified its repair at h3092, this checks
the audit with my own crossing-number ladder and my own \(g(n,f)\):

  1. the four rungs, and the \(\mathrm{cr}(K_{27}), \mathrm{cr}(K_{28})\) they
     produce;
  2. piece 2 (no two disjoint triangles) recomputed from the forced degree sum;
  3. piece 3 (\(b \ge 8\)) re-run with my \(\mathrm{cr}\) and my \(g\) at every
     rung, using the lane's classifier;
  4. piece 1 re-run with my \(\mathrm{cr}\) substituted, at every rung;
  5. the negative finding about the \(s = 23\) barrier: \(g(32,113)\), the mean
     \(f_v\), and my own version of the "strongest possible averaging".
"""
import sys
from functools import lru_cache

LANE = ('/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/notes/'
        'topological-graph-theory/albertson-order-2r-1-barrier-dichotomy')
MINE = ('/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/notes/'
        'reviews/albertson-crminus-repair')
sys.path.insert(0, LANE)
sys.path.insert(0, MINE)

import indep_g as IG            # my own g(n,f) from the h3092 review
import order2r as O             # only for the sampling bound L(n,m)

R, N = 29, 58
BASE = {5: 1, 6: 3, 7: 9, 8: 18, 9: 36, 10: 60, 11: 100, 12: 150}
RUNGS = [('counting only', {}),
         ('MPR 2015 (219)', {13: 219}),
         ('EuroCG 2015 (223)', {13: 223}),
         ('CCCG 2021 (225, 315)', {13: 225, 14: 315})]


def make_crK(seed):
    base = {**BASE, **seed}

    @lru_cache(maxsize=None)
    def crK(q):
        if q in base:
            return base[q]
        if q < 5:
            return 0
        return -(-q * crK(q - 1) // (q - 4))
    return crK


def Zh(n):
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4


def piece2(crK, m):
    """min of cr(K_a) + cr(K_b) over the forced degree sum a + b >= thr"""
    eH = N * (N - 1) // 2 - m
    eF = eH - (3 * R - 3)
    thr = -(-4 * eF // (2 * R - 3))
    return thr, min(crK(a) + crK(thr - a)
                    for a in range(1, R + 1) if 1 <= thr - a <= R)


def strongest_averaging(f0=113, n0=32):
    """my own version of the 'strongest possible' vertex-deletion averaging:
    at each level use sum_v f_v = f(n-2) exactly, with 0 <= f_v <= min(f, n-1),
    and take the distribution that MINIMISES sum_v g(n-1, f_v) — that is the one
    a lower bound must respect."""
    crK, g = IG.make({})

    @lru_cache(maxsize=None)
    def h(n, f):
        if n < 5:
            return 0
        if f <= 0:
            return crK(n)
        best = max(crK(max(0, n - f)), O.L(n, n * (n - 1) // 2 - f))
        if n - 4 <= 0:
            return best
        cap = min(f, n - 1)
        total = f * (n - 2)
        # minimise sum over v of h(n-1, f_v): h is non-increasing in f, so put
        # as many f_v as possible at the cap
        full, rem = divmod(total, cap) if cap else (0, 0)
        if full > n:
            return best                      # infeasible, no constraint gained
        s = full * h(n - 1, cap)
        if full < n:
            s += h(n - 1, rem)
            s += (n - full - 1) * h(n - 1, 0)
        val = -(-s // (n - 4))
        return max(best, val)

    return h(n0, f0)


def main():
    print('(1) THE FOUR RUNGS, my own ladder')
    for name, seed in RUNGS:
        crK = make_crK(seed)
        print(f'   {name:24s} cr(K13) >= {crK(13):4d}, cr(K24) >= {crK(24)}, '
              f'cr(K27) >= {crK(27)}, cr(K28) >= {crK(28)}')
    print()

    print('(2) PIECE 2, from the forced degree sum')
    for name, seed in RUNGS:
        crK = make_crK(seed)
        vals = []
        for m in (838, 839, 840):
            thr, v = piece2(crK, m)
            vals.append((thr, v))
        print(f'   {name:24s} thresholds {[t for t, _ in vals]}, split minima '
              f'{[v for _, v in vals]} against Z(29) = {Zh(R)}  '
              f'{"holds" if all(v > Zh(R) for _, v in vals) else "FAILS"}')
    print()

    print('(3) PIECE 3 (b >= 8) and (4) PIECE 1, with my cr and my g substituted')
    import verify_range as V
    import crminus as C
    for name, seed in RUNGS:
        crK = make_crK(seed)
        _, gmine = IG.make(seed)
        V.crK = crK
        C.g = gmine
        import k4free as K
        K.V.crK = crK
        K.CM.g = gmine
        live, _ = K.branch_survivors(838, use_gallai=True)
        big838 = [t for t in live if t[0] >= 8]
        out = []
        for m in (838, 839, 840):
            live, _ = K.branch_survivors(m, use_gallai=True)
            out.append(len([t for t in live if t[0] >= 8]))
        # piece 1 with my crK, through the lane's own row test
        import ladder as LD
        LD.V.crK = crK
        p1 = [LD.piece1(m) for m in (838, 839, 840)]
        print(f'   {name:24s} piece 3 survivors {out}; piece 1 rows '
              f'(gallai, split, neither) '
              f'{[(a, b, len(c)) for a, b, c in p1]}')
    print()

    print('(5) THE s = 23 BARRIER, where the dense bound stops')
    crK, g = IG.make({})
    need, n0, f0 = 3557, 32, 113
    mine = g(n0, f0)
    sampling = O.L(n0, n0 * (n0 - 1) // 2 - f0)
    mean_fv = f0 * (n0 - 2) / n0
    strongest = strongest_averaging(f0, n0)
    print(f'   my g({n0},{f0}) = {mine}, the sampling bound alone = {sampling}, '
          f'needed {need}: short by {need - mine}')
    print(f'   mean f_v = {f0} x {n0 - 2} / {n0} = {mean_fv:.4f} against the cap '
          f'{f0}')
    print(f'   my own strongest-averaging variant gives {strongest} '
          f'(the contribution says at most 3016), still short of {need}')


if __name__ == '__main__':
    main()

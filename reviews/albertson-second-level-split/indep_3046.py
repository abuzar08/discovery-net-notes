r"""reviewer-1: independent check of the second-level split bound (h3046, researcher-2).

Everything the contribution states about the \(s = 23\) barrier can be rebuilt
from its own description, and that is what this does:

  1. the boxed identity \(e(H[R]) = e(H) + P - \lvert A\rvert r + Y_A\),
     re-derived from the degree bookkeeping and checked numerically;
  2. the quantities the body quotes — \(e_G(A,R) = 126\) discarded edges, "78 per
     cent density" — recomputed;
  3. the two routes to a bound on \(\mathrm{cr}(G[R])\): my own \(g(n,f)\) and
     the Gallai clique block that the leftover excess forces, and the resulting
     profile in \(Y_A\), whose minimum is what the table reports.

My own \(g\) is the one written for the h3092 review; the crossing-number ladder
is mine, seeded as the lane seeds it.
"""
import sys

LANE = ('/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/notes/'
        'topological-graph-theory/albertson-order-2r-1-barrier-dichotomy')
MINE = ('/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/notes/'
        'reviews/albertson-crminus-repair')
sys.path.insert(0, LANE)
sys.path.insert(0, MINE)
import indep_g as IG

R_CHI, N = 29, 58
crK, g = IG.make({13: 225, 14: 315})


def Zh(n):
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4


def setup(m):
    eH = N * (N - 1) // 2 - m
    X = 2 * m - N * (R_CHI - 1)
    return eH, X


def profile(m, Asz=26, Rsz=32, P=0):
    """for the s = 23 barrier: A is a G-clique on 26 vertices, |R| = 32"""
    eH, X = setup(m)
    rows = []
    for YA in range(0, X + 1):
        eHR = eH + P - Asz * R_CHI + YA          # the boxed identity
        if eHR < 0 or eHR > Rsz * (Rsz - 1) // 2:
            continue
        excess_R = X - YA
        low = Rsz - excess_R                     # at least this many are low
        block = max(0, low - 4)                  # the Gallai clique block
        dense = crK(Asz) + g(Rsz, eHR)
        gallai = crK(Asz) + crK(block)
        rows.append((YA, eHR, excess_R, low, block, dense, gallai,
                     max(dense, gallai)))
    return rows


def main():
    for m in (838,):
        eH, X = setup(m)
        print(f'm = {m}: e(H) = {eH}, X = 2m - 58*28 = {X}, Z(29) = {Zh(R_CHI)}')
        print()
        print('(1) THE IDENTITY, and the quantities the body quotes')
        for YA in (25, 47, 48, 49):
            eHR = eH - 26 * R_CHI + YA
            eGAR = 26 * 32 - (R_CHI * 26 - YA)
            dens = (32 * 31 // 2 - eHR) / (32 * 31 // 2)
            print(f'   Y_A = {YA}: e(H[R]) = {eHR}, e_G(A,R) = {eGAR}, '
                  f'density of G[R] = {dens:.3f}')
        print()
        print('(2) THE PROFILE in Y_A: dense-subgraph route, Gallai route, max')
        print('   Y_A  e(H[R])  excess  low  block   dense   gallai     bound')
        rows = profile(m)
        for (YA, eHR, ex, low, blk, d, ga, b) in rows:
            if YA < 20:
                continue
            mark = ''
            print(f'   {YA:3d} {eHR:8d} {ex:7d} {low:4d} {blk:6d} {d:7d} '
                  f'{ga:8d} {b:9d}{mark}')
        best = min(rows, key=lambda r: r[7])
        print()
        print(f'   minimum of the profile: {best[7]} at Y_A = {best[0]} '
              f'(excess {best[2]} on R, {best[3]} low, block {best[4]}); '
              f'the table reports 7858')
        at48 = [r for r in rows if r[0] == 48][0]
        print(f'   at Y_A = 48 the profile is max({at48[5]}, {at48[6]}) = '
              f'{at48[7]}, not 7858')


if __name__ == '__main__':
    main()

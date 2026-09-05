"""reviewer-1: independent recomputation of the r = 29 order frontier of h2933.

Floors are re-derived here from the published statements, checked against the
sources by hand:

  Kostochka-Yancey (JAMS 2014 / arXiv:1209.1050): every k-critical graph has
      e >= (k/2 - 1/(k-1)) n - k(k-3)/(2(k-1))
        = ((k+1)(k-2) n - k(k-3)) / (2(k-1)),
  Barat-Toth (EJC 17 (2010), arXiv:0909.0413) Corollary 7: r >= 4, G r-critical
      with no topological K_r  =>  2m >= (r-1)n + (2r-6),
  Barat-Toth Corollary 5: r >= 4, 2 <= p = n-r <= r-1, G r-critical with no
      topological K_r  =>  2m >= (r-1)n + p(r-p) - 1,
  Barat-Toth Corollary 11: every r-critical graph on at most r+4 vertices
      contains a topological K_r (so those orders are settled).

The ceiling (the largest m whose forced crossing number is still below Z(r)) is
the recursive bound of the target's own recursive.py, which is prior work of the
same lane and is used here unchanged; the point of this script is that the floors
and the row arithmetic do not depend on the target's code.

usage: python3 indep_frontier.py [r]
"""
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'target'))
import recursive as R
import verify_range as V


def ky(r, n):
    if r <= 2:
        return 0 if r <= 1 else 1
    return -(-((r + 1) * (r - 2) * n - r * (r - 3)) // (2 * (r - 1)))


def cor7(r, n):
    return -(-((r - 1) * n + (2 * r - 6)) // 2)


def cor5(r, n):
    p = n - r
    if not (2 <= p <= r - 1):
        return 0
    return -(-((r - 1) * n + p * (r - p) - 1) // 2)


def main():
    r = int(sys.argv[1]) if len(sys.argv) > 1 else 29
    NMAX = 80
    _L = R.build(NMAX, rounds=3)
    zz = V.Z(r)
    print(f'r = {r}: Z({r}) = {zz} = (14*14*13*13)//4 for r=29' if r == 29 else f'r = {r}: Z = {zz}')
    print(f'orders n <= r+4 = {r + 4} are settled by Barat-Toth Corollary 11')
    rows = 0
    surv = []
    for n in range(r + 5, NMAX + 1):
        lo = max(ky(r, n), cor7(r, n), cor5(r, n))
        hi = max([q for q in range(len(_L[n])) if _L[n][q] < zz], default=-1)
        if lo <= hi:
            surv.append((n, lo, hi))
            rows += hi - lo + 1
    print('surviving orders (my floors vs the recursive ceiling, no Cranston band used):')
    for n, lo, hi in surv:
        which = max([('KY', ky(r, n)), ('BT7', cor7(r, n)), ('BT5', cor5(r, n))], key=lambda t: t[1])
        print(f'   n={n}  m in [{lo}, {hi}]  ({hi - lo + 1} rows)   binding floor: {which[0]}')
    print(f'total {len(surv)} orders, {rows} rows')
    print()
    print('order 2r-2 = %d: Gallai join decompositions within the edge budget must be checked '
          'separately (the target finds none)' % (2 * r - 2))


if __name__ == '__main__':
    main()

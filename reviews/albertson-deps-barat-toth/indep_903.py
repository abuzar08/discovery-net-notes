"""reviewer-1: independent check of the computational claims of h2903.

My own floors, from the statements as printed in the EJC version of Barat-Toth
(EJC 17 (2010) #R73), against the target's recursive ceiling (prior machinery of
this lane, used as given):

  Kostochka-Yancey   e >= ((r+1)(r-2)n - r(r-3)) / (2(r-1))
  BT Corollary 7     2m >= (r-1)n + (2r-6)
  BT Corollary 5     2m >= (r-1)n + p(r-p) - 1     for p = n-r in [2, r-1]

Checks: (a) the PART 3 table of deps.py at r = 28; (b) the claim that the floors
alone leave only n = 52 (m in [701,702]) and n = 53 (m = 713) at r = 27, without
Sadhu Theorem 1.3 and without Cranston's bands; (c) which orders Corollary 5
closes that Corollary 7 does not.

usage: python3 indep_903.py
"""
import recursive as R
import verify_range as V

NMAX = 80
_L = R.build(NMAX, rounds=3)


def ky(r, n):
    return -(-((r + 1) * (r - 2) * n - r * (r - 3)) // (2 * (r - 1)))


def cor7(r, n):
    return -(-((r - 1) * n + (2 * r - 6)) // 2)


def cor5(r, n):
    p = n - r
    if not (2 <= p <= r - 1):
        return 0
    return -(-((r - 1) * n + p * (r - p) - 1) // 2)


def ceiling(r, n):
    zz = V.Z(r)
    return max([q for q in range(len(_L[n])) if _L[n][q] < zz], default=-1)


def main():
    print('(a) my floors against the recursive ceiling, r = 28 '
          '(h2903 PART 3 rows)')
    print('    n     KY   Cor7   Cor5   ceiling   rows with Cor7 only -> with Cor5')
    for n in (33, 34, 50, 51, 52, 53, 54, 55):
        k, c7, c5, ce = ky(28, n), cor7(28, n), cor5(28, n), ceiling(28, n)
        lo7 = max(k, c7)
        lo5 = max(k, c7, c5)
        r7 = max(0, ce - lo7 + 1)
        r5 = max(0, ce - lo5 + 1)
        tag = '   <- closed by Corollary 5' if r5 == 0 and r7 > 0 else ''
        print(f'   {n:3d}  {k:5d}  {c7:5d}  {c5:5d}   {ce:5d}      {r7:3d} -> {r5:3d}{tag}')
    print()
    print('(b) r = 27, floors only (no Sadhu, no Cranston band): surviving orders')
    surv = []
    for n in range(27 + 5, NMAX + 1):
        lo = max(ky(27, n), cor7(27, n), cor5(27, n))
        hi = ceiling(27, n)
        if lo <= hi:
            surv.append((n, lo, hi))
    for n, lo, hi in surv:
        print(f'   n={n}  m in [{lo}, {hi}]  ({hi - lo + 1} rows)')
    print(f'   => {[t[0] for t in surv]}, {sum(t[2] - t[1] + 1 for t in surv)} rows in total')
    print()
    print('(c) orders 32..55 at r = 27 that Corollary 5 closes but Corollary 7 does not:')
    only5 = []
    for n in range(32, 56):
        ce = ceiling(27, n)
        if max(ky(27, n), cor7(27, n)) <= ce < max(ky(27, n), cor7(27, n), cor5(27, n)):
            only5.append(n)
    print(f'   {only5}')


if __name__ == '__main__':
    main()

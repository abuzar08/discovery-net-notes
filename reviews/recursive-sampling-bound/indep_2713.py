r"""reviewer-1: independent implementation of the recursive integer-aware
sampling bound of h2713 (researcher-4), written from the lemma statement alone.

Base at \((n,q)\), rounded up and at least 0:
  * Euler: \(q - (3n-6)\);
  * the density sum \(2\,\mathrm{cr} \ge \sum_j \max(0, q - e_{j-1}(n))\) over
    \(3n-6,\ 4n-8,\ 5n-10,\ \lfloor 5.5n-11.5 \rfloor,\ 6n-12\);
  * Bungener-Kaufmann \(5q - \tfrac{203}{9}(n-2)\) and
    \(\tfrac{37}{9}q - \tfrac{155}{9}(n-2)\).
Recursion, for \(4 \le s < n\):
  \(L(n,q) \ge \lceil \binom{n}{s}\hat L(s, q\binom{n-2}{s-2}/\binom{n}{s})
  / \binom{n-4}{s-4} \rceil\).
Exact integer and Fraction arithmetic throughout.
"""
import bisect
import sys
from fractions import Fraction
from math import comb

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 54


def base(n, q):
    vals = [Fraction(q - (3 * n - 6))]
    dens = [3 * n - 6, 4 * n - 8, 5 * n - 10, (11 * n - 23) // 2, 6 * n - 12]
    s = sum(max(0, q - e) for e in dens)
    vals.append(Fraction(s, 2))
    vals.append(Fraction(45 * q - 203 * (n - 2), 9))
    vals.append(Fraction(37 * q - 155 * (n - 2), 9))
    m = max(vals)
    if m <= 0:
        return 0
    return -((-m.numerator) // m.denominator)


def hull_of(row):
    """lower convex hull of the points (q, row[q]), as two parallel lists"""
    hx, hy = [], []
    for q, y in enumerate(row):
        while len(hx) >= 2:
            if (hy[-1] - hy[-2]) * (q - hx[-1]) >= (y - hy[-1]) * (hx[-1] - hx[-2]):
                hx.pop(); hy.pop()
            else:
                break
        hx.append(q); hy.append(y)
    return hx, hy


def hull_eval(hull, qbar):
    hx, hy = hull
    i = bisect.bisect_right(hx, qbar) - 1
    if i >= len(hx) - 1:
        return Fraction(hy[-1])
    x1, y1, x2, y2 = hx[i], hy[i], hx[i + 1], hy[i + 1]
    return y1 + Fraction((y2 - y1) * (qbar - x1), x2 - x1)


def build(nmax=NMAX):
    L, hulls = {}, {}
    for n in range(3, nmax + 1):
        M = comb(n, 2)
        row = [base(n, q) for q in range(M + 1)]
        for s in range(4, n):
            hs = hulls[s]
            a, b = comb(n, s), comb(n - 4, s - 4)
            c = comb(n - 2, s - 2)
            for q in range(M + 1):
                qbar = Fraction(q * c, a)
                val = Fraction(a, b) * hull_eval(hs, qbar)
                cand = -((-val.numerator) // val.denominator)
                if cand > row[q]:
                    row[q] = cand
        L[n] = row
        hulls[n] = hull_of(row)
    return L


def Zh(n):
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4


CRK = {5: 1, 6: 3, 7: 9, 8: 18, 9: 36, 10: 60, 11: 100, 12: 150}


def main():
    L = build()
    print(f'my own table to n = {NMAX}')
    print('  worked values of the contribution:')
    for (n, q, pub) in ((24, 132, 164), (50, 634, 4778), (50, 635, 4804),
                        (53, 713, 6071), (53, 714, 6100), (53, 715, 6130),
                        (54, 726, 6134)):
        mine = L[n][q]
        print(f'    L({n},{q}) = {mine}   published {pub}   '
              f'{"agree" if mine == pub else "DIFFER"}')
    if 32 in L:
        print(f'  L(32,383) = {L[32][383]} (the incumbent of the h3285 lane, '
              f'published 3022)')
    print('  small exact values: L(5,10) = %d (cr(K_5) = 1), L(6,15) = %d '
          '(cr(K_6) = 3)' % (L[5][10], L[6][15]))

    print('  my own soundness checks:')
    bad = []
    for n in range(5, NMAX + 1):
        ub = CRK.get(n, Zh(n))
        if L[n][comb(n, 2)] > ub:
            bad.append(('K_n', n, L[n][comb(n, 2)], ub))
        for a in range(5, n + 1):                       # K_a plus isolates
            if L[n][comb(a, 2)] > CRK.get(a, Zh(a)):
                bad.append(('K_a+isolates', (n, a), L[n][comb(a, 2)],
                            CRK.get(a, Zh(a))))
        for a in range(1, n):                            # complete bipartite
            b = n - a
            zar = (a // 2) * ((a - 1) // 2) * (b // 2) * ((b - 1) // 2)
            if L[n][a * b] > zar:
                bad.append(('K_ab', (a, b), L[n][a * b], zar))
        for a in range(5, n - 4):                        # K_a u K_b
            b = n - a
            if b >= 5 and L[n][comb(a, 2) + comb(b, 2)] > \
                    CRK.get(a, Zh(a)) + CRK.get(b, Zh(b)):
                bad.append(('K_a u K_b', (a, b),
                            L[n][comb(a, 2) + comb(b, 2)],
                            CRK.get(a, Zh(a)) + CRK.get(b, Zh(b))))
        mono = all(L[n][q] <= L[n][q + 1] for q in range(comb(n, 2)))
        if not mono:
            bad.append(('monotone', n, None, None))
        if any(L[n][q] != 0 for q in range(min(3 * n - 6, comb(n, 2)) + 1)):
            bad.append(('zero below 3n-6', n, None, None))
    print(f'    upper-bound, monotonicity and vanishing checks: '
          f'{"all pass" if not bad else bad[:6]}')
    print(f'    margin at K_54: Z(54) = {Zh(54)}, L = {L[54][comb(54,2)]}, '
          f'gap {Zh(54) - L[54][comb(54,2)]}')


if __name__ == '__main__':
    main()

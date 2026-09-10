r"""reviewer-1: independent audit of inequality (6), the U-degree bound.

Lower side. At order 58 with \(r = 29\), \(x_z = 29 - d_H(z)\), so
\(\sum_{z \in U} d_H(z) = 29u - \sum_{z \in U} x_z\). Every \(z \in R\) has
\(x_z \ge 1\) and \(\sum_{z \in R} x_z = X = 2m - 1624\), so
\(\sum_{z \in U} x_z \le X - (\lvert R\rvert - u)\) and
\(\sum_{z \in U} d_H(z) \ge 28u + \lvert R\rvert - X\); if \(w \notin U\) then one
of the omitted terms is at least 25 rather than 1, adding 24.

Upper side. A \(U\)-vertex has no \(A\)-neighbour, so its \(L\)-neighbours lie in
\(S_L\) or among the \(3k\) deleted triangle vertices and its \(H[R]\)-neighbours
in its own component or \(S_R\), giving
\(u(s_L + 3k + s_R) + \sum_i 2\,\mathrm{tur}(n_i)\) over the \(t\) components of
\(U\). The last sum is at most \(2\,\mathrm{tur}(u - t + 1)\), which is the step
worth checking.
"""
import itertools


def tur(x):
    return 0 if x < 2 else x * x // 3


def max_component_sum(u, t):
    """max of sum tur(n_i) over t positive parts summing to u, by dynamic
    programming"""
    NEG = -1
    dp = [[NEG] * (u + 1) for _ in range(t + 1)]
    dp[0][0] = 0
    for parts in range(1, t + 1):
        for rem in range(parts, u + 1):
            best = NEG
            for n in range(1, rem - (parts - 1) + 1):
                prev = dp[parts - 1][rem - n]
                if prev > NEG:
                    v = prev + tur(n)
                    if v > best:
                        best = v
            dp[parts][rem] = best
    return dp[t][u]


def main():
    print('the concentration step: max sum of tur(n_i) over t parts summing to u')
    bad = []
    for u in range(1, 33):
        for t in range(1, u + 1):
            got, claim = max_component_sum(u, t), tur(u - t + 1)
            if got != claim:
                bad.append((u, t, got, claim))
    print(f'   checked every 1 <= t <= u <= 32: '
          f'{"the maximum is always tur(u - t + 1)" if not bad else bad[:5]}')
    print()
    print('the excess budget X = 2m - 1624 at the three rows:')
    for m in (838, 839, 840):
        print(f'   m = {m}: X = {2*m - 1624}')
    print('   so X <= 56, as the inequality assumes')
    print()
    print('the lower side, symbolically checked at sample points '
          '(|R|, u, X, w outside U):')
    for RSZ, u, X, out in ((28, 10, 56, True), (24, 6, 52, False),
                           (32, 20, 56, True)):
        naive = 29 * u - (X - (RSZ - u)) + (24 if out else 0)
        stated = 28 * u + RSZ - X + (24 if out else 0)
        print(f'   |R| = {RSZ}, u = {u}, X = {X}, w outside U = {out}: '
              f'29u - (X - (|R| - u)) = {naive}, stated bound {stated} -> '
              f'{"identical" if naive == stated else "DIFFER"}')


if __name__ == '__main__':
    main()

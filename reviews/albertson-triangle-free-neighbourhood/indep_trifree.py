r"""reviewer-1: audit of researcher-2's triangle-free-neighbourhood condition.

For a low vertex \(v\) lying in a single block \(Q_i\) of order \(q_i\), the
per-block identity gives \(\lvert N_H(v) \cap R\rvert = \lvert R\rvert - 28 +
D_v\) with \(D_v = q_i - 1\), so \(\rho_i = q_i + \lvert R\rvert - 29\); that set
is triangle-free in \(H\) because \(v\) plus a triangle of it would be a
\(K_4\). Splitting \(R\) into that set and the rest bounds
\(e(H[R]) \le \lfloor \rho^2/4 \rfloor + \rho(\lvert R\rvert - \rho) +
\lfloor (\lvert R\rvert - \rho)^2/3 \rfloor\).

I check the derivation's arithmetic, the published pair of values, the boundary
condition \(\rho \le \lvert R\rvert\), and where the new bound beats the
\(w\)-sharpened cap.
"""


def wcap(R):
    return (R - 1) * (R - 1) // 3 + 4


def tricap(R, q):
    rho = q + R - 29
    if rho < 0:
        return None, rho
    if rho > R:
        return 'impossible', rho          # more R-neighbours than R has vertices
    out = R - rho
    return rho * rho // 4 + rho * out + out * out // 3, rho


def main():
    print('the published pair: |R| = 28, q_1 = 27')
    v, rho = tricap(28, 27)
    print(f'   rho = {rho}, new bound = {v} (published 222), w-cap = {wcap(28)} '
          f'(published 247) -> '
          f'{"both match" if v == 222 and wcap(28) == 247 else "MISMATCH"}')
    print()
    print('the boundary condition')
    print('   rho <= |R| forces q_i <= 29; the lane has q_1 <= 28 from '
          'Stehlik\'s partition, so rho <= |R| - 1 always')
    bad = [(R, q) for R in range(11, 33) for q in range(30, 40)
           if tricap(R, q)[0] == 'impossible']
    print(f'   parameter pairs with q_i >= 30 where the identity alone is '
          f'contradictory: {len(bad)} (all of them, as expected)')
    print()
    print('where the new bound beats the w-sharpened cap')
    print('   |R|   q_1 range with a win        smallest winning q_1   gain at q_1 = |L| cap')
    for R in (11, 16, 21, 26, 28, 32):
        wins = []
        for q in range(2, 29):
            t, rho = tricap(R, q)
            if isinstance(t, int) and t < wcap(R):
                wins.append((q, wcap(R) - t))
        if wins:
            print(f'   {R:3d}   {wins[0][0]}..{wins[-1][0]:<24d} {wins[0][0]:>10d}'
                  f'            {wins[-1][1]:>6d}')
        else:
            print(f'   {R:3d}   none')
    print()
    print('   so the condition is strictly stronger exactly when q_1 is large '
          'relative to |R|,')
    print('   which is the regime the document identifies; the two caps are '
          'incomparable in general')


if __name__ == '__main__':
    main()

r"""reviewer-1: independent reconstruction of the Mohar Conjecture 5 status map.

The recursion, re-derived: deleting one of the \(2t\) covered vertices of
\(M_{n,t}\) leaves \(M_{n-1,t-1}\), deleting one of the \(n-2t\) uncovered ones
leaves \(M_{n-1,t}\), and each crossing survives \(n-4\) of the \(n\) deletions,
so \((n-4)\mathrm{cr}(M_{n,t}) \ge 2t\,\mathrm{cr}(M_{n-1,t-1}) +
(n-2t)\,\mathrm{cr}(M_{n-1,t})\).

Seeds used: Hill's \(Z(n)\) for \(t = 0\) and Chia-Lee for \(t = 1\), both at
\(n \le 12\); Ho's \(\mathrm{cr}(K_{2,2,2,2}) = 6\); and the three small values
the lane computed, of which I verified \(\mathrm{cr}(M_{7,2}) = 4\) and
\(\mathrm{cr}(M_{7,3}) = 3\) myself from Euler plus a two-page drawing.
"""
from math import comb


def Z(n):
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4


def euler(n, t):
    m = comb(n, 2) - t
    return max(0, m - (3 * n - 6))


def prediction(n, t):
    assert n % 2 == 0
    k = n // 2
    return Z(n) - t * (k - 1) * (k - 2) // 2


KNOWN = {}
for n in range(5, 13):
    KNOWN[(n, 0)] = Z(n)
    KNOWN[(n, 1)] = Z(n) - comb((n - 1) // 2, 2)
KNOWN[(6, 2)] = 1
KNOWN[(6, 3)] = 0
KNOWN[(7, 2)] = 4
KNOWN[(7, 3)] = 3
KNOWN[(8, 4)] = 6


def main():
    lb = dict(KNOWN)
    print('the recursion applied upward, with the stated seeds:')
    for n in range(6, 13):
        for t in range(2, n // 2 + 1):
            if (n, t) in KNOWN:
                continue
            a = lb.get((n - 1, t - 1))
            b = lb.get((n - 1, t)) if n - 2 * t > 0 else 0
            if a is None or b is None:
                continue
            num = 2 * t * a + (n - 2 * t) * b
            val = -(-num // (n - 4))
            lb[(n, t)] = max(val, euler(n, t))
    pub = {(8, 2): 10, (8, 3): 8,
           (10, 2): 42, (10, 3): 34, (10, 4): 28, (10, 5): 24,
           (12, 2): 118, (12, 3): 101, (12, 4): 87, (12, 5): 75, (12, 6): 66}
    print('   n  t   my lower bound   published   prediction   verdict')
    bad = 0
    for (n, t), p in sorted(pub.items()):
        mine = lb.get((n, t))
        if mine is None:
            print(f'  {n:3d} {t:2d}   (no value)  {p:12d}'); bad += 1; continue
        pred = prediction(n, t)
        ok = mine == p
        if not ok:
            bad += 1
        print(f'  {n:3d} {t:2d} {mine:12d} {p:12d} {pred:12d}   '
              f'{"agree" if ok else "DIFFER"}'
              f'{"" if mine <= pred else "   LOWER BOUND EXCEEDS PREDICTION"}')
    print(f'   rows disagreeing with the published map: {bad}')
    print()
    known_even = [(n, t) for (n, t) in KNOWN if n % 2 == 0 and t <= n // 2]
    print(f'   verified even cases in the seed set: {len(known_even)} '
          f'{sorted(known_even)}')
    print(f'   they all equal the prediction: '
          f'{all(KNOWN[(n,t)] == prediction(n,t) for n, t in known_even)}')
    opens = [(n, t) for n in range(6, 13, 2) for t in range(0, n // 2 + 1)
             if (n, t) not in KNOWN]
    print(f'   open even cases at n <= 12: {len(opens)}')
    print(f'   no lower bound exceeds its prediction: '
          f'{all(lb.get((n,t), 0) <= prediction(n,t) for n, t in opens)}')
    print()
    print('   odd-order values the even rows depend on, from the same recursion:')
    for nt in ((9, 2), (9, 3), (9, 4), (11, 2), (11, 3)):
        print(f'     M_{nt[0]},{nt[1]}: lower bound {lb.get(nt)}')


if __name__ == '__main__':
    main()

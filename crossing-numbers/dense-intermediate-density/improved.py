"""Strengthen the base of the recursion with known bounds on cr(K_n).

L(n,q) must hold for every n-vertex q-edge graph.  At q = C(n,2) there is only
one such graph, K_n, so any published lower bound on cr(K_n) is a valid base
value there -- and the published base bounds (Euler, the density sum, and
Buengener-Kaufmann) are far weaker at that point.  Raising the right-hand end of
L(n, .) lifts its lower convex envelope, which is what the recursion consumes.

Values used:
  * cr(K_n) exactly for n <= 12 (settled; equals Z(n));
  * cr(K_n) >= 0.8594 * Z(n) for n >= 13, de Klerk, Pasechnik and Schrijver's
    semidefinite bound, which is the standard published constant.
"""
from fractions import Fraction as F
from math import comb

import recursive_sampling as RS

EXACT = {5: 1, 6: 3, 7: 9, 8: 18, 9: 36, 10: 60, 11: 100, 12: 150}


def Z(n):
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4


def crKn_lower(n):
    if n < 5:
        return 0
    if n in EXACT:
        return EXACT[n]
    return RS.ceil_frac(F(8594, 10000) * Z(n))


def build(nmax, use_kn=True):
    L, env = {}, {}
    for n in range(3, nmax + 1):
        qmax = comb(n, 2)
        vals = [RS.base_bound(n, q) for q in range(qmax + 1)]
        if use_kn:
            vals[qmax] = max(vals[qmax], crKn_lower(n))
        for s in range(4, n):
            cnk, cn4, cn2 = comb(n, s), comb(n - 4, s - 4), comb(n - 2, s - 2)
            E = env[s]
            for q in range(qmax + 1):
                v = RS.ceil_frac(F(cnk) * E(F(q * cn2, cnk)) / cn4)
                if v > vals[q]:
                    vals[q] = v
        if use_kn:
            vals[qmax] = max(vals[qmax], crKn_lower(n))
        L[n] = vals
        env[n] = RS.Envelope(vals)
    return L


if __name__ == '__main__':
    n, q = 32, 383
    old = RS.build(n)
    new = build(n)
    print(f"{'n':>3} {'cr(K_n) base':>13} {'old L(n,C(n,2))':>16} "
          f"{'new':>8}")
    for m in (12, 16, 20, 24, 28, 32):
        print(f"{m:>3} {crKn_lower(m):>13} {old[m][comb(m,2)]:>16} "
              f"{new[m][comb(m,2)]:>8}")
    print()
    print(f"published L(32,383) = {old[n][q]}")
    print(f"with cr(K_n) bases   = {new[n][q]}")
    print(f"gain = {new[n][q] - old[n][q]};  target 3557; ceiling 4644")

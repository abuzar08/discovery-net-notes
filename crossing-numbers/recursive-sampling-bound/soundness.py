"""Soundness suite for the recursive integer-aware sampling bound.

A lower bound on the crossing number is worthless if it can exceed the truth.
This suite checks L(n,q) against every value that is settled or achievable by
an explicit drawing, for all n <= NMAX and all q those families reach:

  * L(n, C(n,2)) against cr(K_n): exact for n <= 12, and against Z(n) (Hill's
    two-circle drawing) beyond -- Z(n) is an upper bound on cr(K_n), so nothing
    here depends on the Harary-Hill conjecture;
  * L(n, C(a,2)) against cr(K_a) for K_a plus isolated vertices, every a <= n;
  * L(n, ab) against the Zarankiewicz drawing Z(a,b) for every K_{a,b};
  * disjoint unions K_a u K_b and K_a u K_{c,d}, crossing number being additive
    over components;
  * monotonicity of L(n, .) in q;
  * L(n,q) = 0 whenever q <= 3n-6, since such a graph may be planar.

    python3 soundness.py [NMAX]
"""
import sys
from math import comb

from recursive_sampling import build

CR_K = {5: 1, 6: 3, 7: 9, 8: 18, 9: 36, 10: 60, 11: 100, 12: 150}


def Z(r):
    return ((r // 2) * ((r - 1) // 2) * ((r - 2) // 2) * ((r - 3) // 2)) // 4


def Zb(a, b):
    return (a // 2) * ((a - 1) // 2) * (b // 2) * ((b - 1) // 2)


def ub_K(a):
    return CR_K.get(a, Z(a))


def main(nmax=54):
    L = build(nmax)
    bad, checks = [], 0

    def test(n, q, ub, desc):
        nonlocal checks
        if q > comb(n, 2):
            return
        checks += 1
        if L[n][q] > ub:
            bad.append((desc, n, q, L[n][q], ub))

    for n in range(5, nmax + 1):
        for a in range(1, n + 1):
            test(n, comb(a, 2), ub_K(a), f"K_{a} + isolated")
            b = n - a
            if b >= 1:
                test(n, a * b, Zb(a, b), f"K_{{{a},{b}}}")
                test(n, comb(a, 2) + comb(b, 2), ub_K(a) + ub_K(b),
                     f"K_{a} u K_{b}")
                for c in range(1, b + 1):
                    d = b - c
                    if d >= 1:
                        test(n, comb(a, 2) + c * d, ub_K(a) + Zb(c, d),
                             f"K_{a} u K_{{{c},{d}}}")

    mono = all(L[n][q] <= L[n][q + 1]
               for n in L for q in range(len(L[n]) - 1))
    vanish = all(L[n][q] == 0
                 for n in L for q in range(min(3 * n - 6, comb(n, 2)) + 1))

    print(f"recursive integer-aware sampling bound, n <= {nmax}")
    print(f"  upper-bound checks run          : {checks}")
    print(f"  never exceeds an achievable value: "
          f"{'yes' if not bad else 'NO -- ' + str(bad[:3])}")
    print(f"  monotone in q                   : {mono}")
    print(f"  vanishes for q <= 3n-6          : {vanish}")
    print(f"  reproduces cr(K_5) = {L[5][10]}, cr(K_6) = {L[6][15]} exactly")
    print(f"  margin at K_{nmax}: bound {L[nmax][comb(nmax,2)]} "
          f"vs Z({nmax}) = {Z(nmax)}")
    assert not bad and mono and vanish

    print("\nworked values")
    for (n, q, note) in [(24, 132, "Ackerman 4-planar density 6n-12"),
                         (50, 634, "mean 50-subset count for (53,714)"),
                         (50, 635, ""),
                         (53, 713, "Albertson r=27 frontier row"),
                         (53, 714, ""), (53, 715, ""), (54, 726, "")]:
        print(f"  L({n},{q}) = {L[n][q]}" + (f"   [{note}]" if note else ""))
    print("\nall soundness checks pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 54))

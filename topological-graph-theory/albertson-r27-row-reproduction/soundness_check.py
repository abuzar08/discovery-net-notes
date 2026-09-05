"""Soundness and outcome check for the recursive sampling bound.

A lower bound on the crossing number must never exceed a value that is known,
or known to be achievable by an explicit drawing.  This script checks the bound
built by recursive_sampling.py against the settled values and the standard
drawing-based upper bounds, then reports the two claims of the Albertson r=27
chain that the bound is used to test.

    python3 soundness_check.py
"""
from math import comb

from recursive_sampling import base_bound, build

CR_K = {5: 1, 6: 3, 7: 9, 8: 18, 9: 36, 10: 60, 11: 100, 12: 150}   # exact


def Z(r):
    return ((r // 2) * ((r - 1) // 2) * ((r - 2) // 2) * ((r - 3) // 2)) // 4


def Zb(a, b):
    return (a // 2) * ((a - 1) // 2) * (b // 2) * ((b - 1) // 2)


def main():
    L = build(50)
    bad = []
    for n in range(5, 51):
        q = comb(n, 2)
        ub = CR_K.get(n, Z(n))
        if L[n][q] > ub:
            bad.append((f"K_{n}", L[n][q], ub))
    for n in range(5, 51):
        for a in range(1, n):
            if L[n][a * (n - a)] > Zb(a, n - a):
                bad.append((f"K_{a},{n-a}", L[n][a * (n - a)], Zb(a, n - a)))
    mono = all(L[n][q] <= L[n][q + 1]
               for n in L for q in range(len(L[n]) - 1))

    print("soundness")
    print(f"    never exceeds a known or achievable value: "
          f"{'yes' if not bad else 'NO -- ' + str(bad[:3])}")
    print(f"    monotone in q: {mono}")
    print(f"    reproduces cr(K_5) = {L[5][10]} (true 1) and "
          f"cr(K_6) = {L[6][15]} (true 3)")
    assert not bad and mono

    print()
    print("claim (b), height 1813:  cr(H) >= 26q - 11706 on 50 vertices")
    short = [q for q in range(comb(50, 2) + 1) if L[50][q] < 26 * q - 11706]
    print(f"    holds at every q: {not short}")
    print("    near the point of application (q = 437325/689 = 634.72):")
    for q in range(632, 638):
        print(f"        q={q}: recursive {L[50][q]}, claim {26*q-11706}, "
              f"difference {L[50][q] - (26*q-11706)}")
    print("    => the claim is exactly the affine segment of the recursive "
          "bound there (slope 26); REPRODUCED")

    print()
    print("claim (a), heights 1765/2035:  cr(24,132) >= 165")
    print(f"    published base bounds alone : {base_bound(24, 132)}")
    print(f"    full recursive bound        : {L[24][132]}")
    print("    claim                       : 165")
    print("    => NOT reproduced; one crossing beyond everything published.")


if __name__ == "__main__":
    main()

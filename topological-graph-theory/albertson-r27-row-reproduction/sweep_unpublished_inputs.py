"""Falsification sweep for the two unpublished inputs of the Albertson r=27
chain:

  (a) cr(H) >= 5e - 495     for every 24-vertex e-edge simple graph H
  (b) cr(H) >= 26q - 11706  for every 50-vertex q-edge simple graph H

Each is tested against graph families whose crossing numbers have rigorous
drawing-based UPPER bounds: complete graphs (cr(K_r) <= Z(r), the two-circle
drawing), complete bipartite graphs (cr(K_{a,b}) <= Z(a,b), Zarankiewicz's
drawing), and disjoint unions of these (crossing number is additive over
components).  A violation would refute the claim; none is found.

This is a consistency check only.  The margins are large, so it does not
seriously stress either claim: these families are far from the extremal-density
regime where (a) and (b) are applied.  Standard library only.
"""
from math import comb


def Z(r):
    return ((r // 2) * ((r - 1) // 2) * ((r - 2) // 2) * ((r - 3) // 2)) // 4


def Zb(a, b):
    return (a // 2) * ((a - 1) // 2) * (b // 2) * ((b - 1) // 2)


def sweep(n, claim, name):
    viol = []
    tight = None

    def test(q, ub, desc):
        nonlocal tight
        if q > comb(n, 2):
            return
        c = claim(q)
        if c > ub:
            viol.append((desc, q, ub, c))
        if tight is None or ub - c < tight[0]:
            tight = (ub - c, desc, q)

    for a in range(1, n + 1):
        test(comb(a, 2), Z(a), f"K_{a}")
        b = n - a
        if b >= 1:
            test(a * b, Zb(a, b), f"K_{{{a},{b}}}")
    for a in range(1, n):
        b = n - a
        test(comb(a, 2) + comb(b, 2), Z(a) + Z(b), f"K_{a} u K_{b}")
        for c in range(1, n - a):
            d = n - a - c
            if d >= 1:
                test(comb(a, 2) + c * d, Z(a) + Zb(c, d), f"K_{a} u K_{{{c},{d}}}")
    for a in range(1, n):
        for b in range(1, n - a):
            for c in range(1, n - a - b):
                d = n - a - b - c
                if d >= 1:
                    test(a * b + c * d, Zb(a, b) + Zb(c, d),
                         f"K_{{{a},{b}}} u K_{{{c},{d}}}")

    print(f"{name}")
    print(f"    {'NO VIOLATION' if not viol else 'VIOLATIONS: ' + str(viol[:3])}")
    print(f"    tightest margin {tight[0]} at {tight[1]} (q = {tight[2]})")
    return viol


if __name__ == "__main__":
    v = sweep(50, lambda q: 26 * q - 11706,
              "(b) 50-vertex claim  cr >= 26q - 11706")
    v += sweep(24, lambda q: 5 * q - 495,
               "(a) 24-vertex claim  cr >= 5e - 495")
    raise SystemExit(1 if v else 0)

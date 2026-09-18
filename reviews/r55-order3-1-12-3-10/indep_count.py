r"""reviewer-1: independent count of the labelled \((5,5)\)-good \(Z_3\)-graphs on
four 3-cycles — the completeness number the cube decomposition rests on.

A \(Z_3\)-invariant graph on the twelve vertices of four 3-cycles is an
assignment to the 22 orbits of vertex pairs (18 cross-cycle, 4 internal). Such a
graph is good iff no 5-subset is a clique and none is independent, which is a
condition on the orbits the subset meets. With only 22 variables the count is a
direct enumeration over \(2^{22}\) assignments, done here with bit masks.
"""
import itertools

import numpy as np

N = 12
CYCLES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11)]


def sigma():
    p = list(range(N))
    for c in CYCLES:
        for i, v in enumerate(c):
            p[v] = c[(i + 1) % 3]
    return p


def pair_orbits(p):
    orb, nxt = {}, 0
    for u in range(N):
        for v in range(u + 1, N):
            if (u, v) in orb:
                continue
            a, b = u, v
            while True:
                e = (min(a, b), max(a, b))
                if e in orb:
                    break
                orb[e] = nxt
                a, b = p[a], p[b]
            nxt += 1
    return orb, nxt


def main():
    p = sigma()
    orb, north = pair_orbits(p)
    print(f'four 3-cycles on {N} vertices: {north} pair orbits '
          f'(18 cross-cycle + 4 internal expected)')
    masks = []
    for S in itertools.combinations(range(N), 5):
        m = 0
        for a, b in itertools.combinations(S, 2):
            m |= 1 << orb[(a, b)]
        masks.append(m)
    masks = np.array(sorted(set(masks)), dtype=np.uint32)
    print(f'   5-subsets: {len(list(itertools.combinations(range(N), 5)))}, '
          f'distinct orbit supports: {len(masks)}')
    x = np.arange(1 << north, dtype=np.uint32)
    good = np.ones(x.shape, dtype=bool)
    for m in masks:
        both = x & m
        good &= (both != m) & (both != 0)
    cnt = int(good.sum())
    print(f'   labelled (5,5)-good Z_3-graphs on four cycles: {cnt}')
    print(f'   published completeness count: 2541538 -> '
          f'{"match" if cnt == 2541538 else "DIFFER"}')


if __name__ == '__main__':
    main()

r"""reviewer-1: independent checks on the degree-window control.

A degree is a weighted sum over pair orbits: for a vertex \(v\) and an orbit
\(o\), the weight is the number of pairs of \(o\) containing \(v\), so
\(d(v) = \sum_o w_{v,o} x_o\). The control's two failure modes are those weights
and the totaliser. Here I check the weight side from scratch: the dichotomy that
weights above 1 require a fixed point, the resulting collapse at
\(1^0 2^{21}\), the window \([17,24]\) on the catalogue, and the count of Klein
actions where multiplicities are live.
"""
import sys
from collections import Counter

sys.path.insert(0, '../r45')
sys.path.insert(0, '../r55o9')
from indep_r45 import graph6
from indep_o9 import perm_from_type, pair_orbits
from indep_inv import z2z2_actions

N = 42
CAT = '../r55auto/catalog/r55_42some.g6'


def weights(cycles):
    p = perm_from_type(cycles)
    orb, north = pair_orbits(p)
    w = [Counter() for _ in range(N)]
    for (u, v), o in orb.items():
        w[u][o] += 1
        w[v][o] += 1
    return orb, north, w


def main():
    print('(1) the weight dichotomy, computed for several cycle types')
    for name, cyc in (('1^0 2^21', [2] * 21), ('1^2 2^20', [1, 1] + [2] * 20),
                      ('1^6 9^4', [1] * 6 + [9] * 4), ('1^0 2^1 4^10', [2] + [4] * 10)):
        orb, north, w = weights(cyc)
        mx = max(max(c.values()) for c in w)
        nz = sum(len(c) for c in w)
        big = sum(1 for c in w for v in c.values() if v > 1)
        print(f'    {name:12s} orbits {north:3d}  nonzero weights {nz:5d}  '
              f'max weight {mx}  weights above 1: {big}')
    print('    argument: a weight above 1 needs two pairs of one orbit at the '
          'same vertex v,')
    print('    which for a cyclic action forces v to be fixed; a '
          'fixed-point-free involution has none.')
    print()
    print('(2) the degree window on the catalogue')
    lines = [l.strip() for l in open(CAT) if l.strip()]
    lo = hi = None
    bad = 0
    for l in lines:
        n, adj = graph6(l)
        ds = [bin(a).count('1') for a in adj]
        lo = min(ds) if lo is None else min(lo, min(ds))
        hi = max(ds) if hi is None else max(hi, max(ds))
        if min(ds) < 17 or max(ds) > 24:
            bad += 1
    print(f'    {len(lines)} graphs: degrees range {lo} to {hi}; outside '
          f'[17,24]: {bad}')
    print(f'    the window is forced: d <= R(4,5) - 1 = 24 and '
          f'41 - d <= 24 gives d >= 17')
    print()
    print('(3) the weighted-sum reconstruction, on the graphs with a '
          'fixed-point-free involution')
    sys.path.insert(0, '.')
    from indep_invcensus import involutions
    orb, north, w = weights([2] * 21)
    checked = mismatch = 0
    for l in lines:
        n, adj = graph6(l)
        invs, _ = involutions(adj)
        real = [q for q in invs if any(q[i] != i for i in range(n))]
        if not real:
            continue
        q = real[0]
        # relabel the graph so that the involution is the standard 2^21 layout
        pairs, seen = [], set()
        for v in range(n):
            if v in seen:
                continue
            pairs.append((v, q[v]))
            seen.add(v)
            seen.add(q[v])
        lab = {}
        for i, (a, b) in enumerate(pairs):
            lab[a], lab[b] = 2 * i, 2 * i + 1
        radj = [0] * n
        for u in range(n):
            for v in range(n):
                if (adj[u] >> v) & 1:
                    radj[lab[u]] |= 1 << lab[v]
        val = {}
        ok = True
        for (u, v), o in orb.items():
            bit = (radj[u] >> v) & 1
            if o in val and val[o] != bit:
                ok = False
                break
            val[o] = bit
        if not ok:
            mismatch += 1
            continue
        for v in range(n):
            d = sum(w[v][o] * val[o] for o in w[v])
            if d != bin(radj[v]).count('1'):
                mismatch += 1
                break
        checked += 1
    print(f'    graphs checked: {checked}; weighted sums disagreeing with the '
          f'true degrees: {mismatch}')
    print()
    print('(4) where the multiplicities are live at order 4')
    acts = z2z2_actions(ordered=False)
    live = [a for a in acts if a[0] >= 1 and a[2] >= 1]
    print(f'    Klein actions (up to relabelling): {len(acts)}; with a fixed '
          f'point and a regular orbit: {len(live)} (published 855)')


if __name__ == '__main__':
    main()

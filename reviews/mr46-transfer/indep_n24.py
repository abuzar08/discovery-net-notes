r"""reviewer-1: the \(n = 24\) half of MR46-TRANSFER.md, from McKay's complete
catalogue, with my own decoder and my own statistics."""
import collections
import json
import sys

from indep_r45 import graph6, edges, has_clique, has_independent

CAT = 'dl/r45_24.g6'
T45 = ('../../notes/graph-ramsey-theory/r55-upper-bound-neighbourhood-edges/'
       't45_24.json')


def triangles(n, adj):
    t = 0
    for v in range(n):
        nb = adj[v]
        c = nb & ~((1 << (v + 1)) - 1)
        while c:
            u = (c & -c).bit_length() - 1
            c &= c - 1
            t += bin(adj[u] & nb & ~((1 << (u + 1)) - 1)).count('1')
    return t


def main():
    dist = collections.Counter()
    tri = collections.defaultdict(lambda: [10 ** 9, -1])
    cotri = collections.defaultdict(lambda: [10 ** 9, -1])
    mins = []
    full = (1 << 24) - 1
    for line in open(CAT):
        if not line.strip():
            continue
        n, adj = graph6(line)
        e = edges(n, adj)
        dist[e] += 1
        t = triangles(n, adj)
        a, b = tri[e]
        tri[e] = [min(a, t), max(b, t)]
        comp = [(~x) & full & ~(1 << i) for i, x in enumerate(adj)]
        ct = triangles(n, comp)
        a, b = cotri[e]
        cotri[e] = [min(a, ct), max(b, ct)]
        if e == 116:
            mins.append((n, adj))
    tot = sum(dist.values())
    print(f'catalogue: {tot} graphs of order 24')
    print(f'   edge range: {min(dist)} to {max(dist)}; '
          f'counts at the extremes: {dist[min(dist)]} at {min(dist)}, '
          f'{dist[max(dist)]} at {max(dist)}')
    print(f'   e45.json claims e_min(4,5,24) = 116, e_max = 132 -> '
          f'{"agree" if min(dist) == 116 and max(dist) == 132 else "DIFFER"}')
    print(f'   conjectured lower bound 113 for i = 24: '
          f'{"holds (116 >= 113)" if min(dist) >= 113 else "fails"}')

    print(f'   the {len(mins)} minimum-edge graphs, checked in full with my own '
          f'clique and independence searches:')
    ok = all(not has_clique(n, adj, 4) and not has_independent(n, adj, 5)
             for n, adj in mins)
    print(f'      all {len(mins)} are genuine (4,5,24)-graphs with 116 edges: '
          f'{ok}')

    pub = {int(k): v for k, v in json.load(open(T45)).items()}
    print('   triangle bounds per edge count, mine against t45_24.json:')
    bad = []
    for e in sorted(pub):
        mine = tri[e] + cotri[e] + [dist[e]]
        if mine != pub[e]:
            bad.append((e, mine, pub[e]))
    print(f'      rows compared: {len(pub)}; mismatches: '
          f'{bad if bad else "none — every [t_min, t_max, cot_min, cot_max, count] row agrees"}')
    print(f'      edge counts present in my scan but absent from the published '
          f'table: {sorted(set(dist) - set(pub))}')
    print(f'      Table IV rows 109-115 are claimed empty: my counts '
          f'{[dist.get(e, 0) for e in range(109, 116)]}')


if __name__ == '__main__':
    main()

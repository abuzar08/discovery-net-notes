r"""reviewer-1: skewness of the generalized Petersen graphs \(GP(4k,k)\), to check
researcher-4's corrected table and the \(2k-3\) hypothesis.

\(\mathrm{sk}(G)\) is the least number of edges whose deletion leaves a planar
graph. Any planarising set meets every Kuratowski subgraph, so the search
branches on the edges of one obstruction; deleted sets are memoised.
"""
import sys
from functools import lru_cache

import networkx as nx


def GP(n, k):
    G = nx.Graph()
    for i in range(n):
        G.add_edge(('u', i), ('u', (i + 1) % n))
        G.add_edge(('u', i), ('v', i))
        G.add_edge(('v', i), ('v', (i + k) % n))
    return G


def skew_le(G, k):
    seen = set()

    def rec(H, budget, deleted):
        ok, cert = nx.check_planarity(H, counterexample=True)
        if ok:
            return True
        if budget == 0:
            return False
        for e in sorted(tuple(sorted(map(str, x))) for x in cert.edges()):
            ee = tuple(eval(x) for x in e)
            nd = deleted | {e}
            if nd in seen:
                continue
            seen.add(nd)
            H.remove_edge(*ee)
            if rec(H, budget - 1, nd):
                H.add_edge(*ee)
                return True
            H.add_edge(*ee)
        return False
    return rec(G.copy(), k, frozenset())


def main():
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    for k in (2, 3, 4, 5):
        n = 4 * k
        G = GP(n, k)
        planar = nx.check_planarity(G, counterexample=False)[0]
        if planar:
            print(f'GP({n},{k}): {G.number_of_nodes()} vertices, '
                  f'{G.number_of_edges()} edges, planar so skewness 0')
            continue
        val = None
        for j in range(1, cap + 1):
            if skew_le(G, j):
                val = j
                break
        print(f'GP({n},{k}): {G.number_of_nodes()} vertices, '
              f'{G.number_of_edges()} edges, skewness '
              + (f'= {val}' if val is not None else f'>= {cap + 1}'), flush=True)


if __name__ == '__main__':
    main()

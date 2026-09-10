r"""reviewer-1: exact skewness of the 48 survivors, iterative deepening with
Kuratowski-guided branching and memoisation on the set of deleted edges."""
import sys
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache

import networkx as nx


def skew_le(G, k):
    """is there a planarising deletion of at most k edges?"""
    seen = set()

    def rec(H, dropped, deleted):
        ok, cert = nx.check_planarity(H, counterexample=True)
        if ok:
            return True
        if dropped == k:
            return False
        for e in sorted(tuple(sorted(x)) for x in cert.edges()):
            nd = deleted | {e}
            if nd in seen:
                continue
            seen.add(nd)
            H.remove_edge(*e)
            if rec(H, dropped + 1, nd):
                H.add_edge(*e)
                return True
            H.add_edge(*e)
        return False
    return rec(G.copy(), 0, frozenset())


def job(line):
    G = nx.from_graph6_bytes(line.encode())
    for k in range(1, 8):
        if skew_le(G, k):
            return line, G.number_of_edges(), k
    return line, G.number_of_edges(), 8


def main():
    lines = [l.split()[0] for l in open('n10_survivors.txt') if l.strip()]
    with ProcessPoolExecutor(max_workers=5) as ex:
        res = list(ex.map(job, lines))
    dist = {}
    for _, m, s in res:
        dist[s] = dist.get(s, 0) + 1
    print(f'exact skewness of the {len(res)} four-connected non-Hamiltonian '
          f'graphs at n = 10 (8 means at least 8):')
    for k in sorted(dist):
        print(f'   skewness {k}: {dist[k]} graphs')
    lo = min(dist)
    print(f'   every survivor has cr >= skewness >= {lo}, so any reduction to '
          f'cr = 3 must remove at least {lo - 3} crossings')
    open('skew_exact_values.txt', 'w').write(
        '\n'.join(f'{l} {m} {s}' for l, m, s in res) + '\n')


if __name__ == '__main__':
    main()

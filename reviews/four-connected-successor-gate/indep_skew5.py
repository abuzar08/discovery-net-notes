r"""reviewer-1: is the skewness of any of the 48 survivors at most 4?

A planarising deletion set must contain an edge of every Kuratowski subgraph, so
the search restricts to sets containing one edge of a fixed obstruction; the rest
is exhaustive over the remaining edges. This settles skewness >= 5 for the
survivors, sharpening the lower bound the successor gate needs.
"""
import itertools
from concurrent.futures import ProcessPoolExecutor

import networkx as nx


def skew_le(G, k):
    ok, cert = nx.check_planarity(G, counterexample=True)
    if ok:
        return True
    if k == 0:
        return False
    obstruction = sorted(tuple(sorted(e)) for e in cert.edges())
    for e in obstruction:
        H = G.copy()
        H.remove_edge(*e)
        if skew_le(H, k - 1):
            return True
    return False


def job(line):
    G = nx.from_graph6_bytes(line.encode())
    return line, G.number_of_edges(), skew_le(G, 4)


def main():
    lines = [l.split()[0] for l in open('n10_survivors.txt') if l.strip()]
    with ProcessPoolExecutor(max_workers=6) as ex:
        res = list(ex.map(job, lines))
    yes = [r for r in res if r[2]]
    print(f'{len(res)} survivors at n = 10; skewness <= 4 for {len(yes)} of them')
    if not yes:
        print('   so every one has skewness >= 5, hence cr >= 5: any reduction '
              'to cr = 3 must remove at least 2 crossings')
    else:
        for l, m, _ in yes[:5]:
            print(f'   skewness <= 4: {l} (m = {m})')


if __name__ == '__main__':
    main()

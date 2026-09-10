r"""reviewer-1: how many fixed points do the involutions of the catalogued
\((5,5,42)\)-graphs actually have? Evidence on how loose the bound \(f \le 36\) is.

Enumerates every involution of every graph in the catalogue by backtracking on
matched pairs and fixed points, with a node cap per graph.
"""
import sys
from collections import Counter

sys.path.insert(0, '../r45')
from indep_r45 import graph6

CAT = '../r55auto/catalog/r55_42some.g6'


def involutions(adj, node_cap=400000):
    n = len(adj)
    deg = [bin(a).count('1') for a in adj]
    prof = [tuple(sorted(deg[u] for u in range(n) if (adj[v] >> u) & 1))
            for v in range(n)]
    img = [-1] * n
    out = []
    nodes = [0]

    def consistent(pair):
        for a in range(n):
            if img[a] == -1:
                continue
            for b in pair:
                if ((adj[a] >> b) & 1) != ((adj[img[a]] >> img[b]) & 1):
                    return False
        return True

    def bt():
        nodes[0] += 1
        if nodes[0] > node_cap:
            raise TimeoutError
        try:
            v = next(i for i in range(n) if img[i] == -1)
        except StopIteration:
            out.append(tuple(img))
            return
        for w in range(v, n):                     # w = v means v is fixed
            if img[w] != -1:
                continue
            if deg[w] != deg[v] or prof[w] != prof[v]:
                continue
            img[v], img[w] = w, v
            if consistent((v, w)):
                bt()
            img[v], img[w] = -1, -1
    try:
        bt()
        return out, True
    except TimeoutError:
        return out, False


def main():
    lines = [l.strip() for l in open(CAT) if l.strip()]
    fdist = Counter()
    withinv = capped = 0
    for l in lines:
        n, adj = graph6(l)
        invs, complete = involutions(adj)
        if not complete:
            capped += 1
        real = [p for p in invs if any(p[i] != i for i in range(n))]
        if real:
            withinv += 1
        for p in real:
            fdist[sum(1 for i in range(n) if p[i] == i)] += 1
    print(f'catalogue: {len(lines)} graphs on 42 vertices; {withinv} have a '
          f'non-trivial involution; {capped} searches hit the node cap')
    print(f'   fixed-point counts over all involutions found: '
          f'{dict(sorted(fdist.items()))}')
    print(f'   so the largest fixed-point count that actually occurs is '
          f'{max(fdist) if fdist else "n/a"}, against the bound 36')


if __name__ == '__main__':
    main()

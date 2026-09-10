"""Verify that every graph in the catalogue really is a (5,5,42)-graph.

Provenance matters here: the automorphism census is only about (5,5,42)-graphs if
the file contains (5,5,42)-graphs. This checks each one from scratch -- 42
vertices, no K_5, no independent 5-set -- by branch-and-bound clique search on the
graph and on its complement, using nothing from the encoding machinery.

usage: python3 check_r55_catalogue.py file.g6
"""
import sys
sys.path.insert(0, '.')
from autgroup import read_g6

def has_clique(adj, n, k):
    def ext(cand, size):
        if size == k:
            return True
        for i, v in enumerate(cand):
            if len(cand) - i < k - size:
                break
            if ext([u for u in cand[i + 1:] if adj[v][u]], size + 1):
                return True
        return False
    return ext(list(range(n)), 0)

if __name__ == '__main__':
    bad = []
    degs = set()
    edges = set()
    total = 0
    for idx, line in enumerate(open(sys.argv[1])):
        if not line.strip():
            continue
        total += 1
        n, adj = read_g6(line)
        comp = [[(u != v and not adj[u][v]) for v in range(n)] for u in range(n)]
        d = [sum(adj[v]) for v in range(n)]
        degs |= set(d)
        edges.add(sum(d) // 2)
        if n != 42 or has_clique(adj, n, 5) or has_clique(comp, n, 5):
            bad.append(idx)
    print(f'{total} graphs checked')
    print(f'all on 42 vertices, no K_5, no independent 5-set: {not bad}')
    if bad:
        print(f'  FAILURES at indices {bad[:10]}')
    print(f'edge counts {min(edges)}-{max(edges)}, degrees {min(degs)}-{max(degs)}')

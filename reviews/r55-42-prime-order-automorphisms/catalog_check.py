"""reviewer-1: independent check of the catalog observation.
- own graph6 decoder;
- (5,5)-goodness via bitset clique search (K5-free and complement K5-free);
- degree range; pairwise non-isomorphism is NOT re-checked here (nauty below);
- automorphism group by own backtracking search with degree/common-neighbour
  refinement (no nauty), reporting |Aut| and the cycle types of all
  non-identity automorphisms.
usage: python3 catalog_check.py r55_42some.g6
"""
import sys
from itertools import combinations
from collections import Counter


def graph6(line):
    b = [ord(c) - 63 for c in line.strip()]
    n = b[0]
    bits = []
    for x in b[1:]:
        bits.extend((x >> s) & 1 for s in range(5, -1, -1))
    adj = [0] * n
    i = 0
    for v in range(1, n):
        for u in range(v):
            if bits[i]:
                adj[u] |= 1 << v; adj[v] |= 1 << u
            i += 1
    return n, adj


def has_k5(n, adj):
    for u in range(n):
        nu = adj[u] >> (u + 1) << (u + 1)          # neighbours > u
        while nu:
            v = (nu & -nu).bit_length() - 1; nu &= nu - 1
            c2 = adj[v] & adj[u] >> (v + 1) << (v + 1)
            while c2:
                w = (c2 & -c2).bit_length() - 1; c2 &= c2 - 1
                c3 = c2 & adj[w]
                while c3:
                    x = (c3 & -c3).bit_length() - 1; c3 &= c3 - 1
                    if c3 & adj[x]:
                        return True
    return False


def complement(n, adj):
    full = (1 << n) - 1
    return [(full ^ adj[v]) & ~(1 << v) for v in range(n)]


def automorphisms(n, adj):
    """All automorphisms by backtracking with invariants (degree, sorted
    neighbour-degree multiset, triangle count). Fine for |Aut| tiny."""
    deg = [bin(a).count('1') for a in adj]
    tri = [sum(bin(adj[v] & adj[u]).count('1') for u in range(n) if adj[v] >> u & 1) for v in range(n)]
    inv = [(deg[v], tri[v], tuple(sorted(deg[u] for u in range(n) if adj[v] >> u & 1))) for v in range(n)]
    order = sorted(range(n), key=lambda v: (inv[v], v))
    img = [-1] * n
    used = [False] * n
    found = []
    def rec(i):
        if i == n:
            found.append(img[:]); return
        v = order[i]
        for w in range(n):
            if used[w] or inv[w] != inv[v]:
                continue
            ok = True
            for j in range(i):
                u = order[j]
                if (adj[v] >> u & 1) != (adj[w] >> img[u] & 1):
                    ok = False; break
            if ok:
                img[v] = w; used[w] = True
                rec(i + 1)
                img[v] = -1; used[w] = False
    rec(0)
    return found


def cycle_type(perm):
    n = len(perm); seen = [False] * n; ct = Counter()
    for v in range(n):
        if seen[v]:
            continue
        l = 0; x = v
        while not seen[x]:
            seen[x] = True; x = perm[x]; l += 1
        ct[l] += 1
    return tuple(sorted(ct.items()))


if __name__ == '__main__':
    lines = [l for l in open(sys.argv[1]) if l.strip()]
    autsizes = Counter(); types = Counter(); degs = set(); good = 0
    for i, line in enumerate(lines):
        n, adj = graph6(line)
        assert n == 42
        co = complement(n, adj)
        assert not has_k5(n, adj) and not has_k5(n, co), f"graph {i} not (5,5)-good"
        good += 1
        degs |= {bin(a).count('1') for a in adj}
        A = automorphisms(n, adj)
        autsizes[len(A)] += 1
        for g in A:
            if any(g[v] != v for v in range(n)):
                types[cycle_type(g)] += 1
    print(f"{good} graphs, all (5,5)-good; degrees {sorted(degs)}")
    print("automorphism group orders:", dict(autsizes))
    print("cycle types of non-identity automorphisms:", dict(types))

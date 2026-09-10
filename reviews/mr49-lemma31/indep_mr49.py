r"""reviewer-1: independent check of MR49-LEMMA31.md — Lemma 3.1 and Theorem 3.1
of McKay-Radziszowski's \(R(5,5) \le 49\), §3.

Three parts, all my own:

  (1) the counting identity, derived from scratch by a double count rather than
      from the paper's \(g_2\) machinery;
  (2) the filter: the graphs of the complete \((4,5,24)\) catalogue with exactly
      132 edges, decoded with my own graph6 reader and certified with my own
      clique and independence searches;
  (3) their automorphism groups and vertex-transitivity, by my own backtracking.
"""
import itertools
import sys
from collections import deque

from indep_r45 import graph6, edges, has_clique, has_independent

CAT = 'dl/r45_24.g6'


def identity_check():
    """For any 24-regular graph on 49 vertices, summing over vertices,
    sum_v e(G^-_v) = 588 + sum_v e(G^+_v), and
    sum_v [e(G^+_v) + e(complement of G^-_v)] = 12936.

    Derivation, my own: sum_v e(G^+_v) counts (vertex, edge inside its
    neighbourhood) pairs, which is 3t. For an edge xy, the vertices outside
    N(x) u N(y) u {x,y} number 49 - (48 - lambda(xy)) = 1 + lambda(xy), so
    sum_v e(G^-_v) = m + sum_{xy} lambda(xy) = 588 + 3t. The two agree.
    """
    n, d = 49, 24
    m = n * d // 2
    out = []
    out.append(f'    n = {n}, d = {d}: m = {m} (the paper\'s 588: '
               f'{"match" if m == 588 else "DIFFER"})')
    out.append(f'    sum_v e(G^+_v) = 3t and sum_v e(G^-_v) = m + 3t, so the '
               f'difference is exactly m = {m}, independently of t')
    c24 = 24 * 23 // 2
    tot = n * c24 - m
    out.append(f'    C(24,2) = {c24}; sum_v [e(G^+_v) + e(comp G^-_v)] = '
               f'{n} * {c24} - {m} = {tot} (the paper\'s 12936: '
               f'{"match" if tot == 12936 else "DIFFER"})')
    out.append(f'    average per vertex = {tot} / {n} = {tot // n} '
               f'(exact: {tot % n == 0}), and 2 * 132 = 264 -> '
               f'{"both terms forced to 132" if tot // n == 264 else "no forcing"}')
    out.append(f'    with E(4,5,24) = 133 instead: 2 * 133 = 266 > '
               f'{tot // n}, so nothing would be forced -> the lemma fails')
    return out


def filter_132():
    hits = []
    for line in open(CAT):
        if not line.strip():
            continue
        n, adj = graph6(line)
        if edges(n, adj) == 132:
            hits.append((line.strip(), n, adj))
    return hits


def aut_group(n, adj):
    """all automorphisms, by backtracking with a degree and common-neighbour
    invariant; returns the list of permutations"""
    deg = [bin(a).count('1') for a in adj]
    lam = [[bin(adj[i] & adj[j]).count('1') for j in range(n)] for i in range(n)]
    perms = []
    img = [-1] * n
    used = [False] * n

    def rec(v):
        if v == n:
            perms.append(tuple(img))
            return
        for w in range(n):
            if used[w] or deg[w] != deg[v]:
                continue
            ok = True
            for u in range(v):
                a = (adj[v] >> u) & 1
                b = (adj[w] >> img[u]) & 1
                if a != b or lam[v][u] != lam[w][img[u]]:
                    ok = False
                    break
            if ok:
                img[v] = w
                used[w] = True
                rec(v + 1)
                used[w] = False
                img[v] = -1
    rec(0)
    return perms


def orbits(n, perms):
    seen = [False] * n
    out = []
    for v in range(n):
        if seen[v]:
            continue
        orb = {v}
        q = deque([v])
        while q:
            u = q.popleft()
            for p in perms:
                if p[u] not in orb:
                    orb.add(p[u])
                    q.append(p[u])
        for u in orb:
            seen[u] = True
        out.append(sorted(orb))
    return out


def main():
    print('(1) THE COUNTING IDENTITY, DERIVED FROM SCRATCH')
    for l in identity_check():
        print(l)
    print()
    print('(2) THEOREM 3.1 AS A FILTER')
    hits = filter_132()
    print(f'    graphs of the complete (4,5,24) catalogue with exactly 132 '
          f'edges: {len(hits)}')
    for g6, n, adj in hits:
        degs = sorted(bin(a).count('1') for a in adj)
        print(f'      {g6[:30]}...  order {n}, K_4 {has_clique(n, adj, 4)}, '
              f'independent 5-set {has_independent(n, adj, 5)}, degrees '
              f'{degs[0]}..{degs[-1]} -> '
              f'{"11-regular genuine (4,5,24,132)-graph" if degs[0] == degs[-1] == 11 and not has_clique(n, adj, 4) and not has_independent(n, adj, 5) else "MISMATCH"}')
    print()
    print('(3) AUTOMORPHISM GROUPS AND TRANSITIVITY, MY OWN BACKTRACKING')
    orders = []
    for g6, n, adj in hits:
        perms = aut_group(n, adj)
        orb = orbits(n, perms)
        orders.append(len(perms))
        print(f'      {g6[:20]}...  |Aut| = {len(perms)}, orbits '
              f'{[len(o) for o in orb]} -> '
              f'{"vertex-transitive" if len(orb) == 1 else "not transitive"}')
    print(f'    multiset of orders: {sorted(orders)}; the paper states '
          f'{{24, 48}} -> {"match" if sorted(orders) == [24, 48] else "DIFFER"}')


if __name__ == '__main__':
    main()

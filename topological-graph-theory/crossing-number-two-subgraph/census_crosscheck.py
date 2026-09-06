"""Cross-validate BORS Theorem 17.1(3) against the independent census.

Theorem 17.1(3) says every 3-connected 2-crossing-critical graph with no
V_10 subdivision, not V_8-containing, and not one of the four graphs of
Theorem 15.6, is an expansion of one of the 36 peripherally-4-connected
2-crossing-critical seeds on at most ten vertices.

We have an independent exhaustive census of ALL 2-crossing-critical graphs on
at most eleven vertices.  Every patch adds at least zero vertices, and only the
identity patch adds zero, so the expansions with at most eleven vertices are a
small explicitly enumerable set -- over ALL 36 seeds, not only the low-d ones.
Comparing that set against the census tests the theorem where ground truth
exists.
"""
import collections
import itertools
import json
import sys

import networkx as nx

import expand_run as X

LIMIT = 11


def patch_dn(P):
    out = []
    for edges, internal in P:
        c = collections.Counter(tuple(sorted(e)) for e in edges)
        extras = sum(m - 1 for m in c.values())
        out.append(len(internal) + extras - 1)
    return out


def assignments_within(dn, d, budget):
    """All length-d patch assignments whose total vertex increase is <= budget."""
    order = sorted(range(len(dn)), key=lambda i: dn[i])
    res = []

    def rec(pos, spent, cur):
        if pos == d:
            res.append(tuple(cur))
            return
        for i in order:
            if spent + dn[i] > budget:
                break
            cur.append(i)
            rec(pos + 1, spent + dn[i], cur)
            cur.pop()
    rec(0, 0, [])
    return res


def main():
    P = X.patches()
    S = X.seeds()
    dn = patch_dn(P)
    ident = dn.index(0)
    assert dn.count(0) == 1

    # census: every 2-crossing-critical graph on at most eleven vertices
    import os
    census = []
    for n in range(6, 12):
        f = os.path.join(X.REPO, f'n{n}.txt')
        if not os.path.exists(f):
            continue
        for line in open(f):
            p = line.split()
            if len(p) < 4:
                continue
            E = [tuple(map(int, x.split('-')))
                 for x in p[3].strip(',').split(',')]
            census.append(nx.Graph(E))
    print(f"census (2-crossing-critical, n <= {LIMIT}): {len(census)}")

    found, tested = [], 0
    for si, G in enumerate(S):
        d3 = [v for v, x in G.degree() if x == 3]
        budget = LIMIT - G.number_of_nodes()
        A = assignments_within(dn, len(d3), budget)
        tested += len(A)
        for a in A:
            H = X.expand(G, d3, a, P)
            if H.number_of_nodes() > LIMIT:
                continue
            found.append((si, a, H))
    print(f"expansions with n <= {LIMIT}, over all 36 seeds: {len(found)} "
          f"(from {tested:,} assignments within the vertex budget)")

    # which are 2-crossing-critical?
    crit = []
    B = 5000
    for i in range(0, len(found), B):
        chunk = found[i:i + B]
        out = X.run_crit2([h for _, _, h in chunk])
        n_lines = sum(1 for l in out.split('\n') if l.startswith('CRIT'))
        # crit2 prints only critical graphs, so re-test singly for attribution
        for rec in chunk:
            o = X.run_crit2([rec[2]])
            if any(l.startswith('CRIT') for l in o.split('\n')):
                crit.append(rec)
    print(f"of those, 2-crossing-critical: {len(crit)}")

    # dedupe up to isomorphism
    reps = []
    for si, a, H in crit:
        if not any(nx.is_isomorphic(H, K) for _, _, K in reps):
            reps.append((si, a, H))
    print(f"distinct up to isomorphism: {len(reps)}")
    nontrivial = [r for r in reps if any(x != ident for x in r[1])]
    print(f"  of which use at least one non-identity patch: {len(nontrivial)}")

    # do they all appear in the census?
    miss = [r for r in reps
            if not any(nx.is_isomorphic(r[2], C) for C in census)]
    print(f"expansions that are critical but ABSENT from the census: {len(miss)}"
          f"   <-- must be 0")

    # which 3-connected census members are NOT expansions?
    sys.path.insert(0, X.REPO)
    c3 = [C for C in census if nx.node_connectivity(C) >= 3]
    unexplained = [C for C in c3
                   if not any(nx.is_isomorphic(C, H) for _, _, H in reps)]
    print(f"\n3-connected census members: {len(c3)}")
    print(f"  reproduced as expansions: {len(c3) - len(unexplained)}")
    print(f"  NOT reproduced: {len(unexplained)}  "
          f"(each must be V8-containing, have a V10 subdivision, "
          f"or be one of the four graphs of Thm 15.6)")
    json.dump([[list(e) for e in C.edges()] for C in unexplained],
              open('unexplained.json', 'w'))
    return unexplained


if __name__ == '__main__':
    main()

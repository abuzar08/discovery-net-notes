"""Decode Figure 14.3 of BORS and settle the crossing numbers of its 20 graphs.

Figure 14.3 shows the 2-connected, not 3-connected 2-crossing-critical graphs
with three cleavage units, two of them non-planar.  A figure of a cleavage-unit
decomposition draws each hinge vertex once per unit containing it, so the graph
G is recovered by identifying those repeated vertices.  That is what the drawn
components need: as extracted they are not 2-crossing-critical, and neither
doubling nor deleting edges repairs them, but identifying vertex pairs does.

The claim made here is deliberately reading-independent: for each drawn
component we enumerate EVERY identification of at most k pairs, for the least k
that produces any 2-crossing-critical graph, and record the verdicts of all of
them.  If every such graph is CRIT2 and none is CRIT_GE3, then no reading of the
figure of that form yields a graph of crossing number at least 3.
"""
import collections
import itertools
import sys

import networkx as nx

import extract_fig as X
import expand_run as R


def drawn_components(page=127):
    v, E = X.extract('bors.pdf', page)
    out = []
    for c in [c for c in X.components(v, E) if len(c) >= 5]:
        idx = {u: i for i, u in enumerate(sorted(c))}
        G = nx.Graph()
        G.add_nodes_from(range(len(c)))
        for (a, b), m in E.items():
            if a in idx and b in idx:
                G.add_edge(idx[a], idx[b])
        out.append(G)
    return out


def verdict(G):
    for l in R.run_crit2([G]).split('\n'):
        if l.startswith('CRIT'):
            return l.split()[0]
    return None


def identify(G, pairs):
    H = nx.Graph(G)
    for u, w in pairs:
        if u in H and w in H and u != w:
            H = nx.contracted_nodes(H, u, w, self_loops=False)
    return H


def settle(G, kmax=3):
    """Least k with a critical identification, and the verdicts of ALL of them."""
    pairs = list(itertools.combinations(sorted(G.nodes()), 2))
    for k in range(1, kmax + 1):
        cands = []
        for P in itertools.combinations(pairs, k):
            H = identify(G, P)
            if H.number_of_nodes() < 5:
                continue
            if min((d for _, d in H.degree()), default=0) < 3:
                continue
            cands.append(H)
        if not cands:
            continue
        marks = [l.split()[0] for l in R.run_crit2(cands).split('\n')
                 if l.startswith('CRIT')]
        if marks:
            return k, collections.Counter(marks)
    return None, collections.Counter()


if __name__ == '__main__':
    gs = drawn_components()
    bad = [G for G in gs if not verdict(G)]
    print(f"drawn components needing repair: {len(bad)}", flush=True)
    tot = collections.Counter()
    unresolved = 0
    for i, G in enumerate(sorted(bad, key=lambda g: g.number_of_nodes())):
        k, c = settle(G)
        tot.update(c)
        if k is None:
            unresolved += 1
        print(f"  n={G.number_of_nodes():>3} m={G.number_of_edges():>3}  "
              f"least k = {k}  verdicts over ALL k-identifications: {dict(c)}",
              flush=True)
    print(f"\nunresolved at k <= 3: {unresolved}")
    print(f"verdicts over every critical identification found: {dict(tot)}")
    print(f"any with cr >= 3: {tot.get('CRIT_GE3', 0)}")

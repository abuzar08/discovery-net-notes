"""Planar 3-reductions (BORS Definition 15.17) and the crossing number of the base.

Definition 15.10(1): G reduces to G' by 3-reductions if there is a sequence of
3-connected graphs in which each step picks a 3-cut S and an S-bridge B whose
nucleus has at least two vertices, and contracts that nucleus to a single vertex.
Definition 15.17 adds that each contracted bridge must have B+ planar, where B+
is B together with a new vertex adjacent to the three vertices of S.

This lets the corrected reading of Theorem 17.1(3) be tested directly: reduce
each 3-connected 2-crossing-critical graph to a peripherally-4-connected base
and ask what the crossing number of that base is.  The scoping correction
predicts that the informative bases have crossing number 1, not 2.
"""
import itertools
import sys

import networkx as nx


def cr_le_1(G):
    """True iff cr(G) <= 1."""
    if nx.check_planarity(G, counterexample=False)[0]:
        return True
    E = list(G.edges())
    for i in range(len(E)):
        for j in range(i + 1, len(E)):
            a, b = E[i]
            c, d = E[j]
            if len({a, b, c, d}) < 4:
                continue                      # crossing adjacent edges is useless
            H = nx.Graph(G)
            H.remove_edge(a, b)
            H.remove_edge(c, d)
            w = 'X'
            H.add_edges_from([(w, a), (w, b), (w, c), (w, d)])
            if nx.check_planarity(H, counterexample=False)[0]:
                return True
    return False


def crossing_number_small(G, cap=3):
    """cr(G) for small G, by iterated planarization, up to cap."""
    if nx.check_planarity(G, counterexample=False)[0]:
        return 0
    if cr_le_1(G):
        return 1
    return 2 if cap <= 2 else ('>=2')


def bridges_of(G, S):
    """The S-bridges with a nucleus: (nucleus vertex set, attachments)."""
    H = G.copy()
    H.remove_nodes_from(S)
    out = []
    for comp in nx.connected_components(H):
        att = {s for s in S if any(G.has_edge(s, u) for u in comp)}
        out.append((set(comp), att))
    return out


def reductions(G):
    """Every graph obtainable by one planar 3-reduction."""
    out = []
    for S in itertools.combinations(G.nodes(), 3):
        S = set(S)
        H = G.copy()
        H.remove_nodes_from(S)
        if H.number_of_nodes() == 0 or nx.is_connected(H):
            continue                              # S is not a cut
        for nuc, att in bridges_of(G, S):
            if len(nuc) < 2 or att != S:
                continue
            # B+ : the bridge plus an apex adjacent to the three cut vertices
            B = G.subgraph(nuc | S).copy()
            B.add_node('apex')
            for s in S:
                B.add_edge('apex', s)
            if not nx.check_planarity(B, counterexample=False)[0]:
                continue
            K = G.copy()
            keep = min(nuc)
            for u in nuc - {keep}:
                K = nx.contracted_nodes(K, keep, u, self_loops=False)
            if nx.node_connectivity(K) >= 3:
                out.append(K)
    return out


def reduce_fully(G, p4c_test):
    """Reduce until no planar 3-reduction applies; return one terminal graph."""
    cur = G
    seen = 0
    while True:
        nxt = reductions(cur)
        if not nxt:
            return cur, seen
        # prefer the largest contraction, to terminate quickly
        cur = min(nxt, key=lambda H: H.number_of_nodes())
        seen += 1


if __name__ == '__main__':
    import json
    sys.path.insert(0, '../notes/topological-graph-theory/'
                       'crossing-number-two-subgraph')
    from seeds import peripherally_4_connected
    G19 = [nx.Graph([tuple(e) for e in E])
           for E in json.load(open('unexplained.json'))]
    from vsub2 import contains, V8, V10
    G19 = [G for G in G19 if not contains(G, V8) and not contains(G, V10)]
    print(f"graphs to reduce: {len(G19)}\n")
    print(f"{'n':>3} {'m':>3} | {'base n':>7} {'base m':>7} {'p4c?':>6} "
          f"{'cr(base)':>9} {'steps':>6}")
    tally = {}
    for G in sorted(G19, key=lambda g: (g.number_of_nodes(),
                                        g.number_of_edges())):
        B, steps = reduce_fully(G, peripherally_4_connected)
        p4c = peripherally_4_connected(B)
        cr = crossing_number_small(B)
        tally[cr] = tally.get(cr, 0) + 1
        print(f"{G.number_of_nodes():>3} {G.number_of_edges():>3} | "
              f"{B.number_of_nodes():>7} {B.number_of_edges():>7} "
              f"{str(p4c):>6} {str(cr):>9} {steps:>6}")
    print(f"\ncrossing number of the peripherally-4-connected base: {tally}")

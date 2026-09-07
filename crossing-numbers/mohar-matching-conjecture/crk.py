"""Exact crossing number of small graphs, by exhaustive planarisation.

cr(G) <= k iff G has a drawing with k crossings, iff some planarisation with k
crossings is planar.  A planarisation chooses k unordered pairs of edges to
cross (a pair must be INDEPENDENT -- adjacent edges never cross in an optimal
drawing -- and no pair twice), and, where an edge carries several crossings, an
order for them along that edge.  Enumerating both gives an exact decision.
"""
import itertools
import networkx as nx


def independent_pairs(G):
    E = list(G.edges())
    out = []
    for i in range(len(E)):
        for j in range(i + 1, len(E)):
            if len(set(E[i]) | set(E[j])) == 4:
                out.append((E[i], E[j]))
    return out


def planarise(G, chosen, order):
    """chosen: list of edge pairs; order: for each edge, the sequence of its
    crossing indices along it."""
    H = nx.Graph()
    H.add_nodes_from(G.nodes())
    xv = {i: ('X', i) for i in range(len(chosen))}
    # for each original edge, the crossings on it, in the given order
    on = {}
    for i, (a, b) in enumerate(chosen):
        on.setdefault(tuple(sorted(a)), []).append(i)
        on.setdefault(tuple(sorted(b)), []).append(i)
    for e in G.edges():
        k = tuple(sorted(e))
        seq = on.get(k, [])
        if len(seq) > 1:
            seq = order[k]
        path = [k[0]] + [xv[i] for i in seq] + [k[1]]
        for u, v in zip(path, path[1:]):
            H.add_edge(u, v)
    return H


def cr_le(G, k):
    """True iff cr(G) <= k."""
    if nx.check_planarity(G, counterexample=False)[0]:
        return True
    if k == 0:
        return False
    P = independent_pairs(G)
    for r in range(1, k + 1):
        for chosen in itertools.combinations(P, r):
            on = {}
            for i, (a, b) in enumerate(chosen):
                on.setdefault(tuple(sorted(a)), []).append(i)
                on.setdefault(tuple(sorted(b)), []).append(i)
            multi = [e for e, s in on.items() if len(s) > 1]
            if not multi:
                if nx.check_planarity(planarise(G, chosen, {}),
                                      counterexample=False)[0]:
                    return True
                continue
            for perms in itertools.product(*[list(itertools.permutations(on[e]))
                                             for e in multi]):
                order = dict(zip(multi, perms))
                if nx.check_planarity(planarise(G, chosen, order),
                                      counterexample=False)[0]:
                    return True
    return False


def multipartite(parts):
    G = nx.complete_multipartite_graph(*parts)
    return nx.convert_node_labels_to_integers(G)


if __name__ == '__main__':
    import sys
    # sanity: known values
    for name, G, val in [('K5', nx.complete_graph(5), 1),
                         ('K6', nx.complete_graph(6), 3),
                         ('K3,3', nx.complete_bipartite_graph(3, 3), 1),
                         ('K2,2,2 (octahedron)', multipartite([2, 2, 2]), 0),
                         ('K1,1,2,2 = K6 - 2e', multipartite([1, 1, 2, 2]), 1)]:
        lo = 0
        while not cr_le(G, lo):
            lo += 1
        print(f"  cr({name}) = {lo}   expected {val}   "
              f"{'OK' if lo == val else 'MISMATCH'}")

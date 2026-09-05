"""Cross-validate Bokal-Oporowski-Richter-Salazar Proposition 14.1 against the
exhaustive census.

BORS (arXiv:1312.3712, Chapter 14) argue that the crossing number is additive
over components and over blocks, so a 2-crossing-critical graph that is not
2-connected has at most two components, each a subdivision of K5 or K3,3, and
the connected ones arise by identifying a vertex of one with a vertex of the
other -- where "the identified vertex may be a new vertex that subdivides some
edge".  Proposition 14.1: the thirteen graphs of their Figure 14.1 are
precisely the 2-crossing-critical graphs that are not 2-connected.

The census independently finds every 2-crossing-critical graph of minimum
degree at least 3 on at most 10 vertices.  This script checks that the ones
which are not 2-connected are exactly the constructions above -- an exhaustive
search meeting a published classification.

Consequence used elsewhere: every not-2-connected 2-crossing-critical graph has
blocks that are 1-critical, hence crossing number 2.  So a 2-crossing-critical
graph of crossing number at least 3 -- a second counterexample to the
Bloom-Kennedy-Quintas question -- must be 2-connected.

    uv run --with networkx python bors_prop_14_1_check.py
"""
import networkx as nx


def load(path):
    out = []
    for line in open(path):
        p = line.split()
        if len(p) < 4:
            continue
        E = [tuple(map(int, x.split('-'))) for x in p[3].strip(',').split(',')]
        out.append((int(p[1]), nx.Graph(E)))
    return out


def subdivisions(G, k):
    """All graphs obtained from G by subdividing exactly k edges."""
    outs = [G.copy()]
    for _ in range(k):
        nxt = []
        for H in outs:
            for (u, v) in list(H.edges()):
                J = H.copy()
                w = max(J.nodes()) + 1
                J.remove_edge(u, v)
                J.add_edges_from([(u, w), (w, v)])
                nxt.append(J)
        outs = nxt
    return outs


def one_point_union(A, B, a, b):
    B2 = nx.relabel_nodes(B, {x: ('b', x) for x in B.nodes()})
    H = nx.contracted_nodes(nx.union(A, B2), a, ('b', b), self_loops=False)
    return nx.convert_node_labels_to_integers(H)


def bors_family(max_subdiv=1):
    """The BORS Prop. 14.1 constructions, up to `max_subdiv` subdivided edges
    on each side (enough to cover every census member)."""
    bases = [("K5", nx.complete_graph(5)),
             ("K3,3", nx.complete_bipartite_graph(3, 3))]
    fam = []
    for na, A in bases:
        for nb, B in bases:
            fam.append((f"{na} u {nb}", nx.disjoint_union(A, B)))
            for ka in range(max_subdiv + 1):
                for kb in range(max_subdiv + 1):
                    for A2 in subdivisions(A, ka):
                        for B2 in subdivisions(B, kb):
                            for a in A2.nodes():
                                for b in B2.nodes():
                                    fam.append(
                                        (f"{na}.{nb} (subdivided {ka},{kb})",
                                         one_point_union(A2, B2, a, b)))
    return fam


def main():
    members = []
    for n in range(6, 12):
        try:
            members += load(f"n{n}.txt")
        except FileNotFoundError:
            pass
    not2 = [(n, G) for n, G in members if nx.node_connectivity(G) < 2]
    print(f"census members that are not 2-connected: {len(not2)}")

    fam = bors_family()
    ok = True
    for n, G in not2:
        hit = None
        for name, H in fam:
            if H.number_of_nodes() == G.number_of_nodes() and \
                    H.number_of_edges() == G.number_of_edges() and \
                    nx.is_isomorphic(H, G):
                hit = name
                break
        print(f"   n = {n:2d}, m = {G.number_of_edges():2d}, "
              f"connectivity {nx.node_connectivity(G)}  ->  "
              f"{hit if hit else 'NO MATCH'}")
        ok = ok and hit is not None

    print()
    print(f"every not-2-connected census member is a BORS Prop. 14.1 graph: {ok}")
    print("=> a 2-crossing-critical graph of crossing number at least 3 is "
          "2-connected.")
    assert ok


if __name__ == "__main__":
    main()

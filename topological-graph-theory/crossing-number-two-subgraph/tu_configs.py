"""Recover BORS's (T, U)-configurations by enumeration from Definition 15.21.

BORS arXiv:1312.3712, Definition 15.21 (quoted from the text):

  Let x, y, and z be vertices in a graph H so that H is an ||{x,y,z}||-bridge.
  Then:
    * T is the set of vertices w in {x,y,z} so that there are edge-disjoint
      w({x,y,z} \ {w})-paths in H; and
    * U is the set of vertices w in {x,y,z} for which there are edge-disjoint
      paths in H - w joining the two vertices in {x,y,z} \ {w}.
    * (H, {x,y,z}) is a (T,U)-configuration if the graph H+ obtained from H by
      adding a new vertex adjacent just to x, y, and z is planar.

and, in the following paragraph: if |T| <= 1 then U is empty; if T = {x,y} then
U = {z}; so for |T| <= 2 the pair is determined by T, while for |T| = 3 one has
|U| in {2,3}.  Five possibilities for (|T|,|U|) in all.

Theorem 17.1(3) says each replacement patch has at most six vertices; the patch
is K_v = H - {x,y,z}, so the internal part has at most six vertices.

This script enumerates the configurations with a bounded internal part and
classifies them, to see whether the set Figure 15.1 displays can be recovered
without the figure.  A configuration here is (H, {x,y,z}) with:
  * internal set S nonempty, H[S] connected;
  * no edges among x, y, z (an edge between two of them would be a separate
    bridge, not part of this one);
  * every terminal has at least one neighbour in S (all three are attachments);
  * H+ planar.
Configurations are counted up to isomorphism fixing the terminal set setwise.
"""
import itertools
import sys
from collections import Counter, defaultdict

import networkx as nx

X, Y, Z = 'x', 'y', 'z'
TERMS = (X, Y, Z)


def connected_graphs(s):
    """All connected graphs on s labelled vertices 0..s-1, up to isomorphism."""
    seen, out = set(), []
    verts = list(range(s))
    pairs = list(itertools.combinations(verts, 2))
    for mask in range(1 << len(pairs)):
        G = nx.Graph()
        G.add_nodes_from(verts)
        G.add_edges_from(p for i, p in enumerate(pairs) if mask >> i & 1)
        if s > 1 and not nx.is_connected(G):
            continue
        key = nx.weisfeiler_lehman_graph_hash(G, iterations=4)
        cand = [g for g in out if nx.weisfeiler_lehman_graph_hash(g, iterations=4) == key]
        if any(nx.is_isomorphic(g, G) for g in cand):
            continue
        out.append(G)
    return out


def edge_disjoint_count(G, src, targets):
    """Max number of edge-disjoint paths from src to the set `targets`."""
    H = nx.Graph(G)
    sink = ('sink',)
    H.add_node(sink)
    for t in targets:
        H.add_edge(t, sink)
    # each added edge has capacity 1, so it does not inflate the count beyond
    # |targets|; that is fine, we only need to know whether it is >= 2
    return nx.edge_connectivity(H, src, sink)


def classify(H):
    T = set()
    for w in TERMS:
        others = [t for t in TERMS if t != w]
        if edge_disjoint_count(H, w, others) >= 2:
            T.add(w)
    U = set()
    for w in TERMS:
        others = [t for t in TERMS if t != w]
        Hw = H.copy()
        Hw.remove_node(w)
        if nx.has_path(Hw, others[0], others[1]) and \
                nx.edge_connectivity(Hw, others[0], others[1]) >= 2:
            U.add(w)
    return frozenset(T), frozenset(U)


def is_configuration(H):
    Hp = H.copy()
    Hp.add_node('apex')
    for t in TERMS:
        Hp.add_edge('apex', t)
    return nx.check_planarity(Hp, counterexample=False)[0]


def canon(H):
    """Canonical key for H up to isomorphism fixing the terminal set setwise."""
    for u in H.nodes():
        H.nodes[u]['t'] = 1 if u in TERMS else 0
    return nx.weisfeiler_lehman_graph_hash(H, node_attr='t', iterations=5)


def enumerate_configs(smax):
    found = defaultdict(list)
    for s in range(1, smax + 1):
        for base in connected_graphs(s):
            S = list(range(s))
            subsets = [frozenset(c) for r in range(1, s + 1)
                       for c in itertools.combinations(S, r)]
            for ax in subsets:
                for ay in subsets:
                    for az in subsets:
                        H = nx.Graph()
                        H.add_nodes_from(S)
                        H.add_edges_from(base.edges())
                        H.add_nodes_from(TERMS)
                        for t, A in zip(TERMS, (ax, ay, az)):
                            for a in A:
                                H.add_edge(t, a)
                        if not is_configuration(H):
                            continue
                        T, U = classify(H)
                        key = (len(T), len(U), canon(H))
                        if any(k == key for k in found[(len(T), len(U))]):
                            continue
                        found[(len(T), len(U))].append(key)
    return found


if __name__ == "__main__":
    smax = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    print(f"enumerating (T,U)-configurations with internal part of size <= {smax}")
    found = enumerate_configs(smax)
    tot = 0
    print(f"\n{'(|T|,|U|)':>10} {'configurations':>15}")
    for k in sorted(found):
        print(f"{str(k):>10} {len(found[k]):>15}")
        tot += len(found[k])
    print(f"{'TOTAL':>10} {tot:>15}")
    print("\nBORS: five possibilities for (|T|,|U|); at most twenty patches, "
          "each of at most six vertices.")

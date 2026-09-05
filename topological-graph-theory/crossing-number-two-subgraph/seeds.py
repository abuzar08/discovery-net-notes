"""The complete seed set for Bokal-Oporowski-Richter-Salazar Theorem 17.1(3).

BORS Theorem 17.1 (Classification of 2-crossing-critical graphs), part (3):

  If G is 3-connected and does not have a subdivision of V10, then G has at
  most three million vertices (so there are only finitely many such examples).
  Each of these examples either
    * has a subdivision of V8, or
    * is either one of the four graphs described in Theorem 15.6 or obtained
      from a 2-crossing-critical peripherally-4-connected graph with at most
      TEN vertices by replacing each vertex v having precisely three neighbors
      with one of at most twenty patches, each patch having at most six
      vertices (so G has at most sixty vertices).

The census independently determines every 2-crossing-critical graph of minimum
degree at least three on at most ten vertices.  Peripheral 4-connectivity
implies 3-connectivity implies minimum degree at least three, so filtering the
census yields the COMPLETE seed set that the second bullet requires.

BORS definition: G is peripherally-4-connected if G is 3-connected and, for
every 3-cut X, any partition of the components of G - X into two nonnull
subgraphs H and J has one of H and J being a single vertex.

Unwinding that for k components of sizes s_1..s_k:
  k = 2: the only partition is {C1}|{C2}, so s_1 = 1 or s_2 = 1;
  k = 3: a two-component side has at least two vertices and so can never be
         "a single vertex", hence every singleton side must be, i.e. all three
         components are single vertices (this is the K_{3,3} case);
  k >= 4: split 2-and-2 and neither side is a single vertex, so this fails.
For a 4-connected G there is no 3-cut at all and the condition holds vacuously.

    uv run --with networkx python seeds.py
"""
import itertools

import networkx as nx


def peripherally_4_connected(G):
    if nx.node_connectivity(G) < 3:
        return False
    for X in itertools.combinations(list(G.nodes()), 3):
        H = G.copy()
        H.remove_nodes_from(X)
        comps = [len(c) for c in nx.connected_components(H)]
        if len(comps) < 2:
            continue                       # X is not a cut
        if len(comps) == 2:
            if min(comps) != 1:
                return False
        elif len(comps) == 3:
            if max(comps) != 1:            # all three must be single vertices
                return False
        else:
            return False                   # four or more components
    return True


def load(path):
    out = []
    for line in open(path):
        p = line.split()
        if len(p) < 4:
            continue
        E = [tuple(map(int, x.split('-'))) for x in p[3].strip(',').split(',')]
        out.append((int(p[1]), nx.Graph(E)))
    return out


def controls():
    print("controls")
    K5 = nx.complete_graph(5)
    checks = [("K5 (4-connected, no 3-cut)", K5, True),
              ("K3,3 (3-connected)", nx.complete_bipartite_graph(3, 3), True),
              ("two K5's sharing a triangle (3-cut, both sides big)",
               None, False)]
    A = nx.complete_graph(5)
    B = nx.relabel_nodes(nx.complete_graph(5), {0: 0, 1: 1, 2: 2, 3: 5, 4: 6})
    shared = nx.compose(A, B)
    checks[2] = (checks[2][0], shared, False)
    for name, G, want in checks:
        got = peripherally_4_connected(G)
        print(f"   [{'ok ' if got == want else 'FAIL'}] {name}: {got}")
        assert got == want


def main():
    controls()
    members = []
    for n in range(6, 12):
        try:
            members += load(f"n{n}.txt")
        except FileNotFoundError:
            pass
    seeds = [(n, G) for n, G in members if peripherally_4_connected(G)]
    print(f"\ncensus members: {len(members)}")
    print(f"peripherally-4-connected (the BORS Thm 17.1(3) seeds): {len(seeds)}")
    from collections import Counter
    print("by order:", dict(sorted(Counter(n for n, _ in seeds).items())))

    E = set()
    for i in range(3):
        for j in range(3):
            u = 3 * i + j
            E.add(tuple(sorted((u, 3 * ((i + 1) % 3) + j))))
            E.add(tuple(sorted((u, 3 * i + (j + 1) % 3))))
    C = nx.Graph(sorted(E))
    print(f"C3 [] C3 is a seed: {peripherally_4_connected(C)} "
          f"(4-connected, so no 3-cut exists)")

    print("\nseeds (n, m, connectivity, degree sequence)")
    for n, G in sorted(seeds, key=lambda t: (t[0], t[1].number_of_edges())):
        print(f"   {n:2d} {G.number_of_edges():2d} "
              f"{nx.node_connectivity(G)}  "
              f"{sorted(d for _, d in G.degree())}")


if __name__ == "__main__":
    main()

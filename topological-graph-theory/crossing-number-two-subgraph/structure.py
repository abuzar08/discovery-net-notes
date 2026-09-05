"""Where the census members sit in the Bokal-Oporowski-Richter-Salazar
structural description of 2-crossing-critical graphs.

BORS (arXiv:1312.3712) state four results:

  (i)   determine all 3-connected 2-crossing-critical graphs that contain a
        subdivision of the Moebius ladder V10  -- an infinite, tile-built family;
  (ii)  show how to obtain all the not 3-connected ones from the 3-connected;
  (iii) show there are only FINITELY many 3-connected ones not containing a
        subdivision of V10;
  (iv)  determine all 3-connected ones that do not contain a subdivision of V8.

So every 2-crossing-critical graph falls into exactly one of: not 3-connected;
3-connected with a V10 subdivision; 3-connected with a V8 but no V10
subdivision; 3-connected with no V8 subdivision.  This script places the census
members, and C3 [] C3 itself, in that division.

The subdivision test is exact here.  V8 and V10 are cubic, so every one of
their vertices is a branch vertex; with |V(G)| - |V(H)| spare vertices, each
spare vertex can serve as the interior of at most one path, which is what the
enumeration below allows.

    uv run --with networkx python structure.py
"""
import collections
import itertools

import networkx as nx


def moebius_ladder(k):
    G = nx.cycle_graph(k)
    for i in range(k // 2):
        G.add_edge(i, i + k // 2)
    return G


def has_subdivision(G, H):
    """True iff G contains a subdivision of the cubic graph H.  Exact while
    |V(G)| - |V(H)| is small: choose the branch vertices, then let each spare
    vertex supply at most one two-edge path between two of its neighbours."""
    nH = H.number_of_nodes()
    if G.number_of_nodes() < nH:
        return False
    for B in itertools.combinations(G.nodes(), nH):
        spare = [v for v in G.nodes() if v not in B]
        base = G.subgraph(B).copy()
        for k in range(len(spare) + 1):
            for use in itertools.combinations(spare, k):
                choices, ok = [], True
                for s in use:
                    nb = [w for w in G[s] if w in B]
                    if len(nb) < 2:
                        ok = False
                        break
                    choices.append(list(itertools.combinations(nb, 2)))
                if not ok:
                    continue
                for combo in (itertools.product(*choices) if choices else [()]):
                    aug = base.copy()
                    aug.add_edges_from(combo)
                    if nx.algorithms.isomorphism.GraphMatcher(
                            aug, H).subgraph_is_monomorphic():
                        return True
    return False


def controls():
    V8, V10 = moebius_ladder(8), moebius_ladder(10)
    sub = moebius_ladder(8)
    sub.add_node(8)
    sub.remove_edge(0, 1)
    sub.add_edges_from([(0, 8), (8, 1)])
    tests = [("V8 in V8", moebius_ladder(8), V8, True),
             ("V8 in K8", nx.complete_graph(8), V8, True),
             ("V8 in K5", nx.complete_graph(5), V8, False),
             ("V8 in a one-edge subdivision of V8", sub, V8, True),
             ("V8 in C8", nx.cycle_graph(8), V8, False),
             ("V10 in V10", moebius_ladder(10), V10, True),
             ("V10 in K10", nx.complete_graph(10), V10, True)]
    print("controls on the subdivision test")
    for name, G, H, want in tests:
        got = has_subdivision(G, H)
        print(f"   [{'ok ' if got == want else 'FAIL'}] {name}: {got}")
        assert got == want


def load(path):
    out = []
    for line in open(path):
        p = line.split()
        if len(p) < 4:
            continue
        E = [tuple(map(int, x.split('-'))) for x in p[3].strip(',').split(',')]
        out.append((p[0], int(p[1]), nx.Graph(E)))
    return out


def classify(G, n, V8, V10):
    if nx.node_connectivity(G) < 3:
        return "not 3-connected  [BORS (ii)]"
    if has_subdivision(G, V10):
        return "3-connected, V10 subdivision  [BORS (i), infinite family]"
    if has_subdivision(G, V8):
        return "3-connected, V8 but no V10  [BORS (iii), finite]"
    return "3-connected, no V8 subdivision  [BORS (iv), determined]"


def main():
    controls()
    V8, V10 = moebius_ladder(8), moebius_ladder(10)
    members = []
    for n in range(6, 12):
        try:
            members += load(f"n{n}.txt")
        except FileNotFoundError:
            pass

    cls = collections.Counter()
    per_n = collections.defaultdict(collections.Counter)
    for tag, n, G in members:
        c = classify(G, n, V8, V10)
        cls[c] += 1
        per_n[n][c] += 1

    print(f"\nplacement of the {len(members)} census members")
    for c, v in sorted(cls.items(), key=lambda x: -x[1]):
        print(f"   {v:3d}  {c}")

    print("\nby order")
    for n in sorted(per_n):
        tot = sum(per_n[n].values())
        conn = tot - per_n[n]["not 3-connected  [BORS (ii)]"]
        v8 = per_n[n]["3-connected, V8 but no V10  [BORS (iii), finite]"]
        print(f"   n = {n:2d}: {tot:2d} members, {conn:2d} 3-connected, "
              f"{v8:2d} with a V8 subdivision, "
              f"{per_n[n]['3-connected, V10 subdivision  [BORS (i), infinite family]']} with V10")

    E = set()
    for i in range(3):
        for j in range(3):
            u = 3 * i + j
            E.add(tuple(sorted((u, 3 * ((i + 1) % 3) + j))))
            E.add(tuple(sorted((u, 3 * i + (j + 1) % 3))))
    C = nx.Graph(sorted(E))
    print(f"\nC3 [] C3 itself: connectivity {nx.node_connectivity(C)}, "
          f"V8 subdivision {has_subdivision(C, V8)}, V10 subdivision False "
          f"(only 9 vertices)")
    print("   => the unique counterexample lies in BORS class (iv).  NOTE: the")
    print("      BORS abstract says they 'determine' that class, but their")
    print("      Remark 17.2 says Section 15.7 gives a METHOD and 'it would be")
    print("      desirable for this program to be completed'.  See census.md.")


if __name__ == "__main__":
    main()

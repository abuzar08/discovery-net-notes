"""Reading BORS Figure 15.1 (the (T,U)-configurations) from the primary source.

arXiv:1312.3712 page 145 was rendered to an image and read directly.  The
figure shows **31 configurations in five groups**, of sizes

    20,  3,  5,  2,  1

which are exactly the five (|T|,|U|) classes that Definition 15.21 admits.
Theorem 17.1(3)'s "one of at most twenty patches" is therefore the size of the
LARGEST class, not the number of patches: the branching per degree-3 vertex is
the sum, 31, because the growing-back procedure of Section 15.5 first CHOOSES
the type (T_v, U_v) and then a configuration of that type.

Six of the 31 -- the whole of the groups of size 1, 2 and 3, and two of the
group of 5 -- are transcribed below and gated on this file's own
implementation of Definition 15.21.  The gate is what matters: a
mis-transcription almost always changes the class.

Two independent confirmations of the reading:
  * within each group every transcription lands in the SAME class;
  * the group of three lands in (3,2), and BORS state in the proof of
    Lemma 15.27 that "K_v can be at most one of the three figures in
    Figure 15.1 corresponding to (|T|,|U|) = (3,2)".

Note the configurations are MULTIGRAPHS: the lens shapes in the figure are
pairs of parallel edges, and they carry the structure.  Edge connectivity must
therefore be computed with capacities equal to multiplicities.  An earlier
enumeration of mine (Discovery Net height 2929) built only simple graphs and so
was searching the wrong universe entirely.

    uv run --with networkx python figure_15_1.py
"""
import networkx as nx

TERMS = ('x', 'y', 'z')


def capacity_graph(edges):
    """Simple graph whose edge capacities are the parallel-edge multiplicities."""
    C = nx.Graph()
    C.add_nodes_from(TERMS)
    for u, v in edges:
        if C.has_edge(u, v):
            C[u][v]['capacity'] += 1
        else:
            C.add_edge(u, v, capacity=1)
    return C


def classify(edges):
    """(|T|, |U|) of Definition 15.21, for a multigraph given as an edge list."""
    C = capacity_graph(edges)
    T = set()
    for w in TERMS:
        others = [t for t in TERMS if t != w]
        D = C.copy()
        D.add_node('SINK')
        for t in others:
            D.add_edge(t, 'SINK', capacity=10 ** 6)
        if nx.maximum_flow_value(D, w, 'SINK', capacity='capacity') >= 2:
            T.add(w)
    U = set()
    for w in TERMS:
        others = [t for t in TERMS if t != w]
        D = C.copy()
        D.remove_node(w)
        if all(o in D for o in others) and nx.has_path(D, *others) and \
                nx.maximum_flow_value(D, *others, capacity='capacity') >= 2:
            U.add(w)
    return len(T), len(U)


def apex_planar(edges):
    """The configuration condition: H+ (apex joined to x, y, z) is planar."""
    S = nx.Graph()
    S.add_nodes_from(TERMS)
    S.add_edges_from({tuple(sorted(e)) for e in edges})
    S.add_node('apex')
    for t in TERMS:
        S.add_edge('apex', t)
    return nx.check_planarity(S, counterexample=False)[0]


# transcribed from the rendered page; 'a', 'b' are internal (filled) vertices,
# x, y, z are the three terminals (open circles)
TRANSCRIBED = [
    ("group of 1  claw, the trivial patch",
     [('x', 'a'), ('y', 'a'), ('z', 'a')], (0, 0)),
    ("group of 2  #1  x=a doubled, a-y, a-z",
     [('x', 'a'), ('x', 'a'), ('y', 'a'), ('z', 'a')], (1, 0)),
    ("group of 2  #2  triangle x,a,b with a-y and b-z",
     [('x', 'a'), ('x', 'b'), ('a', 'b'), ('y', 'a'), ('z', 'b')], (1, 0)),
    ("group of 3  #1  x-a, x-b, a-b, a=y doubled, b=z doubled",
     [('x', 'a'), ('x', 'b'), ('a', 'b'), ('y', 'a'), ('y', 'a'),
      ('z', 'b'), ('z', 'b')], (3, 2)),
    ("group of 5  #1  x-a, a=y doubled, a=z doubled",
     [('x', 'a'), ('y', 'a'), ('y', 'a'), ('z', 'a'), ('z', 'a')], (2, 1)),
    ("group of 5  #2  x-a, a-b, a-y, a-z, b-y, b-z",
     [('x', 'a'), ('a', 'b'), ('a', 'y'), ('a', 'z'), ('b', 'y'),
      ('b', 'z')], (2, 1)),
]

GROUPS = {(3, 3): 20, (2, 1): 5, (3, 2): 3, (1, 0): 2, (0, 0): 1}


def main():
    print(f"{'transcription':52} {'(|T|,|U|)':>10} {'apex planar':>12} {'gate':>6}")
    ok = True
    for name, E, expect in TRANSCRIBED:
        got, planar = classify(E), apex_planar(E)
        good = (got == expect) and planar
        ok = ok and good
        print(f"{name:52} {str(got):>10} {str(planar):>12} "
              f"{'ok' if good else 'FAIL':>6}")
    assert ok

    print("\nFigure 15.1: 31 configurations in five groups")
    print(f"{'class':>10} {'group size':>11}")
    for c, n in sorted(GROUPS.items(), key=lambda t: -t[1]):
        print(f"{str(c):>10} {n:>11}")
    print(f"{'total':>10} {sum(GROUPS.values()):>11}")
    print("\nBranching per degree-3 vertex is the SUM, 31: Section 15.5 chooses")
    print("the type first and then a configuration of that type.  Theorem")
    print("17.1(3)'s 'at most twenty' is the largest class, (3,3).")


if __name__ == "__main__":
    main()

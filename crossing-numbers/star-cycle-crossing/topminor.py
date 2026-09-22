"""K_{1,1,1,m} is a TOPOLOGICAL minor of K_{1,m} box C_3: delete one edge from
each leaf triangle and suppress the resulting degree-2 vertices.  Crossing number
is monotone under topological minors (subgraph-monotone, subdivision-invariant),
so this gives cr(K_{1,m} box C_3) >= cr(K_{1,1,1,m}) -- the direction that
CONTRACTION cannot give, since cr is not minor-monotone.

The same reduction fails for C_n with n >= 4, and `check_n` verifies that.
"""
import networkx as nx


def star_box_cycle(m, n):
    return nx.cartesian_product(nx.star_graph(m), nx.cycle_graph(n))


def join_cycle_empty(n, m):
    """C_n + complement(K_m).  For n = 3 this is K_{1,1,1,m}."""
    G = nx.cycle_graph(n)
    for j in range(m):
        for i in range(n):
            G.add_edge(('v', j), i)
    return G


def suppress(G):
    """Repeatedly suppress degree-2 vertices (inverse of subdivision)."""
    H = nx.Graph(G)
    while True:
        v = next((v for v in H if H.degree(v) == 2), None)
        if v is None:
            return H
        a, b = list(H.neighbors(v))
        H.remove_node(v)
        H.add_edge(a, b)


def reduced(m, n):
    """Delete edge (j,1)-(j,2) from every leaf cycle, then suppress."""
    G = star_box_cycle(m, n)
    H = nx.Graph(G)
    for j in range(1, m + 1):
        H.remove_edge((j, 1), (j, 2))
    return suppress(H)


def check_n(n, ms=(2, 3, 4)):
    return [nx.is_isomorphic(reduced(m, n), join_cycle_empty(n, m)) for m in ms]


if __name__ == '__main__':
    for m in range(2, 14):
        print('m', m, nx.is_isomorphic(reduced(m, 3), join_cycle_empty(3, m)))
    for n in (3, 4, 5, 6):
        print('n', n, check_n(n))          # only n = 3 succeeds

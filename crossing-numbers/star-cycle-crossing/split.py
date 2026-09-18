"""Triangle-splitting: K_{1,1,1,m} with each degree-3 vertex blown up into a
triangle is exactly K_{1,m} box C_3.  Verifies the graph identity underlying
cr(K_{1,m} box C_3) <= cr(K_{1,1,1,m})."""
import networkx as nx

X = lambda m: (m // 2) * ((m - 1) // 2)


def K111m(m):
    G = nx.Graph()
    for x in 'abc':
        for y in 'abc':
            if x < y:
                G.add_edge(x, y)
    for j in range(m):
        for x in 'abc':
            G.add_edge(x, ('v', j))
    return G


def split_deg3(G, nodes):
    """Replace each degree-3 node by a triangle, one triangle vertex per
    incident edge.  A triangle is symmetric under every permutation of its
    vertices, so the resulting graph does not depend on the attachment order --
    only the drawing does."""
    H = nx.Graph(G)
    for v in nodes:
        nb = list(G.neighbors(v))
        assert len(nb) == 3, (v, len(nb))
        H.remove_node(v)
        t = [(v, i) for i in range(3)]
        for i in range(3):
            H.add_edge(t[i], t[(i + 1) % 3])
            H.add_edge(t[i], nb[i])
    return H


def check(m):
    K = K111m(m)
    S = split_deg3(K, [('v', j) for j in range(m)])
    G = nx.cartesian_product(nx.star_graph(m), nx.cycle_graph(3))
    return nx.is_isomorphic(S, G)


if __name__ == '__main__':
    for m in range(2, 13):
        print(m, check(m))

"""Independent checks of the height-5504 theorem cr(K_1m box C_3) = cr(K_1,1,1,m).

(1) the lower-bound topological minor: delete l_{j,1}l_{j,2} from each leaf
    triangle, suppress the degree-2 vertices, compare with the join;
(2) the asymmetry: the same deletion at n = 4,5,6;
(3) the splitting upper bound at n = 3,4,5,6;
(4) the degree census behind the general n >= 4 obstruction.
"""
import sys, itertools, collections
sys.path.insert(0, '.')
import networkx as nx
from indep_chiasim import star_cycle


def join_cycle(n, m):
    """C_n + complement of K_m; at n = 3 this is K_{1,1,1,m}."""
    G = nx.Graph()
    for i in range(n):
        G.add_edge(('c', i), ('c', (i + 1) % n))
    for j in range(m):
        for i in range(n):
            G.add_edge(('v', j), ('c', i))
    return G


def suppress(G):
    H = G.copy()
    changed = True
    while changed:
        changed = False
        for v in list(H.nodes()):
            if H.degree(v) == 2:
                a, b = list(H.neighbors(v))
                if a != b and not H.has_edge(a, b):
                    H.remove_node(v)
                    H.add_edge(a, b)
                    changed = True
                    break
    return H


def split_join(n, m):
    """Split each large-part vertex of the join into an n-cycle."""
    H = join_cycle(n, m)
    for j in range(m):
        v = ('v', j)
        nb = list(H.neighbors(v))
        H.remove_node(v)
        ts = [('t', j, k) for k in range(n)]
        for k in range(n):
            H.add_edge(ts[k], ts[(k + 1) % n])
        for e, t in zip(nb, ts):
            H.add_edge(e, t)
    return H


def deleted(m, n):
    G = star_cycle(m, n).copy()
    for j in range(1, m + 1):
        G.remove_edge((1, j), (2, j))
    return G


if __name__ == '__main__':
    print('(1) lower-bound subdivision, m = 2..13')
    bad = [m for m in range(2, 14)
           if not nx.is_isomorphic(suppress(deleted(m, 3)), join_cycle(3, m))]
    print('   isomorphic to K_1,1,1,m for every m:', not bad, bad)

    print('(2) the same deletion at n >= 4')
    for n in (4, 5, 6):
        for m in (3, 4):
            S, J = suppress(deleted(m, n)), join_cycle(n, m)
            print('   n=%d m=%d: %d/%d vs join %d/%d  isomorphic %s'
                  % (n, m, S.number_of_nodes(), S.number_of_edges(),
                     J.number_of_nodes(), J.number_of_edges(),
                     nx.is_isomorphic(S, J)))

    print('(3) splitting upper bound')
    for n in (3, 4, 5, 6):
        print('   n=%d:' % n, all(nx.is_isomorphic(split_join(n, m), star_cycle(m, n))
                                  for m in (2, 3, 4, 5)))

    print('(4) degree census')
    for n in (3, 4, 5, 6, 7):
        for m in (1, 2, 3, 5, 8):
            G, H = star_cycle(m, n), join_cycle(n, m)
            g4 = sum(1 for _, d in G.degree() if d >= 4)
            h4 = sum(1 for _, d in H.degree() if d >= 4)
            print('   n=%d m=%d: G has %d vertices of degree >= 4, H needs %d'
                  % (n, m, g4, h4))

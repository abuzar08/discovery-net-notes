r"""reviewer-1: independent check of the six Clancy-survey claims at their
smallest admissible parameter, as reported at height 5070.

Exact crossing numbers by exhaustive planarisation over pairs of independent
edges (valid because an optimal drawing crosses only independent edges), with
skewness as the cheap lower bound.
"""
import itertools

import networkx as nx


def star_cycle(m, n):
    G = nx.Graph()
    for c in range(n):
        for j in range(1, m + 1):
            G.add_edge((c, 0), (c, j))
        for j in range(m + 1):
            G.add_edge((c, j), ((c + 1) % n, j))
    return G


def strong_grid(n, m):
    """P_n strong product P_m"""
    G = nx.Graph()
    for i in range(n):
        for j in range(m):
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    a, b = i + di, j + dj
                    if (di or dj) and 0 <= a < n and 0 <= b < m:
                        G.add_edge((i, j), (a, b))
    return G


def flower_snark(n):
    """I_n: n copies of K_{1,3} in a cycle, classical construction"""
    G = nx.Graph()
    for i in range(n):
        for k in (1, 2, 3):
            G.add_edge(('c', i), (k, i))
        G.add_edge((1, i), (1, (i + 1) % n))                 # inner cycle
    for i in range(n):
        G.add_edge((2, i), (2, (i + 1) % n) if i < n - 1 else (3, 0))
        G.add_edge((3, i), (3, (i + 1) % n) if i < n - 1 else (2, 0))
    return G


def skew_le(G, k):
    es = list(G.edges())
    for j in range(k + 1):
        for sub in itertools.combinations(es, j):
            H = G.copy()
            H.remove_edges_from(sub)
            if nx.check_planarity(H, counterexample=False)[0]:
                return j
    return None


def cr_le(G, k):
    """is cr(G) <= k? planarise by replacing crossings of independent edges"""
    if nx.check_planarity(G, counterexample=False)[0]:
        return 0
    if k == 0:
        return None
    es = [tuple(sorted(map(str, e))) for e in G.edges()]
    edges = list(G.edges())
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            (a, b), (c, d) = edges[i], edges[j]
            if len({a, b, c, d}) < 4:
                continue
            H = G.copy()
            H.remove_edge(a, b)
            H.remove_edge(c, d)
            x = ('x', i, j)
            H.add_edges_from([(a, x), (x, b), (c, x), (x, d)])
            r = cr_le(H, k - 1)
            if r is not None:
                return r + 1
    return None


def exact_cr(G, cap=4):
    for k in range(cap + 1):
        r = cr_le(G, k)
        if r is not None:
            return r
    return None


def main():
    print('Clancy survey claims at their smallest admissible parameter:')
    G = star_cycle(3, 3)
    print(f'   cr(S_3 x C_3): {G.number_of_nodes()} vertices, '
          f'{G.number_of_edges()} edges, skewness {skew_le(G, 3)}, '
          f'exact cr {exact_cr(G, 3)} (stated 1)', flush=True)
    G = star_cycle(4, 3)
    print(f'   cr(S_4 x C_3): {G.number_of_nodes()} vertices, '
          f'{G.number_of_edges()} edges, skewness {skew_le(G, 3)}, '
          f'exact cr {exact_cr(G, 3)} (stated 2)', flush=True)
    for n in (2, 3, 4):
        G = strong_grid(n, 2)
        print(f'   cr(P_{n} strong P_2): {G.number_of_nodes()} vertices, '
              f'{G.number_of_edges()} edges, exact cr {exact_cr(G, 3)} '
              f'(stated n-2 = {n-2})', flush=True)
    for n in (3, 4, 5):
        G = nx.cartesian_product(nx.star_graph(n), nx.star_graph(1))
        print(f'   S_{n} x S_1 planar: '
              f'{nx.check_planarity(G, counterexample=False)[0]} (stated cr 0)')
    G = flower_snark(3)
    print(f'   I_3 (Flower Snark): {G.number_of_nodes()} vertices, '
          f'{G.number_of_edges()} edges, cubic '
          f'{all(d == 3 for _, d in G.degree())}, exact cr {exact_cr(G, 3)} '
          f'(stated 2)', flush=True)


if __name__ == '__main__':
    main()

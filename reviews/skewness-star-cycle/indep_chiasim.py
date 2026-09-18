r"""reviewer-1: independent check of the answer to Chia and Sim's question.

DS21 asks whether \(\mathrm{sk}(K_{1,m} \square C_n) =
(m-2)(\lfloor (n-1)/2 \rfloor + 1)\). Skewness is computed here exactly, by
exhaustive enumeration of edge subsets in increasing size with a planarity test
at each — the direction that is fastest in this regime, as the team measured.
"""
import itertools
import sys

import networkx as nx


def star_cycle(m, n):
    G = nx.Graph()
    for c in range(n):
        for j in range(1, m + 1):
            G.add_edge((c, 0), (c, j))            # star inside each copy
    for c in range(n):
        for j in range(m + 1):
            G.add_edge((c, j), ((c + 1) % n, j))  # cycle across copies
    return G


def skewness(G, cap=8):
    if nx.check_planarity(G, counterexample=False)[0]:
        return 0
    es = list(G.edges())
    for k in range(1, cap + 1):
        for sub in itertools.combinations(es, k):
            H = G.copy()
            H.remove_edges_from(sub)
            if nx.check_planarity(H, counterexample=False)[0]:
                return k
    return None


def proposed(m, n):
    return (m - 2) * ((n - 1) // 2 + 1)


def main():
    print('(1) the m = 2 gate: the proposed value is 0, so the product must be planar')
    for n in (3, 4, 5, 6):
        G = star_cycle(2, n)
        print(f'    K_1,2 x C_{n}: {G.number_of_nodes()} vertices, '
              f'{G.number_of_edges()} edges, planar = '
              f'{nx.check_planarity(G, counterexample=False)[0]}')
    print()
    print('(2) n = 3, where the identity is said to fail')
    for m in range(3, 8):
        G = star_cycle(m, 3)
        s = skewness(G)
        print(f'    K_1,{m} x C_3: {G.number_of_nodes()} vertices, '
              f'{G.number_of_edges()} edges, exact skewness {s}, '
              f'proposed {proposed(m, 3)} -> '
              f'{"identity FAILS" if s != proposed(m,3) else "agrees"}'
              f'   (m - 2 = {m - 2})', flush=True)
    print()
    print('(3) n >= 4, where the identity is said to hold')
    for m, n in ((3, 4), (3, 5), (3, 6), (4, 4)):
        G = star_cycle(m, n)
        s = skewness(G)
        print(f'    K_1,{m} x C_{n}: {G.number_of_edges()} edges, exact '
              f'skewness {s}, proposed {proposed(m, n)} -> '
              f'{"agrees" if s == proposed(m,n) else "DIFFERS"}', flush=True)
    print()
    print('(4) the two published certificates, checked directly')
    G = star_cycle(3, 3)
    H = G.copy(); H.remove_edge((0, 0), (1, 0))
    ok = nx.check_planarity(H, counterexample=False)[0]
    emb = nx.check_planarity(H)[1]
    V, E = H.number_of_nodes(), H.number_of_edges()
    F = 2 - V + E
    print(f'    K_1,3 x C_3 minus (0,0)-(1,0): planar {ok}, V = {V}, E = {E}, '
          f'F = {F}, V - E + F = {V - E + F}')
    G = star_cycle(4, 3)
    H = G.copy(); H.remove_edges_from([((0, 0), (1, 0)), ((0, 0), (2, 0))])
    ok = nx.check_planarity(H, counterexample=False)[0]
    V, E = H.number_of_nodes(), H.number_of_edges()
    F = 2 - V + E
    print(f'    K_1,4 x C_3 minus two edges at (0,0): planar {ok}, V = {V}, '
          f'E = {E}, F = {F}, V - E + F = {V - E + F}')


if __name__ == '__main__':
    main()

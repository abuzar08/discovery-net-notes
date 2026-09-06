r"""reviewer-1: branch (1) of h3285 — Figure 14.1, the not-2-connected case."""
import networkx as nx, itertools, sys
import extract_fig as X
from indep_fig143 import verdict

def comps(page, minv=4):
    v, E = X.extract('bors.pdf', page)
    out = []
    for c in [c for c in X.components(v, E) if len(c) >= minv]:
        idx = {u: i for i, u in enumerate(sorted(c))}
        G = nx.Graph(); G.add_nodes_from(range(len(c)))
        for (a, b), m in E.items():
            if a in idx and b in idx:
                G.add_edge(idx[a], idx[b])
        out.append(G)
    return out

for page in range(122, 129):
    try:
        cs = comps(page)
    except Exception as e:
        continue
    if not cs:
        continue
    print(f'page {page}: {len(cs)} components with >= 4 vertices, (n,m) '
          f'{sorted((G.number_of_nodes(), G.number_of_edges()) for G in cs)}')
    if len(cs) == 16:
        K5, K33 = nx.complete_graph(5), nx.complete_bipartite_graph(3, 3)
        conn1 = [G for G in cs if nx.node_connectivity(G) == 1]
        pieces = [G for G in cs if nx.is_isomorphic(G, K5) or nx.is_isomorphic(G, K33)]
        print(f'   connectivity 1: {len(conn1)}, of which min degree >= 3: '
              f'{sum(1 for G in conn1 if min(dict(G.degree).values()) >= 3)}, '
              f'all CRIT2: {all(verdict(G) == "CRIT2" for G in conn1)}')
        print(f'   isomorphic to K5 or K_{{3,3}}: {len(pieces)} '
              f'({sum(1 for G in pieces if nx.is_isomorphic(G, K5))} x K5, '
              f'{sum(1 for G in pieces if nx.is_isomorphic(G, K33))} x K_{{3,3}})')
        unions = []
        for A, B in ((K5, K5), (K5, K33), (K33, K33)):
            U = nx.disjoint_union(A, B)
            unions.append(verdict(U))
        print(f'   the three disjoint unions K5+K5, K5+K33, K33+K33: verdicts {unions}')
        print(f'   total for branch (1): {len(conn1)} + 3 = {len(conn1) + 3}')

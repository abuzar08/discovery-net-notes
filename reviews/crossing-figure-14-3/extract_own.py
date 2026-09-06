r"""reviewer-1: pull the drawn components of BORS Figures 14.2/14.3 through the
lane's own extractor, then check their structural properties with my own code."""
import networkx as nx, collections, sys
import extract_fig as X

def components(page):
    v, E = X.extract('bors.pdf', page)
    out = []
    for c in [c for c in X.components(v, E) if len(c) >= 5]:
        idx = {u: i for i, u in enumerate(sorted(c))}
        G = nx.Graph(); G.add_nodes_from(range(len(c)))
        mult = 0
        for (a, b), m in E.items():
            if a in idx and b in idx:
                G.add_edge(idx[a], idx[b])
                mult += m - 1
        out.append((G, mult))
    return out

for page in (126, 127, 128):
    try:
        cs = components(page)
    except Exception as e:
        print(f'page {page}: {type(e).__name__} {e}'); continue
    print(f'page {page}: {len(cs)} components with >= 5 vertices; '
          f'(n,m) {sorted((G.number_of_nodes(), G.number_of_edges()) for G, _ in cs)[:6]}...')
    if cs:
        print(f'   2-connected: {sum(1 for G,_ in cs if nx.node_connectivity(G) >= 2)}, '
              f'3-connected: {sum(1 for G,_ in cs if nx.node_connectivity(G) >= 3)}, '
              f'min degree >= 3: {sum(1 for G,_ in cs if min(dict(G.degree).values()) >= 3)}, '
              f'with parallel edges dropped: {sum(1 for _,mu in cs if mu > 0)}')

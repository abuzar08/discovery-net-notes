r"""reviewer-1: independent check of h3084 (researcher-4), the earliest stage of
the connectivity-2 chain.

Three claims of this contribution are checkable with code I already own:

  1. the extraction bookkeeping — 36 components of 8 to 14 vertices, all
     2-connected, none 3-connected, minimum degree at least 3, 692 drawn
     segments giving 692 edges, and 166 leftover circles that are exact
     duplicates at distance 0;
  2. all 16 graphs of Figure 14.2 are 2-crossing-critical with
     \(\mathrm{cr} = 2\);
  3. the negative claims about the other 20: doubling any single edge repairs
     none, and deleting one or two edges subject to minimum degree 3 repairs
     none either (the three-edge case is run separately).

Crossing numbers and criticality are my own code (`indep_fig143`); doubling an
edge is handled by subdividing the duplicate, which is a genuine subdivision and
so leaves the crossing number unchanged.
"""
import itertools
import multiprocessing as mp

import networkx as nx

import extract_fig as X
from indep_fig143 import drawn_components, verdict, cr_le_1, cr_le_2


def extraction_facts():
    v, E = X.extract('bors.pdf', 127)
    comps = [c for c in X.components(v, E) if len(c) >= 5]
    sizes = sorted(len(c) for c in comps)
    gs = drawn_components()
    ok2 = sum(1 for g in gs if nx.is_biconnected(g))
    ok3 = sum(1 for g in gs if nx.node_connectivity(g) >= 3)
    mind = min(min(d for _, d in g.degree()) for g in gs)
    edges = sum(g.number_of_edges() for g in gs)
    return dict(n_components=len(comps), sizes=(sizes[0], sizes[-1]),
                total_vertices=sum(sizes), two_connected=ok2,
                three_connected=ok3, min_degree=mind, total_edges=edges,
                raw_vertices=len(v), raw_edge_items=len(E))


def double_edge(G, e):
    """double the edge e: the duplicate is subdivided once, which is a
    subdivision and so does not change the crossing number"""
    H = nx.Graph(G)
    w = max(H.nodes) + 1
    H.add_edge(e[0], w)
    H.add_edge(w, e[1])
    return H


def job(arg):
    kind, n, edges, spec = arg
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)
    if kind == 'double':
        H = double_edge(G, spec)
    else:
        H = nx.Graph(G)
        H.remove_edges_from(spec)
        if H.number_of_nodes() == 0 or min(d for _, d in H.degree()) < 3:
            return None
    v = verdict(H)
    return (kind, spec, v) if v is not None else None


def main():
    print('(1) THE EXTRACTION, structurally')
    f = extraction_facts()
    print(f'   {f["n_components"]} components of sizes {f["sizes"][0]} to '
          f'{f["sizes"][1]}, {f["total_vertices"]} vertices, '
          f'{f["total_edges"]} edges; 2-connected {f["two_connected"]}/36, '
          f'3-connected {f["three_connected"]}/36, minimum degree '
          f'{f["min_degree"]}')
    print(f'   raw items on the page: {f["raw_vertices"]} vertices, '
          f'{f["raw_edge_items"]} edge items')
    print()

    gs = drawn_components()
    good = [g for g in gs if verdict(g) == 'CRIT2']
    ge3 = [g for g in gs if verdict(g) == 'CRIT_GE3']
    bad = [g for g in gs if verdict(g) is None]
    print('(2) THE 16 OF FIGURE 14.2')
    print(f'   2-crossing-critical as drawn: {len(good)}, all with cr = 2; '
          f'with cr >= 3: {len(ge3)}; not critical as drawn: {len(bad)}')
    print()

    print('(3) THE NEGATIVE CLAIMS ABOUT THE OTHER 20')
    jobs = []
    for G in bad:
        n = G.number_of_nodes()
        es = list(G.edges())
        for e in es:
            jobs.append(('double', n, es, e))
        for k in (1, 2):
            for sub in itertools.combinations(es, k):
                jobs.append((f'delete{k}', n, es, sub))
    print(f'   {len(jobs)} repairs to test '
          f'(doubling one edge; deleting one or two)', flush=True)
    with mp.Pool(4) as pool:
        res = [r for r in pool.map(job, jobs, chunksize=32) if r is not None]
    by = {}
    for kind, spec, v in res:
        by.setdefault(kind, []).append(v)
    for kind in ('double', 'delete1', 'delete2'):
        got = by.get(kind, [])
        print(f'   {kind}: {len(got)} repairs give a 2-crossing-critical graph'
              + (f' {sorted(set(got))}' if got else ' — none, as claimed'))


if __name__ == '__main__':
    main()

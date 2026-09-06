r"""reviewer-1: recount with peripheral 4-connectivity read correctly (a 3-cut may
leave three components provided all are single vertices, since then every
partition into two nonempty groups has a side that is a single vertex)."""
import itertools, os, networkx as nx, indep_class as I

def p4c(G):
    if nx.node_connectivity(G) < 3:
        return False
    for X in itertools.combinations(G.nodes, 3):
        H = G.copy(); H.remove_nodes_from(X)
        comps = [len(c) for c in nx.connected_components(H)]
        if len(comps) < 2:
            continue
        if len(comps) == 2 and min(comps) == 1:
            continue
        if len(comps) == 3 and max(comps) == 1:
            continue
        return False
    return True

cen = I.read_census(os.path.dirname(os.path.abspath(__file__)))
three = [(n, m, G) for t, n, m, G in cen if nx.node_connectivity(G) >= 3]
V8, V10 = I.moebius_ladder(8), I.moebius_ladder(10)
P = [(n, m, G) for n, m, G in three if p4c(G)]
print(f'3-connected: {len(three)}; peripherally 4-connected (corrected test): {len(P)}')
print(f'  of those, by order: { {n: sum(1 for k,_,_ in P if k==n) for n in sorted({k for k,_,_ in P})} }')
print(f'  on at most ten vertices: {sum(1 for n,_,_ in P if n <= 10)}')
V = [(n, m, G) for n, m, G in three if I.has_subdivision(G, V8) or I.has_subdivision(G, V10)]
print(f'with a V8 or V10 subdivision: {len(V)}')
notP = [(n, m, G) for n, m, G in three if not p4c(G)]
print(f'not peripherally 4-connected: {len(notP)}')
nv = [(n, m, G) for n, m, G in notP if I.has_subdivision(G, V8) or I.has_subdivision(G, V10)]
print(f'  of those, with a V8 or V10 subdivision: {len(nv)}')
rest = [(n, m, G) for n, m, G in notP if not (I.has_subdivision(G, V8) or I.has_subdivision(G, V10))]
T = I.theorem_15_6_graphs()
four = [(n, m) for n, m, G in rest if any(nx.is_isomorphic(G, H) for H in T)]
print(f'  remainder: {len(rest)}, of which Theorem 15.6 graphs: {len(four)} {four}, leaving {len(rest)-len(four)}')
print(f'\npartition with the corrected test: {len(P)} + {len(nv)} + {len(rest)-len(four)} + {len(four)} = {len(P)+len(nv)+len(rest)}')

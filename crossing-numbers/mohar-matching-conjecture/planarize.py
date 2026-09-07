"""Crossing-minimisation by the planarisation heuristic (not restricted to 2 pages).

The 2-page search only explores book drawings, so it can overestimate cr.  This
explores general drawings: take a maximal planar subgraph, then insert the
remaining edges one at a time along a shortest path in the DUAL of the current
planarisation, each dual step being one crossing.  Randomising the planar
subgraph and the insertion order gives an upper bound on cr that can beat the
2-page value.
"""
import random
import networkx as nx


def faces_of(emb):
    """All faces of a planar embedding, as lists of darts."""
    seen = set()
    out = []
    for u in emb:
        for v in emb[u]:
            if (u, v) in seen:
                continue
            f = emb.traverse_face(u, v, mark_half_edges=seen)
            out.append(f)
    return out


def insert_edge(P, emb, u, v):
    """Insert u-v into planarisation P with the fewest crossings; return new P."""
    fs = faces_of(emb)
    # dual: face index -> face index, crossing the shared edge
    inc = {}
    for i, f in enumerate(fs):
        for a, b in zip(f, f[1:] + f[:1]):
            inc.setdefault(frozenset((a, b)), []).append(i)
    D = nx.Graph()
    D.add_nodes_from(range(len(fs)))
    for e, ff in inc.items():
        if len(ff) == 2:
            D.add_edge(ff[0], ff[1], edge=tuple(e))
    su = [i for i, f in enumerate(fs) if u in f]
    sv = [i for i, f in enumerate(fs) if v in f]
    D.add_node('S'); D.add_node('T')
    for i in su: D.add_edge('S', i, edge=None)
    for i in sv: D.add_edge(i, 'T', edge=None)
    try:
        path = nx.shortest_path(D, 'S', 'T')
    except nx.NetworkXNoPath:
        return None, None
    crossed = []
    for a, b in zip(path, path[1:]):
        e = D[a][b].get('edge')
        if e is not None:
            crossed.append(e)
    Q = nx.Graph(P)
    prev = u
    for k, (x, y) in enumerate(crossed):
        d = ('D', u, v, k)
        if not Q.has_edge(x, y):
            return None, None
        Q.remove_edge(x, y)
        Q.add_edge(x, d); Q.add_edge(d, y)
        Q.add_edge(prev, d)
        prev = d
    Q.add_edge(prev, v)
    ok, e2 = nx.check_planarity(Q)
    if not ok:
        return None, None
    return Q, e2


def crossings(G, seed=0, tries=1):
    rnd = random.Random(seed)
    best = None
    for _ in range(tries):
        E = list(G.edges()); rnd.shuffle(E)
        P = nx.Graph(); P.add_nodes_from(G.nodes())
        rest = []
        for u, v in E:
            P.add_edge(u, v)
            if not nx.check_planarity(P, counterexample=False)[0]:
                P.remove_edge(u, v); rest.append((u, v))
        ok, emb = nx.check_planarity(P)
        n = 0
        good = True
        for u, v in rest:
            P2, emb2 = insert_edge(P, emb, u, v)
            if P2 is None:
                good = False; break
            n += sum(1 for x in P2.nodes() if isinstance(x, tuple) and x[0] == 'D') - n0 if False else 0
            P, emb = P2, emb2
        if not good:
            continue
        c = sum(1 for x in P.nodes() if isinstance(x, tuple) and x[0] == 'D')
        if best is None or c < best:
            best = c
    return best


if __name__ == '__main__':
    import sys
    # validation on known values
    for name, G, val in [('K5', nx.complete_graph(5), 1),
                         ('K6', nx.complete_graph(6), 3),
                         ('K3,3', nx.complete_bipartite_graph(3,3), 1),
                         ('K7', nx.complete_graph(7), 9)]:
        b = crossings(G, seed=1, tries=60)
        print(f"  {name}: heuristic {b}, true {val}  {'OK' if b==val else '(upper bound)'}")

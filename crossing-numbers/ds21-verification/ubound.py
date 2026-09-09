"""Heuristic upper bounds on cr(G) by planarisation with dual edge insertion.

DS21 states its formulas as exact values.  So a *drawing* with fewer crossings
than a stated formula refutes that formula outright, with the drawing as the
certificate -- no lower bound and no exhaustive search needed.  Upper bounds
scale far past exact deciding, so this reaches exactly the entries the exact
sweep reports as undecided or out of range, which is where an error would
otherwise be least likely to be found.

The method is the standard planarisation heuristic:
  1. extract a maximal planar subgraph greedily in a random edge order;
  2. insert each remaining edge along a shortest path in the dual of the current
     planar embedding, so the number of crossings paid is the dual distance;
  3. split each crossed edge with a degree-4 dummy vertex and re-embed.
Randomised restarts; report the best drawing found.

This can only ever OVERestimate cr, never underestimate it, so a value below a
stated formula is a genuine refutation and a value above it proves nothing.
"""
import random, networkx as nx


def _faces(emb):
    """Face list, plus a map from directed edge to the face on its left."""
    faces, where, seen = [], {}, set()
    for u in emb:
        for v in emb[u]:
            if (u, v) in seen:
                continue
            face = emb.traverse_face(u, v, mark_half_edges=seen)
            i = len(faces)
            faces.append(face)
            for a, b in zip(face, face[1:] + face[:1]):
                where[(a, b)] = i
    return faces, where


def _dual(emb):
    """Dual multigraph: one node per face, one edge per primal edge."""
    faces, where = _faces(emb)
    D = nx.Graph()
    D.add_nodes_from(range(len(faces)))
    inc = {}                              # face -> set of primal vertices
    for i, f in enumerate(faces):
        inc[i] = set(f)
    for u, v in emb.to_undirected().edges():
        a, b = where[(u, v)], where[(v, u)]
        if a != b:
            D.add_edge(a, b, primal=(u, v))
    return D, inc


def _insert(G, u, v, tag):
    """Insert edge uv into planar G along a dual shortest path.

    Returns (H, crossings) or None if the route could not be realised.
    """
    ok, emb = nx.check_planarity(G)
    if not ok:
        return None
    D, inc = _dual(emb)
    src = [i for i, s in inc.items() if u in s]
    dst = {i for i, s in inc.items() if v in s}
    if not src or not dst:
        return None
    best = None
    for s in src:
        if s in dst:
            best = []
            break
        try:
            for t in dst:
                p = nx.shortest_path(D, s, t)
                if best is None or len(p) - 1 < len(best):
                    best = [D[a][b]["primal"] for a, b in zip(p, p[1:])]
        except nx.NetworkXNoPath:
            continue
    if best is None:
        return None
    H = G.copy()
    prev = u
    for j, (a, b) in enumerate(best):
        if not H.has_edge(a, b):
            return None
        d = ("x", tag, j)
        H.remove_edge(a, b)
        H.add_edges_from([(a, d), (d, b), (prev, d)])
        prev = d
    H.add_edge(prev, v)
    if not nx.check_planarity(H, counterexample=False)[0]:
        return None
    return H, len(best)


def upper(G, restarts=40, seed=0):
    """Best upper bound on cr(G) found; None if every restart failed."""
    rng = random.Random(seed)
    edges = list(G.edges())
    best = None
    for r in range(restarts):
        order = edges[:]
        rng.shuffle(order)
        P = nx.Graph()
        P.add_nodes_from(G.nodes())
        rest = []
        for e in order:                    # greedy maximal planar subgraph
            P.add_edge(*e)
            if not nx.check_planarity(P, counterexample=False)[0]:
                P.remove_edge(*e)
                rest.append(e)
        total, cur, failed = 0, P, False
        for j, (u, v) in enumerate(rest):
            got = _insert(cur, u, v, (r, j))
            if got is None:
                failed = True
                break
            cur, c = got
            total += c
        if not failed and (best is None or total < best):
            best = total
    return best


if __name__ == "__main__":
    import time
    KNOWN = [("K5", nx.complete_graph(5), 1),
             ("K6", nx.complete_graph(6), 3),
             ("K7", nx.complete_graph(7), 9),
             ("K8", nx.complete_graph(8), 18),
             ("K3,3", nx.complete_bipartite_graph(3, 3), 1),
             ("K4,4", nx.complete_bipartite_graph(4, 4), 4),
             ("K3,5", nx.complete_bipartite_graph(3, 5), 4),
             ("K4,5", nx.complete_bipartite_graph(4, 5), 8),
             ("K5,5", nx.complete_bipartite_graph(5, 5), 16),
             ("K2,2,2", nx.complete_multipartite_graph(2, 2, 2), 0)]
    print(f"{'graph':>8} {'known':>6} {'upper':>6}  verdict")
    for name, G, val in KNOWN:
        t = time.time()
        u = upper(G, restarts=60)
        # An upper bound BELOW a known exact value would mean the heuristic is
        # unsound, so that case is a hard failure, not a better answer.
        v = ("UNSOUND" if u is not None and u < val
             else "tight" if u == val else f"loose (+{u - val})")
        print(f"{name:>8} {val:>6} {str(u):>6}  {v}   ({time.time()-t:.1f}s)", flush=True)

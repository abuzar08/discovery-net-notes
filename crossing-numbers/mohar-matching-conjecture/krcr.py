"""Exact crossing number by branching on Kuratowski subdivisions.

Blind enumeration of k crossing pairs is hopeless at 25 edges (C(168,8) ~ 1e13).
But in any good drawing every Kuratowski subdivision must carry a crossing, and
in an optimal drawing crossings occur only between INDEPENDENT edges.  So: find a
Kuratowski subdivision of the current graph, branch over the independent pairs of
its edges, planarise each, and recurse with the budget reduced.  The branching
set is a handful of pairs from one subdivision rather than all pairs of the
graph, which is what makes it tractable.
"""
import networkx as nx


def kuratowski_edges(G):
    ok, cert = nx.check_planarity(G, counterexample=True)
    return None if ok else list(cert.edges())


def planarise(G, e, f, tag):
    H = nx.Graph(G)
    H.remove_edge(*e)
    H.remove_edge(*f)
    d = ('x', tag)
    H.add_edge(e[0], d); H.add_edge(d, e[1])
    H.add_edge(f[0], d); H.add_edge(d, f[1])
    return H


def _euler_lb(G):
    n, m = G.number_of_nodes(), G.number_of_edges()
    return max(0, m - (3 * n - 6))


def cr_le(G, k, tag=0, memo=None):
    """True iff cr(G) <= k.

    Memoisation is keyed by an EXACT isomorphism test inside a bucket of cheap
    invariants, never by a Weisfeiler-Lehman hash: WL is not a complete
    invariant, so using it as a memo key can merge non-isomorphic graphs and
    prune a branch that in fact succeeds.
    """
    if memo is None:
        memo = {}
    if nx.check_planarity(G, counterexample=False)[0]:
        return True
    if k <= 0 or _euler_lb(G) > k:
        return False
    key = (G.number_of_nodes(), G.number_of_edges(),
           tuple(sorted(d for _, d in G.degree())), k)
    bucket = memo.setdefault(key, [])
    for H, r in bucket:
        if nx.is_isomorphic(G, H):
            return r
    K = kuratowski_edges(G)
    for i in range(len(K)):
        for j in range(i + 1, len(K)):
            if len(set(K[i]) | set(K[j])) != 4:
                continue
            if cr_le(planarise(G, K[i], K[j], tag), k - 1, tag + 1, memo):
                bucket.append((G.copy(), True))
                return True
    bucket.append((G.copy(), False))
    return False


def cr(G, cap=40):
    k = _euler_lb(G)
    while k <= cap:
        if cr_le(G, k, memo={}):
            return k
        k += 1
    return None


if __name__ == '__main__':
    import time
    for name, G, val in [('K5', nx.complete_graph(5), 1),
                         ('K6', nx.complete_graph(6), 3),
                         ('K3,3', nx.complete_bipartite_graph(3, 3), 1),
                         ('K7', nx.complete_graph(7), 9),
                         ('K_{1,2,2,2}', nx.convert_node_labels_to_integers(
                             nx.complete_multipartite_graph(1, 2, 2, 2)), 3)]:
        t0 = time.time()
        v = cr(G)
        print(f"  cr({name}) = {v}   expected {val}   "
              f"{'OK' if v == val else 'MISMATCH'}   ({time.time()-t0:.1f}s)",
              flush=True)

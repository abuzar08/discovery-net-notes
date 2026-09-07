"""Exact crossing number by Kuratowski branching.

The decider in crk.py enumerates every set of k independent edge pairs, which is
exhaustive but explodes: at 18 edges and k = 5 it does not finish.

This one uses the standard branching step.  Let D be an optimal (hence good)
drawing of G with at most k crossings, and let K be any Kuratowski subdivision
in G.  The restriction D|K is a drawing of a non-planar graph, so it contains a
crossing, and that crossing is between two edges *of K*.  In a good drawing
adjacent edges do not cross, so the pair is independent.  Hence it suffices to
branch over independent pairs drawn from K alone, planarise each, and recurse
with k-1.  K is small, so the branching factor is small.

Soundness: every planarisation step is realisable, so a True answer exhibits a
drawing with at most k crossings.  Completeness: the argument above shows some
branch retains an optimal drawing.
"""
import itertools, time, networkx as nx

class Budget(Exception):
    """Raised when a case exhausts its time budget, so it is reported as
    undecided rather than silently answered."""

_deadline = [None]

def _planar_or_kuratowski(G):
    ok, cert = nx.check_planarity(G, counterexample=True)
    return (True, None) if ok else (False, cert)

def _cross(G, e, f, tag):
    """Replace the crossing of e and f by a dummy vertex."""
    H = G.copy()
    H.remove_edge(*e); H.remove_edge(*f)
    d = ("x", tag)
    H.add_node(d)
    for u in e + f:
        H.add_edge(u, d)
    return H

def euler_lb(G):
    """Euler lower bound on cr(G).

    A simple planar graph on n >= 3 vertices has at most 3n - 6 edges, and each
    crossing removed by planarisation costs at most one edge, so
    cr(G) >= m - 3n + 6.  If G is triangle-free the planar bound is 2n - 4 and
    the stronger cr(G) >= m - 2n + 4 applies.  Cheap, and it prunes whole depths.
    """
    n, m = G.number_of_nodes(), G.number_of_edges()
    if n < 3:
        return 0
    lb = m - 3 * n + 6
    if not any(nx.triangles(G).values()) if not G.is_directed() else False:
        lb = max(lb, m - 2 * n + 4)
    return max(0, lb)

def cr_le(G, k, _tag=0):
    """True iff cr(G) <= k."""
    if _deadline[0] is not None and time.time() > _deadline[0]:
        raise Budget()
    if euler_lb(G) > k:
        return False
    ok, K = _planar_or_kuratowski(G)
    if ok:
        return True
    if k == 0:
        return False
    KE = list(K.edges())
    for i in range(len(KE)):
        for j in range(i + 1, len(KE)):
            e, f = KE[i], KE[j]
            if set(e) & set(f):          # adjacent: never crosses in a good drawing
                continue
            if cr_le(_cross(G, e, f, (_tag, i, j)), k - 1, _tag + 1):
                return True
    return False

def cr(G, cap=12, budget=None):
    """Exact cr, or None if the budget is exhausted (never a wrong answer)."""
    _deadline[0] = None if budget is None else time.time() + budget
    try:
        return _cr(G, cap)
    except Budget:
        return None
    finally:
        _deadline[0] = None

def _cr(G, cap=12):
    for k in range(cap + 1):
        if cr_le(G, k):
            return k
    return None

if __name__ == "__main__":
    import time
    for name, G, want in [("K5", nx.complete_graph(5), 1),
                          ("K6", nx.complete_graph(6), 3),
                          ("K3,3", nx.complete_bipartite_graph(3, 3), 1),
                          ("K4,4", nx.complete_bipartite_graph(4, 4), 4),
                          ("K3,5", nx.complete_bipartite_graph(3, 5), 4),
                          ("K2,2,2", nx.complete_multipartite_graph(2,2,2), 0),
                          ("K1,1,2,2", nx.complete_multipartite_graph(1,1,2,2), 1)]:
        t = time.time(); got = cr(G)
        print(f"  cr({name}) = {got}  expected {want}  "
              f"{'OK' if got == want else 'FAIL'}  ({time.time()-t:.1f}s)", flush=True)

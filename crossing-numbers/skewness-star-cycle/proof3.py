"""Towards a proof that sk(K_{1,m} box C_3) = m-2.

Structure: K_{1,m} box C_3 is a centre triangle T_0 on the three copies of the
star's centre, together with m leaf triangles T_1..T_m, each joined to T_0 by
three rungs (the star edges, one in each layer).  So it is m triangular prisms
glued along a common triangle.

UPPER BOUND is the observed witness: delete m-2 rungs, all in one layer.
LOWER BOUND needs an argument.  Euler gives nothing: |V| = 3m+3, |E| = 6m+3,
and 6m+3 <= 3|V|-6 = 9m+3 always.

If G contains k pairwise EDGE-DISJOINT Kuratowski subdivisions then any
planarising set must contain an edge of each, so sk(G) >= k.  This measures how
many the graph actually contains.
"""
import sys, networkx as nx
sys.path.insert(0, '.')
from chiasim import star_box_cycle, planar

def disjoint_kuratowski(G):
    """Greedily peel edge-disjoint Kuratowski subdivisions; return the count."""
    H = G.copy(); found = 0
    while True:
        ok, K = nx.check_planarity(H, counterexample=True)
        if ok:
            return found
        H.remove_edges_from(list(K.edges()))
        found += 1

def rung_only_disjoint(G, m):
    """Same, but peel only ONE edge per subdivision -- a hitting set lower bound
    is what we want, so instead count subdivisions that are pairwise disjoint by
    construction rather than by greedy peeling of whole subdivisions."""
    return None

if __name__ == "__main__":
    print("how many edge-disjoint Kuratowski subdivisions does the greedy peel find?")
    print(f"{'m':>2} {'|V|':>4} {'|E|':>4} {'m-2':>4} {'greedy disjoint':>16}")
    for m in range(3, 9):
        G = star_box_cycle(m, 3)
        d = disjoint_kuratowski(G)
        print(f"{m:>2} {G.number_of_nodes():>4} {G.number_of_edges():>4} {m-2:>4} {d:>16}", flush=True)

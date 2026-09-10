"""Skewness <= k by Kuratowski branching.

Any set of edges whose deletion planarises G must contain at least one edge of
EVERY Kuratowski subdivision in G.  So instead of trying all C(m,k) edge sets,
find one Kuratowski subgraph, branch only over its edges, and recurse on the
remainder.  Exhaustive by the same argument that justifies Kuratowski branching
for the crossing number.

networkx returns a Kuratowski subgraph for free as its planarity counterexample,
so each branching level costs one planarity test.
"""
import sys, time, networkx as nx

def skew_le(G, k):
    ok, K = nx.check_planarity(G, counterexample=True)
    if ok:
        return True
    if k == 0:
        return False
    for e in list(K.edges()):
        H = G.copy(); H.remove_edge(*e)
        if skew_le(H, k - 1):
            return True
    return False

if __name__ == "__main__":
    for nm, G, k, want in [("K5", nx.complete_graph(5), 1, True),
                           ("K5", nx.complete_graph(5), 0, False),
                           ("K6", nx.complete_graph(6), 3, True),
                           ("K6", nx.complete_graph(6), 2, False),
                           ("K3,3", nx.complete_bipartite_graph(3,3), 1, True),
                           ("K3,3", nx.complete_bipartite_graph(3,3), 0, False),
                           ("K7", nx.complete_graph(7), 4, False)]:
        got = skew_le(G, k)
        print(f"  validate skewness({nm}) <= {k}: {got}, expected {want}  "
              f"{'OK' if got == want else 'FAIL'}", flush=True)
        if got != want: sys.exit("branching skewness failed validation")
    print(flush=True)
    n = hits = 0; t0 = time.time()
    for line in open(sys.argv[1]):
        line = line.strip()
        if not line: continue
        G = nx.from_graph6_bytes(line.encode())
        if skew_le(G, 3):
            hits += 1
            print("HIT", line, flush=True)
        n += 1
    el = time.time() - t0
    print(f"\n{n} graphs in {el:.1f}s = {n/el:.1f}/sec; skewness<=3: {hits}")

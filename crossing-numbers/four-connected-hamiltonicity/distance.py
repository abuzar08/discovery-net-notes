"""How far are the known 4-connected non-Hamiltonian graphs from cr = 3?

This is the gate for the construction lane.  Reducing an example's crossing
number to 3 while preserving 4-connectivity and non-Hamiltonicity is only worth
attempting if some example is CLOSE to 3.  If the minimum over everything known
is 8, the reduction has to remove five crossings and the lane is not worth
opening; if something sits at 4 or 5, it is.

The heuristic only overestimates, so these are upper bounds: the true minimum is
at most what is reported, which is the direction that matters here -- a small
upper bound means a genuinely close example.
"""
import sys, networkx as nx, ubound

for nm, G, v in [("K7", nx.complete_graph(7), 9), ("K8", nx.complete_graph(8), 18),
                 ("K5,5", nx.complete_bipartite_graph(5,5), 16)]:
    u = ubound.upper(G, restarts=60)
    print(f"  validate cr({nm}) = {u}, expected {v}  {'OK' if u==v else 'FAIL'}", flush=True)
    if u != v: sys.exit("instrument failed validation")
print(flush=True)

best = None; hist = {}
for i, line in enumerate(open(sys.argv[1])):
    line = line.strip()
    if not line: continue
    G = nx.from_graph6_bytes(line.encode())
    u = ubound.upper(G, restarts=50, seed=i)
    hist[u] = hist.get(u, 0) + 1
    if best is None or u < best[0]:
        best = (u, line, G.number_of_nodes(), G.number_of_edges())
        print(f"  new closest: cr <= {u}  {line}  |V|={G.number_of_nodes()} "
              f"|E|={G.number_of_edges()}", flush=True)
print(f"\nupper-bound distribution: {dict(sorted(hist.items()))}")
print(f"closest to cr = 3: {best}")
print(f"gap to close: {best[0] - 3} crossings")

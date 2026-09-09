"""Does the upper-bound heuristic beat 9 on M_{8,3}?

M_{8,3} = K_8 minus a 3-matching = K_{1,1,2,2,2}: 8 vertices, 25 edges.
The status map confines cr(M_{8,3}) to {8,9}; Mohar's Conjecture 5 predicts 9.
A drawing with 8 crossings would refute the conjecture at its tightest entry.
"""
import time, networkx as nx, ubound

G = nx.complete_graph(8)
for a, b in [(0, 1), (2, 3), (4, 5)]:
    G.remove_edge(a, b)
assert G.number_of_nodes() == 8 and G.number_of_edges() == 25
assert nx.is_isomorphic(G, nx.complete_multipartite_graph(1, 1, 2, 2, 2)), \
    "M_{8,3} should be K_{1,1,2,2,2}"

# Instrument revalidation, per standing practice.
for name, H, val in [("K7", nx.complete_graph(7), 9),
                     ("K8", nx.complete_graph(8), 18),
                     ("K5,5", nx.complete_bipartite_graph(5, 5), 16)]:
    u = ubound.upper(H, restarts=60)
    print(f"   validate cr({name}) = {u}, expected {val}  "
          f"{'OK' if u == val else 'FAIL'}", flush=True)

best = None
t0 = time.time()
for seed in range(40):
    u = ubound.upper(G, restarts=200, seed=seed)
    if u is not None and (best is None or u < best):
        best = u
        print(f"  seed {seed}: new best drawing with {best} crossings "
              f"({time.time()-t0:.0f}s)", flush=True)
    if best is not None and best <= 8:
        break
print(f"\nbest drawing found for M_(8,3): {best} crossings  ({time.time()-t0:.0f}s)")
print("REFUTES the conjectured 9" if best is not None and best < 9
      else "consistent with the conjectured 9 (upper bound only)")

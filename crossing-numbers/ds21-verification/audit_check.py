"""Check DS21 entries not covered by the earlier sweep."""
import networkx as nx, ubound, crk2

def X(n): return (n//2)*((n-1)//2)
def Z(m,n): return X(m)*X(n)
def K(*p): return nx.complete_multipartite_graph(*p)

for name, H, val in [("K7", nx.complete_graph(7), 9), ("K8", nx.complete_graph(8), 18),
                     ("K5,5", nx.complete_bipartite_graph(5,5), 16)]:
    u = ubound.upper(H, restarts=60)
    print(f"  validate cr({name}) = {u}, expected {val}  {'OK' if u==val else 'FAIL'}")

print(f"\n{'entry':>26} {'|V|':>4} {'|E|':>4} {'DS21':>6} {'upper':>6}  verdict")
cases = []
# cr(K_{1,1,1,n}) = X(n)   [Harborth, ref 441]
for n in range(2, 11):
    cases.append((f"K_(1,1,1,{n})", K(1,1,1,n), X(n)))
# cr(K_{1,1,4,n}) = Z(6,n) + 2n + 2*floor(n/2)   [ref 782]
for n in range(1, 9):
    cases.append((f"K_(1,1,4,{n})", K(1,1,4,n), Z(6,n) + 2*n + 2*(n//2)))
# "cr(K_{3,3,n}) >= Z(6,n)+2n+1; this implies cr(K_{3,3,3}) = 15"
cases.append(("K_(3,3,3) [claimed 15]", K(3,3,3), 15))
# cr(K_{1,m,n}) = Z(m+1,n+1) - floor(m/2)floor(n/2), conditional on Zarankiewicz
for m, n in [(2,2),(2,3),(2,4),(3,3),(3,4),(4,4),(2,5),(3,5)]:
    cases.append((f"K_(1,{m},{n})", K(1,m,n), Z(m+1,n+1) - (m//2)*(n//2)))

for label, G, pred in cases:
    u = ubound.upper(G, restarts=60, seed=1)
    if u is None:
        v = "no drawing"
    elif u < pred:
        v = f"*** REFUTED: drawing with {u} < {pred} ***"
    elif u == pred:
        v = "consistent (tight)"
    else:
        v = f"consistent (upper +{u-pred})"
    print(f"{label:>26} {G.number_of_nodes():>4} {G.number_of_edges():>4} "
          f"{pred:>6} {str(u):>6}  {v}", flush=True)

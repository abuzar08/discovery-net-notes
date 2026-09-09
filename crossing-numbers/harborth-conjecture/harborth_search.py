"""One-sided search for a counterexample to Harborth's conjecture (tripartite).

Harborth conjectures cr(K_{n1,n2,n3}) = A(n1,n2,n3); only cr <= A is known in
general, together with 0.666 A <= cr asymptotically (Gethner et al.).  So the
conjecture is open with a factor-1.5 gap, and a DRAWING with fewer than A
crossings would refute it outright, with the drawing as certificate.

The heuristic only ever overestimates cr, so:
  found <  A   ->  Harborth REFUTED, certificate in hand
  found == A   ->  the bound is reproduced; consistent
  found >  A   ->  nothing follows (heuristic weakness)

Cases where DS21 records a proved formula are kept in the sweep on purpose: they
are free validation, since there the answer must come out equal.
"""
import sys, time, networkx as nx, ubound
from harborth import A, X, Z

PROVED = set()
for n in range(1, 20):
    for t in [(1,3,n),(2,3,n),(1,4,n),(2,4,n)]:
        PROVED.add(tuple(sorted(t)))
    for m in range(1, 20):
        PROVED.add(tuple(sorted((1,m,n))))    # conditional on Zarankiewicz

for name, G, val in [("K7", nx.complete_graph(7), 9), ("K8", nx.complete_graph(8), 18),
                     ("K5,5", nx.complete_bipartite_graph(5,5), 16)]:
    u = ubound.upper(G, restarts=60)
    print(f"  validate cr({name}) = {u}, expected {val}  {'OK' if u==val else 'FAIL'}")
    if u != val:
        sys.exit("instrument failed validation")

print(f"\n{'graph':>12} {'|V|':>4} {'|E|':>4} {'A':>6} {'found':>6}  status   verdict")
hits = []
cases = []
for a in range(2, 8):
    for b in range(a, 8):
        for c in range(b, 9):
            if a + b + c <= 16:
                cases.append((a, b, c))
cases.sort(key=lambda t: (t[0]*t[1] + t[0]*t[2] + t[1]*t[2]))
for a, b, c in cases:
    G = nx.complete_multipartite_graph(a, b, c)
    pred = A(a, b, c)
    t0 = time.time()
    u = ubound.upper(G, restarts=40, seed=a*100+b*10+c)
    st = "proved" if tuple(sorted((a,b,c))) in PROVED else "OPEN"
    if u is None:
        v = "no drawing"
    elif u < pred:
        v = f"*** REFUTES Harborth: {u} < {pred} ***"
        hits.append((a,b,c,pred,u))
    elif u == pred:
        v = "reproduces A"
    else:
        v = f"above by {u-pred}"
    print(f"K_({a},{b},{c}){'':>3} {G.number_of_nodes():>4} {G.number_of_edges():>4} "
          f"{pred:>6} {str(u):>6}  {st:>6}   {v}   ({time.time()-t0:.1f}s)", flush=True)

print("\n=== counterexamples ===")
print("none" if not hits else "\n".join(map(str, hits)))

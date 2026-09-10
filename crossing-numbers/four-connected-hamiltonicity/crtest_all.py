"""Decisive test on every 4-connected non-Hamiltonian graph at n = 10.

Ozeki and Zamfirescu: every 4-connected graph with cr <= 2 is Hamiltonian.
So each graph here already has cr >= 3, and "cr <= 3?" is decisive:
  TRUE  -> cr = 3 exactly -> 4-connected, non-Hamiltonian, cr = 3
           -> the DS21 open question is settled, negatively, with a certificate
  FALSE -> not a counterexample at cr = 3
"""
import sys, networkx as nx, crk2, ubound

for nm, G, v in [("K5", nx.complete_graph(5), 1), ("K6", nx.complete_graph(6), 3),
                 ("K3,3", nx.complete_bipartite_graph(3,3), 1),
                 ("K4,4", nx.complete_bipartite_graph(4,4), 4)]:
    got = crk2.cr(G, cap=6)
    print(f"  validate cr({nm}) = {got}, expected {v}  {'OK' if got==v else 'FAIL'}", flush=True)
    if got != v: sys.exit("decider failed validation")
print(flush=True)

hits = []
for i, line in enumerate(open(sys.argv[1])):
    line = line.strip()
    if not line: continue
    G = nx.from_graph6_bytes(line.encode())
    le3 = crk2.cr_le(G.copy(), 3)
    ub = ubound.upper(G, restarts=60)
    if le3: hits.append(line)
    print(f"[{i+1:>3}] {line}  |E|={G.number_of_edges()}  upper={ub}  cr<=3? {le3}"
          + ("  *** COUNTEREXAMPLE ***" if le3 else ""), flush=True)
print(f"\ntested {i+1}; graphs with cr = 3: {len(hits)}")
print("none" if not hits else "\n".join(hits))

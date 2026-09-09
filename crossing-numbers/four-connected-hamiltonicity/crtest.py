"""Exact cr test on the 4-connected non-Hamiltonian survivors.

Ozeki and Zamfirescu proved every 4-connected graph with cr <= 2 is Hamiltonian,
so every graph here already has cr >= 3.  Hence testing cr <= 3 is decisive:
  cr <= 3 TRUE  -> cr = 3 exactly -> the DS21 open question is settled, negatively
  cr <= 3 FALSE -> this graph is not a counterexample at cr = 3
"""
import sys, networkx as nx, crk2, ubound

for nm, G, v in [("K5", nx.complete_graph(5), 1), ("K6", nx.complete_graph(6), 3),
                 ("K3,3", nx.complete_bipartite_graph(3,3), 1),
                 ("K4,4", nx.complete_bipartite_graph(4,4), 4)]:
    got = crk2.cr(G, cap=6)
    print(f"  validate cr({nm}) = {got}, expected {v}  {'OK' if got==v else 'FAIL'}")
    if got != v: sys.exit("decider failed validation")
print()

for line in sys.argv[1:]:
    G = nx.from_graph6_bytes(line.encode())
    ub = ubound.upper(G, restarts=80)
    le3 = crk2.cr_le(G.copy(), 3)
    print(f"{line}  |V|={G.number_of_nodes()} |E|={G.number_of_edges()}  "
          f"upper={ub}  cr<=3? {le3}"
          + ("   *** COUNTEREXAMPLE: 4-connected, non-Hamiltonian, cr = 3 ***" if le3 else ""),
          flush=True)

"""Node rate, to turn the tree size into a cost."""
import time, networkx as nx
G = nx.complete_graph(8)
for a, b in [(0,1),(2,3),(4,5)]:
    G.remove_edge(a, b)
def child(H, e, f, t):
    J = H.copy(); J.remove_edge(*e); J.remove_edge(*f)
    d = ("x", t)
    for u in e+f: J.add_edge(u, d)
    return J
# walk to a typical mid-depth node, then time expansion there
H = G
for d in range(4):
    ok, K = nx.check_planarity(H, counterexample=True)
    KE = list(K.edges())
    e, f = next((a,b) for i,a in enumerate(KE) for b in KE[i+1:] if not set(a)&set(b))
    H = child(H, e, f, d)
n = 0; t0 = time.time()
while time.time() - t0 < 20:
    ok, K = nx.check_planarity(H, counterexample=True)
    KE = list(K.edges())
    e, f = next((a,b) for i,a in enumerate(KE) for b in KE[i+1:] if not set(a)&set(b))
    child(H, e, f, n); n += 1
r = n / (time.time() - t0)
print(f"node rate at depth 4: {r:,.0f} nodes/sec (single core)")
for name, size in [("raw tree", 5.3e12), ("with isomorphism dedup (~285x)", 5.3e12/285)]:
    print(f"  {name:>34}: {size:.2g} nodes = {size/r/3600:,.0f} core-hours")

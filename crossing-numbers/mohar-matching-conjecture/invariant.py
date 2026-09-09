"""Is the Euler bound invariant under planarisation, relative to k?

Planarising one crossing removes 2 edges and adds a degree-4 dummy joined to
their 4 endpoints: n -> n+1, m -> m+2.  So

    lb = m - 3n + 6  ->  (m+2) - 3(n+1) + 6 = m - 3n + 5 = lb - 1,

while the budget goes k -> k-1.  Hence lb - k is INVARIANT along every branch:
if the Euler test does not fire at the root, it can never fire anywhere below it.
Checked empirically here rather than trusted.
"""
import random, networkx as nx
def lb(H):
    n, m = H.number_of_nodes(), H.number_of_edges()
    return max(0, m - 3*n + 6)
G = nx.complete_graph(8)
for a, b in [(0,1),(2,3),(4,5)]:
    G.remove_edge(a, b)
rng = random.Random(0)
H, k, bad = G, 8, 0
print(f"depth 0: lb = {lb(H)}, k = {k}, slack lb-k = {lb(H)-k}")
for d in range(1, 9):
    ok, K = nx.check_planarity(H, counterexample=True)
    if ok:
        print(f"depth {d}: planar"); break
    KE = list(K.edges())
    cand = [(a,b) for i,a in enumerate(KE) for b in KE[i+1:] if not set(a)&set(b)]
    e, f = rng.choice(cand)
    J = H.copy(); J.remove_edge(*e); J.remove_edge(*f)
    dd = ("x", d)
    for u in e+f: J.add_edge(u, dd)
    H, k = J, k-1
    s = lb(H) - k
    bad += (s != -1)
    print(f"depth {d}: lb = {lb(H)}, k = {k}, slack lb-k = {s}")
print("\nslack constant along the branch:", "YES" if bad == 0 else "NO")

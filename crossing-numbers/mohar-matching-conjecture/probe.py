"""Measure the actual branching, so any verdict names its own numbers.

The pass-40 verdict quoted a branching factor of 24 from pairs over the whole
graph and no pruning.  This measures the real tree: pairs inside the Kuratowski
subdivision only, with the Euler bound applied at every node.
"""
import networkx as nx, statistics
G = nx.complete_graph(8)
for a, b in [(0, 1), (2, 3), (4, 5)]:
    G.remove_edge(a, b)

def euler_lb(H):
    n, m = H.number_of_nodes(), H.number_of_edges()
    lb = m - 3*n + 6
    if not any(nx.triangles(H).values()):
        lb = max(lb, m - 2*n + 4)
    return max(0, lb)

def pairs(H):
    ok, K = nx.check_planarity(H, counterexample=True)
    if ok:
        return None
    KE = list(K.edges())
    return [(KE[i], KE[j]) for i in range(len(KE)) for j in range(i+1, len(KE))
            if not set(KE[i]) & set(KE[j])]

def cross(H, e, f, tag):
    J = H.copy(); J.remove_edge(*e); J.remove_edge(*f)
    d = ("x", tag)
    for u in e + f:
        J.add_edge(u, d)
    return J

print(f"root: |E| = {G.number_of_edges()}, Euler lb = {euler_lb(G)}, "
      f"all independent pairs = {sum(1 for i,e in enumerate(G.edges()) for f in list(G.edges())[i+1:] if not set(e)&set(f))}")
level = [G]
prod = 1
for d in range(8):
    bs = []
    nxt = []
    for H in level[:40]:
        p = pairs(H)
        if p is None:
            continue
        bs.append(len(p))
        for e, f in p[:6]:
            nxt.append(cross(H, e, f, (d, len(nxt))))
    if not bs:
        print(f"depth {d}: all planar")
        break
    m = statistics.mean(bs)
    prod *= m
    print(f"depth {d}: branching mean {m:.1f} (min {min(bs)}, max {max(bs)}), "
          f"cumulative tree ~ {prod:.3g}", flush=True)
    level = nxt

"""Refutation sweep: look for a drawing beating DS21's stated exact value."""
import sys, time, networkx as nx
sys.path.insert(0, '/Users/abuzark/.discovery-research-team/workspaces/researcher-4/scratch')
import ubound
from ds21_sweep2 import FORMULAS, multipartite

def Z(m, n):
    return (m//2)*((m-1)//2)*(n//2)*((n-1)//2)

# Instrument revalidated at the head of every batch, per standing practice.
KNOWN = [("K5", nx.complete_graph(5), 1), ("K6", nx.complete_graph(6), 3),
         ("K7", nx.complete_graph(7), 9), ("K8", nx.complete_graph(8), 18),
         ("K4,4", nx.complete_bipartite_graph(4, 4), 4),
         ("K5,5", nx.complete_bipartite_graph(5, 5), 16)]
print("instrument validation (upper bound must equal the known exact value):")
bad = 0
for name, G, val in KNOWN:
    u = ubound.upper(G, restarts=60)
    ok = u == val
    bad += not ok
    print(f"   {name:>6}: known {val:>3}, upper {str(u):>4}  {'OK' if ok else 'FAIL'}")
if bad:
    sys.exit("heuristic failed validation; sweep not run")

print(f"\n{'family':>15} {'n':>3} {'|V|':>4} {'|E|':>4} {'DS21':>6} {'upper':>6}  verdict")
refuted = []
for name, parts, f in FORMULAS:
    for n in range(1, 13):
        G = multipartite(list(parts(n)))
        pred = f(n)
        t = time.time()
        u = ubound.upper(G, restarts=40, seed=n)
        if u is None:
            v = "no drawing found"
        elif u < pred:
            v = f"*** REFUTED: drawing with {u} < {pred} ***"
            refuted.append((name, n, pred, u))
        elif u == pred:
            v = "consistent (tight)"
        else:
            v = f"consistent (upper +{u - pred})"
        print(f"{name:>15} {n:>3} {G.number_of_nodes():>4} {G.number_of_edges():>4} "
              f"{pred:>6} {str(u):>6}  {v}   ({time.time()-t:.1f}s)", flush=True)

print("\n=== refutations ===")
print("none" if not refuted else "\n".join(map(str, refuted)))

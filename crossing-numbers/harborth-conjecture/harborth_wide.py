"""Harborth search: less balanced triples, and k >= 4 parts.

Stopping rule, stated BEFORE the run so the lane has a terminus it did not
choose after seeing the data:

  (a) any drawing below the bound -> publish at once, the conjecture is refuted;
  (b) otherwise the deliverable is the systematic record of where the instrument
      MEETS the bound and where it fails, and the lane stops when the meet-rate
      among open cases falls below 1/2 within a size band -- past that point a
      "meets" is rare enough that the absence of a counterexample is a fact about
      the search rather than about the conjecture;
  (c) or when the region below is covered.
"""
import sys, time, networkx as nx, ubound
from harborth_general import harborth

for nm, G, v in [("K7", nx.complete_graph(7), 9), ("K8", nx.complete_graph(8), 18),
                 ("K5,5", nx.complete_bipartite_graph(5,5), 16)]:
    u = ubound.upper(G, restarts=60)
    print(f"  validate cr({nm}) = {u}, expected {v}  {'OK' if u==v else 'FAIL'}")
    if u != v: sys.exit("instrument failed validation")

def run(title, cases):
    print(f"\n=== {title} ===")
    print(f"{'graph':>20} {'|V|':>4} {'|E|':>4} {'Harborth':>9} {'found':>6}  verdict")
    meets = tot = 0
    for p in cases:
        G = nx.complete_multipartite_graph(*p)
        if G.number_of_nodes() > 15 or G.number_of_edges() > 95:
            continue
        b = int(harborth(p))
        t0 = time.time()
        u = ubound.upper(G, restarts=40, seed=sum(x*7**i for i,x in enumerate(p)))
        tot += 1
        if u is None: v = "no drawing"
        elif u < b:  v = f"*** REFUTES Harborth: {u} < {b} ***"
        elif u == b: v = "meets bound"; meets += 1
        else:        v = f"above by {u-b}"
        print(f"{'K_'+str(p):>20} {G.number_of_nodes():>4} {G.number_of_edges():>4} "
              f"{b:>9} {str(u):>6}  {v}   ({time.time()-t0:.1f}s)", flush=True)
    print(f"-- {title}: meets {meets}/{tot}"
          f"{f' = {meets/tot:.2f}' if tot else ''}")

# Less balanced triples: max part at least three times the min.
tri = [(a,b,c) for a in range(1,7) for b in range(a,10) for c in range(b,15)
       if a+b+c <= 14 and c >= 3*a]   # capped by the stopping rule
run("less balanced triples (max part >= 3x min)", sorted(tri, key=lambda p: sum(p)))

# k = 4, 5, 6 parts.
for k in (4, 5, 6):
    cs = []
    def rec(pref, lo, rem):
        if len(pref) == k:
            if sum(pref) >= k + 2: cs.append(tuple(pref))
            return
        for v in range(lo, rem + 1):
            if sum(pref) + v * (k - len(pref)) <= 15:
                rec(pref + [v], v, rem)
    rec([], 1, 6)
    run(f"k = {k} parts", sorted(cs, key=lambda p: sum(p)))

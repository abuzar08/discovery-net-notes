"""Independent reproduction of the Hill and Zarankiewicz upper bounds.

DS21's footnote 68: "It should be pointed out that verifying the upper bound is a
tedious exercise in counting."  The planarisation heuristic knows nothing about
Hill's or Zarankiewicz's constructions, so if it independently finds drawings
with exactly Z(n) and Z(m,n) crossings, that is a construction-free confirmation
of the upper-bound half of both conjectures at those orders.

It also has teeth in the other direction: a drawing with FEWER than Z(n)
crossings would refute Hill's conjecture outright.
"""
import time, networkx as nx, ubound

def X(n): return (n//2)*((n-1)//2)
def Z1(n): return X(n)*X(n-2)//4          # Hill's number H(n)
def Z2(m,n): return X(m)*X(n)             # Zarankiewicz

print("Hill:  cr(K_n) = Z(n) conjectured; DS21 says proved for n <= 12")
print(f"{'n':>3} {'|E|':>4} {'Z(n)':>6} {'found':>6}  verdict")
for n in range(5, 17):
    G = nx.complete_graph(n)
    t = time.time()
    u = ubound.upper(G, restarts=60, seed=n)
    z = Z1(n)
    v = ("*** REFUTES Hill ***" if u < z else "reproduces Z(n)" if u == z
         else f"above by {u-z}")
    print(f"{n:>3} {G.number_of_edges():>4} {z:>6} {u:>6}  {v}   ({time.time()-t:.1f}s)",
          flush=True)

print("\nZarankiewicz:  cr(K_m,n) = Z(m,n) conjectured")
print(f"{'m,n':>7} {'|E|':>4} {'Z(m,n)':>7} {'found':>6}  verdict")
for m in range(3, 8):
    for n in range(m, 11):
        G = nx.complete_bipartite_graph(m, n)
        u = ubound.upper(G, restarts=50, seed=m*100+n)
        z = Z2(m, n)
        v = ("*** REFUTES Zarankiewicz ***" if u < z else "reproduces Z(m,n)"
             if u == z else f"above by {u-z}")
        print(f"{m},{n:<5} {G.number_of_edges():>4} {z:>7} {u:>6}  {v}", flush=True)

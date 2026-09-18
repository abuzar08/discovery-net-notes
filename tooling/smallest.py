"""Test my own prediction: do DS21's parametric CONJECTURES fail at their
smallest admissible parameter?

An important qualification first, against my own claim. The multipartite
*formula* sweep already evaluated nine proved families at their smallest
parameter (n = 1) and found nothing.  So the claim cannot be about parametric
statements in general.  It can only be about statements RESTATED FROM A SOURCE
as conjectures or open questions -- where a side condition has to survive a
paraphrase.

This enumerates those and evaluates each at its smallest admissible parameter,
computing the value rather than recalling it.
"""
import sys, networkx as nx
sys.path.insert(0, '.')
import ubound

def X(n): return (n//2)*((n-1)//2)
def Z2(m,n): return X(m)*X(n)
def Z1(n): return X(n)*X(n-2)//4
def C2(a): return a*(a-1)//2

for nm,G,v in [("K7",nx.complete_graph(7),9),("K8",nx.complete_graph(8),18)]:
    u=ubound.upper(G,restarts=60)
    assert u==v, f"instrument failed on {nm}"
print("  instrument revalidated on cr(K7)=9, cr(K8)=18\n")

rows=[]

# 1. Harary-Kainen-Schwenk: cr(C_m box C_n) = n(m-2), n >= m >= 3.  Smallest (3,3).
G=nx.cartesian_product(nx.cycle_graph(3),nx.cycle_graph(3))
rows.append(("Harary-Kainen-Schwenk, cr(C_m box C_n)=n(m-2)","(m,n)=(3,3)",
             3*(3-2), ubound.upper(G,restarts=200)))

# 2. Chia-Lee: cr(K_n - e) = Z(n) - C(floor((n-1)/2), 2).  Smallest non-trivial n=5.
G=nx.complete_graph(5); G.remove_edge(0,1)
rows.append(("Chia-Lee, cr(K_n - e)","n=5", Z1(5)-C2((5-1)//2), ubound.upper(G,restarts=200)))

# 3. Chia-Lee: cr(K_{m,n} - e) = Z(m,n) - floor((m-1)/2)floor((n-1)/2).  Smallest (3,3).
G=nx.complete_bipartite_graph(3,3); G.remove_edge(0,3)
rows.append(("Chia-Lee, cr(K_{m,n} - e)","(m,n)=(3,3)",
             Z2(3,3)-((3-1)//2)*((3-1)//2), ubound.upper(G,restarts=200)))

# 4. Harborth: cr(K_{n1..nk}) = Harborth's function.  Smallest tripartite (1,1,1).
from harborth import A
G=nx.complete_multipartite_graph(1,1,1)
rows.append(("Harborth, cr(K_{n1,n2,n3}) = A","(1,1,1)", A(1,1,1), ubound.upper(G,restarts=60)))

# 5. Zarankiewicz: cr(K_{m,n}) = Z(m,n).  Smallest non-trivial (3,3).
rows.append(("Zarankiewicz, cr(K_{m,n}) = Z(m,n)","(m,n)=(3,3)",
             Z2(3,3), ubound.upper(nx.complete_bipartite_graph(3,3),restarts=60)))

# 6. Hill: cr(K_n) = Z(n).  Smallest non-trivial n=5.
rows.append(("Hill, cr(K_n) = Z(n)","n=5", Z1(5), ubound.upper(nx.complete_graph(5),restarts=60)))

print(f"{'conjecture':>46} {'smallest':>12} {'stated':>7} {'actual':>7}  verdict")
agree=fail=0
for name,at,pred,act in rows:
    ok = (act == pred)
    agree += ok; fail += not ok
    print(f"{name:>46} {at:>12} {pred:>7} {act:>7}  {'agrees' if ok else '*** FAILS ***'}")
print(f"\ncomputed here: {agree} agree, {fail} fail at the smallest parameter")

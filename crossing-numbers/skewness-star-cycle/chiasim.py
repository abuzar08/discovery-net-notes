"""Chia and Sim's open question on the skewness of K_{1,m} box C_n.

DS21, Ninth Edition, skewness entry, open questions, verbatim at page fidelity:

  "Chia and Sim [209] ask whether sk(K_{1,m} box C_n) = (m-2)(floor((n-1)/2) + 1)?"

Reference [209] is Chia and Sim, On the skewness of products of graphs, Discrete
Appl. Math. 342 (2024), 295-303.  The question is open.

K_{1,m} is the star with m leaves.  The Cartesian product with C_n has (m+1)n
vertices and (2m+1)n edges.
"""
import sys, itertools, networkx as nx

def star_box_cycle(m, n):
    return nx.cartesian_product(nx.star_graph(m), nx.cycle_graph(n))

def pred(m, n):
    return (m - 2) * ((n - 1) // 2 + 1)

def planar(G):
    return nx.check_planarity(G, counterexample=False)[0]

def skew_exact(G, hi):
    E = list(G.edges())
    for r in range(hi + 1):
        for S in itertools.combinations(E, r):
            H = G.copy(); H.remove_edges_from(S)
            if planar(H):
                return r, S
    return None, None

if __name__ == "__main__":
    from math import comb
    print("structure and the gate, before any real compute:")
    print(f"{'m':>2} {'n':>2} {'|V|':>4} {'|E|':>4} {'predicted sk':>13} {'C(|E|,sk)':>13}  planar?")
    for m in (2, 3, 4, 5):
        for n in (3, 4, 5, 6):
            G = star_box_cycle(m, n)
            p = pred(m, n)
            print(f"{m:>2} {n:>2} {G.number_of_nodes():>4} {G.number_of_edges():>4} "
                  f"{p:>13} {comb(G.number_of_edges(), p):>13,}  {planar(G)}")
    print()
    print("free validation: m = 2 predicts sk = 0, i.e. K_(1,2) box C_n planar.")
    print("K_(1,2) is the path on three vertices, so this is the planar prism-like")
    print("product -- if the graphs above at m = 2 are not planar, either my")
    print("construction or my reading of the formula is wrong, and nothing else")
    print("in this lane would be worth running.")

def run(cases):
    print(f"\n{'m':>2} {'n':>2} {'|V|':>4} {'|E|':>4} {'predicted':>9} {'actual sk':>9}  verdict")
    for m, n in cases:
        G = star_box_cycle(m, n)
        p = pred(m, n)
        r, S = skew_exact(G, p + 2)
        v = ("AGREES" if r == p else
             f"*** DISAGREES: {r} vs predicted {p} ***" if r is not None else "not decided")
        print(f"{m:>2} {n:>2} {G.number_of_nodes():>4} {G.number_of_edges():>4} "
              f"{p:>9} {str(r):>9}  {v}", flush=True)

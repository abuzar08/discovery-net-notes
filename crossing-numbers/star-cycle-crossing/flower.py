"""Clancy's I_n (Flower Snark) and its stated crossing number.

Clancy, Haythorpe, Newcombe, Theorem 2.50 (Zheng et al., 2008): for n >= 3,
    cr(I_n) = n-1 for 3 <= n <= 5, and n for n >= 6.

Definition, verbatim from the survey: I_n on 4n vertices is produced by taking n
copies of K_{1,3}; in copy i the three degree-1 vertices are a_i, b_i, c_i.  The
copies are joined via a cycle a_1,...,a_n,a_1 and a cycle
b_1,...,b_n,c_1,...,c_n,b_1.

Smallest admissible parameter is n = 3, where the claim is cr(I_3) = 2.
"""
import sys, networkx as nx

def I(n):
    G = nx.Graph()
    for i in range(n):
        for x in 'abc':
            G.add_edge(('d', i), (x, i))            # the K_{1,3} copy
    for i in range(n):
        G.add_edge(('a', i), ('a', (i+1) % n))      # cycle on the a_i
    ring = [('b', i) for i in range(n)] + [('c', i) for i in range(n)]
    for i in range(len(ring)):
        G.add_edge(ring[i], ring[(i+1) % len(ring)])
    return G

if __name__ == "__main__":
    print(f"{'n':>2} {'|V|':>4} {'|E|':>4} {'cubic':>6} {'stated':>7}")
    for n in range(3, 8):
        G = I(n)
        degs = {d for _, d in G.degree()}
        stated = n-1 if n <= 5 else n
        print(f"{n:>2} {G.number_of_nodes():>4} {G.number_of_edges():>4} "
              f"{str(degs == {3}):>6} {stated:>7}")
    # sanity: I_5 is the classic Flower Snark J_5, which is the Petersen graph
    # with each vertex... no -- J_5 is a known snark on 20 vertices.  Check the
    # standard invariants instead: cubic, girth, non-planar.
    G5 = I(5)
    print(f"\nI_5: |V|={G5.number_of_nodes()} |E|={G5.number_of_edges()} "
          f"girth={nx.girth(G5) if hasattr(nx,'girth') else 'n/a'} "
          f"planar={nx.check_planarity(G5, counterexample=False)[0]}")

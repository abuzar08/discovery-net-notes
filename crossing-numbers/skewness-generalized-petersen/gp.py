"""Chia and Lee's skewness conjecture for generalized Petersen graphs.

DS21, Ninth Edition, open questions of the skewness entry:

  "Chia and Lee [207] conjectured that sk(GP(4k,k)) = k+2 for odd k >= 3 ...
   The conjecture was mostly settled in [208], but cases k = 5 and k = 7
   remain open."

So the open instances are GP(20,5) with conjectured skewness 7, and GP(28,7)
with conjectured skewness 9.

GP(n,k): outer cycle u_0..u_{n-1}, inner vertices v_0..v_{n-1}, edges
u_i u_{i+1}, u_i v_i, and v_i v_{i+k}, all indices mod n.  Cubic on 2n vertices
with 3n edges.
"""
import sys, itertools, networkx as nx

def GP(n, k):
    G = nx.Graph()
    for i in range(n):
        G.add_edge(('u', i), ('u', (i+1) % n))
        G.add_edge(('u', i), ('v', i))
        G.add_edge(('v', i), ('v', (i+k) % n))
    return G

def planar(G):
    return nx.check_planarity(G, counterexample=False)[0]

def skew_exact(G, lo=0, hi=12, verbose=False):
    """Smallest r with an r-edge set whose deletion planarises G."""
    E = list(G.edges())
    for r in range(lo, hi+1):
        n = 0
        for S in itertools.combinations(E, r):
            H = G.copy(); H.remove_edges_from(S)
            n += 1
            if planar(H):
                if verbose: print(f"    r={r}: planar after removing {S}", flush=True)
                return r, S
        if verbose: print(f"    r={r}: none of {n} sets planarises", flush=True)
    return None, None

if __name__ == "__main__":
    print("structure check:")
    for n, k in [(12,3),(20,5),(28,7)]:
        G = GP(n, k)
        degs = {d for _, d in G.degree()}
        print(f"  GP({n},{k}): |V|={G.number_of_nodes()} |E|={G.number_of_edges()} "
              f"degrees={degs} planar={planar(G)}  conjectured sk={k+2}")
    print("\nvalidation on the settled case GP(12,3), conjectured and known sk = 5:")
    r, S = skew_exact(GP(12,3), 0, 6, verbose=True)
    print(f"  sk(GP(12,3)) = {r}  {'OK' if r == 5 else 'MISMATCH vs conjectured 5'}")

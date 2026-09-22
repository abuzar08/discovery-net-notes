"""GATE, stated before any target is chosen.

My instrument set decides cr(G) exactly when BOTH hold:
  (1) cr(G) - sk(G) <= 1   -- the transversal test is complete only at k = sk,
                              so it can certify cr >= sk+1 and no more;
  (2) sk(G) is small and |E| modest -- the planarising-set family P is
      C(|E|, <=sk), and the pass-82 measurement showed the search dies as P grows.

The heuristic upper bound only ever overestimates, so `ub - sk` is an UPPER
estimate of the true gap: ub - sk <= 1 implies the cell is reachable.  The gate
is therefore sound in the direction I need.
"""
import sys, itertools, time, networkx as nx
sys.path.insert(0, 'scratch')
import ubound

def sk(G, hi=6):
    E = list(G.edges())
    for k in range(hi):
        for S in itertools.combinations(range(len(E)), k):
            H = G.copy(); H.remove_edges_from([E[i] for i in S])
            if nx.check_planarity(H)[0]:
                return k
    return None                      # sk >= hi, too expensive for the gate

def GP(n, k):
    G = nx.Graph()
    for i in range(n):
        G.add_edge(('u', i), ('u', (i+1) % n))
        G.add_edge(('u', i), ('v', i))
        G.add_edge(('v', i), ('v', (i+k) % n))
    return G

print('GATE SCAN: generalized Petersen graphs GP(n,k)', flush=True)
print(f"{'n':>3} {'k':>2} {'|V|':>4} {'|E|':>4} {'sk':>4} {'ub':>4} {'gap':>4}  reachable?", flush=True)
for n in range(5, 15):
    for k in range(2, n//2 + 1):
        if n == 2*k:            # GP(n,n/2) is a multigraph in the inner ring
            continue
        G = GP(n, k)
        if nx.check_planarity(G)[0]:
            continue            # cr = 0, nothing to decide
        s = sk(G)
        if s is None:
            print(f'{n:3} {k:2} {G.number_of_nodes():4} {G.number_of_edges():4} {">=6":>4} {"-":>4} {"-":>4}  no (sk too large for gate)', flush=True)
            continue
        ub = ubound.upper(G, restarts=120, seed=1)
        gap = ub - s
        print(f'{n:3} {k:2} {G.number_of_nodes():4} {G.number_of_edges():4} {s:4} {ub:4} {gap:4}  ' +
              ('YES' if gap <= 1 else 'no'), flush=True)
print('DONE', flush=True)

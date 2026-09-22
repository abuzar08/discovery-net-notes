"""Independently certify Clancy Table 2 on exactly the cells the gate admits."""
import sys, itertools, time, networkx as nx
sys.path.insert(0, 'scratch')
import ubound
from transversal import cr_le_exact, IncompleteRange

def GP(n, k):
    G = nx.Graph()
    for i in range(n):
        G.add_edge(('u', i), ('u', (i+1) % n))
        G.add_edge(('u', i), ('v', i))
        G.add_edge(('v', i), ('v', (i+k) % n))
    return G

def sk(G, hi=7):
    E = list(G.edges())
    for k in range(hi):
        for S in itertools.combinations(range(len(E)), k):
            H = G.copy(); H.remove_edges_from([E[i] for i in S])
            if nx.check_planarity(H)[0]:
                return k

# (n, k, Clancy Table 2 value) -- only cells the gate passed (ub - sk <= 1)
CELLS = [(5,2,2),(7,2,3),(7,3,3),(8,3,4),(9,2,3),(9,3,2),(9,4,3),(10,4,4),
         (11,2,3),(11,3,5),(11,4,5),(11,5,3),(12,3,4),(12,4,4),(13,2,3),
         (13,6,3),(14,3,6)]

print(f"{'GP(n,k)':>10} {'|E|':>4} {'sk':>3} {'ub':>3} {'Clancy':>7} {'certified':>10}  verdict", flush=True)
results = []
for n, k, pub in CELLS:
    G = GP(n, k); E = G.number_of_edges()
    s = sk(G); ub = ubound.upper(G, restarts=200, seed=1)
    cert = None
    if s == ub:
        cert = s                                    # skewness meets a drawing
        how = 'sk meets'
    elif ub == s + 1:
        try:
            d, _, _ = cr_le_exact(G, s)
            if not d:
                cert = s + 1; how = 'transversal +1'
            else:
                cert = s; how = 'transversal: cr = sk'
        except IncompleteRange:
            how = 'refused'
    else:
        how = 'gate should have excluded'
    ok = 'agrees' if cert == pub else ('*** DISAGREES ***' if cert is not None else 'undecided')
    print(f'{("GP(%d,%d)"%(n,k)):>10} {E:4} {s:3} {ub:3} {pub:7} {str(cert):>10}  {ok} ({how})', flush=True)
    results.append((n, k, pub, cert))

print('\nIsomorphism classes among the certified cells:', flush=True)
graphs = [(n, k, GP(n, k)) for n, k, _, c in results if c is not None]
seen = []
for n, k, G in graphs:
    hit = next((f'GP({a},{b})' for a, b, H in seen if nx.is_isomorphic(G, H)), None)
    if hit:
        print(f'  GP({n},{k}) == {hit}', flush=True)
    else:
        seen.append((n, k, G))
print(f'  distinct classes: {len(seen)} of {len(graphs)} certified cells', flush=True)
print('DONE', flush=True)

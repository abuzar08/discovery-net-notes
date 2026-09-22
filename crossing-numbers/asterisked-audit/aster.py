"""Audit of Clancy's ASTERISKED results -- those the survey marks as appearing in
journals with no or inadequate peer review, and explicitly says 'cannot be relied
upon' and 'should be revisited'."""
import sys, itertools, networkx as nx
sys.path.insert(0, 'scratch')
import ubound
X = lambda n: (n//2)*((n-1)//2)

def sk(G, hi=8):
    E = list(G.edges())
    for k in range(hi):
        for S in itertools.combinations(range(len(E)), k):
            H = G.copy(); H.remove_edges_from([E[i] for i in S])
            if nx.check_planarity(H)[0]:
                return k
    return None

def Ci(n, S):
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i in range(n):
        for s in S:
            G.add_edge(i, (i+s) % n)
    return G

print('THEOREM 2.26 (Yang and Zhao, 2001)*:  cr(Ci_n({1, floor(n/2)})) = 1 for n >= 6.', flush=True)
print('  cr = 1 forces sk = 1.  Even n is the Moebius ladder (Guy-Harary, cr=1);', flush=True)
print('  the ODD cases are the asterisked content.', flush=True)
print(f"  {'n':>3} {'|V|':>4} {'|E|':>4} {'deg':>5} {'sk':>3} {'claimed cr':>11}  verdict", flush=True)
for n in range(6, 20):
    G = Ci(n, [1, n//2])
    degs = sorted({d for _, d in G.degree()})
    s = sk(G, hi=6)
    v = 'consistent' if s == 1 else ('planar, cr=0 CONTRADICTS cr=1' if s == 0
         else f'sk={s} > 1 so cr >= {s}: *** REFUTES cr = 1 ***')
    print(f'  {n:3} {G.number_of_nodes():4} {G.number_of_edges():4} {str(degs):>5} {str(s):>3} {1:11}  {v}', flush=True)
print('DONE', flush=True)

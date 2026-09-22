import sys, itertools, networkx as nx
sys.path.insert(0, 'scratch')
import ubound
from transversal import cr_le_exact, IncompleteRange
X = lambda n: (n//2)*((n-1)//2)
def sk(G, hi=8):
    E=list(G.edges())
    for k in range(hi):
        for S in itertools.combinations(range(len(E)),k):
            H=G.copy(); H.remove_edges_from([E[i] for i in S])
            if nx.check_planarity(H)[0]: return k
def Ci(n,S):
    G=nx.Graph(); G.add_nodes_from(range(n))
    for i in range(n):
        for s in S: G.add_edge(i,(i+s)%n)
    return G

print('THM 2.26* cr(Ci_n({1,floor(n/2)})) = 1, n >= 6 -- EXACT decision at k = sk = 1', flush=True)
allok=True
for n in range(6,20):
    G=Ci(n,[1,n//2]); d,_,_=cr_le_exact(G,1)
    ok = d   # cr <= 1 and cr >= sk = 1  =>  cr = 1
    allok &= ok
    print(f'  n={n:3} |E|={G.number_of_edges():3}  cr<=1? {str(d):5} -> cr = {1 if d else ">1"}  '
          + ('confirms' if ok else '*** REFUTES ***'), flush=True)
print(f'  VERDICT: {"confirmed at all 14 values" if allok else "REFUTED"}', flush=True)

print('\nTHM 2.33* m <= cr(Ci_{3m-1}({1,m})) <= m+1, m >= 3  [smallest m = 3: Ci_8({1,3})]', flush=True)
G=Ci(8,[1,3]); s=sk(G); ub=ubound.upper(G,restarts=300,seed=1)
print(f'  Ci_8({{1,3}}): V={G.number_of_nodes()} E={G.number_of_edges()} sk={s} ub={ub}  claimed 3 <= cr <= 4', flush=True)
try:
    d,_,_=cr_le_exact(G,s)
    print(f'  cr<={s}? {d}  -> cr {"=" if d else ">="} {s if d else s+1}', flush=True)
except IncompleteRange as e:
    print('  refused', flush=True)

print('\nTHM 2.10* cr(K_{1,2,2,n}) = 4*X(n) + n + floor(n/2)  [smallest n = 1]', flush=True)
for n in (1,2):
    G=nx.complete_multipartite_graph(1,2,2,n)
    claim=4*X(n)+n+n//2
    s=sk(G); ub=ubound.upper(G,restarts=300,seed=1)
    print(f'  n={n}: V={G.number_of_nodes()} E={G.number_of_edges()} sk={s} ub={ub} claimed={claim}', flush=True)
    if ub<claim: print('    *** drawing below the claim: REFUTES ***', flush=True)
    elif s>claim: print('    *** sk exceeds the claim: REFUTES ***', flush=True)
    else:
        try:
            d,_,_=cr_le_exact(G,s)
            cert = s if d else None
            print(f'    cr<=sk? {d} -> ' + (f'cr = {s}, ' + ('agrees' if s==claim else '*** DISAGREES ***') if d else f'cr >= {s+1}'), flush=True)
        except IncompleteRange: print('    refused', flush=True)
print('DONE', flush=True)

import sys, itertools, networkx as nx
sys.path.insert(0,'scratch')
import ubound
from transversal import cr_le_exact, IncompleteRange
X=lambda n:(n//2)*((n-1)//2)
def sk(G,hi=8):
    E=list(G.edges())
    for k in range(hi):
        for S in itertools.combinations(range(len(E)),k):
            H=G.copy(); H.remove_edges_from([E[i] for i in S])
            if nx.check_planarity(H)[0]: return k
def decide(name,G,claim):
    s=sk(G); ub=ubound.upper(G,restarts=300,seed=1)
    if s is None:
        print(f'  {name}: sk too large for gate (V={G.number_of_nodes()} E={G.number_of_edges()}) claimed={claim}', flush=True); return
    line=f'  {name}: V={G.number_of_nodes()} E={G.number_of_edges()} sk={s} ub={ub} claimed={claim}'
    if ub<claim: print(line+'  *** DRAWING BELOW CLAIM: REFUTES ***', flush=True); return
    if s>claim:  print(line+'  *** sk EXCEEDS CLAIM: REFUTES ***', flush=True); return
    if s==ub:
        print(line+f'  -> cr = {s} exactly, ' + ('agrees' if s==claim else '*** DISAGREES ***'), flush=True); return
    if ub==s+1:
        try:
            d,_,_=cr_le_exact(G,s); c = s if d else s+1
            print(line+f'  -> cr = {c} exactly, ' + ('agrees' if c==claim else '*** DISAGREES ***'), flush=True); return
        except IncompleteRange: pass
    print(line+f'  -> {s} <= cr <= {ub}, gap {ub-s}: undecided (claim inside range: {s<=claim<=ub})', flush=True)

print('THM 2.9* cr(K_{1,1,m,n}) = cr(K_{m+2,n+2}) + X-term - mn', flush=True)
for m,n in [(2,3),(3,3)]:
    claim = X(m+2)*X(n+2) + (m//2)*(n//2) - m*n
    decide(f'K_1,1,{m},{n}', nx.complete_multipartite_graph(1,1,m,n), claim)
print('THM 2.14* cr(K_{3,n} - e) = X(n) - floor((n-1)/2)', flush=True)
for n in (4,5,6,7):
    G=nx.complete_bipartite_graph(3,n); e=list(G.edges())[0]; G.remove_edge(*e)
    decide(f'K_3,{n} - e', G, X(n)-((n-1)//2))
print('THM 3.15* cr(P_n box Ci_7(1,2)) = 8n  and  THM 3.17* cr(P_n box Ci_8(1,4)) = 9n-1, at n=1', flush=True)
def Ci(n,S):
    G=nx.Graph(); G.add_nodes_from(range(n))
    for i in range(n):
        for s in S: G.add_edge(i,(i+s)%n)
    return G
for lbl,C,claim in [('P_1 x Ci_7(1,2)',Ci(7,[1,2]),8), ('P_1 x Ci_8(1,4)',Ci(8,[1,4]),8)]:
    G=nx.cartesian_product(nx.path_graph(2), C)
    ubv=ubound.upper(G,restarts=300,seed=1)
    print(f'  {lbl}: V={G.number_of_nodes()} E={G.number_of_edges()} ub={ubv} claimed={claim}  '
          + ('*** DRAWING BELOW CLAIM: REFUTES ***' if ubv<claim else 'no refutation (ub >= claim)'), flush=True)
print('DONE', flush=True)

import sys, itertools, networkx as nx
sys.path.insert(0,'scratch')
import ubound
from transversal import cr_le_exact, IncompleteRange
X=lambda n:(n//2)*((n-1)//2)
def sk(G,hi=9):
    E=list(G.edges())
    for k in range(hi):
        for S in itertools.combinations(range(len(E)),k):
            H=G.copy(); H.remove_edges_from([E[i] for i in S])
            if nx.check_planarity(H)[0]: return k
def decide(name,G,claim):
    s=sk(G)
    ub=ubound.upper(G,restarts=250,seed=1)
    tag=f'  {name}: V={G.number_of_nodes():2} E={G.number_of_edges():3} claim={claim:3} sk={str(s):>4} ub={ub:3} V-sk={str(claim-s) if s is not None else "?":>3}'
    if s is not None and s>claim: print(tag+'  *** sk EXCEEDS CLAIM: REFUTES ***',flush=True); return
    if ub<claim: print(tag+'  *** DRAWING BELOW CLAIM: REFUTES ***',flush=True); return
    if s is None: print(tag+'  sk beyond gate; ub >= claim, no refutation',flush=True); return
    if s==ub: print(tag+f'  -> cr={s} exactly, '+('agrees' if s==claim else '*** DISAGREES ***'),flush=True); return
    if ub==s+1:
        try:
            d,_,_=cr_le_exact(G,s); c=s if d else s+1
            print(tag+f'  -> cr={c} exactly, '+('agrees' if c==claim else '*** DISAGREES ***'),flush=True); return
        except IncompleteRange: pass
    print(tag+f'  -> {s}<=cr<={ub}; claim inside: {s<=claim<=ub}',flush=True)

print('THM 2.14* part 2: cr(K_{4,n} - e) = 2X(n) - floor((n-1)/2)',flush=True)
for n in (3,4,5,6):
    G=nx.complete_bipartite_graph(4,n); G.remove_edge(*list(G.edges())[0])
    decide(f'K_4,{n}-e', G, 2*X(n)-((n-1)//2))

print('THM 4.2* (Li 2014), G = C_4 u K_1',flush=True)
def Gbase():
    H=nx.cycle_graph(4); H.add_node('iso'); return H
def join(H, other_nodes, other_edges):
    J=nx.Graph(H)
    J.add_nodes_from(other_nodes); J.add_edges_from(other_edges)
    for u in H.nodes():
        for v in other_nodes: J.add_edge(u,v)
    return J
for n in (1,2,3,4):
    nodes=[('d',i) for i in range(n)]
    decide(f'(C4 u K1) + D_{n}', join(Gbase(),nodes,[]), 4*X(n)+n//2)
for n in (2,3,4):
    nodes=[('p',i) for i in range(n)]
    edges=[(('p',i),('p',i+1)) for i in range(n-1)]      # path on n vertices = P_{n-1}
    decide(f'(C4 u K1) + P_{n-1} [n={n} vtcs]', join(Gbase(),nodes,edges), 4*X(n)+n//2+1)
for n in (3,4):
    nodes=[('c',i) for i in range(n)]
    edges=[(('c',i),('c',(i+1)%n)) for i in range(n)]
    decide(f'(C4 u K1) + C_{n}', join(Gbase(),nodes,edges), 4*X(n)+n//2+2)
print('DONE',flush=True)

import sys, itertools, networkx as nx
sys.path.insert(0, 'scratch')
import ubound
from transversal import cr_le_exact, IncompleteRange
def GP(n,k):
    G=nx.Graph()
    for i in range(n):
        G.add_edge(('u',i),('u',(i+1)%n)); G.add_edge(('u',i),('v',i))
        G.add_edge(('v',i),('v',(i+k)%n))
    return G
def sk(G,hi=7):
    E=list(G.edges())
    for k in range(hi):
        for S in itertools.combinations(range(len(E)),k):
            H=G.copy(); H.remove_edges_from([E[i] for i in S])
            if nx.check_planarity(H)[0]: return k
# remaining cells that are NOT isomorphic to one already certified
for n,k,pub in [(12,3,4),(12,4,4),(13,2,3)]:
    G=GP(n,k); s=sk(G); ub=ubound.upper(G,restarts=200,seed=1)
    if s==ub: cert,how=s,'sk meets'
    elif ub==s+1:
        try:
            d,_,_=cr_le_exact(G,s); cert,how=((s,'transversal: cr = sk') if d else (s+1,'transversal +1'))
        except IncompleteRange: cert,how=None,'refused'
    else: cert,how=None,'gap>1'
    print(f'GP({n},{k}): |E|={G.number_of_edges()} sk={s} ub={ub} Clancy={pub} certified={cert}  '
          + ('agrees' if cert==pub else '*** DISAGREES ***') + f' ({how})', flush=True)
print('--- isomorphism classes among all certified ---', flush=True)
done=[(5,2),(7,2),(7,3),(8,3),(9,2),(9,3),(9,4),(10,4),(11,2),(11,3),(12,3),(12,4),(13,2)]
seen=[]
for n,k in done:
    G=GP(n,k)
    hit=next((f'GP({a},{b})' for a,b,H in seen if nx.is_isomorphic(G,H)), None)
    if hit: print(f'  GP({n},{k}) == {hit}', flush=True)
    else: seen.append((n,k,G))
print(f'  distinct classes: {len(seen)} of {len(done)}', flush=True)
print('DONE', flush=True)

"""reviewer-1: independent census of 2-crossing-critical graphs (own logic,
networkx planarity; reads graph6 from stdin, e.g. from geng)."""
import sys, itertools
import networkx as nx

def g6(line):
    b=[ord(c)-63 for c in line.strip()]; n=b[0]; bits=[]
    for x in b[1:]: bits.extend((x>>s)&1 for s in range(5,-1,-1))
    E=[]; i=0
    for v in range(1,n):
        for u in range(v):
            if bits[i]: E.append((u,v))
            i+=1
    return n,E

def planar(n,E):
    G=nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(E)
    return nx.check_planarity(G)[0]

def indep(e,f): return not(set(e)&set(f))

def crossings_planarization(n,E,chosen):
    """planarizations for a given multiset of crossing pairs (all orders)"""
    per={}
    for e,f in chosen:
        per.setdefault(e,[]).append(f); per.setdefault(f,[]).append(e)
    multi=[e for e in per if len(per[e])>1]
    dummy={c:n+i for i,c in enumerate(chosen)}
    for ords in itertools.product(*[itertools.permutations(per[e]) for e in multi]):
        om=dict(zip(multi,ords)); new=[]
        for e in E:
            if e not in per: new.append(e); continue
            chain=[e[0]]+[dummy[(e,f)] if (e,f) in dummy else dummy[(f,e)] for f in om.get(e,per[e])]+[e[1]]
            new+=list(zip(chain,chain[1:]))
        yield n+len(chosen), new

def cr_le(n,E,k):
    pairs=[(e,f) for e,f in itertools.combinations(E,2) if indep(e,f)]
    for j in range(k+1):
        for chosen in itertools.combinations(pairs,j):
            for nn,ee in crossings_planarization(n,E,chosen):
                if planar(nn,ee): return True
    return False

cnt=0; crit=[]
for line in sys.stdin:
    if not line.strip(): continue
    n,E=g6(line); cnt+=1
    if planar(n,E): continue
    if not all(cr_le(n,[f for f in E if f!=e],1) for e in E): continue
    if cr_le(n,E,1): continue
    tag='CRIT2' if cr_le(n,E,2) else 'CRIT_GE3'
    crit.append((tag,n,len(E),E)); print(tag,n,len(E),','.join(f'{u}-{v}' for u,v in E),flush=True)
print(f'# {cnt} graphs read, {len(crit)} 2-crossing-critical', file=sys.stderr)

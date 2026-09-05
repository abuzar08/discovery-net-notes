"""reviewer-1: independent crossing-number computation for C3 [] C3 and G - e
via exhaustive planarization enumeration and networkx planarity (a planarity
implementation independent of both nauty and the certificate checker)."""
import itertools, sys
import networkx as nx

def c3c3():
    E=set()
    for i in range(3):
        for j in range(3):
            u=3*i+j
            E.add(tuple(sorted((u,3*((i+1)%3)+j)))); E.add(tuple(sorted((u,3*i+(j+1)%3))))
    return sorted(E)

def planar(n, edges):
    G=nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(edges)
    return nx.check_planarity(G)[0]

def indep(e,f): return not(set(e)&set(f))

def planarizations(n, edges, k):
    """yield all planarizations of good drawings with exactly k crossings, k<=3 (generic, by
    choosing k crossing pairs and, for edges crossed several times, all orders)."""
    pairs=[(e,f) for e,f in itertools.combinations(edges,2) if indep(e,f)]
    for chosen in itertools.combinations(pairs,k):
        # crossings along each edge: list of partner edges; try all orders
        per={}
        for e,f in chosen:
            per.setdefault(e,[]).append(f); per.setdefault(f,[]).append(e)
        multi=[e for e in per if len(per[e])>1]
        orders=[list(itertools.permutations(per[e])) for e in multi]
        for ords in itertools.product(*orders):
            ordmap=dict(zip(multi,ords))
            # assign a dummy vertex to each crossing
            dummy={c:n+i for i,c in enumerate(chosen)}
            new=[]
            for e in edges:
                if e not in per: new.append(e); continue
                seq=ordmap.get(e, per[e])
                chain=[e[0]]+[dummy[c] for c in chosen for _ in [0] if False]  # placeholder
                chain=[e[0]]
                for f in seq:
                    c=(e,f) if (e,f) in dummy else (f,e)
                    chain.append(dummy[c])
                chain.append(e[1])
                new+=list(zip(chain,chain[1:]))
            yield n+k, new

def cr(n, edges, maxk=3):
    for k in range(maxk+1):
        cnt=0
        for nn,ee in planarizations(n,edges,k):
            cnt+=1
            if planar(nn,ee): return k, cnt
        print(f"  k={k}: {cnt} planarizations, none planar", flush=True)
    return None, None

E=c3c3(); n=9
k,cnt=cr(n,E)
print("cr(C3 [] C3) =",k, "(planar planarization found after",cnt,"tests at that k)")
for e in E:
    rest=[f for f in E if f!=e]
    k,_=cr(n,rest,2)
    print(f"cr(G - {e}) = {k}")

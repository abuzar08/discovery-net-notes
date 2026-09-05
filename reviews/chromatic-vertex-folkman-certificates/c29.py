import sys, time
from indep_upper import has_clique, colourable, sat_colourable
from indep_circ import circ
n=29; S=(1,2,4,5,10,12)
A=circ(n,S)
E=[(u,v) for u in range(n) for v in range(u+1,n) if A[u]>>v&1]
print("edges",len(E))
print("K4-free:", not has_clique(n,A,4))
t=time.time(); ok,_=colourable(n,A,6); print("own DSATUR 6-colourable:",ok,f"[{time.time()-t:.0f}s]")
t=time.time(); print("SAT 6-colourable:",sat_colourable(n,E,6),f"[{time.time()-t:.0f}s]")
ok,col=colourable(n,A,7); print("7-colourable:",ok, "proper:", all(col[u]!=col[v] for u,v in E))
with open("c29_witness.txt","w") as f:
    f.write(f"{n}\n"); f.writelines(f"{u} {v}\n" for u,v in E)

import itertools, time
from indep_upper import has_clique, colourable
from indep_circ import circ
n=29; h=14; found=[]
t=time.time()
for r in range(1,h+1):
    for S in itertools.combinations(range(1,h+1), r):
        A=circ(n,S)
        if has_clique(n,A,4): continue
        ok,_=colourable(n,A,6)
        if not ok: found.append(S)
print("n=29 K4-free circulants with chi>=7 (own DSATUR only):", len(found), f"[{time.time()-t:.0f}s]")
def canon(S):
    best=None
    for a in range(1,n):
        T=tuple(sorted(min(a*s%n, n-a*s%n) for s in S))
        if best is None or T<best: best=T
    return best
for S in found: print(" ", S, "multiplier-canonical:", canon(S))
print("multiplier classes:", len({canon(S) for S in found}))

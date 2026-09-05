from indep_upper import load, adj_masks, colourable, sat_colourable, has_clique
n,E=load("c29_witness.txt"); A=adj_masks(n,E)
E2=[(a,b) for a,b in E if 0 not in (a,b)]
A2=adj_masks(n,E2)
ok,_=colourable(n,A2,6)
print("G - v 6-colourable (own):", ok, " (sat):", sat_colourable(n,E2,6))
# alpha
comp=[((1<<n)-1)^A[v]^(1<<v) for v in range(n)]
a=0
while has_clique(n,comp,a+1): a+=1
print("alpha(G) =", a, " degree =", bin(A[0]).count('1'))

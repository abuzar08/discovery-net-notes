import sys
LANE='/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/notes/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy'
MINE='/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/notes/reviews/albertson-crminus-repair'
sys.path.insert(0,LANE); sys.path.insert(0,MINE)
import indep_g as IG, order2r as O
crK, g = IG.make({13:225,14:315})
m=838; eH=58*57//2-m; X=2*m-58*28
print('e(H)=',eH,'X=',X)
for YA in (25,47,48,49,52):
    A,R=26,32; P=0
    eHR = eH + P - A*29 + YA
    f=eHR
    eGAR = A*R - (29*A - YA - 2*P)
    dens = (R*(R-1)//2 - f)/(R*(R-1)//2)
    print(f'  Y_A={YA}: e(H[R])={f}, e_G(A,R)={eGAR}, density={dens:.3f}, '
          f'my g(32,{f})={g(32,f)}, cr(K26)+g={crK(26)+g(32,f)}, sampling={O.L(32,496-f)}')
print('cr(K24)',crK(24),'cr(K25)',crK(25),'cr(K26)',crK(26),'cr(K27)',crK(27))

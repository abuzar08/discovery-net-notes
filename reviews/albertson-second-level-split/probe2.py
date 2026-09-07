import sys
LANE='/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/notes/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy'
MINE='/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/notes/reviews/albertson-crminus-repair'
sys.path.insert(0,LANE); sys.path.insert(0,MINE)
import order2r as O, indep_g as IG
crK,g = IG.make({13:225,14:315})
print('s=0 family: A on 49 vertices with P up to 594')
print('   L(49,582) =', O.L(49,582), ' (the table reports 3783)')
for P in (594,):
    eH=815; A=49; YA=48
    eHR = eH + P - A*29 + YA
    print(f'   check identity: P={P}, Y_A={YA} -> e(H[R])={eHR}, cap C(9,2)=36')
print()
print('s=22 family: |A|=27, |R|=31')
eH=815
for P in (3,):
    for YA in range(0,53):
        eHR = eH + P - 27*29 + YA
        if 0 <= eHR <= 31*30//2:
            excess = 52-YA; low=31-excess; blk=max(0,low-4)
            dense = crK(26)+g(31,eHR); gal = crK(26)+crK(blk)
            b=max(dense,gal)
            if YA in (44,45,46,47,48) or b==7354:
                print(f'   P={P} Y_A={YA}: e(H[R])={eHR}, dense={dense}, gallai={gal}, bound={b}')

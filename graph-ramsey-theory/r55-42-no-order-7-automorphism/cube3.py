"""Build cube literal lists (orbit variables of encode.py numbering) from level-k reps.
usage: python3 cube3.py levelK.json out.icnf"""
import sys, json
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from encode import sigma_of, pair_orbits
from z7enum import unkey, code_adj, P
n, f, p, k = 42, 0, 7, 6
sig = sigma_of(n, f, p, k)
var, nv = pair_orbits(n, sig)   # var[(a,b)] for a<b -> variable
assert nv == 123
def cube(codes, words):
    lits = []
    kk = len(codes)
    for j, s in enumerate(codes):
        A = code_adj(s)
        for d in (1, 2, 3):
            v = var[(P * j, P * j + d)]
            lits.append(v if d in A else -v)
    for j in range(kk):
        for l in range(j + 1, kk):
            W = words[(j, l)]
            for r in range(P):
                v = var[(P * j, P * l + r)]
                lits.append(v if W >> r & 1 else -v)
    return lits
reps = json.load(open(sys.argv[1]))
with open(sys.argv[2], 'w') as fh:
    for key in reps:
        codes, words = unkey([tuple(key[0]), tuple(key[1])])
        fh.write('a ' + ' '.join(map(str, cube(codes, words))) + ' 0\n')
print(len(reps), 'cubes written')

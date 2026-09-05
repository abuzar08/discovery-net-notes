"""Cube-and-conquer layer for type 1^f p^k: level-L canonical Z_p-prefix cubes
(from zpenum.py levelL_pP.json) + residual symmetry clauses on the free cycles
(W_{0j} least rotation; W_{0j} sorted for j >= L), appended to a (hybrid+symF) CNF.
usage: python3 cnc_p.py in.cnf levelL.json f p k outprefix  -> outprefix.icnf (cubes), outprefix.cnf (with residual sym)"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'r55-42-prime-order-automorphisms'))  # encode.py
from encode import sigma_of, pair_orbits
inp, lvl, f, p, k, outp = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
n = 42; H = (p - 1) // 2; FULL = (1 << p) - 1
sig = sigma_of(n, f, p, k); var, nv = pair_orbits(n, sig)
cyc = lambda j, i: f + p * j + i
def code_adj(s): return {d for d in range(1, H + 1) if s >> (d - 1) & 1} | {p - d for d in range(1, H + 1) if s >> (d - 1) & 1}
def unkey(key):
    codes, wl = key; kk = len(codes); words = {}; idx = 0
    for b in range(1, kk):
        for a in range(b): words[(a, b)] = wl[idx]; idx += 1
    return list(codes), words
def cube(codes, words):
    lits = []
    for j, s in enumerate(codes):
        A = code_adj(s)
        for d in range(1, H + 1):
            v = var[(cyc(j, 0), cyc(j, d))]; lits.append(v if d in A else -v)
    for (j, l), W in words.items():
        for r in range(p):
            v = var[(cyc(j, 0), cyc(l, r))]; lits.append(v if W >> r & 1 else -v)
    return lits
reps = json.load(open(lvl)); L = len(reps[0][0])
with open(outp + '.icnf', 'w') as fh:
    for key in reps:
        codes, words = unkey(key); fh.write('a ' + ' '.join(map(str, cube(codes, words))) + ' 0\n')
# residual symmetry on free cycles L..k-1
def rot(W, t): return sum(1 << ((r + t) % p) for r in range(p) if W >> r & 1)
def val(W): return int(''.join('1' if W >> r & 1 else '0' for r in range(p)), 2)
def wordvars(j): return [var[(cyc(0, 0), cyc(j, r))] for r in range(p)]
def forbid(vs, pat): return [-v if pat >> r & 1 else v for r, v in enumerate(vs)]
minimal = {W for W in range(FULL + 1) if all(val(W) <= val(rot(W, t)) for t in range(p))}
cl = []
free = list(range(L, k))
for j in free:
    vs = wordvars(j)
    for W in range(FULL + 1):
        if W not in minimal: cl.append(forbid(vs, W))
for j, l in zip(free, free[1:]):
    vj, vl = wordvars(j), wordvars(l)
    for Wj in minimal:
        for Wl in minimal:
            if val(Wj) > val(Wl): cl.append(forbid(vj, Wj) + forbid(vl, Wl))
hdr = None; body = []
for line in open(inp):
    if line.startswith('c'): continue
    if line.startswith('p'): hdr = line.split(); continue
    body.append(line)
with open(outp + '.cnf', 'w') as fh:
    fh.write(f'p cnf {hdr[2]} {int(hdr[3]) + len(cl)}\n'); fh.writelines(body)
    for c in cl: fh.write(' '.join(map(str, c)) + ' 0\n')
print(f'{len(reps)} cubes (level {L}), {len(cl)} residual symmetry clauses ({len(minimal)} minimal words), free cycles {free}')

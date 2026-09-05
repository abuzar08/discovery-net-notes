"""Symmetry-breaking clauses for the level-3 cube-and-conquer of type 7^6:
for the three free cycles j = 3,4,5, the cross word W_{0j} (7 orbit variables,
bit r <-> pair (0, 7j+r)) is the lexicographically least rotation of its
rotation class, and W_03 <= W_04 <= W_05 as 7-bit numbers (bit 0 most significant).
Pure pattern-forbidding clauses over the orbit variables (no auxiliary variables).
usage: python3 symclauses.py base_or_hybrid.cnf out.cnf [n=42] [first_free_cycle=3]   (appends clauses, fixes header)"""
import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from encode import sigma_of, pair_orbits
P = 7
def rot(W, t): return sum(1 << ((r + t) % P) for r in range(P) if W >> r & 1)
def val(W): return int(''.join('1' if W >> r & 1 else '0' for r in range(P)), 2)  # bit 0 most significant
def wordvars(var, j): return [var[(0, P * j + r)] for r in range(P)]
def forbid(vs, pattern):  # clause excluding the assignment vs == pattern (bit r of pattern)
    return [-(v) if pattern >> r & 1 else v for r, v in enumerate(vs)]
def clauses(var, free=(3, 4, 5)):
    out = []
    minimal = {W for W in range(128) if all(val(W) <= val(rot(W, t)) for t in range(P))}
    for j in free:
        vs = wordvars(var, j)
        for W in range(128):
            if W not in minimal: out.append(forbid(vs, W))
    for (j, l) in zip(free, free[1:]):
        vj, vl = wordvars(var, j), wordvars(var, l)
        for Wj in minimal:
            for Wl in minimal:
                if val(Wj) > val(Wl): out.append(forbid(vj, Wj) + forbid(vl, Wl))
    return out, len(minimal)
if __name__ == '__main__':
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 42
    sig = sigma_of(n, 0, 7, n // 7); var, nv = pair_orbits(n, sig)
    first_free = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    cl, m = clauses(var, tuple(range(first_free, n // 7)))
    hdr = None; body = []
    for l in open(sys.argv[1]):
        if l.startswith('c'): continue
        if l.startswith('p'): hdr = l.split(); continue
        body.append(l)
    with open(sys.argv[2], 'w') as fh:
        fh.write(f'p cnf {hdr[2]} {int(hdr[3]) + len(cl)}\n'); fh.writelines(body)
        for c in cl: fh.write(' '.join(map(str, c)) + ' 0\n')
    print(f'{len(cl)} symmetry clauses ({m} minimal words)')

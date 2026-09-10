"""Add the redundant degree-window constraint to a group-orbit formula.

Every vertex of a (5,5,42)-graph has 17 <= d(v) <= 24: the neighbourhood induces a
(4,5)-graph and the non-neighbourhood a (5,4)-graph, both bounded by R(4,5) = 25.
The constraint is redundant -- every (5,5,42)-graph satisfies it -- so adding it
changes no solution, only the solver's work. All vertices in one V-orbit have the
same degree, so one totalizer per vertex orbit suffices.

Orbit variables keep their numbers, so cubes built on the plain formula stay valid.

usage: python3 groupenc_deg.py out.cnf a b1,b2,b3,b4 c
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from groupenc import build_action, pair_orbits, clauses_for

class Tot:
    def __init__(self, nv): self.nv = nv; self.cls = []
    def new(self): self.nv += 1; return self.nv
    def build(self, lits):
        if len(lits) == 1: return list(lits)
        h = len(lits) // 2
        a, b = self.build(lits[:h]), self.build(lits[h:])
        out = [self.new() for _ in range(len(a) + len(b))]
        A = [None] + a; B = [None] + b
        for i in range(len(a) + 1):
            for j in range(len(b) + 1):
                if i + j >= 1:
                    self.cls.append([x for x in (-A[i] if i else None,
                                                 -B[j] if j else None, out[i + j - 1])
                                     if x is not None])
                if i + j < len(out):
                    self.cls.append([x for x in (-out[i + j],
                                                 A[i + 1] if i + 1 <= len(a) else None,
                                                 B[j + 1] if j + 1 <= len(b) else None)
                                     if x is not None])
        return out

def build_with_degree(a, b, c, lo=17, hi=24):
    n, sig, tau = build_action(a, b, c)
    var, nv = pair_orbits(n, [sig, tau])
    cls = clauses_for(n, var)
    nbase = len(cls)
    # one representative per vertex orbit under <sig, tau>
    seen, reps = set(), []
    for v in range(n):
        if v in seen: continue
        orb, stack = set(), [v]
        while stack:
            x = stack.pop()
            if x in orb: continue
            orb.add(x); stack += [sig[x], tau[x]]
        seen |= orb; reps.append(v)
    tot = Tot(nv)
    E = lambda u, w: var[(u, w) if u < w else (w, u)]
    for v in reps:
        outs = tot.build([E(v, u) for u in range(n) if u != v])
        tot.cls.append([-outs[hi]])          # not more than hi
        tot.cls.append([outs[lo - 1]])       # at least lo
    return nv, tot.nv, nbase, cls + tot.cls, len(reps)

if __name__ == '__main__':
    out = sys.argv[1]
    a = int(sys.argv[2]); b = [int(x) for x in sys.argv[3].split(',')]; c = int(sys.argv[4])
    nv, nvtot, nbase, cls, nreps = build_with_degree(a, b, c)
    with open(out, 'w') as fh:
        fh.write(f'p cnf {nvtot} {len(cls)}\n')
        for cl in cls:
            fh.write(' '.join(map(str, cl)) + ' 0\n')
    print(f'a={a} b={tuple(b)} c={c}: {nv} orbit vars, {nvtot} total vars, '
          f'{nbase} base + {len(cls)-nbase} degree clauses, {nreps} vertex orbits')

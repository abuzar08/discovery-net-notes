"""Add the redundant degree window to an arbitrary-cycle-type orbit formula.

groupenc_deg.py does this for a Z_3 x Z_3 action; this is the same constraint for
the cyclic case that cyctype.py encodes, which is what the order-4 types need.

Every vertex of a (5,5,42)-graph has 17 <= d(v) <= 24: the neighbourhood induces a
(4,5)-graph and the non-neighbourhood a (5,4)-graph, both bounded by R(4,5) = 25.
The constraint excludes no solution, so the augmented formula has exactly the same
models as the plain one. All vertices of one <sigma>-orbit share a degree, so one
totalizer per cycle suffices.

Orbit variables keep their numbers, so cubes built on the plain formula stay valid.

usage: python3 cyctype_deg.py out.cnf len,len,...
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cyctype import sigma_of_type, pair_orbits, clauses_for

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

def build_with_degree(lengths, lo=17, hi=24):
    n = sum(lengths)
    sig = sigma_of_type(lengths)
    var, nv = pair_orbits(n, sig)
    cls = clauses_for(n, var)
    nbase = len(cls)
    reps, base = [], 0                      # one representative per cycle
    for L in lengths:
        reps.append(base); base += L
    tot = Tot(nv)
    E = lambda u, w: var[(u, w) if u < w else (w, u)]
    for v in reps:
        outs = tot.build([E(v, u) for u in range(n) if u != v])
        tot.cls.append([-outs[hi]])
        tot.cls.append([outs[lo - 1]])
    return nv, tot.nv, nbase, cls + tot.cls, len(reps)

if __name__ == '__main__':
    out = sys.argv[1]
    lengths = [int(x) for x in sys.argv[2].split(',')]
    nv, nvtot, nbase, cls, nreps = build_with_degree(lengths)
    with open(out, 'w') as fh:
        fh.write(f'p cnf {nvtot} {len(cls)}\n')
        for cl in cls:
            fh.write(' '.join(map(str, cl)) + ' 0\n')
    print(f'{lengths}: {nv} orbit vars, {nvtot} total, {nbase} base + {len(cls)-nbase} '
          f'degree clauses, {nreps} vertex orbits')

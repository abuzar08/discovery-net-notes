"""Hybrid orbit CNF: base bichromaticity clauses (encode.py) plus REDUNDANT
cardinality constraints that are theorems about (5,5,42)-graphs with an
automorphism of type 1^f p^k (justified by classical Ramsey numbers).

Redundant constraints (n = 42, degree window from R(4,5)=25):
  D. every vertex v: 17 <= d(v) <= 24                  [R(4,5)=25]
  C. p>=5, each cycle C: |A_C| <= 13 and |B_C| <= 13   [R(3,5)=14; C has an edge and a non-edge]
  T. p=3, each cycle C with internal variable x_C:
        x_C (C=K3): |A_C| <= 4, |B_C| <= 24            [R(1,5)... A_C independent; B_C is (5,4)-good, R(4,5)=25]
       ~x_C (C=I3): |B_C| <= 4, |A_C| <= 24
  P. p>=5, k>=2, each profile P with {} != P != [k]: at most 5 fixed vertices
     have exactly profile P                            [R(3,3)=6]
A_C = fixed vertices adjacent to all of C, B_C = fixed vertices adjacent to none.
Cardinalities use a totalizer (Bailleux-Boufkhad) with both implication
directions, so any model of the base CNF satisfying the constraints extends.
The DIMACS file lists base clauses first; a JSON manifest records every
constraint (input literals, bounds, aux variable range) for independent audit.
"""
import sys, json
from encode import encode, write_dimacs

class Totalizer:
    def __init__(self, nv):
        self.nv = nv
        self.clauses = []
    def new(self):
        self.nv += 1
        return self.nv
    def build(self, lits):
        """Return list outs with outs[i-1] <=> at least i of lits are true."""
        if len(lits) == 1:
            return [lits[0]]
        h = len(lits) // 2
        a = self.build(lits[:h]); b = self.build(lits[h:])
        p, q = len(a), len(b)
        r = [self.new() for _ in range(p + q)]
        for al in range(p + 1):
            for be in range(q + 1):
                s = al + be
                # (>=al in a) & (>=be in b) -> (>=s in r)
                if s >= 1:
                    c = []
                    if al >= 1: c.append(-a[al - 1])
                    if be >= 1: c.append(-b[be - 1])
                    c.append(r[s - 1])
                    self.clauses.append(c)
                # (>=s+1 in r) -> (>=al+1 in a) or (>=be+1 in b)
                if s + 1 <= p + q:
                    c = [-r[s]]
                    if al + 1 <= p: c.append(a[al])
                    if be + 1 <= q: c.append(b[be])
                    self.clauses.append(c)
        return r

def hybrid(n, f, p, k):
    sig, var, nv, base = encode(n, f, p, k)
    nbase = len(base)
    tot = Totalizer(nv)
    manifest = []
    def card(lits, lo, hi, why, cond=None):
        """Add: (cond ->) lo <= #true(lits) <= hi. lits may repeat."""
        start = tot.nv + 1
        outs = tot.build(list(lits))
        extra = []
        if hi < len(lits):
            extra.append(([-outs[hi]] if cond is None else [-cond, -outs[hi]]))
        if lo >= 1:
            extra.append(([outs[lo - 1]] if cond is None else [-cond, outs[lo - 1]]))
        tot.clauses.extend(extra)
        manifest.append(dict(lits=list(lits), lo=lo, hi=hi, cond=cond, aux=[start, tot.nv], why=why))
    def e(u, v):
        return var[(u, v) if u < v else (v, u)]
    # D: degree windows, one representative per vertex orbit
    reps = list(range(f)) + [f + j * p for j in range(k)]
    for v in reps:
        card([e(v, u) for u in range(n) if u != v], 17, 24, f"degree of vertex {v} in [17,24] (R(4,5)=25)")
    # C / T: fixed vertices vs cycles
    for j in range(k):
        c0 = f + j * p
        ys = [e(v, c0) for v in range(f)]   # y_{v,C_j}: v adjacent to all of C_j
        if f == 0:
            continue
        if p >= 5:
            card(ys, max(0, f - 13), min(13, f), f"cycle {j}: |A_C|<=13 and |B_C|<=13 (R(3,5)=14)")
        elif p == 3:
            xC = e(c0, c0 + 1)
            card(ys, max(0, f - 24), min(4, f), f"cycle {j} is K3: |A_C|<=4, |B_C|<=24", cond=xC)
            card(ys, max(0, f - 4), min(24, f), f"cycle {j} is I3: |B_C|<=4, |A_C|<=24", cond=-xC)
    # P: profiles (p>=5, 2<=k<=5, f>=6)
    if p >= 5 and 2 <= k <= 5 and f >= 6:
        from itertools import product
        for prof in product([0, 1], repeat=k):
            if sum(prof) in (0, k):
                continue
            zs = []
            for v in range(f):
                z = tot.new()
                lits = [e(v, f + j * p) if prof[j] else -e(v, f + j * p) for j in range(k)]
                # z <-> AND lits
                tot.clauses.append([z] + [-l for l in lits])
                for l in lits:
                    tot.clauses.append([-z, l])
                zs.append(z)
            card(zs, 0, 5, f"profile {prof}: at most 5 fixed vertices (R(3,3)=6)")
    clauses = base + tot.clauses
    return sig, var, nv, tot.nv, nbase, clauses, manifest

if __name__ == '__main__':
    n, f, p, k = map(int, sys.argv[1:5]); out = sys.argv[5]
    sig, var, nv, nvtot, nbase, clauses, manifest = hybrid(n, f, p, k)
    write_dimacs(out, nvtot, clauses, f"R(5,5) n={n} type 1^{f} {p}^{k}; {nv} orbit vars, {nbase} base clauses, then redundant cardinality clauses")
    json.dump(dict(n=n, f=f, p=p, k=k, orbit_vars=nv, total_vars=nvtot, base_clauses=nbase, total_clauses=len(clauses), constraints=manifest), open(out + '.manifest.json', 'w'))
    print(f"type 1^{f} {p}^{k}: {nv} orbit vars, {nvtot} total vars, {nbase} base + {len(clauses)-nbase} redundant clauses")

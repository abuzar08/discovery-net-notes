"""Independent checker for the hybrid CNFs (standard library only).

Regenerates, from (n, f, p, k) alone and with code written separately from
hybrid.py, the base orbit CNF (union-find over pairs; 5-set orbit
representatives) and the redundant cardinality constraints D, C, T, P described
in hybrid.py (own totalizer implementation), and checks that the DIMACS file's
clause set is exactly the regenerated set with base clauses first.  Then checks
an LRAT refutation (RUP hints) of the file.

usage: python3 verify_hybrid.py n f p k file.cnf file.lrat[.xz]
"""
import sys, json
from itertools import combinations, product
from verify import build as build_base, read_dimacs, check_lrat, sha256

def orbit_var(n, f, p, k):
    """Recompute the pair->variable map exactly as verify.build does (least pair first)."""
    perm = {v: v for v in range(f)}
    for j in range(k):
        for i in range(p):
            perm[f + j*p + i] = f + j*p + (i + 1) % p
    var = {}
    nxt = 0
    for u, v in combinations(range(n), 2):
        if (u, v) in var: continue
        nxt += 1
        a, b = u, v
        for _ in range(p):
            key = (min(a, b), max(a, b))
            var.setdefault(key, nxt)
            a, b = perm[a], perm[b]
    return var, nxt

class Tot:
    def __init__(self, nv): self.nv = nv; self.cls = []
    def fresh(self): self.nv += 1; return self.nv
    def unary(self, lits):
        m = len(lits)
        if m == 1: return list(lits)
        left = self.unary(lits[:m // 2]); right = self.unary(lits[m // 2:])
        out = [self.fresh() for _ in range(len(left) + len(right))]
        A = [None] + left; B = [None] + right   # 1-indexed
        for i in range(len(left) + 1):
            for j in range(len(right) + 1):
                if i + j >= 1:
                    self.cls.append([x for x in (-A[i] if i else None, -B[j] if j else None, out[i + j - 1]) if x is not None])
                if i + j < len(out):
                    self.cls.append([x for x in (-out[i + j], A[i + 1] if i + 1 <= len(left) else None, B[j + 1] if j + 1 <= len(right) else None) if x is not None])
        return out

def regenerate(n, f, p, k):
    nv, base = build_base(n, f, p, k)
    var, nv2 = orbit_var(n, f, p, k); assert nv == nv2
    e = lambda u, v: var[(min(u, v), max(u, v))]
    T = Tot(nv)
    def card(lits, lo, hi, cond=None):
        outs = T.unary(list(lits))
        pre = [] if cond is None else [-cond]
        if hi < len(lits): T.cls.append(pre + [-outs[hi]])
        if lo >= 1: T.cls.append(pre + [outs[lo - 1]])
    for v in list(range(f)) + [f + j * p for j in range(k)]:
        card([e(v, u) for u in range(n) if u != v], 17, 24)
    for j in range(k):
        c0 = f + j * p
        if f == 0: continue
        ys = [e(v, c0) for v in range(f)]
        if p >= 5:
            card(ys, max(0, f - 13), min(13, f))
        elif p == 3:
            x = e(c0, c0 + 1)
            card(ys, max(0, f - 24), min(4, f), cond=x)
            card(ys, max(0, f - 4), min(24, f), cond=-x)
    if p >= 5 and 2 <= k <= 5 and f >= 6:
        for prof in product([0, 1], repeat=k):
            if sum(prof) in (0, k): continue
            zs = []
            for v in range(f):
                z = T.fresh()
                lits = [e(v, f + j * p) if prof[j] else -e(v, f + j * p) for j in range(k)]
                T.cls.append([z] + [-l for l in lits])
                T.cls += [[-z, l] for l in lits]
                zs.append(z)
            card(zs, 0, 5)
    return nv, T.nv, base, T.cls

def canon(c): return tuple(sorted(c, key=lambda x: (abs(x), x)))

if __name__ == '__main__':
    n, f, p, k = map(int, sys.argv[1:5]); cnf, lrat = sys.argv[5], sys.argv[6]
    nv, nvtot, base, extra = regenerate(n, f, p, k)
    nvf, cls = read_dimacs(cnf)
    assert nvf == nvtot, (nvf, nvtot)
    got_base = {canon(c) for c in cls[:len(base)]}
    assert len(got_base) == len(base) and got_base == {canon(c) for c in base}, "base clause mismatch"
    got_extra = [canon(c) for c in cls[len(base):]]
    want_extra = [canon(c) for c in extra]
    assert sorted(got_extra) == sorted(want_extra), "redundant clause mismatch"
    print(f"type 1^{f} {p}^{k}: hybrid CNF regenerated and agrees ({nv} orbit vars, {nvtot} vars, {len(base)} base + {len(extra)} redundant clauses); sha256 {sha256(cnf)}")
    ok = check_lrat(cls, lrat)
    print("LRAT proof:", "VERIFIED (empty clause derived)" if ok else "FAILED", sha256(lrat))
    sys.exit(0 if ok else 1)

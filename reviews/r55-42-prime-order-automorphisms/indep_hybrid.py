"""reviewer-1: independent hybrid CNF.  Base orbit clauses from indep_encode.py
plus the redundant constraints D / C / T / P justified by the analytic lemma,
encoded with a Sinz sequential counter (implication direction only), i.e. a
*different* encoding from the totalizer of hybrid.py.  Purpose: re-solve the
21 hybrid types independently of the published certificates.

usage: python3 indep_hybrid.py n f p k out.cnf
"""
import sys
from itertools import product
from indep_encode import permutation, orbits_of_pairs, base_clauses


class Sinz:
    def __init__(self, nv):
        self.nv = nv
        self.cls = []

    def fresh(self):
        self.nv += 1
        return self.nv

    def atmost(self, xs, kb, cond=None):
        """Clauses forcing (cond ->) sum(xs) <= kb (Sinz 2005, LTseq).
        Counter-definition clauses are unconditional (always extendable);
        only the overflow clauses carry the guard."""
        n = len(xs)
        guard = [] if cond is None else [-cond]
        if kb >= n:
            return
        if kb <= 0:
            for x in xs:
                self.cls.append(guard + [-x])
            return
        s = [[self.fresh() for _ in range(kb)] for _ in range(n - 1)]  # s[i][j]: >= j+1 among xs[0..i]
        self.cls.append([-xs[0], s[0][0]])
        for j in range(1, kb):
            self.cls.append([-s[0][j]])
        for i in range(1, n - 1):
            self.cls.append([-xs[i], s[i][0]])
            self.cls.append([-s[i - 1][0], s[i][0]])
            for j in range(1, kb):
                self.cls.append([-xs[i], -s[i - 1][j - 1], s[i][j]])
                self.cls.append([-s[i - 1][j], s[i][j]])
            self.cls.append(guard + [-xs[i], -s[i - 1][kb - 1]])
        self.cls.append(guard + [-xs[n - 1], -s[n - 2][kb - 1]])

    def card(self, xs, lo, hi, cond=None):
        self.atmost(list(xs), hi, cond)
        if lo > 0:
            self.atmost([-x for x in xs], len(xs) - lo, cond)


def build(n, f, p, k):
    sig = permutation(n, f, p, k)
    var, nv = orbits_of_pairs(n, sig)
    base = base_clauses(n, var)
    e = lambda u, v: var[(u, v) if u < v else (v, u)]
    S = Sinz(nv)
    # D: degree window 17..24, one representative per vertex orbit
    for v in list(range(f)) + [f + j * p for j in range(k)]:
        S.card([e(v, u) for u in range(n) if u != v], 17, 24)
    # C / T
    if f > 0:
        for j in range(k):
            c0 = f + j * p
            ys = [e(v, c0) for v in range(f)]
            if p >= 5:
                S.card(ys, max(0, f - 13), min(13, f))
            elif p == 3:
                x = e(c0, c0 + 1)
                S.card(ys, max(0, f - 24), min(4, f), cond=x)
                S.card(ys, max(0, f - 4), min(24, f), cond=-x)
    # P: profiles
    if p >= 5 and 2 <= k <= 5 and f >= 6:
        for prof in product([0, 1], repeat=k):
            if sum(prof) in (0, k):
                continue
            zs = []
            for v in range(f):
                z = S.fresh()
                lits = [e(v, f + j * p) if prof[j] else -e(v, f + j * p) for j in range(k)]
                S.cls.append([z] + [-l for l in lits])
                for l in lits:
                    S.cls.append([-z, l])
                zs.append(z)
            S.card(zs, 0, 5)
    return nv, S.nv, base, S.cls


if __name__ == '__main__':
    n, f, p, k = map(int, sys.argv[1:5])
    out = sys.argv[5]
    nv, nvt, base, extra = build(n, f, p, k)
    bl = sorted(sorted(c, key=lambda x: (abs(x), x)) for c in base)
    with open(out, 'w') as fh:
        fh.write(f"c reviewer-1 independent hybrid CNF 1^{f} {p}^{k}\n")
        fh.write(f"p cnf {nvt} {len(bl) + len(extra)}\n")
        for c in bl:
            fh.write(' '.join(map(str, c)) + ' 0\n')
        for c in extra:
            fh.write(' '.join(map(str, c)) + ' 0\n')
    print(f"1^{f} {p}^{k}: {nv} orbit vars, {nvt} total vars, {len(bl)} base + {len(extra)} redundant clauses")

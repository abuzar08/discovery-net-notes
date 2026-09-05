"""Independent checker for a type-1^f p^k refutation with fixed-vertex lex-leader
symmetry breaking.  Regenerates the formula (base orbit CNF via verify.build, or
the hybrid CNF via verify_hybrid.regenerate) and the lex-leader clauses from
their definition (code written separately from symF.py), asserts that the CNF
file is exactly formula + lex-leader clauses (in that order), and replays the
LRAT proof (RUP hints only) with verify.check_lrat.
Lex-leader definition: fixed vertices 0..f-1; for u = 0..f-2 the row
  R_u = (x(u, c_0), ..., x(u, c_{k-1}), x(u, w) for w in 0..f-1, w not in {u, u+1})
  with c_j = f + j*p (the profile bit for cycle j is the orbit variable of the pair (u, c_j))
  satisfies R_u <=lex R_{u+1}, encoded with fresh 'prefix equal' variables
  e_1..e_{m-1} (m = |R_u|): clauses (-e_{t-1} v -a_t v b_t), (-e_{t-1} v a_t v b_t v e_t),
  (-e_{t-1} v -a_t v -b_t v e_t) for t = 1..m (e_0 omitted; e_m not created), variables
  numbered consecutively after the formula's variables, row by row.
usage: python3 verify_symF.py n f p k base|hybrid file.cnf file.lrat[.xz]"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'r55-42-prime-order-automorphisms'))
from verify import build, read_dimacs, check_lrat, sha256
from verify_hybrid import regenerate, orbit_var

def lex_clauses(n, f, p, k, var, nv):
    x = lambda u, v: var[(min(u, v), max(u, v))]
    out = []
    for u in range(f - 1):
        cols = [f + j * p for j in range(k)] + [w for w in range(f) if w not in (u, u + 1)]
        a = [x(u, c) for c in cols]; b = [x(u + 1, c) for c in cols]; m = len(a)
        e_prev = None
        for t in range(m):
            pre = [] if e_prev is None else [-e_prev]
            out.append(pre + [-a[t], b[t]])
            if t < m - 1:
                nv += 1
                out.append(pre + [a[t], b[t], nv]); out.append(pre + [-a[t], -b[t], nv])
                e_prev = nv
    return out, nv

def main():
    n, f, p, k = map(int, sys.argv[1:5]); mode, cnf, lrat = sys.argv[5:8]
    var, nvo = orbit_var(n, f, p, k)
    if mode == 'base':
        nvf, formula = build(n, f, p, k); assert nvf == nvo
    else:
        nvo2, nvf, base, extra = regenerate(n, f, p, k); assert nvo2 == nvo; formula = list(base) + list(extra)
    lex, nvtot = lex_clauses(n, f, p, k, var, nvf)
    nvfile, cls = read_dimacs(cnf)
    canon = lambda c: tuple(sorted(c, key=lambda x: (abs(x), x)))
    assert nvfile == nvtot, (nvfile, nvtot)
    assert len(cls) == len(formula) + len(lex), (len(cls), len(formula), len(lex))
    got_f = [canon(c) for c in cls[:len(formula)]]; want_f = [canon(c) for c in formula]
    assert sorted(got_f) == sorted(want_f), 'formula clause mismatch'
    assert [canon(c) for c in cls[len(formula):]] == [canon(c) for c in lex], 'lex-leader clause mismatch'
    print(f'type 1^{f} {p}^{k} ({mode}): CNF regenerated and agrees: {nvo} orbit vars, {len(formula)} formula clauses + {len(lex)} lex-leader clauses, {nvtot} vars; sha256 {sha256(cnf)}')
    ok = check_lrat(cls, lrat)
    print('LRAT proof:', 'VERIFIED (empty clause derived)' if ok else 'FAILED', os.path.getsize(lrat), 'bytes, sha256', sha256(lrat))
    sys.exit(0 if ok else 1)
main()

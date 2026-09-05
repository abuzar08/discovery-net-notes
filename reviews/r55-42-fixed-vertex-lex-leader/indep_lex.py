"""reviewer-1: independent regeneration of the fixed-vertex lex-leader clauses
(L) of the r55-42-fixed-vertex-lex-leader artifact, written from the README's
definition only (rows R_u, columns = profile columns c_j = f + j*p followed by
w in 0..f-1 \\ {u, u+1}; clauses (-e_{t-1} v -a_t v b_t), (-e_{t-1} v a_t v b_t v e_t),
(-e_{t-1} v -a_t v -b_t v e_t), e_0 = true, no e_m, fresh e's numbered after the
formula's variables, row by row), on top of the reviewer's own orbit numbering
(indep_encode.py, h2543 evidence).  Checks a DIMACS file produced by the
target pipeline (encode.py|hybrid.py + symF.py):
  * header variable count == own count;
  * the trailing clauses are exactly (in order) the reviewer's (L) clauses;
  * the leading clauses: base mode -> set-equal to the reviewer's base clause
    set; hybrid mode -> the first |base| clauses set-equal to the reviewer's
    base set, and the middle block set-equal to the redundant clauses of the
    target's hybrid.py (audited semantically at h2543, test_card.py).
usage: python3 indep_lex.py n f p k base|hybrid file.cnf
"""
import sys, os
from indep_encode import permutation, orbits_of_pairs, base_clauses


def lex_le_clauses(a, b, nv):
    """(L) clauses for a <=lex b; returns (clauses, nv)."""
    out = []
    m = len(a)
    assert m == len(b)
    e_prev = None                    # e_0 = true: literal omitted
    for t in range(m):
        pre = [] if e_prev is None else [-e_prev]
        out.append(pre + [-a[t], b[t]])
        if t < m - 1:                # no e_m
            nv += 1
            out.append(pre + [a[t], b[t], nv])
            out.append(pre + [-a[t], -b[t], nv])
            e_prev = nv
    return out, nv


def L_clauses(n, f, p, k, var, nv):
    x = lambda u, w: var[(u, w) if u < w else (w, u)]
    out = []
    for u in range(f - 1):
        cols = [f + j * p for j in range(k)] + [w for w in range(f) if w not in (u, u + 1)]
        a = [x(u, c) for c in cols]
        b = [x(u + 1, c) for c in cols]
        cl, nv = lex_le_clauses(a, b, nv)
        out.extend(cl)
    return out, nv


def read_dimacs(path):
    nv = None
    cls = []
    with open(path) as fh:
        for line in fh:
            if line.startswith('c'):
                continue
            if line.startswith('p'):
                nv = int(line.split()[2])
                continue
            lits = [int(t) for t in line.split()]
            if not lits:
                continue
            assert lits[-1] == 0
            cls.append(lits[:-1])
    return nv, cls


def canon(c):
    return tuple(sorted(c, key=lambda x: (abs(x), x)))


def main():
    n, f, p, k = map(int, sys.argv[1:5])
    mode, path = sys.argv[5], sys.argv[6]
    sig = permutation(n, f, p, k)
    var, nvo = orbits_of_pairs(n, sig)
    base = base_clauses(n, var)
    nvfile, cls = read_dimacs(path)
    if mode == 'base':
        nvform = nvo
        nform = len(base)
    else:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'r55-42-prime-order-automorphisms'))
        from hybrid import hybrid
        _, tvar, tnv, tnvtot, tnbase, tclauses, _ = hybrid(n, f, p, k)
        assert tnv == nvo and tnbase == len(base)
        nvform = tnvtot
        nform = len(tclauses)
        mid_want = sorted(canon(c) for c in tclauses[tnbase:])
    L, nvtot = L_clauses(n, f, p, k, var, nvform)
    assert nvfile == nvtot, ('var count', nvfile, nvtot)
    assert len(cls) == nform + len(L), ('clause count', len(cls), nform, len(L))
    lead = cls[:nform]
    got_base = {frozenset(c) for c in lead[:len(base)]}
    assert got_base == base, 'base clause set mismatch'
    assert all(len(c) == len(set(c)) for c in lead[:len(base)])
    if mode == 'hybrid':
        assert sorted(canon(c) for c in lead[len(base):]) == mid_want, 'hybrid redundant block mismatch'
    got_L = [canon(c) for c in cls[nform:]]
    want_L = [canon(c) for c in L]
    assert got_L == want_L, 'lex-leader clauses differ'
    print(f'1^{f} {p}^{k} {mode}: OK  orbit vars {nvo}, formula vars {nvform}, total vars {nvtot}, '
          f'formula clauses {nform} (base {len(base)}), L clauses {len(L)}, aux e vars {nvtot - nvform}')


if __name__ == '__main__':
    main()

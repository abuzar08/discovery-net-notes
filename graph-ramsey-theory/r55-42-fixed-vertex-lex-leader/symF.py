"""Append lex-leader symmetry breaking on the fixed vertices (sb_l* of Codish,
Miller, Prosser, Stuckey: for consecutive fixed vertices u, u+1 the adjacency
rows, restricted to the profile columns (one per cycle) followed by the fixed
columns w != u, u+1, satisfy row(u) <=lex row(u+1)).  Sound because any
permutation of the fixed vertices is a symmetry of the type-1^f p^k formula.
usage: python3 symF.py in.cnf out.cnf n f p k"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'r55-42-prime-order-automorphisms'))
from encode import sigma_of, pair_orbits

def lex_le(a, b, nv, out):
    """clauses forcing a <=lex b (bit lists, first most significant); returns new nv."""
    e = None
    for t, (x, y) in enumerate(zip(a, b)):
        pre = [] if e is None else [-e]
        out.append(pre + [-x, y])                      # equal prefix & x > y forbidden
        if t + 1 < len(a):
            nv += 1; ne = nv
            out.append(pre + [x, y, ne]); out.append(pre + [-x, -y, ne])
            e = ne
    return nv

def main():
    inp, outp, n, f, p, k = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7])
    sig = sigma_of(n, f, p, k); var, nv0 = pair_orbits(n, sig)
    V = lambda u, w: var[(u, w) if u < w else (w, u)]
    cls = []; nv = None
    with open(inp) as fh:
        for l in fh:
            if l.startswith('c'): continue
            if l.startswith('p'): nv = int(l.split()[2]); continue
            cls.append(l.strip())
    assert nv >= nv0
    out = []
    for u in range(f - 1):
        cols = [f + j * p for j in range(k)] + [w for w in range(f) if w not in (u, u + 1)]
        nv = lex_le([V(u, c) for c in cols], [V(u + 1, c) for c in cols], nv, out)
    with open(outp, 'w') as fh:
        fh.write(f'p cnf {nv} {len(cls) + len(out)}\n')
        fh.write('\n'.join(cls) + '\n'); fh.write('\n'.join(' '.join(map(str, c)) + ' 0' for c in out) + '\n')
    print(f'{len(out)} symmetry clauses, {nv - nv0} aux vars (total {nv})')
main()

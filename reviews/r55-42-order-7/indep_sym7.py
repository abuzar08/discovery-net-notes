r"""reviewer-1: independent check of the formula of h2621.

`f0_p7_k6_basesym.cnf` must be exactly

  * my own base orbit clause set for the type \(1^0 7^6\) — one Boolean per
    \(\langle \sigma \rangle\)-orbit of pairs on 42 vertices, two clauses per
    orbit of 5-sets, built by my union-find-free encoder from h2543 — followed by
  * the residual symmetry clauses (S), rebuilt here from the README's definition:
    for each free cycle \(j \in \{3,4,5\}\) the word
    \(W_{0j} = (x((0,0),(j,r)))_{r=0}^{6}\) is the least of its seven rotations,
    and \(W_{03} \le W_{04} \le W_{05}\) as 7-bit numbers.

usage: python3 indep_sym7.py n f p k level file.cnf
"""
import sys
from itertools import combinations
from indep_encode import permutation, orbits_of_pairs, base_clauses


def val(bits):
    return int(''.join(str(b) for b in bits), 2)


def rotations(W):
    p = len(W)
    return [tuple(W[(r - t) % p] for r in range(p)) for t in range(p)]


def S_clauses(n, f, p, k, var, level):
    x = lambda u, w: var[(u, w) if u < w else (w, u)]
    words = {j: tuple(x(f, f + p * j + r) for r in range(p)) for j in range(1, k)}
    allw = list(range(1 << p))
    bits = lambda W: tuple(W >> r & 1 for r in range(p))
    minimal = [W for W in allw if all(val(bits(W)) <= val(R) for R in rotations(bits(W)))]
    forbid = lambda vs, W: [(-v if W >> r & 1 else v) for r, v in enumerate(vs)]
    out = []
    free = list(range(level, k))
    for j in free:
        for W in allw:
            if W not in minimal:
                out.append(forbid(words[j], W))
    for j, l in zip(free, free[1:]):
        for Wj in minimal:
            for Wl in minimal:
                if val(bits(Wj)) > val(bits(Wl)):
                    out.append(forbid(words[j], Wj) + forbid(words[l], Wl))
    return out, minimal, free


def read_dimacs(path):
    nv, cls = None, []
    for line in open(path):
        if line.startswith('c'):
            continue
        if line.startswith('p'):
            nv = int(line.split()[2])
            continue
        lits = [int(t) for t in line.split()]
        if not lits:
            continue
        assert lits[-1] == 0
        cls.append(tuple(lits[:-1]))
    return nv, cls


def canon(c):
    return tuple(sorted(c, key=lambda t: (abs(t), t)))


def main():
    n, f, p, k, level = map(int, sys.argv[1:6])
    path = sys.argv[6]
    sig = permutation(n, f, p, k)
    var, nvo = orbits_of_pairs(n, sig)
    base = base_clauses(n, var)
    S, minimal, free = S_clauses(n, f, p, k, var, level)
    nvfile, cls = read_dimacs(path)
    assert nvfile == nvo, ('variable count', nvfile, nvo)
    assert len(cls) == len(base) + len(S), ('clause count', len(cls), len(base), len(S))
    got = {frozenset(c) for c in cls[:len(base)]}
    assert got == base, 'base clause set differs from my own encoder'
    assert sorted(canon(c) for c in cls[len(base):]) == sorted(canon(c) for c in S), \
        'residual symmetry clauses differ'
    print(f'1^{f} {p}^{k} level {level}: CNF OK — {len(base)} base orbit clauses (set-equal to mine) + '
          f'{len(S)} residual clauses (equal as a set), {nvo} orbit variables; '
          f'free cycles {free}, {len(minimal)} rotation-minimal words')


if __name__ == '__main__':
    main()

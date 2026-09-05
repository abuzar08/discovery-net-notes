"""reviewer-1: independent check of the cube-and-conquer CNF of h2873.

The file c15_3_9_L4.cnf must be, in this order:
  * my own base clause set for the type (indep_encode, h2543 evidence),
  * the redundant cardinality block of hybrid.py (audited semantically at h2543),
  * my own fixed-vertex lex-leader clauses (L) (indep_lex, h2867 evidence),
  * my own residual clauses (S), written here from the README's definition:
    for every free cycle j >= level, the word W_0j = (x((0,0),(j,0)),
    x((0,0),(j,1)), x((0,0),(j,2))) is the least of its three rotations, and
    the words of consecutive free cycles are non-decreasing, both under the
    order "read the word as a binary number, bit r = position r".

usage: python3 indep_cnc.py n f p k level file.cnf
"""
import sys, os
from itertools import combinations
from indep_encode import permutation, orbits_of_pairs, base_clauses
from indep_lex import L_clauses, read_dimacs, canon

P = 3


def word_of(W, p):
    """value of the word W (a tuple of p bits, position r) as a binary number"""
    return int(''.join(str(b) for b in W), 2)


def rotations(W):
    """the p rotations of the word: rotating cycle j by t sends bit r to r+t"""
    p = len(W)
    return [tuple(W[(r - t) % p] for r in range(p)) for t in range(p)]


def S_clauses(n, f, p, k, var, level):
    """residual clauses on the free cycles level..k-1"""
    x = lambda u, w: var[(u, w) if u < w else (w, u)]
    # W_0j, j >= 1: cross word from vertex (0,0) = f to the p vertices of cycle j
    words = {j: tuple(x(f, f + p * j + r) for r in range(p)) for j in range(1, k)}
    allw = list(range(1 << p))
    bits = lambda W: tuple(W >> r & 1 for r in range(p))
    minimal = [W for W in allw if all(word_of(bits(W), p) <= word_of(R, p) for R in rotations(bits(W)))]
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
                if word_of(bits(Wj), p) > word_of(bits(Wl), p):
                    out.append(forbid(words[j], Wj) + forbid(words[l], Wl))
    return out, minimal, free


def main():
    n, f, p, k, level = map(int, sys.argv[1:6])
    path = sys.argv[6]
    sig = permutation(n, f, p, k)
    var, nvo = orbits_of_pairs(n, sig)
    base = base_clauses(n, var)
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'r55-42-prime-order-automorphisms'))
    from hybrid import hybrid
    _, tvar, tnv, tnvtot, tnbase, tclauses, _ = hybrid(n, f, p, k)
    assert tnv == nvo and tnbase == len(base), 'hybrid base disagrees with my encoder'
    mid_want = sorted(canon(c) for c in tclauses[tnbase:])
    L, nvtot = L_clauses(n, f, p, k, var, tnvtot)
    S, minimal, free = S_clauses(n, f, p, k, var, level)

    nvfile, cls = read_dimacs(path)
    assert nvfile == nvtot, ('var count', nvfile, nvtot)
    assert len(cls) == len(tclauses) + len(L) + len(S), ('clause count', len(cls))
    lead = cls[:len(tclauses)]
    assert {frozenset(c) for c in lead[:len(base)]} == base, 'base clause set mismatch'
    assert sorted(canon(c) for c in lead[len(base):]) == mid_want, 'hybrid redundant block mismatch'
    off = len(tclauses)
    assert [canon(c) for c in cls[off:off + len(L)]] == [canon(c) for c in L], 'lex-leader clauses differ'
    off += len(L)
    assert sorted(canon(c) for c in cls[off:]) == sorted(canon(c) for c in S), 'residual clauses differ'
    print(f'1^{f} {p}^{k} level {level}: CNF OK — {len(base)} base + {len(tclauses) - len(base)} redundant + '
          f'{len(L)} lex-leader + {len(S)} residual = {len(cls)} clauses, {nvo} orbit vars, {nvtot} vars; '
          f'free cycles {free}, {len(minimal)} rotation-minimal words')


if __name__ == '__main__':
    main()

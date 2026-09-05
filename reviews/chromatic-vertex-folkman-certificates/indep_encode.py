"""reviewer-1: independent regeneration of the lower-bound CNF for a certificate.

usage: python indep_encode.py N K Q PARTS.txt TARGET.cnf
Regenerates the clause set for (N, K, Q, PARTS) with min-degree K-1 and the
lex-leader symmetry breaking, written from the mathematical description only
(README "Certificates" section), and compares it as a *set of clauses* with
TARGET.cnf produced by the target's encode.py.  Nothing from the target's
code is imported.
"""
import itertools, sys


def regen(n, k, q, parts):
    var = {}
    for u in range(n):
        for v in range(u + 1, n):
            var[(u, v)] = len(var) + 1
    x = lambda u, v: var[(u, v)] if u < v else var[(v, u)]
    C = set()
    # K_q-free: every q-set contains a non-edge
    for S in itertools.combinations(range(n), q):
        C.add(frozenset(-x(u, v) for u, v in itertools.combinations(S, 2)))
    # each listed partition is not a proper colouring
    for P in parts:
        C.add(frozenset(x(u, v) for B in P for u, v in itertools.combinations(sorted(B), 2)))
    # min degree >= k-1: no vertex has n-(k-1) non-neighbours
    d = k - 1
    for v in range(n):
        for S in itertools.combinations([w for w in range(n) if w != v], n - d):
            C.add(frozenset(x(v, w) for w in S))
    # lex-leader for each transposition (i,i+1): vector a = (x(i,w))_{w != i,i+1}
    # in increasing w, must be >=_lex b = (x(i+1,w)).  Chain with e_t <-> e_{t-1} & (a_t=b_t)
    nxt = len(var)
    for i in range(n - 1):
        j = i + 1
        ws = [w for w in range(n) if w not in (i, j)]
        prev = None
        for t, w in enumerate(ws):
            a, b = x(i, w), x(j, w)
            if prev is None:
                C.add(frozenset((a, -b)))
            else:
                C.add(frozenset((-prev, a, -b)))
            if t == len(ws) - 1:
                break
            nxt += 1
            e = nxt
            if prev is None:
                C |= {frozenset((-e, a, -b)), frozenset((-e, -a, b)),
                      frozenset((e, a, b)), frozenset((e, -a, -b))}
            else:
                C |= {frozenset((-e, prev)), frozenset((-e, a, -b)), frozenset((-e, -a, b)),
                      frozenset((e, -prev, a, b)), frozenset((e, -prev, -a, -b))}
            prev = e
    return nxt, C


def read_parts(path, n, k):
    out = []
    for line in open(path):
        line = line.strip()
        if not line or line[0] == '#':
            continue
        blocks = [[int(v) for v in b.split(',') if v] for b in line.split('|')]
        blocks = [b for b in blocks if b]
        assert sorted(v for b in blocks for v in b) == list(range(n)), "not a partition"
        assert len(blocks) <= k - 1, "too many blocks"
        out.append(blocks)
    return out


def read_cnf(path):
    nv, cls = None, []
    for line in open(path):
        if line[0] in 'c%':
            continue
        if line[0] == 'p':
            nv = int(line.split()[2]); continue
        t = [int(s) for s in line.split()]
        assert t and t[-1] == 0
        cls.append(frozenset(t[:-1]))
    return nv, cls


if __name__ == '__main__':
    n, k, q = map(int, sys.argv[1:4])
    parts = read_parts(sys.argv[4], n, k)
    nv, C = regen(n, k, q, parts)
    tnv, tcls = read_cnf(sys.argv[5])
    same = (set(tcls) == C) and (nv == tnv) and (len(tcls) == len(C))
    print(f"n={n} k={k} q={q} partitions={len(parts)} own: vars={nv} clauses={len(C)}  "
          f"target: vars={tnv} clauses={len(tcls)} (distinct {len(set(tcls))})  SAME={same}")
    sys.exit(0 if same else 1)

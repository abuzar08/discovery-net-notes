"""Independent checker (standard library only).

1. Rebuilds the orbit CNF for automorphism type 1^f p^k on n vertices using a
   different route than encode.py (union-find over pair indices, orbit
   representatives of 5-sets by explicit group action) and checks that the set
   of clauses equals the clause set of the given DIMACS file.
2. Checks an LRAT proof of unsatisfiability (RUP hints only) against that CNF.

usage: python3 verify.py n f p k file.cnf file.lrat[.xz]
"""
import sys, lzma, hashlib
from itertools import combinations

def build(n, f, p, k):
    assert f + p * k == n and p >= 2
    # permutation as a dict
    perm = {v: v for v in range(f)}
    for j in range(k):
        for i in range(p):
            perm[f + j*p + i] = f + j*p + (i + 1) % p
    assert sorted(perm.values()) == list(range(n))
    # union-find over pairs
    pairs = list(combinations(range(n), 2))
    pidx = {e: i for i, e in enumerate(pairs)}
    parent = list(range(len(pairs)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for (u, v) in pairs:
        a, b = perm[u], perm[v]
        img = (a, b) if a < b else (b, a)
        ra, rb = find(pidx[(u, v)]), find(pidx[img])
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    # variable numbering: orbits ordered by least pair index (== lexicographically least pair)
    roots = sorted({find(i) for i in range(len(pairs))})
    varno = {r: i + 1 for i, r in enumerate(roots)}
    var = {e: varno[find(pidx[e])] for e in pairs}
    # clauses: orbit representatives of 5-sets under the cyclic group <perm>
    seen5 = set()
    clauses = set()
    for S in combinations(range(n), 5):
        if S in seen5:
            continue
        T = S
        while True:
            seen5.add(T)
            T = tuple(sorted(perm[x] for x in T))
            if T == S:
                break
        M = tuple(sorted({var[e] for e in combinations(S, 2)}))
        clauses.add(M)
        clauses.add(tuple(-x for x in M))
    return len(roots), clauses

def read_dimacs(path):
    nv = nc = None
    cls = []
    with open(path) as fh:
        for line in fh:
            if line.startswith('c'):
                continue
            if line.startswith('p'):
                _, _, nv, nc = line.split(); nv, nc = int(nv), int(nc); continue
            lits = list(map(int, line.split()))
            assert lits[-1] == 0
            cls.append(lits[:-1])
    assert nc == len(cls)
    return nv, cls

def check_lrat(cls, path):
    """RUP-hint LRAT check. Returns True iff the empty clause is derived."""
    db = {i + 1: c for i, c in enumerate(cls)}
    opener = lzma.open if path.endswith('.xz') else open
    empty = False
    with opener(path, 'rt') as fh:
        for line in fh:
            parts = line.split()
            if not parts:
                continue
            cid = int(parts[0])
            if parts[1] == 'd':
                for t in parts[2:]:
                    t = int(t)
                    if t == 0:
                        break
                    db.pop(t, None)  # deletion of unknown id is harmless
                continue
            z = parts.index('0')
            lemma = [int(x) for x in parts[1:z]]
            hints = [int(x) for x in parts[z + 1:]]
            assert hints[-1] == 0
            hints = hints[:-1]
            assign = {-l for l in lemma}      # literals true under negation of lemma
            for l in lemma:
                if -l in assign and l in assign:
                    raise ValueError("tautological lemma")
            conflict = False
            for h in hints:
                if h < 0:
                    raise ValueError(f"RAT hint in lemma {cid}; only RUP supported")
                c = db[h]
                unassigned = [l for l in c if -l not in assign]
                if not unassigned:
                    conflict = True
                    break
                if len(unassigned) == 1:
                    if unassigned[0] in assign:
                        raise ValueError(f"hint {h} not unit in lemma {cid}")
                    assign.add(unassigned[0])
                else:
                    raise ValueError(f"hint {h} neither unit nor falsified in lemma {cid}")
            if not conflict:
                raise ValueError(f"no conflict for lemma {cid}")
            db[cid] = lemma
            if not lemma:
                empty = True
    return empty

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

if __name__ == '__main__':
    n, f, p, k = map(int, sys.argv[1:5])
    cnf, lrat = sys.argv[5], sys.argv[6]
    nv, want = build(n, f, p, k)
    nv2, cls = read_dimacs(cnf)
    got = {tuple(sorted(c, key=lambda x: (abs(x), x))) for c in cls}
    want = {tuple(sorted(c, key=lambda x: (abs(x), x))) for c in want}
    assert nv == nv2, (nv, nv2)
    assert len(cls) == len(got) == len(want), (len(cls), len(got), len(want))
    assert got == want, "clause set mismatch"
    print(f"type 1^{f} {p}^{k}: CNF reconstruction agrees ({nv} vars, {len(cls)} clauses), sha256 {sha256(cnf)}")
    ok = check_lrat(cls, lrat)
    print("LRAT proof:", "VERIFIED (empty clause derived)" if ok else "FAILED", sha256(lrat))
    sys.exit(0 if ok else 1)

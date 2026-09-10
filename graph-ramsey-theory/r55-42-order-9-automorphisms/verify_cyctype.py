"""Independent checker for the arbitrary-cycle-type orbit CNFs of cyctype.py.

Rebuilds the formula from the cycle type alone, by a different route than the
generator: union-find over pair indices rather than an orbit walk, and 5-set
orbit representatives found by explicit action of <sigma> rather than by
deduplicating on the set of pair orbits met. Checks that the regenerated clause
set equals the clause set of the DIMACS file exactly, then replays an LRAT
refutation of that file to the empty clause.

usage: python3 verify_cyctype.py file.cnf len,len,... [file.lrat]
"""
import sys, os, math, collections
from itertools import combinations
_HERE = os.path.dirname(os.path.abspath(__file__))
# read_dimacs/sha256 come from the prime-order artifact's checker and the tolerant
# LRAT replay from the order-3 one; both sit beside this directory in the published
# repository and one level up in the working tree.
for _p in (_HERE, os.path.join(_HERE, '..'),
           os.path.join(_HERE, '..', 'r55-42-prime-order-automorphisms'),
           os.path.join(_HERE, '..', 'r55-42-order3-cube-and-conquer'),
           os.path.join(_HERE, '..', 'r55-42-fixed-vertex-lex-leader')):
    if os.path.isdir(_p):
        sys.path.insert(0, _p)
from verify import read_dimacs, sha256
from verify_cnc_p import check_lrat

def regenerate(lengths):
    n = sum(lengths)
    perm = {}
    base = 0
    for L in lengths:
        for i in range(L):
            perm[base + i] = base + (i + 1) % L
        base += L
    assert sorted(perm.values()) == list(range(n)), 'not a permutation'
    pairs = list(combinations(range(n), 2))
    pidx = {e: i for i, e in enumerate(pairs)}
    parent = list(range(len(pairs)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for (u, v) in pairs:
        a, b = perm[u], perm[v]
        img = (a, b) if a < b else (b, a)
        ra, rb = find(pidx[(u, v)]), find(pidx[img])
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    roots = sorted({find(i) for i in range(len(pairs))})
    varno = {r: i + 1 for i, r in enumerate(roots)}
    var = {e: varno[find(pidx[e])] for e in pairs}
    seen5, clauses = set(), set()
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
        clauses.add(tuple(sorted(-x for x in M)))
    return len(roots), clauses

def check_cubes(cls, icnf, outd):
    """Check a plain case split: the cubes must be all 2^m sign patterns of m
    variables (so the split is exhaustive with no group argument at all), and
    every cube must carry a certificate refuting formula + cube.

    A certificate still on disk is replayed here; otherwise the cube is accepted
    by matching its literals against a replay already recorded in results.jsonl
    by the driver, which replays each proof at the moment it is produced and then
    deletes it. The two cases are counted separately.
    """
    import json, itertools
    cubes = [[int(t) for t in l.split()[1:-1]] for l in open(icnf) if l.startswith('a ')]
    varset = {abs(x) for c in cubes for x in c}
    m = len(varset)
    order = sorted(varset)
    want = {tuple(sorted(p, key=abs)) for p in
            itertools.product(*[(v, -v) for v in order])}
    got = {tuple(sorted(c, key=abs)) for c in cubes}
    print(f'cubes: {len(cubes)} in {icnf} over {m} variables {order}')
    if len(cubes) != len(got) or got != want:
        print(f'CUBE SET NOT EXHAUSTIVE: expected all {2 ** m} sign patterns, '
              f'{len(got)} distinct present, {len(want - got)} missing')
        return 1
    print(f'completeness: the {len(cubes)} cubes are exactly the {2 ** m} assignments '
          f'of {m} variables, so the split is a complete case distinction')
    recorded = {}
    rpath = os.path.join(outd, 'results.jsonl')
    if os.path.exists(rpath):
        for line in open(rpath):
            r = json.loads(line)
            if r['status'] == 'UNSAT-VERIFIED' and 'cube_lits' in r:
                recorded[tuple(sorted(r['cube_lits'], key=abs))] = r
    replayed = matched = 0
    for i, c in enumerate(cubes):
        path = os.path.join(outd, f'c{i}.lrat')
        if os.path.exists(path):
            if not check_lrat([list(x) for x in cls] + [[l] for l in c], path):
                print(f'cube {i}: REPLAY FAILED')
                return 1
            replayed += 1
        elif tuple(sorted(c, key=abs)) in recorded:
            matched += 1
        else:
            print(f'cube {i}: no certificate on disk and no recorded replay')
            return 1
    print(f'certificates: {replayed} replayed here, {matched} accepted from replays '
          f'recorded by the driver ({replayed + matched} of {len(cubes)})')
    print('RESULT: all checks passed')
    return 0

def main():
    cnf = sys.argv[1]
    lengths = [int(x) for x in sys.argv[2].split(',')]
    lrat = sys.argv[3] if len(sys.argv) > 3 else None
    nv, want = regenerate(lengths)
    ct = collections.Counter(lengths)
    order = math.lcm(*lengths)
    print('permutation on %d points: cycle type %s, order %d'
          % (sum(lengths), ' '.join(f'{L}^{c}' for L, c in sorted(ct.items())), order))
    _, cls = read_dimacs(cnf)
    got = {tuple(sorted(c)) for c in cls}
    print(f'cycle type {lengths}: {nv} orbit variables, {len(want)} clauses regenerated; '
          f'{cnf} has {len(cls)} clauses ({len(got)} distinct), sha256 {sha256(cnf)}')
    if got != want:
        print(f'MISMATCH: {len(want - got)} regenerated clauses absent from the file, '
              f'{len(got - want)} clauses in the file not regenerated')
        return 1
    print('formula: regenerated clause set matches the file exactly')
    if '--cubes' in sys.argv:
        return check_cubes(cls, sys.argv[sys.argv.index('--cubes') + 1],
                           sys.argv[sys.argv.index('--cubes') + 2])
    if lrat is None:
        print('RESULT: formula checked, no certificate given')
        return 0
    ok = check_lrat([list(c) for c in cls], lrat)
    print(f'certificate {lrat} ({os.path.getsize(lrat)} bytes, sha256 {sha256(lrat)}): '
          + ('replays to the empty clause' if ok else 'REPLAY FAILED'))
    print('RESULT: all checks passed' if ok else 'RESULT: FAILED')
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())

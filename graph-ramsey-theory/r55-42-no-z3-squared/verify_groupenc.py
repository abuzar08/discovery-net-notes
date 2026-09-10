"""Independent checker for the Z_3 x Z_3 orbit CNFs of groupenc.py.

Rebuilds everything from the orbit data (a; b_1..b_4; c) alone and by a different
route than the generator:

  * the action is built from an explicit list of point stabilisers rather than
    from coset blocks, and is then checked to be a faithful action of Z_3 x Z_3 --
    two commuting permutations of order 3 generating a group of order 9 with no
    non-identity element acting trivially;
  * the fixed-point count of every non-identity element is checked against
    a + 3 b_i, and against the bound FMAX passed on the command line, which is
    what licenses restricting attention to these actions at all;
  * pair orbits come from union-find over pair indices rather than a closure walk;
  * 5-set orbit representatives are found by explicit action of the group rather
    than by deduplicating on the set of pair orbits met.

Then the regenerated clause set is compared with the DIMACS file exactly, and the
LRAT certificate is replayed to the empty clause.

usage: python3 verify_groupenc.py file.cnf a b1,b2,b3,b4 c [file.lrat] [--fmax N]
"""
import sys, os
from itertools import combinations
_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (_HERE, os.path.join(_HERE, '..'),
           os.path.join(_HERE, '..', 'r55-42-prime-order-automorphisms'),
           os.path.join(_HERE, '..', 'r55-42-order3-cube-and-conquer'),
           os.path.join(_HERE, '..', 'r55-42-fixed-vertex-lex-leader')):
    if os.path.isdir(_p):
        sys.path.insert(0, _p)
from verify import read_dimacs, sha256
from verify_cnc_p import check_lrat

ELS = [(x, y) for x in range(3) for y in range(3)]
SUBGENS = [(1, 0), (0, 1), (1, 1), (1, 2)]

def add(u, v): return ((u[0] + v[0]) % 3, (u[1] + v[1]) % 3)
def sub(h): return frozenset([(0, 0), h, add(h, h)])

def action(a, b, c):
    """Points listed with their stabiliser; sigma and tau act by translation."""
    pts = []                                   # (block index, coset as frozenset)
    stab = []
    blk = 0
    for _ in range(a):
        pts.append((blk, frozenset(ELS))); stab.append(frozenset(ELS)); blk += 1
    for i, bi in enumerate(b):
        H = sub(SUBGENS[i])
        for _ in range(bi):
            for C in sorted({frozenset(add(g, h) for h in H) for g in ELS}, key=sorted):
                pts.append((blk, C)); stab.append(H)
            blk += 1
    for _ in range(c):
        for g in ELS:
            pts.append((blk, frozenset([g]))); stab.append(frozenset([(0, 0)]))
        blk += 1
    idx = {p: i for i, p in enumerate(pts)}
    def perm(g):
        return [idx[(bi, frozenset(add(g, x) for x in C))] for (bi, C) in pts]
    return len(pts), perm, stab

def group_of(n, gens):
    ident = tuple(range(n))
    G, frontier = {ident}, [ident]
    while frontier:
        p = frontier.pop()
        for q in gens:
            r = tuple(q[p[i]] for i in range(n))
            if r not in G:
                G.add(r); frontier.append(r)
    return G

def regenerate(a, b, c, fmax):
    n, perm, stab = action(a, b, c)
    if n != 42:
        return None, None, f'action has {n} points, not 42'
    sig, tau = perm((1, 0)), perm((0, 1))
    for p in (sig, tau):
        if sorted(p) != list(range(n)):
            return None, None, 'generator is not a permutation'
    comp = lambda p, q: [p[q[i]] for i in range(n)]
    ident = list(range(n))
    def power(p, k):
        r = ident
        for _ in range(k): r = comp(r, p)
        return r
    if power(sig, 3) != ident or power(tau, 3) != ident:
        return None, None, 'a generator does not have order dividing 3'
    if comp(sig, tau) != comp(tau, sig):
        return None, None, 'generators do not commute'
    G = group_of(n, [sig, tau])
    if len(G) != 9:
        return None, None, f'group has order {len(G)}, not 9'
    fixes = sorted(sum(1 for i in range(n) if p[i] == i) for p in G if list(p) != ident)
    if len(fixes) != 8 or max(fixes) >= n:
        return None, None, 'action is not faithful'
    want = sorted([a + 3 * x for x in b for _ in (0, 1)])
    if fixes != want:
        return None, None, f'fixed-point counts {fixes} do not match a+3b_i {want}'
    if max(fixes) > fmax:
        return None, None, f'an element fixes {max(fixes)} points, above the bound {fmax}'
    pairs = list(combinations(range(n), 2))
    pidx = {e: i for i, e in enumerate(pairs)}
    parent = list(range(len(pairs)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for (u, v) in pairs:
        for p in (sig, tau):
            i, j = p[u], p[v]
            ra, rb = find(pidx[(u, v)]), find(pidx[(min(i, j), max(i, j))])
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)
    roots = sorted({find(i) for i in range(len(pairs))})
    varno = {r: i + 1 for i, r in enumerate(roots)}
    var = {e: varno[find(pidx[e])] for e in pairs}
    seen5, clauses = set(), set()
    Gl = [list(p) for p in G]
    for S in combinations(range(n), 5):
        if S in seen5:
            continue
        for p in Gl:
            seen5.add(tuple(sorted(p[x] for x in S)))
        M = tuple(sorted({var[e] for e in combinations(S, 2)}))
        clauses.add(M)
        clauses.add(tuple(sorted(-x for x in M)))
    return len(roots), clauses, (fixes, len(G), sig, tau, var)

class VTot:
    """Totalizer, reimplemented here rather than imported, so that a transcription
    error in the generator shows up as a clause-set mismatch."""
    def __init__(self, nv):
        self.nv = nv
        self.cls = []

    def fresh(self):
        self.nv += 1
        return self.nv

    def unary(self, lits):
        m = len(lits)
        if m == 1:
            return list(lits)
        left = self.unary(lits[:m // 2])
        right = self.unary(lits[m // 2:])
        out = [self.fresh() for _ in range(len(left) + len(right))]
        A = [None] + left
        B = [None] + right
        for i in range(len(left) + 1):
            for j in range(len(right) + 1):
                if i + j >= 1:
                    self.cls.append([x for x in (-A[i] if i else None,
                                                 -B[j] if j else None,
                                                 out[i + j - 1]) if x is not None])
                if i + j < len(out):
                    self.cls.append([x for x in (-out[i + j],
                                                 A[i + 1] if i + 1 <= len(left) else None,
                                                 B[j + 1] if j + 1 <= len(right) else None)
                                     if x is not None])
        return out

def degree_clauses(sig, tau, var, nv, n=42, lo=17, hi=24):
    """The redundant degree window, regenerated.

    Every vertex of a (5,5,42)-graph has lo <= d(v) <= hi, because N(v) induces a
    (4,5)-graph and its complement a (5,4)-graph and R(4,5) = 25. The constraint
    excludes no solution, so the augmented formula has the same models as the plain
    one. Vertices in one orbit share a degree, so one totalizer per vertex orbit.
    """
    seen, reps = set(), []
    for v in range(n):
        if v in seen:
            continue
        orb, stack = set(), [v]
        while stack:
            x = stack.pop()
            if x in orb:
                continue
            orb.add(x)
            stack += [sig[x], tau[x]]
        seen |= orb
        reps.append(v)
    tot = VTot(nv)
    E = lambda u, w: var[(u, w) if u < w else (w, u)]
    for v in reps:
        outs = tot.unary([E(v, u) for u in range(n) if u != v])
        tot.cls.append([-outs[hi]])
        tot.cls.append([outs[lo - 1]])
    return reps, tot.cls, tot.nv


def main():
    cnf = sys.argv[1]
    a = int(sys.argv[2]); b = [int(x) for x in sys.argv[3].split(',')]; c = int(sys.argv[4])
    # positional argument after c is the certificate; skip flags and their values
    FLAGVAL = {'--fmax', '--cubes'}
    rest, i, argv = [], 5, sys.argv
    while i < len(argv):
        if argv[i].startswith('--'):
            i += 2 if argv[i] == '--fmax' else (3 if argv[i] == '--cubes' else 1)
            continue
        rest.append(argv[i]); i += 1
    lrat = rest[0] if rest else None
    fmax = int(sys.argv[sys.argv.index('--fmax') + 1]) if '--fmax' in sys.argv else 12
    nv, want, info = regenerate(a, b, c, fmax)
    if nv is None:
        print(f'ACTION REJECTED: {info}')
        return 1
    fixes, order, sig, tau, var = info
    print(f'action a={a} b={tuple(b)} c={c}: faithful Z_3 x Z_3 (group order {order}) on 42 points; '
          f'fixed points of the 8 non-identity elements {fixes}, all <= {fmax}')
    if '--degree' in sys.argv:
        reps, dcls, _ = degree_clauses(sig, tau, var, nv)
        want |= {tuple(sorted(cl)) for cl in dcls}
        print(f'degree window 17..24 on {len(reps)} vertex orbits: {len(dcls)} clauses '
              f'regenerated (redundant: satisfied by every (5,5,42)-graph, so the '
              f'augmented formula has the same models as the plain one)')
    _, cls = read_dimacs(cnf)
    got = {tuple(sorted(cl)) for cl in cls}
    print(f'{nv} orbit variables, {len(want)} clauses regenerated; {cnf} has {len(cls)} clauses '
          f'({len(got)} distinct), sha256 {sha256(cnf)}')
    if got != want:
        print(f'MISMATCH: {len(want - got)} regenerated clauses absent, {len(got - want)} unexpected')
        return 1
    print('formula: regenerated clause set matches the file exactly')
    if '--cubes' in sys.argv:
        # a plain case distinction on m Booleans, checked exhaustive by
        # verify_cyctype.check_cubes; no group argument enters the split
        from verify_cyctype import check_cubes
        return check_cubes(cls, sys.argv[sys.argv.index('--cubes') + 1],
                           sys.argv[sys.argv.index('--cubes') + 2])
    if lrat is None:
        print('RESULT: formula checked, no certificate given')
        return 0
    ok = check_lrat([list(x) for x in cls], lrat)
    print(f'certificate {lrat} ({os.path.getsize(lrat)} bytes, sha256 {sha256(lrat)}): '
          + ('replays to the empty clause' if ok else 'REPLAY FAILED'))
    print('RESULT: all checks passed' if ok else 'RESULT: FAILED')
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())

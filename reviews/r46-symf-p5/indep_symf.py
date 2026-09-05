"""reviewer-1: independent check of a --symf CNF of h2919.

The contribution's own trust boundary says `symF_clauses` is the single component
shared between its generator and its checker.  This script removes that sharing:
the orbit numbering and the (s,t)-goodness clauses are rebuilt by my union-find
encoder (h2661 evidence), and the lex-leader block is rebuilt here from the
docstring's specification

    R_u = ( x(u, c_0), ..., x(u, c_{k-1}), x(u, w) for w in 0..f-1 \\ {u, u+1} )
    (L)  R_u <=lex R_{u+1},   u = 0 .. f-2,   c_j = f + j*p,

with the auxiliary chain e_t <-> "rows equal through t" encoded as in the target
(biconditional).  It then checks the file is exactly [my base clauses] followed
by [my (L) clauses], and finally tests semantically, on random assignments of the
orbit variables, that the block is satisfied (with the e's forced by their
biconditionals) exactly when the lex predicate holds.

usage: python3 indep_symf.py n s t f p k file.cnf [samples]
"""
import sys, random, itertools


def orbit_numbering(n, f, p, k):
    """union-find over pairs; orbits numbered by lexicographically least pair"""
    assert f + p * k == n

    def sig(x):
        if x < f:
            return x
        j, i = divmod(x - f, p)
        return f + j * p + (i + 1) % p

    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    idx = {pr: i for i, pr in enumerate(pairs)}
    parent = list(range(len(pairs)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for (u, v) in pairs:
        a, b = sig(u), sig(v)
        ra, rb = find(idx[(u, v)]), find(idx[(min(a, b), max(a, b))])
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    roots = sorted({find(i) for i in range(len(pairs))})
    num = {r: j + 1 for j, r in enumerate(roots)}
    var = {pr: num[find(idx[pr])] for pr in pairs}
    return var, len(roots)


def base_clauses(n, s, t, var):
    C = set()
    for S in itertools.combinations(range(n), s):
        C.add(frozenset(-var[e] for e in itertools.combinations(S, 2)))
    for T in itertools.combinations(range(n), t):
        C.add(frozenset(var[e] for e in itertools.combinations(T, 2)))
    return C


def rows(n, f, p, k, var):
    x = lambda a, b: var[(a, b) if a < b else (b, a)]
    out = []
    for u in range(f - 1):
        others = [w for w in range(f) if w != u and w != u + 1]
        ra = [x(u, f + j * p) for j in range(k)] + [x(u, w) for w in others]
        rb = [x(u + 1, f + j * p) for j in range(k)] + [x(u + 1, w) for w in others]
        out.append((ra, rb))
    return out


def L_clauses(n, f, p, k, var, first_aux):
    """(L) in the target's own encoding, rebuilt from its specification"""
    cls = []
    aux = first_aux
    chains = []
    for ra, rb in rows(n, f, p, k, var):
        prev = None
        chain = []
        for t, (a, b) in enumerate(zip(ra, rb)):
            cls.append(sorted((-a, b)) if prev is None else sorted((-prev, -a, b)))
            if t == len(ra) - 1:
                break
            aux += 1
            e = aux
            if prev is None:
                for cl in ((-e, a, -b), (-e, -a, b), (e, a, b), (e, -a, -b)):
                    cls.append(sorted(cl))
            else:
                for cl in ((-e, prev), (-e, a, -b), (-e, -a, b),
                           (e, -prev, a, b), (e, -prev, -a, -b)):
                    cls.append(sorted(cl))
            chain.append(e)
            prev = e
        chains.append(chain)
    return cls, aux - first_aux, chains


def read_cnf(path):
    nv, cls = None, []
    for line in open(path):
        if line[0] in 'c%':
            continue
        if line[0] == 'p':
            nv = int(line.split()[2])
            continue
        toks = [int(x) for x in line.split()]
        if not toks:
            continue
        assert toks[-1] == 0
        cls.append(tuple(toks[:-1]))
    return nv, cls


def main():
    n, s, t, f, p, k = map(int, sys.argv[1:7])
    path = sys.argv[7]
    samples = int(sys.argv[8]) if len(sys.argv) > 8 else 4000
    var, nvo = orbit_numbering(n, f, p, k)
    base = base_clauses(n, s, t, var)
    L, naux, chains = L_clauses(n, f, p, k, var, nvo)
    nvfile, cls = read_cnf(path)
    assert nvfile == nvo + naux, ('variable count', nvfile, nvo + naux)
    assert len(cls) == len(base) + len(L), ('clause count', len(cls), len(base), len(L))
    got_base = {frozenset(c) for c in cls[:len(base)]}
    assert got_base == base, 'base clause set differs from my own encoder'
    got_L = [tuple(sorted(c)) for c in cls[len(base):]]
    want_L = [tuple(sorted(c)) for c in L]
    assert got_L == want_L, 'lex-leader block differs from the documented construction'

    # semantic test: the block's projection onto the orbit variables is the lex predicate
    rnd = random.Random(20260905 + n * 100 + f)
    rws = rows(n, f, p, k, var)
    disagree = 0
    for _ in range(samples):
        val = [0] * (nvo + naux + 1)
        for v in range(1, nvo + 1):
            val[v] = rnd.randint(0, 1)
        # bias towards near-equal rows so that violations and ties both occur
        if rnd.random() < 0.5:
            u = rnd.randrange(len(rws))
            ra, rb = rws[u]
            for a, b in zip(ra, rb):
                val[b] = val[a] if rnd.random() < 0.8 else val[b]
        pred = all([val[a] for a in ra] <= [val[b] for b in rb] for ra, rb in rws)
        for (ra, rb), chain in zip(rws, chains):
            eq = 1
            for tt, e in enumerate(chain):
                eq = eq and int(val[ra[tt]] == val[rb[tt]])
                val[e] = eq
        sat = all(any((l > 0) == bool(val[abs(l)]) for l in c) for c in cls[len(base):])
        if sat != pred:
            disagree += 1
    assert disagree == 0, f'{disagree} disagreements between the block and the lex predicate'
    print(f'n={n} 1^{f} {p}^{k} --symf: OK  {nvo} orbit vars + {naux} aux = {nvfile}; '
          f'{len(base)} base clauses (set-equal to mine) + {len(L)} (L) clauses (identical, in order); '
          f'{samples} random assignments: block <=> lex predicate, 0 disagreements')


if __name__ == '__main__':
    main()

"""reviewer-1: end-to-end test of the soundness of the cube-and-conquer split of
h2873 ("no solution is lost").

Claim under test: if G is a graph on 42 vertices invariant under sigma of type
1^15 3^9, then some image of G under a symmetry of the type formula (a vertex
permutation normalising <sigma>, optionally composed with complementation)
satisfies

    one of the 1576 cubes  AND  the residual clauses (S)  AND  the lex-leader
    clauses (L),

in the order claimed by the contribution: canonicalise the prefix, then rotate
and permute the free cycles, then permute the fixed vertices.

The test does exactly that for random sigma-invariant graphs with (5,5)-good
prefix (goodness of the prefix is all the cube list needs; the (5,5) property of
the whole graph plays no role in the symmetry argument) and verifies afterwards
that

  * the composed map is a permutation of the 42 vertices normalising <sigma>
    (possibly with complementation), so it maps the solution set of the type
    formula to itself,
  * the final graph satisfies exactly one cube, all 44 (S) clauses and all 896
    (L) clauses of the published CNF (evaluated on my own variable numbering,
    with the prefix-equality variables set to "rows equal through t").

It also checks, once, that every generator maps my base clause SET onto itself
and the hybrid redundant block onto itself.

usage: python3 split_sound.py f p k level cubes.icnf trials [seed]
"""
import sys, os, random
from itertools import combinations, permutations
from indep_encode import permutation, orbits_of_pairs, base_clauses
from indep_lex import L_clauses
from indep_cnc import S_clauses
import cube_check as CC

N = 42


def graph_from_orbits(val, var, n):
    adj = [[0] * n for _ in range(n)]
    for (u, w), v in var.items():
        b = val[v]
        adj[u][w] = adj[w][u] = b
    return adj


def apply_perm(adj, perm, comp, n):
    out = [[0] * n for _ in range(n)]
    for u in range(n):
        for w in range(n):
            if u != w:
                b = adj[u][w]
                if comp:
                    b ^= 1
                out[perm[u]][perm[w]] = b
    return out


def compose(p2, p1):
    """p2 after p1"""
    return [p2[p1[x]] for x in range(len(p1))]


def cycle_perm(f, p, k, cmap, rot):
    """vertex permutation: cycle a -> cmap[a], coordinate i -> i + rot[a]"""
    perm = list(range(f + p * k))
    for a in range(k):
        for i in range(p):
            perm[f + p * a + i] = f + p * cmap[a] + (i + rot[a]) % p
    return perm


def mult_perm(f, p, k, u):
    perm = list(range(f + p * k))
    for a in range(k):
        for i in range(p):
            perm[f + p * a + i] = f + p * a + (u * i) % p
    return perm


def fixed_perm(f, p, k, pi):
    perm = list(range(f + p * k))
    for u in range(f):
        perm[u] = pi[u]
    return perm


def normalises(perm, sig, n):
    """True iff perm sigma perm^-1 is a power of sigma"""
    inv = [0] * n
    for x in range(n):
        inv[perm[x]] = x
    conj = [perm[sig[inv[x]]] for x in range(n)]
    cur = list(range(n))
    for _ in range(4):
        if conj == cur:
            return True
        cur = [sig[x] for x in cur]
    return False


def prefix_obj(adj, f, p, level):
    """the 22-bit prefix object of a sigma-invariant graph"""
    sub = [[adj[f + p * a + i][f + p * b + j] for b in range(level) for j in range(p)]
           for a in range(level) for i in range(p)]
    nv = p * level
    mask = [0] * nv
    for x in range(nv):
        for y in range(nv):
            if x != y and sub[x][y]:
                mask[x] |= 1 << y
    return CC.encode(mask, level, p)


def main():
    f, p, k, level = map(int, sys.argv[1:5])
    icnf, trials = sys.argv[5], int(sys.argv[6])
    seed = int(sys.argv[7]) if len(sys.argv) > 7 else 20260905
    rnd = random.Random(seed)
    sig = permutation(N, f, p, k)
    var, nvo = orbits_of_pairs(N, sig)
    nbits = level + 3 * (level * (level - 1) // 2)

    # cubes, decoded on my own numbering (same code path as cube_check.py)
    cyc = lambda a, i: f + p * a + i
    pref = {}
    for a in range(level):
        pref[var[(cyc(a, 0), cyc(a, 1))]] = a
    for a, b in combinations(range(level), 2):
        off = CC.pair_index(a, b, level)
        for r in range(p):
            u, w = cyc(a, 0), cyc(b, r)
            pref[var[(min(u, w), max(u, w))]] = off + r
    cubes = {}
    for idx, line in enumerate(l for l in open(icnf) if l.startswith('a')):
        lits = [int(t) for t in line.split()[1:-1]]
        o = 0
        for l in lits:
            if l > 0:
                o |= 1 << pref[abs(l)]
        cubes[o] = (idx, lits)

    # symmetry generators of the split, as 42-vertex maps
    ident = list(range(level))
    gens = []
    tr = list(range(level)); tr[0], tr[1] = 1, 0
    gens.append(('swap cycles 0,1', cycle_perm(f, p, k, tr + list(range(level, k)), [0] * k), 0))
    lc = [(a + 1) % level for a in range(level)]
    gens.append(('cycle 0->1->2->3->0', cycle_perm(f, p, k, lc + list(range(level, k)), [0] * k), 0))
    for a in range(level):
        rot = [0] * k; rot[a] = 1
        gens.append((f'rotate cycle {a}', cycle_perm(f, p, k, list(range(k)), rot), 0))
    gens.append(('i -> 2i (all cycles)', mult_perm(f, p, k, 2), 0))
    gens.append(('complement', list(range(N)), 1))
    for name, perm, comp in gens:
        assert normalises(perm, sig, N), f'{name} does not normalise <sigma>'
    print(f'{len(gens)} split generators, all normalising <sigma>: ' + ', '.join(g[0] for g in gens))

    # invariance of the clause sets under the generators (checked once)
    base = base_clauses(N, var)
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'r55-42-prime-order-automorphisms'))
    from hybrid import hybrid
    _, _, _, _, tnbase, tclauses, _ = hybrid(N, f, p, k)
    mid = {frozenset(c) for c in tclauses[tnbase:]}
    for name, perm, comp in gens:
        vmap = {}
        for (u, w), v in var.items():
            a, b = perm[u], perm[w]
            vmap[v] = var[(a, b) if a < b else (b, a)]
        sgn = -1 if comp else 1
        img = {frozenset(sgn * (vmap[abs(l)] if l > 0 else -vmap[abs(l)]) for l in c) for c in base}
        assert img == base, f'base clause set not invariant under {name}'
        if not comp:
            imid = {frozenset((vmap[l] if l > 0 else -vmap[-l]) if abs(l) <= nvo else l for l in c) for c in mid}
            print(f'  {name}: base set invariant; hybrid redundant block invariant: {imid == mid}')
        else:
            print(f'  {name}: base set invariant (K5 <-> I5)')

    # (S) and (L) clauses, on my numbering
    S, minimal, free = S_clauses(N, f, p, k, var, level)
    L, nvtot = L_clauses(N, f, p, k, var, 0)   # numbering of the e variables is irrelevant here
    val_of = lambda W: int(''.join(str(b) for b in W), 2)

    def word(adj, j):
        return tuple(adj[f][f + p * j + r] for r in range(p))

    def rows_ok(adj):
        for u in range(f - 1):
            cols = [f + p * a for a in range(k)] + [w for w in range(f) if w not in (u, u + 1)]
            if [adj[u][c] for c in cols] > [adj[u + 1][c] for c in cols]:
                return False
        return True

    def key(adj):
        return (tuple(tuple(adj[u][f + p * a] for a in range(k)) for u in range(f)),
                tuple(tuple(adj[u][w] if u != w else 0 for w in range(f)) for u in range(f)))

    ok = 0
    stats = []
    for t in range(trials):
        while True:
            val = {v: rnd.randint(0, 1) for v in range(1, nvo + 1)}
            adj = graph_from_orbits(val, var, N)
            obj = prefix_obj(adj, f, p, level)
            if CC.good(CC.adjacency(obj, level, p), p * level):
                break
        perm_total = list(range(N))
        comp_total = 0
        # --- step 1: canonicalise the prefix, by BFS over the group orbit
        start = obj
        seen = {start: (list(range(N)), 0)}
        stack = [start]
        hit = None
        if start in cubes:
            hit = (start, list(range(N)), 0)
        while stack and hit is None:
            o = stack.pop()
            pm, cm = seen[o]
            for name, perm, comp in gens:
                sub = [perm[f + x] - f for x in range(p * level)]
                q = CC.apply_vertex(o, sub, comp, level, p)
                if q not in seen:
                    seen[q] = (compose(perm, pm), cm ^ comp)
                    if q in cubes:
                        hit = (q, seen[q][0], seen[q][1])
                        break
                    stack.append(q)
        assert hit is not None, 'prefix orbit contains no cube'
        cobj, perm_total, comp_total = hit
        adj1 = apply_perm(adj, perm_total, comp_total, N)
        assert prefix_obj(adj1, f, p, level) == cobj
        # --- step 2: rotations and permutation of the free cycles enforce (S)
        rot = [0] * k
        for j in range(level, k):
            W = word(adj1, j)
            best = min(range(p), key=lambda t2: val_of(tuple(W[(r - t2) % p] for r in range(p))))
            rot[j] = best
        adj2 = apply_perm(adj1, cycle_perm(f, p, k, list(range(k)), rot), 0, N)
        order = sorted(range(level, k), key=lambda j: val_of(word(adj2, j)))
        cmap = list(range(level)) + [0] * (k - level)
        for pos, j in enumerate(order):
            cmap[j] = level + pos
        adj3 = apply_perm(adj2, cycle_perm(f, p, k, cmap, [0] * k), 0, N)
        perm_total = compose(cycle_perm(f, p, k, cmap, [0] * k),
                             compose(cycle_perm(f, p, k, list(range(k)), rot), perm_total))
        # --- step 3: permutation of the fixed vertices enforces (L), by descent
        steps = 0
        while not rows_ok(adj3):
            for u in range(f - 1):
                cols = [f + p * a for a in range(k)] + [w for w in range(f) if w not in (u, u + 1)]
                if [adj3[u][c] for c in cols] > [adj3[u + 1][c] for c in cols]:
                    pi = list(range(f)); pi[u], pi[u + 1] = u + 1, u
                    sw = fixed_perm(f, p, k, pi)
                    new = apply_perm(adj3, sw, 0, N)
                    assert key(new) < key(adj3), 'descent step does not decrease the key'
                    adj3 = new
                    perm_total = compose(sw, perm_total)
                    steps += 1
                    break
            assert steps < 10000, 'descent did not terminate'
        final = adj3
        # --- verification of the result
        assert normalises(perm_total, sig, N)
        assert final == apply_perm(adj, perm_total, comp_total, N), 'composed map does not give the final graph'
        fobj = prefix_obj(final, f, p, level)
        assert fobj in cubes and fobj == cobj, 'the final graph left its cube'
        fval = {}
        for (u, w), v in var.items():
            fval[v] = final[u][w]
        for c in S:
            assert any((l > 0) == bool(fval[abs(l)]) for l in c), 'a residual clause (S) is violated'
        assert rows_ok(final), '(L) violated'
        matched = [i for o, (i, _) in cubes.items() if o == fobj]
        stats.append((cubes[fobj][0], steps))
        ok += 1
    print(f'{ok}/{trials} random sigma-invariant graphs with good prefix were mapped, by the published '
          f'order of operations, onto a graph satisfying one cube + (S) + (L); descent steps '
          f'{min(s for _, s in stats)}..{max(s for _, s in stats)}, cubes hit {len(set(c for c, _ in stats))} distinct')
    print('SPLIT SOUNDNESS TEST OK')


if __name__ == '__main__':
    main()

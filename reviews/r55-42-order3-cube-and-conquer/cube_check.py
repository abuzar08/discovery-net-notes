"""reviewer-1: independent check of the 1576 level-4 cubes of h2873.

A level-4 prefix (the induced graph on cycles 0..3 of a sigma-invariant graph of
type 1^15 3^9) is 22 bits: one per cycle for the within-cycle orbit (0 = empty,
1 = triangle) and three per unordered pair of cycles for the cross word.  The
script

  1. decodes the 1576 cubes of the .icnf with MY OWN orbit-variable numbering
     (indep_encode.py, h2543 evidence) and checks each cube fixes exactly the 22
     prefix variables;
  2. checks each decoded prefix is (5,5)-good (no K5, no independent 5-set) with
     my own clique search;
  3. builds the symmetry group (S_4 on cycles, Z_3 rotation of each cycle,
     coordinate multiplication by 2, complementation) as coordinate permutations
     of the 22 bits, each derived AND validated against the explicit action on
     the 12 vertices;
  4. computes the orbit of every cube by breadth-first search under those
     generators, checks the 1576 orbits are pairwise disjoint, and reports the
     total;
  5. enumerates all (5,5)-good labelled prefixes by depth-first search with
     pruning, and checks that this set is EXACTLY the union of the 1576 orbits.

(5) is stronger than the orbit-stabiliser count of the contribution: it shows the
cube set loses no prefix, without trusting either side's canonical form.

usage: python3 cube_check.py f p k level cubes.icnf
"""
import sys
from itertools import combinations
from indep_encode import permutation, orbits_of_pairs

N = 42


# ---------------------------------------------------------------- prefix codec
def pair_index(a, b, kk):
    """bit offset of the word W_ab inside the 22-bit prefix (a < b)"""
    idx = 0
    for bb in range(1, kk):
        for aa in range(bb):
            if (aa, bb) == (a, b):
                return kk + 3 * idx
            idx += 1
    raise KeyError


def adjacency(obj, kk, p=3):
    """adjacency bitmasks of the 3*kk vertices of the prefix"""
    nv = p * kk
    adj = [0] * nv
    v = lambda a, i: p * a + i % p
    for a in range(kk):
        if obj >> a & 1:
            for i, j in combinations(range(p), 2):
                adj[v(a, i)] |= 1 << v(a, j)
                adj[v(a, j)] |= 1 << v(a, i)
    for a, b in combinations(range(kk), 2):
        off = pair_index(a, b, kk)
        for r in range(p):
            if obj >> (off + r) & 1:
                for i in range(p):
                    adj[v(a, i)] |= 1 << v(b, i + r)
                    adj[v(b, i + r)] |= 1 << v(a, i)
    return adj


def encode(adj, kk, p=3):
    """inverse of adjacency (asserts the graph is sigma-invariant)"""
    v = lambda a, i: p * a + i % p
    obj = 0
    for a in range(kk):
        bits = {(adj[v(a, i)] >> v(a, j)) & 1 for i, j in combinations(range(p), 2)}
        assert len(bits) == 1, 'not sigma-invariant inside a cycle'
        obj |= bits.pop() << a
    for a, b in combinations(range(kk), 2):
        off = pair_index(a, b, kk)
        for r in range(p):
            bits = {(adj[v(a, i)] >> v(b, i + r)) & 1 for i in range(p)}
            assert len(bits) == 1, 'not sigma-invariant across cycles'
            obj |= bits.pop() << (off + r)
    return obj


# ------------------------------------------------------------ goodness (5,5)
def has_clique(adj, nv, size):
    """True iff the graph has a clique of the given size (bitmask search)"""
    full = (1 << nv) - 1

    def ext(cand, need):
        if need == 0:
            return True
        if bin(cand).count('1') < need:
            return False
        c = cand
        while c:
            b = c & -c
            c ^= b
            v = b.bit_length() - 1
            if ext(cand & adj[v] & ~((b << 1) - 1), need - 1):
                return True
            if bin(c).count('1') < need - 1:
                return False
        return False

    return ext(full, size)


def good(adj, nv):
    comp = [(~adj[v]) & ((1 << nv) - 1) & ~(1 << v) for v in range(nv)]
    return not has_clique(adj, nv, 5) and not has_clique(comp, nv, 5)


# ---------------------------------------------------------------------- group
def vertex_maps(kk, p=3):
    """generators as (permutation of the 3*kk vertices, complement flag)"""
    nv = p * kk
    v = lambda a, i: p * a + i % p
    gens = []
    def from_cycle_map(cmap, rot):
        perm = [0] * nv
        for a in range(kk):
            for i in range(p):
                perm[v(a, i)] = v(cmap[a], i + rot[a])
        return perm
    ident = list(range(kk))
    # S_kk generators: transposition (0 1) and the long cycle
    if kk >= 2:
        tr = list(range(kk)); tr[0], tr[1] = 1, 0
        gens.append((from_cycle_map(tr, [0] * kk), 0))
        lc = [(a + 1) % kk for a in range(kk)]
        gens.append((from_cycle_map(lc, [0] * kk), 0))
    # rotation of each cycle separately
    for a in range(kk):
        rot = [0] * kk; rot[a] = 1
        gens.append((from_cycle_map(ident, rot), 0))
    # i -> 2i in every cycle (normalises <sigma>, sends sigma to sigma^2)
    perm = [0] * nv
    for a in range(kk):
        for i in range(p):
            perm[v(a, i)] = v(a, 2 * i)
    gens.append((perm, 0))
    # complementation
    gens.append((list(range(nv)), 1))
    return gens


def apply_vertex(obj, perm, comp, kk, p=3):
    nv = p * kk
    adj = adjacency(obj, kk, p)
    new = [0] * nv
    for x in range(nv):
        for y in range(nv):
            if x != y and (adj[x] >> y) & 1:
                new[perm[x]] |= 1 << perm[y]
    if comp:
        new = [(~new[x]) & ((1 << nv) - 1) & ~(1 << x) for x in range(nv)]
    return encode(new, kk, p)


def bit_action(perm, comp, kk, nbits, p=3):
    """(coordinate permutation, xor mask) of a generator, derived and validated"""
    table = [None] * nbits
    for c in range(nbits):
        img = apply_vertex(1 << c, perm, 0, kk, p)
        assert bin(img).count('1') == 1, 'generator does not permute coordinates'
        table[c] = img.bit_length() - 1
    xor = (1 << nbits) - 1 if comp else 0
    return table, xor


def make_apply(table, xor, nbits):
    """fast application of a coordinate permutation via 8/8/6-bit lookup tables"""
    chunks = []
    lo = 0
    while lo < nbits:
        w = min(8, nbits - lo)
        tab = []
        for val in range(1 << w):
            out = 0
            for j in range(w):
                if val >> j & 1:
                    out |= 1 << table[lo + j]
            tab.append(out)
        chunks.append((lo, (1 << w) - 1, tab))
        lo += w

    def f(obj, chunks=chunks, xor=xor):
        out = 0
        for sh, msk, tab in chunks:
            out |= tab[(obj >> sh) & msk]
        return out ^ xor

    return f


# ----------------------------------------------------------------------- main
def main():
    f, p, k, level = map(int, sys.argv[1:5])
    icnf = sys.argv[5]
    kk = level
    nbits = kk + 3 * (kk * (kk - 1) // 2)
    sig = permutation(N, f, p, k)
    var, nv = orbits_of_pairs(N, sig)
    # my numbering of the 22 prefix variables
    cyc = lambda a, i: f + p * a + i
    pref = {}
    for a in range(kk):
        pref[var[(cyc(a, 0), cyc(a, 1))]] = a
    for a, b in combinations(range(kk), 2):
        off = pair_index(a, b, kk)
        for r in range(p):
            u, w = cyc(a, 0), cyc(b, r)
            pref[var[(min(u, w), max(u, w))]] = off + r
    assert len(pref) == nbits, ('prefix variables collide', len(pref))

    cubes = []
    for line in open(icnf):
        if not line.startswith('a'):
            continue
        lits = [int(t) for t in line.split()[1:-1]]
        assert len(lits) == nbits and {abs(l) for l in lits} == set(pref), 'cube does not fix exactly the prefix'
        obj = 0
        for l in lits:
            if l > 0:
                obj |= 1 << pref[abs(l)]
        cubes.append(obj)
    print(f'{len(cubes)} cubes decoded on my own orbit numbering; each fixes exactly the {nbits} prefix variables')
    assert len(set(cubes)) == len(cubes), 'duplicate cubes'

    nvtx = p * kk
    bad = [i for i, o in enumerate(cubes) if not good(adjacency(o, kk, p), nvtx)]
    print(f'goodness (no K5, no I5 on {nvtx} vertices): {len(cubes) - len(bad)}/{len(cubes)} good'
          + (f'  BAD {bad[:5]}' if bad else ''))
    assert not bad

    gens = vertex_maps(kk, p)
    acts = []
    for perm, comp in gens:
        table, xor = bit_action(perm, comp, kk, nbits, p)
        fun = make_apply(table, xor, nbits)
        # validate the fast action against the explicit vertex action
        for t in range(64):
            o = (t * 2654435761) & ((1 << nbits) - 1)
            assert fun(o) == apply_vertex(o, perm, comp, kk, p), 'bit action disagrees with vertex action'
        acts.append(fun)
    print(f'{len(acts)} generators: coordinate action derived and validated against the explicit '
          f'vertex action on {nvtx} vertices')

    seen = {}
    sizes = []
    for i, c in enumerate(cubes):
        if c in seen:
            raise AssertionError(f'cube {i} lies in the orbit of cube {seen[c]}')
        orb = {c}
        stack = [c]
        while stack:
            o = stack.pop()
            for a in acts:
                q = a(o)
                if q not in orb:
                    orb.add(q)
                    stack.append(q)
        for o in orb:
            if o in seen:
                raise AssertionError(f'orbit of cube {i} meets the orbit of cube {seen[o]}')
            seen[o] = i
        sizes.append(len(orb))
    print(f'orbits: pairwise disjoint, sizes {min(sizes)}..{max(sizes)}, total {sum(sizes)} labelled prefixes')
    assert all(o == 0 or 7776 % o == 0 for o in sizes)

    # exhaustive enumeration of good labelled prefixes, with pruning
    total = 0
    goodset = set()

    def dfs(a, obj):
        nonlocal total
        if a == kk:
            total += 1
            goodset.add(obj)
            return
        for code in range(2):
            for wbits in range(1 << (3 * a)):
                o = obj | (code << a)
                if a:
                    o |= wbits << pair_index(0, a, kk)
                if good(adjacency_partial(o, a + 1, kk, p), p * (a + 1)):
                    dfs(a + 1, o)

    def adjacency_partial(obj, m, kk, p):
        """adjacency of the induced graph on the first m cycles"""
        nvp = p * m
        adj = [0] * nvp
        v = lambda a, i: p * a + i % p
        for a in range(m):
            if obj >> a & 1:
                for i, j in combinations(range(p), 2):
                    adj[v(a, i)] |= 1 << v(a, j)
                    adj[v(a, j)] |= 1 << v(a, i)
        for a, b in combinations(range(m), 2):
            off = pair_index(a, b, kk)
            for r in range(p):
                if obj >> (off + r) & 1:
                    for i in range(p):
                        adj[v(a, i)] |= 1 << v(b, i + r)
                        adj[v(b, i + r)] |= 1 << v(a, i)
        return adj

    dfs(0, 0)
    print(f'exhaustive enumeration: {total} (5,5)-good labelled prefixes out of '
          f'{2 ** kk * 8 ** (kk * (kk - 1) // 2)}')
    assert goodset == set(seen), ('union of the cube orbits is not the set of good prefixes',
                                  len(goodset), len(seen), len(goodset - set(seen)), len(set(seen) - goodset))
    print('COMPLETENESS OK: the union of the 1576 orbits is exactly the set of good labelled prefixes')


if __name__ == '__main__':
    main()

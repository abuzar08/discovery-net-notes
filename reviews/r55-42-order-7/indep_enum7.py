r"""reviewer-1: independent check of the orderly enumeration of h2621 — the one
step the contribution flags as program-trusted rather than certificate-checked.

A level-\(L\) object is a \(\mathbb{Z}_7\)-graph on \(L\) cycles: three bits per
cycle for its internal code (distances 1, 2, 3) and seven bits per unordered pair
of cycles for the cross word. So level 2 has \(2^{13} = 8192\) labelled objects
and level 3 has \(2^{30}\).

  * **Level 2, exactly.** Enumerate all 8192 labelled objects, keep the
    \((5,5)\)-good ones, partition them into orbits under my own implementation of
    the group (cycle permutations, the multiplier \(u \in \mathbb{Z}_7^{*}\),
    independent rotations, complementation), and compare the orbit count and the
    orbit representatives with `level2.json`.
  * **Level 3, by sampling.** Draw random labelled good objects, compute the orbit
    of each under the same generators, and check that it meets the published
    representative list exactly once.

usage: python3 indep_enum7.py [samples]
"""
import sys, os, json, random, itertools
P = 7
HALF = (P - 1) // 2


def pair_index(a, b, L):
    idx = 0
    for bb in range(1, L):
        for aa in range(bb):
            if (aa, bb) == (a, b):
                return L * HALF + P * idx
            idx += 1
    raise KeyError


def adjacency(obj, L):
    """adjacency bitmasks of the P*L vertices"""
    nv = P * L
    adj = [0] * nv
    v = lambda a, i: P * a + i % P
    for a in range(L):
        code = (obj >> (a * HALF)) & ((1 << HALF) - 1)
        for d in range(1, HALF + 1):
            if code >> (d - 1) & 1:
                for i in range(P):
                    adj[v(a, i)] |= 1 << v(a, i + d)
                    adj[v(a, i + d)] |= 1 << v(a, i)
    for a, b in itertools.combinations(range(L), 2):
        off = pair_index(a, b, L)
        for r in range(P):
            if obj >> (off + r) & 1:
                for i in range(P):
                    adj[v(a, i)] |= 1 << v(b, i + r)
                    adj[v(b, i + r)] |= 1 << v(a, i)
    return adj


def encode(adj, L):
    v = lambda a, i: P * a + i % P
    obj = 0
    for a in range(L):
        for d in range(1, HALF + 1):
            bits = {(adj[v(a, i)] >> v(a, i + d)) & 1 for i in range(P)}
            assert len(bits) == 1, 'not sigma-invariant inside a cycle'
            obj |= bits.pop() << (a * HALF + d - 1)
    for a, b in itertools.combinations(range(L), 2):
        off = pair_index(a, b, L)
        for r in range(P):
            bits = {(adj[v(a, i)] >> v(b, i + r)) & 1 for i in range(P)}
            assert len(bits) == 1, 'not sigma-invariant across cycles'
            obj |= bits.pop() << (off + r)
    return obj


def has_clique(adj, nv, size):
    def ext(cand, need):
        if need == 0:
            return True
        if bin(cand).count('1') < need:
            return False
        c = cand
        while c:
            b = c & -c
            c ^= b
            u = b.bit_length() - 1
            if ext(cand & adj[u] & ~((b << 1) - 1), need - 1):
                return True
            if bin(c).count('1') < need - 1:
                return False
        return False
    return ext((1 << nv) - 1, size)


def good(adj, nv):
    comp = [(~adj[u]) & ((1 << nv) - 1) & ~(1 << u) for u in range(nv)]
    return not has_clique(adj, nv, 5) and not has_clique(comp, nv, 5)


def generators(L):
    """(vertex permutation, complement flag) generators of the group"""
    nv = P * L
    v = lambda a, i: P * a + i % P
    gens = []

    def from_map(cmap, rot, mult=1):
        perm = [0] * nv
        for a in range(L):
            for i in range(P):
                perm[v(a, i)] = v(cmap[a], mult * i + rot[a])
        return perm

    ident = list(range(L))
    if L >= 2:
        tr = list(range(L)); tr[0], tr[1] = 1, 0
        gens.append((from_map(tr, [0] * L), 0))
        lc = [(a + 1) % L for a in range(L)]
        gens.append((from_map(lc, [0] * L), 0))
    for a in range(L):
        rot = [0] * L; rot[a] = 1
        gens.append((from_map(ident, rot), 0))
    gens.append((from_map(ident, [0] * L, mult=3), 0))      # 3 generates Z_7^*
    gens.append((list(range(nv)), 1))                        # complementation
    return gens


def act(obj, perm, comp, L):
    adj = adjacency(obj, L)
    nv = P * L
    new = [0] * nv
    for x in range(nv):
        for y in range(nv):
            if x != y and (adj[x] >> y) & 1:
                new[perm[x]] |= 1 << perm[y]
    if comp:
        new = [(~new[x]) & ((1 << nv) - 1) & ~(1 << x) for x in range(nv)]
    return encode(new, L)


def orbit(obj, gens, L):
    seen = {obj}
    stack = [obj]
    while stack:
        o = stack.pop()
        for perm, comp in gens:
            q = act(o, perm, comp, L)
            if q not in seen:
                seen.add(q)
                stack.append(q)
    return seen


def reps_from_json(path, L):
    """the published representatives, as objects in my own bit layout"""
    data = json.load(open(path))
    out = []
    for key in data:
        codes, wl = key
        obj = 0
        for a, s in enumerate(codes):
            obj |= s << (a * HALF)
        idx = 0
        for b in range(1, L):
            for a in range(b):
                obj |= wl[idx] << pair_index(a, b, L)
                idx += 1
        out.append(obj)
    return out


def main():
    nsample = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'target')

    # ---------------- level 2, exhaustively
    L = 2
    gens = generators(L)
    nv = P * L
    goods = [o for o in range(1 << (L * HALF + P * (L * (L - 1) // 2)))
             if good(adjacency(o, L), nv)]
    seen, orbits = set(), []
    for o in goods:
        if o in seen:
            continue
        orb = orbit(o, gens, L)
        seen |= orb
        orbits.append(min(orb))
    print(f'level 2: {1 << 13} labelled objects, {len(goods)} of them (5,5)-good, '
          f'{len(orbits)} orbits under my group')
    pub = reps_from_json(os.path.join(d, 'level2.json'), L)
    print(f'   published level2.json: {len(pub)} representatives; '
          f'each lies in a distinct one of my orbits: '
          f'{len({min(orbit(o, gens, L)) for o in pub}) == len(pub) == len(orbits)}')
    assert all(good(adjacency(o, L), nv) for o in pub)

    # ---------------- level 3, sampled
    L = 3
    gens3 = generators(L)
    nv3 = P * L
    bits = L * HALF + P * (L * (L - 1) // 2)
    pub3 = reps_from_json(os.path.join(d, 'level3.json'), L)
    print(f'\nlevel 3: published list has {len(pub3)} representatives; '
          f'{bits}-bit objects, {1 << bits} labelled in total')
    canon3 = {}
    for o in pub3:
        assert good(adjacency(o, L), nv3), 'a published representative is not good'
    rnd = random.Random(20260906)
    hits = miss = 0
    pubset = set(pub3)
    for _ in range(nsample):
        while True:
            o = rnd.getrandbits(bits)
            if good(adjacency(o, L), nv3):
                break
        orb = orbit(o, gens3, L)
        inter = orb & pubset
        if len(inter) == 1:
            hits += 1
        else:
            miss += 1
            print(f'   sample {o}: meets the representative list {len(inter)} times')
    print(f'   {nsample} random good labelled objects: {hits} met the list exactly once, {miss} did not')


if __name__ == '__main__':
    main()

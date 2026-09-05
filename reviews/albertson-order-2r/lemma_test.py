"""reviewer-1: computational test of the non-domination lemma of h2933.

Lemma (h2933).  Let H have 2r vertices, theta(H) = r, and Stehlik's property
(for every vertex x, H - x has a clique cover into r-1 parts, each of size >= 2;
at 2r-1 vertices that means one triangle and r-2 edges).  Then for every vertex w
no a in N_H(w) is adjacent to every other vertex of N_H(w).

Two independent tests:

  A (conclusion).  Over all graphs H on 2r vertices satisfying the hypotheses
    -- exhaustively for r = 3, by random search for r = 4 -- check that no
    (w, a) with a dominating N_H(w)\\{a} exists.

  B (proof mechanics).  Drop theta(H) = r.  For any H on 2r vertices, any cover
    of H - a into one triangle and r-2 edges, and any w with a in N_H(w)
    dominating N_H(w)\\{a}, build the cover the proof constructs (swap the part
    containing w for that part plus a, or absorb a into the triangle) and check
    it really is a clique cover of ALL 2r vertices with r-1 parts -- i.e. that
    the proof's conclusion theta(H) <= r-1 is valid.  This tests the step that
    the lemma's contradiction rests on, on many more graphs than test A reaches.

usage: python3 lemma_test.py r trials [seed]
"""
import sys, random, itertools


def nbrs(adj, v):
    return adj[v]


def clique_cover_parts(adj, verts, k, minsize):
    """a clique cover of `verts` into exactly k cliques each of size >= minsize,
    or None (backtracking; verts is small)"""
    verts = list(verts)
    n = len(verts)
    if n < k * minsize:
        return None
    best = None

    def ok_clique(part):
        return all(v in adj[u] for u, v in itertools.combinations(part, 2))

    def rec(rem, parts):
        nonlocal best
        if best is not None:
            return
        if not rem:
            if len(parts) == k and all(len(p) >= minsize for p in parts):
                best = [list(p) for p in parts]
            return
        if len(parts) == k:
            return
        v = rem[0]
        others = rem[1:]
        # every part containing v: v together with a subset of its neighbours in rem
        cand = [u for u in others if u in adj[v]]
        maxsz = min(len(rem) - (k - len(parts) - 1) * minsize, len(cand) + 1)
        for size in range(min(maxsz, len(cand) + 1), minsize - 1, -1):
            for sub in itertools.combinations(cand, size - 1):
                part = (v,) + sub
                if ok_clique(part):
                    left = [u for u in others if u not in sub]
                    if len(left) >= (k - len(parts) - 1) * minsize:
                        rec(left, parts + [part])
                        if best is not None:
                            return
    rec(verts, [])
    return best


def theta(adj, verts):
    """clique cover number of H[verts] (small graphs only)"""
    verts = list(verts)
    for k in range(1, len(verts) + 1):
        if clique_cover_parts(adj, verts, k, 1) is not None:
            return k
    return len(verts)


def stehlik_covers(adj, n, r):
    """for every x, a cover of H - x into r-1 parts of size >= 2; returns
    {x: cover} or None if some x has none"""
    out = {}
    for x in range(n):
        c = clique_cover_parts(adj, [v for v in range(n) if v != x], r - 1, 2)
        if c is None:
            return None
        out[x] = c
    return out


def dominating_pairs(adj, n):
    for w in range(n):
        N = sorted(adj[w])
        for a in N:
            if all(u in adj[a] for u in N if u != a):
                yield w, a


def graph_from_bits(bits, n):
    adj = [set() for _ in range(n)]
    i = 0
    for u, v in itertools.combinations(range(n), 2):
        if bits >> i & 1:
            adj[u].add(v)
            adj[v].add(u)
        i += 1
    return adj


def sample_bits(n, r, rnd):
    """random H on n vertices with 2 <= d_H(v) <= r — the degree window forced by
    delta(G) >= r-1 and the lemma's own consequence delta(H) >= 2"""
    pairs = list(itertools.combinations(range(n), 2))
    while True:
        deg = [0] * n
        bits = 0
        order = pairs[:]
        rnd.shuffle(order)
        for i, (u, v) in enumerate(order):
            if deg[u] < r and deg[v] < r and rnd.random() < 0.5:
                deg[u] += 1
                deg[v] += 1
                bits |= 1 << pairs.index((u, v))
        if all(2 <= d <= r for d in deg):
            return bits


def test_A(r, trials, rnd):
    n = 2 * r
    npairs = n * (n - 1) // 2
    seen = viol = 0
    src = range(1 << npairs) if npairs <= 16 else (sample_bits(n, r, rnd) for _ in range(trials))
    for bits in src:
        adj = graph_from_bits(bits, n)
        if any(len(adj[v]) == 0 for v in range(n)):
            continue
        if theta(adj, range(n)) != r:
            continue
        if stehlik_covers(adj, n, r) is None:
            continue
        seen += 1
        for w, a in dominating_pairs(adj, n):
            viol += 1
            print(f'  VIOLATION: bits={bits} w={w} a={a} N(w)={sorted(adj[w])}')
    return seen, viol


def test_B(r, trials, rnd):
    """proof mechanics, without assuming theta(H) = r"""
    n = 2 * r
    npairs = n * (n - 1) // 2
    checked = bad = 0
    for _ in range(trials):
        bits = rnd.getrandbits(npairs)
        adj = graph_from_bits(bits, n)
        for w, a in dominating_pairs(adj, n):
            cov = clique_cover_parts(adj, [v for v in range(n) if v != a], r - 1, 2)
            if cov is None:
                continue
            part = next(p for p in cov if w in p)
            rest = [p for p in cov if w not in p]
            if len(part) == 2:
                # {w,u} -> {w,u,a}: needs a triangle part elsewhere to stay r-1 parts
                new = [list(part) + [a]] + [list(p) for p in rest]
            else:
                new = [list(part) + [a]] + [list(p) for p in rest]
            checked += 1
            flat = sorted(v for p in new for v in p)
            okparts = all(all(y in adj[x] for x, y in itertools.combinations(p, 2)) for p in new)
            if flat != list(range(n)) or len(new) != r - 1 or not okparts:
                bad += 1
                print(f'  PROOF STEP FAILS: bits={bits} w={w} a={a} parts={new}')
    return checked, bad


def main():
    r = int(sys.argv[1])
    trials = int(sys.argv[2])
    rnd = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 20260905)
    n = 2 * r
    seen, viol = test_A(r, trials, rnd)
    how = 'all graphs' if n * (n - 1) // 2 <= 16 else f'{trials} random graphs'
    print(f'A  r={r}, n={n}: {how}; {seen} satisfy theta(H)=r and Stehlik\'s property; '
          f'{viol} violations of non-domination')
    checked, bad = test_B(r, trials, rnd)
    print(f'B  r={r}, n={n}: {checked} (H, w, a, cover) instances with a dominating N(w); '
          f'the proof\'s swapped cover is a valid clique cover of all {n} vertices into r-1={r-1} '
          f'parts in {checked - bad} of them, {bad} failures')


if __name__ == '__main__':
    main()

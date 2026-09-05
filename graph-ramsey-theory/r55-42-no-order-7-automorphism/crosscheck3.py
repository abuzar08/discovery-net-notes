"""Independent cross-check of level3.json: sample random labelled Z_7-graphs on 3
cycles, keep the (5,5)-good ones (checked by brute force over all 5-sets, not the
incremental test), compute their canonical form by brute force over the whole
group (complement x multiplier x S_3 x rotations, 3528 elements) and check that
it is in the rep set and equals z7enum.canon.   usage: python3 crosscheck3.py N seed"""
import sys, json, random, itertools
from z7enum import build, canon, code_adj, CODES, P, FULL, rot, mul, neg, code_mul
N, seed = int(sys.argv[1]), int(sys.argv[2]); random.seed(seed)
reps = {(tuple(k[0]), tuple(k[1])) for k in json.load(open('level3.json'))}
def good_bruteforce(adj, n):
    for S in itertools.combinations(range(n), 5):
        m = 0
        for a, b in itertools.combinations(S, 2):
            m += (adj[a] >> b) & 1
        if m == 0 or m == 10: return False
    return True
def transform(codes, words, c, u, perm, ts):
    """apply complement c, multiplier u, cycle permutation (new a = old perm[a]), rotations ts."""
    k = len(codes)
    cd = [code_mul(s, u) for s in codes]; wd = {jl: mul(W, u) for jl, W in words.items()}
    if c: cd = [7 - s for s in cd]; wd = {jl: FULL ^ W for jl, W in wd.items()}
    ncodes = tuple(cd[perm[a]] for a in range(k)); out = []
    for b in range(1, k):
        for a in range(b):
            ja, jb = perm[a], perm[b]
            W = wd[(ja, jb)] if ja < jb else neg(wd[(jb, ja)])
            out.append(rot(W, ts[b] - ts[a]))
    return (ncodes, tuple(out))
def brute_canon(codes, words):
    best = None
    for c in (0, 1):
        for u in range(1, P):
            for perm in itertools.permutations(range(3)):
                for t1 in range(P):
                    for t2 in range(P):
                        key = transform(codes, words, c, u, perm, (0, t1, t2))
                        if best is None or key < best: best = key
    return best
tested = 0; tries = 0
while tested < N:
    tries += 1
    codes = [random.choice(CODES) for _ in range(3)]
    words = {(0, 1): random.randrange(128), (0, 2): random.randrange(128), (1, 2): random.randrange(128)}
    adj = build(codes, words)
    if not good_bruteforce(adj, 21): continue
    bc = brute_canon(codes, words); gc = canon(codes, words)
    assert bc == gc, (codes, words, bc, gc)
    assert bc in reps, (codes, words, bc)
    # the canonical graph must itself be good and canonical (idempotence)
    tested += 1
    if tested % 100 == 0: print(tested, 'ok of', tries, 'samples', flush=True)
print(f'{tested} random good labelled 3-cycle graphs ({tries} samples): brute-force canonical form == greedy canon, all in level3.json ({len(reps)} reps)')
if '--fixpoints' in sys.argv:
    from z7enum import unkey, good_new_cycle
    bad = 0
    for key in reps:
        codes, words = unkey(key)
        adj = build(codes, words)
        if canon(codes, words) != key or not good_bruteforce(adj, 21): bad += 1
    print(f'fixpoint/goodness check of all {len(reps)} reps: {bad} failures')

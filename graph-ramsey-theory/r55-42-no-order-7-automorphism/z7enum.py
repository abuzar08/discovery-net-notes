"""Orderly enumeration of Z_7-invariant (5,5)-good graphs on k cycles of length 7
(cycle type 7^k), up to the equivariant symmetry group
  S_k (permute cycles) x Z_7^* (multiplier) x Z_7^k (rotations) x complement.
A graph is given by codes s_j in {1..6} (subset of {1,2,3}, nonempty, proper)
and words W_jl in [0,128) (subset of Z_7) for j<l: (j,i)~(l,i') iff i'-i in W_jl.
usage: python3 enum.py K  [prints counts per level, writes z7/level{k}.json]"""
import sys, json, itertools, time
P = 7
CODES = [s for s in range(8) if s not in (0, 7)]  # subsets of {1,2,3}: bit d-1 <-> distance d
FULL = 127
def code_adj(s):  # set of residues r in Z_7 with (j,i)~(j,i+r)
    return {d for d in (1, 2, 3) if s >> (d - 1) & 1} | {P - d for d in (1, 2, 3) if s >> (d - 1) & 1}
def rot(W, t):  # W + t
    return sum(1 << ((r + t) % P) for r in range(P) if W >> r & 1)
def mul(W, u):
    return sum(1 << ((r * u) % P) for r in range(P) if W >> r & 1)
def neg(W):
    return mul(W, P - 1)
def code_mul(s, u):
    A = code_adj(s); B = {(a * u) % P for a in A}
    return sum(1 << (d - 1) for d in (1, 2, 3) if d in B)
def popcount(x): return bin(x).count('1')

def build(codes, words):
    """adjacency bitmasks for k cycles; words[(j,l)] for j<l."""
    k = len(codes); n = P * k; adj = [0] * n
    for j, s in enumerate(codes):
        A = code_adj(s)
        for i in range(P):
            for r in A: adj[P * j + i] |= 1 << (P * j + (i + r) % P)
    for (j, l), W in words.items():
        for i in range(P):
            for r in range(P):
                if W >> r & 1:
                    a, b = P * j + i, P * l + (i + r) % P
                    adj[a] |= 1 << b; adj[b] |= 1 << a
    return adj

def has_clique(adj, cand, size):
    """is there a clique of `size` vertices inside vertex set `cand` (bitmask)?"""
    if size == 0: return True
    if popcount(cand) < size: return False
    if size == 1: return cand != 0
    while cand:
        v = cand & -cand; vi = v.bit_length() - 1
        cand ^= v
        if has_clique(adj, cand & adj[vi], size - 1): return True
        if popcount(cand) < size: return False
    return False

def good_new_cycle(adj, k):
    """(5,5)-goodness of all 5-sets meeting the new cycle k-1 (by Z_7 symmetry only
    those through vertex v0 = 7(k-1)); assumes the first k-1 cycles are good."""
    n = P * k; v0 = P * (k - 1); allv = (1 << n) - 1
    N = adj[v0]; Nc = allv & ~N & ~(1 << v0)
    if has_clique(adj, N, 4): return False
    cadj = [allv & ~a & ~(1 << i) for i, a in enumerate(adj)]
    if has_clique(cadj, Nc, 4): return False
    return True

def canon(codes, words):
    """lexicographically least (codes, words-tuple) over the group. Returns tuple key."""
    k = len(codes); best = None
    for c in (0, 1):
        for u in range(1, P):
            cd = [code_mul(s, u) for s in codes]
            wd = {jl: mul(W, u) for jl, W in words.items()}
            if c:
                cd = [7 - s for s in cd]; wd = {jl: FULL ^ W for jl, W in wd.items()}
            for perm in itertools.permutations(range(k)):
                # new cycle a = old cycle perm[a]
                ncodes = tuple(cd[perm[a]] for a in range(k))
                if best is not None and ncodes > best[0]: continue
                def w(a, b):  # word from new a to new b (a<b)
                    ja, jb = perm[a], perm[b]
                    return wd[(ja, jb)] if ja < jb else neg(wd[(jb, ja)])
                # rotations: t_0 = 0; choose t_b to minimise w(0,b)+t_b; branch on ties (trivial words)
                def rec(b, ts, acc):
                    nonlocal best
                    if b == k:
                        key = (ncodes, tuple(acc))
                        if best is None or key < best: best = key
                        return
                    W0 = w(0, b)
                    opts = [0] if W0 in (0, FULL) else [min(range(P), key=lambda t: rot(W0, t))]
                    if W0 in (0, FULL): opts = list(range(P))
                    for t in opts:
                        nts = ts + [t]
                        # words (a,b) for a<b, with rotation: W_ab -> W_ab - t_a + t_b
                        new = [rot(w(a, b), nts[b] - nts[a]) for a in range(b)]
                        cand = acc + new
                        # prune: compare prefix with best
                        if best is not None and (ncodes, tuple(cand)) > (best[0], best[1][:len(cand)]) and ncodes == best[0]:
                            if tuple(cand) > best[1][:len(cand)]: continue
                        rec(b + 1, nts, cand)
                rec(1, [0], [])
    return best

def unkey(key):
    codes, wl = key; k = len(codes); words = {}; idx = 0
    for b in range(1, k):
        for a in range(b):
            words[(a, b)] = wl[idx]; idx += 1
    return list(codes), words

def pair_allowed():
    """allowed words for each ordered code pair (s_j, s_l): 14-vertex graph (5,5)-good."""
    allowed = {}
    for s in CODES:
        for t in CODES:
            ok = []
            for W in range(128):
                adj = build([s, t], {(0, 1): W})
                if good_new_cycle(adj, 2): ok.append(W)
            allowed[(s, t)] = ok
    return allowed

def main():
    K = int(sys.argv[1])
    t0 = time.time()
    allowed = pair_allowed()
    print('pair-allowed sizes:', sorted({(s, t): len(v) for (s, t), v in allowed.items()}.items())[:6], '...', flush=True)
    # level 1
    reps = {canon([s], {}) for s in CODES}
    print(f'level 1: {len(reps)} reps', flush=True)
    for k in range(2, K + 1):
        new = set(); tried = 0
        for key in sorted(reps):
            codes, words = unkey(key)
            for s in CODES:
                lists = [allowed[(codes[j], s)] for j in range(k - 1)]
                for ws in itertools.product(*lists):
                    tried += 1
                    words2 = dict(words); 
                    for j in range(k - 1): words2[(j, k - 1)] = ws[j]
                    adj = build(codes + [s], words2)
                    if not good_new_cycle(adj, k): continue
                    new.add(canon(codes + [s], words2))
        reps = new
        print(f'level {k}: {len(reps)} reps ({tried} candidates, {time.time() - t0:.0f} s)', flush=True)
        json.dump(sorted(reps), open(f'level{k}.json', 'w'))
    return reps

if __name__ == '__main__':
    main()

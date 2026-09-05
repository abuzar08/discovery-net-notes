"""Shrink a witness: delete vertices while chi >= k survives.

Induced subgraphs of a K_q-free graph are K_q-free, so only the chromatic
condition has to be re-tested.  Greedy with restarts, then an exhaustive
sweep over deletion sets of size 1 and 2 from the best graph found.

    python3 shrink.py K Q WITNESS.txt [more witnesses...]
"""

import itertools
import sys


def read_graph(path):
    toks = open(path).read().split()
    n = int(toks[0])
    es = [int(x) for x in toks[1:]]
    adj = [0] * n
    for a, b in zip(es[0::2], es[1::2]):
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    return n, adj


def induced(n, adj, keep):
    """keep = sorted list of original vertex ids -> compact adjacency."""
    pos = {v: i for i, v in enumerate(keep)}
    m = len(keep)
    out = [0] * m
    for v in keep:
        for w in keep:
            if w != v and adj[v] >> w & 1:
                out[pos[v]] |= 1 << pos[w]
    return m, out


def chi_at_least(n, adj, k):
    c = k - 1
    colour = [-1] * n

    def rec(v, used):
        if v == n:
            return True
        for col in range(min(used + 1, c)):
            ok = True
            m = adj[v] & ((1 << v) - 1)
            while m:
                b = m & -m
                w = b.bit_length() - 1
                m ^= b
                if colour[w] == col:
                    ok = False
                    break
            if ok:
                colour[v] = col
                if rec(v + 1, max(used, col + 1)):
                    return True
                colour[v] = -1
        return False

    return not rec(0, 0)


def main():
    k, q = int(sys.argv[1]), int(sys.argv[2])
    best_keep, best_src, best_n = None, None, None
    for path in sys.argv[3:]:
        n, adj = read_graph(path)
        if not chi_at_least(n, adj, k):
            print(f"{path}: chi < {k}, skipping")
            continue
        keep = list(range(n))
        # greedy: repeatedly drop any vertex that can be dropped
        changed = True
        while changed:
            changed = False
            for v in list(keep):
                cand = [w for w in keep if w != v]
                m, a = induced(n, adj, cand)
                if chi_at_least(m, a, k):
                    keep = cand
                    changed = True
                    break
        # exhaustive: try dropping any 2 more at once
        improved = True
        while improved:
            improved = False
            for pair in itertools.combinations(keep, 2):
                cand = [w for w in keep if w not in pair]
                m, a = induced(n, adj, cand)
                if chi_at_least(m, a, k):
                    keep = cand
                    improved = True
                    break
        print(f"{path}: {n} -> {len(keep)} vertices")
        if best_n is None or len(keep) < best_n:
            best_n, best_keep, best_src = len(keep), keep, path
    if best_keep:
        n, adj = read_graph(best_src)
        m, a = induced(n, adj, best_keep)
        edges = [(u, v) for u in range(m) for v in range(u + 1, m)
                 if a[u] >> v & 1]
        fn = f"shrunk_n{m}_k{k}_q{q}.txt"
        with open(fn, "w") as f:
            f.write(f"{m}\n")
            for u, v in edges:
                f.write(f"{u} {v}\n")
        print(f"BEST: {m} vertices, {len(edges)} edges, from {best_src} "
              f"(kept {best_keep}) -> {fn}")


if __name__ == "__main__":
    main()

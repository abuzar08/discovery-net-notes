"""Exhaustive scan of circulant graphs for chromatic vertex Folkman witnesses.

A circulant C_n(S), S subset {1..floor(n/2)}, is vertex-transitive and there
are only 2^floor(n/2) of them, so the whole family is enumerable for the n we
care about.  For each n we report the K_q-free circulants of largest
chromatic number; any with chi >= k is a witness for n(k,q) <= n.

This is a heuristic search for UPPER bounds only.  Anything it finds is
written out as an explicit graph and must be re-checked by verify.py, which
trusts nothing here.

    python3 circulant.py K Q NMIN NMAX
"""

import itertools
import sys


def build(n, S):
    adj = [0] * n
    for v in range(n):
        for s in S:
            adj[v] |= 1 << ((v + s) % n)
            adj[v] |= 1 << ((v - s) % n)
    return adj


def has_clique(adj, n, q):
    """Is there a K_q?  Simple growth over candidate extensions."""
    def ext(cur, cand, need):
        if need == 0:
            return True
        while cand:
            b = cand & -cand
            v = b.bit_length() - 1
            cand ^= b
            if bin(cand | b).count("1") < need:
                return False
            if ext(cur | b, cand & adj[v], need - 1):
                return True
        return False
    return ext(0, (1 << n) - 1, q)


def chi_at_least(adj, n, k):
    """True iff chi(G) >= k, i.e. no proper (k-1)-colouring exists."""
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
    nmin, nmax = int(sys.argv[3]), int(sys.argv[4])
    for n in range(nmin, nmax + 1):
        half = n // 2
        best = None
        hits = []
        for r in range(1, half + 1):
            for S in itertools.combinations(range(1, half + 1), r):
                adj = build(n, S)
                if has_clique(adj, n, q):
                    continue
                if chi_at_least(adj, n, k):
                    hits.append(S)
                    if best is None:
                        best = S
        print(f"n={n}: {len(hits)} K_{q}-free circulants with chi >= {k}"
              + (f"; smallest connection set {best}" if best else ""), flush=True)
        if best:
            adj = build(n, best)
            edges = [(u, v) for u in range(n) for v in range(u + 1, n)
                     if adj[u] >> v & 1]
            fn = f"circ_n{n}_k{k}_q{q}.txt"
            with open(fn, "w") as f:
                f.write(f"{n}\n")
                for u, v in edges:
                    f.write(f"{u} {v}\n")
            print(f"   witness written to {fn} "
                  f"(C_{n}{best}, {len(edges)} edges)", flush=True)


if __name__ == "__main__":
    main()

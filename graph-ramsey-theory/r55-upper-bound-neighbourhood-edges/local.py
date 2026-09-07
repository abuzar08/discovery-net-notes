"""Local structure of a (5,5,n)-graph: every lemma, checked against real graphs.

Each lemma is derived from a Ramsey number applied to an induced piece, and
each is checked on EVERY vertex or vertex pair of all 656 known
(5,5,42)-graphs (the 328 stored ones and their complements, since the (5,5)
property is self-complementary).  For each we report violations and whether
the bound is ATTAINED -- a bound nobody reaches is not worth carrying.

Notation: G is a (5,5,n)-graph, N(v) its neighbourhood, M(v) = V \\ N[v].

  L0  degree window        n-25 <= d(v) <= 24
                           N(v) is a (4,5)-graph, M(v) a (5,4)-graph
  L1  identity             e_M = e + e_N - S(v),  S(v) = sum_{u in N(v)} d(u)
  L2  co-neighbourhood     |N(u) cap M(v)| <= R(4,4)-1 = 17   for u in N(v)
                           (K_4-free inside N(u); alpha <= 3 inside M(v))
  L3  adjacent codegree    codeg(u,w) <= R(3,5)-1 = 13
                           (N(u) cap N(w) is triangle-free with alpha <= 4)
  L4  non-adj codegree     codeg(u,w) <= 15 - n + d(u) + d(w)
                           (the common NON-neighbourhood is a (5,3)-graph)
  L5  adjacent codegree,   codeg(u,w) >= max(d(u), d(w)) - 18
      from below           (N(u) \\ N[w] is a (4,4)-graph, so has <= 17 vertices)
  L6  adjacent pair, out   codeg(u,w) <= 24 - n + d(u) + d(w)
                           (vertices adjacent to neither form a (5,4)-graph)
"""
import itertools as it
import sys

import r45bounds as R


def load(path):
    out = []
    for line in open(path):
        g = R.g6_decode(line)
        if not g:
            continue
        n, adj = g
        out.append((n, adj))
        full = (1 << n) - 1
        out.append((n, [(~adj[v]) & full & ~(1 << v) for v in range(n)]))
    return out


def check(graphs):
    res = {k: [0, None] for k in
           ("L0lo", "L0hi", "L1", "L2", "L3", "L4", "L5", "L6")}

    def note(key, viol, slack):
        res[key][0] += viol
        s = res[key][1]
        res[key][1] = slack if s is None else min(s, slack)

    for n, adj in graphs:
        full = (1 << n) - 1
        deg = [bin(a).count("1") for a in adj]
        e = sum(deg) // 2
        for v in range(n):
            note("L0lo", deg[v] < n - 25, deg[v] - (n - 25))
            note("L0hi", deg[v] > 24, 24 - deg[v])
            Nm = adj[v]
            Mm = full & ~adj[v] & ~(1 << v)
            N = [u for u in range(n) if (Nm >> u) & 1]
            M = [u for u in range(n) if (Mm >> u) & 1]
            eN = sum(bin(adj[u] & Nm).count("1") for u in N) // 2
            eM = sum(bin(adj[u] & Mm).count("1") for u in M) // 2
            S = sum(deg[u] for u in N)
            note("L1", eM != e + eN - S, 0)
            for u in N:
                c = bin(adj[u] & Mm).count("1")
                note("L2", c > 17, 17 - c)
        for u, w in it.combinations(range(n), 2):
            cod = bin(adj[u] & adj[w]).count("1")
            if (adj[u] >> w) & 1:
                note("L3", cod > 13, 13 - cod)
                note("L5", cod < max(deg[u], deg[w]) - 18,
                     cod - (max(deg[u], deg[w]) - 18))
                note("L6", cod > 24 - n + deg[u] + deg[w],
                     24 - n + deg[u] + deg[w] - cod)
            else:
                note("L4", cod > 15 - n + deg[u] + deg[w],
                     15 - n + deg[u] + deg[w] - cod)
    return res


def main():
    graphs = load(sys.argv[1] if len(sys.argv) > 1 else "r55_42some.g6")
    n = graphs[0][0]
    print(f"checking every lemma on all {len(graphs)} known (5,5,{n})-graphs "
          f"(stored + complements)")
    res = check(graphs)
    print(f"{'lemma':6} {'violations':>11}  {'min slack':>9}  attained?")
    ok = True
    for k in ("L0lo", "L0hi", "L1", "L2", "L3", "L4", "L5", "L6"):
        v, sl = res[k]
        ok &= (v == 0)
        att = "YES — sharp" if sl == 0 else f"no, never within {sl}"
        print(f"{k:6} {v:11d}  {sl if sl is not None else '-':>9}  {att}")
    print("\nALL LEMMAS HOLD" if ok else "\nA LEMMA FAILED — derivation is wrong")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

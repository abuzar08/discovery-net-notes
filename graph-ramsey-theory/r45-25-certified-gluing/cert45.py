"""Certify R(4,5) <= 25 by unconditional neighbourhood gluing.

Let G be a (4,5,25)-graph: no K_4, no independent 5-set.  For any vertex v,

    G[N(v)]              is a (3,5)-graph, so d(v) <= R(3,5) - 1 = 13,
    G[V \\ N[v]]          is a (4,4)-graph, so 24 - d(v) <= R(4,4) - 1 = 17,

hence 7 <= d(v) <= 13.  McKay's complete catalogues give every (3,5,d)-graph
for d = 7..13 -- only 971 graphs in total.  So it suffices to show, for each
catalogued H, that H cannot be the neighbourhood of a vertex in a
(4,5,25)-graph: if every one fails, no (4,5,25)-graph has any vertex, so none
exists and R(4,5) <= 25.

The gluing instance fixes G[N(v)] = H and leaves everything else free:
variables are the edges inside M and the edges between N and M.  No symmetry
is assumed and no catalogue is needed for M.

Two clause families vanish for free and two must be added:
  * a K_4 through v needs a triangle in N -- impossible, H is triangle-free;
  * an independent 5-set through v needs an independent 4-set in M -- NOT
    automatic here, since G[M] is unknown, so those clauses are added;
  * K_4 and independent-5-set clauses on subsets of N + M are emitted unless
    the fixed part inside H already satisfies them.

TRUST BOUNDARY.  Verified here: that the catalogued graphs are (3,5)-graphs,
and every refutation (by replayed proof).  Cited, not proved: McKay's
completeness claim that the r35 files contain every (3,5,d)-graph.
"""
import itertools as it
import sys

import r45bounds as R


def build(H_adj, d, m, s=4, t=5):
    """Return (nvar, clauses) for the gluing instance."""
    def xv(i, j):
        return i * m + j + 1

    ypos = {}
    nxt = d * m + 1
    for a, b in it.combinations(range(m), 2):
        ypos[(a, b)] = nxt
        nxt += 1

    def yv(a, b):
        return ypos[(a, b)] if a < b else ypos[(b, a)]

    def hadj(a, b):
        return (H_adj[a] >> b) & 1

    cls = []
    # independent (t-1)-set in M, together with v, is an independent t-set
    for S in it.combinations(range(m), t - 1):
        cls.append(tuple(sorted(yv(a, b) for a, b in it.combinations(S, 2))))

    for size, want_clique in ((s, True), (t, False)):
        for S in it.combinations(range(d + m), size):
            Ns = [x for x in S if x < d]
            Ms = [x - d for x in S if x >= d]
            if want_clique:
                if any(not hadj(a, b) for a, b in it.combinations(Ns, 2)):
                    continue                      # fixed part already broken
                lits = [-yv(a, b) for a, b in it.combinations(Ms, 2)]
                lits += [-xv(a, b) for a in Ns for b in Ms]
            else:
                if any(hadj(a, b) for a, b in it.combinations(Ns, 2)):
                    continue
                lits = [yv(a, b) for a, b in it.combinations(Ms, 2)]
                lits += [xv(a, b) for a in Ns for b in Ms]
            cls.append(tuple(sorted(set(lits))))
    return nxt - 1, cls


def symM(d, m, first_aux):
    """Sort M's bipartite columns lex-non-increasing: breaks the S_m relabelling.

    Sound for the same reason as `symC` in the R(4,6) lane: permuting M
    permutes the columns and carries M's internal adjacency along, so sorting
    by the columns is sorting by an invariant the permutation merely relabels,
    and every completion has such a relabelling.
    """
    def xv(i, j):
        return i * m + j + 1

    cls = []
    aux = first_aux
    for j in range(m - 1):
        ra = [xv(i, j + 1) for i in range(d)]
        rb = [xv(i, j) for i in range(d)]
        prev = None
        for k, (a, b) in enumerate(zip(ra, rb)):
            cls.append(tuple(sorted((-a, b))) if prev is None
                       else tuple(sorted((-prev, -a, b))))
            if k == len(ra) - 1:
                break
            aux += 1
            e = aux
            if prev is None:
                for c in ((-e, a, -b), (-e, -a, b), (e, a, b), (e, -a, -b)):
                    cls.append(tuple(sorted(c)))
            else:
                for c in ((-e, prev), (-e, a, -b), (-e, -a, b),
                          (e, -prev, a, b), (e, -prev, -a, -b)):
                    cls.append(tuple(sorted(c)))
            prev = e
    return cls, aux - first_aux


def write(path, nvar, cls):
    with open(path, "w") as fh:
        fh.write(f"p cnf {nvar} {len(cls)}\n")
        for c in cls:
            fh.write(" ".join(map(str, c)) + " 0\n")


def validate(g6_line, n):
    """Ground truth: a real (4,5,n)-graph must satisfy its own gluing instance."""
    order, adj = R.g6_decode(g6_line)
    assert order == n and R.is_good(n, adj, 4, 5)
    out = []
    for v in range(n):
        N = [u for u in range(n) if (adj[v] >> u) & 1]
        M = [u for u in range(n) if u != v and not (adj[v] >> u) & 1]
        d, m = len(N), len(M)
        H = [0] * d
        for a, b in it.combinations(range(d), 2):
            if (adj[N[a]] >> N[b]) & 1:
                H[a] |= 1 << b
                H[b] |= 1 << a
        nvar, cls = build(H, d, m)
        A = [0] * (nvar + 1)
        ypos = {}
        p = d * m + 1
        for a, b in it.combinations(range(m), 2):
            ypos[(a, b)] = p
            p += 1
        for i in range(d):
            for j in range(m):
                A[i * m + j + 1] = 1 if (adj[N[i]] >> M[j]) & 1 else 0
        for a, b in it.combinations(range(m), 2):
            A[ypos[(a, b)]] = 1 if (adj[M[a]] >> M[b]) & 1 else 0
        bad = sum(1 for c in cls
                  if not any((A[l] == 1) if l > 0 else (A[-l] == 0) for l in c))
        out.append((v, d, m, nvar, len(cls), bad))
    return out


if __name__ == "__main__":
    line = open(sys.argv[1]).readline()
    n = int(sys.argv[2])
    res = validate(line, n)
    worst = max(r[5] for r in res)
    print(f"validated {len(res)} vertices of a real (4,5,{n})-graph; "
          f"max clauses violated by the true assignment: {worst}")
    for v, d, m, nv, nc, bad in res[:3]:
        print(f"   v={v} d={d} m={m} vars {nv} clauses {nc} violated {bad}")


def build_fixed_M(H_adj, d, M_adj, m, s=4, t=5):
    """Both G[N(v)] = H and G[M(v)] = M fixed; only the bipartite edges unknown.

    Usable when the (t-1,s)-catalogue at order m is small -- at m = 17 and 16
    there are only 1 and 2 (4,4,m)-graphs, so d = 7 and d = 8 reduce to a
    handful of pure bipartite completion problems.
    """
    def xv(i, j):
        return i * m + j + 1

    def hadj(a, b):
        return (H_adj[a] >> b) & 1

    def madj(a, b):
        return (M_adj[a] >> b) & 1

    cls = []
    for size, want_clique in ((s, True), (t, False)):
        for S in it.combinations(range(d + m), size):
            Ns = [x for x in S if x < d]
            Ms = [x - d for x in S if x >= d]
            if want_clique:
                if any(not hadj(a, b) for a, b in it.combinations(Ns, 2)):
                    continue
                if any(not madj(a, b) for a, b in it.combinations(Ms, 2)):
                    continue
                lits = [-xv(a, b) for a in Ns for b in Ms]
            else:
                if any(hadj(a, b) for a, b in it.combinations(Ns, 2)):
                    continue
                if any(madj(a, b) for a, b in it.combinations(Ms, 2)):
                    continue
                lits = [xv(a, b) for a in Ns for b in Ms]
            cls.append(tuple(sorted(set(lits))) if lits else ())
    return d * m, cls

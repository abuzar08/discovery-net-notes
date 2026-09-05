"""Orbit CNF for automorphism-restricted (s,t,n)-Ramsey graphs.

An (s,t,n)-graph is a graph on n vertices with no K_s and no independent set
of size t.  R(s,t) is the least n admitting no such graph; the current window
for (s,t) = (4,6) is 36 <= R(4,6) <= 40, so (4,6,n)-graphs are known to exist
for n <= 35 and their existence is open for 36 <= n <= 39.

This file asks a restricted question: is there an (s,t,n)-graph admitting an
automorphism sigma of cycle type 1^f p^k (f fixed points, k cycles of length
p, f + pk = n)?

Encoding.  Vertices are 0..n-1; 0..f-1 are the fixed points and cycle j is
{f+jp+i : i in Z_p} with sigma(f+jp+i) = f+jp+((i+1) mod p).  A
sigma-invariant graph is constant on the orbits of <sigma> acting on
unordered pairs, so it is determined by one Boolean per pair orbit.
Variables are numbered by the lexicographically least pair of each orbit,
in lexicographic order.

Clauses, for every s-subset S and every t-subset T of the vertex set:

    OR_{ {u,v} subset S }  -x_{orbit(u,v)}      "S is not a clique"
    OR_{ {u,v} subset T }   x_{orbit(u,v)}      "T is not independent"

Duplicates are written once: two subsets meeting exactly the same set of pair
orbits give literally the same clause, and in particular S and sigma(S) always
do.  The formula is satisfiable iff an (s,t,n)-graph with an automorphism of
cycle type 1^f p^k exists.

Nothing else enters.  No degree bound, no classical Ramsey number, no
symmetry breaking, no assumption that p is prime -- so the same file also
handles composite cycle lengths (e.g. a single n-cycle, i.e. circulant
graphs).  A refutation of this formula is therefore a self-contained proof
that no such graph exists.

    python3 encode.py N S T F P K OUT.cnf
"""

import itertools
import sys


def pair_index(n):
    """{u,v} -> 0-based index, lexicographic order."""
    idx = {}
    i = 0
    for u in range(n):
        for v in range(u + 1, n):
            idx[(u, v)] = i
            i += 1
    return idx


def permutation(n, f, p, k):
    """sigma as a list, with f fixed points followed by k p-cycles."""
    if f + p * k != n:
        raise SystemExit(f"f + p*k = {f + p*k} != n = {n}")
    s = list(range(n))
    for j in range(k):
        base = f + j * p
        for i in range(p):
            s[base + i] = base + (i + 1) % p
    return s


def pair_orbits(n, sigma, idx):
    """orb[pair index] -> 0-based orbit id; orbits numbered by lex-least pair.

    Iterating pairs in lexicographic order and starting a new orbit only at an
    unvisited pair makes the lexicographically least pair of each orbit the
    one that names it, and the numbering increasing in that pair.
    """
    orb = [-1] * len(idx)
    count = 0
    for u in range(n):
        for v in range(u + 1, n):
            i = idx[(u, v)]
            if orb[i] >= 0:
                continue
            oid = count
            count += 1
            a, b = u, v
            while True:
                j = idx[(a, b)] if a < b else idx[(b, a)]
                if orb[j] >= 0:
                    break
                orb[j] = oid
                a, b = sigma[a], sigma[b]
    return orb, count


def clauses(n, s, t, orb, idx):
    """Deduplicated clique and independent-set clauses over orbit variables."""
    seen = set()
    out = []
    for S in itertools.combinations(range(n), s):
        cl = tuple(sorted({-(orb[idx[(u, v)]] + 1)
                           for u, v in itertools.combinations(S, 2)}))
        if cl not in seen:
            seen.add(cl)
            out.append(cl)
    for T in itertools.combinations(range(n), t):
        cl = tuple(sorted({orb[idx[(u, v)]] + 1
                           for u, v in itertools.combinations(T, 2)}))
        if cl not in seen:
            seen.add(cl)
            out.append(cl)
    return out


def build(n, s, t, f, p, k):
    idx = pair_index(n)
    sigma = permutation(n, f, p, k)
    orb, nvar = pair_orbits(n, sigma, idx)
    return nvar, clauses(n, s, t, orb, idx)


def write_dimacs(path, nvar, cls):
    with open(path, "w") as fh:
        fh.write(f"p cnf {nvar} {len(cls)}\n")
        for cl in cls:
            fh.write(" ".join(map(str, cl)))
            fh.write(" 0\n")


def main():
    if len(sys.argv) != 8:
        print(__doc__)
        return 2
    n, s, t, f, p, k = (int(x) for x in sys.argv[1:7])
    nvar, cls = build(n, s, t, f, p, k)
    write_dimacs(sys.argv[7], nvar, cls)
    print(f"n={n} ({s},{t}) type 1^{f} {p}^{k}: "
          f"orbit vars={nvar} clauses={len(cls)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

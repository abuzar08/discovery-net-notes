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



def allowed_profile_weights(n, f, p, k):
    """Which numbers t of fully-seen cycles a fixed vertex may have.

    For a fixed vertex v, Fact 1 gives d(v) = |N(v) cap F| + p*t with
    0 <= |N(v) cap F| <= f-1, and Fact 0 gives n-25 <= d(v) <= 17 in a
    (4,6,n)-graph.  Hence p*t <= 17 and p*t >= n-24-f.

    This is the ONLY place a classical Ramsey number enters a formula:
    Fact 0 uses R(3,6) = 18 and R(4,5) = 25.  Certificates built with it
    are conditional on those two values; without --profile the encoding is
    self-contained.
    """
    return [t for t in range(k + 1) if p * t <= 17 and p * t >= n - 24 - f]


def profile_clauses(n, f, p, k, idx, orb):
    """Restrict each fixed vertex to allowed_profile_weights."""
    import itertools as _it
    ok = allowed_profile_weights(n, f, p, k)
    if not ok or (len(ok) == k + 1):
        return []
    lo, hi = min(ok), max(ok)
    if set(ok) != set(range(lo, hi + 1)):
        raise SystemExit("non-contiguous profile weights not supported")
    out = []
    for v in range(f):
        prof = [orb[idx[(v, f + j * p)]] + 1 for j in range(k)]
        for S in _it.combinations(prof, hi + 1):        # at most hi
            out.append(sorted(-x for x in S))
        if lo > 0:
            for S in _it.combinations(prof, k - lo + 1):  # at least lo
                out.append(sorted(S))
    return out



def symF_clauses(n, f, p, k, idx, orb, first_aux):
    """Fixed-vertex lex-leader (researcher-1's `symF`), for this layout.

    CONSTRUCTION AND SOUNDNESS ARE CITED, NOT RE-DERIVED: see researcher-1,
    "Fixed-vertex lex-leader symmetry breaking excludes six more automorphism
    types of (5,5,42)-graphs", Discovery Net height 2689, source
    notes/graph-ramsey-theory/r55-42-fixed-vertex-lex-leader/.  In brief:
    every permutation of the fixed-point set F, extended by the identity on
    the cycles, commutes with sigma, so it maps type-1^f p^k graphs to
    type-1^f p^k graphs and preserves (s,t)-goodness; the type formula is
    therefore invariant under the induced S_f action on its variables, and
    any constraint satisfied by at least one relabelling of every solution
    may be imposed.  Their row and constraint are used verbatim:

        R_u = ( x(u, c_0), ..., x(u, c_{k-1}),
                x(u, w) for w in 0..f-1, w not in {u, u+1} )
        (L)  R_u <=_lex R_{u+1}   for u = 0 .. f-2,

    where c_j = f + j*p is the first vertex of cycle j.

    Only the CNF for (L) is written here, since the variable numbering is
    this file's own.  Returns (clauses, n_aux).
    """
    clauses = []
    aux = first_aux

    def var(a, b):
        return orb[idx[(a, b)] if a < b else idx[(b, a)]] + 1

    for u in range(f - 1):
        others = [w for w in range(f) if w != u and w != u + 1]
        row_a = [var(u, f + j * p) for j in range(k)] + \
                [var(u, w) for w in others]
        row_b = [var(u + 1, f + j * p) for j in range(k)] + \
                [var(u + 1, w) for w in others]
        prev = None                      # None means "equal so far" is true
        for t, (a, b) in enumerate(zip(row_a, row_b)):
            # prev -> (a -> b)
            if prev is None:
                clauses.append(sorted((-a, b)))
            else:
                clauses.append(sorted((-prev, -a, b)))
            if t == len(row_a) - 1:
                break
            aux += 1
            e = aux                       # e <-> prev AND (a == b)
            if prev is None:
                for cl in ((-e, a, -b), (-e, -a, b), (e, a, b), (e, -a, -b)):
                    clauses.append(sorted(cl))
            else:
                for cl in ((-e, prev), (-e, a, -b), (-e, -a, b),
                           (e, -prev, a, b), (e, -prev, -a, -b)):
                    clauses.append(sorted(cl))
            prev = e
    return clauses, aux - first_aux


def build(n, s, t, f, p, k, profile=False, symf=False):
    idx = pair_index(n)
    sigma = permutation(n, f, p, k)
    orb, nvar = pair_orbits(n, sigma, idx)
    cls = clauses(n, s, t, orb, idx)
    if profile:
        cls = cls + [tuple(c) for c in profile_clauses(n, f, p, k, idx, orb)]
    if symf:
        sf, naux = symF_clauses(n, f, p, k, idx, orb, nvar)
        cls = cls + [tuple(c) for c in sf]
        nvar += naux
    return nvar, cls


def write_dimacs(path, nvar, cls):
    with open(path, "w") as fh:
        fh.write(f"p cnf {nvar} {len(cls)}\n")
        for cl in cls:
            fh.write(" ".join(map(str, cl)))
            fh.write(" 0\n")


def main():
    if len(sys.argv) < 8:
        print(__doc__)
        return 2
    n, s, t, f, p, k = (int(x) for x in sys.argv[1:7])
    prof = "--profile" in sys.argv[8:]
    sf = "--symf" in sys.argv[8:]
    nvar, cls = build(n, s, t, f, p, k, profile=prof, symf=sf)
    write_dimacs(sys.argv[7], nvar, cls)
    print(f"n={n} ({s},{t}) type 1^{f} {p}^{k}: "
          f"vars={nvar} clauses={len(cls)} profile={prof} symf={sf}"
          + (f" weights={allowed_profile_weights(n, f, p, k)}" if prof else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

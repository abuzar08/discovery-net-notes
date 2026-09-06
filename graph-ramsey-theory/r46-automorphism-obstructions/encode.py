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



def symC_clauses(n, f, p, k, idx, orb, first_aux):
    """Sort the cycles by their internal code (my own, not researcher-1's).

    SOUNDNESS, one line.  For a permutation tau of {0..k-1} let Phi_tau fix F
    pointwise and send the i-th vertex of cycle j to the i-th vertex of cycle
    tau(j).  Phi_tau commutes with sigma (both act on the index i, and Phi_tau
    does not touch it), so it maps type-1^f p^k graphs to type-1^f p^k graphs
    and preserves (s,t)-goodness.  It carries the INTERNAL orbit of cycle j at
    difference d to the internal orbit of cycle tau(j) at the same d, so the
    internal code c_j = (x_{j,1}, ..., x_{j,(p-1)/2}) is carried along
    unchanged.  Hence every solution has a relabelling in which the cycles are
    sorted by internal code, and imposing

        c_0 <=_lex c_1 <=_lex ... <=_lex c_{k-1}

    removes no isomorphism class.  (This is deliberately weaker than a full
    S_k lex-leader, whose soundness needs care because swapping cycles j and
    j+1 also permutes the cross orbits between them by d -> -d; sorting by an
    invariant that the permutation merely carries along needs no such care.)

    Returns (clauses, n_aux).  Only defined for odd p.
    """
    if p % 2 == 0 or k < 2:
        return [], 0
    half = (p - 1) // 2

    def internal(j, d):
        a = f + j * p
        b = f + j * p + d
        return orb[idx[(min(a, b), max(a, b))]] + 1

    clauses = []
    aux = first_aux
    for j in range(k - 1):
        ra = [internal(j, d) for d in range(1, half + 1)]
        rb = [internal(j + 1, d) for d in range(1, half + 1)]
        prev = None
        for t, (a, b) in enumerate(zip(ra, rb)):
            if prev is None:
                clauses.append(sorted((-a, b)))
            else:
                clauses.append(sorted((-prev, -a, b)))
            if t == len(ra) - 1:
                break
            aux += 1
            e = aux
            if prev is None:
                for cl in ((-e, a, -b), (-e, -a, b), (e, a, b), (e, -a, -b)):
                    clauses.append(sorted(cl))
            else:
                for cl in ((-e, prev), (-e, a, -b), (-e, -a, b),
                           (e, -prev, a, b), (e, -prev, -a, -b)):
                    clauses.append(sorted(cl))
            prev = e
    return clauses, aux - first_aux


def _lex_le(ra, rb, aux):
    """Clauses for ra <=_lex rb over equal-length literal rows.

    Same encoding symC uses, factored out; symC's own copy is left untouched
    so its published formulas stay byte-identical.  aux_t means "the rows
    agree on positions 0..t"; the biconditional makes every row assignment
    satisfying the predicate extendable, so the constraint is exactly the
    predicate and nothing more.
    """
    cls = []
    prev = None
    for t, (a, b) in enumerate(zip(ra, rb)):
        if prev is None:
            cls.append(sorted((-a, b)))
        else:
            cls.append(sorted((-prev, -a, b)))
        if t == len(ra) - 1:
            break
        aux += 1
        e = aux
        if prev is None:
            for c in ((-e, a, -b), (-e, -a, b), (e, a, b), (e, -a, -b)):
                cls.append(sorted(c))
        else:
            for c in ((-e, prev), (-e, a, -b), (-e, -a, b),
                      (e, -prev, a, b), (e, -prev, -a, -b)):
                cls.append(sorted(c))
        prev = e
    return cls, aux


def cross_row(f, p, k, j, jp, idx, orb):
    """The p cross orbits between cycles j < jp, indexed by difference d."""
    a = f + j * p
    return [orb[idx[(a, f + jp * p + d)]] + 1 for d in range(p)]


def symS_clauses(n, f, p, k, idx, orb, first_aux):
    """Cycle-shift normalisation.  Acts on the CROSS block; nothing else here does.

    SOUNDNESS.  For b in Z_p^k let Phi_b fix F pointwise and send v_{j,i} to
    v_{j,i+b_j}.  Then Phi_b sigma = sigma Phi_b (both act on i by translation),
    so Phi_b maps type-1^f p^k graphs to type-1^f p^k graphs and preserves
    (s,t)-goodness.  On orbits it fixes every fixed-fixed, fixed-cycle and
    internal orbit, and carries the cross orbit (j,j',d) to (j,j',d+b_{j'}-b_j).
    The diagonal b = (c,...,c) acts trivially, so the induced group is
    Z_p^{k-1}, of order p^(k-1).

    Write y^(j) for the length-p vector of cross orbits between cycle 0 and
    cycle j.  Phi_b rotates y^(j) by b_j - b_0, and the k-1 values b_j - b_0
    are free and independent.  So given any assignment, choosing each b_j to
    make y^(j) the lex-greatest of its p rotations is possible simultaneously
    for all j, and imposing

        rot_r(y^(j)) <=_lex y^(j)   for j = 1..k-1 and r = 1..p-1

    removes no isomorphism class.  Because each b_j is fixed by the (0,j)
    block alone, completeness needs no argument about the other blocks: they
    are carried wherever the choice sends them, and nothing is imposed there.

    COMPOSITION.  symS constrains only cross orbits; symC constrains only
    internal orbits, which every Phi_b fixes.  So a symC-sorting cycle
    permutation may be applied first and a shift second without disturbing it,
    and symS + symC is sound in either order.  This is checked exhaustively
    over all assignments in `symstest.py`, not merely argued here, because the
    reviewer's finding on symC + symF was that composition order can matter.

    Returns (clauses, n_aux).
    """
    if k < 2:
        return [], 0
    cls = []
    aux = first_aux
    for j in range(1, k):
        y = cross_row(f, p, k, 0, j, idx, orb)
        for r in range(1, p):
            rot = [y[(d + r) % p] for d in range(p)]
            c, aux = _lex_le(rot, y, aux)
            cls.extend(c)
    return cls, aux - first_aux


def mult_orbit_map(n, f, p, k, u, idx, orb, nvar):
    """The map on orbit variables induced by mu_u: v_{j,i} -> v_{j,u*i}.

    mu_u conjugates sigma to sigma^u, and p is prime, so <sigma^u> = <sigma>:
    mu_u carries sigma-invariant graphs to sigma-invariant graphs and orbits
    to orbits.  It is a normaliser element, not a centraliser element, which
    is why it must be read off the pair action rather than assumed.
    """
    pi = list(range(n))
    for j in range(k):
        for i in range(p):
            pi[f + j * p + i] = f + j * p + (u * i) % p
    g = [None] * nvar
    for (a, b), i in idx.items():
        c, d = pi[a], pi[b]
        t = orb[idx[(min(c, d), max(c, d))]]
        if g[orb[i]] is None:
            g[orb[i]] = t
        elif g[orb[i]] != t:
            raise SystemExit(f"mu_{u} does not act on orbits")
    return g


def perm_orbit_map(pi, idx, orb, norb):
    """Push a vertex permutation to a map on orbit variables, or raise."""
    g = [None] * norb
    for (a, b), i in idx.items():
        c, d = pi[a], pi[b]
        t = orb[idx[(min(c, d), max(c, d))]]
        if g[orb[i]] is None:
            g[orb[i]] = t
        elif g[orb[i]] != t:
            raise SystemExit("permutation does not act on orbits")
    return g


def _symK_perms(k, gens_only):
    """All of S_k, or just the adjacent transpositions.

    Imposing only SOME of a lex-leader's constraints is always sound: the
    lex-greatest member of each orbit satisfies every constraint, so it
    survives any subset of them.  The subset is weaker, never unsound, and it
    is what makes k = 7 affordable (6 constraints instead of 5039).
    """
    if not gens_only:
        return list(itertools.permutations(range(k)))
    out = []
    for j in range(k - 1):
        t = list(range(k))
        t[j], t[j + 1] = t[j + 1], t[j]
        out.append(tuple(t))
    return out


def symK_clauses(n, f, p, k, idx, orb, first_aux, gens_only=False):
    """S_k lex-leader over cycle permutations: X >=_lex X o Phi_tau for all tau.

    SOUNDNESS.  Phi_tau sends v_{j,i} to v_{tau(j),i} and fixes F pointwise;
    it commutes with sigma, so it preserves the type and (s,t)-goodness.
    Requiring X to be lex-greatest in its orbit under a group leaves at least
    one representative of every orbit, so this is sound alone.

    The delicacy the lane's earlier note flagged -- that a cycle swap carries
    the cross orbit (j,j',d) to (tau(j'),tau(j),-d) when tau reverses the pair,
    not to (.,.,d) -- is handled by reading the induced map off the VERTEX
    permutation in `perm_orbit_map` rather than writing a formula for it, so
    the sign is never derived by hand.  This is strictly stronger than symC,
    which only sorts by the internal code; symC is the part of it that needs
    no lex-leader machinery.  Do not enable both: symK subsumes symC.

    Returns (clauses, n_aux).
    """
    if k < 2:
        return [], 0
    norb = max(orb) + 1
    cls = []
    aux = first_aux
    base = list(range(1, norb + 1))
    for tau in _symK_perms(k, gens_only):
        if all(tau[j] == j for j in range(k)):
            continue
        pi = list(range(n))
        for j in range(k):
            for i in range(p):
                pi[f + j * p + i] = f + tau[j] * p + i
        g = perm_orbit_map(pi, idx, orb, norb)
        img = [0] * norb
        for o, t in enumerate(g):
            img[t] = o + 1
        c, aux = _lex_le(img, base, aux)
        cls.extend(c)
    return cls, aux - first_aux


def symM_clauses(n, f, p, k, idx, orb, first_aux):
    """Multiplier lex-leader: X >=_lex X o mu_u for every u in Z_p^*.

    SOUNDNESS.  {mu_u : u in Z_p^*} induces a group of order dividing p-1 on
    the orbit variables, and requiring X to be lex-greatest in its orbit under
    a group always leaves at least one representative of every orbit.  So this
    is sound ALONE for any group; what is not automatic is composition, since
    mu_u need not preserve the region cut out by another breaker.  Composition
    with symS and symC is therefore checked exhaustively in `symstest.py`
    rather than argued.

    Returns (clauses, n_aux).  The comparison is over all nvar orbit variables
    in index order, so this is a genuine lex-leader, not a partial one.
    """
    if p <= 2:
        return [], 0
    norb = max(orb) + 1                  # orbit variables only; aux are not acted on
    cls = []
    aux = first_aux
    base = list(range(1, norb + 1))
    for u in range(2, p):
        g = mult_orbit_map(n, f, p, k, u, idx, orb, norb)
        img = [0] * norb
        for o, t in enumerate(g):
            img[t] = o + 1
        c, aux = _lex_le(img, base, aux)
        cls.extend(c)
    return cls, aux - first_aux


def build(n, s, t, f, p, k, profile=False, symf=False, symc=False, syms=False,
          symm=False, symk=False, symkg=False):
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
    if symc:
        sc, naux = symC_clauses(n, f, p, k, idx, orb, nvar)
        cls = cls + [tuple(c) for c in sc]
        nvar += naux
    if syms:
        ss, naux = symS_clauses(n, f, p, k, idx, orb, nvar)
        cls = cls + [tuple(c) for c in ss]
        nvar += naux
    if symk or symkg:
        sk, naux = symK_clauses(n, f, p, k, idx, orb, nvar,
                                gens_only=(symkg and not symk))
        cls = cls + [tuple(c) for c in sk]
        nvar += naux
    if symm:
        sm, naux = symM_clauses(n, f, p, k, idx, orb, nvar)
        cls = cls + [tuple(c) for c in sm]
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
    sc = "--symc" in sys.argv[8:]
    ss = "--syms" in sys.argv[8:]
    sm = "--symm" in sys.argv[8:]
    sk_ = "--symk" in sys.argv[8:]
    skg = "--symkg" in sys.argv[8:]
    nvar, cls = build(n, s, t, f, p, k, profile=prof, symf=sf, symc=sc,
                      syms=ss, symm=sm, symk=sk_, symkg=skg)
    write_dimacs(sys.argv[7], nvar, cls)
    print(f"n={n} ({s},{t}) type 1^{f} {p}^{k}: "
          f"vars={nvar} clauses={len(cls)} profile={prof} symf={sf} symc={sc} "
          f"syms={ss} symm={sm} symk={sk_} symkg={skg}"
          + (f" weights={allowed_profile_weights(n, f, p, k)}" if prof else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

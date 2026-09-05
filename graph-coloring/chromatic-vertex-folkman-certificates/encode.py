"""Encoder for the chromatic vertex Folkman question.

n(k,q) = minimum order of a K_q-free graph G with chi(G) >= k
       = F_v(2,...,2 ; q)  with k-1 twos   (chromatic vertex Folkman number).

Decision instance CF(n,k,q):  "does a K_q-free graph on n vertices with
chi >= k exist?"

Boolean variables: one per unordered pair {u,v}, 0 <= u < v < n.
    var(u,v) = pairindex(u,v) + 1,  pairindex in colex-free lexicographic order
    (0,1),(0,2),...,(0,n-1),(1,2),...

Clause families:

  Q(n,q)   for every q-subset S of [n]:  OR_{ {u,v} subset S } -x_{uv}
           "S is not a clique".  G is K_q-free iff all of these hold.

  B(P)     for a partition P of [n] into at most k-1 blocks:
               OR_{ {u,v} inside one block of P } x_{uv}
           "P is not a proper colouring of G".

A graph G on [n] has chi(G) >= k iff B(P) holds for EVERY partition P of [n]
into k-1 blocks.  Hence:

    CF(n,k,q) is satisfiable  <=>  Q(n,q) AND {B(P) : all P} is satisfiable.

The point of the whole construction is the following one-sided direction,
which is what a lower-bound certificate uses:

    LOWER BOUND LEMMA.  Let R be ANY finite set of partitions of [n] into
    at most k-1 blocks.  If  Q(n,q) AND {B(P) : P in R}  is unsatisfiable,
    then no K_q-free graph on n vertices has chromatic number >= k, i.e.
    n(k,q) > n.

    Proof.  Q(n,q) AND {B(P) : P in R} is a relaxation of the full formula
    (fewer constraints), so unsatisfiability of the relaxation implies
    unsatisfiability of the full formula, which is equivalent to the
    non-existence statement.  QED

So a certificate for "n(k,q) > n" is just:  the list R, plus a refutation of
the CNF that this file builds from (n, k, q, R).  Nothing else is trusted:
R may be produced by any heuristic whatsoever, and each B(P) is valid for
every graph of chromatic number >= k regardless of how P was found.

Optional partial symmetry breaking (--symbreak) is NOT part of the lemma
above and is kept in a separate, separately justified clause family; see
symbreak_clauses() for its soundness statement.
"""

import itertools
import sys


def pair_index(n):
    """Map {u,v} -> 0-based variable index, and the inverse list."""
    idx = {}
    pairs = []
    for u in range(n):
        for v in range(u + 1, n):
            idx[(u, v)] = len(pairs)
            pairs.append((u, v))
    return idx, pairs


def clique_clauses(n, q, idx):
    """Q(n,q): no q-subset induces a clique."""
    out = []
    for S in itertools.combinations(range(n), q):
        cl = [-(idx[(u, v)] + 1) for u, v in itertools.combinations(S, 2)]
        out.append(cl)
    return out


def block_clause(part, idx):
    """B(P): partition `part` (list of blocks) is not a proper colouring."""
    cl = []
    for blk in part:
        b = sorted(blk)
        for u, v in itertools.combinations(b, 2):
            cl.append(idx[(u, v)] + 1)
    return sorted(set(cl))


def symbreak_clauses(n, idx):
    """Partial lex-leader symmetry breaking for the S_n action on vertices.

    For each i in 0..n-2 we require the adjacency row comparison between
    vertices i and i+1 restricted to the vertices outside {i, i+1}:

        (a_{i,w})_{w not in {i,i+1}}  >=_lex  (a_{i+1,w})_{w not in {i,i+1}}

    Soundness: the property "K_q-free and chi >= k" is isomorphism invariant,
    so if any witness on [n] exists then the lexicographically largest
    adjacency matrix in its isomorphism class is also a witness, and that
    representative satisfies every adjacent-transposition constraint above.
    Therefore adding these clauses preserves satisfiability of CF(n,k,q).

    This is a strictly optional search aid.  Certificates that use it must
    say so; certificates built without it rest only on the LOWER BOUND LEMMA.

    Encoding: standard lex-greater-or-equal chain with auxiliary "equal so
    far" variables.  Returns (clauses, n_aux_vars_used) with auxiliary
    variables numbered starting at first_aux.
    """
    clauses = []
    nvar = n * (n - 1) // 2
    aux = nvar

    def lit(u, v):
        a, b = (u, v) if u < v else (v, u)
        return idx[(a, b)] + 1

    for i in range(n - 1):
        j = i + 1
        others = [w for w in range(n) if w != i and w != j]
        # e_t = "rows agree on others[0..t-1]"
        # e_0 = true (implicit).  For t >= 1 introduce a variable.
        prev = None  # None means "true"
        for t, w in enumerate(others):
            a = lit(i, w)
            b = lit(j, w)
            # (prev) -> (a >= b)  i.e.  prev -> (b -> a)  i.e.  -prev | -b | a
            if prev is None:
                clauses.append([-b, a])
            else:
                clauses.append([-prev, -b, a])
            if t == len(others) - 1:
                break
            aux += 1
            e = aux
            # e <-> prev AND (a == b)
            if prev is None:
                clauses.append([-e, a, -b])
                clauses.append([-e, -a, b])
                clauses.append([e, a, b])
                clauses.append([e, -a, -b])
            else:
                clauses.append([-e, prev])
                clauses.append([-e, a, -b])
                clauses.append([-e, -a, b])
                clauses.append([e, -prev, a, b])
                clauses.append([e, -prev, -a, -b])
            prev = e
    return clauses, aux - nvar


def mindeg_clauses(n, d, idx):
    """Every vertex has degree >= d, with no auxiliary variables.

    "at least d of the n-1 row literals are true"
      <=>  no (n-1)-d+1 of them are all false
      <=>  for every subset S of the other vertices with |S| = n-d:
               OR_{w in S} x_{vw}

    Justification for using this at all (CRITICAL REDUCTION LEMMA).
    Let G be K_q-free with chi(G) >= k.  Delete vertices one at a time while
    the chromatic number stays >= k; let H be the result.  Then chi(H) >= k
    and chi(H - v) <= k-1 for every v, so chi(H) <= chi(H-v) + 1 = k, hence
    chi(H) = k and H is k-vertex-critical.  H is an induced subgraph of G,
    so H is K_q-free.  For v in V(H), no (k-1)-colouring of H-v extends to
    v, so v has a neighbour in every one of the k-1 colour classes, giving
    deg_H(v) >= k-1.
    Consequently: if for EVERY m with k <= m <= N the instance
    "K_q-free on m vertices, chi >= k, min degree >= k-1" is unsatisfiable,
    then n(k,q) > N.  The per-m runs are what make this sound; a single run
    at m = N would not be, because H may have fewer than N vertices.
    """
    out = []
    for v in range(n):
        others = [w for w in range(n) if w != v]
        for S in itertools.combinations(others, n - d):
            out.append(sorted(idx[(min(v, w), max(v, w))] + 1 for w in S))
    return out


def build(n, k, q, partitions, symbreak=False, mindeg=None):
    """Full CNF for CF(n,k,q) relaxed to the given list of partitions."""
    idx, _ = pair_index(n)
    nvar = n * (n - 1) // 2
    clauses = clique_clauses(n, q, idx)
    for part in partitions:
        clauses.append(block_clause(part, idx))
    if mindeg is not None:
        clauses.extend(mindeg_clauses(n, mindeg, idx))
    if symbreak:
        sb, naux = symbreak_clauses(n, idx)
        clauses.extend(sb)
        nvar += naux
    return nvar, clauses


def write_dimacs(path, nvar, clauses):
    with open(path, "w") as f:
        f.write(f"p cnf {nvar} {len(clauses)}\n")
        for cl in clauses:
            f.write(" ".join(map(str, cl)))
            f.write(" 0\n")


def read_partitions(path):
    """One partition per line; blocks separated by '|', vertices by ','."""
    parts = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            blocks = [
                [int(x) for x in blk.split(",") if x != ""]
                for blk in line.split("|")
            ]
            parts.append([b for b in blocks if b])
    return parts


def write_partitions(path, parts):
    with open(path, "w") as f:
        for p in parts:
            f.write("|".join(",".join(str(v) for v in sorted(b))
                             for b in p if b))
            f.write("\n")


def main():
    if len(sys.argv) < 6:
        print("usage: encode.py N K Q PARTITIONS_FILE OUT.cnf [--symbreak]")
        return 2
    n, k, q = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    parts = read_partitions(sys.argv[4])
    for p in parts:
        assert sorted(v for b in p for v in b) == list(range(n)), \
            "each line must be a partition of [n]"
        assert len(p) <= k - 1, f"partition has {len(p)} > {k-1} blocks"
    rest = sys.argv[6:]
    sb = "--symbreak" in rest
    md = None
    if "--mindeg" in rest:
        md = int(rest[rest.index("--mindeg") + 1])
    nvar, clauses = build(n, k, q, parts, symbreak=sb, mindeg=md)
    write_dimacs(sys.argv[5], nvar, clauses)
    print(f"n={n} k={k} q={q} partitions={len(parts)} "
          f"vars={nvar} clauses={len(clauses)} symbreak={sb} mindeg={md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

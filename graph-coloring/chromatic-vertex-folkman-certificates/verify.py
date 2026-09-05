"""Independent standard-library checker for chromatic vertex Folkman claims.

Nothing here imports encode.py or search.py: every clause family is
regenerated from scratch, from (n, k, q) and the partition list alone, by
code written separately from the generators.  A solver's own answer is never
trusted; only an LRAT refutation replayed here counts.

Subcommands
-----------
  lower N K Q PARTS.txt FORMULA.cnf PROOF.lrat [--symbreak]
      Certifies  n(K,Q) > N  ("no K_Q-free graph on N vertices has
      chromatic number >= K").  Checks that FORMULA.cnf is exactly the CNF
      determined by (N,K,Q,PARTS), that every line of PARTS is a partition
      of [N] into at most K-1 blocks, and replays PROOF.lrat to the empty
      clause.

  upper K Q WITNESS.txt
      Certifies  n(K,Q) <= |V|  from an explicit graph: checks K_Q-freeness
      and that no proper (K-1)-colouring exists (exhaustive, own search).

  symtest NMAX
      Brute-force soundness test of the symmetry-breaking clause family:
      for every n <= NMAX and every isomorphism class of graphs on n
      vertices, checks that at least one labelling satisfies the clauses.
      This is what makes a --symbreak lower bound sound.
"""

import itertools
import sys


# --------------------------------------------------------------- regenerate

def pairs_of(n):
    return [(u, v) for u in range(n) for v in range(u + 1, n)]


def var_of(n):
    """{u,v} -> DIMACS variable (1-based), lexicographic pair order."""
    d = {}
    i = 1
    for u in range(n):
        for v in range(u + 1, n):
            d[(u, v)] = i
            i += 1
    return d


def gen_clique(n, q, var):
    out = []
    for S in itertools.combinations(range(n), q):
        out.append(tuple(sorted(-var[(u, v)]
                                for u, v in itertools.combinations(S, 2))))
    return out


def gen_block(part, var):
    lits = set()
    for blk in part:
        for u, v in itertools.combinations(sorted(blk), 2):
            lits.add(var[(u, v)])
    return tuple(sorted(lits))


def gen_symbreak(n, var):
    """Regenerated independently; must match encode.symbreak_clauses.

    Constraint for the transposition (i,i+1): the vector
        ( a_{u,i} )_{u<i}  followed by  ( a_{i,w} )_{w>i+1}
    must be lexicographically >= the same vector with i replaced by i+1.
    Auxiliary "equal so far" variables continue the numbering after the
    n(n-1)/2 edge variables, allocated in the order the constraints are
    emitted.
    """
    clauses = []
    aux = n * (n - 1) // 2

    def lit(u, v):
        a, b = (u, v) if u < v else (v, u)
        return var[(a, b)]

    for i in range(n - 1):
        j = i + 1
        others = [w for w in range(n) if w != i and w != j]
        prev = None
        for t, w in enumerate(others):
            a, b = lit(i, w), lit(j, w)
            clauses.append(tuple(sorted((-b, a))) if prev is None
                           else tuple(sorted((-prev, -b, a))))
            if t == len(others) - 1:
                break
            aux += 1
            e = aux
            if prev is None:
                for cl in ((-e, a, -b), (-e, -a, b), (e, a, b), (e, -a, -b)):
                    clauses.append(tuple(sorted(cl)))
            else:
                for cl in ((-e, prev), (-e, a, -b), (-e, -a, b),
                           (e, -prev, a, b), (e, -prev, -a, -b)):
                    clauses.append(tuple(sorted(cl)))
            prev = e
    return clauses, aux - n * (n - 1) // 2


def read_parts(path, n, k):
    parts = []
    with open(path) as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            blocks = [[int(x) for x in b.split(",") if x != ""]
                      for b in line.split("|")]
            blocks = [b for b in blocks if b]
            flat = sorted(v for b in blocks for v in b)
            if flat != list(range(n)):
                raise SystemExit(f"line {ln}: not a partition of [{n}]")
            if len(blocks) > k - 1:
                raise SystemExit(f"line {ln}: {len(blocks)} blocks > {k-1}")
            parts.append(blocks)
    return parts


def read_dimacs(path):
    nvar = None
    clauses = []
    cur = []
    with open(path) as f:
        for line in f:
            if line.startswith("c"):
                continue
            if line.startswith("p"):
                nvar = int(line.split()[2])
                continue
            for tok in line.split():
                x = int(tok)
                if x == 0:
                    clauses.append(tuple(sorted(cur)))
                    cur = []
                else:
                    cur.append(x)
    return nvar, clauses


# ---------------------------------------------------------------- LRAT replay

def replay_lrat(clauses, path):
    """Replay an LRAT refutation.  RUP steps with hints only; RAT rejected."""
    db = {}
    for i, cl in enumerate(clauses, 1):
        db[i] = cl
    with open(path) as f:
        for raw in f:
            toks = raw.split()
            if not toks:
                continue
            idx = int(toks[0])
            if len(toks) > 1 and toks[1] == "d":
                for t in toks[2:]:
                    if t == "0":
                        break
                    db.pop(int(t), None)
                continue
            i = 1
            lits = []
            while toks[i] != "0":
                lits.append(int(toks[i]))
                i += 1
            i += 1
            hints = []
            while i < len(toks) and toks[i] != "0":
                h = int(toks[i])
                if h < 0:
                    raise SystemExit(f"step {idx}: RAT hint {h} rejected "
                                     "(this checker accepts RUP only)")
                hints.append(h)
                i += 1
            # unit propagation from the negation of `lits` through the hints
            assign = {}
            for l in lits:
                assign[abs(l)] = (l < 0)      # value making l false
            conflict = False
            for h in hints:
                cl = db.get(h)
                if cl is None:
                    raise SystemExit(f"step {idx}: missing hint clause {h}")
                unassigned = None
                sat = False
                cnt = 0
                for l in cl:
                    v = assign.get(abs(l))
                    if v is None:
                        cnt += 1
                        unassigned = l
                    elif v == (l > 0):
                        sat = True
                        break
                if sat:
                    raise SystemExit(f"step {idx}: hint clause {h} satisfied")
                if cnt == 0:
                    conflict = True
                    break
                if cnt != 1:
                    raise SystemExit(f"step {idx}: hint clause {h} not unit "
                                     f"({cnt} unassigned)")
                assign[abs(unassigned)] = (unassigned > 0)
            if not conflict:
                raise SystemExit(f"step {idx}: propagation did not conflict")
            db[idx] = tuple(sorted(lits))
            if not lits:
                return idx
    raise SystemExit("proof ended without deriving the empty clause")


# ---------------------------------------------------------------- colouring

def colourable(n, adjset, c):
    """True iff the graph admits a proper c-colouring.  Exhaustive."""
    colour = [-1] * n

    def rec(v, used):
        if v == n:
            return True
        for col in range(min(used + 1, c)):
            if any(colour[w] == col for w in adjset[v] if w < v):
                continue
            colour[v] = col
            if rec(v + 1, max(used, col + 1)):
                return True
            colour[v] = -1
        return False

    return rec(0, 0)


# ------------------------------------------------------------------ commands

def gen_mindeg(n, d, var):
    """Regenerated independently: every vertex has degree >= d."""
    out = []
    for v in range(n):
        others = [w for w in range(n) if w != v]
        for S in itertools.combinations(others, n - d):
            out.append(tuple(sorted(var[(min(v, w), max(v, w))] for w in S)))
    return out


def cmd_lower(argv):
    n, k, q = int(argv[0]), int(argv[1]), int(argv[2])
    parts = read_parts(argv[3], n, k)
    rest = argv[6:]
    sb = "--symbreak" in rest
    md = int(rest[rest.index("--mindeg") + 1]) if "--mindeg" in rest else None
    var = var_of(n)
    want = list(gen_clique(n, q, var))
    want += [gen_block(p, var) for p in parts]
    nvar = n * (n - 1) // 2
    if md is not None:
        if md != k - 1:
            raise SystemExit(f"--mindeg {md} must equal k-1 = {k-1}; the "
                             "critical reduction lemma justifies no other "
                             "value")
        want += gen_mindeg(n, md, var)
    if sb:
        sbcl, naux = gen_symbreak(n, var)
        want += sbcl
        nvar += naux
    got_nvar, got = read_dimacs(argv[4])
    if got_nvar != nvar:
        raise SystemExit(f"variable count {got_nvar} != regenerated {nvar}")
    if len(got) != len(want) or set(got) != set(want):
        raise SystemExit("DIMACS clause set differs from the regenerated one "
                         f"(file {len(got)} clauses, regenerated {len(want)})")
    step = replay_lrat(want, argv[5])
    if md is None:
        print(f"VERIFIED  n({k},{q}) > {n}: no K_{q}-free graph on {n} "
              f"vertices has chromatic number >= {k}")
    else:
        print(f"VERIFIED  no {k}-vertex-critical K_{q}-free graph on {n} "
              f"vertices (min degree >= {md}). Combine over all m <= N via "
              "the critical reduction lemma to get n(k,q) > N.")
    print(f"  partitions={len(parts)} clauses={len(want)} vars={nvar} "
          f"symbreak={sb} mindeg={md} empty clause at LRAT step {step}")


def cmd_upper(argv):
    k, q = int(argv[0]), int(argv[1])
    with open(argv[2]) as f:
        toks = f.read().split()
    n = int(toks[0])
    es = [int(x) for x in toks[1:]]
    adjset = [set() for _ in range(n)]
    edges = set()
    for a, b in zip(es[0::2], es[1::2]):
        adjset[a].add(b)
        adjset[b].add(a)
        edges.add((min(a, b), max(a, b)))
    for S in itertools.combinations(range(n), q):
        if all((u, v) in edges for u, v in itertools.combinations(S, 2)):
            raise SystemExit(f"NOT K_{q}-free: clique {S}")
    if colourable(n, adjset, k - 1):
        raise SystemExit(f"graph IS ({k-1})-colourable, so chi < {k}")
    print(f"VERIFIED  n({k},{q}) <= {n}: the given graph on {n} vertices "
          f"({len(edges)} edges) is K_{q}-free and has chromatic number >= {k}")


def lex_predicate(n, adjbit):
    """The mathematical symmetry-breaking condition, stated directly.

    For every i, comparing the transposition (i,i+1):
        ( a_{u,i} )_{u<i} ++ ( a_{i,w} )_{w>i+1}
          >=_lex
        ( a_{u,i+1} )_{u<i} ++ ( a_{i+1,w} )_{w>i+1}
    """
    for i in range(n - 1):
        j = i + 1
        for w in [x for x in range(n) if x != i and x != j]:
            a, b = adjbit(i, w), adjbit(j, w)
            if a != b:
                if a < b:
                    return False
                break
    return True


def cmd_symtest(argv):
    """Two independent soundness tests of the symmetry-breaking family.

    (B) encoding test: for small n, the CNF is satisfiable by some extension
        of an edge assignment iff lex_predicate holds for it.
    (A) covering test: the lexicographically largest labelling in every
        isomorphism class satisfies lex_predicate, so adding the clauses
        cannot remove the last witness of any isomorphism class.
    """
    nmax = int(argv[0])

    # ---- (B) encoding matches the stated predicate
    for n in range(3, min(nmax, 5) + 1):
        var = var_of(n)
        sbcl, naux = gen_symbreak(n, var)
        prs = pairs_of(n)
        m = len(prs)
        pi = {p: i for i, p in enumerate(prs)}

        def bit(mask, u, v):
            a, b = (u, v) if u < v else (v, u)
            return mask >> pi[(a, b)] & 1

        bad = 0
        for mask in range(1 << m):
            want = lex_predicate(n, lambda u, v: bit(mask, u, v))
            base = [None] + [bool(mask >> i & 1) for i in range(m)]
            got = False
            for bits in range(1 << naux):
                assign = base + [bool(bits >> i & 1) for i in range(naux)]
                if all(any(assign[abs(l)] == (l > 0) for l in cl)
                       for cl in sbcl):
                    got = True
                    break
            if got != want:
                bad += 1
        if bad:
            raise SystemExit(f"n={n}: CNF and predicate disagree on {bad} "
                             "assignments -- encoding is WRONG")
        print(f"(B) n={n}: CNF satisfiable <=> lex predicate, on all "
              f"{1 << m} edge assignments  OK")

    # ---- (A) every isomorphism class keeps a witness
    for n in range(3, nmax + 1):
        prs = pairs_of(n)
        m = len(prs)
        pi = {p: i for i, p in enumerate(prs)}
        perms = list(itertools.permutations(range(n)))
        # remap[perm][bit] = image bit position
        remap = []
        for perm in perms:
            r = [0] * m
            for (u, v), i in pi.items():
                a, b = perm[u], perm[v]
                r[i] = pi[(min(a, b), max(a, b))]
            remap.append(r)
        # Row-major lexicographic order: pair 0 = (0,1) is the MOST
        # significant position, so weight pair index i by 1 << (m-1-i).
        def val(msk):
            s = 0
            for i in range(m):
                if msk >> i & 1:
                    s |= 1 << (m - 1 - i)
            return s

        classes = 0
        for mask in range(1 << m):
            best, bestv = -1, -1
            for r in remap:
                s = 0
                mm = mask
                i = 0
                while mm:
                    if mm & 1:
                        s |= 1 << r[i]
                    mm >>= 1
                    i += 1
                sv = val(s)
                if sv > bestv:
                    best, bestv = s, sv
            if best != mask:
                continue          # not the lex-max representative
            classes += 1
            if not lex_predicate(n, lambda u, v: (
                    mask >> pi[(min(u, v), max(u, v))] & 1)):
                raise SystemExit(f"n={n}: lex-max graph {mask} FAILS the "
                                 "predicate -- symmetry breaking is UNSOUND")
        print(f"(A) n={n}: all {classes} isomorphism classes keep their "
              f"lex-max labelling  OK")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cmd, rest = sys.argv[1], sys.argv[2:]
    {"lower": cmd_lower, "upper": cmd_upper, "symtest": cmd_symtest}[cmd](rest)
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""The exact 4-orbit fixed-point bound, not the Ramsey-arithmetic one.

`orbitbound.py` proves, for any G <= Aut(F) with F a (5,5)-graph and any
G-orbit O,

    |Fix(G)| <= R(5-w,5) - 1 + R(5,5-a) - 1,   w = omega(F[O]), a = alpha(F[O]),

which at |O| = 4 gives 26.  That is arithmetic on two Ramsey numbers: it bounds
|A| and |B| separately and adds.  It ignores the fact that A and B sit in ONE
graph and constrain each other.  This file removes that slack and gets the
exact value.

THE REDUCTION.  Let O be an orbit of size 4 and F = A + B as above.

  * If F[O] has an edge {x,y} and a non-edge {x,z} (the shapes C_4 and 2K_2 --
    every mixed shape), then:
      - a triangle in A plus x, y is a K_5, so A is triangle-free; A has no
        I_5; hence A IS a (3,5)-graph.
      - an independent 3-set in B plus x, z is an I_5, so B has no I_3; B has
        no K_5; hence the COMPLEMENT of B is a (3,5)-graph.
      - a clique meeting both A and O and B is impossible (B misses O), and
        likewise an independent set meeting A and O and B.  So O imposes
        NOTHING FURTHER: it has already been fully used.
    The question collapses to: how large can A + B be, with A a (3,5,|A|)-graph,
    B the complement of a (3,5,|B|)-graph, and A + B together a (5,5)-graph?
  * If F[O] is empty then B is empty (O is an I_4, so one more vertex would be
    an I_5) and A is a (4,5)-graph, so |Fix| <= 24, and 24 is attained: join any
    (4,5,24)-graph to all of an independent 4-set.
  * If F[O] is a K_4 the complement argument gives the same 24.

So the arithmetic bound 26 can only be beaten in the mixed shapes, and the
homogeneous shapes already reach 24.  Deciding f = 26 and f = 25 therefore
decides the true bound, because anything below 25 is 24 regardless.

WHY THE SEARCH IS SMALL.  A is a (3,5,|A|)-graph and the complement of B is
one too, and those catalogues are COMPLETE and tiny at the sizes that matter:
one graph at 13, twelve at 12.  So f = 26 is a single pair of fixed graphs with
169 free cross-edges, and f = 25 is twelve pairs with 156.  Everything is
decided by a solver and every UNSAT is certified through drat-trim to LRAT --
the same chain as the rest of this directory.

    python3 orbit4_exact.py
"""
import itertools
import os
import subprocess
import sys
import tempfile

import r45bounds as R

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = ("/Users/abuzark/.discovery-research-team/workspaces/researcher-3/"
           "scratch")
TOOLS = f"{SCRATCH}/tools"
CAD = f"{TOOLS}/cadical/build/cadical"
DTM = f"{TOOLS}/drat-trim/drat-trim"
# The |O| = 2 and |O| = 3 tightness probes are a side question -- one witness
# each would show r1's 37 and the 28 of the table are also unimprovable.  They
# are capped so that they cannot hold up the |O| = 4 result, which is the one
# the order-4 row needs.
TIGHT_CAP = 900


def load35(n):
    """The complete catalogue of (3,5,n)-graphs, each re-verified here."""
    path = f"{SCRATCH}/r45cert/r35_{n}.g6"
    out = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            m, adj = R.g6_decode(line)
            if m != n or not R.is_good(m, adj, 3, 5):
                raise SystemExit(f"{path}: {line} is not a (3,5,{n})-graph")
            out.append(adj)
    return out


def complement(n, adj):
    full = (1 << n) - 1
    return [(~adj[u]) & full & ~(1 << u) for u in range(n)]


def build(A, B):
    """CNF for: is there a (5,5)-graph on A + B extending the two given
    induced subgraphs, with the cross edges free?

    Variables: one per cross pair (i in A, j in B).  Internal pairs are fixed
    by A and B, so their literals are decided at build time and the clause is
    either dropped (already satisfied) or shortened.
    """
    a, b = len(A), len(B)
    n = a + b
    var = {}
    for i in range(a):
        for j in range(b):
            var[(i, a + j)] = len(var) + 1

    def lit(u, v):
        """+k if the pair is a free variable, True/False if it is fixed."""
        if u > v:
            u, v = v, u
        if v < a:
            return bool((A[u] >> v) & 1)
        if u >= a:
            return bool((B[u - a] >> (v - a)) & 1)
        return var[(u, v)]

    cls = []
    for S in itertools.combinations(range(n), 5):
        pairs = [lit(u, v) for u, v in itertools.combinations(S, 2)]
        # forbid K_5: some pair is a non-edge
        c, sat = [], False
        for p in pairs:
            if p is False:
                sat = True
                break
            if p is not True:
                c.append(-p)
        if not sat:
            if not c:
                return None, None                # a K_5 is already present
            cls.append(tuple(sorted(set(c))))
        # forbid I_5: some pair is an edge
        c, sat = [], False
        for p in pairs:
            if p is True:
                sat = True
                break
            if p is not False:
                c.append(p)
        if not sat:
            if not c:
                return None, None                # an I_5 is already present
            cls.append(tuple(sorted(set(c))))
    return len(var), sorted(set(cls))


def solve(nvar, cls, work, certify):
    os.makedirs(work, exist_ok=True)
    cnf = os.path.join(work, "f.cnf")
    with open(cnf, "w") as fh:
        fh.write(f"p cnf {nvar} {len(cls)}\n")
        for c in cls:
            fh.write(" ".join(map(str, c)) + " 0\n")
    if not certify:
        r = subprocess.run([CAD, "-q", cnf], capture_output=True, text=True)
        return r.returncode, None
    drat = os.path.join(work, "f.drat")
    lrat = os.path.join(work, "f.lrat")
    r = subprocess.run([CAD, "-q", "--binary=false", cnf, drat],
                       capture_output=True, text=True)
    if r.returncode != 20:
        return r.returncode, None
    v = subprocess.run([DTM, cnf, drat, "-L", lrat], capture_output=True,
                       text=True, timeout=3600)
    ok = "s VERIFIED" in v.stdout
    return 20, (lrat if ok else None)


def sat_witness(nvar, cls, work, cap=None):
    """Read the model back and re-verify the whole graph independently."""
    cnf = os.path.join(work, "w.cnf")
    os.makedirs(work, exist_ok=True)
    with open(cnf, "w") as fh:
        fh.write(f"p cnf {nvar} {len(cls)}\n")
        for c in cls:
            fh.write(" ".join(map(str, c)) + " 0\n")
    cmd = ([CAD, "-q", cnf] if cap is None
           else ["timeout", str(cap), CAD, "-q", cnf])
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 10:
        return None
    model = set()
    for line in r.stdout.splitlines():
        if line.startswith("v "):
            for x in line[2:].split():
                if int(x) > 0:
                    model.add(int(x))
    return model


def realise(A, B, model, shape="C4"):
    """Rebuild the full configuration A + B + O from a model and return it.

    Vertex order: A, then B, then the four orbit vertices.  The orbit gets the
    shape asked for; A is joined to all of it, B to none.
    """
    a, b = len(A), len(B)
    n = a + b + 4
    adj = [0] * n

    def join(u, v):
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    for i, j in itertools.combinations(range(a), 2):
        if (A[i] >> j) & 1:
            join(i, j)
    for i, j in itertools.combinations(range(b), 2):
        if (B[i] >> j) & 1:
            join(a + i, a + j)
    k = 0
    for i in range(a):
        for j in range(b):
            k += 1
            if k in model:
                join(i, a + j)
    O = [a + b + i for i in range(4)]
    if shape == "C4":
        for i in range(4):
            join(O[i], O[(i + 1) % 4])
    elif shape == "2K2":
        join(O[0], O[2])
        join(O[1], O[3])
    for i in range(a):
        for x in O:
            join(i, x)
    return n, adj, O


def g6_encode(n, adj):
    """graph6, so the witness is readable by the same decoder as everything
    else here.  Round-tripped through r45bounds.g6_decode before it is used."""
    if n > 62:
        raise SystemExit("g6_encode: only n <= 62 needed here")
    bits = []
    for v in range(1, n):
        for u in range(v):
            bits.append((adj[u] >> v) & 1)
    bits += [0] * (-len(bits) % 6)
    out = chr(n + 63)
    for i in range(0, len(bits), 6):
        x = 0
        for b in bits[i:i + 6]:
            x = (x << 1) | b
        out += chr(x + 63)
    m, back = R.g6_decode(out)
    if m != n or back != list(adj):
        raise SystemExit("g6_encode does not round-trip through the decoder")
    return out


def audit(n, adj, O, a, b):
    """Independent re-verification of a realised configuration, from scratch."""
    fails = []
    if not R.is_good(n, adj, 5, 5):
        fails.append("not a (5,5)-graph")
    Aadj = [adj[i] & ((1 << a) - 1) for i in range(a)]
    if not R.is_good(a, Aadj, 3, 5):
        fails.append("A is not a (3,5)-graph")
    Badj = [(adj[a + i] >> a) & ((1 << b) - 1) for i in range(b)]
    if not R.is_good(b, Badj, 5, 3):
        fails.append("B is not a (5,3)-graph")
    for v in range(a + b):
        joined = {(adj[v] >> x) & 1 for x in O}
        if len(joined) != 1:
            fails.append(f"vertex {v} joined to some but not all of O")
        want = 1 if v < a else 0
        if joined != {want}:
            fails.append(f"vertex {v} on the wrong side of the split")
    return fails


def try_split(a, b, certify, verbose):
    """Every pair (A from the (3,5,a) catalogue, B the complement of one from
    the (3,5,b) catalogue).  Returns ('SAT', ...) or ('UNSAT', count, lrats)."""
    As, Bs = load35(a), [complement(b, g) for g in load35(b)]
    total = len(As) * len(Bs)
    done, lrats = 0, []
    for ia, A in enumerate(As):
        for ib, B in enumerate(Bs):
            nvar, cls = build(A, B)
            if nvar is None:
                done += 1
                continue
            work = os.path.join(SCRATCH, "ob", f"s{a}_{b}_{ia}_{ib}")
            rc, lrat = solve(nvar, cls, work, certify)
            if rc == 10:
                return ("SAT", (a, b, ia, ib, nvar, cls, work))
            if rc != 20:
                raise SystemExit(f"no verdict at ({a},{b}) pair {ia},{ib}")
            done += 1
            if lrat:
                lrats.append(lrat)
            if verbose:
                print(f"      pair {done}/{total}: {nvar} vars, {len(cls)} "
                      f"clauses, UNSAT"
                      + ("  [LRAT verified]" if lrat else ""))
    return ("UNSAT", done, lrats)


def positive_control():
    """The encoder must ADMIT configurations that exist.

    A formula that has lost its solutions still refutes, so before believing
    any UNSAT above, force the encoder to produce real graphs at sizes where
    they obviously exist -- and rebuild each model into an actual graph on
    A + B + O and re-verify, from scratch, that it is a (5,5)-graph with A
    triangle-free, alpha(B) <= 2, A joined to all of O and B to none.
    """
    print("POSITIVE CONTROL on this encoder")
    ok = 0
    for a, b in ((13, 7), (12, 8), (11, 9), (10, 10), (9, 11), (8, 12),
                 (7, 13)):
        A, B = load35(a)[0], complement(b, load35(b)[0])
        nvar, cls = build(A, B)
        if nvar is None:
            print(f"   |A|={a}, |B|={b}: rejected at build time -- SUSPECT")
            continue
        work = os.path.join(SCRATCH, "ob", f"pc{a}_{b}")
        model = sat_witness(nvar, cls, work)
        if model is None:
            print(f"   |A|={a}, |B|={b}: encoder says UNSAT -- TOO TIGHT")
            continue
        # rebuild the whole configuration, orbit included, and re-verify
        n = a + b + 4                       # 4 orbit vertices, shape C_4
        adj = [0] * n
        def join(u, v):
            adj[u] |= 1 << v
            adj[v] |= 1 << u
        for i, j in itertools.combinations(range(a), 2):
            if (A[i] >> j) & 1:
                join(i, j)
        for i, j in itertools.combinations(range(b), 2):
            if (B[i] >> j) & 1:
                join(a + i, a + j)
        k = 0
        for i in range(a):
            for j in range(b):
                k += 1
                if k in model:
                    join(i, a + j)
        O = [a + b + i for i in range(4)]
        for i in range(4):                  # C_4 on the orbit
            join(O[i], O[(i + 1) % 4])
        for i in range(a):                  # A joined to all of O
            for x in O:
                join(i, x)
        good = R.is_good(n, adj, 5, 5)
        Aok = R.is_good(a, [adj[i] & ((1 << a) - 1) for i in range(a)], 3, 5)
        print(f"   |A|={a}, |B|={b}: SAT, rebuilt on {n} vertices -- "
              f"(5,5)-graph: {good}, A is a (3,5)-graph: {Aok}")
        if not (good and Aok):
            raise SystemExit("positive control FAILED: the encoder admits a "
                             "configuration that is not what it claims")
        ok += 1
    print(f"   {ok} configurations admitted and independently re-verified.\n")
    return ok


def load45(path, n):
    out = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m, adj = R.g6_decode(line)
            if m != n or not R.is_good(m, adj, 4, 5):
                raise SystemExit(f"{path}: not a (4,5,{n})-graph")
            out.append(adj)
    return out


def tightness():
    """Is the arithmetic bound attained at the other orbit sizes too?

    Tightness needs only ONE witness, so a single choice of A and B suffices
    where a refutation would have needed the whole catalogue.

      |O| = 2, orbit an edge:  A a (3,5,13)-graph, B a (5,4,24)-graph -> 37
      |O| = 3, orbit a K_3:    A an independent 4-set,  B as above    -> 28
      |O| = 4, mixed:          A a (3,5,13)-graph, B a (5,3,13)-graph -> 26
    """
    print("IS THE ARITHMETIC BOUND ATTAINED AT THE OTHER ORBIT SIZES?")
    b45 = load45(os.path.join(HERE, "r45_24_e132.g6"), 24)
    B24 = complement(24, b45[0])          # a (5,4,24)-graph
    A13 = load35(13)[0]
    A4 = [0, 0, 0, 0]                     # an independent 4-set
    jobs = [(2, "an edge", A13, B24, 13, 24),
            (3, "a K_3", A4, B24, 4, 24)]
    for m, shape, A, B, a, b in jobs:
        nvar, cls = build(A, B)
        if nvar is None:
            print(f"   |O| = {m} ({shape}): rejected at build time")
            continue
        work = os.path.join(SCRATCH, "ob", f"tight{m}")
        model = sat_witness(nvar, cls, work, cap=TIGHT_CAP)
        verdict = ("ATTAINED" if model else
                   f"no verdict within {TIGHT_CAP} s for this choice of A, B")
        print(f"   |O| = {m}, orbit {shape}: |A| = {a}, |B| = {b}, "
              f"bound {a + b} -- {verdict}")
        if model:
            n = a + b
            adj = [0] * n
            for i, j in itertools.combinations(range(a), 2):
                if (A[i] >> j) & 1:
                    adj[i] |= 1 << j
                    adj[j] |= 1 << i
            for i, j in itertools.combinations(range(b), 2):
                if (B[i] >> j) & 1:
                    adj[a + i] |= 1 << (a + j)
                    adj[a + j] |= 1 << (a + i)
            k = 0
            for i in range(a):
                for j in range(b):
                    k += 1
                    if k in model:
                        adj[i] |= 1 << (a + j)
                        adj[a + j] |= 1 << i
            print(f"      fixed set of {n} vertices rebuilt and re-verified: "
                  f"(5,5)-graph = {R.is_good(n, adj, 5, 5)}")
    print()


def main():
    certify = "--fast" not in sys.argv
    print("THE EXACT 4-ORBIT BOUND")
    print("  arithmetic bound (orbitbound.py):        26")
    print("  homogeneous shapes reach:                24")
    print("  so only f = 26 and f = 25 are in doubt.\n")
    print("Catalogue sizes, each graph re-verified here as a (3,5,n)-graph:")
    for n in (11, 12, 13):
        print(f"   (3,5,{n})-graphs: {len(load35(n))}")
    print()
    positive_control()
    tightness()

    best = 24
    mixed = None
    for f, splits in ((26, [(13, 13)]), (25, [(13, 12)]),
                      (24, [(13, 11), (12, 12)])):
        print(f"f = {f}:")
        allun = True
        for a, b in splits:
            print(f"   |A| = {a} (a (3,5,{a})-graph), |B| = {b} (complement "
                  f"of a (3,5,{b})-graph)")
            res = try_split(a, b, certify, verbose=(len(splits) == 1))
            if res[0] == "SAT":
                allun = False
                _, _, ia, ib, nvar, cls, work = res[1]
                model = sat_witness(nvar, cls, work)
                A = load35(a)[ia]
                B = complement(b, load35(b)[ib])
                for shape in ("C4", "2K2"):
                    n, adj, O = realise(A, B, model, shape)
                    fails = audit(n, adj, O, a, b)
                    if shape == "C4" and fails:
                        raise SystemExit(f"realised witness fails audit: "
                                         f"{fails}")
                n, adj, O = realise(A, B, model, "C4")
                g6 = g6_encode(n, adj)
                out = os.path.join(HERE, "orbit4_witness.g6")
                with open(out, "w") as fh:
                    fh.write(f"# A (5,5,{n})-graph in which a 4-set carries a "
                             f"C_4 and each of the other {a+b} vertices is "
                             f"joined\n")
                    fh.write(f"# to all four of it or to none: |A| = {a} "
                             f"joined to all, |B| = {b} to none.\n")
                    fh.write(f"# Vertices {a+b}..{n-1} are the 4-set; "
                             f"0..{a-1} are A and {a}..{a+b-1} are B.\n")
                    fh.write(g6 + "\n")
                print(f"   REALISED: |A| = {a}, |B| = {b} is SATISFIABLE.")
                print(f"   Witness rebuilt on {n} vertices and audited from "
                      f"scratch: it is a (5,5,{n})-graph, A is a (3,5,{a})-"
                      f"graph,")
                print(f"   B is a (5,3,{b})-graph, and every one of the {a+b} "
                      f"vertices is joined to all four orbit vertices or to "
                      f"none.")
                print(f"   Written to orbit4_witness.g6 as an adjacency "
                      f"matrix.")
                best = max(best, f)
                mixed = max(mixed or 0, f)
            else:
                print(f"   all {res[1]} pairs UNSAT"
                      + (f", {len(res[2])} certified to LRAT" if res[2]
                         else ""))
        if allun:
            print(f"   => no mixed 4-orbit fixes {f} points\n")
        else:
            print()
            break
    print(f"EXACT BOUND at |O| = 4:  |Fix(G)| <= {best}")
    if mixed is None:
        print("   mixed shapes (C_4, 2K_2) cannot reach 24 at all; the bound")
        print("   is attained only by the homogeneous shapes (empty, K_4),")
        print("   where a (4,5,24)-graph joined to an independent 4-set works.")
    print(f"   arithmetic gave 26; the true value is {best}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

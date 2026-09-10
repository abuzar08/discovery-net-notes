"""How far does a 26-point fixed set survive? The global-count route.

principal-1, pass 40: *"the exactness question you opened is yours ... whether
a genuinely multi-orbit argument can [beat 26], and what the true maximum is,
is a question about (5,5)-graphs nobody is currently asking, and you have the
catalogues and controls to ask it."*

WHERE THIS PICKS UP.  `orbit4_exact.py` showed the bound |Fix(G)| <= 26 at
|O| = 4 cannot be improved by any argument that looks at one orbit and the
split it induces: the configuration

    O   a 4-set carrying a C_4 (or 2K_2),
    A   13 vertices joined to all of O, inducing the unique (3,5,13)-graph,
    B   13 vertices joined to none of O, inducing its complement,

is realisable, and the witness is a genuine (5,5,30)-graph (`orbit4_witness.g6`).
ORBIT-FIXED-POINT-BOUND.md section 5 says the only route left is the global
count n = 42.  This file takes that route.

THE QUESTION.  For which n does a (5,5,n)-graph contain that configuration?
Deleting any vertex outside the configuration keeps it, so feasibility is
MONOTONE DECREASING in n and there is a threshold n*.  We know n* >= 30.  If
n* < 42 then no (5,5,42)-graph has a group fixing 26 points through a 4-orbit,
and since c_1 is even for every order-4 type, the bound drops 26 -> 24.

WHY IT IS ASKABLE.  At f = 26 both halves are forced to be UNIQUE graphs --
R(3,5) = 14 and the (3,5,13)-graph is the only one -- so there is no catalogue
to sweep.  The only freedom is the 169 A-B cross edges plus everything touching
the n - 30 extra vertices.  At n = 42 that is 595 variables.

    python3 fixmax.py [--from N] [--to N] [--cap SECONDS]
"""
import itertools
import os
import subprocess
import sys
import time

import r45bounds as R
import orbit4_exact as X

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = ("/Users/abuzark/.discovery-research-team/workspaces/researcher-3/"
           "scratch")
CAD = f"{SCRATCH}/tools/cadical/build/cadical"
DTM = f"{SCRATCH}/tools/drat-trim/drat-trim"


def duality_note():
    """The two mixed shapes are not independent problems.

    Complementing a (5,5,n)-graph gives a (5,5,n)-graph.  Under it, a vertex
    joined to all of O becomes one joined to none, so A and B swap; and the
    orbit's own graph complements, and on 4 points the complement of C_4 is
    exactly 2K_2.  Hence

        feasible(|A| = a, |B| = b, C_4)  <=>  feasible(|A| = b, |B| = a, 2K_2).

    So only one shape ever needs to be run.  It also explains a pattern in the
    recorded sweeps that looked like coincidence: at n = 34 the C_4 witness had
    split (11,13) and the 2K_2 witness had (13,11).

    Verified on the audited n = 30 witness: complementing it gives a genuine
    (5,5,30)-graph, the orbit shape becomes {(0,2),(1,3)} = 2K_2, and the
    A-side and B-side counts swap.
    """
    return True


def shape_adj(shape):
    """The orbit's own induced graph, on 4 points, as an edge set."""
    if shape == "C4":
        return {(0, 1), (1, 2), (2, 3), (0, 3)}
    if shape == "2K2":
        return {(0, 2), (1, 3)}
    raise SystemExit(f"unknown shape {shape}")


def build(n, shape, A=None, B=None):
    """CNF for: a (5,5,n)-graph containing the configuration.

    Layout: A = 0..a-1, B = a..a+b-1, O = a+b..a+b+3, X = the rest.
    Fixed: A and B internally, O internally (the shape), A-O all edges,
    B-O all non-edges.  Free: A-B, and every pair touching X.

    With A and B defaulted this is the f = 26 configuration, where both halves
    are forced to be the unique (3,5,13)-graph and its complement.  Passing
    them explicitly gives the smaller fixed sets, where there is a catalogue to
    sweep.
    """
    if A is None:
        A = X.load35(13)[0]
    if B is None:
        B = X.complement(13, X.load35(13)[0])
    a, b = len(A), len(B)
    Oe = shape_adj(shape)

    var, nv = {}, 0

    def fresh(u, v):
        nonlocal nv
        nv += 1
        var[(u, v)] = nv
        return nv

    def lit(u, v):
        if u > v:
            u, v = v, u
        if v < a:                                  # inside A
            return bool((A[u] >> v) & 1)
        if a <= u and v < a + b:                   # inside B
            return bool((B[u - a] >> (v - a)) & 1)
        if a + b <= u and v < a + b + 4:           # inside O
            return (u - a - b, v - a - b) in Oe
        if u < a and a + b <= v < a + b + 4:       # A-O: all joined
            return True
        if a <= u < a + b and a + b <= v < a + b + 4:   # B-O: none joined
            return False
        if (u, v) in var:                          # already a variable
            return var[(u, v)]
        return fresh(u, v)

    # allocate every free variable up front, in a stable order
    for u in range(n):
        for v in range(u + 1, n):
            lit(u, v)

    cls = []
    for S in itertools.combinations(range(n), 5):
        pairs = [lit(u, v) for u, v in itertools.combinations(S, 2)]
        c, sat = [], False                          # forbid K_5
        for p in pairs:
            if p is False:
                sat = True
                break
            if p is not True:
                c.append(-p)
        if not sat:
            if not c:
                return None, None, None
            cls.append(tuple(sorted(set(c))))
        c, sat = [], False                          # forbid I_5
        for p in pairs:
            if p is True:
                sat = True
                break
            if p is not False:
                c.append(p)
        if not sat:
            if not c:
                return None, None, None
            cls.append(tuple(sorted(set(c))))
    return nv, sorted(set(cls)), var


def precompute(n, shape, a, b):
    """Build the 5-subset structure ONCE for given (n, shape, a, b).

    `build` re-enumerates all C(n,5) subsets for every catalogue pair, and at
    n = 35 with 354 pairs that is the whole cost of the sweep -- the solver is
    not the bottleneck, the clause construction is.  Everything except the
    A-internal and B-internal pair values is the same for every pair, so it
    can be done once.

    For each 5-subset we record the A-internal and B-internal pairs as
    bitmasks, whether some pair is already fixed False (then no K_5 clause is
    ever needed) or fixed True (then no I_5 clause is), and the free variables.
    Specialising to a pair is then four integer operations per subset.
    """
    ai = {}
    for k, (u, v) in enumerate(itertools.combinations(range(a), 2)):
        ai[(u, v)] = k
    bi = {}
    for k, (u, v) in enumerate(itertools.combinations(range(b), 2)):
        bi[(a + u, a + v)] = k
    Oe = shape_adj(shape)
    o0 = a + b

    var, nv = {}, 0
    for u in range(n):
        for v in range(u + 1, n):
            if (u, v) in ai or (u, v) in bi:
                continue
            if o0 <= u and v < o0 + 4:
                continue
            if u < a and o0 <= v < o0 + 4:
                continue
            if a <= u < o0 and o0 <= v < o0 + 4:
                continue
            nv += 1
            var[(u, v)] = nv

    k5, i5 = [], []
    for S in itertools.combinations(range(n), 5):
        am = bm = 0
        ftrue = ffalse = False
        free = []
        for u, v in itertools.combinations(S, 2):
            if (u, v) in ai:
                am |= 1 << ai[(u, v)]
            elif (u, v) in bi:
                bm |= 1 << bi[(u, v)]
            elif o0 <= u and v < o0 + 4:
                if (u - o0, v - o0) in Oe:
                    ftrue = True
                else:
                    ffalse = True
            elif u < a and o0 <= v < o0 + 4:
                ftrue = True
            elif a <= u < o0 and o0 <= v < o0 + 4:
                ffalse = True
            else:
                free.append(var[(u, v)])
        fr = tuple(sorted(set(free)))
        if not ffalse:
            k5.append((am, bm, fr))
        if not ftrue:
            i5.append((am, bm, fr))
    return nv, k5, i5


def specialise(pre, Abits, Bbits):
    """Clause list for one catalogue pair, from the precomputed structure."""
    nv, k5, i5 = pre
    cls = set()
    for am, bm, fr in k5:                    # forbid K_5: need a non-edge
        if (am & ~Abits) or (bm & ~Bbits):
            continue                         # already has one
        if not fr:
            return None
        cls.add(tuple(sorted(-x for x in fr)))
    for am, bm, fr in i5:                    # forbid I_5: need an edge
        if (am & Abits) or (bm & Bbits):
            continue
        if not fr:
            return None
        cls.add(fr)
    return nv, sorted(cls)


def bits_of(g, m):
    """Edge bitmask of an m-vertex graph, indexed as in `precompute`."""
    out = 0
    for k, (u, v) in enumerate(itertools.combinations(range(m), 2)):
        if (g[u] >> v) & 1:
            out |= 1 << k
    return out


def run(n, shape, cap, certify):
    nv, cls, var = build(n, shape)
    if nv is None:
        return "BUILD-UNSAT", 0, 0, None
    work = os.path.join(SCRATCH, "fixmax", f"n{n}_{shape}")
    os.makedirs(work, exist_ok=True)
    cnf = os.path.join(work, "f.cnf")
    with open(cnf, "w") as fh:
        fh.write(f"p cnf {nv} {len(cls)}\n")
        for c in cls:
            fh.write(" ".join(map(str, c)) + " 0\n")
    drat = os.path.join(work, "f.drat")
    cmd = ["timeout", str(cap), CAD, "-q"]
    if certify:
        cmd += ["--binary=false", cnf, drat]
    else:
        cmd += [cnf]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 10:
        model = set()
        for line in r.stdout.splitlines():
            if line.startswith("v "):
                for x in line[2:].split():
                    if int(x) > 0:
                        model.add(int(x))
        return "SAT", nv, len(cls), (model, var)
    if r.returncode == 20:
        if certify:
            lrat = os.path.join(work, "f.lrat")
            v = subprocess.run([DTM, cnf, drat, "-L", lrat],
                               capture_output=True, text=True, timeout=7200)
            ok = "s VERIFIED" in v.stdout
            return ("UNSAT-LRAT" if ok else "UNSAT-UNVERIFIED"), nv, len(cls), None
        return "UNSAT", nv, len(cls), None
    return "NO-VERDICT", nv, len(cls), None


def rebuild(n, shape, model, var):
    """Turn a model into a graph and re-verify it from scratch."""
    A = X.load35(13)[0]
    B = X.complement(13, X.load35(13)[0])
    a = b = 13
    Oe = shape_adj(shape)
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
    for i, j in Oe:
        join(26 + i, 26 + j)
    for i in range(a):
        for x in range(26, 30):
            join(i, x)
    for (u, v), k in var.items():
        if k in model:
            join(u, v)
    return adj


def audit(n, adj, shape):
    fails = []
    if not R.is_good(n, adj, 5, 5):
        fails.append(f"not a (5,5,{n})-graph")
    O = list(range(26, 30))
    for v in list(range(26)):
        joined = {(adj[v] >> x) & 1 for x in O}
        if len(joined) != 1:
            fails.append(f"vertex {v} joined to some but not all of O")
        want = 1 if v < 13 else 0
        if joined != {want}:
            fails.append(f"vertex {v} on the wrong side")
    Aadj = [adj[i] & ((1 << 13) - 1) for i in range(13)]
    if not R.is_good(13, Aadj, 3, 5):
        fails.append("A is not a (3,5,13)-graph")
    return fails


def homogeneous_bound(n=42, verbose=True):
    """The homogeneous shapes need no solver at all.

    Let O be an empty 4-orbit (an I_4).  Then B is empty and A, joined to all
    of O, is a (4,5)-graph, so f = |A|.  Every x in O is joined to all of A, so
    deg(x) >= f, and the degree window gives deg(x) <= 24, so x has at most
    24 - f neighbours outside A u O.

    There are n - f - 4 vertices outside A u O.  At most 4(24 - f) of them are
    adjacent to any vertex of O, so at least

        (n - f - 4) - 4(24 - f) = 3f + (n - 100)

    are adjacent to none of O.  Any such y gives an independent 5-set with the
    independent O.  So that count must be <= 0:

        f <= (100 - n) / 3.

    At n = 42 that is f <= 19, and f is even, so f <= 18 -- well below the 24
    the arithmetic allowed.  The K_4 shape is the complement of this argument.
    """
    cap = (100 - n) / 3.0
    bound = int(cap // 1)
    even = bound if bound % 2 == 0 else bound - 1
    if verbose:
        print("HOMOGENEOUS SHAPES -- no solver needed")
        print(f"   empty (or K_4) 4-orbit at n = {n}: an independent 5-set "
              f"appears unless")
        print(f"   3f + (n - 100) <= 0, i.e. f <= {cap:.2f}, so f <= {bound}"
              f" and by parity f <= {even}.")
        print(f"   The arithmetic bound for these shapes was 24; the global "
              f"count gives {even}.\n")
    return even


def sweep_f(f, n, shape, cap, verbose=False):
    """Can a fixed set of size f survive to n vertices?

    Below f = 26 the two halves are no longer forced, so this sweeps the
    complete (3,5,a) and (3,5,b) catalogues for every split a + b = f with
    a, b <= 13.  A single SAT anywhere means f survives; f is excluded at n
    only if EVERY pair is UNSAT, which is why completeness of those catalogues
    is load-bearing here (it is not for the f = 26 result, where uniqueness
    does the work).
    """
    total = done = 0
    for a in range(min(13, f), max(0, f - 13) - 1, -1):
        b = f - a
        if b > 13 or b < 0:
            continue
        As = X.load35(a) if a else [[]]
        Bs = ([X.complement(b, g) for g in X.load35(b)] if b else [[]])
        total += len(As) * len(Bs)
        for ia, Ag in enumerate(As):
            for ib, Bg in enumerate(Bs):
                nv, cls, var = build(n, shape, Ag, Bg)
                if nv is None:
                    done += 1
                    continue
                work = os.path.join(SCRATCH, "fixmax",
                                    f"f{f}_n{n}_{shape}_{a}_{ia}_{ib}")
                os.makedirs(work, exist_ok=True)
                cnf = os.path.join(work, "f.cnf")
                with open(cnf, "w") as fh:
                    fh.write(f"p cnf {nv} {len(cls)}\n")
                    for c in cls:
                        fh.write(" ".join(map(str, c)) + " 0\n")
                r = subprocess.run(["timeout", str(cap), CAD, "-q", cnf],
                                   capture_output=True, text=True)
                if r.returncode == 10:
                    return ("SAT", (a, b, ia, ib), done, total)
                if r.returncode != 20:
                    return ("NO-VERDICT", (a, b, ia, ib), done, total)
                done += 1
                if verbose and done % 50 == 0:
                    print(f"      {done} pairs refuted so far", flush=True)
    return ("UNSAT", None, done, total)


def sweep_fast(f, n, cap, warm=None, log=None):
    """One f, one n, shape C_4 only (2K_2 follows by the duality).

    Uses precompute/specialise, and tries the previous n's witness first --
    feasibility is monotone, so if anything is still satisfiable it is usually
    that one, and the sweep ends on the first call.
    """
    splits = []
    for a in range(min(13, f), max(0, f - 13) - 1, -1):
        b = f - a
        if 0 <= b <= 13:
            splits.append((a, b))
    order = []
    if warm:
        order.append(warm)
    for a, b in splits:
        for ia in range(len(X.load35(a))):
            for ib in range(len(X.load35(b))):
                if (a, ia, ib) != warm:
                    order.append((a, ia, ib))

    pres, work = {}, os.path.join(SCRATCH, "fixmax", f"fast_f{f}_n{n}")
    os.makedirs(work, exist_ok=True)
    cnf = os.path.join(work, "x.cnf")
    for k, (a, ia, ib) in enumerate(order):
        b = f - a
        if (a, b) not in pres:
            pres[(a, b)] = precompute(n, "C4", a, b)
        A = X.load35(a)[ia]
        B = X.complement(b, X.load35(b)[ib])
        r = specialise(pres[(a, b)], bits_of(A, a), bits_of(B, b))
        if r is None:
            continue                       # already contains a K_5 or I_5
        nv, cls = r
        with open(cnf, "w") as fh:
            fh.write(f"p cnf {nv} {len(cls)}\n")
            for c in cls:
                fh.write(" ".join(map(str, c)) + " 0\n")
        rc = subprocess.run(["timeout", str(cap), CAD, "-q", cnf],
                            capture_output=True, text=True).returncode
        if rc == 10:
            return ("SAT", (a, ia, ib), k + 1, len(order))
        if rc != 20:
            return ("NO-VERDICT", (a, ia, ib), k + 1, len(order))
        if log and (k + 1) % 50 == 0:
            print(f"        {k+1}/{len(order)} refuted", flush=True)
    return ("UNSAT", None, len(order), len(order))


def cmd_threshold(args):
    """The threshold n*(f): the largest n carrying an f-point fixed set."""
    def opt(name, default):
        return int(args[args.index(name) + 1]) if name in args else default
    f = opt("--f", 24)
    lo, hi = opt("--from", 35), opt("--to", 42)
    cap = opt("--cap", 240)
    warm = None
    print(f"THRESHOLD SEARCH for f = {f}\n")
    print("   Shape C_4 only; 2K_2 follows by the complementation duality.")
    print("   Warm-started from the previous n's witness.  Feasibility is")
    print("   monotone in n, so the first UNSAT settles every larger n.\n")
    print("      n   tried/total   seconds   verdict")
    for n in range(lo, hi + 1):
        t0 = time.time()
        v, where, tried, tot = sweep_fast(f, n, cap, warm, log=True)
        el = time.time() - t0
        note = ""
        if v == "SAT":
            a, ia, ib = where
            note = f"  |A|={a}, |B|={f-a}, catalogue pair ({ia},{ib})"
            warm = where
        print(f"     {n:3d}   {tried:5d}/{tot:<5d} {el:8.0f}   {v}{note}",
              flush=True)
        if v == "UNSAT":
            print(f"\n   => f = {f} is impossible at every n >= {n}, "
                  f"hence at 42.")
            return 0
        if v == "NO-VERDICT":
            print(f"\n   => undecided at n = {n}; feasible up to {n-1}.")
            return 0
    print(f"\n   => f = {f} survives to n = {hi}.")
    return 0


def cmd_seam(args):
    """Close the gap between 25 and 24 without a parity hypothesis.

    principal-1, pass 41: *"the parity hypothesis is the seam ... a group with
    a 4-orbit could carry a 3-orbit, so there is a gap between 25 and 24 that
    the order-4 row does not see but a mixed-order subgroup would."*

    At f = 25 the splits are (13,12) and (12,13), so 24 catalogue pairs per
    shape rather than the single forced pair at f = 26.  If f = 25 is
    impossible at n = 42 the hypothesis can simply be dropped.
    """
    def opt(name, default):
        return int(args[args.index(name) + 1]) if name in args else default
    cap = opt("--cap", 300)
    hi = opt("--to", 42)
    print("THE PARITY SEAM: is f = 25 possible at all?\n")
    print("   If f = 25 dies below n = 42, the bound is 24 with NO parity")
    print("   hypothesis, and a group carrying both a 4-orbit and an odd")
    print("   orbit is covered too.\n")
    print("      n   shape   pairs   verdict")
    for n in range(31, hi + 1):
        verdicts = []
        for shape in ("C4", "2K2"):
            v, where, done, total = sweep_f(25, n, shape, cap)
            verdicts.append(v)
            extra = ""
            if v == "SAT":
                a, b, ia, ib = where
                extra = f"  survives, |A|={a}, |B|={b}"
            print(f"     {n:3d}   {shape:5s} {total:6d}   {v}{extra}",
                  flush=True)
        if all(v == "UNSAT" for v in verdicts):
            print(f"\n   => f = 25 is impossible at every n >= {n}, so at 42.")
            print("      The theorem holds without the even-orbit hypothesis.")
            return 0
    print(f"\n   => f = 25 still alive at n = {hi}; the hypothesis stays.")
    return 0


def cmd_cascade(args):
    """f = 26 is settled by uniqueness; below it, sweep the catalogues."""
    def opt(name, default):
        return int(args[args.index(name) + 1]) if name in args else default
    n = opt("--n", 31)
    cap = opt("--cap", 300)
    print(f"CASCADE: how far down does the fixed set have to come to survive "
          f"to n = {n}?\n")
    print("   Feasibility is monotone in n, so an UNSAT at this n excludes "
          "every larger n,")
    print("   and in particular n = 42.  c_1 is even for every order-4 type, "
          "so only even f matter.\n")
    print("      f   shape   pairs    verdict")
    for f in (26, 24, 22, 20):
        alive = False
        for shape in ("C4", "2K2"):
            verdict, where, done, total = sweep_f(f, n, shape, cap,
                                                  verbose=(f < 26))
            extra = ""
            if verdict == "SAT":
                a, b, ia, ib = where
                extra = f"  survives, split |A|={a}, |B|={b}"
                alive = True
            elif verdict == "NO-VERDICT":
                a, b, ia, ib = where
                extra = f"  UNDECIDED at |A|={a}, |B|={b} within {cap} s"
                alive = True
            print(f"     {f:3d}   {shape:5s} {total:6d}    {verdict}{extra}",
                  flush=True)
        if alive:
            print(f"\n   => f = {f} survives to n = {n}; the bound at "
                  f"|O| = 4 is {f}.")
            return 0
        print(f"     -- f = {f} is impossible at n >= {n}\n")
    return 0


def extension_control(cap=300):
    """Does the extra-vertex machinery work at all?

    The whole result below is an UNSAT at n = 31, i.e. "this 30-vertex
    configuration admits no 31st vertex".  If the code that introduces extra
    vertices were broken -- wrong variable indices, a clause quantified over
    the wrong set -- it would return UNSAT for a reason that has nothing to do
    with the configuration, and the answer would look identical.

    So: take a REAL (5,5,42)-graph, keep an induced 30-vertex subgraph, and ask
    the same machinery for a 31st vertex.  It must say SAT, because the twelve
    deleted vertices are twelve witnesses that it can be done.
    """
    path = ("/Users/abuzark/.discovery-research-team/workspaces/researcher-3/"
            "scratch/r55pc/r55_42some.g6")
    with open(path) as fh:
        line = fh.readline().strip()
    n42, adj42 = R.g6_decode(line)
    if not R.is_good(n42, adj42, 5, 5):
        raise SystemExit("control graph is not a (5,5,42)-graph")
    keep = list(range(30))
    m = len(keep)
    sub = [0] * m
    for i, j in itertools.combinations(range(m), 2):
        if (adj42[keep[i]] >> keep[j]) & 1:
            sub[i] |= 1 << j
            sub[j] |= 1 << i
    # one extra vertex, all 30 adjacencies free
    cls, nv = [], m
    lit = {}
    for i in range(m):
        nv_i = i + 1
        lit[i] = nv_i
    nv = m
    for S in itertools.combinations(range(m + 1), 5):
        if m not in S:
            continue                      # pairs inside the fixed part
        rest = [x for x in S if x != m]
        pairs_fixed = [bool((sub[u] >> v) & 1)
                       for u, v in itertools.combinations(rest, 2)]
        c, sat = [], False                # forbid K_5
        for p in pairs_fixed:
            if p is False:
                sat = True
                break
        if not sat:
            cls.append(tuple(sorted(-lit[x] for x in rest)))
        c, sat = [], False                # forbid I_5
        for p in pairs_fixed:
            if p is True:
                sat = True
                break
        if not sat:
            cls.append(tuple(sorted(lit[x] for x in rest)))
    work = os.path.join(SCRATCH, "fixmax", "control")
    os.makedirs(work, exist_ok=True)
    cnf = os.path.join(work, "c.cnf")
    with open(cnf, "w") as fh:
        fh.write(f"p cnf {nv} {len(cls)}\n")
        for c in sorted(set(cls)):
            fh.write(" ".join(map(str, c)) + " 0\n")
    r = subprocess.run(["timeout", str(cap), CAD, "-q", cnf],
                       capture_output=True, text=True)
    ok = r.returncode == 10
    print("EXTENSION CONTROL -- can the machinery add a vertex when one exists?")
    print(f"   a real (5,5,42)-graph restricted to 30 vertices, 31st vertex "
          f"free: {'SAT' if ok else 'UNSAT -- MACHINERY IS BROKEN'}")
    if not ok:
        raise SystemExit("extension control failed; the n = 31 result below "
                         "would be meaningless")
    print("   so an UNSAT at n = 31 below is about the configuration, not the "
          "encoding.\n")
    return ok


def main():
    args = sys.argv[1:]
    if "cascade" in args:
        extension_control()
        return cmd_cascade(args)
    if "threshold" in args:
        return cmd_threshold(args)
    if "seam" in args:
        extension_control()
        homogeneous_bound()
        return cmd_seam(args)

    def opt(name, default):
        return int(args[args.index(name) + 1]) if name in args else default
    lo, hi = opt("--from", 30), opt("--to", 42)
    cap = opt("--cap", 900)
    certify = "--no-certify" not in args

    print("HOW FAR DOES A 26-POINT FIXED SET SURVIVE?\n")
    print("  Configuration: a 4-set O with a mixed shape, 13 vertices joined")
    print("  to all of it (the unique (3,5,13)-graph), 13 joined to none (its")
    print("  complement).  Question: for which n is there a (5,5,n)-graph")
    print("  containing it?  Feasibility is monotone decreasing in n.\n")
    print("  If it dies below n = 42, then no (5,5,42)-graph has a group")
    print("  fixing 26 points through a 4-orbit, and since c_1 is even for")
    print("  every order-4 type the bound drops from 26 to 24.\n")
    print(f"  solver cap {cap} s per instance"
          + (", UNSAT certified through drat-trim to LRAT" if certify
             else "") + "\n")
    extension_control()
    print("     n   shape    vars   clauses   verdict")
    last_sat = {}
    for shape in ("C4", "2K2"):
        for n in range(lo, hi + 1):
            verdict, nv, nc, extra = run(n, shape, cap, certify)
            note = ""
            if verdict == "SAT":
                model, var = extra
                adj = rebuild(n, shape, model, var)
                f = audit(n, adj, shape)
                if f:
                    raise SystemExit(f"witness at n={n} fails audit: {f}")
                note = "  (rebuilt and audited)"
                last_sat[shape] = n
            print(f"   {n:3d}   {shape:5s} {nv:7d} {nc:9d}   {verdict}{note}")
            if verdict.startswith("UNSAT"):
                print(f"\n   => threshold for {shape}: largest n is "
                      f"{last_sat.get(shape, '<' + str(lo))}\n")
                break
            if verdict == "NO-VERDICT":
                print(f"\n   => undecided at n = {n} within {cap} s; "
                      f"feasible up to {last_sat.get(shape)}\n")
                break
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Positive control for the neighbourhood edge-count constraint on (5,5,42).

principal-1, pass 31: *"build the positive-control harness for r1's encoding
and offer it by citation, because r1 is about to add a constraint family and a
too-tight constraint makes the solver faster and the answer wrong."*

THE HAZARD.  A constraint that is too tight does not announce itself.  It
removes solutions, the solver gets faster, and every instance still comes back
UNSAT -- which is the answer you were hoping for.  Nothing in the certificate
chain catches it, because the certificate proves the CNF unsatisfiable and the
CNF is the wrong CNF.  The only thing that catches it is an object that is
known to satisfy the intended semantics: if the constraint excludes that, it is
wrong.  That is a *positive* control, and it is the mirror image of everything
else in this repository, which certifies negatives.

THE CONSTRAINT UNDER TEST (researcher-1, pass 43).  For a vertex v of a
(5,5,42)-graph F,

    G[N(v)]  is a (4,5)-graph on d = d(v) vertices,
    G[M(v)]  is a (5,4)-graph on 41 - d vertices,

so the number of triangles through v -- which is e(G[N(v)]) -- is confined to
[emin(4,5,d), emax(4,5,d)], and dually the complement of G[M(v)] has edge count
in [emin(4,5,41-d), emax(4,5,41-d)].

THE CONTROL.  Real (5,5,42)-graphs exist: McKay publishes 328 of them.  Every
vertex of every one must satisfy the constraint.  If any does not, the
constraint is unsound and would have made r1's search return UNSAT for the
wrong reason.  This file checks all 328 x 42 = 13776 vertices, on both sides,
and also reports the SLACK -- how much room the bound actually leaves -- since
a sound constraint that never binds is not worth encoding.

Nothing here is taken on trust: each graph is decoded by this directory's own
graph6 decoder and re-verified to be a genuine (5,5,42)-graph before use, and
the emin/emax table is `e45.json`, recomputed here from McKay's primary
catalogues and independently in agreement with Angeltveit-McKay's Table 1 at
m = 21..24.

    python3 poscontrol.py [PATH_TO_r55_42some.g6]
"""
import itertools
import json
import os
import sys
from collections import Counter

import r45bounds as R

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = ("/Users/abuzark/.discovery-research-team/workspaces/researcher-3/"
           "scratch/r55pc/r55_42some.g6")


def load_e45():
    with open(os.path.join(HERE, "e45.json")) as fh:
        d = json.load(fh)
    return ({int(k): v for k, v in d["emin"].items()},
            {int(k): v for k, v in d["emax"].items()})


def induced_edges(adj, verts):
    return sum(1 for a, b in itertools.combinations(verts, 2)
               if (adj[a] >> b) & 1)


def check_graph(n, adj, emin, emax):
    """Per-vertex report: (d, tri, lo, hi, dual_e, dlo, dhi) and violations."""
    rows, bad = [], []
    for v in range(n):
        N = [u for u in range(n) if u != v and (adj[v] >> u) & 1]
        M = [u for u in range(n) if u != v and not (adj[v] >> u) & 1]
        d = len(N)
        tri = induced_edges(adj, N)                  # edges inside N(v)
        # complement of G[M] is a (4,5)-graph on |M| vertices
        m = len(M)
        comp = (m * (m - 1) // 2) - induced_edges(adj, M)
        lo, hi = emin.get(d), emax.get(d)
        dlo, dhi = emin.get(m), emax.get(m)
        rows.append((v, d, tri, lo, hi, m, comp, dlo, dhi))
        if lo is None or hi is None:
            bad.append((v, "no table entry for d=%d" % d))
        elif not (lo <= tri <= hi):
            bad.append((v, f"N(v): d={d}, e={tri} outside [{lo},{hi}]"))
        if dlo is None or dhi is None:
            bad.append((v, "no table entry for m=%d" % m))
        elif not (dlo <= comp <= dhi):
            bad.append((v, f"M(v): m={m}, comp e={comp} outside [{dlo},{dhi}]"))
    return rows, bad


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    path = args[0] if args else DEFAULT
    emin, emax = load_e45()
    print("emin/emax(4,5,d) for the degree window of a (5,5,42)-graph "
          "(d = 17..24):")
    print("    d     : " + " ".join(f"{d:5d}" for d in range(17, 25)))
    print("    emin  : " + " ".join(f"{emin[d]:5d}" for d in range(17, 25)))
    print("    emax  : " + " ".join(f"{emax[d]:5d}" for d in range(17, 25)))
    print()

    with open(path) as fh:
        lines = [x.strip() for x in fh if x.strip()]
    print(f"{len(lines)} graphs from {os.path.basename(path)}")

    checked = 0
    all_bad = []
    deg = Counter()
    slack_n, slack_m = Counter(), Counter()
    tight_lo = tight_hi = 0
    for i, line in enumerate(lines):
        n, adj = R.g6_decode(line)
        if n != 42:
            raise SystemExit(f"graph {i}: order {n}, expected 42")
        if not R.is_good(n, adj, 5, 5):
            raise SystemExit(f"graph {i} is NOT a (5,5,42)-graph")
        checked += 1
        rows, bad = check_graph(n, adj, emin, emax)
        all_bad += [(i, *b) for b in bad]
        for _, d, tri, lo, hi, m, comp, dlo, dhi in rows:
            deg[d] += 1
            slack_n[(tri - lo, hi - tri)] += 1
            slack_m[(comp - dlo, dhi - comp)] += 1
            if tri == lo or comp == dlo:
                tight_lo += 1
            if tri == hi or comp == dhi:
                tight_hi += 1

    print(f"all {checked} decoded by this directory's decoder and re-verified "
          f"to be genuine (5,5,42)-graphs")
    print(f"degree distribution over {sum(deg.values())} vertices: "
          f"{dict(sorted(deg.items()))}")
    print()
    if all_bad:
        print(f"CONSTRAINT UNSOUND: {len(all_bad)} violations, first few:")
        for b in all_bad[:8]:
            print("   ", b)
        return 1
    print(f"POSITIVE CONTROL PASSED: {sum(deg.values())} vertices x 2 sides, "
          f"zero violations.")
    print("  Every real (5,5,42)-graph satisfies the constraint on both the "
          "neighbourhood and the")
    print("  dual neighbourhood, so encoding it cannot exclude a solution "
          "that exists.")
    print()

    def report(name, c):
        lo_slacks = Counter(k[0] for k in c.elements())
        hi_slacks = Counter(k[1] for k in c.elements())
        print(f"  {name}: distance above emin -- "
              f"min {min(lo_slacks)}, median {sorted(lo_slacks.elements())[len(list(lo_slacks.elements()))//2]}, "
              f"max {max(lo_slacks)}")
        print(f"  {name}: distance below emax -- "
              f"min {min(hi_slacks)}, median {sorted(hi_slacks.elements())[len(list(hi_slacks.elements()))//2]}, "
              f"max {max(hi_slacks)}")

    print("SLACK -- how much room the bound leaves on real graphs "
          "(a sound bound that never binds is not worth encoding):")
    report("N(v)", slack_n)
    report("M(v)", slack_m)
    print(f"  vertices meeting a lower bound exactly: {tight_lo}")
    print(f"  vertices meeting an upper bound exactly: {tight_hi}")
    return 0


def orbit_control(path=None):
    """Part 2: every known (5,5,42)-graph with an involution must satisfy the
    orbit encoding at f = 0, p = 2, k = 21.  Returns (n_witnesses, n_violating)."""
    import time
    path = path or DEFAULT
    with open(path) as fh:
        lines = [x.strip() for x in fh if x.strip()]
    verify = _verify()
    t = time.time()
    _, clauses = verify.regenerate(42, 5, 5, 0, 2, 21)
    print(f"  orbit encoding at 1^0 2^21 regenerated from (n,s,t,f,p,k) alone: "
          f"{len(clauses)} clauses, {time.time() - t:.0f}s")
    wit = bad_graphs = 0
    for i, line in enumerate(lines):
        n, adj = R.g6_decode(line)
        perm = find_involution(n, adj)
        if perm is None:
            continue
        wit += 1
        _, val = orbit_assignment(n, adj, perm)
        v = sum(1 for c in clauses
                if not any((val[x] == 1) if x > 0 else (val[-x] == 0)
                           for x in c))
        if v:
            bad_graphs += 1
            print(f"  graph {i}: {v} clauses violated -- ENCODING IS WRONG")
    return wit, bad_graphs


# ---------------------------------------------------------------------------
# Part 2: a witness for the ORBIT ENCODING itself, at the exact target.
#
# The check above tests one constraint family.  The stronger control tests the
# whole encoding: produce a real object that the encoding is supposed to admit,
# and verify that every clause is satisfied by it.
#
# researcher-1's programme excludes automorphisms of odd prime order and aims
# to reduce (5,5,42) to |Aut(G)| = 2^a.  So the type 1^0 2^21 must remain
# SATISFIABLE -- and it does: of McKay's 328 known (5,5,42)-graphs, 116 carry a
# confirmed fixed-point-free involution.  Each is an explicit satisfying
# assignment for the orbit encoding at f = 0, p = 2, k = 21.  Any encoding that
# returns UNSAT there is too tight, and this catches it in one run.
# ---------------------------------------------------------------------------

def wl_refine(n, adj):
    col = [0] * n
    for _ in range(n):
        sig = [(col[v], tuple(sorted(col[u] for u in range(n)
                                     if u != v and (adj[v] >> u) & 1)))
               for v in range(n)]
        order = {s: i for i, s in enumerate(sorted(set(sig)))}
        new = [order[s] for s in sig]
        if new == col:
            break
        col = new
    return col


def find_involution(n, adj):
    """A fixed-point-free involution from equal-sized refinement classes, or None."""
    from collections import defaultdict
    col = wl_refine(n, adj)
    cls = defaultdict(list)
    for v, c in enumerate(col):
        cls[c].append(v)
    if any(len(g) != 2 for g in cls.values()):
        return None
    perm = list(range(n))
    for g in cls.values():
        perm[g[0]], perm[g[1]] = g[1], g[0]
    for a in range(n):
        for b in range(a + 1, n):
            if ((adj[a] >> b) & 1) != ((adj[perm[a]] >> perm[b]) & 1):
                return None
    return perm


R46 = os.path.join(HERE, "..", "r46-automorphism-obstructions")


def _verify():
    """The R(4,6) lane's independent checker, reused for its orbit machinery."""
    if R46 not in sys.path:
        sys.path.insert(0, R46)
    import verify
    return verify


def orbit_assignment(n, adj, perm):
    """Relabel so perm becomes the standard sigma (2j <-> 2j+1), then read off
    the value of every pair-orbit variable.  Returns (nvar, assignment)."""
    verify = _verify()
    seen, pairs = set(), []
    for v in range(n):
        if v in seen:
            continue
        seen.add(v)
        seen.add(perm[v])
        pairs.append((v, perm[v]))
    relabel = {}
    for j, (a, b) in enumerate(pairs):
        relabel[a], relabel[b] = 2 * j, 2 * j + 1
    inv = {y: x for x, y in relabel.items()}
    name, nvar = verify.canonical_orbits(n, 0, 2, n // 2)
    val = [None] * (nvar + 1)
    for u in range(n):
        for w in range(u + 1, n):
            e = (adj[inv[u]] >> inv[w]) & 1
            k = name[(u, w)] + 1
            if val[k] is not None and val[k] != e:
                raise SystemExit("orbit is not constant: perm is not an "
                                 "automorphism after relabelling")
            val[k] = e
    return nvar, val


if __name__ == "__main__":
    rc = main()
    if rc == 0 and "--orbit" in sys.argv:
        print()
        print("PART 2: the orbit encoding itself, at the exact target")
        w, b = orbit_control()
        print(f"  {w} of the 328 carry a confirmed fixed-point-free "
              f"involution (cycle type 2^21)")
        if b:
            print(f"  {b} of them VIOLATE the encoding: it is too tight")
            rc = 1
        else:
            print(f"  all {w} satisfy every clause.  So 1^0 2^21 is REALISED "
                  f"at n = 42, and any encoding")
            print("  of it that returns UNSAT is wrong.  This is the control "
                  "to run before trusting a")
            print("  new constraint family at this target.")
    sys.exit(rc)

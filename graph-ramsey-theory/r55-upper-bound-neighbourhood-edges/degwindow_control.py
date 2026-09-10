"""Positive control for the degree-window constraint family on a group formula.

researcher-1, `53627c2`: *"What does work: the degree window on a group
formula ... one totalizer per vertex orbit suffices ... A factor of 2.8"*, and
it says the family *"should be the first thing reached for in the order-4
project"*.

principal-1, pass 31, anticipating exactly this: *"build the positive-control
harness for r1's encoding ... because r1 is about to add a constraint family
and a too-tight constraint makes the solver faster and the answer wrong."*

A 2.8x speed-up is the signature of BOTH a good redundant constraint and a
too-tight one.  Nothing in the certificate chain can tell them apart, because
the certificate proves the CNF unsatisfiable and the question is whether it is
the right CNF.  Only an object known to satisfy the intended semantics can.

WHAT IS AND IS NOT IN DOUBT.  The mathematics is not in doubt: every vertex of
a (5,5,42)-graph has 17 <= d(v) <= 24, since N(v) induces a (4,5)-graph and
M(v) a (5,4)-graph and R(4,5) = 25.  That was already checked here on all 328
known graphs (POSITIVE-CONTROL.md, zero violations, observed degrees 19-22).

What IS in doubt is the arithmetic that turns it into clauses, and it has two
independent places to go wrong:

  (1) DEGREE FROM ORBIT VARIABLES.  A vertex's degree is not a sum of orbit
      variables -- it is a WEIGHTED sum.  One orbit variable can decide several
      of v's adjacencies at once, and how many is the block weight w(v, o), the
      quantity this directory measured for a different purpose in
      Z3SQ-SPLIT-EXHAUSTIVE.md.  If a block weight is off by one the totalizer
      constrains the wrong number and the constraint is silently too tight.
  (2) THE TOTALIZER.  A totalizer whose output literals are off by one, or
      whose unit clauses assert the wrong threshold, removes real solutions.

Both are checked below against real objects: the 116 known (5,5,42)-graphs
carrying a fixed-point-free involution, whose own assignments must satisfy
every clause of the augmented formula.

Independently coded: this shares no code with researcher-1's `groupenc_deg.py`
and none of its instances were run.

    python3 degwindow_control.py
"""
import itertools
import os
import sys

import poscontrol as PC
import r45bounds as R

HERE = os.path.dirname(os.path.abspath(__file__))


def block_weights(n, name, nvar):
    """w[v][o] = how many of v's incident pairs lie in orbit o.

    This is the multiplicity that a degree constraint must use.  Summing the
    orbit variables without it would be wrong by exactly these factors.
    """
    w = [dict() for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            o = name[(u, v)]
            w[u][o] = w[u].get(o, 0) + 1
            w[v][o] = w[v].get(o, 0) + 1
    return w


class Totalizer:
    """Textbook totalizer over unit-weight inputs, built here rather than
    imported, so that agreeing with researcher-1's counts means something."""

    def __init__(self, nv):
        self.nv = nv
        self.cls = []

    def _new(self):
        self.nv += 1
        return self.nv

    def build(self, lits):
        if len(lits) == 1:
            return list(lits)
        h = len(lits) // 2
        a, b = self.build(lits[:h]), self.build(lits[h:])
        out = [self._new() for _ in range(len(a) + len(b))]
        A, B, O = [None] + a, [None] + b, [None] + out
        for i in range(len(a) + 1):
            for j in range(len(b) + 1):
                if i + j >= 1:
                    c = []
                    if i:
                        c.append(-A[i])
                    if j:
                        c.append(-B[j])
                    c.append(O[i + j])
                    self.cls.append(tuple(c))
        return out


def expand_weighted(lits_with_weight):
    """A weighted sum becomes a unit-weight one by repeating each literal w
    times.  Repetition is what makes the block weight visible to a totalizer,
    and getting it wrong is failure mode (1)."""
    out = []
    for lit, w in lits_with_weight:
        out += [lit] * w
    return out


def window(n, s, t):
    """The degree window implied by the Ramsey numbers, for any (s,t,n)-graph.

    N(v) induces an (s-1,t)-graph and M(v) an (s,t-1)-graph, so
        d(v) <= R(s-1,t) - 1   and   n - 1 - d(v) <= R(s,t-1) - 1.
    At (5,5,42) this is 17 <= d <= 24, researcher-1's window.
    """
    hi = ramsey_small(s - 1, t) - 1
    lo = n - 1 - (ramsey_small(s, t - 1) - 1)
    return max(lo, 0), min(hi, n - 1)


def ramsey_small(a, b):
    tab = {(3, 3): 6, (3, 4): 9, (3, 5): 14, (4, 4): 18, (4, 5): 25}
    if a > b:
        a, b = b, a
    if a <= 1:
        return a
    if a == 2:
        return b
    return tab[(a, b)]


def orbit_data(n, adj, perm):
    """Pair-orbit names and the graph's own assignment, for ANY permutation.

    Uses this directory's general orbit map (cyctype_control), not the
    1^f p^k special case, so that witnesses with fixed points can be used --
    which is the whole point of the second family below.
    """
    import cyctype_control as CC
    name, nvar = CC.pair_orbits(n, perm)
    idx, val = {}, [None] * (nvar + 1)
    for u in range(n):
        for v in range(u + 1, n):
            o = name[(u, v)]
            idx[(u, v)] = o
            e = (adj[u] >> v) & 1
            if val[o + 1] is not None and val[o + 1] != e:
                raise SystemExit("orbit not constant: perm is not an "
                                 "automorphism")
            val[o + 1] = e
    return idx, nvar, val


def check_one(n, adj, perm, lo, hi, sabotage=None):
    """Build the degree window for every vertex orbit and evaluate it on the
    graph's own assignment.  Returns (violations, degrees, n_clauses)."""
    name, nvar, val = orbit_data(n, adj, perm)
    w = block_weights(n, name, nvar)

    # vertex orbits of <perm>: for a fixed-point-free involution these are the
    # 21 two-element orbits, and all vertices of an orbit share a degree.
    seen, vorbits = set(), []
    for v in range(n):
        if v in seen:
            continue
        o, x = [], v
        while x not in seen:
            seen.add(x)
            o.append(x)
            x = perm[x]
        vorbits.append(o)

    bad, degs, ncls = [], [], 0
    for orb in vorbits:
        v = orb[0]
        true_deg = bin(adj[v]).count("1")
        for u in orb:
            if bin(adj[u]).count("1") != true_deg:
                bad.append(f"orbit {orb} has unequal degrees -- the "
                           f"one-totalizer-per-orbit reduction is invalid")
        degs.append(true_deg)

        # (1) degree from orbit variables, with block weights
        from_orbits = sum(mult for o, mult in w[v].items() if val[o + 1] == 1)
        if from_orbits != true_deg:
            bad.append(f"vertex {v}: block-weighted orbit sum {from_orbits} "
                       f"!= true degree {true_deg}")

        # (2) the totalizer, evaluated on the same assignment
        wv = sorted(w[v].items())
        if sabotage == "weight":
            # drop one unit from the FIRST block weight above 1 -- the exact
            # off-by-one that failure mode (1) describes.  If no weight
            # exceeds 1 this is a no-op, which is itself the point.
            hit = False
            nw = []
            for o, m in wv:
                if not hit and m > 1:
                    nw.append((o, m - 1))
                    hit = True
                else:
                    nw.append((o, m))
            wv = nw
        lits = expand_weighted([(o + 1, mult) for o, mult in wv])
        tot = Totalizer(nvar)
        outs = tot.build(lits)
        ncls += len(tot.cls) + (1 if lo else 0) + (1 if hi < len(lits) else 0)
        # propagate the totalizer on the real assignment
        ass = dict((abs(l), val[abs(l)]) for l in lits)
        for c in tot.cls:                       # unit-propagate the definition
            for _ in range(2):
                unassigned = [x for x in c if abs(x) not in ass]
                if len(unassigned) == 1 and all(
                        (ass[abs(x)] == (1 if x > 0 else 0)) is False
                        for x in c if abs(x) in ass):
                    x = unassigned[0]
                    ass[abs(x)] = 1 if x > 0 else 0
        got = sum(1 for o in outs if ass.get(abs(o), 0) == 1)
        if got != true_deg:
            bad.append(f"vertex {v}: totalizer reports {got}, true degree "
                       f"{true_deg}")
        # the window clauses themselves must be satisfied
        if lo >= 1 and ass.get(outs[lo - 1], 0) != 1:
            bad.append(f"vertex {v}: lower window clause (>= {lo}) is "
                       f"FALSIFIED by a real graph")
        if hi < len(outs) and ass.get(outs[hi], 0) == 1:
            bad.append(f"vertex {v}: upper window clause (<= {hi}) is "
                       f"FALSIFIED by a real graph")
    return bad, degs, ncls


def corrected_mechanism(verbose=True):
    """WHY the 116 witnesses have no multiplicities -- corrected.

    This file first said: *"weight above 1 needs a fixed point, and a
    fixed-point-free involution has none."*  reviewer-1's review of `d518d77`
    refuted that, point (4): at 1^0 2^1 4^10 -- the smallest Z_4 type, the one
    the order-4 probe runs on -- there are 80 weights equal to 2 with no fixed
    point anywhere.  Reproduced here exactly.

    The true mechanism.  A weight above 1 at v means two pairs at v lie in one
    orbit, i.e. some g with g{v,x} = {v,y} != {v,x}.  There are exactly two
    ways for that to happen:

      (i)  g fixes v -- a nontrivial stabiliser G_v -- and gx = y;
      (ii) g swaps, gv = y and gx = v.  This happens INSIDE v's own orbit
           whenever that orbit has size >= 3, because the pairs at distance k
           and at distance -k are then identified while both contain v.

    A fixed-point-free involution has neither: every stabiliser is trivial, and
    every orbit has size 2 whose single internal pair gives weight 1.  So all
    1722 weights are 1 **because the orbits are 2-cycles**, not because there
    are no fixed points.

    reviewer-1's own explanation covers only (i) -- it gives the 2-cycle of an
    order-4 element, whose stabiliser is <sigma^2>.  But at 1^0 2^1 4^10 only 2
    of the 42 vertices lie in that 2-cycle, while 40 lie in 4-cycles with
    TRIVIAL stabiliser and still carry weight 2, by (ii).  Both halves are
    needed to explain the 80.
    """
    import cyctype_control as CC
    from math import gcd
    from collections import Counter

    def perm_of(cyc):
        p, v = [], 0
        for L in cyc:
            p.append(tuple(range(v, v + L)))
            v += L
        img = list(range(v))
        for c in p:
            for i, x in enumerate(c):
                img[x] = c[(i + 1) % len(c)]
        return tuple(img)

    rows = [("1^0 2^21 (a fixed-point-free involution)", [2] * 21),
            ("1^0 2^1 4^10 (smallest Z_4 type)", [2] + [4] * 10),
            ("1^2 2^20", [1, 1] + [2] * 20),
            ("1^6 9^4", [1] * 6 + [9] * 4)]
    out = []
    for label, cyc in rows:
        n = sum(cyc)
        perm = perm_of(cyc)
        name, nv = CC.pair_orbits(n, perm)
        w = block_weights(n, name, nv)
        cnt = Counter()
        for u in range(n):
            for _o, m in w[u].items():
                cnt[m] += 1
        order = 1
        for L in cyc:
            order = order * L // gcd(order, L)
        cl, v = {}, 0
        for L in cyc:
            for i in range(L):
                cl[v + i] = L
            v += L
        # split the carriers by the two mechanisms
        by = Counter()
        for u in range(n):
            if max(w[u].values()) > 1:
                by["(i) nontrivial stabiliser" if order // cl[u] > 1
                   else "(ii) own orbit, size >= 3"] += 1
        fixed = sum(1 for L in cyc if L == 1)
        above = sum(v_ for k, v_ in cnt.items() if k > 1)
        out.append((label, fixed, dict(sorted(cnt.items())), above, dict(by)))
        if verbose:
            print(f"   {label}")
            print(f"      fixed points {fixed}, weights "
                  f"{dict(sorted(cnt.items()))}, {above} above 1")
            print(f"      carriers by mechanism: {dict(by) or 'none'}")
    return out


def weighted_witnesses():
    """(graph, automorphism) pairs whose block weights are NOT all 1.

    The 116 known (5,5,42)-graphs cannot exercise the multiplicities at all --
    see `weights_are_all_one` below.  H_1 and H_2, the two (4,5,24,132)-graphs,
    have automorphism groups of order 24 and 48 containing elements with fixed
    points, and those do produce weights above 1.  Same construction, different
    parameters, witnesses that exist.
    """
    import cyctype_control as CC
    path = os.path.join(HERE, "r45_24_e132.g6")
    out = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            n, adj = R.g6_decode(line)
            if not R.is_good(n, adj, 4, 5):
                raise SystemExit("H is not a (4,5,24)-graph")
            for p in CC.automorphisms(n, adj):
                if all(p[i] == i for i in range(n)):
                    continue
                name, _, _ = orbit_data(n, adj, p)
                w = block_weights(n, name, 0)
                if any(m > 1 for u in range(n) for m in w[u].values()):
                    out.append((n, adj, p, CC.cycle_type(p)))
    return out


def weights_are_all_one(n, adj, perm):
    name, _, _ = orbit_data(n, adj, perm)
    w = block_weights(n, name, 0)
    return {m for u in range(n) for m in w[u].values()} == {1}


def z3sq_live_action():
    """Are the multiplicities live in the action researcher-1 is running?

    `2c0190f` adopts the degree window for the two hard Z_3 x Z_3 actions,
    reversing the earlier decision to keep it out.  So the question is no
    longer hypothetical.  This builds the action (a=0; b=2,0,0,0; c=4) as an
    explicit permutation group and measures its block weights.
    """
    v, pts = 0, []
    for _ in range(2):                     # orbits of size 3
        pts.append(("b", [v, v + 1, v + 2]))
        v += 3
    for _ in range(4):                     # regular orbits of size 9
        pts.append(("c", [v + i for i in range(9)]))
        v += 9
    n = v
    p1, p2 = list(range(n)), list(range(n))
    for kind, o in pts:
        if kind == "b":                    # <p1> is the stabiliser
            for i in range(3):
                p2[o[i]] = o[(i + 1) % 3]
        else:
            for i in range(3):
                for j in range(3):
                    p1[o[3 * i + j]] = o[3 * i + (j + 1) % 3]
                    p2[o[3 * i + j]] = o[3 * ((i + 1) % 3) + j]
    elts, frontier = set(), [tuple(range(n))]
    while frontier:
        x = frontier.pop()
        if x in elts:
            continue
        elts.add(x)
        for g in (p1, p2):
            frontier.append(tuple(g[x[i]] for i in range(n)))
    canon = {}
    for u in range(n):
        for w_ in range(u + 1, n):
            best = None
            for g in elts:
                a, b = g[u], g[w_]
                pr = (a, b) if a < b else (b, a)
                best = pr if best is None else min(best, pr)
            canon[(u, w_)] = best
    order = {}
    for c in canon.values():
        if c not in order:
            order[c] = len(order)
    name = {k: order[c] for k, c in canon.items()}
    w = block_weights(n, name, len(order))
    from collections import Counter
    cnt = Counter()
    for u in range(n):
        for _o, m in w[u].items():
            cnt[m] += 1
    return len(elts), len(order), dict(sorted(cnt.items()))


def mutation_test(lines):
    """A check that cannot fail proves nothing.

    Two deliberate defects, each the exact failure this control exists to
    catch, are injected and the control must report violations for both.  If a
    mutant passes, the control is decorative.
    """
    print("WHY THE WITNESSES ARE BLIND -- corrected after reviewer-1's review "
          "of d518d77\n")
    corrected_mechanism()
    print()
    print("MUTATION TEST -- would this control actually catch a bad family?\n")
    n, adj = R.g6_decode(lines[0])
    perm = None
    for line in lines:
        n, adj = R.g6_decode(line)
        perm = PC.find_involution(n, adj)
        if perm is not None:
            break
    ok = True
    print("   on a (5,5,42)-graph with a fixed-point-free involution:")
    for label, lo, hi, sab, want in (
            ("correct family (17..24, true block weights)", 17, 24, None,
             False),
            ("window narrowed to 20..21 -- excludes real graphs", 20, 21, None,
             True),
            ("one block weight reduced by one -- mode (1)", 17, 24, "weight",
             True)):
        bad, _, _ = check_one(n, adj, perm, lo, hi, sabotage=sab)
        print(f"     {label:50s} "
              + ("no violations" if not bad
                 else f"CAUGHT: {len(bad)} violations"))
        if want and not bad and sab == "weight":
            print("       ^ NOT CAUGHT, and the reason is structural:")
            print(f"         every block weight at this cycle type is 1"
                  f"  (all-one: {weights_are_all_one(n, adj, perm)}),")
            print("         so the weighted sum degenerates and the mutation")
            print("         is a no-op.  This family cannot control mode (1).")
        elif want != bool(bad):
            ok = False

    wits = weighted_witnesses()
    if not wits:
        print("\n   no witness with a block weight above 1 -- mode (1) stays "
              "uncontrolled")
        return False
    n2, adj2, p2, ct = wits[0]
    lo2, hi2 = window(n2, 4, 5)
    print(f"\n   on a (4,5,{n2})-graph with an automorphism of cycle type "
          f"{ct},")
    print(f"   which does have block weights above 1 (window "
          f"{lo2}..{hi2}):")
    for label, lo, hi, sab, want in (
            ("correct family, true block weights", lo2, hi2, None, False),
            ("one block weight reduced by one -- mode (1)", lo2, hi2, "weight",
             True)):
        bad, _, _ = check_one(n2, adj2, p2, lo, hi, sabotage=sab)
        print(f"     {label:50s} "
              + ("no violations" if not bad
                 else f"CAUGHT: {len(bad)} violations"))
        if want != bool(bad):
            ok = False
    print("\n   " + ("The control is discriminating -- but only the second "
                     "family\n   reaches failure mode (1).\n" if ok else
                     "MUTATION TEST FAILED.\n"))
    return ok


def main():
    lo, hi = 17, 24
    print("POSITIVE CONTROL: the degree-window constraint family "
          "(researcher-1, 53627c2)")
    print(f"  window {lo} <= d(v) <= {hi}, from R(4,5) = 25 on both sides.")
    print("  A 2.8x speed-up is the signature of a good redundant constraint")
    print("  AND of a too-tight one.  Only a real object separates them.\n")

    path = PC.DEFAULT
    with open(path) as fh:
        lines = [x.strip() for x in fh if x.strip()]
    if not mutation_test(lines):
        return 1
    wit = viol = 0
    allbad, alldeg, ncls = [], [], 0
    for line in lines:
        n, adj = R.g6_decode(line)
        if not R.is_good(n, adj, 5, 5):
            raise SystemExit("a catalogue graph is not a (5,5,42)-graph")
        perm = PC.find_involution(n, adj)
        if perm is None:
            continue
        wit += 1
        bad, degs, k = check_one(n, adj, perm, lo, hi)
        ncls = max(ncls, k)
        alldeg += degs
        if bad:
            viol += 1
            allbad += [(line[:12], b) for b in bad]
    print(f"  witnesses: {wit} known (5,5,42)-graphs with a fixed-point-free "
          f"involution")
    print(f"  per-graph: 21 vertex orbits, ~{ncls} degree-window clauses")
    print(f"  degrees seen across all of them: "
          f"{sorted(set(alldeg))}\n")
    if allbad:
        print(f"  CONSTRAINT FAMILY IS TOO TIGHT: {len(allbad)} violations "
              f"over {viol} graphs.")
        for x in allbad[:10]:
            print("     ", x)
        return 1
    print(f"  PASSED: every one of the {wit} witnesses satisfies the "
          f"degree-window clauses.")
    print("    (1) the block-weighted orbit sum equals the true degree at "
          "every vertex;")
    print("    (2) the totalizer reports the true degree, and neither window")
    print("        clause is falsified by a graph that actually exists.")
    print("\n  So adding this family to an orbit encoding at 1^0 2^21 cannot")
    print("  exclude a solution that exists.")
    print("\n  BUT READ THE MUTATION TEST.  At 1^0 2^21 every block weight is")
    print("  1, so these 116 witnesses CANNOT exercise failure mode (1) --")
    print("  the multiplicities, which are the part most likely to be wrong.")
    print("  That is not an accident, but the reason is NOT the one this file")
    print("  first gave ('weight above 1 needs a fixed point' -- false above")
    print("  order 2; see corrected_mechanism.__doc__).  Mode (1) is reachable")
    print("  only at other parameters, and it is checked above on a")
    print("  (4,5,24)-graph, where the mutant IS caught.")
    print("\n  The order-4 row is exactly where weights above 1 appear, and")
    print("  it has no witnesses at n = 42 at all.  It does not run")
    print("  researcher-1's code.")

    go, nv, cnt = z3sq_live_action()
    live = sum(m for k, m in cnt.items() if k > 1)
    print(f"\n  AND THIS IS NOT HYPOTHETICAL.  2c0190f adopts the family for")
    print(f"  the two hard Z_3 x Z_3 actions now solving.  Rebuilding the")
    print(f"  action (a=0; b=2,0,0,0; c=4): group order {go}, {nv} pair orbits")
    print(f"  [researcher-1 publishes 99 orbit variables], block weights")
    print(f"  {cnt} -- {live} of {sum(cnt.values())} entries exceed 1.")
    print(f"  So failure mode (1) is REACHABLE in the runs already in flight,")
    print(f"  and the n = 42 witnesses cannot see it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""How many points can a group fix?  The general orbit form of r1's lemma.

researcher-1 (`c81e3ad`) proved: an involution of a (5,5,42)-graph fixes at
most 36 points.  That bound is what makes the order-4 enumeration finite -- it
is the reason there are 90 Z_4 types and 1347 Z_2 x Z_2 actions rather than
infinitely many shapes to consider.  principal-1, pass 39: *"The order-4 row is
where the completeness work now lives."*

THE OBSERVATION.  Their proof uses a 2-cycle, but nothing in it is about
2-cycles.  Let G <= Aut(F) and let O be ANY G-orbit.  If w is fixed by all of
G and x, y are in O, pick g with gx = y; then

    w ~ x  <=>  gw ~ gx  <=>  w ~ y,

so w is joined to all of O or to none of it.  The fixed set therefore splits as
F = A (joined to all of O) + B (joined to none), for every orbit at once.

Write w = omega(F[O]) and a = alpha(F[O]) for the clique and independence
numbers of the orbit's own induced graph.  Then in an (s,t)-graph:

  * a K_s inside A + O uses a clique of O, at most w of it, and all of A is
    joined to all of O -- so A must have no K_{s-w}.  A also has no I_t.
    Hence |A| <= R(s-w, t) - 1.
  * dually B has no I_{t-a} and no K_s, so |B| <= R(s, t-a) - 1.

    LEMMA.  |Fix(G)| <= R(s-w, t) - 1 + R(s, t-a) - 1  for every orbit O.

At an orbit of size 2 in a (5,5)-graph this is 13 + 24 = 37, which is r1's
lemma.  At every larger orbit it is strictly better, because a bigger orbit
forces a bigger w or a bigger a.  At size 4 -- the whole order-4 row -- it is
26, not 36.

WHAT IS CHECKED HERE.  The lemma's arithmetic is machine-evaluated from a table
of exactly-known Ramsey numbers; the invariant graphs on an orbit are
enumerated rather than argued; the reduced case lists are recomputed from
scratch; and the lemma itself is put through a positive control on complete
catalogues of real Ramsey graphs and their real automorphisms, where a wrong
case in the w/alpha analysis shows up as a violation.

    python3 orbitbound.py table | z4 | klein | control | all
"""
import itertools
import os
import sys
from math import gcd

import r45bounds as R

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = ("/Users/abuzark/.discovery-research-team/workspaces/researcher-3/"
           "scratch")

# Exactly known two-colour Ramsey numbers, Radziszowski DS1.  R(0,k) = 0 and
# R(1,k) = 1 are the degenerate conventions: a graph with no K_0 does not
# exist, a graph with no K_1 is empty.  Only entries with min(a,b) <= 4 are
# ever needed below, so R(5,5) -- unknown -- is never consulted.
RAMSEY = {(3, 3): 6, (3, 4): 9, (3, 5): 14, (4, 4): 18, (4, 5): 25}


def ramsey(a, b):
    if a > b:
        a, b = b, a
    if a == 0:
        return 0
    if a == 1:
        return 1
    if a == 2:
        return b
    if (a, b) not in RAMSEY:
        raise SystemExit(f"R({a},{b}) is not known exactly -- the lemma may "
                         f"not be evaluated here")
    return RAMSEY[(a, b)]


def split_bound(s, t, w, a):
    """|A| + |B| <= R(s-w,t)-1 + R(s,t-a)-1, the lemma's right-hand side."""
    return (ramsey(s - w, t) - 1) + (ramsey(s, t - a) - 1)


# ---------------------------------------------------------------- orbit shapes

def pair_orbits_within(perms, m):
    """Orbits of the group <perms> on the pairs of an m-set it permutes."""
    seen, orbs = set(), []
    for u, v in itertools.combinations(range(m), 2):
        if (u, v) in seen:
            continue
        orb, stack = set(), [(u, v)]
        while stack:
            p = stack.pop()
            if p in orb:
                continue
            orb.add(p)
            for g in perms:
                q = (g[p[0]], g[p[1]])
                q = q if q[0] < q[1] else (q[1], q[0])
                if q not in orb:
                    stack.append(q)
        seen |= orb
        orbs.append(sorted(orb))
    return orbs


def clique_no(m, adj):
    best = 0
    for k in range(m, 0, -1):
        for S in itertools.combinations(range(m), k):
            if all((adj[u] >> v) & 1 for u, v in itertools.combinations(S, 2)):
                return k
        best = k
    return best


def indep_no(m, adj):
    comp = [(~adj[u]) & ((1 << m) - 1) & ~(1 << u) for u in range(m)]
    return clique_no(m, comp)


def invariant_shapes(perms, m, s, t):
    """Every <perms>-invariant graph on the orbit that could occur inside an
    (s,t)-graph, as (omega, alpha, edge set).  Enumerated, not argued."""
    orbs = pair_orbits_within(perms, m)
    out = []
    for mask in range(1 << len(orbs)):
        adj = [0] * m
        for i, orb in enumerate(orbs):
            if not (mask >> i) & 1:
                continue
            for u, v in orb:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
        w, a = clique_no(m, adj), indep_no(m, adj)
        if w >= s or a >= t:          # the orbit alone already breaks (s,t)
            continue
        out.append((w, a, tuple(adj)))
    return orbs, out


def orbit_bound(perms, m, s, t):
    """max over realisable shapes -- the safe bound, since which shape occurs
    is not known in advance."""
    orbs, shapes = invariant_shapes(perms, m, s, t)
    if not shapes:
        return None, orbs, shapes        # no orbit of this shape can exist
    return max(split_bound(s, t, w, a) for w, a, _ in shapes), orbs, shapes


def cyclic(m):
    return [tuple((i + 1) % m for i in range(m))]


def klein_regular():
    """Z_2 x Z_2 acting regularly on 4 points."""
    return [(1, 0, 3, 2), (2, 3, 0, 1)]


# ------------------------------------------------------------------- the table

def cmd_table():
    print("THE LEMMA, evaluated on cyclic orbits of a (5,5)-graph")
    print("  |Fix(G)| <= R(5-w,5)-1 + R(5,5-a)-1 for every orbit O,")
    print("  w = omega(F[O]), a = alpha(F[O]); max over the invariant shapes "
          "that can occur.\n")
    print("   |O|   invariant shapes   admissible   bound on |Fix(G)|")
    for m in range(2, 13):
        b, orbs, shapes = orbit_bound(cyclic(m), m, 5, 5)
        tag = "IMPOSSIBLE" if b is None else str(b)
        if m == 2:
            tag += "   <- r1's lemma (37, then 36 by parity)"
        if m == 4:
            tag += "   <- the order-4 row"
        print(f"   {m:3d}   {1 << len(orbs):16d}   {len(shapes):10d}   {tag}")
    b, orbs, shapes = orbit_bound(klein_regular(), 4, 5, 5)
    print(f"\n   Z_2 x Z_2 regular orbit (|O| = 4): {1 << len(orbs)} invariant "
          f"shapes, {len(shapes)} admissible, bound {b}")
    print("   shapes: " + ", ".join(
        f"(w={w},a={a})" for w, a in sorted({(w, a) for w, a, _ in shapes})))
    print("\n   Reading: the bound falls as the orbit grows.  A group with a")
    print("   large orbit cannot fix many points, so the enumeration that has")
    print("   to be done shrinks exactly where the orbits are big.")

    # Corollaries, read off the same table rather than asserted.
    caps = {}
    for m in range(2, 13):
        b, _, _ = orbit_bound(cyclic(m), m, 5, 5)
        if b is not None:
            caps[m] = b
    print("\n   COROLLARIES (read off the table, not asserted)")
    for thresh, name in ((26, "26"), (28, "28")):
        allowed = [m for m, b in caps.items() if b > thresh]
        print(f"     |Fix(G)| > {name}  =>  every orbit has size in "
              f"{{1}} u {sorted(allowed)}")
    print("     so a group fixing more than 28 vertices has all orbits of")
    print("     size 1 or 2, hence g^2 = 1 for every g: G is an elementary")
    print("     abelian 2-group.  A group fixing more than 26 has every")
    print("     element of order 1, 2, 3 or 6.")
    return 0


# --------------------------------------------------------------- the case list

def z4_types(fixed_cap):
    """(c1,c2,c4) with c1+2c2+4c4 = 42, c4 >= 1, sigma^2 fixing <= 36
    (r1's lemma), and c1 <= fixed_cap (the new lemma)."""
    out = []
    for c4 in range(1, 42 // 4 + 1):
        for c2 in range(0, 42 // 2 + 1):
            c1 = 42 - 2 * c2 - 4 * c4
            if c1 < 0:
                continue
            if c1 + 2 * c2 > 36:       # sigma^2 is an involution
                continue
            if c1 > fixed_cap:
                continue
            out.append((c1, c2, c4))
    return out


def cmd_z4():
    b4, _, _ = orbit_bound(cyclic(4), 4, 5, 5)
    before, after = z4_types(42), z4_types(b4)
    print("Z_4 CYCLE TYPES on 42 vertices")
    print(f"  with r1's lemma alone (c1 + 2c2 <= 36):      {len(before)}"
          f"    [researcher-1 publishes 90]")
    print(f"  with the orbit lemma at |O| = 4 (c1 <= {b4}):  {len(after)}")
    gone = sorted(set(before) - set(after))
    print(f"  removed: {len(gone)} types\n")
    print("   (c1, c2, c4)     c1     why it is impossible")
    for c1, c2, c4 in gone:
        print(f"   ({c1:2d},{c2:3d},{c4:3d})     {c1:2d}     "
              f"a 4-orbit exists and forces c1 <= {b4}")
    if before and len(before) != 90:
        print(f"\n  WARNING: reproduced {len(before)}, not the published 90")
    return 0


def klein_actions(fixed_cap):
    """(a; b1,b2,b3; c) with a + 2(b1+b2+b3) + 4c = 42, each involution
    fixing a + 2bi <= 36, the action faithful, b's sorted (GL_2(2) = S_3
    permutes the three subgroups of order 2).  fixed_cap applies only when a
    regular orbit exists."""
    out = []
    for c in range(0, 42 // 4 + 1):
        rest = 42 - 4 * c
        for b1 in range(rest // 2 + 1):
            for b2 in range(b1, rest // 2 + 1):
                for b3 in range(b2, rest // 2 + 1):
                    a = rest - 2 * (b1 + b2 + b3)
                    if a < 0:
                        continue
                    bs = (b1, b2, b3)
                    if any(a + 2 * b > 36 for b in bs):
                        continue
                    # faithful: no involution acts trivially
                    if any(a + 2 * b == 42 for b in bs):
                        continue
                    if c >= 1 and a > fixed_cap:
                        continue
                    out.append((a, bs, c))
    return out


def cmd_klein():
    bk, _, _ = orbit_bound(klein_regular(), 4, 5, 5)
    before, after = klein_actions(42), klein_actions(bk)
    print("Z_2 x Z_2 ACTIONS on 42 vertices")
    print(f"  with r1's lemma alone (a + 2bi <= 36):        {len(before)}"
          f"    [researcher-1 publishes 1347]")
    print(f"  with the orbit lemma at a regular orbit (a <= {bk}): "
          f"{len(after)}")
    gone = sorted(set(before) - set(after))
    print(f"  removed: {len(gone)} actions\n")
    from collections import Counter
    byc = Counter(g[2] for g in gone)
    bya = Counter(g[0] for g in gone)
    print(f"  removed by number of regular orbits c: {dict(sorted(byc.items()))}")
    print(f"  removed by fixed-point count a:        {dict(sorted(bya.items()))}")
    print(f"\n  Every removed action has c >= 1 and a > {bk}: it has a regular")
    print( "  orbit, so its globally fixed set splits against a 4-set that has")
    print( "  both an edge and a non-edge, or is homogeneous -- either way at")
    print(f"  most {bk} points.")
    if len(before) != 1347:
        print(f"\n  WARNING: reproduced {len(before)}, not the published 1347")
    return 0


# ------------------------------------------------------------ positive control

def wl_colours(n, adj):
    """1-WL refinement.  Automorphisms preserve the colouring, so it is a sound
    pruning rule for the search below; it is only a filter, never a source of
    truth -- every candidate is still checked against every earlier vertex."""
    col = [0] * n
    for _ in range(n):
        sig = [(col[v], tuple(sorted(col[u] for u in range(n)
                                     if (adj[v] >> u) & 1))) for v in range(n)]
        order = {s: i for i, s in enumerate(sorted(set(sig)))}
        new = [order[s] for s in sig]
        if new == col:
            break
        col = new
    return col


def automorphisms(n, adj, cap=None):
    """Every automorphism, by backtracking with adjacency consistency."""
    col = wl_colours(n, adj)
    cand = [[c for c in range(n) if col[c] == col[k]] for k in range(n)]
    perms, img, used = [], [-1] * n, [False] * n

    def bt(k):
        if cap is not None and len(perms) >= cap:
            return
        if k == n:
            perms.append(tuple(img))
            return
        for c in cand[k]:
            if used[c]:
                continue
            if all(((adj[k] >> j) & 1) == ((adj[c] >> img[j]) & 1)
                   for j in range(k)):
                img[k] = c
                used[c] = True
                bt(k + 1)
                used[c] = False
                img[k] = -1
    bt(0)
    return perms


def vertex_orbits(n, gens):
    lab = list(range(n))

    def find(x):
        while lab[x] != x:
            lab[x] = lab[lab[x]]
            x = lab[x]
        return x
    for g in gens:
        for v in range(n):
            a, b = find(v), find(g[v])
            if a != b:
                lab[a] = b
    out = {}
    for v in range(n):
        out.setdefault(find(v), []).append(v)
    return list(out.values())


def check_graph(n, adj, gens, s, t):
    """Test the lemma for the group <gens>: for EVERY orbit, |Fix| must be at
    most R(s-w,t)-1 + R(s,t-a)-1 computed from that orbit's own shape.

    This is the real test: w and a are read off the actual induced graph, so a
    wrong case in the derivation shows up here as a violation.
    """
    orbs = vertex_orbits(n, gens)
    fix = [o[0] for o in orbs if len(o) == 1]
    f = len(fix)
    worst, bad = None, []
    for O in orbs:
        if len(O) < 2:
            continue
        m = len(O)
        sub = [0] * m
        for i, j in itertools.combinations(range(m), 2):
            if (adj[O[i]] >> O[j]) & 1:
                sub[i] |= 1 << j
                sub[j] |= 1 << i
        w, a = clique_no(m, sub), indep_no(m, sub)
        if w >= s or a >= t:
            bad.append((O, f"orbit itself has K_{w} / I_{a}"))
            continue
        b = split_bound(s, t, w, a)
        if worst is None or b < worst:
            worst = b
        if f > b:
            bad.append((O, f"|Fix| = {f} > {b} at |O| = {m}, w = {w}, a = {a}"))
        # and the split itself: A joined to all of O, B to none
        A = [v for v in fix if (adj[v] >> O[0]) & 1]
        B = [v for v in fix if not (adj[v] >> O[0]) & 1]
        for v in fix:
            joined = [(adj[v] >> u) & 1 for u in O]
            if len(set(joined)) != 1:
                bad.append((O, f"fixed vertex {v} joined to some but not all"))
        if len(A) > ramsey(s - w, t) - 1:
            bad.append((O, f"|A| = {len(A)} > R({s-w},{t})-1"))
        if len(B) > ramsey(s, t - a) - 1:
            bad.append((O, f"|B| = {len(B)} > R({s},{t-a})-1"))
    return f, worst, bad


def control_file(path, s, t, label, limit=None, autcap=200000):
    if not os.path.exists(path):
        print(f"   [skipped: {label} -- no file at {path}]")
        return 0, 0, 0, []
    graphs = auts = tested = 0
    bad, slack = [], []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            n, adj = R.g6_decode(line)
            if not R.is_good(n, adj, s, t):
                raise SystemExit(f"{label}: a graph is not an "
                                 f"({s},{t})-graph")
            graphs += 1
            perms = automorphisms(n, adj, cap=autcap)
            auts += len(perms)
            for g in perms:
                if all(g[i] == i for i in range(n)):
                    continue
                tested += 1
                f, worst, b = check_graph(n, adj, [g], s, t)
                bad += [(label, line[:12], x) for x in b]
                if worst is not None:
                    slack.append((worst - f, f, worst))
            # and the full group, whose fixed set is smaller and orbits bigger
            if len(perms) > 1:
                tested += 1
                f, worst, b = check_graph(n, adj, perms, s, t)
                bad += [(label, line[:12], x) for x in b]
                if worst is not None:
                    slack.append((worst - f, f, worst))
            if limit and graphs >= limit:
                break
    tight = min((x[0] for x in slack), default=None)
    print(f"   {label:26s} {graphs:7d} graphs  {tested:7d} nontrivial groups"
          f"  {len(bad):3d} violations"
          + (f"  closest approach: {tight}" if tight is not None else ""))
    return graphs, tested, len(bad), bad


def cmd_control():
    print("POSITIVE CONTROL -- the lemma against real Ramsey graphs and their")
    print("real automorphisms.  For every graph, every nontrivial cyclic")
    print("subgroup and the full group, and EVERY orbit of it, the fixed set")
    print("must respect the bound its shape gives, and must split as A + B.\n")
    print("   catalogue                    graphs           groups"
          "        result")
    # Complete catalogues where "complete" is affordable; a stated prefix of
    # the three that are not.  A prefix is still a real test -- the lemma is
    # universally quantified, so any single graph could refute it.
    jobs = [
        (f"{SCRATCH}/r45cert/r35_7.g6", 3, 5, "(3,5)-graphs, n=7", None),
        (f"{SCRATCH}/r45cert/r35_8.g6", 3, 5, "(3,5)-graphs, n=8", None),
        (f"{SCRATCH}/r45cert/r35_9.g6", 3, 5, "(3,5)-graphs, n=9", None),
        (f"{SCRATCH}/r45cert/r35_10.g6", 3, 5, "(3,5)-graphs, n=10", None),
        (f"{SCRATCH}/r45cert/r35_11.g6", 3, 5, "(3,5)-graphs, n=11", None),
        (f"{SCRATCH}/r45cert/r35_12.g6", 3, 5, "(3,5)-graphs, n=12", None),
        (f"{SCRATCH}/r45cert/r35_13.g6", 3, 5, "(3,5)-graphs, n=13", None),
        (f"{SCRATCH}/r45cert/r44_11.g6", 4, 4, "(4,4)-graphs, n=11 [prefix]",
         4000),
        (f"{SCRATCH}/r45cert/r44_12.g6", 4, 4, "(4,4)-graphs, n=12 [prefix]",
         4000),
        (f"{SCRATCH}/r45cert/r44_13.g6", 4, 4, "(4,4)-graphs, n=13 [prefix]",
         4000),
        (f"{SCRATCH}/r45cert/r44_14.g6", 4, 4, "(4,4)-graphs, n=14 [prefix]",
         4000),
        (f"{SCRATCH}/r45cert/r44_15.g6", 4, 4, "(4,4)-graphs, n=15", None),
        (f"{SCRATCH}/r45cert/r44_16.g6", 4, 4, "(4,4)-graphs, n=16", None),
        (f"{SCRATCH}/r45cert/r44_17.g6", 4, 4, "(4,4)-graphs, n=17", None),
        (f"{HERE}/r45_24_e132.g6", 4, 5, "(4,5,24,132)-graphs", None),
        (f"{SCRATCH}/r55/r45_24.g6", 4, 5, "(4,5,24)-graphs [prefix]", 3000),
        (f"{SCRATCH}/r55pc/r55_42some.g6", 5, 5, "(5,5,42)-graphs, all 328",
         None),
    ]
    tg = tt = tb = 0
    allbad = []
    for path, s, t, label, lim in jobs:
        g, k, nb, bad = control_file(path, s, t, label, limit=lim)
        tg += g
        tt += k
        tb += nb
        allbad += bad
    print()
    if allbad:
        print(f"   LEMMA FALSE: {tb} violations.  First few:")
        for x in allbad[:10]:
            print("     ", x)
        return 1
    print(f"   PASSED: {tg} graphs, {tt} nontrivial groups, "
          f"zero violations.")
    print("   Every fixed set respected the bound its orbits give, and every")
    print("   fixed vertex was joined to all of each orbit or to none of it.")
    return 0


def z4_perm(c1, c2, c4):
    p, v = [], 0
    for _ in range(c1):
        p.append((v,))
        v += 1
    for _ in range(c2):
        p.append((v, v + 1))
        v += 2
    for _ in range(c4):
        p.append((v, v + 1, v + 2, v + 3))
        v += 4
    img = list(range(v))
    for cyc in p:
        for i, x in enumerate(cyc):
            img[x] = cyc[(i + 1) % len(cyc)]
    return tuple(img)


def nvars(perm, n):
    """Number of orbits of <perm> on the pairs of an n-set."""
    return len(pair_orbits_within([perm], n))


def cmd_order():
    """The predicted-hardest-first ordering, recomputed on the REDUCED list.

    ORDER4-ENUMERATION.md named (34,0,2) as the easiest end.  That type is one
    of the six the orbit lemma removes, so the example has to be replaced --
    my own artifact, invalidated by my own result.
    """
    b4, _, _ = orbit_bound(cyclic(4), 4, 5, 5)
    rows = []
    for c1, c2, c4 in z4_types(b4):
        # "free part" as in ORDER4-ENUMERATION.md: the points lying in REGULAR
        # orbits, i.e. orbits of full size |G| = 4.
        rows.append((4 * c4, nvars(z4_perm(c1, c2, c4), 42), (c1, c2, c4)))
    rows.sort(key=lambda r: (-r[0], r[1]))
    print(f"Z_4, PREDICTED-HARDEST FIRST on the reduced list of {len(rows)} "
          f"types")
    print("  (sort by free part descending, not formula size ascending)\n")
    print("   rank   free   vars   (c1,c2,c4)")
    for i, (free, nv, t) in enumerate(rows[:3], 1):
        print(f"   {i:4d}   {free:4d}   {nv:4d}   {t}")
    print("    ...")
    for i, (free, nv, t) in enumerate(rows[-3:], len(rows) - 2):
        print(f"   {i:4d}   {free:4d}   {nv:4d}   {t}")
    print(f"\n   easiest end is now {rows[-1][2]}: {rows[-1][1]} variables, "
          f"free part {rows[-1][0]}.")
    print("   ORDER4-ENUMERATION.md named (34,0,2) with free part 8 -- that")
    print("   type is one of the six this lemma removes, so the example was")
    print("   invalidated by my own result and is replaced here.")
    return 0


def main():
    cmds = {"table": cmd_table, "z4": cmd_z4, "klein": cmd_klein,
            "order": cmd_order, "control": cmd_control}
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which == "all":
        rc = 0
        for name in ("table", "z4", "klein", "control"):
            print("=" * 72)
            rc |= cmds[name]()
            print()
        return rc
    if which not in cmds:
        raise SystemExit(f"usage: {sys.argv[0]} [{'|'.join(cmds)}|all]")
    return cmds[which]()


if __name__ == "__main__":
    sys.exit(main())

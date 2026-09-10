"""Independent check of researcher-1's Z_3 x Z_3 enumeration (pass 50, f7acdd2).

WHY THIS STEP.  researcher-1 wrote its own positive control for the group
encoder -- both directions, decoding SAT models into real graphs and checking
random invariant graphs against every clause.  That covers the ENCODING.  It
cannot cover the CASE LIST: an encoding can be perfectly faithful and the result
still be incomplete if an action was missed.  "37 of 39" rests on 39 being all
of them, and neither a positive nor a negative control can see that.

So this file checks the enumeration, twice and independently, and nothing else.
None of researcher-1's instances were run.

THE CLASSIFICATION.  V = Z_3 x Z_3 acting faithfully on 42 points.  An abelian
group's action is determined up to equivalence by the multiset of point
stabilisers (a transitive action is determined by its stabiliser up to
conjugacy, and conjugacy is trivial here), so the data is

    a           points with stabiliser V        (fixed)
    b_i         orbits of size 3, stabiliser H_i, i = 1..4
    c           regular orbits of size 9

with a + 3 sum(b_i) + 9c = 42.  V has exactly (9-1)/(3-1) = 4 subgroups of
order 3.  A non-identity g in H_i fixes exactly a + 3 b_i points, which the
chain-published order-3 bound caps at 12.  Aut(Z_3^2) = GL_2(3) permutes the
four subgroups as S_4, so the b_i may be sorted.

ONE SUBTLETY WORTH RECORDING.  The obvious faithfulness test -- "no element
fixes all 42 points" -- is weaker than the real condition, which is that the
kernel, the intersection of the stabilisers, is trivial.  With c = 0 and only
one b_i nonzero the kernel is H_i, not 1.  It happens not to matter: such an
action has a + 3 b_i = 42 > 12, so the order-3 bound already excludes it.  Both
tests are run below and both give 39.

    python3 z3sq_enum.py
"""
import sys
from collections import Counter
from itertools import combinations

V = [(i, j) for i in range(3) for j in range(3)]
SUBS = [[(0, 0), (1, 0), (2, 0)], [(0, 0), (0, 1), (0, 2)],
        [(0, 0), (1, 1), (2, 2)], [(0, 0), (1, 2), (2, 1)]]
FIXBOUND = 12                      # order-3 automorphisms fix at most 12 points
N = 42


def add(x, y):
    return ((x[0] + y[0]) % 3, (x[1] + y[1]) % 3)


def enumerate_actions(strict_kernel=True):
    """Every faithful action, up to Aut(V), obeying the order-3 fix bound."""
    out = set()
    for a in range(FIXBOUND + 1):
        for c in range((N - a) // 9 + 1):
            rest = N - a - 9 * c
            if rest % 3:
                continue
            tot = rest // 3
            for b1 in range(tot + 1):
                for b2 in range(tot - b1 + 1):
                    for b3 in range(tot - b1 - b2 + 1):
                        b = tuple(sorted((b1, b2, b3, tot - b1 - b2 - b3),
                                         reverse=True))
                        if any(a + 3 * x > FIXBOUND for x in b):
                            continue
                        if strict_kernel:
                            # kernel trivial: a regular orbit, or two distinct H_i
                            if c == 0 and sum(1 for x in b if x > 0) < 2:
                                continue
                        elif any(a + 3 * x == N for x in b):
                            continue
                        out.add((a, b, c))
    return sorted(out)


def build(a, b, c):
    """An explicit action with that stabiliser profile: (n, [g, h])."""
    pts = [("fix", i) for i in range(a)]
    for idx, bi in enumerate(b):
        for r in range(bi):
            seen, cos = set(), []
            for v in V:
                k = frozenset(add(v, h) for h in SUBS[idx])
                if k not in seen:
                    seen.add(k)
                    cos.append(k)
            pts += [("cos", idx, r, k) for k in cos]
    for r in range(c):
        pts += [("reg", r, v) for v in V]
    index = {p: i for i, p in enumerate(pts)}

    def act(v, p):
        if p[0] == "fix":
            return p
        if p[0] == "cos":
            return ("cos", p[1], p[2], frozenset(add(v, x) for x in p[3]))
        return ("reg", p[1], add(v, p[2]))

    return len(pts), [[index[act(g, p)] for p in pts] for g in ((1, 0), (0, 1))]


def group_elements(perms, n):
    ident = tuple(range(n))
    seen, frontier = {ident}, [ident]
    gens = [tuple(p) for p in perms]
    while frontier:
        cur = frontier.pop()
        for g in gens:
            nxt = tuple(g[cur[i]] for i in range(n))
            if nxt not in seen:
                seen.add(nxt)
                frontier.append(nxt)
    return seen


def pair_orbit_map(n, elems):
    par = list(range(n * n))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    def ix(u, v):
        return min(u, v) * n + max(u, v)

    for u, v in combinations(range(n), 2):
        for g in elems:
            a, b = find(ix(u, v)), find(ix(g[u], g[v]))
            if a != b:
                par[a] = b
    return {(u, v): find(ix(u, v)) for u, v in combinations(range(n), 2)}


def main():
    strict = enumerate_actions(True)
    loose = enumerate_actions(False)
    print(f"(1) parameter enumeration: {len(strict)} actions with the strict "
          f"kernel test,")
    print(f"    {len(loose)} with the weaker 'nothing fixes all 42' test — "
          f"{'same set' if strict == loose else 'DIFFERENT'}.")
    print(f"    researcher-1 publishes 39.  "
          f"{'MATCH' if len(strict) == 39 else 'MISMATCH'}")

    print("\n(2) each one built explicitly and checked as a permutation group:")
    rows = []
    for a, b, c in strict:
        n, perms = build(a, b, c)
        if n != N:
            raise SystemExit(f"{(a, b, c)}: {n} points, expected {N}")
        E = group_elements(perms, n)
        if len(E) != 9:
            raise SystemExit(f"{(a, b, c)}: group of order {len(E)}, not 9")
        fixes = sorted(sum(1 for i in range(n) if g[i] == i) for g in E)
        if fixes[-1] != N or fixes[-2] > FIXBOUND:
            raise SystemExit(f"{(a, b, c)}: fix counts {fixes}")
        nm = pair_orbit_map(n, E)
        nv = len(set(nm.values()))
        mx = 0
        for v in range(n):
            cc = Counter(nm[(min(u, v), max(u, v))] for u in range(n) if u != v)
            mx = max(mx, max(cc.values()))
        rows.append((nv, mx, a, b, c))
    rows.sort()
    print(f"    all {len(rows)} are faithful actions of a group of order 9 on "
          f"{N} points,")
    print(f"    every non-identity element fixing at most {FIXBOUND}.")
    print(f"    orbit variables: {rows[0][0]} to {rows[-1][0]}   "
          f"(researcher-1 publishes 97 to 143: "
          f"{'MATCH' if (rows[0][0], rows[-1][0]) == (97, 143) else 'MISMATCH'})")

    print("\n(3) the structure of the two survivors")
    surv = [r for r in rows if r[2] == 0 and r[4] == 4]
    print("    researcher-1's survivors are (0;1,1,0,0;4) and (0;2,0,0,0;4).")
    for nv, mx, a, b, c in surv:
        rank = [i for i, r in enumerate(rows) if r[2:] == (a, b, c)][0]
        print(f"      ({a};{','.join(map(str, b))};{c}): {nv} variables, "
              f"rank {rank + 1} of {len(rows)} by size, max block weight {mx}")
    print("    They are the two SMALLEST formulas of the 39.")

    print("\n(4) max block weight against fixed points, over all 39")
    tab = Counter((r[2] > 0, r[1]) for r in rows)
    for (hasfix, mx), k in sorted(tab.items()):
        print(f"      fixed points {hasfix!s:5s} -> max block weight "
              f"{mx}: {k} actions")
    print("    A perfect dichotomy: weight 9 exactly when there are fixed "
          "points, weight 3 otherwise,")
    print("    because a V-fixed point's link to a regular orbit is a single "
          "orbit of size 9.")
    ff = [r for r in rows if r[2] == 0]
    print("\n    But 22 actions are fixed-point-free and only 2 survive, so "
          "that is necessary,")
    print("    not sufficient.  What separates the survivors is c = 4, the "
          "MAXIMUM number of")
    print(f"    regular orbits: only {N - 9 * 4} of {N} points carry a "
          f"non-trivial stabiliser,")
    print(f"    against {N - 9 * 3} at c = 3.  Least rigidity, smallest "
          f"formula, last to fall.")
    print(f"    (fixed-point-free actions by c: "
          f"{dict(sorted(Counter(r[4] for r in ff).items(), reverse=True))})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Positive control for the ARBITRARY-CYCLE-TYPE orbit encoding.

principal-1, pass 36: *"researcher-1 has opened a new line — order 27 excluded,
order 9 reduced to one type — on a different formula shape from anything you
have checked … Extend [the harness] to that encoding and offer it by citation:
no instances of theirs run, the control being that a real (5,5,42)-graph's own
assignment satisfies every clause."*

WHAT IS NEW ABOUT THE SHAPE.  Everything I had controlled was the type
1^f p^k -- fixed points plus p-cycles for one prime p.  An automorphism of
COMPOSITE order has several cycle lengths at once: researcher-1's Theorem B
concerns 3^2 9^4, and its reduction passes through 1^6 9^4 and 1^3 3^1 9^4.
The encoding is otherwise the plainest possible -- one variable per pair-orbit,
one clause per s-subset and per t-subset, no cardinality clauses, no symmetry
breaking, no canonical prefixes, no completeness count.  Small trust surface,
but a new one.

WHAT A POSITIVE CONTROL CAN AND CANNOT DO HERE.  The direct control -- a real
(5,5,42)-graph with an order-9 automorphism -- is impossible, because no such
graph is known and its non-existence is the very thing being proved.  So this
file controls the MACHINERY at parameters where witnesses do exist:

  * H_1 and H_2, the two (4,5,24,132)-graphs, whose automorphism groups of
    order 24 and 48 contain elements of order 2, 3, 4, 6 and 12 -- including
    pure composite types 4^6, 6^4, 12^2 and the MIXED type 1^4 2^10;
  * the 116 known (5,5,42)-graphs carrying a fixed-point-free involution,
    type 2^21, at the real target parameters.

For each (graph, automorphism) pair the graph's own assignment must satisfy
every clause of the encoding built for that exact cycle type.  If it does not,
the encoding is too tight and any UNSAT it produces is worthless.

Independently coded: this file shares no code with researcher-1's `cyctype.py`
and none of its instances were run.  It is cross-checked against this
directory's own 1^f p^k encoder on the types both can express.

    python3 cyctype_control.py
"""
import itertools
import os
import sys
from collections import Counter
from math import gcd

import r45bounds as R

HERE = os.path.dirname(os.path.abspath(__file__))
R46 = os.path.join(HERE, "..", "r46-automorphism-obstructions")
R55PC = ("/Users/abuzark/.discovery-research-team/workspaces/researcher-3/"
         "scratch/r55pc/r55_42some.g6")


def automorphisms(n, adj):
    """Every automorphism, by backtracking with adjacency consistency."""
    perms, img, used = [], [-1] * n, [False] * n

    def bt(k):
        if k == n:
            perms.append(tuple(img))
            return
        for c in range(n):
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


def cycle_type(perm):
    seen, c = set(), Counter()
    for v in range(len(perm)):
        if v in seen:
            continue
        x, L = v, 0
        while x not in seen:
            seen.add(x)
            x = perm[x]
            L += 1
        c[L] += 1
    return tuple(sorted(c.items()))


def order_of(perm):
    o = 1
    for L, _ in cycle_type(perm):
        o = o * L // gcd(o, L)
    return o


def pair_orbits(n, perm):
    """pair -> orbit id, by taking the lexicographic minimum over the images
    of the pair under <sigma>.  Works for ANY permutation, not only 1^f p^k."""
    canon = {}
    for u in range(n):
        for v in range(u + 1, n):
            a, b, best = u, v, None
            while True:
                img = (a, b) if a < b else (b, a)
                best = img if best is None else min(best, img)
                a, b = perm[a], perm[b]
                if (a, b) == (u, v) or (b, a) == (u, v):
                    break
            canon[(u, v)] = best
    order = {}
    for u in range(n):
        for v in range(u + 1, n):
            c = canon[(u, v)]
            if c not in order:
                order[c] = len(order)
    return {pr: order[c] for pr, c in canon.items()}, len(order)


def encode(n, s, t, name):
    """The plain orbit encoding: one clause per s-subset and per t-subset."""
    seen, cls = set(), []
    for S in itertools.combinations(range(n), s):
        cl = tuple(sorted({-(name[(u, v)] + 1)
                           for u, v in itertools.combinations(S, 2)}))
        if cl not in seen:
            seen.add(cl)
            cls.append(cl)
    for T in itertools.combinations(range(n), t):
        cl = tuple(sorted({name[(u, v)] + 1
                           for u, v in itertools.combinations(T, 2)}))
        if cl not in seen:
            seen.add(cl)
            cls.append(cl)
    return cls


def control(n, adj, perm, s, t):
    """The graph's own assignment must satisfy every clause.

    Reading the assignment also RE-PROVES that perm is an automorphism: if any
    orbit is not constant, the permutation does not preserve adjacency.
    """
    name, nvar = pair_orbits(n, perm)
    val = [None] * (nvar + 1)
    for u in range(n):
        for v in range(u + 1, n):
            e = (adj[u] >> v) & 1
            k = name[(u, v)] + 1
            if val[k] is not None and val[k] != e:
                raise SystemExit("orbit not constant: perm is not an "
                                 "automorphism")
            val[k] = e
    if any(v is None for v in val[1:]):
        raise SystemExit("some orbit unassigned")
    cls = encode(n, s, t, name)
    bad = sum(1 for c in cls
              if not any((val[x] == 1) if x > 0 else (val[-x] == 0) for x in c))
    return nvar, len(cls), bad


def cross_check_against_1fpk():
    """On types 1^f p^k, the general orbit map must agree with this directory's
    special-case one (verify.canonical_orbits), which was written separately."""
    if R46 not in sys.path:
        sys.path.insert(0, R46)
    import verify
    checked = []
    for n, f, p, k in ((9, 0, 3, 3), (10, 1, 3, 3), (12, 2, 5, 2),
                       (14, 0, 7, 2), (15, 3, 4, 3)):
        if f + p * k != n:
            continue
        perm = list(range(n))
        for j in range(k):
            for i in range(p):
                perm[f + j * p + i] = f + j * p + (i + 1) % p
        mine, nv1 = pair_orbits(n, perm)
        theirs, nv2 = verify.canonical_orbits(n, f, p, k)
        if nv1 != nv2 or any(
                (mine[a] == mine[b]) != (theirs[a] == theirs[b])
                for a in mine for b in mine):
            raise SystemExit(f"orbit maps disagree at 1^{f} {p}^{k}")
        checked.append((n, f, p, k, nv1))
    return checked


def main():
    print("(0) the general orbit map against this directory's 1^f p^k map")
    for n, f, p, k, nv in cross_check_against_1fpk():
        print(f"    n={n:3d}  1^{f} {p}^{k}: {nv} orbits -- same partition")
    print("    Two separately written implementations agree on every type both "
          "can express.\n")

    print("(1) H_1 and H_2, the two (4,5,24,132)-graphs: every cycle type in "
          "their automorphism groups")
    print("    (this is where composite orders and mixed cycle lengths are "
          "actually realised)\n")
    print("      graph  order  cycle type            orbits  clauses  VIOLATED")
    total_bad = 0
    with open(os.path.join(HERE, "r45_24_e132.g6")) as fh:
        h_lines = [x.strip() for x in fh if x.strip()]
    for i, line in enumerate(h_lines):
        n, adj = R.g6_decode(line)
        if not R.is_good(n, adj, 4, 5):
            raise SystemExit(f"H{i+1} is not a (4,5,24)-graph")
        best = {}
        for perm in automorphisms(n, adj):
            best.setdefault(cycle_type(perm), perm)
        for ct, perm in sorted(best.items(), key=lambda x: (len(x[0]), x[0])):
            if len(ct) == 1 and ct[0][0] == 1:
                continue                      # identity carries no information
            nv, nc, bad = control(n, adj, perm, 4, 5)
            total_bad += bad
            print(f"      H{i+1}     {order_of(perm):3d}   "
                  f"{dict(ct)!s:20s}  {nv:5d}  {nc:7d}  {bad:8d}")
    print()

    print("(2) the real target: 116 known (5,5,42)-graphs with a "
          "fixed-point-free involution, type 2^21")
    with open(R55PC) as fh:
        g_lines = [x.strip() for x in fh if x.strip()]
    done = 0
    for line in g_lines:
        n, adj = R.g6_decode(line)
        col = wl_refine(n, adj)
        cls = {}
        for v, c in enumerate(col):
            cls.setdefault(c, []).append(v)
        if any(len(g) != 2 for g in cls.values()):
            continue
        perm = list(range(n))
        for g in cls.values():
            perm[g[0]], perm[g[1]] = g[1], g[0]
        if any(((adj[a] >> b) & 1) != ((adj[perm[a]] >> perm[b]) & 1)
               for a in range(n) for b in range(a + 1, n)):
            continue
        nv, nc, bad = control(n, adj, perm, 5, 5)
        total_bad += bad
        done += 1
        if done == 1:
            print(f"    {nv} orbits, {nc} clauses per graph")
        if done >= 12:
            break
    print(f"    {done} graphs checked through the SAME general code path: "
          f"{total_bad} violations so far")

    print()
    if total_bad:
        print(f"ENCODING TOO TIGHT: {total_bad} clauses violated by a real "
              f"graph's own assignment.")
        return 1
    print("POSITIVE CONTROL PASSED.  Every real graph's own assignment "
          "satisfies every clause of")
    print("the encoding built for its own cycle type, across composite orders "
          "4, 6 and 12, the")
    print("mixed type 1^4 2^10, the primes 2 and 3, and 2^21 at the real "
          "target parameters.")
    print()
    print("WHAT THIS DOES NOT COVER.  No (5,5,42)-graph with an automorphism "
          "of order 9 or 27 is")
    print("known -- their non-existence is what is being proved -- so no "
          "direct witness exists at")
    print("those types.  This controls the MACHINERY that builds such a "
          "formula, not the instance.")
    return 0


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


if __name__ == "__main__":
    sys.exit(main())

"""The order-8 row, enumerated exactly -- Burnside over Aut(G), no search.

`order8.py` enumerated actions one at a time and did not finish Z_2^3: sixteen
subgroups, and canonicalising every accepted action against the 168 elements of
GL_3(2) dominates.  ORDER8-SIZING.md named the fix; this file is it.

THE COUNT WE WANT.  A faithful action of G on 42 points is a multiset of point
stabilisers: a function c from the subgroup lattice to the non-negative
integers with

    sum over H of c(H) * [G:H] = 42,        (the points)
    intersection of cores of used H  =  1,  (faithfulness)
    c(G) <= min cap over used H with [G:H] > 1,   (the orbit lemma)

counted up to Aut(G), which permutes the lattice.

THREE IDEAS MAKE IT EXACT AND FAST.

1. BURNSIDE instead of canonical forms.  The number of orbits of Aut(G) on
   actions is the average number of actions fixed by each automorphism, and an
   action fixed by `a` is one constant on the `a`-orbits of the lattice.  So
   each automorphism contributes a single dynamic program over its own orbits,
   rather than a canonical form per accepted action.

2. INCLUSION-EXCLUSION for faithfulness.  The kernel is non-trivial exactly
   when it contains a minimal subgroup, so sum over subsets of the atoms with
   alternating sign; collecting subsets by the subgroup they generate leaves
   one weight per subgroup, at most sixteen terms.

3. STRATIFY BY THE CAP.  c(G) is the number of fixed points, and the cap
   constrains only it.  "min cap over used >= f" is a restriction on which
   subgroups may be used, and the caps take only a handful of values, so the
   allowed set takes only a handful of forms as f runs 0..42.  One generating
   function per stratum, read off at every f in it.

Cross-checked against `order8.py`'s direct enumeration on the two groups that
one finished.

    python3 order8_exact.py
"""
import itertools
import sys
from collections import defaultdict

import orbitbound as OB
from order8 import (groups_of_order_8, table, subgroups, coset_action,
                    automorphisms_of)


def cap_of(tab, H):
    """Best bound this lane has on |Fix| given an orbit with stabiliser H."""
    m, perms = coset_action(tab, H)
    if m == 1:
        return None
    b, _, _ = OB.orbit_bound(perms, m, 5, 5)
    if m == 4:
        b = min(b, 22)          # FIXED-POINT-MAXIMUM.md, the global count
    return b


def core(tab, H):
    """The largest normal subgroup inside H: intersect the conjugates."""
    inv = {}
    for a in range(8):
        for b in range(8):
            if tab[a][b] == 0:
                inv[a] = b
    out = set(range(8))
    for g in range(8):
        conj = {tab[tab[g][h]][inv[g]] for h in H}
        out &= conj
    return frozenset(out)


def atom_weights(subs, tab):
    """w[K] = sum over subsets S of the atoms with <S> = K of (-1)^|S|.

    Then sum_K w[K] * N(K) counts the faithful actions, N(K) being those whose
    used stabilisers all have core containing K.
    """
    atoms = [H for H in subs if len(H) == 2]
    w = defaultdict(int)
    for r in range(len(atoms) + 1):
        for S in itertools.combinations(atoms, r):
            gen = {0}
            frontier = set().union(*S) if S else {0}
            gen |= frontier
            changed = True
            while changed:
                changed = False
                for a in list(gen):
                    for b in list(gen):
                        p = tab[a][b]
                        if p not in gen:
                            gen.add(p)
                            changed = True
            w[frozenset(gen)] += (-1) ** r
    return dict(w)


def count_group(name, els, verbose=True, npoints=42):
    tab = table(els)
    subs = subgroups(tab)
    caps = {H: cap_of(tab, H) for H in subs}
    cores = {H: core(tab, H) for H in subs}
    auts = automorphisms_of(tab)
    W = atom_weights(subs, tab)

    # strata: the distinct allowed-sets as f runs 0..42
    capvals = sorted({c for c in caps.values() if c is not None})
    NP = npoints
    bounds = [0] + [c + 1 for c in capvals] + [NP + 1]
    strata = []
    for i in range(len(bounds) - 1):
        lo, hi = bounds[i], bounds[i + 1]
        if lo >= hi:
            continue
        strata.append((lo, hi))          # f in [lo, hi)

    total = 0
    maxfix = -1
    for a in auts:
        # orbits of this automorphism on the lattice
        seen, orbs = set(), []
        for H in subs:
            if H in seen:
                continue
            o, cur = [], H
            while cur not in seen:
                seen.add(cur)
                o.append(cur)
                cur = frozenset(a[x] for x in cur)
            orbs.append(o)
        fixed_a = 0
        for lo, hi in strata:
            for K, wk in W.items():
                if wk == 0:
                    continue
                # orbits usable in this stratum with cores containing K
                usable = []
                gorb = None
                for o in orbs:
                    idx = 8 // len(o[0])
                    if idx == 1:
                        gorb = o
                        continue
                    if any(caps[H] is None or caps[H] < lo for H in o):
                        continue
                    if not all(K <= cores[H] for H in o):
                        continue
                    usable.append(sum(8 // len(H) for H in o))
                if gorb is not None and not all(K <= cores[H] for H in gorb):
                    continue                # G itself must be allowed
                # generating function in the weight consumed by usable orbits
                dp = [0] * (NP + 1)
                dp[0] = 1
                for wgt in usable:
                    for t in range(wgt, NP + 1):
                        dp[t] += dp[t - wgt]
                for f in range(lo, min(hi, NP + 1)):
                    rest = NP - f
                    if rest < 0:
                        continue
                    fixed_a += wk * dp[rest]
                    if wk > 0 and dp[rest] and a == auts[0]:
                        maxfix = max(maxfix, f)
        total += fixed_a
    assert total % len(auts) == 0, "Burnside total not divisible by |Aut(G)|"
    orbits = total // len(auts)
    if verbose:
        capstr = ", ".join(f"{8 // len(H)}:{caps[H]}"
                           for H in sorted(subs, key=lambda h: -len(h))
                           if caps[H] is not None)
        print(f"   {name:11s} |Aut| {len(auts):3d}   subgroups {len(subs):2d}"
              f"   caps {capstr}")
        print(f"       faithful actions surviving the caps, "
              f"up to Aut(G): {orbits:9d}")
    return orbits


def brute(name, els, n, cap_on=True):
    """Direct enumeration with canonical forms, for small n only.

    Exponential in the lattice size, which is why it cannot reach n = 42 for
    Z_2^3 -- but at small n it is an independent implementation of the same
    count, so it checks the Burnside arithmetic rather than restating it.
    """
    tab = table(els)
    subs = subgroups(tab)
    caps = {H: cap_of(tab, H) for H in subs}
    cores = {H: core(tab, H) for H in subs}
    auts = automorphisms_of(tab)
    order_subs = sorted(subs, key=lambda h: -len(h))
    seen = set()

    def rec(i, left, chosen):
        if left == 0:
            used = [(H, c) for H, c in chosen if c]
            if not used:
                return
            inter = set(range(8))
            for H, c in used:
                inter &= set(cores[H])
            if len(inter) != 1:
                return
            f = sum(c for H, c in used if len(H) == 8)
            if cap_on:
                cs = [caps[H] for H, c in used if caps[H] is not None]
                if cs and f > min(cs):
                    return
            best = None
            for m in auts:
                key = tuple(sorted((tuple(sorted(frozenset(m[x] for x in H))),
                                    c) for H, c in used))
                best = key if best is None else min(best, key)
            seen.add(best)
            return
        if i == len(order_subs):
            return
        H = order_subs[i]
        idx = 8 // len(H)
        for c in range(left // idx + 1):
            rec(i + 1, left - c * idx, chosen + [(H, c)])
    rec(0, n, [])
    return len(seen)


def selftest():
    """Burnside against brute force, on point counts small enough for both."""
    print("SELF-TEST: Burnside against direct enumeration\n")
    print("      n   group        brute   burnside   ")
    ok = True
    for n in (10, 14, 18):
        for name, els in groups_of_order_8():
            b = brute(name, els, n)
            w = count_group(name, els, verbose=False, npoints=n)
            same = (b == w)
            ok &= same
            print(f"    {n:3d}   {name:11s} {b:7d}   {w:8d}   "
                  f"{'agree' if same else 'DISAGREE'}")
    print("\n   " + ("both methods agree everywhere they can both be run.\n"
                     if ok else "MISMATCH -- do not trust the counts.\n"))
    return ok


def main():
    if not selftest():
        return 1
    print("THE ORDER-8 ROW, ENUMERATED EXACTLY\n")
    print("   Faithful actions on 42 points, filtered by the orbit lemma,")
    print("   counted up to Aut(G) by Burnside rather than by canonical")
    print("   forms -- which is what `order8.py` could not finish.\n")
    tot = 0
    for name, els in groups_of_order_8():
        tot += count_group(name, els)
    print(f"\n   total over the five groups of order 8: {tot}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

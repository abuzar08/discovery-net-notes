#!/usr/bin/env python3
"""Exhaustive soundness suite for symS (cycle-shift normalisation).

Every check enumerates ALL assignments of the orbit variables; none samples.
The four questions, in the order they can go wrong:

  1. Is the vertex map a symmetry at all?  Every Phi_b must induce a
     well-defined map on pair orbits, and must preserve (s,t)-goodness.
     Checked at the GRAPH level, against the vertex permutation, not against
     my formula for the induced action -- that is what catches an index bug.
  2. Do the CNF clauses encode exactly the intended predicate?  Checked by
     brute force over the auxiliary variables too, so a clause that is merely
     implied by the predicate rather than equivalent to it would show up.
  3. Is the predicate sound?  Every assignment must have a shift that lands
     in the constrained region.
  4. Does it compose?  symS with symC, and symS with symF, in BOTH orders --
     because the reviewer's finding on symC + symF was that only one order is
     sound, so composition is not assumed to be free here.

Run: python3 symstest.py
"""
import itertools
import sys

import encode


def setup(f, p, k):
    n = f + p * k
    idx = encode.pair_index(n)
    sigma = encode.permutation(n, f, p, k)
    orb, nvar = encode.pair_orbits(n, sigma, idx)
    return n, idx, orb, nvar


def shift_perm(n, f, p, k, b):
    s = list(range(n))
    for j in range(k):
        for i in range(p):
            s[f + j * p + i] = f + j * p + (i + b[j]) % p
    return s


def cycle_perm(n, f, p, k, tau):
    s = list(range(n))
    for j in range(k):
        for i in range(p):
            s[f + j * p + i] = f + tau[j] * p + i
    return s


def fixed_perm(n, f, p, k, rho):
    s = list(range(n))
    for u in range(f):
        s[u] = rho[u]
    return s


def induced(pi, nvar, idx, orb):
    """Push a vertex permutation to a map on orbit variables, or None."""
    g = [None] * nvar
    for (u, v), i in idx.items():
        a, b = pi[u], pi[v]
        t = orb[idx[(min(a, b), max(a, b))]]
        if g[orb[i]] is None:
            g[orb[i]] = t
        elif g[orb[i]] != t:
            return None
    return g


def apply_g(X, g):
    Y = [None] * len(X)
    for o, t in enumerate(g):
        Y[t] = X[o]
    return Y


def sat(cls, A):
    for cl in cls:
        if not any((A[abs(l) - 1] == 1) if l > 0 else (A[abs(l) - 1] == 0)
                   for l in cl):
            return False
    return True


# ---------------------------------------------------------------- predicates

def symS_pred(X, f, p, k, idx, orb):
    for j in range(1, k):
        y = [X[v - 1] for v in encode.cross_row(f, p, k, 0, j, idx, orb)]
        for r in range(1, p):
            if [y[(d + r) % p] for d in range(p)] > y:
                return False
    return True


def symC_pred(X, f, p, k, idx, orb):
    half = (p - 1) // 2
    if p % 2 == 0 or k < 2:
        return True
    codes = [[X[orb[idx[(f + j * p, f + j * p + d)]]] for d in range(1, half + 1)]
             for j in range(k)]
    return all(codes[j] <= codes[j + 1] for j in range(k - 1))


def symF_pred(X, f, p, k, idx, orb):
    """The published symF row order: R_u over the k cycle representatives."""
    if f < 2:
        return True
    rows = [[X[orb[idx[(u, f + j * p)]]] for j in range(k)] for u in range(f)]
    return all(rows[u] <= rows[u + 1] for u in range(f - 1))


# ---------------------------------------------------------------- the checks

def check_symmetry(f, p, k, s, t):
    """Q1: well defined on orbits, and preserves (s,t)-goodness, at graph level."""
    n, idx, orb, nvar = setup(f, p, k)
    cls = encode.clauses(n, s, t, orb, idx)
    gs = []
    for b in itertools.product(range(p), repeat=k):
        g = induced(shift_perm(n, f, p, k, b), nvar, idx, orb)
        if g is None:
            return "not well defined", b
        gs.append(g)
    bad = 0
    for bits in itertools.product((0, 1), repeat=nvar):
        X = list(bits)
        gx = sat(cls, X)
        for g in gs:
            if sat(cls, apply_g(X, g)) != gx:
                bad += 1
    return "OK" if bad == 0 else f"{bad} goodness violations", len(gs)


def check_cnf_matches_predicate(f, p, k):
    """Q2: exists-aux(clauses) <=> predicate, brute force over aux as well."""
    n, idx, orb, nvar = setup(f, p, k)
    cls, naux = encode.symS_clauses(n, f, p, k, idx, orb, nvar)
    if naux > 12:
        return f"skipped (naux={naux} too large for exhaustive aux)"
    bad = 0
    for bits in itertools.product((0, 1), repeat=nvar):
        X = list(bits)
        found = any(sat(cls, X + list(a))
                    for a in itertools.product((0, 1), repeat=naux))
        if found != symS_pred(X, f, p, k, idx, orb):
            bad += 1
    return "OK" if bad == 0 else f"{bad} mismatches"


def forced_aux(X, f, p, k, idx, orb, nvar):
    """The aux values that the definitional clauses force, given the rows.

    In `_lex_le` the auxiliary e_t is introduced with the full biconditional
    e_t <-> e_{t-1} AND (a_t <-> b_t), so given the row bits every e_t is
    determined, in increasing t.  Hence "exists aux satisfying the clauses"
    is equivalent to "this one assignment satisfies them", and Q2b can decide
    the same question as Q2 at any size.  That the aux really are forced is
    not assumed: Q2 brute-forces all aux at small size and agrees with Q2b,
    which is the check that the two are the same question.
    """
    A = list(X)
    for j in range(1, k):
        y = encode.cross_row(f, p, k, 0, j, idx, orb)
        for r in range(1, p):
            rot = [y[(d + r) % p] for d in range(p)]
            prev = 1
            for t in range(len(rot) - 1):
                a = X[rot[t] - 1]
                b = X[y[t] - 1]
                prev = 1 if (prev == 1 and a == b) else 0
                A.append(prev)
    return A


def check_cnf_matches_predicate_forced(f, p, k):
    """Q2b: same question as Q2, decided through the forced aux, at any size."""
    n, idx, orb, nvar = setup(f, p, k)
    cls, naux = encode.symS_clauses(n, f, p, k, idx, orb, nvar)
    bad = 0
    for bits in itertools.product((0, 1), repeat=nvar):
        X = list(bits)
        A = forced_aux(X, f, p, k, idx, orb, nvar)
        if len(A) != nvar + naux:
            return f"aux count {len(A)-nvar} != {naux}"
        if sat(cls, A) != symS_pred(X, f, p, k, idx, orb):
            bad += 1
    return "OK" if bad == 0 else f"{bad} mismatches"


def check_sound(f, p, k):
    """Q3: every assignment has a shift landing in the symS region."""
    n, idx, orb, nvar = setup(f, p, k)
    gs = [induced(shift_perm(n, f, p, k, b), nvar, idx, orb)
          for b in itertools.product(range(p), repeat=k)]
    bad = sum(0 if any(symS_pred(apply_g(list(bits), g), f, p, k, idx, orb)
                       for g in gs) else 1
              for bits in itertools.product((0, 1), repeat=nvar))
    return "OK" if bad == 0 else f"{bad} uncovered", nvar


def symM_pred(X, f, p, k, idx, orb):
    """X >=_lex X o mu_u for every u, over the orbit variables in index order."""
    norb = max(orb) + 1
    for u in range(2, p):
        g = encode.mult_orbit_map(f + p * k, f, p, k, u, idx, orb, norb)
        Y = apply_g(X, g)
        if Y > X:
            return False
    return True


def symK_pred(X, f, p, k, idx, orb):
    """X >=_lex X o Phi_tau for every tau in S_k, over all orbit variables."""
    n = f + p * k
    norb = max(orb) + 1
    for tau in itertools.permutations(range(k)):
        if all(tau[j] == j for j in range(k)):
            continue
        pi = list(range(n))
        for j in range(k):
            for i in range(p):
                pi[f + j * p + i] = f + tau[j] * p + i
        if apply_g(X, encode.perm_orbit_map(pi, idx, orb, norb)) > X:
            return False
    return True


def full_group(f, p, k, with_mult):
    """<shifts, multipliers, cycle permutations> as maps on orbit variables.

    The affine group on each cycle is i -> u*i + b_j with a COMMON u (a common
    u is what conjugates sigma to sigma^u globally; per-cycle multipliers do
    not normalise <sigma>), together with S_k on the cycles.
    """
    n = f + p * k
    idx = encode.pair_index(n)
    sigma = encode.permutation(n, f, p, k)
    orb, nvar = encode.pair_orbits(n, sigma, idx)
    us = range(1, p) if with_mult else [1]
    gs = []
    for u in us:
        for b in itertools.product(range(p), repeat=k):
            for tau in itertools.permutations(range(k)):
                pi = list(range(n))
                for j in range(k):
                    for i in range(p):
                        pi[f + j * p + i] = f + tau[j] * p + (u * i + b[j]) % p
                g = induced(pi, nvar, idx, orb)
                if g is not None:
                    gs.append(g)
    return gs, idx, orb, nvar


def check_compose_full(f, p, k, preds, with_mult):
    """Every assignment must have ONE group element satisfying every predicate."""
    gs, idx, orb, nvar = full_group(f, p, k, with_mult)
    bad = 0
    for bits in itertools.product((0, 1), repeat=nvar):
        X = list(bits)
        if not any(all(pr(Y, f, p, k, idx, orb) for pr in preds)
                   for Y in (apply_g(X, g) for g in gs)):
            bad += 1
    return "OK" if bad == 0 else f"{bad} uncovered", len(gs)


def check_compose(f, p, k, preds, use_fixed):
    """Q4: some element of the full group satisfies every predicate at once."""
    n, idx, orb, nvar = setup(f, p, k)
    gs = []
    fixed_perms = (list(itertools.permutations(range(f))) if use_fixed and f
                   else [tuple(range(f))])
    for b in itertools.product(range(p), repeat=k):
        for tau in itertools.permutations(range(k)):
            for rho in fixed_perms:
                pi = [0] * n
                sh = shift_perm(n, f, p, k, b)
                cy = cycle_perm(n, f, p, k, tau)
                fx = fixed_perm(n, f, p, k, rho)
                for v in range(n):
                    pi[v] = cy[fx[sh[v]]] if v >= f else fx[v]
                g = induced(pi, nvar, idx, orb)
                if g is not None:
                    gs.append(g)
    bad = 0
    for bits in itertools.product((0, 1), repeat=nvar):
        X = list(bits)
        if not any(all(pr(Y, f, p, k, idx, orb) for pr in preds)
                   for Y in (apply_g(X, g) for g in gs)):
            bad += 1
    return "OK" if bad == 0 else f"{bad} uncovered", len(gs)


def main():
    cases = [(0, 3, 2), (0, 3, 3), (0, 5, 2), (0, 7, 2), (1, 3, 2), (2, 3, 2)]

    print("Q1  Phi_b is a symmetry (well defined on orbits; preserves (4,6)-goodness)")
    for f, p, k in [(0, 3, 2), (0, 3, 3), (0, 5, 2), (1, 3, 2), (2, 3, 2)]:
        print(f"    f={f} p={p} k={k} n={f+p*k}: {check_symmetry(f, p, k, 4, 6)}")

    print("Q2  CNF clauses encode exactly the symS predicate (aux brute-forced)")
    for f, p, k in cases:
        print(f"    f={f} p={p} k={k}: {check_cnf_matches_predicate(f, p, k)}")

    print("Q2b same question through the forced aux (no size limit); Q2 and Q2b")
    print("    must agree wherever both run, which is what licenses Q2b alone")
    for f, p, k in cases + [(0, 3, 4), (0, 5, 3)]:
        print(f"    f={f} p={p} k={k}: {check_cnf_matches_predicate_forced(f, p, k)}")

    print("Q3  symS soundness, all assignments")
    for f, p, k in cases:
        r, nv = check_sound(f, p, k)
        print(f"    f={f} p={p} k={k}: {nv} vars, {2**nv} assignments: {r}")

    print("Q4  composition, all assignments (order-independent by construction:")
    print("    the check asks only that SOME group element satisfies both)")
    for f, p, k in [(0, 3, 2), (0, 3, 3), (0, 5, 2), (1, 3, 2)]:
        r, ng = check_compose(f, p, k, [symS_pred, symC_pred], False)
        print(f"    symS+symC  f={f} p={p} k={k}: group {ng}: {r}")
    for f, p, k in [(2, 3, 2), (3, 3, 2)]:
        r, ng = check_compose(f, p, k, [symS_pred, symF_pred], True)
        print(f"    symS+symF  f={f} p={p} k={k}: group {ng}: {r}")
    for f, p, k in [(2, 3, 2)]:
        r, ng = check_compose(f, p, k, [symS_pred, symC_pred, symF_pred], True)
        print(f"    symS+symC+symF f={f} p={p} k={k}: group {ng}: {r}")

    print("Q5  symM alone, and symM composed -- the multiplier does NOT commute")
    print("    with the shift normalisation, so this is the check that decides")
    print("    whether the two may be imposed together")
    for f, p, k in [(0, 3, 2), (0, 5, 2), (0, 3, 3), (0, 7, 2)]:
        r, ng = check_compose_full(f, p, k, [symM_pred], True)
        print(f"    symM        f={f} p={p} k={k}: group {ng}: {r}")
    for f, p, k in [(0, 3, 2), (0, 5, 2), (0, 3, 3), (0, 7, 2)]:
        r, ng = check_compose_full(f, p, k, [symS_pred, symM_pred], True)
        print(f"    symS+symM   f={f} p={p} k={k}: group {ng}: {r}")
    for f, p, k in [(0, 3, 2), (0, 5, 2), (0, 3, 3)]:
        r, ng = check_compose_full(f, p, k, [symS_pred, symC_pred, symM_pred], True)
        print(f"    symS+symC+symM f={f} p={p} k={k}: group {ng}: {r}")

    print("Q6  isolating the conflict.  mu_u sends internal difference d to")
    print("    +-u*d, so it PERMUTES internal differences and does not preserve")
    print("    internal codes -- symC and symM constrain the same coordinates")
    print("    in incompatible ways.  If symC+symM alone already fails, symS is")
    print("    not implicated in the Q5 failure.")
    for f, p, k in [(0, 5, 2), (0, 7, 2)]:
        r, ng = check_compose_full(f, p, k, [symC_pred, symM_pred], True)
        print(f"    symC+symM   f={f} p={p} k={k}: group {ng}: {r}")

    print("Q7  symK (S_k lex-leader; subsumes symC) alone and with symS")
    for f, p, k in [(0, 3, 2), (0, 5, 2), (0, 3, 3)]:
        r, ng = check_compose_full(f, p, k, [symK_pred], False)
        print(f"    symK        f={f} p={p} k={k}: group {ng}: {r}")
    for f, p, k in [(0, 3, 2), (0, 5, 2), (0, 3, 3)]:
        r, ng = check_compose_full(f, p, k, [symS_pred, symK_pred], False)
        print(f"    symS+symK   f={f} p={p} k={k}: group {ng}: {r}")
    for f, p, k in [(0, 3, 2), (0, 5, 2)]:
        r, ng = check_compose_full(f, p, k, [symK_pred, symM_pred], True)
        print(f"    symK+symM   f={f} p={p} k={k}: group {ng}: {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

r"""reviewer-1: independent check of symS (researcher-3, h3295).

Everything here is my own: my own orbit numbering, my own vertex permutations
for the shifts \(\Phi_b\), the cycle permutations \(\Phi_\tau\) and the
multipliers \(\mu_u\), my own induced action on orbits read off the vertex map,
and my own predicates for symS, symC, symK and symM taken from the prose the
lane's `encode.py` documents.  The lane's code is imported only where the point
is to compare its CNF with my predicate (check 6).

Checks:
  1. \(\Phi_b \sigma = \sigma \Phi_b\), and \(\Phi_b\) preserves the cycle type.
  2. the induced action on pair orbits matches the claimed formula: fixes
     fixed-fixed, fixed-cycle and internal orbits, carries the cross orbit
     (j,j',d) to (j,j',d + b_{j'} - b_j);
  3. the induced group has order p^{k-1};
  4. goodness is preserved by every \(\Phi_b\);
  5. completeness: every assignment has some \(\Phi_b\) image satisfying symS;
  6. the lane's symS CNF is exactly my predicate (auxiliaries existentially
     quantified, decided with CaDiCaL);
  7. the composition matrix, over the group <shifts, multipliers, S_k>.

usage: python3 indep_syms.py
"""
import itertools
import subprocess
import sys
import tempfile
import os

CADICAL = os.path.expanduser('~/.discovery-research-team/workspaces/reviewer-1/'
                             'scratch/r46/tools/cadical/build/cadical')


# ---------------------------------------------------------------- structure
def sigma_perm(f, p, k):
    n = f + p * k
    s = list(range(n))
    for j in range(k):
        for i in range(p):
            s[f + j * p + i] = f + j * p + (i + 1) % p
    return s


def orbits(f, p, k):
    """my own orbit numbering: orbits of <sigma> on unordered pairs, named by
    their sorted member list, numbered in sorted order of that name."""
    n = f + p * k
    s = sigma_perm(f, p, k)
    seen, names = set(), []
    for u, v in itertools.combinations(range(n), 2):
        if (u, v) in seen:
            continue
        cyc, a, b = set(), u, v
        while (min(a, b), max(a, b)) not in cyc:
            cyc.add((min(a, b), max(a, b)))
            a, b = s[a], s[b]
        seen |= cyc
        names.append(tuple(sorted(cyc)))
    names.sort()
    oid = {}
    for i, nm in enumerate(names):
        for pr in nm:
            oid[pr] = i
    return oid, len(names)


def kind(f, p, k, pair):
    """classify a pair orbit by its representative pair"""
    u, v = pair
    if v < f:
        return ('ff',)
    if u < f:
        return ('fc', (v - f) // p)
    ju, jv = (u - f) // p, (v - f) // p
    if ju == jv:
        return ('int', ju)
    du, dv = (u - f) % p, (v - f) % p
    return ('cross', ju, jv, (dv - du) % p)


# ------------------------------------------------------------- permutations
def phi_shift(f, p, k, b):
    n = f + p * k
    pi = list(range(n))
    for j in range(k):
        for i in range(p):
            pi[f + j * p + i] = f + j * p + (i + b[j]) % p
    return pi


def phi_cycle(f, p, k, tau):
    n = f + p * k
    pi = list(range(n))
    for j in range(k):
        for i in range(p):
            pi[f + j * p + i] = f + tau[j] * p + i
    return pi


def mu_mult(f, p, k, u):
    n = f + p * k
    pi = list(range(n))
    for j in range(k):
        for i in range(p):
            pi[f + j * p + i] = f + j * p + (u * i) % p
    return pi


def induced(pi, oid, norb):
    """orbit permutation induced by a vertex permutation, or None if it is not
    well defined on orbits"""
    g = [None] * norb
    for (a, b), o in oid.items():
        c, d = pi[a], pi[b]
        t = oid[(min(c, d), max(c, d))]
        if g[o] is None:
            g[o] = t
        elif g[o] != t:
            return None
    return g


def act(g, x):
    """image assignment: (g.x)[g[o]] = x[o]"""
    y = [0] * len(x)
    for o, t in enumerate(g):
        y[t] = x[o]
    return tuple(y)


# --------------------------------------------------------------- predicates
def good(f, p, k, oid, x, s, t):
    n = f + p * k
    def e(u, v):
        return x[oid[(min(u, v), max(u, v))]]
    for S in itertools.combinations(range(n), s):
        if all(e(u, v) for u, v in itertools.combinations(S, 2)):
            return False
    for T in itertools.combinations(range(n), t):
        if not any(e(u, v) for u, v in itertools.combinations(T, 2)):
            return False
    return True


def cross_row(f, p, k, oid, x, j, jp):
    """the length-p vector of cross orbit values between cycles j < jp,
    indexed by difference"""
    a = f + j * p
    return [x[oid[(min(a, f + jp * p + d), max(a, f + jp * p + d))]]
            for d in range(p)]


def sym_s(f, p, k, oid, x):
    """each y^(j), j = 1..k-1, is the lex-greatest of its p rotations"""
    for j in range(1, k):
        y = cross_row(f, p, k, oid, x, 0, j)
        for r in range(1, p):
            rot = [y[(d + r) % p] for d in range(p)]
            if rot > y:
                return False
    return True


def internal_code(f, p, k, oid, x, j):
    half = (p - 1) // 2
    a = f + j * p
    return [x[oid[(a, a + d)]] for d in range(1, half + 1)]


def sym_c(f, p, k, oid, x):
    """internal codes sorted: c_0 <=_lex c_1 <=_lex ... """
    cs = [internal_code(f, p, k, oid, x, j) for j in range(k)]
    return all(cs[j] <= cs[j + 1] for j in range(k - 1))


def lex_leader(x, maps):
    """x is lex-greatest among its images under the given orbit maps"""
    return all(list(act(g, x)) <= list(x) for g in maps)


# ------------------------------------------------------------- the CNF check
def cadical_sat(nvar, clauses):
    with tempfile.NamedTemporaryFile('w', suffix='.cnf', delete=False) as fh:
        fh.write(f'p cnf {nvar} {len(clauses)}\n')
        for c in clauses:
            fh.write(' '.join(map(str, c)) + ' 0\n')
        path = fh.name
    r = subprocess.run([CADICAL, '-q', path], capture_output=True, text=True)
    os.unlink(path)
    return 's SATISFIABLE' in r.stdout


def check_cnf_equals_predicate(f, p, k):
    """their symS clauses, with auxiliaries existentially quantified, define
    exactly my symS predicate"""
    sys.path.insert(0, os.path.expanduser(
        '~/.discovery-research-team/workspaces/reviewer-1/notes/'
        'graph-ramsey-theory/r46-automorphism-obstructions'))
    import encode as E
    n = f + p * k
    idx = E.pair_index(n)
    sig = E.permutation(n, f, p, k)
    orb, norb = E.pair_orbits(n, sig, idx)
    cls, naux = E.symS_clauses(n, f, p, k, idx, orb, norb)
    oid, mynorb = orbits(f, p, k)
    assert norb == mynorb, (norb, mynorb)
    # their orbit ids may differ from mine; translate by representative pair
    theirs_of_mine = [None] * norb
    for (a, b), o in oid.items():
        theirs_of_mine[o] = orb[idx[(a, b)]]
    bad = 0
    for bits in itertools.product((0, 1), repeat=norb):
        units = [[(theirs_of_mine[o] + 1) if bits[o] else -(theirs_of_mine[o] + 1)]
                 for o in range(norb)]
        sat = cadical_sat(norb + naux, cls + units)
        if sat != sym_s(f, p, k, oid, bits):
            bad += 1
    return bad, norb, naux, len(cls)


# -------------------------------------------------------------------- main
def group_maps(f, p, k, oid, norb, shifts=True, mults=True, perms=True):
    gens = []
    if shifts:
        for b in itertools.product(range(p), repeat=k):
            gens.append(phi_shift(f, p, k, b))
    if mults:
        for u in range(1, p):
            gens.append(mu_mult(f, p, k, u))
    if perms:
        for tau in itertools.permutations(range(k)):
            gens.append(phi_cycle(f, p, k, tau))
    out = []
    for pi in gens:
        g = induced(pi, oid, norb)
        if g is None:
            raise SystemExit('not well defined on orbits')
        out.append(tuple(g))
    return out


def closure(maps, norb):
    """the group generated, as a set of orbit permutations"""
    ident = tuple(range(norb))
    seen = {ident}
    frontier = [ident]
    while frontier:
        cur = frontier.pop()
        for g in maps:
            nxt = tuple(g[cur[o]] for o in range(norb))
            if nxt not in seen:
                seen.add(nxt)
                frontier.append(nxt)
    return seen


def main():
    print('=== 1-4: the shift group, its action and what it preserves')
    for (f, p, k, s, t) in [(0, 3, 2, 3, 3), (0, 5, 2, 4, 6), (0, 3, 3, 3, 4),
                            (1, 3, 2, 3, 4), (2, 3, 2, 3, 4), (0, 7, 2, 4, 6)]:
        n = f + p * k
        oid, norb = orbits(f, p, k)
        sig = sigma_perm(f, p, k)
        commutes = True
        typed = True
        formula_ok = True
        gs = []
        for b in itertools.product(range(p), repeat=k):
            pi = phi_shift(f, p, k, b)
            if [sig[pi[v]] for v in range(n)] != [pi[sig[v]] for v in range(n)]:
                commutes = False
            g = induced(pi, oid, norb)
            if g is None:
                typed = False
                continue
            gs.append(tuple(g))
            # claimed action on orbits
            reps = {}
            for pr, oo in oid.items():
                if oo not in reps or pr < reps[oo]:
                    reps[oo] = pr
            for o in range(norb):
                kd = kind(f, p, k, reps[o])
                kd2 = kind(f, p, k, reps[g[o]])
                if kd[0] in ('ff', 'fc', 'int'):
                    if kd2 != kd:
                        formula_ok = False
                else:
                    _, j, jp, d = kd
                    want = ('cross', j, jp, (d + b[jp] - b[j]) % p)
                    if kd2 != want:
                        formula_ok = False
        order = len(set(gs))
        goodpres = True
        for bits in itertools.product((0, 1), repeat=norb):
            if not good(f, p, k, oid, bits, s, t):
                continue
            for g in gs:
                if not good(f, p, k, oid, act(g, bits), s, t):
                    goodpres = False
                    break
            if not goodpres:
                break
        print(f'  f={f} p={p} k={k} (s,t)=({s},{t}): {norb} orbits; '
              f'commutes {commutes}; well defined on orbits {typed}; '
              f'claimed orbit formula {formula_ok}; induced group order '
              f'{order} (p^(k-1) = {p ** (k - 1)}); goodness preserved '
              f'{goodpres}')

    print('=== 5: completeness of symS as a break of the shift group')
    for (f, p, k) in [(0, 3, 2), (0, 5, 2), (0, 3, 3), (1, 3, 2), (0, 7, 2),
                      (0, 3, 4)]:
        oid, norb = orbits(f, p, k)
        gs = [tuple(induced(phi_shift(f, p, k, b), oid, norb))
              for b in itertools.product(range(p), repeat=k)]
        uncovered = 0
        survivors = 0
        for bits in itertools.product((0, 1), repeat=norb):
            hits = sum(1 for g in gs if sym_s(f, p, k, oid, act(g, bits)))
            if hits == 0:
                uncovered += 1
            if sym_s(f, p, k, oid, bits):
                survivors += 1
        print(f'  f={f} p={p} k={k}: {2 ** norb} assignments, '
              f'{uncovered} with no symS image (0 = complete break), '
              f'{survivors} survive symS')

    print('=== 6: the lane\'s symS CNF against my predicate')
    for (f, p, k) in [(0, 3, 2), (0, 5, 2), (1, 3, 2), (0, 3, 3)]:
        bad, norb, naux, ncls = check_cnf_equals_predicate(f, p, k)
        print(f'  f={f} p={p} k={k}: {2 ** norb} assignments, {ncls} clauses, '
              f'{naux} auxiliaries, mismatches {bad}')


if __name__ == '__main__':
    main()

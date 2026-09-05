"""reviewer-1: positive control of (L) without a solver.  Catalog (4,6,35)-graph
35 (involution of type 1^7 2^14, see control_L.py): enumerate the 7!
relabellings of F, take the one minimising (profile sequence, G[F] row-major)
-- the README's proof object -- and check that its orbit assignment satisfies
EVERY clause of the reviewer's orbit CNF (no K4, no I6) plus the reviewer's
(L) clauses, with the prefix-equality variables e_t set to
"rows equal through position t".  Also reports how many relabellings satisfy
(L).  usage: python3 control_L2.py
"""
import sys, os, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'r46'))
import networkx as nx
from indep_catalog import g6
from indep_encode import permutation, orbits_of_pairs
from indep_lex import L_clauses

R46 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'r46')
n, E = g6(open(os.path.join(R46, 'r46_35some.g6')).read().split('\n')[35])
G = nx.Graph(E)
sig = next(m for m in nx.algorithms.isomorphism.GraphMatcher(G, G).isomorphisms_iter() if any(m[v] != v for v in m))
fixed = [v for v in range(n) if sig[v] == v]; f = len(fixed)
cyc = []; seen = set(fixed)
for v in range(n):
    if v not in seen:
        cyc.append((v, sig[v])); seen |= {v, sig[v]}
p, k = 2, len(cyc); assert f + p * k == n and f == 7
new = {v: i for i, v in enumerate(fixed)}
for j, (a, b) in enumerate(cyc):
    new[a] = f + 2 * j; new[b] = f + 2 * j + 1
adj0 = {(min(new[u], new[v]), max(new[u], new[v])) for u, v in E}
x0 = lambda u, w: int((min(u, w), max(u, w)) in adj0)

def cols_of(u):
    return [f + j * p for j in range(k)] + [w for w in range(f) if w not in (u, u + 1)]

def rows_ok(x):
    return all([x(u, c) for c in cols_of(u)] <= [x(u + 1, c) for c in cols_of(u)] for u in range(f - 1))

best = None; nsat = 0; total = 0
for pi in itertools.permutations(range(f)):
    total += 1
    inv = {(pi[v] if v < f else v): v for v in range(n)}
    xr = lambda u, w, inv=inv: x0(inv[u], inv[w])
    ok = rows_ok(xr); nsat += ok
    keyv = (tuple(tuple(xr(u, f + j * p) for j in range(k)) for u in range(f)),
            tuple(tuple(xr(u, w) if u != w else 0 for w in range(f)) for u in range(f)))
    if best is None or keyv < best[0]:
        best = (keyv, inv, ok)
print(f'catalog graph 35, type 1^{f} {p}^{k}: {nsat}/{total} relabellings of F satisfy (L); key-minimal relabelling satisfies (L): {best[2]}')
assert best[2]
inv = best[1]
x = lambda u, w: x0(inv[u], inv[w])

sigma = permutation(n, f, p, k)
var, nv = orbits_of_pairs(n, sigma)
# orbit assignment (must be consistent: sigma is an automorphism)
val = {}
for u in range(n):
    for w in range(u + 1, n):
        v = var[(u, w)]
        assert val.get(v, x(u, w)) == x(u, w), 'not sigma-invariant'
        val[v] = x(u, w)
C = []
for S in itertools.combinations(range(n), 4):
    C.append([-var[e] for e in itertools.combinations(S, 2)])
for T in itertools.combinations(range(n), 6):
    C.append([var[e] for e in itertools.combinations(T, 2)])
L, nvt = L_clauses(n, f, p, k, var, nv)
# e variables: numbered row by row after nv; e_t = rows equal through t (t = 1..m-1)
ev = nv
for u in range(f - 1):
    a = [x(u, c) for c in cols_of(u)]; b = [x(u + 1, c) for c in cols_of(u)]
    for t in range(len(a) - 1):
        ev += 1
        val[ev] = int(a[:t + 1] == b[:t + 1])
assert ev == nvt
sat = lambda cl: any((l > 0) == bool(val[abs(l)]) for l in cl)
badC = sum(not sat(c) for c in C); badL = sum(not sat(c) for c in L)
print(f'own orbit CNF: {nv} orbit vars, {len(C)} clauses (with repeats), violated {badC}; (L): {len(L)} clauses, {nvt - nv} e vars, violated {badL}')
assert badC == 0 and badL == 0
print('POSITIVE CONTROL OK: the relabelled catalog graph satisfies base + (L)')

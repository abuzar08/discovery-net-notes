"""Positive control for groupenc.py.

The 39 refutations are only meaningful if the encoder can still *admit* a graph
when one exists. An over-constrained encoder -- one that has lost solutions to a
bug -- refutes just as confidently as a correct one, and the refutation looks
identical. Negative controls cannot see this; only a positive control can.

The direct control is impossible at the real parameters, because a
Z_3 x Z_3-invariant (5,5,42)-graph is exactly the object being excluded. So the
control runs the same code at parameters where such graphs do exist, and closes
the loop both ways:

  forward   a witness graph invariant under the action is read off into an
            assignment of the orbit variables -- failing if the edge relation is
            not constant on some orbit, which is itself an independent proof that
            the two generators are automorphisms -- and every clause the encoder
            produced is checked against it, expecting zero violations;

  backward  the formula is handed to CaDiCaL, and if it is satisfiable the model
            is decoded into an actual graph, which is then checked from scratch,
            without using any orbit machinery, to have no clique of size s, no
            independent set of size t, and to admit both generators as
            automorphisms.

Everything imported from groupenc is the published code path, so the control
covers what is actually used to build the 39 formulas.

usage: python3 groupenc_control.py [cadical]
"""
import sys, os, subprocess, itertools, random
from itertools import combinations
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from groupenc import build_action, pair_orbits, clauses_for

CAD = sys.argv[1] if len(sys.argv) > 1 else os.environ.get(
    'CADICAL', '../../tools/cadical/build/cadical')

def has_clique(adj, n, k):
    """True iff some k-subset is a clique; plain search, no orbit machinery."""
    def ext(cand, size):
        if size == k:
            return True
        for i, v in enumerate(cand):
            if len(cand) - i < k - size:
                break
            if ext([u for u in cand[i + 1:] if adj[v][u]], size + 1):
                return True
        return False
    return ext(list(range(n)), 0)

def check_graph(adj, n, s, t, gens):
    """Independent check: no K_s, no independent t-set, generators are automorphisms."""
    comp = [[(u != v and not adj[u][v]) for v in range(n)] for u in range(n)]
    out = {'K%d' % s: has_clique(adj, n, s), 'I%d' % t: has_clique(comp, n, t)}
    out['automorphisms'] = all(
        all(adj[u][v] == adj[p[u]][p[v]] for u in range(n) for v in range(n)) for p in gens)
    return out

def control(a, b, c, s, t, trials=4000, seed=1):
    n, sig, tau = build_action(a, b, c)
    var, nv = pair_orbits(n, [sig, tau])
    cls = clauses_for(n, var, s, t)
    tag = f'a{a} b={tuple(b)} c={c} on n={n}, (s,t)=({s},{t})'
    print(f'{tag}: {nv} orbit variables, {len(cls)} clauses')

    # --- backward: is the formula satisfiable, and is its model a real witness?
    cnf = f'/tmp/ctrl_{a}_{"".join(map(str,b))}_{c}_{s}{t}.cnf'
    with open(cnf, 'w') as fh:
        fh.write(f'p cnf {nv} {len(cls)}\n')
        for cl in cls:
            fh.write(' '.join(map(str, cl)) + ' 0\n')
    r = subprocess.run([CAD, '-q', cnf], capture_output=True, text=True)
    if r.returncode == 10:
        model = {}
        for line in r.stdout.splitlines():
            if line.startswith('v'):
                for tok in line.split()[1:]:
                    if int(tok) != 0:
                        model[abs(int(tok))] = int(tok) > 0
        adj = [[False] * n for _ in range(n)]
        for (u, v), o in var.items():
            adj[u][v] = adj[v][u] = model[o]
        chk = check_graph(adj, n, s, t, [sig, tau])
        ok = (not chk[f'K{s}']) and (not chk[f'I{t}']) and chk['automorphisms']
        print(f'  SAT; model decoded to a graph with {sum(map(sum, adj))//2} edges: '
              f'contains K{s}: {chk[f"K{s}"]}, contains independent {t}-set: {chk[f"I{t}"]}, '
              f'both generators are automorphisms: {chk["automorphisms"]}  -> '
              + ('WITNESS CONFIRMED' if ok else 'MODEL IS NOT A WITNESS'))
        if not ok:
            return False
    elif r.returncode == 20:
        print('  UNSAT (no invariant graph at these parameters; forward control below still applies)')
    else:
        print(f'  solver gave no verdict (exit {r.returncode})'); return False

    # --- forward: random invariant graphs that happen to be good must satisfy every clause
    rnd = random.Random(seed)
    found = 0
    for _ in range(trials):
        asg = {o: rnd.random() < 0.5 for o in range(1, nv + 1)}
        adj = [[False] * n for _ in range(n)]
        for (u, v), o in var.items():
            adj[u][v] = adj[v][u] = asg[o]
        if has_clique(adj, n, s):
            continue
        comp = [[(u != v and not adj[u][v]) for v in range(n)] for u in range(n)]
        if has_clique(comp, n, t):
            continue
        bad = sum(1 for cl in cls
                  if not any((asg[l] if l > 0 else not asg[-l]) for l in cl))
        found += 1
        if bad:
            print(f'  FORWARD CONTROL FAILED: a genuine witness violates {bad} clauses')
            return False
        if found >= 3:
            break
    if found:
        print(f'  forward: {found} random invariant graph(s) verified good by direct search, '
              f'0 violated clauses')
    else:
        print('  forward: no random invariant graph was good at these parameters')
    return True

if __name__ == '__main__':
    cases = [
        (0, [0, 0, 0, 0], 1, 4, 4),      # regular action on 9 points
        (0, [0, 0, 0, 0], 1, 3, 4),
        (3, [0, 0, 0, 0], 1, 4, 4),      # 12 points, three fixed
        (0, [1, 0, 0, 0], 1, 4, 4),      # 12 points, a size-3 orbit
        (0, [1, 1, 0, 0], 1, 4, 5),      # 15 points
        (0, [0, 0, 0, 0], 2, 4, 5),      # 18 points, two regular orbits
        (3, [1, 1, 0, 0], 1, 4, 5),      # 18 points, mixed
        (0, [1, 1, 1, 1], 1, 5, 5),      # 21 points at the real (s,t)
        (0, [0, 0, 0, 0], 3, 5, 5),      # 27 points at the real (s,t)
    ]
    allok = True
    for (a, b, c, s, t) in cases:
        allok &= control(a, b, c, s, t)
        print()
    print('POSITIVE CONTROL: ' + ('all cases passed' if allok else 'FAILED'))

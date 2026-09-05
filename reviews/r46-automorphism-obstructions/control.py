"""reviewer-1: positive control of encode.py. Take a catalog graph with |Aut|=2, its
involution sigma (cycle type 1^f 2^k), relabel so sigma is the encoder's canonical
permutation, and check that the graph's orbit assignment satisfies every clause of
encode.py's CNF for (35,4,6,f,2,k)."""
import subprocess, sys
import networkx as nx
from indep_catalog import g6
lines = open('r46_35some.g6').read().split('\n')
n, E = g6(lines[int(sys.argv[1])])
G = nx.Graph(E)
sig = next(m for m in nx.algorithms.isomorphism.GraphMatcher(G, G).isomorphisms_iter() if any(m[v] != v for v in m))
fixed = [v for v in range(n) if sig[v] == v]; f = len(fixed)
cyc = []; seen = set(fixed)
for v in range(n):
    if v not in seen: cyc.append((v, sig[v])); seen |= {v, sig[v]}
k = len(cyc); assert f + 2 * k == n
new = {v: i for i, v in enumerate(fixed)}
for j, (a, b) in enumerate(cyc): new[a] = f + 2 * j; new[b] = f + 2 * j + 1
adj = {(min(new[u], new[v]), max(new[u], new[v])) for u, v in E}
subprocess.run([sys.executable, 'target/encode.py', str(n), '4', '6', str(f), '2', str(k), 'tmp/ctrl.cnf'], check=True, capture_output=True)
# variable numbering: lexicographically least pair of each orbit, orbits in lex order (README)
def s2(x):
    if x < f: return x
    j, i = divmod(x - f, 2); return f + 2 * j + (i + 1) % 2
pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
canon = {}
for u, v in pairs:
    a, b = s2(u), s2(v); canon[(u, v)] = min((u, v), (min(a, b), max(a, b)))
order = {}
for pr in pairs:
    c = canon[pr]
    if c not in order: order[c] = len(order) + 1
val = {}
for pr in pairs:
    x = order[canon[pr]]; e = pr in adj
    assert val.get(x, e) == e, "graph is not sigma-invariant under the relabelling"
    val[x] = e
nv = None; ncl = 0; bad = 0
for line in open('tmp/ctrl.cnf'):
    if line[0] == 'c': continue
    if line[0] == 'p': nv = int(line.split()[2]); continue
    lits = [int(t) for t in line.split()][:-1]; ncl += 1
    if not any(val[abs(l)] == (l > 0) for l in lits): bad += 1
print(f"graph {sys.argv[1]}: cycle type 1^{f} 2^{k}, orbit vars {nv} (assignment covers {len(val)}), clauses {ncl}, violated by the catalog graph: {bad}")

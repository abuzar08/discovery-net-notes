"""reviewer-1: circulant (4,6,n)-graphs for n = 30..39 via the orbit CNF (f=0, p=n, k=1),
solved with python-sat Glucose4; a SAT answer is decoded and re-checked directly."""
import itertools, sys, time
from pysat.solvers import Glucose4
from indep_orbit_encode import build

def check(n, S):
    adj = [set() for _ in range(n)]
    for v in range(n):
        for s in S:
            adj[v].add((v+s) % n); adj[v].add((v-s) % n)
    K4 = any(all(b in adj[a] for a, b in itertools.combinations(Q, 2)) for Q in itertools.combinations(range(n), 4))
    I6 = any(all(b not in adj[a] for a, b in itertools.combinations(Q, 2)) for Q in itertools.combinations(range(n), 6))
    return (not K4) and (not I6)

for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    t = time.time()
    nv, C = build(n, 4, 6, 0, n, 1)
    s = Glucose4()
    for c in C: s.add_clause(list(c))
    r = s.solve()
    if r:
        m = set(x for x in s.get_model() if x > 0)
        S = [d for d in range(1, n//2 + 1) if d in m]   # orbit d is rooted at pair (0,d)
        print(f"n={n}: vars={nv} clauses={len(C)} SAT  S={S}  direct check (K4-free & no I6): {check(n, S)}  [{time.time()-t:.1f}s]", flush=True)
    else:
        print(f"n={n}: vars={nv} clauses={len(C)} UNSAT  (no circulant (4,6,{n})-graph)  [{time.time()-t:.1f}s]", flush=True)
    s.delete()

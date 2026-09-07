r"""reviewer-1: independent check of h2879's involution measurements.

My own encoder for the four n = 36 types, the p = 7 comparison range, and the
profile-constraint count; then a single refutation of 1^0 2^18 under the same
1500 s cap (symF is vacuous at f = 0 and symC is undefined at p = 2, so the
formula is the base orbit CNF).
"""
import itertools, os, subprocess, sys, time
from indep_syms import orbits

TOOLS = os.path.expanduser('~/.discovery-research-team/workspaces/reviewer-1/scratch/r46/tools')
CAD = os.path.join(TOOLS, 'cadical', 'build', 'cadical')

def build(f, p, k, s=4, t=6):
    n = f + p*k
    oid, norb = orbits(f, p, k)
    seen, out = set(), []
    for A in itertools.combinations(range(n), s):
        cl = tuple(sorted({-(oid[(u,v)]+1) for u,v in itertools.combinations(A,2)}))
        if cl not in seen: seen.add(cl); out.append(cl)
    for B in itertools.combinations(range(n), t):
        cl = tuple(sorted({oid[(u,v)]+1 for u,v in itertools.combinations(B,2)}))
        if cl not in seen: seen.add(cl); out.append(cl)
    return norb, out

if __name__ == '__main__':
    print('THE FOUR n = 36 TYPES (my own encoder)')
    for (f,k) in [(0,18),(2,17),(4,16),(6,15)]:
        norb, cls = build(f,2,k)
        print(f'   1^{f} 2^{k}: {norb} orbit variables, {len(cls)} clauses', flush=True)
    print()
    print('THE p = 7 TYPES ALREADY MEASURED INFEASIBLE, for scale')
    vals = []
    for n in range(36,40):
        for k in range(1, n//7+1):
            f = n - 7*k
            if f < 0: continue
            oid, norb = orbits(f,7,k)
            vals.append((norb, n, f, k))
    vals.sort()
    print(f'   {len(vals)} types 1^f 7^k across 36..39: orbit variables '
          f'{vals[0][0]} (n={vals[0][1]}, f={vals[0][2]}, k={vals[0][3]}) to '
          f'{vals[-1][0]} (n={vals[-1][1]}, f={vals[-1][2]}, k={vals[-1][3]})', flush=True)
    n36 = [v for v in vals if v[1]==36]
    print(f'   at n = 36: {[v[0] for v in n36]}', flush=True)
    print()
    print('THE PROFILE CONSTRAINT: how many of the 74 involution types it restricts')
    types = [(n, n-2*k, k) for n in range(36,40) for k in range(1, n//2+1)
             if n-2*k >= 0]
    print(f'   involution types: {len(types)}')
    for name, cond in [('f >= 1 (non-vacuous)', lambda n,f,k: f >= 1),
                       ('f >= 1 and f <= 20', lambda n,f,k: 1 <= f <= 20),
                       ('f >= 1 and f < 20', lambda n,f,k: 1 <= f < 20),
                       ('f >= 1 and lower bound positive (f < n-24)',
                        lambda n,f,k: f >= 1 and n-24-f > 0)]:
        print(f'   {name}: {sum(1 for n,f,k in types if cond(n,f,k))}', flush=True)
    print()
    print('SINGLE REFUTATION OF 1^0 2^18 AT THE 1500 s CAP', flush=True)
    norb, cls = build(0,2,18)
    path = 'invol_1_0_2_18.cnf'
    with open(path,'w') as fh:
        fh.write(f'p cnf {norb} {len(cls)}\n')
        for c in cls: fh.write(' '.join(map(str,c))+' 0\n')
    proof = 'invol.drat'
    t0=time.time()
    r = subprocess.run([CAD,'-q','-t','1500',path,proof], capture_output=True, text=True)
    el=time.time()-t0
    v = ('UNSAT' if 's UNSATISFIABLE' in r.stdout else
         'SAT' if 's SATISFIABLE' in r.stdout else 'NO VERDICT')
    sz = os.path.getsize(proof)/1e6 if os.path.exists(proof) else 0
    print(f'   {v} after {el:.0f}s; DRAT {sz:.0f} MB (the contribution reports '
          f'no verdict and 2837 MB)', flush=True)
    for p_ in (path, proof):
        if os.path.exists(p_): os.unlink(p_)

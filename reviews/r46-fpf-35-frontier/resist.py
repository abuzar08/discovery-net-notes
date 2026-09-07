r"""reviewer-1: do the two fixed-point-free (4,6,35) instances resist a single
refutation attempt at 1500 s, as h3044 reports?

The configuration is the one the contribution used: symF is vacuous at f = 0, so
the formula is the base orbit CNF plus symC only.  Both formula and breaking
clauses are my own, auxiliary-free.  Also counts the clauses of the n = 36
involution formula 1^0 2^18, which the body puts at about 1.0e6.
"""
import itertools, os, subprocess, sys, time
from indep_syms import orbits

TOOLS = os.path.expanduser('~/.discovery-research-team/workspaces/reviewer-1/scratch/r46/tools')
CAD = os.path.join(TOOLS, 'cadical', 'build', 'cadical')

def base(f, p, k, s=4, t=6):
    n = f + p*k
    oid, norb = orbits(f, p, k)
    seen, out = set(), []
    for A in itertools.combinations(range(n), s):
        cl = tuple(sorted({-(oid[(u,v)]+1) for u,v in itertools.combinations(A,2)}))
        if cl not in seen: seen.add(cl); out.append(cl)
    for B in itertools.combinations(range(n), t):
        cl = tuple(sorted({oid[(u,v)]+1 for u,v in itertools.combinations(B,2)}))
        if cl not in seen: seen.add(cl); out.append(cl)
    return oid, norb, out

def symc(oid, f, p, k):
    half = (p-1)//2
    out = []
    for j in range(k-1):
        a, b = f + j*p, f + (j+1)*p
        ra = [oid[(a, a+d)]+1 for d in range(1, half+1)]
        rb = [oid[(b, b+d)]+1 for d in range(1, half+1)]
        for wa in itertools.product((0,1), repeat=half):
            for wb in itertools.product((0,1), repeat=half):
                if list(wa) <= list(wb): continue
                lits = [(-ra[i] if wa[i] else ra[i]) for i in range(half)]
                lits += [(-rb[i] if wb[i] else rb[i]) for i in range(half)]
                out.append(tuple(sorted(set(lits))))
    return out

if __name__ == '__main__':
    for (f,p,k) in [(0,7,5),(0,5,7)]:
        t0=time.time()
        oid, norb, cls = base(f,p,k)
        sc = symc(oid,f,p,k)
        path=f'resist_{p}_{k}.cnf'
        with open(path,'w') as fh:
            fh.write(f'p cnf {norb} {len(cls)+len(sc)}\n')
            for c in cls+sc: fh.write(' '.join(map(str,c))+' 0\n')
        print(f'1^{f} {p}^{k}: {norb} vars, {len(cls)} base + {len(sc)} symC '
              f'clauses, built in {time.time()-t0:.0f}s', flush=True)
        t0=time.time()
        r = subprocess.run([CAD,'-q','-t','1500',path], capture_output=True, text=True)
        el=time.time()-t0
        v = ('UNSAT' if 's UNSATISFIABLE' in r.stdout else
             'SAT' if 's SATISFIABLE' in r.stdout else 'NO VERDICT')
        print(f'   single refutation, 1500 s cap: {v} after {el:.0f}s', flush=True)
        os.unlink(path)
    # the n = 36 involution formula size
    t0=time.time()
    oid, norb, cls = base(0,2,18)
    print(f'1^0 2^18 at n = 36: {norb} orbit variables, {len(cls)} clauses '
          f'(built in {time.time()-t0:.0f}s)', flush=True)

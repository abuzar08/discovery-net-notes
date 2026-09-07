r"""reviewer-1: independent check of h3044 (researcher-3), the two fixed-point-free
(4,6,35) instances and the lane frontier.

My own orbit numbering and my own clause construction (no lane code) for:
  * the two instances' variable and clause counts;
  * the cross-cycle / internal decomposition of the orbit variables;
  * the 74 involution types across 36 <= n <= 39 and their variable range.
"""
import itertools
from indep_syms import orbits, kind

def formula(f, p, k, s=4, t=6):
    n = f + p*k
    oid, norb = orbits(f, p, k)
    seen, cnt = set(), 0
    for A in itertools.combinations(range(n), s):
        cl = tuple(sorted({-(oid[(u,v)]+1) for u,v in itertools.combinations(A,2)}))
        if cl not in seen: seen.add(cl); cnt += 1
    for B in itertools.combinations(range(n), t):
        cl = tuple(sorted({oid[(u,v)]+1 for u,v in itertools.combinations(B,2)}))
        if cl not in seen: seen.add(cl); cnt += 1
    reps = {}
    for pr, o in oid.items():
        if o not in reps or pr < reps[o]: reps[o] = pr
    kinds = {}
    for o in range(norb):
        kinds[kind(f,p,k,reps[o])[0]] = kinds.get(kind(f,p,k,reps[o])[0], 0) + 1
    return norb, cnt, kinds

print('THE TWO INSTANCES (my own encoder)')
for (f,p,k) in [(0,5,7),(0,7,5)]:
    norb, ncl, kinds = formula(f,p,k)
    cross = (k*(k-1)//2)*p
    internal = k*(p-1)//2
    print(f'  1^{f} {p}^{k}: {norb} orbit variables, {ncl} clauses; '
          f'by kind {kinds}; cross C(k,2)p = {cross}, internal k(p-1)/2 = '
          f'{internal}, sum {cross+internal}; cross share '
          f'{100*cross/norb:.1f}%')
print()
print('THE INVOLUTION FRONTIER, 36 <= n <= 39')
types = []
for n in range(36,40):
    for k in range(1, n//2+1):
        f = n - 2*k
        if f < 0: continue
        types.append((n,f,k))
print(f'  {len(types)} types 1^f 2^k in total')
sizes = []
for (n,f,k) in types:
    oid, norb = orbits(f,2,k)
    sizes.append((norb,n,f,k))
sizes.sort()
print(f'  orbit variables range from {sizes[0][0]} (n={sizes[0][1]}, '
      f'1^{sizes[0][2]} 2^{sizes[0][3]}) to {sizes[-1][0]} (n={sizes[-1][1]}, '
      f'1^{sizes[-1][2]} 2^{sizes[-1][3]})')
n36 = [s for s in sizes if s[1]==36]
print(f'  at n = 36: {len(n36)} types, variables {n36[0][0]}..{n36[-1][0]}')

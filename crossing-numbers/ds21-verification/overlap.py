"""Do DS21's multipartite formulas agree wherever their domains overlap?

Several families denote the same graph at different parameters: K_{1,3,4} is
K_{1,4,3}, and both are K_{1,m,n} with (m,n) = (3,4).  Since a complete
multipartite graph is determined by the MULTISET of its part sizes, any two
formulas whose domains meet must agree there.  This is a pure internal
consistency test -- no crossing number is computed and no drawing is needed, so
it cannot be fooled by heuristic weakness, and it is exhaustive over the range.
"""
from collections import defaultdict
from fractions import Fraction

def X(n): return (n//2)*((n-1)//2)
def Z(m,n): return X(m)*X(n)

# (name, parts-as-multiset given the free parameter(s), formula)
FAM = [
 ("K_{1,3,n}",      lambda n: (1,3,n),      lambda n: Z(4,n) + n//2),
 ("K_{2,3,n}",      lambda n: (2,3,n),      lambda n: Z(5,n) + n),
 ("K_{1,4,n}",      lambda n: (1,4,n),      lambda n: n*(n-1)),
 ("K_{2,4,n}",      lambda n: (2,4,n),      lambda n: Z(6,n) + 2*n),
 ("K_{1,1,3,n}",    lambda n: (1,1,3,n),    lambda n: Z(5,n) + (3*n)//2),
 ("K_{1,1,4,n}",    lambda n: (1,1,4,n),    lambda n: Z(6,n) + 2*n + 2*(n//2)),
 ("K_{1,2,2,n}",    lambda n: (1,2,2,n),    lambda n: Z(5,n) + (3*n)//2),
 ("K_{2,2,2,n}",    lambda n: (2,2,2,n),    lambda n: Z(6,n) + 3*n),
 ("K_{1,1,1,n}",    lambda n: (1,1,1,n),    lambda n: X(n)),
 ("K_{1,1,1,1,n}",  lambda n: (1,1,1,1,n),  lambda n: Z(4,n) + n),
 ("K_{1,1,1,2,n}",  lambda n: (1,1,1,2,n),  lambda n: Z(5,n) + 2*n),
 # conditional on Zarankiewicz
 ("K_{3,3,n} [cond]", lambda n: (3,3,n),    lambda n: Z(6,n) + 2*n + 2*(n//2) + 1),
]

pred = defaultdict(list)
for name, parts, f in FAM:
    for n in range(1, 15):
        key = tuple(sorted(parts(n)))
        pred[key].append((f"{name} at n={n}", f(n)))

# K_{1,m,n} = Z(m+1,n+1) - floor(m/2)floor(n/2), conditional on Zarankiewicz
for m in range(1, 12):
    for n in range(m, 12):
        key = tuple(sorted((1, m, n)))
        pred[key].append((f"K_(1,{m},{n}) [cond]", Z(m+1,n+1) - (m//2)*(n//2)))
# K_{m,n} = Z(m,n), conjectured
for m in range(1, 14):
    for n in range(m, 14):
        pred[tuple(sorted((m,n)))].append((f"K_({m},{n}) [conj]", Z(m,n)))

overlaps = {k: v for k, v in pred.items() if len({x[1] for x in v}) >= 1 and len(v) > 1}
bad = []
for k, v in sorted(overlaps.items()):
    vals = {x[1] for x in v}
    if len(vals) > 1:
        bad.append((k, v))
print(f"multisets with two or more formulas applying: {len(overlaps)}")
print(f"disagreements: {len(bad)}\n")
for k, v in bad:
    print("MISMATCH", k)
    for nm, val in v:
        print(f"    {nm:>28} -> {val}")
    print()
if not bad:
    print("every overlapping pair agrees")
# show a sample of the agreements actually exercised
print("\nsample of exercised overlaps:")
shown = 0
for k, v in sorted(overlaps.items()):
    if len(v) >= 2 and shown < 12:
        print(f"  K_{k} = {v[0][1]:>5}   via {', '.join(nm for nm,_ in v)}")
        shown += 1

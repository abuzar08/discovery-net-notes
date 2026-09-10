"""Upper bounds for sk(GP(28,7)), the other case DS21 records as open.

The LOWER bound is out of range and this is recorded rather than attempted:
ruling out r <= 8 needs 48,563,893,286 planarity tests, about 8,296 core-hours
at the measured rate -- four times the M_(8,3) figure declined earlier in this
campaign.  So k = 7 cannot be SETTLED here; only upper bounds are reachable.

The structured shape that produced every witness so far -- one outer edge plus
spokes -- gives sk <= 11 in a single test.  This searches the same shape for
fewer spokes, to see whether DS21's conjectured 9 is achievable within it.

A failure here is NOT evidence against 9: it would only show that 9 is not
achievable by deleting one outer edge and spokes, which is one shape among many.
"""
import sys, itertools, time
sys.path.insert(0, '/Users/abuzark/.discovery-research-team/workspaces/researcher-4/scratch')
from gp import GP, planar

G = GP(28, 7)
outer = (('u', 0), ('u', 1))
print(f"GP(28,7): |V|={G.number_of_nodes()} |E|={G.number_of_edges()}", flush=True)
print("DS21 conjectures k+2 = 9; the structured pattern gives 11\n", flush=True)
t0 = time.time()
for s in range(5, 11):
    n = 0
    hit = None
    for spokes in itertools.combinations(range(28), s):
        H = G.copy()
        H.remove_edge(*outer)
        H.remove_edges_from([(('u', i), ('v', i)) for i in spokes])
        n += 1
        if planar(H):
            hit = spokes
            break
    tot = 1 + s
    if hit:
        print(f"  {s} spokes ({tot} edges): FOUND {hit}   ({time.time()-t0:.0f}s)", flush=True)
        print(f"\nsk(GP(28,7)) <= {tot}", flush=True)
        break
    print(f"  {s} spokes ({tot} edges): none of {n:,} sets   ({time.time()-t0:.0f}s)", flush=True)

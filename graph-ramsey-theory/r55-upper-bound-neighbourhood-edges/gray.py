"""Does the gray-edge cover idea help MY pair enumeration?

principal-1's inference: beta(24) <= 125 is a question about 15913 named
(4,5,24)-graphs at ~26 minutes each, so a cover of partially-specified graphs
over those 15913 would keep local sharpness while collapsing the count -- the
structure my pincer diagnosis said was missing.

The measurement.  A generalization is a graph with some edges GRAY, i.e. left
undetermined; refuting it refutes every graph it covers at once.  In the CNF
that means the gray edges of H become variables instead of constants.  So a
gray instance is the concrete instance plus extra free variables, and the
question is purely empirical: does grouping pay for the added freedom?

Note on soundness of the coarsening.  Graying an edge may admit graphs that
are not (4,5,24)-graphs at all, or that have fewer than 126 edges.  For the
present purpose that is harmless: refuting a LARGER set is a stronger
statement than refuting the intended one, so any cover is sound here, and
Gauthier-Brown's "exact cover" requirement is not needed.

    python3 gray.py H.g6 K [TIMEOUT]     # K = number of edges greyed
"""
import itertools as it
import subprocess
import sys
import time

import r45bounds as R

CAD = ("/Users/abuzark/.discovery-research-team/workspaces/researcher-3/"
       "scratch/tools/cadical/build/cadical")


def build(H_adj, d, m, gray, n=45):
    """n=45, degree-d vertex v.  H's gray edges become variables.

    Variables: bipartite x(i,j) [d*m], M-internal y(a,b) [C(m,2)],
    then one variable per gray pair of H.
    """
    def xv(i, j):
        return i * m + j + 1

    ypos, p = {}, d * m + 1
    for a, b in it.combinations(range(m), 2):
        ypos[(a, b)] = p
        p += 1

    def yv(a, b):
        return ypos[(a, b)] if a < b else ypos[(b, a)]

    gpos = {}
    for a, b in gray:
        gpos[(a, b)] = p
        p += 1

    def hlit(a, b):
        """None-or-literal: returns 1/0 if fixed, or a variable if gray."""
        k = (a, b) if a < b else (b, a)
        if k in gpos:
            return gpos[k]
        return 1 if (H_adj[a] >> b) & 1 else 0

    cls = []
    # alpha(M) <= 3
    for S in it.combinations(range(m), 4):
        cls.append(tuple(sorted(yv(a, b) for a, b in it.combinations(S, 2))))
    for S in it.combinations(range(d + m), 5):
        Ns = [x for x in S if x < d]
        Ms = [x - d for x in S if x >= d]
        hp = [hlit(a, b) for a, b in it.combinations(Ns, 2)]
        # clique clause: forbid all pairs being edges
        if not any(h == 0 for h in hp):
            lits = [-h for h in hp if h != 1]
            lits += [-yv(a, b) for a, b in it.combinations(Ms, 2)]
            lits += [-xv(a, b) for a in Ns for b in Ms]
            cls.append(tuple(sorted(set(lits))))
        # independent clause: forbid all pairs being non-edges
        if not any(h == 1 for h in hp):
            lits = [h for h in hp if h != 0]
            lits += [yv(a, b) for a, b in it.combinations(Ms, 2)]
            lits += [xv(a, b) for a in Ns for b in Ms]
            cls.append(tuple(sorted(set(lits))))
    return p - 1, cls


def main():
    line = open(sys.argv[1]).readline()
    K = int(sys.argv[2])
    timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 1800
    d, H = R.g6_decode(line)
    assert d == 24 and R.is_good(24, H, 4, 5)
    m = 44 - d
    edges = [(a, b) for a, b in it.combinations(range(d), 2) if (H[a] >> b) & 1]
    gray = edges[:K]                       # gray the first K edges of H
    nvar, cls = build(H, d, m, gray)
    with open("g.cnf", "w") as fh:
        fh.write(f"p cnf {nvar} {len(cls)}\n")
        for c in cls:
            fh.write(" ".join(map(str, c)) + " 0\n")
    t = time.time()
    r = subprocess.run(["timeout", str(timeout), CAD, "-q", "g.cnf"],
                       capture_output=True)
    el = time.time() - t
    res = {10: "SAT", 20: "UNSAT", 124: "no verdict"}.get(r.returncode,
                                                          f"rc={r.returncode}")
    print(f"  gray={K:3d}  covers 2^{K} = {2**K:>10} graphs  "
          f"vars {nvar}  clauses {len(cls)}  ->  {res} in {el:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())

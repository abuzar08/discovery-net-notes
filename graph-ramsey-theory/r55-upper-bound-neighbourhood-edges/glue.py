"""Cost the neighbourhood-gluing instance for a (5,5,n)-graph.

Fix a vertex v of degree d in a hypothetical (5,5,n)-graph.  Then
V = {v} + N + M with |N| = d, |M| = m = n-1-d, and

    G[N] = H            a (4,5,d)-graph, taken from McKay's catalogue
    G[M] = complement of H'   with H' a (4,5,m)-graph, likewise

are FIXED.  The only unknowns are the d*m edges between N and M.  So the
gluing question "do H and H' glue to a (5,5,n)-graph with v of degree d?" is a
SAT instance with exactly d*m variables and no symmetry assumption anywhere --
which is what makes this line independent of the automorphism programme.

Two families of constraint disappear for free:

  * a K_5 through v needs a K_4 inside N, impossible since H is K_4-free;
  * an independent 5-set through v needs an independent 4-set inside M,
    impossible since G[M] is a (5,4)-graph.

So every clause lives on a 5-subset of N + M, and a 5-subset whose fixed part
already contains a non-edge (for cliques) or an edge (for independent sets) is
satisfied outright and is not emitted.

    python3 glue.py H.g6 HPRIME.g6 OUT.cnf [--limit N]
"""
import itertools
import sys

sys.path.insert(0, ".")
import r45bounds as R


def build(H_adj, d, Hp_adj, m):
    """Return (nvar, clauses).  Variable x(i,j), i in N, j in M, is 1-based."""
    def var(i, j):
        return i * m + j + 1

    # G[M] is the COMPLEMENT of the (4,5,m)-graph H'
    Madj = [(~Hp_adj[j]) & ((1 << m) - 1) & ~(1 << j) for j in range(m)]

    def nadj(a, b):                     # adjacency inside N
        return (H_adj[a] >> b) & 1

    def madj(a, b):                     # adjacency inside M
        return (Madj[a] >> b) & 1

    cls = []
    verts = [("N", i) for i in range(d)] + [("M", j) for j in range(m)]
    for S in itertools.combinations(range(d + m), 5):
        Ns = [x for x in S if x < d]
        Ms = [x - d for x in S if x >= d]
        # ---- clique clause: forbid all ten pairs being edges
        lits = []
        dead = False
        for a, b in itertools.combinations(Ns, 2):
            if not nadj(a, b):
                dead = True
                break
        if not dead:
            for a, b in itertools.combinations(Ms, 2):
                if not madj(a, b):
                    dead = True
                    break
        if not dead:
            for a in Ns:
                for b in Ms:
                    lits.append(-var(a, b))
            cls.append(tuple(sorted(set(lits))) if lits else ())
        # ---- independent-set clause: forbid all ten pairs being non-edges
        lits = []
        dead = False
        for a, b in itertools.combinations(Ns, 2):
            if nadj(a, b):
                dead = True
                break
        if not dead:
            for a, b in itertools.combinations(Ms, 2):
                if madj(a, b):
                    dead = True
                    break
        if not dead:
            for a in Ns:
                for b in Ms:
                    lits.append(var(a, b))
            cls.append(tuple(sorted(set(lits))) if lits else ())
    return d * m, cls


def main():
    hs = open(sys.argv[1]).readline()
    hps = open(sys.argv[2]).readline()
    d, Hadj = R.g6_decode(hs)
    m, Hpadj = R.g6_decode(hps)
    nvar, cls = build(Hadj, d, Hpadj, m)
    empty = [c for c in cls if not c]
    print(f"d={d} m={m}  e(H)={R.edges(d,Hadj)}  e(H')={R.edges(m,Hpadj)}")
    print(f"  variables {nvar}   clauses {len(cls)}   empty clauses {len(empty)}")
    if empty:
        print("  -> UNSAT at generation: some 5-set is already forced")
        return 0
    with open(sys.argv[3], "w") as fh:
        fh.write(f"p cnf {nvar} {len(cls)}\n")
        for c in cls:
            fh.write(" ".join(map(str, c)) + " 0\n")
    print(f"  wrote {sys.argv[3]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())


def build_open_M(H_adj, d, m):
    """Fix only H = G[N(v)]; leave G[M] AND the bipartite part unknown.

    Variables: x(i,j) for i in N, j in M (bipartite), then y(a,b) for a<b in M
    (inside M).  This is the unconditional question "can H be the neighbourhood
    of a degree-d vertex in a (5,5,n)-graph?" with no symmetry assumed and no
    catalogue needed for M.

    A K_5 through v still needs a K_4 in N, impossible since H is K_4-free.  An
    independent 5-set through v now needs an independent 4-set in M, which is
    NO LONGER automatic because G[M] is unknown, so those clauses are added
    explicitly.
    """
    import itertools as it
    nb = d * m

    def xv(i, j):
        return i * m + j + 1

    ypos = {}
    nxt = nb + 1
    for a, b in it.combinations(range(m), 2):
        ypos[(a, b)] = nxt
        nxt += 1

    def yv(a, b):
        return ypos[(a, b)] if a < b else ypos[(b, a)]

    def nadj(a, b):
        return (H_adj[a] >> b) & 1

    cls = []
    # alpha(M) <= 3 : no independent 4-set in M (with v that would be an
    # independent 5-set of G)
    for S in it.combinations(range(m), 4):
        cls.append(tuple(sorted(yv(a, b) for a, b in it.combinations(S, 2))))
    # 5-subsets of N + M
    for S in it.combinations(range(d + m), 5):
        Ns = [x for x in S if x < d]
        Ms = [x - d for x in S if x >= d]
        dead = any(not nadj(a, b) for a, b in it.combinations(Ns, 2))
        if not dead:
            lits = [-yv(a, b) for a, b in it.combinations(Ms, 2)]
            lits += [-xv(a, b) for a in Ns for b in Ms]
            cls.append(tuple(sorted(set(lits))))
        dead = any(nadj(a, b) for a, b in it.combinations(Ns, 2))
        if not dead:
            lits = [yv(a, b) for a, b in it.combinations(Ms, 2)]
            lits += [xv(a, b) for a in Ns for b in Ms]
            cls.append(tuple(sorted(set(lits))))
    return nxt - 1, cls


def symM_clauses(d, m, first_aux):
    """Break the S_m relabelling symmetry of M by sorting its bipartite columns.

    SOUNDNESS.  The vertices of M carry no labels: any permutation tau of M
    gives an isomorphic completion, and it acts on the variables by permuting
    the bipartite columns col(j) = (x(0,j), ..., x(d-1,j)) and carrying M's
    internal adjacency along with them.  Sorting by the columns is therefore
    sorting by an invariant that the permutation merely relabels, so every
    assignment has a relabelling with

        col(0) >=_lex col(1) >=_lex ... >=_lex col(m-1),

    and imposing it removes no completion up to isomorphism.  (This is the same
    argument as `symC` in the R(4,6) lane, and it needs no care about induced
    signs precisely because nothing is imposed on M's internal variables.)

    Returns (clauses, n_aux).
    """
    import itertools as it

    def xv(i, j):
        return i * m + j + 1

    cls = []
    aux = first_aux
    for j in range(m - 1):
        ra = [xv(i, j + 1) for i in range(d)]      # want col(j+1) <=_lex col(j)
        rb = [xv(i, j) for i in range(d)]
        prev = None
        for t, (a, b) in enumerate(zip(ra, rb)):
            cls.append(tuple(sorted((-a, b))) if prev is None
                       else tuple(sorted((-prev, -a, b))))
            if t == len(ra) - 1:
                break
            aux += 1
            e = aux
            if prev is None:
                for c in ((-e, a, -b), (-e, -a, b), (e, a, b), (e, -a, -b)):
                    cls.append(tuple(sorted(c)))
            else:
                for c in ((-e, prev), (-e, a, -b), (-e, -a, b),
                          (e, -prev, a, b), (e, -prev, -a, -b)):
                    cls.append(tuple(sorted(c)))
            prev = e
    return cls, aux - first_aux

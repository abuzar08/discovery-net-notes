"""reviewer-1: independent re-run of the target's circulant observations.

usage: python indep_circ.py Q K NMIN NMAX
For every n in [NMIN, NMAX] and every S subset of {1..floor(n/2)}, test whether
C_n(S) is K_Q-free with chi >= K (own clique test, colourability via pysat).
Reports per n the number of such circulants and the lexicographically smallest S.
"""
import itertools, sys, time
from pysat.solvers import Glucose4


def circ(n, S):
    A = [0] * n
    for v in range(n):
        for s in S:
            A[v] |= 1 << ((v + s) % n)
            A[v] |= 1 << ((v - s) % n)
    return A


def has_clique(n, A, q):
    # vertex-transitive: it suffices to look for cliques containing vertex 0
    def rec(cands, size):
        if size == q:
            return True
        while cands:
            v = (cands & -cands).bit_length() - 1
            cands &= cands - 1
            if rec(cands & A[v], size + 1):
                return True
        return False
    return rec(A[0], 1)


def colourable(n, A, c):
    var = lambda v, i: v * c + i + 1
    s = Glucose4()
    for v in range(n):
        s.add_clause([var(v, i) for i in range(c)])
        m = A[v]
        while m:
            w = (m & -m).bit_length() - 1
            m &= m - 1
            if w > v:
                for i in range(c):
                    s.add_clause([-var(v, i), -var(w, i)])
    s.add_clause([var(0, 0)])
    r = s.solve()
    s.delete()
    return r


if __name__ == '__main__':
    q, k, nmin, nmax = map(int, sys.argv[1:5])
    for n in range(nmin, nmax + 1):
        t = time.time()
        h = n // 2
        found = []
        nfree = 0
        for r in range(1, h + 1):
            for S in itertools.combinations(range(1, h + 1), r):
                A = circ(n, S)
                if has_clique(n, A, q):
                    continue
                nfree += 1
                if not colourable(n, A, k - 1):
                    found.append(S)
        print(f"n={n:2d}: K{q}-free circulants={nfree:6d}  with chi>={k}: {len(found):4d}"
              + (f"  smallest S={found[0]} (|E|={n*len(found[0]) - (n//2 if n%2==0 and h in found[0] else 0)})"
                 if found else "") + f"  [{time.time()-t:.0f}s]", flush=True)

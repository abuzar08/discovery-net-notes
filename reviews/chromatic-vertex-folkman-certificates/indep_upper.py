"""reviewer-1: independent check of the upper-bound witnesses.

For each witness file (first line n, then one edge per line) and its (k, q):
  * K_q-free: every q-subset misses an edge (own bitset check)
  * chi >= k: no proper (k-1)-colouring, by own DSATUR backtracking
    and, independently, by a SAT encoding solved with python-sat (Glucose4)
  * chi <= k: an explicit k-colouring is found (reported, not needed for the bound)
Nothing from the target's code is imported.
"""
import itertools, sys, time


def load(path):
    L = [l.split() for l in open(path) if l.strip() and not l.startswith('#')]
    n = int(L[0][0])
    E = [(int(a), int(b)) for a, b in L[1:]]
    return n, E


def adj_masks(n, E):
    A = [0] * n
    for u, v in E:
        assert u != v and 0 <= u < n and 0 <= v < n
        A[u] |= 1 << v
        A[v] |= 1 << u
    return A


def has_clique(n, A, q):
    # enumerate cliques by extension; bounded by q
    def rec(cands, size):
        if size == q:
            return True
        while cands:
            v = (cands & -cands).bit_length() - 1
            cands &= cands - 1
            if rec(cands & A[v], size + 1):
                return True
        return False
    return rec((1 << n) - 1, 0)


def colourable(n, A, c, limit=None):
    """Own exact test: is there a proper c-colouring? DSATUR order, first-fit
    symmetry breaking on new colours."""
    col = [-1] * n
    used_max = [-1]

    def rec(assigned):
        if assigned == n:
            return True
        # pick uncoloured vertex with max saturation, tie-break by degree
        best, bsat, bdeg = -1, -1, -1
        for v in range(n):
            if col[v] < 0:
                sat = len({col[w] for w in bits(A[v]) if col[w] >= 0})
                deg = bin(A[v]).count('1')
                if sat > bsat or (sat == bsat and deg > bdeg):
                    best, bsat, bdeg = v, sat, deg
        v = best
        forbidden = {col[w] for w in bits(A[v]) if col[w] >= 0}
        top = min(c - 1, used_max[0] + 1)
        for colour in range(top + 1):
            if colour in forbidden:
                continue
            old = used_max[0]
            col[v] = colour
            used_max[0] = max(old, colour)
            if rec(assigned + 1):
                return True
            col[v] = -1
            used_max[0] = old
        return False
    return rec(0), col


def bits(m):
    while m:
        b = m & -m
        yield b.bit_length() - 1
        m ^= b


def sat_colourable(n, E, c):
    from pysat.solvers import Glucose4
    var = lambda v, i: v * c + i + 1
    s = Glucose4()
    for v in range(n):
        s.add_clause([var(v, i) for i in range(c)])
    for u, v in E:
        for i in range(c):
            s.add_clause([-var(u, i), -var(v, i)])
    s.add_clause([var(0, 0)])  # symmetry: vertex 0 gets colour 0
    r = s.solve()
    s.delete()
    return r


def check(path, k, q):
    n, E = load(path)
    A = adj_masks(n, E)
    assert len(set(tuple(sorted(e)) for e in E)) == len(E), "repeated edge"
    t = time.time()
    kq = has_clique(n, A, q)
    t1 = time.time() - t
    t = time.time()
    ok_km1, _ = colourable(n, A, k - 1)
    t2 = time.time() - t
    t = time.time()
    sat_km1 = sat_colourable(n, E, k - 1)
    t3 = time.time() - t
    ok_k, col = colourable(n, A, k)
    if ok_k:
        assert all(col[u] != col[v] for u, v in E)
    print(f"{path.split('/')[-1]:26s} n={n:2d} m={len(E):3d} (k,q)=({k},{q}): "
          f"K{q}-free={not kq} [{t1:.1f}s]  "
          f"({k-1})-colourable own={ok_km1} [{t2:.1f}s] sat={sat_km1} [{t3:.1f}s]  "
          f"{k}-colourable={ok_k}  =>  chi>={k}: {not kq and not ok_km1 and not sat_km1}")
    return (not kq) and (not ok_km1) and (not sat_km1)


if __name__ == "__main__":
    import re
    allok = True
    for path in sys.argv[1:]:
        m = re.search(r'n(\d+)[a-z]*_k(\d+)_q(\d+)', path)
        k, q = int(m.group(2)), int(m.group(3))
        allok &= check(path, k, q)
    print("ALL WITNESSES CONFIRMED" if allok else "SOME WITNESS FAILED")

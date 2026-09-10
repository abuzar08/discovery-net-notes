r"""reviewer-1: my own positive control for the arbitrary-cycle-type orbit
encoding, written to check researcher-3's `cyctype_control.py` claims.

The control: take a graph that really is an \((s,t,n)\)-graph and really has an
automorphism \(\sigma\) of some cycle type; build the orbit encoding for that
cycle type from scratch; read the graph's own edge relation as an assignment to
the pair-orbit variables; and check that every clause is satisfied. A formula
that has lost solutions fails this test, which no amount of negative controlling
can detect.
"""
import itertools
import sys
from collections import Counter

sys.path.insert(0, '../r45')
from indep_r45 import graph6, edges, has_clique, has_independent


def cycle_type(p):
    n = len(p)
    seen = [False] * n
    c = Counter()
    for v in range(n):
        if seen[v]:
            continue
        L, u = 0, v
        while not seen[u]:
            seen[u] = True
            u = p[u]
            L += 1
        c[L] += 1
    return dict(sorted(c.items()))


def perm_order(p):
    from math import lcm
    o = 1
    for L in cycle_type(p):
        o = lcm(o, L)
    return o


def is_automorphism(adj, p):
    n = len(adj)
    for u in range(n):
        for v in range(u + 1, n):
            if ((adj[u] >> v) & 1) != ((adj[p[u]] >> p[v]) & 1):
                return False
    return True


def pair_orbits(p):
    n = len(p)
    orb, nxt = {}, 0
    for u in range(n):
        for v in range(u + 1, n):
            if (u, v) in orb:
                continue
            a, b = u, v
            while True:
                e = (min(a, b), max(a, b))
                if e in orb:
                    break
                orb[e] = nxt
                a, b = p[a], p[b]
            nxt += 1
    return orb, nxt


def control(adj, p, s, t):
    """build the encoding for p's cycle type and test the graph's own assignment"""
    n = len(adj)
    assert is_automorphism(adj, p), 'not an automorphism'
    orb, north = pair_orbits(p)
    val = {}
    for (u, v), o in orb.items():
        bit = (adj[u] >> v) & 1
        if o in val and val[o] != bit:
            return dict(error='pair orbit not constant — adjacency not preserved')
        val[o] = bit
    msets = set()
    viol = 0
    for k, want in ((s, 1), (t, 0)):
        for S in itertools.combinations(range(n), k):
            os_ = frozenset(orb[(a, b)] for a, b in itertools.combinations(S, 2))
            msets.add((k, os_))
            if want == 1:                      # no clique of order s
                if all(val[o] == 1 for o in os_):
                    viol += 1
            else:                              # no independent set of order t
                if all(val[o] == 0 for o in os_):
                    viol += 1
    return dict(orbits=north, distinct_clause_supports=len(msets),
                clauses=len(msets), violated=viol)


def find_involution(adj, fixed_point_free=True, node_cap=2_000_000):
    """my own backtracking search for an automorphism with sigma^2 = id"""
    n = len(adj)
    deg = [bin(a).count('1') for a in adj]
    prof = [tuple(sorted(deg[u] for u in range(n) if (adj[v] >> u) & 1))
            for v in range(n)]
    img = [-1] * n
    nodes = [0]

    def consistent(v, w):
        for a in range(n):
            if img[a] == -1 or a == v or a == w:
                continue
            for b in (v, w):
                if img[b] == -1:
                    continue
                if ((adj[a] >> b) & 1) != ((adj[img[a]] >> img[b]) & 1):
                    return False
        return True

    def bt():
        nodes[0] += 1
        if nodes[0] > node_cap:
            raise TimeoutError
        try:
            v = next(i for i in range(n) if img[i] == -1)
        except StopIteration:
            return tuple(img)
        for w in range(n):
            if img[w] != -1 or (fixed_point_free and w == v):
                continue
            if deg[w] != deg[v] or prof[w] != prof[v]:
                continue
            img[v], img[w] = w, v
            if consistent(v, w):
                r = bt()
                if r:
                    return r
            img[v], img[w] = -1, -1
        return None
    try:
        return bt(), nodes[0]
    except TimeoutError:
        return None, nodes[0]


def automorphisms(adj):
    """all automorphisms, by backtracking (used at n = 24)"""
    n = len(adj)
    deg = [bin(a).count('1') for a in adj]
    lam = [[bin(adj[i] & adj[j]).count('1') for j in range(n)] for i in range(n)]
    out, img, used = [], [-1] * n, [False] * n

    def bt(v):
        if v == n:
            out.append(tuple(img))
            return
        for w in range(n):
            if used[w] or deg[w] != deg[v]:
                continue
            if all(((adj[v] >> u) & 1) == ((adj[w] >> img[u]) & 1)
                   and lam[v][u] == lam[w][img[u]] for u in range(v)):
                img[v], used[w] = w, True
                bt(v + 1)
                img[v], used[w] = -1, False
    bt(0)
    return out

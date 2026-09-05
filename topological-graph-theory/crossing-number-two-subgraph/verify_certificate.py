"""Standard-library-only checker for certificate.json.

Verifies, from first principles, that G = C3 [] C3 satisfies
    cr(G) = 3   and   cr(G - e) <= 1 for every edge e,
hence that G is 2-crossing-critical, every proper subgraph of G has crossing
number at most 1, and G therefore has no subgraph of crossing number exactly 2.

Positive (planarity) claims are certified by rotation systems checked with
Euler's formula.  Negative (non-planarity) claims are certified by explicit
Kuratowski subdivisions.  Nothing here trusts networkx, nauty, or the
generator.

    python3 verify_certificate.py certificate.json
"""
import itertools
import json
import sys

N = 9


# --------------------------------------------------------------- the graph

def c3_box_c3():
    E = set()
    for i in range(3):
        for j in range(3):
            u = 3 * i + j
            E.add(tuple(sorted((u, 3 * ((i + 1) % 3) + j))))
            E.add(tuple(sorted((u, 3 * i + (j + 1) % 3))))
    return sorted(E)


def indep(e, f):
    return not (set(e) & set(f))


# ------------------------------------------------------- planarity by Euler

def check_planar_embedding(nn, edges, rotation):
    """True iff `rotation` is a rotation system of the graph (nn, edges)
    whose face count satisfies Euler's formula for the sphere."""
    edges = [tuple(sorted(e)) for e in edges]
    if len(set(edges)) != len(edges):
        return False, "multi-edge"
    adj = {v: set() for v in range(nn)}
    for u, v in edges:
        if u == v:
            return False, "loop"
        adj[u].add(v)
        adj[v].add(u)

    rot = {}
    for v in range(nn):
        lst = rotation.get(str(v))
        if lst is None:
            return False, f"no rotation at {v}"
        if sorted(lst) != sorted(adj[v]) or len(set(lst)) != len(lst):
            return False, f"rotation at {v} is not its neighbourhood"
        rot[v] = list(lst)

    # connectivity
    seen = {0}
    stack = [0]
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    if len(seen) != nn:
        return False, "not connected"

    # trace faces: after arriving at v from u, leave along the neighbour
    # following u in v's rotation
    pos = {v: {w: i for i, w in enumerate(rot[v])} for v in range(nn)}
    darts = set()
    for u, v in edges:
        darts.add((u, v))
        darts.add((v, u))
    unused = set(darts)
    faces = 0
    while unused:
        start = next(iter(unused))
        d = start
        while True:
            unused.discard(d)
            u, v = d
            k = pos[v][u]
            w = rot[v][(k + 1) % len(rot[v])]
            d = (v, w)
            if d == start:
                break
            if d not in darts:
                return False, "bad dart"
        faces += 1

    V, Ecount, F = nn, len(edges), faces
    if V - Ecount + F != 2:
        return False, f"Euler V-E+F = {V - Ecount + F} != 2"
    return True, "planar"


# --------------------------------------------------- Kuratowski subdivision

def check_kuratowski(nn, edges, witness):
    """True iff `witness` is a subgraph of (nn, edges) that is a subdivision
    of K5 or K3,3 (hence certifies non-planarity)."""
    mask = witness
    if not isinstance(mask, int) or mask < 0 or (mask >> len(edges)):
        return False, "witness mask out of range"
    W = [tuple(sorted(e)) for i, e in enumerate(edges) if (mask >> i) & 1]
    if len(set(W)) != len(W):
        return False, "repeated edge in witness"
    if not W:
        return False, "empty witness"

    adj = {}
    for u, v in W:
        if u == v:
            return False, "loop"
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    branch = [v for v in adj if len(adj[v]) != 2]
    if any(len(adj[v]) < 2 for v in adj):
        return False, "degree < 2 vertex"

    # suppress degree-2 vertices: walk from each branch vertex along paths
    contracted = []
    for b in branch:
        for start in adj[b]:
            prev, cur = b, start
            while len(adj[cur]) == 2:
                a, c = adj[cur]
                nxt = c if a == prev else a
                prev, cur = cur, nxt
                if cur == b and len(adj[cur]) == 2:
                    return False, "cycle of degree-2 vertices"
            contracted.append(tuple(sorted((b, cur))))
    # every path counted from both ends
    if len(contracted) % 2 != 0:
        return False, "path parity"
    seen = {}
    for e in contracted:
        seen[e] = seen.get(e, 0) + 1
    if any(c != 2 for c in seen.values()):
        return False, "path multiplicity"
    core = sorted(seen)
    if len(core) != len(seen):
        return False, "impossible"

    deg = {}
    for u, v in core:
        if u == v:
            return False, "loop after suppression"
        deg[u] = deg.get(u, 0) + 1
        deg[v] = deg.get(v, 0) + 1
    nb, ne = len(deg), len(core)
    if nb == 5 and ne == 10 and all(d == 4 for d in deg.values()):
        return True, "K5 subdivision"
    if nb == 6 and ne == 9 and all(d == 3 for d in deg.values()):
        # verify bipartite with parts of size 3 and complete between them
        vs = sorted(deg)
        colour = {vs[0]: 0}
        stack = [vs[0]]
        nbr = {v: set() for v in vs}
        for u, v in core:
            nbr[u].add(v)
            nbr[v].add(u)
        while stack:
            v = stack.pop()
            for w in nbr[v]:
                if w not in colour:
                    colour[w] = 1 - colour[v]
                    stack.append(w)
                elif colour[w] == colour[v]:
                    return False, "not bipartite"
        if len(colour) != 6:
            return False, "disconnected core"
        A = [v for v in vs if colour[v] == 0]
        B = [v for v in vs if colour[v] == 1]
        if len(A) != 3 or len(B) != 3:
            return False, "not 3+3"
        return True, "K3,3 subdivision"
    return False, f"core is not K5 or K3,3 ({nb} vertices, {ne} edges)"


# ---------------------------------------------------------- planarizations

def planarize(edges, crossings, n0=N):
    edges = list(edges)
    nxt = n0
    for c in crossings:
        if c[0] == 'x':
            _, e, f = c
            edges.remove(e)
            edges.remove(f)
            edges += [(e[0], nxt), (nxt, e[1]), (f[0], nxt), (nxt, f[1])]
            nxt += 1
        else:
            _, e, f, g = c
            edges.remove(e)
            edges.remove(f)
            edges.remove(g)
            x1, x2 = nxt, nxt + 1
            edges += [(e[0], x1), (x1, x2), (x2, e[1]),
                      (f[0], x1), (x1, f[1]),
                      (g[0], x2), (x2, g[1])]
            nxt += 2
    return nxt, edges


def two_crossing_configs(edges):
    out = []
    pairs = [(e, f) for e, f in itertools.combinations(edges, 2) if indep(e, f)]
    for (a, b), (c, d) in itertools.combinations(pairs, 2):
        if len({a, b, c, d}) == 4:
            out.append([('x', a, b), ('x', c, d)])
    for e in edges:
        others = [f for f in edges if f != e and indep(e, f)]
        for f, g in itertools.permutations(others, 2):
            out.append([('xx', e, f, g)])
    return out


# ------------------------------------------------------------------- main

def main(path):
    cert = json.load(open(path))
    E = c3_box_c3()
    got = sorted(tuple(sorted(e)) for e in cert["graph"]["edges"])
    assert got == E, "certificate graph is not C3 [] C3"
    assert cert["graph"]["n"] == N
    print(f"graph: C3 [] C3, n = {N}, m = {len(E)}  [matches product construction]")

    ok, why = check_kuratowski(N, E, cert["G_nonplanar"])
    assert ok, why
    print(f"cr(G) >= 1: G is non-planar ({why})")

    # cr(G) >= 2
    one = [(e, f) for e, f in itertools.combinations(E, 2) if indep(e, f)]
    assert len(one) == len(cert["one_crossing_witnesses"]), "1-crossing count"
    for (f, g), w in zip(one, cert["one_crossing_witnesses"]):
        nn, ee = planarize(E, [('x', f, g)])
        ok, why = check_kuratowski(nn, ee, w)
        assert ok, f"1-crossing {f},{g}: {why}"
    print(f"cr(G) >= 2: all {len(one)} one-crossing planarizations non-planar")

    # cr(G) >= 3
    cfgs = two_crossing_configs(E)
    assert len(cfgs) == cert["two_crossing_configs"] == len(cert["kuratowski_witnesses"]), \
        "2-crossing configuration count mismatch"
    for cfg, w in zip(cfgs, cert["kuratowski_witnesses"]):
        nn, ee = planarize(E, cfg)
        ok, why = check_kuratowski(nn, ee, w)
        assert ok, f"2-crossing {cfg}: {why}"
    print(f"cr(G) >= 3: all {len(cfgs)} two-crossing planarizations non-planar")

    # cr(G) <= 3
    c3 = cert["cr_le_3"]
    cfg = [('x', tuple(a), tuple(b)) for a, b in c3["crossings"]]
    nn, ee = planarize(E, cfg)
    ok, why = check_planar_embedding(nn, ee, c3["rotation"])
    assert ok, why
    print("cr(G) <= 3: explicit 3-crossing drawing verified  =>  cr(G) = 3")

    # cr(G - e) <= 1 for every edge
    assert len(cert["cr_G_minus_e_le_1"]) == len(E)
    covered = set()
    for w in cert["cr_G_minus_e_le_1"]:
        e = tuple(w["deleted"])
        assert e in E
        covered.add(e)
        rest = [f for f in E if f != e]
        if w["crossing"] is None:
            nn, ee = N, rest
        else:
            f, g = (tuple(x) for x in w["crossing"])
            assert f in rest and g in rest and indep(f, g), f"bad crossing pair for {e}"
            nn, ee = planarize(rest, [('x', f, g)])
        ok, why = check_planar_embedding(nn, ee, w["rotation"])
        assert ok, f"G-{e}: {why}"
    assert covered == set(E), "not every edge covered"
    print(f"cr(G - e) <= 1 for all {len(E)} edges: verified by rotation systems")

    print()
    print("CONCLUSION")
    print("  cr(C3 [] C3) = 3 >= 2.")
    print("  Every proper subgraph is contained in some G - e, so has cr <= 1.")
    print("  Hence C3 [] C3 has NO subgraph of crossing number exactly 2:")
    print("  it is a counterexample to the Bloom-Kennedy-Quintas question.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "certificate.json")

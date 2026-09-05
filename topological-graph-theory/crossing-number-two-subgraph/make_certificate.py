"""Generate a self-contained certificate that C3 [] C3 is 2-crossing-critical
with crossing number 3, hence a counterexample to

    "every graph with crossing number at least 2 contains a subgraph
     with crossing number exactly 2"

The certificate consists of
  (A) for each of the 18 edges e, a 1-crossing planarization of G-e together
      with a rotation system, proving cr(G-e) <= 1;
  (B) for every good 2-crossing planarization of G, a Kuratowski subdivision,
      proving cr(G) >= 3;
  (C) a 3-crossing planarization with a rotation system, proving cr(G) <= 3.

Requires networkx (planarity + Kuratowski subgraphs).  The companion checker
verify_certificate.py uses only the Python standard library.
"""
import itertools
import json

import networkx as nx

# ---------------------------------------------------------------- the graph

def c3_box_c3():
    """C3 [] C3 on vertices 3*i + j, i,j in {0,1,2}."""
    E = []
    for i in range(3):
        for j in range(3):
            u = 3 * i + j
            E.append((u, 3 * ((i + 1) % 3) + j))       # column edge
            E.append((u, 3 * i + (j + 1) % 3))         # row edge
    return sorted(tuple(sorted(e)) for e in set(map(lambda e: tuple(sorted(e)), E)))


N = 9
E = c3_box_c3()
assert len(E) == 18


def indep(e, f):
    return not (set(e) & set(f))


# ------------------------------------------------- planarization generators
# A "configuration" is a list of crossings.  Each crossing consumes edges and
# introduces one dummy vertex.  For an edge crossed twice we split it into
# three arcs, in the stated order.

def planarize(edges, crossings):
    """crossings: list of ('x', e, f) meaning e crosses f at a fresh dummy, or
    ('xx', e, f, g) meaning e is crossed first by f then by g along e."""
    edges = list(edges)
    nxt = N
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
    """All good drawings of `edges` with exactly two crossings, as
    configurations.  Deterministic order; the checker regenerates this list."""
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


# ---------------------------------------------------------------- witnesses

def rotation_system(nn, edges):
    """Planar embedding of (nn, edges) as {v: [neighbours in cyclic order]}."""
    G = nx.Graph()
    G.add_nodes_from(range(nn))
    G.add_edges_from(edges)
    ok, emb = nx.check_planarity(G, counterexample=False)
    if not ok:
        return None
    return {str(v): list(emb.neighbors_cw_order(v)) for v in range(nn)}


def kuratowski(nn, edges):
    """A Kuratowski subdivision inside (nn, edges), or None if planar."""
    G = nx.Graph()
    G.add_nodes_from(range(nn))
    G.add_edges_from(edges)
    ok, cex = nx.check_planarity(G, counterexample=True)
    if ok:
        return None
    want = set(tuple(sorted(e)) for e in cex.edges())
    mask = 0
    for i, e in enumerate(edges):
        if tuple(sorted(e)) in want:
            mask |= 1 << i
    return mask


# ------------------------------------------------------------------ build

def main():
    cert = {"graph": {"n": N, "edges": [list(e) for e in E],
                      "name": "C3 box C3 (= K3 box K3, the 3x3 rook's graph)"}}

    # (A) cr(G - e) <= 1 for every edge e
    partA = []
    for e in E:
        rest = [f for f in E if f != e]
        wit = None
        if rotation_system(N, rest) is not None:
            wit = {"deleted": list(e), "crossing": None,
                   "rotation": rotation_system(N, rest)}
        else:
            for f, g in itertools.combinations(rest, 2):
                if not indep(f, g):
                    continue
                nn, ee = planarize(rest, [('x', f, g)])
                rot = rotation_system(nn, ee)
                if rot is not None:
                    wit = {"deleted": list(e),
                           "crossing": [list(f), list(g)],
                           "rotation": rot}
                    break
        assert wit is not None, f"no 1-crossing drawing of G-{e}"
        partA.append(wit)
    cert["cr_G_minus_e_le_1"] = partA

    # (B) cr(G) >= 3 : every good 2-crossing planarization is non-planar
    configs = two_crossing_configs(E)
    partB = []
    for cfg in configs:
        if cfg[0][0] == 'x':
            nn, ee = planarize(E, cfg)
        else:
            nn, ee = planarize(E, cfg)
        k = kuratowski(nn, ee)
        assert k is not None, f"planar 2-crossing planarization found: {cfg}"
        partB.append(k)
    cert["two_crossing_configs"] = len(configs)
    cert["kuratowski_witnesses"] = partB

    # also: G itself and every 1-crossing planarization are non-planar
    cert["G_nonplanar"] = kuratowski(N, E)
    one = []
    for f, g in itertools.combinations(E, 2):
        if not indep(f, g):
            continue
        nn, ee = planarize(E, [('x', f, g)])
        k = kuratowski(nn, ee)
        assert k is not None, f"cr(G) <= 1 via {f},{g}"
        one.append(k)
    cert["one_crossing_witnesses"] = one

    # (A') each G - e is non-planar, so cr(G - e) = 1 exactly
    cert["G_minus_e_nonplanar"] = [kuratowski(N, [f for f in E if f != e])
                                   for e in E]
    assert all(w is not None for w in cert["G_minus_e_nonplanar"])

    # (C) cr(G) <= 3
    pairs = [(e, f) for e, f in itertools.combinations(E, 2) if indep(e, f)]
    got = None
    for t in itertools.combinations(pairs, 3):
        flat = [x for p in t for x in p]
        if len(set(flat)) != 6:
            continue
        cfg = [('x', a, b) for a, b in t]
        nn, ee = planarize(E, cfg)
        rot = rotation_system(nn, ee)
        if rot is not None:
            got = {"crossings": [[list(a), list(b)] for a, b in t],
                   "rotation": rot}
            break
    assert got is not None
    cert["cr_le_3"] = got

    with open("certificate.json", "w") as fh:
        json.dump(cert, fh, sort_keys=True)
    print("2-crossing configurations:", len(configs))
    print("1-crossing configurations:", len(one))
    print("wrote certificate.json")


if __name__ == "__main__":
    main()

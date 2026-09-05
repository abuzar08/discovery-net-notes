"""Certify every member of the census: for each simple 2-crossing-critical
graph of minimum degree >= 3 on at most 10 vertices, emit

  * a Kuratowski subdivision inside the graph                      (cr >= 1)
  * a Kuratowski subdivision inside every 1-crossing planarization (cr >= 2)
  * a rotation system for one 2-crossing planarization             (cr <= 2)
  * a rotation system for a <=1-crossing planarization of H - e,
    for every edge e                                        (2-crossing-critical)

Together these certify "H is 2-crossing-critical and cr(H) = 2" for each
member, with no planarity algorithm in the trust base of the checker.
"""
import itertools
import json
import sys

import networkx as nx


def indep(e, f):
    return not (set(e) & set(f))


def planarize(n0, edges, crossings):
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


def rotation(nn, edges):
    G = nx.Graph()
    G.add_nodes_from(range(nn))
    G.add_edges_from(edges)
    ok, emb = nx.check_planarity(G, counterexample=False)
    if not ok:
        return None
    return {str(v): list(emb.neighbors_cw_order(v)) for v in range(nn)}


def kuratowski(nn, edges):
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


def ser(cfg):
    """serialise a crossing configuration"""
    out = []
    for c in cfg:
        out.append([c[0]] + [list(x) for x in c[1:]])
    return out


def certify(n, E):
    rec = {"n": n, "edges": [list(e) for e in E]}

    k = kuratowski(n, E)
    assert k is not None, "member is planar"
    rec["nonplanar"] = k

    pairs = [(e, f) for e, f in itertools.combinations(E, 2) if indep(e, f)]
    ones = []
    for f, g in pairs:
        nn, ee = planarize(n, E, [('x', f, g)])
        w = kuratowski(nn, ee)
        assert w is not None, f"cr <= 1 via {f},{g}"
        ones.append(w)
    rec["one_crossing"] = ones

    got = None
    for cfg in two_crossing_configs(E):
        nn, ee = planarize(n, E, cfg)
        r = rotation(nn, ee)
        if r is not None:
            got = {"config": ser(cfg), "rotation": r}
            break
    assert got is not None, "no 2-crossing drawing: this member has cr >= 3"
    rec["cr_le_2"] = got

    dels = []
    for e in E:
        rest = [f for f in E if f != e]
        r = rotation(n, rest)
        if r is not None:
            dels.append({"e": list(e), "crossing": None, "rotation": r})
            continue
        found = None
        for f, g in itertools.combinations(rest, 2):
            if not indep(f, g):
                continue
            nn, ee = planarize(n, rest, [('x', f, g)])
            r = rotation(nn, ee)
            if r is not None:
                found = {"e": list(e), "crossing": [list(f), list(g)],
                         "rotation": r}
                break
        assert found is not None, f"cr(H-{e}) >= 2: not critical"
        dels.append(found)
    rec["delete"] = dels
    return rec


def load(path):
    out = []
    for line in open(path):
        p = line.split()
        if len(p) < 4:
            continue
        E = [tuple(map(int, x.split('-'))) for x in p[3].strip(',').split(',')]
        out.append((p[0], int(p[1]), sorted(E)))
    return out


def main(paths, outpath):
    members = []
    for path in paths:
        for tag, n, E in load(path):
            if tag != "CRIT2":
                continue                       # cr >= 3 members are certified
            members.append(certify(n, E))      # separately in certificate.json
            print(f"  certified n={n} m={len(E)}", flush=True)
    json.dump({"members": members}, open(outpath, "w"), sort_keys=True)
    print(f"wrote {outpath}: {len(members)} certified members")


if __name__ == "__main__":
    main(sys.argv[1:-1], sys.argv[-1])

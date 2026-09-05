"""Validate the reduction lemmas of census.md against an unrestricted search.

`crit2` was also run with no minimum-degree and no edge-count restriction, over
*all* graphs on at most 9 vertices (unrestricted/u6.txt ... u9.txt).  Lemmas 1-4
predict that every 2-crossing-critical graph found there either

  * suppresses (deletion of degree-2 vertices) to a simple graph isomorphic to a
    member of the restricted census n6.txt ... n10.txt, or
  * suppresses to a multigraph with parallel edges, in which case Lemma 2 forces
    crossing number exactly 2,

and that the only one with crossing number >= 3 is C3 [] C3.

    uv run --with networkx python check_reduction.py
"""
import collections
import networkx as nx


def load(path):
    out = []
    for line in open(path):
        p = line.split()
        if len(p) < 4:
            continue
        E = [tuple(map(int, x.split('-'))) for x in p[3].strip(',').split(',')]
        out.append((p[0], int(p[1]), E))
    return out


def suppress(E):
    """Suppress degree-2 vertices; return (#branch vertices, edge multiset)."""
    adj = collections.defaultdict(list)
    for u, v in E:
        adj[u].append(v)
        adj[v].append(u)
    branch = [v for v in adj if len(adj[v]) != 2]
    if not branch:
        return None, 'cycle'
    out = []
    for b in branch:
        for s in adj[b]:
            prev, cur = b, s
            while len(adj[cur]) == 2:
                a, c = adj[cur]
                prev, cur = cur, (c if a == prev else a)
            out.append(tuple(sorted((b, cur))))
    edges = []
    for e, c in collections.Counter(out).items():
        if e[0] == e[1]:
            return None, 'loop'
        edges += [e] * (c // 2)
    return len(branch), edges


def main():
    restricted = []
    for n in range(6, 11):
        restricted += load(f"n{n}.txt")
    R = [(tag, nx.Graph(E)) for tag, _, E in restricted]
    print("restricted census members:", len(R))

    simple_ok = multi = 0
    bad = []
    ge3 = []
    total = 0
    for n in range(6, 10):
        for tag, nn, E in load(f"unrestricted/u{n}.txt"):
            total += 1
            if tag == "CRIT_GE3":
                ge3.append((nn, E))
            nb, edges = suppress(E)
            if nb is None:
                bad.append(("degenerate suppression", nn, edges))
                continue
            if len(set(edges)) != len(edges):
                multi += 1
                if tag != "CRIT2":
                    bad.append(("parallel edges but cr >= 3", nn, E))
                continue
            G = nx.Graph(edges)
            match = [rtag for rtag, H in R if nx.is_isomorphic(G, H)]
            if not match:
                bad.append(("suppression not in restricted census", nn, E))
            elif any(rtag != tag for rtag in match):
                # crossing number is invariant under subdivision, so the tag of
                # an unrestricted graph must equal the tag of the census member
                # its suppression is isomorphic to
                bad.append(("tag mismatch with census member", nn, tag, match))
            else:
                simple_ok += 1

    print(f"unrestricted 2-crossing-critical graphs on <= 9 vertices: {total}")
    print(f"  suppress into the restricted census: {simple_ok}")
    print(f"  suppress to a multigraph with parallel edges (Lemma 2): {multi}")
    print(f"  anomalies: {len(bad)}")
    for b in bad[:10]:
        print("   ", b)
    C33 = nx.cartesian_product(nx.cycle_graph(3), nx.cycle_graph(3))
    print(f"  with crossing number >= 3: {len(ge3)}")
    for nn, E in ge3:
        print(f"    n={nn} isomorphic to C3 [] C3: "
              f"{nx.is_isomorphic(nx.Graph(E), C33)}")
    assert not bad
    print("\nreduction lemmas validated on the unrestricted search")


if __name__ == "__main__":
    main()

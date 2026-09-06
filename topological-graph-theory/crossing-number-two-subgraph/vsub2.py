"""V_8 / V_10 topological containment, without lossy deduplication.

A subdivision of V_k inside a graph on n vertices uses k branch vertices and at
most n - k subdivision vertices, so enumerating every subdivision of V_k with at
most n - k subdivision vertices and testing subgraph monomorphism is complete.
The earlier version deduplicated the enumeration by Weisfeiler-Lehman hash,
which is not a complete invariant and can merge non-isomorphic subdivisions,
producing false negatives; this version does not deduplicate at all.

V_8 and V_10 are cubic, so containing one as a minor and containing a
subdivision of it are equivalent; testing subdivisions is therefore also a
minor test.
"""
import itertools
import json

import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher


def mobius_ladder(k):
    G = nx.cycle_graph(k)
    for i in range(k // 2):
        G.add_edge(i, i + k // 2)
    return G


def subdivisions(H, maxsub):
    E = list(H.edges())
    out = []
    for k in range(maxsub + 1):
        for combo in itertools.combinations_with_replacement(range(len(E)), k):
            G = nx.Graph(H)
            nxt = max(H.nodes()) + 1
            # track, per original edge, the current path realising it
            chain = {i: [E[i][0], E[i][1]] for i in range(len(E))}
            for ei in combo:
                path = chain[ei]
                a, b = path[0], path[1]
                G.remove_edge(a, b)
                G.add_edge(a, nxt)
                G.add_edge(nxt, b)
                chain[ei] = [a, nxt] + path[1:]
                nxt += 1
            out.append(G)
    return out


def contains(G, H, name=''):
    n = G.number_of_nodes()
    k = H.number_of_nodes()
    if n < k:
        return False
    for S in subdivisions(H, n - k):
        if S.number_of_nodes() > n or S.number_of_edges() > G.number_of_edges():
            continue
        if GraphMatcher(G, S).subgraph_is_monomorphic():
            return True
    return False


V8, V10 = mobius_ladder(8), mobius_ladder(10)

if __name__ == '__main__':
    # ---- sanity checks against ground truth from Robertson's Theorem
    C3C3 = nx.cartesian_product(nx.cycle_graph(3), nx.cycle_graph(3))
    C3C3 = nx.convert_node_labels_to_integers(C3C3)
    checks = [
        ('V8 contains V8', V8, V8, True),
        ('V10 contains V10', V10, V10, True),
        ('V10 contains V8', V10, V8, True),
        ('K5 contains V8', nx.complete_graph(5), V8, False),
        ('K33 contains V8', nx.complete_bipartite_graph(3, 3), V8, False),
        # Robertson: C3 x C3 is one of the V8-FREE internally-4-connected graphs
        ('C3xC3 contains V8 (must be False)', C3C3, V8, False),
        ('K7 contains V8', nx.complete_graph(7), V8, False),
        ('K8 contains V8', nx.complete_graph(8), V8, True),
    ]
    bad = 0
    for name, G, H, want in checks:
        got = contains(G, H)
        ok = got == want
        bad += not ok
        print(f"  {name:<38} got {str(got):<6} want {str(want):<6} "
              f"{'OK' if ok else 'FAIL'}")
    print(f"detector sanity: {'all pass' if not bad else str(bad)+' FAIL'}\n")

    graphs = [nx.Graph([tuple(e) for e in E])
              for E in json.load(open('unexplained.json'))]
    rows = []
    for G in graphs:
        rows.append((G.number_of_nodes(), G.number_of_edges(),
                     contains(G, V8), contains(G, V10)))
    ok = sum(1 for _, _, a, b in rows if a or b)
    print(f"census residue: {len(rows)} graphs")
    print(f"explained by a V_8 or V_10 subdivision: {ok}/{len(rows)}")
    byn = {}
    for n, m, a, b in rows:
        byn.setdefault(n, [0, 0])
        byn[n][1] += 1
        byn[n][0] += (a or b)
    for n in sorted(byn):
        print(f"  n={n}: {byn[n][0]}/{byn[n][1]}")
    bad = [(n, m) for n, m, a, b in rows if not (a or b)]
    print(f"\nnot explained: {len(bad)}  {bad}")

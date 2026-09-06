r"""reviewer-1: independent classification of the 3-connected census members of
h3080, to test the partition \(65 = 36 + 10 + 15 + 4\).

My own code for each ingredient:

  * peripheral 4-connectivity, from BORS's definition read out of arXiv:1312.3712
    ("G is peripherally-4-connected if G is 3-connected and, for every 3-cut X in
    G, any partition of the components into nonnull subgraphs H and J has one of
    H and J being a single vertex"), which is equivalent to: for every 3-cut X,
    \(G - X\) has exactly two components and one of them is a single vertex;
  * \(V_8\) and \(V_{10}\) subdivision containment, exhaustive: \(V_k\) is cubic,
    so all \(k\) of its vertices are branch vertices and a subdivision inside an
    \(n\)-vertex graph has at most \(n-k\) subdivision vertices; enumerating how
    those spare vertices are distributed over the \(3k/2\) edges and testing
    subgraph monomorphism is therefore complete;
  * the four graphs of BORS Theorem 15.6, built from Definition 15.2:
    \(K^{*}_{3,4}\) is two disjoint copies of \(K_{2,3}\) whose 3-element sides
    are joined by a perfect matching \(M\); contracting subsets of \(M\) gives
    them.

usage: python3 indep_class.py [census_dir]
"""
import sys, os, itertools, collections
import networkx as nx


# ------------------------------------------------------------------ census I/O
def read_census(d):
    out = []
    for n in range(6, 12):
        p = os.path.join(d, f'n{n}.txt')
        if not os.path.exists(p):
            continue
        for line in open(p):
            q = line.split()
            if not q or not q[0].startswith('CRIT'):
                continue
            nn, mm = int(q[1]), int(q[2])
            E = [tuple(int(x) for x in e.split('-')) for e in q[3].strip(',').split(',') if e]
            G = nx.Graph(E)
            G.add_nodes_from(range(nn))
            assert G.number_of_edges() == mm
            out.append((q[0], nn, mm, G))
    return out


# ------------------------------------------------- peripheral 4-connectivity
def peripherally_4_connected(G):
    if nx.node_connectivity(G) < 3:
        return False
    for X in itertools.combinations(G.nodes, 3):
        H = G.copy()
        H.remove_nodes_from(X)
        comps = list(nx.connected_components(H))
        if len(comps) < 2:
            continue
        if len(comps) > 2 or min(len(c) for c in comps) != 1:
            return False
    return True


# --------------------------------------------------- V_k subdivision testing
def moebius_ladder(k):
    """V_k: the cycle 0..k-1 plus the k/2 main diagonals"""
    G = nx.cycle_graph(k)
    for i in range(k // 2):
        G.add_edge(i, i + k // 2)
    return G


def subdivisions(H, spare):
    """all graphs obtained from H by subdividing edges, using at most `spare`
    new vertices in total"""
    edges = list(H.edges())
    out = []
    for total in range(spare + 1):
        for dist in itertools.combinations_with_replacement(range(len(edges)), total):
            cnt = collections.Counter(dist)
            S = nx.Graph()
            S.add_nodes_from(H.nodes)
            nxt = max(H.nodes) + 1
            for i, (u, v) in enumerate(edges):
                k = cnt.get(i, 0)
                if k == 0:
                    S.add_edge(u, v)
                else:
                    prev = u
                    for _ in range(k):
                        S.add_edge(prev, nxt)
                        prev = nxt
                        nxt += 1
                    S.add_edge(prev, v)
            out.append(S)
    return out


def has_subdivision(G, H):
    """is there a subdivision of H inside G? exhaustive for cubic H"""
    spare = G.number_of_nodes() - H.number_of_nodes()
    if spare < 0:
        return False
    for S in subdivisions(H, spare):
        if S.number_of_nodes() > G.number_of_nodes() or S.number_of_edges() > G.number_of_edges():
            continue
        gm = nx.algorithms.isomorphism.GraphMatcher(G, S)
        if gm.subgraph_is_monomorphic():
            return True
    return False


# ------------------------------------------------- the four Theorem 15.6 graphs
def k34star():
    """Definition 15.2: two disjoint K_{2,3} joined by a perfect matching between
    their 3-element sides"""
    G = nx.Graph()
    # copy A: parts {a0,a1} and {x0,x1,x2}; copy B: {b0,b1} and {y0,y1,y2}
    for a in ('a0', 'a1'):
        for x in ('x0', 'x1', 'x2'):
            G.add_edge(a, x)
    for b in ('b0', 'b1'):
        for y in ('y0', 'y1', 'y2'):
            G.add_edge(b, y)
    M = [('x0', 'y0'), ('x1', 'y1'), ('x2', 'y2')]
    G.add_edges_from(M)
    return G, M


def theorem_15_6_graphs():
    G, M = k34star()
    seen = []
    for r in range(len(M) + 1):
        for sub in itertools.combinations(M, r):
            H = G.copy()
            for (u, v) in sub:
                H = nx.contracted_nodes(H, u, v, self_loops=False)
            H = nx.convert_node_labels_to_integers(H)
            if not any(nx.is_isomorphic(H, K) for K in seen):
                seen.append(H)
    return seen


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    cen = read_census(d)
    print(f'census: {len(cen)} members, tags {collections.Counter(t for t, *_ in cen)}')
    three = [(t, n, m, G) for t, n, m, G in cen if nx.node_connectivity(G) >= 3]
    print(f'3-connected members: {len(three)}')

    V8, V10 = moebius_ladder(8), moebius_ladder(10)
    p4c, withV, rest = [], [], []
    for t, n, m, G in three:
        if peripherally_4_connected(G):
            p4c.append((n, m, G))
        elif has_subdivision(G, V8) or has_subdivision(G, V10):
            withV.append((n, m, G))
        else:
            rest.append((n, m, G))
    print(f'  peripherally 4-connected            : {len(p4c)}')
    print(f'  else with a V8 or V10 subdivision   : {len(withV)}')
    print(f'  remainder                           : {len(rest)}  '
          f'orders/sizes {[(n, m) for n, m, _ in rest]}')

    T = theorem_15_6_graphs()
    print(f'\nBORS Theorem 15.6: {len(T)} graphs from K*_{{3,4}} by contracting subsets of M, '
          f'(n,m) = {sorted((H.number_of_nodes(), H.number_of_edges()) for H in T)}')
    matched = []
    for n, m, G in rest:
        hit = [i for i, H in enumerate(T) if nx.is_isomorphic(G, H)]
        if hit:
            matched.append((n, m, hit[0]))
    print(f'remainder members isomorphic to one of the four: {len(matched)} of {len(rest)}  {matched}')

    # sanity controls for the detector
    print('\ndetector controls:')
    for name, G, H, want in (('V8 in V8', V8, V8, True), ('V8 in V10', V10, V8, True),
                             ('V8 in K8', nx.complete_graph(8), V8, True),
                             ('V8 in K7', nx.complete_graph(7), V8, False),
                             ('V8 in C3xC3', nx.convert_node_labels_to_integers(
                                 nx.cartesian_product(nx.cycle_graph(3), nx.cycle_graph(3))), V8, False),
                             ('V10 in K10', nx.complete_graph(10), V10, True)):
        got = has_subdivision(G, H)
        print(f'   {name:14s} {got} (expected {want}) {"ok" if got == want else "MISMATCH"}')


if __name__ == '__main__':
    main()

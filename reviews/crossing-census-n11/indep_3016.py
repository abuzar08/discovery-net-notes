r"""reviewer-1: independent check of the n <= 11 census claims (h3016).

My own parsing, my own connectivity and subdivision tests; the geng coverage
counts are checked separately with my own build of nauty 2.8.9.
"""
import collections, itertools, sys
import networkx as nx

LANE = ('/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/notes/'
        'topological-graph-theory/crossing-number-two-subgraph/')

def load():
    out = []
    for n in range(6, 12):
        try:
            fh = open(LANE + f'n{n}.txt')
        except FileNotFoundError:
            continue
        for line in fh:
            p = line.split()
            if not p or not p[0].startswith('CRIT'):
                continue
            tag, nn, mm, edges = p[0], int(p[1]), int(p[2]), p[3]
            G = nx.Graph()
            G.add_nodes_from(range(nn))
            for e in edges.strip(',').split(','):
                if not e: continue
                a, b = e.split('-')
                G.add_edge(int(a), int(b))
            out.append((tag, nn, mm, G))
    return out


def has_subdivision(G, H):
    """is there a subdivision of the cubic-or-small graph H inside G? branch
    vertices are mapped injectively, paths internally disjoint"""
    hn = H.number_of_nodes()
    if G.number_of_nodes() < hn:
        return False
    hdeg = dict(H.degree())
    nodes = list(G.nodes())
    for branch in itertools.permutations(nodes, hn):
        if any(G.degree(branch[i]) < hdeg[i] for i in range(hn)):
            continue
        used = set(branch)
        ok = True
        for (a, b) in H.edges():
            Gp = G.copy()
            Gp.remove_nodes_from((used - {branch[a], branch[b]}))
            if not nx.has_path(Gp, branch[a], branch[b]):
                ok = False
                break
            path = nx.shortest_path(Gp, branch[a], branch[b])
            used |= set(path)
        if ok:
            return True
    return False


def main():
    cen = load()
    per = collections.Counter((n, tag) for tag, n, m, G in cen)
    print('CENSUS, my own parse')
    tot2 = tot3 = 0
    for n in range(6, 12):
        c2, c3 = per[(n,'CRIT2')], per[(n,'CRIT_GE3')]
        tot2 += c2; tot3 += c3
        print(f'   n = {n:2d}: CRIT2 {c2:3d}, CRIT_GE3 {c3}')
    print(f'   totals: {tot2} + {tot3} = {tot2+tot3} members')
    conn = collections.Counter(nx.node_connectivity(G) for _, _, _, G in cen)
    print(f'   vertex connectivity distribution {dict(sorted(conn.items()))}')
    print()
    print('THE NON-2-CONNECTED MEMBERS (BORS Proposition 14.1)')
    K5, K33 = nx.complete_graph(5), nx.complete_bipartite_graph(3,3)
    for tag, n, m, G in sorted(cen, key=lambda t: (t[1], t[2])):
        k = nx.node_connectivity(G)
        if k >= 2:
            continue
        if k == 0:
            comps = [G.subgraph(c).copy() for c in nx.connected_components(G)]
        else:
            comps = [G.subgraph(b).copy() for b in nx.biconnected_components(G)]
        kinds = []
        for c in comps:
            kinds.append('K5' if has_subdivision(c, K5)
                         else 'K33' if has_subdivision(c, K33) else '?')
        print(f'   n={n} m={m} connectivity {k}: {len(comps)} '
              f'{"components" if k == 0 else "blocks"}, each a subdivision of '
              f'{kinds}')
    print()
    print('V10 SUBDIVISIONS (my h3080 detector: V_k is cubic, so all k vertices')
    print('   are branch vertices and the spare n-k vertices are distributed over')
    print('   the 3k/2 edges — exhaustive)')
    sys.path.insert(0, '/Users/abuzark/.discovery-research-team/workspaces/'
                       'reviewer-1/notes/reviews/crossing-bors-17-1-3')
    import indep_class as IC
    V10 = IC.moebius_ladder(10)
    hits = [(n, m) for tag, n, m, G in cen if IC.has_subdivision(G, V10)]
    print(f'   members containing a V10 subdivision: {len(hits)} {hits}')


if __name__ == '__main__':
    main()

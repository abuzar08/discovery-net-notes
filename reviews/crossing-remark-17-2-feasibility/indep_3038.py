r"""reviewer-1: independent check of h3038 (researcher-4), the feasibility
correction for BORS Remark 17.2's expansion program.

  1. the 36 peripherally-4-connected seeds and their degree-3 counts, with my
     own p4c test (written for the h3080 review) over the census;
  2. the cumulative expansion counts at branching 31;
  3. the tester's representation limits, read from crit2.c;
  4. the claw-identity acceptance criterion, with my own implementation of the
     expansion (join the patch terminals to the neighbours, then suppress the
     degree-2 vertices), and the sizes it produces.
"""
import collections, itertools, json, sys
import networkx as nx

LANE = ('/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/notes/'
        'topological-graph-theory/crossing-number-two-subgraph/')


def census():
    out = []
    for n in range(6, 12):
        try: fh = open(LANE + f'n{n}.txt')
        except FileNotFoundError: continue
        for line in fh:
            p = line.split()
            if not p or not p[0].startswith('CRIT'): continue
            nn = int(p[1]); G = nx.Graph(); G.add_nodes_from(range(nn))
            for e in p[3].strip(',').split(','):
                if e:
                    a, b = e.split('-'); G.add_edge(int(a), int(b))
            out.append(G)
    return out


def p4c(G):
    """BORS: 3-connected, and for every 3-cut any partition of the components
    into nonnull H, J has one of them a single vertex"""
    if nx.node_connectivity(G) < 3:
        return False
    for X in itertools.combinations(G.nodes, 3):
        H = G.copy(); H.remove_nodes_from(X)
        comps = [len(c) for c in nx.connected_components(H)]
        if len(comps) < 2: continue
        if len(comps) == 2 and min(comps) == 1: continue
        if len(comps) == 3 and max(comps) == 1: continue
        return False
    return True


def expand(G, assign, patches, naive=False):
    """my own expansion.  Correct version: every patched vertex contributes its
    patch with three named terminals, an original edge between two patched
    vertices is realised as an edge between the corresponding terminals, and the
    degree-2 vertices are then suppressed.  With naive=True the terminals are
    joined to the ORIGINAL neighbours instead, which is the construction h3038
    reports as silently wrong when two degree-3 vertices are adjacent."""
    H = nx.MultiGraph()
    H.add_nodes_from(v for v in G.nodes() if v not in assign)
    nxt = max(G.nodes) + 1
    term_of = {}
    for v, pid in assign.items():
        pat = patches[pid]
        nbrs = list(G.neighbors(v))
        assert len(nbrs) == 3
        mapping = {}
        for node in set(itertools.chain(*pat['edges'])) | set(pat['terminals']):
            mapping[node] = nxt; nxt += 1
        for a, b in pat['edges']:
            H.add_edge(mapping[a], mapping[b])
        term_of[v] = {w: mapping[t] for t, w in zip(pat['terminals'], nbrs)}
    for u, w in G.edges():
        if u in assign and w in assign:
            if naive:
                H.add_edge(term_of[u][w], w)      # w no longer exists: the trap
            else:
                H.add_edge(term_of[u][w], term_of[w][u])
        elif u in assign:
            H.add_edge(term_of[u][w], w)
        elif w in assign:
            H.add_edge(term_of[w][u], u)
        else:
            H.add_edge(u, w)
    # suppress degree-2 vertices
    changed = True
    while changed:
        changed = False
        for u in list(H.nodes()):
            if H.degree(u) == 2:
                nb = [w for w in H.neighbors(u) for _ in H.get_edge_data(u, w)]
                if len(nb) == 2 and nb[0] != nb[1]:
                    H.remove_node(u); H.add_edge(nb[0], nb[1]); changed = True
    return H


def main():
    cen = census()
    seeds = [G for G in cen if G.number_of_nodes() <= 10 and p4c(G)]
    print(f'peripherally 4-connected census members on <= 10 vertices: '
          f'{len(seeds)}')
    dist = collections.Counter(sum(1 for _, d in G.degree() if d == 3)
                               for G in seeds)
    print(f'   degree-3 counts d: {dict(sorted(dist.items()))}')
    print()
    print('CUMULATIVE EXPANSIONS AT BRANCHING 31')
    tot = 0
    for d in sorted(dist):
        tot += dist[d] * 31 ** d
        if d in (4, 5, 6):
            print(f'   d <= {d}: {tot}')
    print()
    print('THE TESTER LIMITS, from crit2.c')
    src = open(LANE + 'crit2.c').read()
    print(f'   MAXV = 32 and the guard is "n > MAXV - 4": '
          f'{"n > MAXV - 4" in src} -> at most 28 vertices')
    print(f'   edge guard "M >= 63": {"M >= 63" in src} -> at most 62 edges')
    print(f'   both call exit(1) rather than skipping: '
          f'{src.count("exit(1)") >= 2}')
    print()
    print('THE CLAW-IDENTITY CRITERION, with my own expansion')
    art = json.load(open(LANE + 'figure_15_1_configurations.json'))['configurations']
    claw = [c for c in art if len(c['internal']) == 1
            and len(c['edges']) == 3]
    print(f'   patches with one internal vertex and three edges (the claw): '
          f'{len(claw)}')
    if claw:
        pat = claw[0]
        for naive in (False, True):
            ok = 0
            for G in seeds:
                deg3 = [v for v, d in G.degree() if d == 3]
                H = expand(G, {v: 0 for v in deg3}, [pat], naive=naive)
                S = nx.Graph(); S.add_edges_from(H.edges())
                if nx.is_isomorphic(S, G):
                    ok += 1
            print(f'   {"naive (terminals joined to original neighbours)" if naive else "correct construction"}: '
                  f'{ok} of {len(seeds)} seeds returned unchanged by the claw')
        adj = sum(1 for G in seeds
                  if any(G.degree(u) == 3 and G.degree(w) == 3 for u, w in G.edges()))
        print(f'   seeds with two adjacent degree-3 vertices, where the two '
              f'constructions differ: {adj} of {len(seeds)}')


if __name__ == '__main__':
    main()

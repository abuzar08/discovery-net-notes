r"""reviewer-1: h2929's qualitative conclusion, re-tested in the MULTIGRAPH
universe that h3018 showed is the right one.

h2929 enumerated (T,U)-configurations as simple graphs and concluded that
subgraph-minimality does not select Figure 15.1's patches, the counts growing
with the enumeration bound.  h3018 corrected the universe: the patches are
multigraphs.  This checks the conclusion where it belongs:

  1. are the 31 published patches minimal — i.e. does some proper subgraph of
     the same (T,U) type remain a configuration?
  2. in the multigraph universe with internal size at most 2 and at most 3, how
     many configurations and how many minimal representatives are there, and do
     the counts grow with the bound?
"""
import collections, itertools, json
import networkx as nx
from indep_fig151 import classify, apex_planar, ART


def load_patches():
    art = json.load(open(ART))['configurations']
    out = []
    for c in art:
        H = nx.MultiGraph()
        H.add_nodes_from(c['terminals'] + c['internal'])
        H.add_edges_from(tuple(e) for e in c['edges'])
        out.append((H, c['terminals'], c['internal'], (c['T'], c['U'])))
    return out


def is_bridge(H, terms):
    """an ||{x,y,z}||-bridge: connected, and every internal vertex has all its
    neighbours inside H (automatic here), with at least one edge"""
    return H.number_of_edges() > 0 and nx.is_connected(H)


def is_config(H, terms):
    return is_bridge(H, terms) and apex_planar(H, terms)


def proper_subgraphs(H, terms):
    """delete one edge, or delete one internal vertex, keeping the terminals"""
    edges = list(H.edges(keys=True))
    for (u, v, k) in edges:
        K = H.copy(); K.remove_edge(u, v, key=k)
        K.remove_nodes_from([w for w in list(K.nodes())
                             if w not in terms and K.degree(w) == 0])
        yield K
    for w in list(H.nodes()):
        if w in terms:
            continue
        K = H.copy(); K.remove_node(w)
        yield K


def minimal(H, terms, cls):
    for K in proper_subgraphs(H, terms):
        if K.number_of_edges() == 0:
            continue
        if not nx.is_connected(K):
            continue
        if classify(K, terms) == cls and is_config(K, terms):
            return False, K
    return True, None


def enumerate_multigraphs(ninternal, maxmult=2):
    terms = ['x', 'y', 'z']
    internal = [f'a{i}' for i in range(ninternal)]
    nodes = terms + internal
    pairs = list(itertools.combinations(nodes, 2))
    seen = {}
    for mult in itertools.product(range(maxmult + 1), repeat=len(pairs)):
        H = nx.MultiGraph()
        H.add_nodes_from(nodes)
        for (u, v), m in zip(pairs, mult):
            for _ in range(m):
                H.add_edge(u, v)
        if any(H.degree(w) == 0 for w in internal):
            continue
        if not is_config(H, terms):
            continue
        cls = classify(H, terms)
        key = canon(H, terms)
        if key not in seen:
            seen[key] = (H, cls)
    return seen


def canon(H, terms):
    """canonical form under permutations of the internal vertices only
    (terminals are distinguishable, but the figure's grouping is up to
    relabelling the terminals too, so also quotient by the 6 terminal maps)"""
    internal = [w for w in H.nodes() if w not in terms]
    best = None
    for tp in itertools.permutations(terms):
        for ip in itertools.permutations(internal):
            m = dict(zip(terms, tp)); m.update(dict(zip(internal, ip)))
            e = sorted(tuple(sorted((m[u], m[v]))) for u, v in H.edges())
            k = tuple(e)
            if best is None or k < best:
                best = k
    return best


def main():
    print('(1) ARE THE 31 PUBLISHED PATCHES MINIMAL?')
    pats = load_patches()
    nonmin = []
    for H, terms, internal, cls in pats:
        ok, wit = minimal(H, terms, cls)
        if not ok:
            nonmin.append((cls, len(internal)))
    print(f'   patches: {len(pats)}; NOT minimal: {len(nonmin)}')
    if nonmin:
        c = collections.Counter(nonmin)
        print(f'   non-minimal by (class, internal size): {dict(c)}')
    print(f'   internal sizes of the (3,2) class: '
          f'{[len(i) for H,t,i,c in pats if c == (3,2)]}')
    print()
    print('(2) THE MULTIGRAPH UNIVERSE, internal size at most 2 and 3')
    for ni in (1, 2):
        seen = enumerate_multigraphs(ni)
        cls = collections.Counter(c for _, c in seen.values())
        mins = collections.Counter()
        for H, c in seen.values():
            ok, _ = minimal(H, ['x', 'y', 'z'], c)
            if ok:
                mins[c] += 1
        print(f'   internal size exactly {ni}: {len(seen)} configurations '
              f'{dict(sorted(cls.items()))}')
        print(f'      minimal among them: {sum(mins.values())} '
              f'{dict(sorted(mins.items()))}')


if __name__ == '__main__':
    main()

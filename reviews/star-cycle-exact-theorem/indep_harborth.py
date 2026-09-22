"""Independent exact crossing numbers for K_{1,1,1,m}, small m.

Gates the Harborth closed form X(m) = floor(m/2)*floor((m-1)/2) that the
height-5504 theorem inherits rather than reproves.

Method: cr(G) <= k iff some planarisation of G with k crossings is planar.
Optimal drawings may be assumed good -- no edge crosses itself, adjacent
edges do not cross, two edges cross at most once -- so it suffices to
enumerate k-subsets of non-adjacent edge pairs, and, for an edge carrying
several crossings, the orders in which they occur along it.
"""
import itertools
import networkx as nx


def k111m(m):
    G = nx.Graph()
    for i, j in itertools.combinations(range(3), 2):
        G.add_edge(('c', i), ('c', j))
    for v in range(m):
        for i in range(3):
            G.add_edge(('v', v), ('c', i))
    return G


def planarise(G, pairs, orders):
    """Split each edge at its crossing points in the given order."""
    H = nx.Graph()
    H.add_nodes_from(G.nodes())
    xing = {p: ('x', idx) for idx, p in enumerate(pairs)}
    on = {}
    for p in pairs:
        for e in p:
            on.setdefault(e, []).append(p)
    for e in G.edges():
        e = tuple(sorted(e, key=repr))
        if e not in on:
            H.add_edge(*e)
            continue
        seq = orders[e]
        chain = [e[0]] + [xing[p] for p in seq] + [e[1]]
        for a, b in zip(chain, chain[1:]):
            H.add_edge(a, b)
    return H


def cr_leq(G, k):
    """Is there a good drawing of G with at most k crossings?"""
    edges = [tuple(sorted(e, key=repr)) for e in G.edges()]
    cand = [(e, f) for e, f in itertools.combinations(edges, 2)
            if not set(e) & set(f)]
    for size in range(k + 1):
        for pairs in itertools.combinations(cand, size):
            on = {}
            for p in pairs:
                for e in p:
                    on.setdefault(e, []).append(p)
            multi = [e for e in on if len(on[e]) > 1]
            fixed = {e: on[e] for e in on if len(on[e]) == 1}
            for perm in itertools.product(*[itertools.permutations(on[e])
                                            for e in multi]):
                orders = dict(fixed)
                orders.update(dict(zip(multi, perm)))
                if nx.check_planarity(planarise(G, pairs, orders),
                                      counterexample=False)[0]:
                    return True, pairs
    return False, None


def X(m):
    return (m // 2) * ((m - 1) // 2)


if __name__ == '__main__':
    for m in range(2, 6):
        G = k111m(m)
        t = X(m)
        up, w = cr_leq(G, t)
        lo = cr_leq(G, t - 1)[0] if t else False
        print('K_1,1,1,%d: n=%d m=%d  X(m)=%d  cr <= X(m): %s  cr <= X(m)-1: %s'
              % (m, G.number_of_nodes(), G.number_of_edges(), t, up, lo),
              flush=True)
        print('   => cr = %s' % (t if (up and not lo) else '?'), flush=True)

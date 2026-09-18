r"""reviewer-1: independent checks on the Mohar Conjecture 5 chain.

Everything here is elementary. Lower bounds come from Euler
(\(\mathrm{cr} \ge m - (3n-6)\)) and from the vertex-deletion counting bound
(\(\sum_v \mathrm{cr}(G-v) \le (n-4)\,\mathrm{cr}(G)\)); upper bounds come from
exhaustive two-page drawings — all cyclic vertex orders, pages optimised by local
search with restarts — since the two-page crossing number bounds the crossing
number above. Where the two meet, the value is exact.
"""
import itertools
import random

import networkx as nx


def euler_lb(G):
    n, m = G.number_of_nodes(), G.number_of_edges()
    return max(0, m - (3 * n - 6))


def interleave(a, b, c, d):
    return (a < c < b < d) or (c < a < d < b)


def twopage(G, restarts=6, rng=None):
    """exact-ish two-page crossing number: all cyclic orders, pages by local
    search"""
    rng = rng or random.Random(12345)
    nodes = list(G.nodes())
    n = len(nodes)
    best = None
    for perm in itertools.permutations(nodes[1:]):
        order = [nodes[0]] + list(perm)
        if order[1] > order[-1]:
            continue                            # fix reflection
        pos = {v: i for i, v in enumerate(order)}
        edges = [(pos[u], pos[v]) if pos[u] < pos[v] else (pos[v], pos[u])
                 for u, v in G.edges()]
        cross = [[] for _ in edges]
        for i in range(len(edges)):
            for j in range(i + 1, len(edges)):
                a, b = edges[i]
                c, d = edges[j]
                if len({a, b, c, d}) == 4 and interleave(a, b, c, d):
                    cross[i].append(j)
                    cross[j].append(i)
        for t in range(restarts):
            page = [rng.randrange(2) for _ in edges]
            improved = True
            while improved:
                improved = False
                for i in range(len(edges)):
                    same = sum(1 for j in cross[i] if page[j] == page[i])
                    if len(cross[i]) - same < same:
                        page[i] ^= 1
                        improved = True
            tot = sum(1 for i, cs in enumerate(cross) for j in cs
                      if j > i and page[j] == page[i])
            if best is None or tot < best:
                best = tot
    return best


def Km(n, t):
    """K_n minus a matching of size t"""
    G = nx.complete_graph(n)
    for i in range(t):
        G.remove_edge(2 * i, 2 * i + 1)
    return G


def counting_lb(G, values):
    """(n-4) cr(G) >= sum_v cr(G - v), with cr(G-v) supplied"""
    n = G.number_of_nodes()
    s = sum(values)
    return -(-s // (n - 4))


def main():
    print('(1) DS21 rendering at n = 5: reduction term (2-1)(2-2) = 0, so the')
    print('    rendering asserts cr(K_5 - M) = H(5) = 1 for every matching M')
    for t in (1, 2):
        G = Km(5, t)
        print(f'    K_5 minus a {t}-matching: planar = '
              f'{nx.check_planarity(G, counterexample=False)[0]}, so cr = 0')
    print()
    print('(2) n = 6, k = 3: the conjecture predicts 3 - t for t = 0..3')
    for t in range(4):
        G = Km(6, t)
        lb, ub = euler_lb(G), twopage(G)
        print(f'    t = {t}: {G.number_of_edges()} edges, Euler lower bound '
              f'{lb}, two-page upper bound {ub} -> '
              f'{"exact " + str(lb) if lb == ub else "range [%d,%d]" % (lb, ub)}'
              f'   (predicted {3 - t})')
    print()
    print('(3) the two inputs to the n = 8, t = 2 lower bound, verified from scratch')
    k7e = Km(7, 1)
    vals = []
    for v in k7e.nodes():
        H = k7e.copy()
        H.remove_node(v)
        m = H.number_of_edges()
        vals.append(3 if m == 15 else 2)
    print(f'    K_7 - e: vertex-deleted subgraphs are two copies of K_6 '
          f'(cr 3) and five of K_6 - e (cr 2)')
    print(f'      counting bound: 3 cr >= {sum(vals)}, so cr >= '
          f'{counting_lb(k7e, vals)}; two-page upper bound {twopage(k7e)}')
    k72 = Km(7, 2)
    print(f'    K_7 - 2e: {k72.number_of_edges()} edges, Euler lower bound '
          f'{euler_lb(k72)}, two-page upper bound {twopage(k72)}')
    print()
    print('(4) the counting bound at n = 8, t = 2')
    M82 = Km(8, 2)
    degs = sorted(d for _, d in M82.degree())
    print(f'    M_82: {M82.number_of_nodes()} vertices, '
          f'{M82.number_of_edges()} edges, degrees {degs}')
    vals = [6, 6, 6, 6, 4, 4, 4, 4]
    print(f'    four covered vertices give K_7 - e (6), four uncovered give '
          f'K_7 - 2e (4): 4 cr >= {sum(vals)}, so cr >= {counting_lb(M82, vals)}')
    ind = M82.number_of_edges() * (M82.number_of_edges() - 1) // 2 \
        - sum(d * (d - 1) // 2 for _, d in M82.degree())
    print(f'    independent edge pairs: {ind} (published 181)')
    print(f'    Euler lower bound alone: {euler_lb(M82)}')
    print()
    print('(5) K_2222 at n = 8, t = 4, attributed to Ho (2008)')
    M84 = Km(8, 4)
    print(f'    {M84.number_of_edges()} edges, Euler lower bound '
          f'{euler_lb(M84)}; the value 6 therefore needs no citation for its '
          f'lower half')


if __name__ == '__main__':
    main()

r"""reviewer-1: the matching model at k <= 3 over all 20 Figure 14.3 components.

h3285 reports 55 identified graphs across the 19 components settled at
\(k \le 3\); h3305 says "all identifications of at most four pairs have been
checked exhaustively (137 are 2-crossing-critical)".  55 + 64 = 119, not 137,
so the two statements do not agree.  This measures the least-\(k\) counts myself,
in the matching model of h3285 and with its minimum-degree filter reported
separately, so the discrepancy can be located rather than guessed at.
"""
import multiprocessing as mp

from indep_fig143 import drawn_components, identify, verdict


def matchings(nodes, k):
    if k == 0:
        yield ()
        return
    nodes = list(nodes)
    if len(nodes) < 2 * k:
        return
    first = nodes[0]
    for rest in matchings(nodes[1:], k):
        yield rest
    for j in range(1, len(nodes)):
        pair = (first, nodes[j])
        remain = nodes[1:j] + nodes[j + 1:]
        for rest in matchings(remain, k - 1):
            yield (pair,) + rest


def work(arg):
    idx, n, edges, m = arg
    import networkx as nx
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)
    H = identify(G, m)
    if H.number_of_nodes() < 5:
        return None
    mindeg = min(d for _, d in H.degree())
    v = verdict(H)
    if v is None:
        return None
    return (idx, v, mindeg)


if __name__ == '__main__':
    gs = drawn_components()
    bad = [g for g in gs if verdict(g) is None]
    print(f'components not 2-crossing-critical as drawn: {len(bad)}', flush=True)
    total_all, total_kept = 0, 0
    pool = mp.Pool(4)
    for i, G in enumerate(bad):
        n = G.number_of_nodes()
        edges = list(G.edges())
        nm = (n, G.number_of_edges())
        hit = None
        for k in (1, 2, 3):
            jobs = [(i, n, edges, m) for m in matchings(range(n), k) if len(m) == k]
            res = [r for r in pool.map(work, jobs, chunksize=64) if r is not None]
            if res:
                hit = (k, res, len(jobs))
                break
        if hit is None:
            print(f'  {nm}: no matching of <= 3 pairs is 2-crossing-critical', flush=True)
            continue
        k, res, tried = hit
        kinds = sorted({v for _, v, _ in res})
        kept = [r for r in res if r[2] >= 3]
        total_all += len(res)
        total_kept += len(kept)
        print(f'  {nm}: least k = {k}, {tried} matchings, {len(res)} critical '
              f'{kinds}, of which {len(kept)} have minimum degree >= 3', flush=True)
    print(f'total over the settled components: {total_all} critical, '
          f'{total_kept} with minimum degree >= 3', flush=True)

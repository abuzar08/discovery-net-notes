r"""reviewer-1: reconcile my (14,22) matching search with h3285's counts.

h3285 reports "over all matchings of four pairs, 142,321 tested, 64 yield a
2-crossing-critical graph".  My own run (match4.py) enumerates 315315 matchings
of four pairs on 14 vertices and finds 274 that are 2-crossing-critical.  The
lane's fig143b.py counts only the identifications that survive a filter — at
least five vertices and minimum degree at least 3 — applied BEFORE the verdict,
so its "tested" number is the size of the filtered set, not of the search.

This script measures both numbers with my own code: how many of the 315315
matchings survive that filter, and how many of those are 2-crossing-critical.
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


G = None


def init():
    global G
    gs = drawn_components()
    t = [g for g in gs
         if (g.number_of_nodes(), g.number_of_edges()) == (14, 22)
         and verdict(g) is None]
    G = t[0]


def work(m):
    H = identify(G, m)
    if H.number_of_nodes() < 5:
        return ('small', None)
    mindeg = min(d for _, d in H.degree())
    if mindeg < 3:
        return ('lowdeg', verdict(H))
    return ('kept', verdict(H))


if __name__ == '__main__':
    init()
    ms = [m for m in matchings(range(14), 4) if len(m) == 4]
    print(f'matchings of four pairs on 14 vertices: {len(ms)}', flush=True)
    with mp.Pool(4, initializer=init) as pool:
        res = pool.map(work, ms, chunksize=64)
    kept = [v for tag, v in res if tag == 'kept']
    low = [v for tag, v in res if tag == 'lowdeg']
    small = [1 for tag, _ in res if tag == 'small']
    crit_kept = [v for v in kept if v is not None]
    crit_low = [v for v in low if v is not None]
    print(f'  fewer than five vertices after identification : {len(small)}')
    print(f'  minimum degree < 3 after identification       : {len(low)}')
    print(f'  surviving the lane\'s filter (n>=5, mindeg>=3) : {len(kept)}')
    print(f'  2-crossing-critical among the survivors       : {len(crit_kept)} '
          f'{sorted(set(crit_kept))}')
    print(f'  2-crossing-critical among the min-degree-2 set: {len(crit_low)} '
          f'{sorted(set(crit_low))}')
    print(f'  2-crossing-critical over all matchings        : '
          f'{len(crit_kept) + len(crit_low)}')

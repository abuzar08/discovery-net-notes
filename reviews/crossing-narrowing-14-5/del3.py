r"""reviewer-1: the three-edge deletion case of h3084's negative claim, plus a
check that the 166 leftover circles really are coincident duplicates."""
import itertools, multiprocessing as mp
import networkx as nx
import extract_fig as X
from indep_fig143 import drawn_components, verdict
from indep_3084 import job

def duplicates():
    v, E = X.extract('bors.pdf', 127)
    used = set()
    for c in X.components(v, E):
        if len(c) >= 5:
            used |= set(c)
    left = [u for u in range(len(v)) if u not in used]
    pts = [c for c, _ in v]
    coincident = 0
    for u in left:
        x, y = pts[u]
        if any(w != u and abs(pts[w][0] - x) < 1e-9 and abs(pts[w][1] - y) < 1e-9
               for w in range(len(pts))):
            coincident += 1
    return len(left), coincident

if __name__ == '__main__':
    n_left, coin = duplicates()
    print(f'leftover raw vertices: {n_left}, of which coincident with another '
          f'at distance 0: {coin}', flush=True)
    gs = drawn_components()
    bad = [g for g in gs if verdict(g) is None]
    jobs = []
    for G in bad:
        n = G.number_of_nodes(); es = list(G.edges())
        for sub in itertools.combinations(es, 3):
            jobs.append(('delete3', n, es, sub))
    print(f'{len(jobs)} three-edge deletions to test', flush=True)
    with mp.Pool(4) as pool:
        res = [r for r in pool.map(job, jobs, chunksize=64) if r is not None]
    print(f'delete3: {len(res)} give a 2-crossing-critical graph'
          + (f' {sorted({r[2] for r in res})}' if res else ' — none, as claimed'),
          flush=True)

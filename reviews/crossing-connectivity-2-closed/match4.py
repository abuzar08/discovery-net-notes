r"""reviewer-1: my own matching-model identification search for the (14,22)
component of BORS Figure 14.3 — the holdout that h3285 settles.

Identifying vertices the figure drew twice pairs up DISTINCT duplicates, so the
faithful model is a partial matching on the vertex set. This enumerates all
matchings of at most four pairs, applies them, and records the verdict of every
one that is 2-crossing-critical, with my own crossing-number code."""
import itertools, sys
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


gs = drawn_components()
target = [G for G in gs if (G.number_of_nodes(), G.number_of_edges()) == (14, 22)
          and verdict(G) is None]
print(f'holdout components: {len(target)}', flush=True)
for G in target:
    n = G.number_of_nodes()
    for k in range(1, 5):
        res, tried = [], 0
        for m in matchings(range(n), k):
            if len(m) != k:
                continue
            tried += 1
            H = identify(G, m)
            if H.number_of_nodes() < 5:
                continue
            v = verdict(H)
            if v is not None:
                res.append(v)
        print(f'  k = {k}: {tried} matchings tried, {len(res)} are 2-crossing-critical, '
              f'verdicts {sorted(set(res))}', flush=True)

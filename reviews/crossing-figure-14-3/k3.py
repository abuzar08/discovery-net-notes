r"""reviewer-1: k = 3 identifications for the two components unresolved at k <= 2."""
import itertools, sys, networkx as nx
from indep_fig143 import drawn_components, identify, verdict
gs = drawn_components()
targets = [G for G in gs if verdict(G) is None and
           (G.number_of_nodes(), G.number_of_edges()) in {(13, 21), (14, 22)}]
print(f'targets: {[(G.number_of_nodes(), G.number_of_edges()) for G in targets]}', flush=True)
for G in targets:
    n, m = G.number_of_nodes(), G.number_of_edges()
    res = []
    for pairs in itertools.combinations(itertools.combinations(range(n), 2), 3):
        H = identify(G, pairs)
        if H.number_of_nodes() < 5:
            continue
        v = verdict(H)
        if v is not None:
            res.append(v)
    kinds = sorted(set(res))
    print(f'({n},{m}): {len(res)} identifications of 3 pairs are 2-crossing-critical, verdicts {kinds}', flush=True)

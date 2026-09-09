r"""reviewer-1: exhaustive decidable counts for the five 8-vertex d = 4 seeds,
to test whether the published per-class figure 163,783 of 923,521 is per seed."""
import collections, itertools, json, sys
import networkx as nx
from indep_3038 import census, p4c, expand, LANE
from indep_d4 import sizes

art = json.load(open(LANE + 'figure_15_1_configurations.json'))['configurations']
seeds = [G for G in census() if G.number_of_nodes() <= 10 and p4c(G)]
eight = [G for G in seeds
         if G.number_of_nodes() == 8
         and sum(1 for _, d in G.degree() if d == 3) == 4]
print(f'{len(eight)} seeds on 8 vertices with d = 4', flush=True)
for idx, G in enumerate(eight):
    deg3 = [v for v, d in G.degree() if d == 3]
    dec = 0
    for choice in itertools.product(range(31), repeat=4):
        H = expand(G, dict(zip(deg3, choice)), art)
        n, m = sizes(H)
        if n <= 28 and m <= 62:
            dec += 1
    print(f'   seed {idx}: {dec} of 923521 decidable = {100*dec/923521:.2f}% '
          f'(published 163783 = 17.73%)', flush=True)

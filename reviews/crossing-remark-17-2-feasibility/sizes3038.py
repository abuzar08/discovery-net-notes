r"""reviewer-1: the sizes of the expansions, and the fraction the tester can
decide, sampled with my own expansion construction."""
import json, random, collections
import networkx as nx
from indep_3038 import census, p4c, expand, LANE

random.seed(20260907)
art = json.load(open(LANE + 'figure_15_1_configurations.json'))['configurations']
seeds = [G for G in census() if G.number_of_nodes() <= 10 and p4c(G)]
bydeg = collections.defaultdict(list)
for G in seeds:
    bydeg[sum(1 for _, d in G.degree() if d == 3)].append(G)

print('sampled expansions, my own construction (1000 per d)')
for d in (4, 5, 6):
    if d not in bydeg:
        continue
    maxn = maxm = 0
    dec = 0
    N = 1000
    for _ in range(N):
        G = random.choice(bydeg[d])
        deg3 = [v for v, dd in G.degree() if dd == 3]
        assign = {v: random.randrange(len(art)) for v in deg3}
        H = expand(G, assign, art)
        # what is handed to crit2: extra parallel copies subdivided, so each
        # extra copy costs one vertex and one edge
        extra = sum(c - 1 for c in collections.Counter(
            (min(u, v), max(u, v)) for u, v in H.edges()).values())
        n = H.number_of_nodes() + extra
        m = H.number_of_edges() + extra
        maxn, maxm = max(maxn, n), max(maxm, m)
        if n <= 28 and m <= 62:
            dec += 1
    print(f'   d = {d}: max n = {maxn}, max m = {maxm}; decidable by crit2 '
          f'(n <= 28 and m <= 62): {100*dec/N:.1f}%   '
          f'(published: {"n = 45, m = 71, 16.7%" if d == 4 else "n = 55, m = 87, 2.3%" if d == 5 else "n = 59, m = 92, 0%"})')

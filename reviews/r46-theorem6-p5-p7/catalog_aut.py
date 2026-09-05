"""reviewer-1: check the catalog claim of h3014 -- Exoo's known (4,6,35)-graphs
all have |Aut| in {1,2,4}, so none has an automorphism of order 5 or 7."""
import sys, os, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'r46'))
import networkx as nx
from indep_catalog import g6
lines = [l for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'r46',
                                      'r46_35some.g6')).read().split('\n') if l.strip()]
print(f'{len(lines)} graphs in r46_35some.g6')
from collections import Counter
cnt = Counter(); bad = []
for i, l in enumerate(lines):
    n, E = g6(l)
    G = nx.Graph(E); G.add_nodes_from(range(n))
    assert n == 35
    # (4,6)-good: no K4, no independent 6-set
    k4 = any(all(G.has_edge(a, b) for a, b in itertools.combinations(S, 2))
             for S in itertools.combinations(range(n), 4))
    aut = sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(G, G).isomorphisms_iter())
    cnt[aut] += 1
    if aut % 5 == 0 or aut % 7 == 0:
        bad.append((i, aut))
    if k4:
        bad.append((i, 'K4'))
print('automorphism group orders:', dict(sorted(cnt.items())))
print('graphs with order divisible by 5 or 7, or containing a K4:', bad if bad else 'none')

r"""reviewer-1: the partition exactly as h3080 states it."""
import itertools, os, networkx as nx, indep_class as I
from p4c_fix import p4c
cen = I.read_census(os.path.dirname(os.path.abspath(__file__)))
three = [(n, m, G) for t, n, m, G in cen if nx.node_connectivity(G) >= 3]
V8, V10 = I.moebius_ladder(8), I.moebius_ladder(10)
hasV = lambda G: I.has_subdivision(G, V8) or I.has_subdivision(G, V10)
bases = [(n,m,G) for n,m,G in three if p4c(G) and n <= 10]
rest1 = [(n,m,G) for n,m,G in three if not (p4c(G) and n <= 10)]
vv    = [(n,m,G) for n,m,G in rest1 if hasV(G)]
rest2 = [(n,m,G) for n,m,G in rest1 if not hasV(G)]
T = I.theorem_15_6_graphs()
four  = [(n,m,G) for n,m,G in rest2 if any(nx.is_isomorphic(G,H) for H in T)]
fifteen = [(n,m,G) for n,m,G in rest2 if not any(nx.is_isomorphic(G,H) for H in T)]
print(f'bases: peripherally 4-connected on <= 10 vertices : {len(bases)}')
print(f'V8 or V10 subdivision among the rest              : {len(vv)}  '
      f'(orders {sorted(n for n,_,_ in vv)}, of which peripherally 4-connected on 11 vertices: '
      f'{sum(1 for n,m,G in vv if p4c(G))})')
print(f'Theorem 15.6 graphs                               : {len(four)}  {[(n,m) for n,m,_ in four]}')
print(f'remaining, for the replacement construction       : {len(fifteen)}  '
      f'(orders {sorted(n for n,_,_ in fifteen)})')
print(f'\n{len(bases)} + {len(vv)} + {len(fifteen)} + {len(four)} = '
      f'{len(bases)+len(vv)+len(fifteen)+len(four)}   (h3080: 36 + 10 + 15 + 4 = 65)')

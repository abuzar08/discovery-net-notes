r"""reviewer-1: does h3080's partition order explain the class sizes?
Classify the 65 3-connected census members as: (a) has a V8 or V10 subdivision;
(b) otherwise peripherally 4-connected; (c) the rest."""
import networkx as nx, indep_class as I, collections, os
cen = I.read_census(os.path.dirname(os.path.abspath(__file__)))
three = [(n, m, G) for t, n, m, G in cen if nx.node_connectivity(G) >= 3]
V8, V10 = I.moebius_ladder(8), I.moebius_ladder(10)
withV, p4c, rest = [], [], []
for n, m, G in three:
    if I.has_subdivision(G, V8) or I.has_subdivision(G, V10):
        withV.append((n, m, G))
    elif I.peripherally_4_connected(G):
        p4c.append((n, m, G))
    else:
        rest.append((n, m, G))
print(f'3-connected members: {len(three)}')
print(f'  with a V8 or V10 subdivision : {len(withV)}   orders {sorted(n for n,_,_ in withV)}')
print(f'  else peripherally 4-connected: {len(p4c)}')
print(f'  remainder                    : {len(rest)}   (n,m) {sorted((n,m) for n,m,_ in rest)}')
T = I.theorem_15_6_graphs()
four = [(n, m) for n, m, G in rest if any(nx.is_isomorphic(G, H) for H in T)]
print(f'  of the remainder, isomorphic to a Theorem 15.6 graph: {len(four)} {four}')
print(f'  leaving {len(rest)-len(four)} for the replacement construction with cr(L) = 1')
print(f'\npartition: {len(p4c)} + {len(withV)} + {len(rest)-len(four)} + {len(four)} = '
      f'{len(p4c)+len(withV)+len(rest)}  (h3080 claims 36 + 10 + 15 + 4 = 65)')

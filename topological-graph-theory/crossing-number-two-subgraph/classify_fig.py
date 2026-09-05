"""Classify every configuration extracted from BORS Figure 15.1.

Definition 15.21 (BORS arXiv:1312.3712), for H an ||{x,y,z}||-bridge:
  T = { w in {x,y,z} : there are edge-disjoint w-({x,y,z}-w) paths in H }
  U = { w in {x,y,z} : there are edge-disjoint paths in H-w joining the other two }
(H,{x,y,z}) is a (T,U)-configuration when H plus an apex adjacent to x,y,z is
planar.

The patches are MULTIGRAPHS -- Figure 15.1 draws parallel edges as lenses -- so
both conditions must be evaluated with edge multiplicities as capacities.  Using
simple-graph edge connectivity misclassifies them; that error is what height
2929 recorded and what this run corrects.
"""
import collections
import itertools

import networkx as nx

import extract_fig as X

TERMS = ('x', 'y', 'z')


def capacity_graph(mult):
    C = nx.Graph()
    C.add_nodes_from(TERMS)
    for (u, v), m in mult.items():
        C.add_edge(u, v, capacity=m)
    return C


def classify(mult, nodes):
    C = nx.Graph()
    C.add_nodes_from(nodes)
    for (u, v), m in mult.items():
        C.add_edge(u, v, capacity=m)
    T = set()
    for w in TERMS:
        others = [t for t in TERMS if t != w]
        D = C.copy()
        D.add_node('SINK')
        for t in others:
            D.add_edge(t, 'SINK', capacity=10 ** 6)
        if nx.maximum_flow_value(D, w, 'SINK', capacity='capacity') >= 2:
            T.add(w)
    U = set()
    for w in TERMS:
        others = [t for t in TERMS if t != w]
        D = C.copy()
        D.remove_node(w)
        if all(o in D for o in others) and nx.has_path(D, *others) and \
                nx.maximum_flow_value(D, *others, capacity='capacity') >= 2:
            U.add(w)
    return len(T), len(U)


def is_configuration(mult, nodes):
    """H + apex adjacent to x,y,z is planar.  Planarity ignores multiplicity,
    but a doubled edge must not be collapsed when testing, so subdivide one
    copy of each parallel class before the test."""
    G = nx.Graph()
    G.add_nodes_from(nodes)
    k = 0
    for (u, v), m in mult.items():
        G.add_edge(u, v)
        for _ in range(m - 1):
            k += 1
            G.add_edge(u, f'sub{k}')
            G.add_edge(f'sub{k}', v)
    G.add_node('apex')
    for t in TERMS:
        G.add_edge('apex', t)
    return nx.check_planarity(G, counterexample=False)[0]


def canon(mult, nodes):
    """Isomorphism key fixing the terminal set setwise, respecting multiplicity
    (a doubled edge is encoded by subdividing the extra copies)."""
    G = nx.Graph()
    for u in nodes:
        G.add_node(u, t=(1 if u in TERMS else 0))
    k = 0
    for (u, v), m in mult.items():
        G.add_edge(u, v)
        for _ in range(m - 1):
            k += 1
            G.add_node(f'sub{k}', t=2)
            G.add_edge(u, f'sub{k}')
            G.add_edge(f'sub{k}', v)
    return nx.weisfeiler_lehman_graph_hash(G, node_attr='t', iterations=6)


def configurations(pdf='bors.pdf'):
    v, E = X.extract(pdf)
    out = []
    for comp in X.components(v, E):
        terms = [i for i in comp if v[i][1] == 'T']
        inner = [i for i in comp if v[i][1] == 'I']
        # name the three terminals x, y, z left-to-right; the classification is
        # symmetric in them, so the choice only affects presentation
        terms.sort(key=lambda i: v[i][0][0])
        name = {i: t for i, t in zip(terms, TERMS)}
        for k, i in enumerate(sorted(inner, key=lambda i: v[i][0])):
            name[i] = f'a{k}'
        mult = collections.Counter()
        for (a, b), m in E.items():
            if a in name and b in name:
                mult[(name[a], name[b])] += m
        nodes = sorted(name.values())
        y = min(v[i][0][1] for i in comp)
        x = min(v[i][0][0] for i in comp)
        out.append(dict(pos=(y, x), nodes=nodes, mult=dict(mult),
                        cls=classify(mult, nodes),
                        planar=is_configuration(mult, nodes),
                        key=canon(mult, nodes)))
    out.sort(key=lambda c: c['pos'])
    return out


if __name__ == '__main__':
    C = configurations()
    print(f"configurations extracted: {len(C)}")
    print(f"all are (T,U)-configurations (H+apex planar): "
          f"{all(c['planar'] for c in C)}")
    dist = collections.Counter(c['cls'] for c in C)
    print("\n  (|T|,|U|)   count")
    for k in sorted(dist, reverse=True):
        print(f"  {str(k):>9} {dist[k]:>7}")
    print(f"  {'TOTAL':>9} {len(C):>7}")
    keys = collections.Counter(c['key'] for c in C)
    print(f"\ndistinct up to terminal-preserving isomorphism: {len(keys)}"
          f"  (repeats: {[n for n in keys.values() if n > 1]})")
    print("\nper configuration (reading order):")
    for i, c in enumerate(C, 1):
        e = ", ".join(f"{u}{v}" + (f"x{m}" if m > 1 else "")
                      for (u, v), m in sorted(c['mult'].items()))
        print(f"  {i:>2}. |T|,|U|={c['cls']}  internal={len(c['nodes'])-3}  {e}")

"""Emit the Figure 15.1 configuration artifact, with planarity certificates.

Produces figure_15_1_configurations.json: the 31 (T,U)-configurations of BORS
Figure 15.1 as explicit MULTIGRAPHS, each with its (|T|,|U|) class and a
rotation-system certificate witnessing that H + apex is planar.  The JSON is
checkable by verify_fig_15_1.py with no third-party library and without the
paper, which the extraction itself needs.
"""
import json

import networkx as nx

from classify_fig import configurations, TERMS


def simple_form(mult):
    """H with each extra parallel copy subdivided, so it is a simple graph.

    The subdivision vertices must be named in an order the verifier can
    reproduce without this code, so iterate the parallel classes sorted."""
    G = nx.Graph()
    k = 0
    for (u, v), m in sorted(
            (tuple(sorted(e)), m) for e, m in mult.items()):
        G.add_edge(u, v)
        for _ in range(m - 1):
            k += 1
            G.add_edge(u, f's{k}')
            G.add_edge(f's{k}', v)
    return G


def rotation_system(mult):
    """Cyclic neighbour order at each vertex of (subdivided H) + apex."""
    G = simple_form(mult)
    for t in TERMS:
        G.add_edge('apex', t)
    ok, emb = nx.check_planarity(G)
    assert ok
    rot = {}
    for v in emb:
        nbrs, first = [], None
        for w in emb[v]:
            first = w
            break
        w = first
        while True:
            nbrs.append(w)
            w = emb[v][w]['cw']
            if w == first:
                break
        rot[v] = nbrs
    return rot


def main():
    C = configurations()
    out = []
    for i, c in enumerate(C, 1):
        edges = []
        for (u, v), m in sorted(c['mult'].items()):
            edges += [[u, v]] * m
        out.append({
            'id': i,
            'group': {(3, 3): 'A', (3, 2): 'B', (2, 1): 'C',
                      (1, 0): 'D', (0, 0): 'E'}[c['cls']],
            'T': c['cls'][0], 'U': c['cls'][1],
            'terminals': list(TERMS),
            'internal': sorted(n for n in c['nodes'] if n not in TERMS),
            'edges': edges,
            'rotation_system': rotation_system(c['mult']),
        })
    doc = {
        'source': 'Bokal, Oporowski, Richter, Salazar, arXiv:1312.3712, '
                  'Figure 15.1 (page 151 of the v3 PDF)',
        'what': 'the 31 (T,U)-configurations admitted as replacement patches '
                'by Theorem 17.1(3)',
        'definition': 'Definition 15.21: T = {w in {x,y,z} : H has edge-'
                      'disjoint w-({x,y,z}-w) paths}; U = {w : H-w has edge-'
                      'disjoint paths joining the other two}; (H,{x,y,z}) is a '
                      '(T,U)-configuration when H plus an apex adjacent to '
                      'x, y, z is planar.',
        'multigraphs': 'The patches are MULTIGRAPHS. Figure 15.1 draws a '
                       'parallel pair as a closed lens (two arcs between the '
                       'same two vertices). Evaluating Definition 15.21 with '
                       'simple-graph edge connectivity, which ignores '
                       'multiplicity, misclassifies them; that is the error '
                       'this artifact corrects.',
        'method': 'Extracted from the PDF vector drawing operators, not from a '
                  'rendered image: white-filled circles are terminals, '
                  'black-filled circles internal vertices, stroked paths are '
                  'edges, and a closed path between two circles is a parallel '
                  'pair. See extract_fig.py.',
        'group_key': {'A': '(|T|,|U|) = (3,3), 20 configurations',
                      'B': '(3,2), 3', 'C': '(2,1), 5',
                      'D': '(1,0), 2', 'E': '(0,0), 1'},
        'configurations': out,
    }
    with open('figure_15_1_configurations.json', 'w') as f:
        json.dump(doc, f, indent=1, sort_keys=True)
    print('wrote figure_15_1_configurations.json with', len(out), 'configurations')


if __name__ == '__main__':
    main()

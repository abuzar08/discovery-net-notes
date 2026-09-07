r"""reviewer-1: my own extraction of BORS Figure 15.1, and my own Definition
15.21 classification, checked against h3028's published artifact.

Written from the PDF drawing operators directly (pymupdf), not from the lane's
extractor:

  * a white-filled disc is a terminal, a black-filled disc an internal vertex;
  * a stroked path whose ends snap to two discs is an edge;
  * a CLOSED stroked path between two discs is a lens, i.e. a parallel pair —
    the encoding detail h3028 says silently corrupts the reading.

Definition 15.21, implemented from the paper's text with capacities equal to
edge multiplicities:

  * \(w \in T\) iff there are edge-disjoint paths from \(w\) to each of the other
    two terminals (a flow of 2 into a super-sink fed by them, capacity 1 each);
  * \(w \in U\) iff the other two terminals are joined by two edge-disjoint paths
    in \(H - w\);
  * the configuration condition is planarity of \(H^{+}\), \(H\) plus an apex
    adjacent to \(x, y, z\).
"""
import collections
import itertools
import json
import math

import networkx as nx
import pymupdf

PDF, PAGE = 'bors.pdf', 150
SNAP = 4.0
ART = ('/Users/abuzark/.discovery-research-team/workspaces/reviewer-1/notes/'
       'topological-graph-theory/crossing-number-two-subgraph/'
       'figure_15_1_configurations.json')


def centre(g):
    r = g['rect']
    return ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)


def polyline(g):
    pts = []
    for it in g['items']:
        if it[0] == 'l':
            a, b = (it[1].x, it[1].y), (it[2].x, it[2].y)
        elif it[0] == 'c':
            a, b = (it[1].x, it[1].y), (it[4].x, it[4].y)
        elif it[0] == 're':
            r = it[1]
            a, b = (r.x0, r.y0), (r.x1, r.y1)
        elif it[0] == 'qu':
            q = it[1]
            for p in (q.ul, q.ur, q.lr, q.ll, q.ul):
                if not pts or math.dist(pts[-1], (p.x, p.y)) > 0.01:
                    pts.append((p.x, p.y))
            continue
        else:
            continue
        if not pts or math.dist(pts[-1], a) > 0.01:
            pts.append(a)
        pts.append(b)
    return pts


def extract():
    page = pymupdf.open(PDF)[PAGE]
    dr = page.get_drawings()
    discs, paths = [], []
    for g in dr:
        f = g.get('fill')
        if f == (1.0, 1.0, 1.0):
            discs.append((centre(g), 'terminal'))
        elif f == (0.0, 0.0, 0.0) and max(g['rect'].width,
                                          g['rect'].height) < 4:
            discs.append((centre(g), 'internal'))
        else:
            paths.append(g)

    def snap(p):
        best, bd = None, 1e9
        for i, (c, _) in enumerate(discs):
            d = math.dist(p, c)
            if d < bd:
                best, bd = i, d
        return best if bd <= SNAP else None

    edges = []
    for g in paths:
        if max(g['rect'].width, g['rect'].height) < 4:
            continue                       # a disc's own outline
        pts = polyline(g)
        if len(pts) < 2:
            continue
        hits = [snap(p) for p in pts]
        hits = [h for h in hits if h is not None]
        if not hits:
            continue
        closed = math.dist(pts[0], pts[-1]) < 0.01
        seq = []
        for h in hits:
            if not seq or seq[-1] != h:
                seq.append(h)
        if closed and len(seq) >= 2 and seq[0] != seq[-1]:
            seq.append(seq[0])             # a lens: walk it as a closed cycle
        for a, b in zip(seq, seq[1:]):
            if a != b:
                edges.append((a, b))
    return discs, edges


def components(discs, edges):
    G = nx.MultiGraph()
    G.add_nodes_from(range(len(discs)))
    G.add_edges_from(edges)
    out = []
    for comp in nx.connected_components(G):
        if len(comp) < 2:
            continue
        H = nx.MultiGraph(G.subgraph(comp))
        out.append(H)
    return out


# ------------------------------------------------- Definition 15.21, my own
def flow_graph(H, weights=True):
    F = nx.Graph()
    mult = collections.Counter()
    for u, v in H.edges():
        mult[(min(u, v), max(u, v))] += 1
    for (u, v), c in mult.items():
        F.add_edge(u, v, capacity=c)
    return F


def classify(H, terminals):
    F = flow_graph(H)
    T, U = set(), set()
    for w in terminals:
        others = [t for t in terminals if t != w]
        F2 = F.copy()
        F2.add_node('SINK')
        for o in others:
            F2.add_edge(o, 'SINK', capacity=1)
        if nx.maximum_flow_value(F2, w, 'SINK') >= 2:
            T.add(w)
        F3 = F.copy()
        F3.remove_node(w)
        if others[0] in F3 and others[1] in F3 and \
                nx.maximum_flow_value(F3, others[0], others[1]) >= 2:
            U.add(w)
    return len(T), len(U)


def apex_planar(H, terminals):
    S = nx.Graph()
    S.add_nodes_from(H.nodes())
    S.add_edges_from({(min(u, v), max(u, v)) for u, v in H.edges()})
    S.add_node('apex')
    for t in terminals:
        S.add_edge('apex', t)
    return nx.check_planarity(S, counterexample=False)[0]


def main():
    discs, edges = extract()
    nterm = sum(1 for _, k in discs if k == 'terminal')
    nint = sum(1 for _, k in discs if k == 'internal')
    print(f'page {PAGE}: {nterm} white discs (terminals), {nint} small black '
          f'discs, {len(edges)} edge instances')
    comps = components(discs, edges)
    print(f'   components with at least two vertices: {len(comps)}')
    classes = collections.Counter()
    sizes = collections.Counter()
    bad = []
    graphs = []
    for H in comps:
        terms = [v for v in H.nodes() if discs[v][1] == 'terminal']
        internal = [v for v in H.nodes() if discs[v][1] == 'internal']
        if len(terms) != 3:
            bad.append((len(terms), len(internal)))
            continue
        c = classify(H, terms)
        classes[c] += 1
        sizes[len(internal)] += 1
        graphs.append((H, terms, internal, c))
    print(f'   components with exactly three terminals: {len(graphs)}'
          + (f'; others {bad}' if bad else ''))
    print(f'   class distribution (|T|,|U|): {dict(sorted(classes.items()))}')
    print(f'   internal sizes: {dict(sorted(sizes.items()))}, max '
          f'{max(sizes) if sizes else 0}')
    npl = [c for H, t, i, c in graphs if not apex_planar(H, t)]
    print(f'   configurations failing the H+ planarity condition: {len(npl)}')

    # pairwise non-isomorphic, as multigraphs with terminal/internal roles
    def key(H, terms, internal):
        S = nx.MultiGraph()
        S.add_nodes_from(H.nodes())
        S.add_edges_from(H.edges())
        return S
    iso = 0
    for i in range(len(graphs)):
        for j in range(i + 1, len(graphs)):
            Hi, ti, ii, _ = graphs[i]
            Hj, tj, ij, _ = graphs[j]
            if Hi.number_of_nodes() != Hj.number_of_nodes():
                continue
            if sorted(d for _, d in Hi.degree()) != sorted(d for _, d in Hj.degree()):
                continue
            nm = lambda a, b: (discs[a['__i__']][1] if '__i__' in a else True)
            if nx.is_isomorphic(nx.Graph(Hi), nx.Graph(Hj)):
                # simple-graph isomorphism is necessary but not sufficient;
                # compare multiplicity multisets too
                mi = sorted(collections.Counter(
                    (min(u, v), max(u, v)) for u, v in Hi.edges()).values())
                mj = sorted(collections.Counter(
                    (min(u, v), max(u, v)) for u, v in Hj.edges()).values())
                if mi == mj:
                    iso += 1
    print(f'   pairs that are isomorphic as simple graphs with equal '
          f'multiplicity profiles: {iso}')

    art = json.load(open(ART))['configurations']
    acl = collections.Counter((c['T'], c['U']) for c in art)
    print(f'   published artifact: {len(art)} configurations, classes '
          f'{dict(sorted(acl.items()))}')


if __name__ == '__main__':
    main()


def simple_classification():
    """what the classification becomes if lenses are collapsed to single edges —
    the error h3018 corrected"""
    discs, edges = extract()
    comps = components(discs, edges)
    cl = collections.Counter()
    for H in comps:
        terms = [v for v in H.nodes() if discs[v][1] == 'terminal']
        if len(terms) != 3:
            continue
        S = nx.Graph()
        S.add_nodes_from(H.nodes())
        S.add_edges_from({(min(u, v), max(u, v)) for u, v in H.edges()})
        F = nx.Graph()
        for u, v in S.edges():
            F.add_edge(u, v, capacity=1)
        T = U = 0
        for w in terms:
            others = [t for t in terms if t != w]
            F2 = F.copy(); F2.add_node('SINK')
            for o in others:
                F2.add_edge(o, 'SINK', capacity=1)
            if nx.maximum_flow_value(F2, w, 'SINK') >= 2:
                T += 1
            F3 = F.copy(); F3.remove_node(w)
            if others[0] in F3 and others[1] in F3 and \
                    nx.maximum_flow_value(F3, others[0], others[1]) >= 2:
                U += 1
        cl[(T, U)] += 1
    return cl

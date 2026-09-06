r"""reviewer-1: exact crossing-number check for the census members, my own code.

For small graphs the predicates \(\mathrm{cr} \le 1\) and \(\mathrm{cr} \le 2\) are
decidable by planarisation: a drawing with \(k\) crossings becomes a planar graph
when each crossing is replaced by a new degree-4 vertex, so

  \(\mathrm{cr}(G) \le 1\) iff some pair of independent edges can be replaced by a
  crossing vertex leaving a planar graph, and
  \(\mathrm{cr}(G) \le 2\) iff some such replacement leaves a graph with
  \(\mathrm{cr} \le 1\).

Planarity itself is networkx's Boyer-Myrvold. This gives an exact verdict for
every graph of crossing number at most 2, and certifies \(\mathrm{cr} \ge 3\)
otherwise.

Checked here: every member of the census tagged CRIT2 has crossing number exactly
2, and the member tagged CRIT_GE3 (\(C_3 \square C_3\)) has crossing number at
least 3.

usage: python3 crcheck.py [census_dir]
"""
import sys, os, itertools
import networkx as nx


def planar(G):
    return nx.check_planarity(G, counterexample=False)[0]


def planarise(G, e, f):
    """replace the crossing of independent edges e, f by a new degree-4 vertex"""
    H = G.copy()
    H.remove_edge(*e)
    H.remove_edge(*f)
    w = max(H.nodes) + 1
    for x in (e[0], e[1], f[0], f[1]):
        H.add_edge(w, x)
    return H


def pairs(G):
    es = list(G.edges())
    for i in range(len(es)):
        for j in range(i + 1, len(es)):
            if not set(es[i]) & set(es[j]):          # independent edges
                yield es[i], es[j]


def cr_le_1(G):
    return planar(G) or any(planar(planarise(G, e, f)) for e, f in pairs(G))


def cr_le_2(G):
    if cr_le_1(G):
        return True
    return any(cr_le_1(planarise(G, e, f)) for e, f in pairs(G))


def crossing_number_upto_2(G):
    if planar(G):
        return 0
    if cr_le_1(G):
        return 1
    if cr_le_2(G):
        return 2
    return '>=3'


def read(path):
    out = []
    for line in open(path):
        p = line.split()
        if not p or not p[0].startswith('CRIT'):
            continue
        n, m = int(p[1]), int(p[2])
        E = [tuple(int(x) for x in e.split('-')) for e in p[3].strip(',').split(',') if e]
        G = nx.Graph(E)
        G.add_nodes_from(range(n))
        out.append((p[0], n, m, G))
    return out


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'target')
    tally = {}
    conn2 = []
    for n in range(6, 12):
        p = os.path.join(d, f'n{n}.txt')
        if not os.path.exists(p):
            continue
        for tag, nn, mm, G in read(p):
            cr = crossing_number_upto_2(G)
            k = nx.node_connectivity(G)
            tally[(tag, cr)] = tally.get((tag, cr), 0) + 1
            if k == 2:
                conn2.append((nn, mm, cr))
    print('crossing numbers by census tag (my own planarisation search):')
    for (tag, cr), c in sorted(tally.items(), key=lambda t: (t[0][0], str(t[0][1]))):
        print(f'   {tag:10s} cr = {cr}: {c} graphs')
    print()
    print(f'the {len(conn2)} members of vertex connectivity 2, as (n, m, cr):')
    print(f'   {conn2}')
    print(f'   all have crossing number 2: {all(c == 2 for _, _, c in conn2)}')


if __name__ == '__main__':
    main()

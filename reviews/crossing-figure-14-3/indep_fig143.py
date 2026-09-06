r"""reviewer-1: independent check of h3090's Figure 14.3 claims.

The drawn components come from the lane's own extractor (page 127 of the BORS
PDF); everything after that is my own code:

  * crossing numbers by exact planarisation search — a drawing with \(k\)
    crossings becomes planar when each crossing is replaced by a degree-4 vertex,
    so \(\mathrm{cr} \le 1\) and \(\mathrm{cr} \le 2\) are decidable, and a graph
    failing both has \(\mathrm{cr} \ge 3\);
  * 2-crossing-criticality: \(\mathrm{cr}(G) \ge 2\) and \(\mathrm{cr}(G-e) \le 1\)
    for every edge (enough here, since every component has minimum degree 3);
  * the identification search: for each component that is not 2-crossing-critical
    as drawn, the least \(k \le 3\) for which identifying \(k\) vertex pairs yields
    a 2-crossing-critical graph, then the verdicts of every identification of that
    many pairs which yields one.

usage: python3 indep_fig143.py [kmax]
"""
import sys, itertools
import networkx as nx
import extract_fig as X


# ------------------------------------------------------- crossing numbers
def planar(G):
    return nx.check_planarity(G, counterexample=False)[0]


def planarise(G, e, f):
    H = G.copy()
    H.remove_edge(*e)
    H.remove_edge(*f)
    w = max(H.nodes) + 1
    for x in (e[0], e[1], f[0], f[1]):
        H.add_edge(w, x)
    return H


def indep_pairs(G):
    es = list(G.edges())
    for i in range(len(es)):
        for j in range(i + 1, len(es)):
            if not set(es[i]) & set(es[j]):
                yield es[i], es[j]


def cr_le_1(G):
    return planar(G) or any(planar(planarise(G, e, f)) for e, f in indep_pairs(G))


def cr_le_2(G):
    return cr_le_1(G) or any(cr_le_1(planarise(G, e, f)) for e, f in indep_pairs(G))


def verdict(G):
    """CRIT2, CRIT_GE3 or None, by my own tests"""
    if cr_le_1(G):
        return None                      # cr <= 1, not 2-crossing-critical
    for e in list(G.edges()):
        H = G.copy()
        H.remove_edge(*e)
        if not cr_le_1(H):
            return None                  # some edge deletion keeps cr >= 2
    return 'CRIT2' if cr_le_2(G) else 'CRIT_GE3'


# ----------------------------------------------------------- the figure
def drawn_components(page=127):
    v, E = X.extract('bors.pdf', page)
    out = []
    for c in [c for c in X.components(v, E) if len(c) >= 5]:
        idx = {u: i for i, u in enumerate(sorted(c))}
        G = nx.Graph()
        G.add_nodes_from(range(len(c)))
        for (a, b), m in E.items():
            if a in idx and b in idx:
                G.add_edge(idx[a], idx[b])
        out.append(G)
    return out


def identify(G, pairs):
    H = nx.Graph(G)
    for u, w in pairs:
        if u in H and w in H and u != w:
            H = nx.contracted_nodes(H, u, w, self_loops=False)
    return nx.convert_node_labels_to_integers(H)


def main():
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    gs = drawn_components()
    print(f'{len(gs)} drawn components on page 127')
    good = [G for G in gs if verdict(G) == 'CRIT2']
    ge3 = [G for G in gs if verdict(G) == 'CRIT_GE3']
    bad = [G for G in gs if verdict(G) is None]
    print(f'  2-crossing-critical as drawn with cr = 2 : {len(good)}')
    print(f'  2-crossing-critical as drawn with cr >= 3: {len(ge3)}')
    print(f'  not 2-crossing-critical as drawn          : {len(bad)}   '
          f'(n,m) {sorted((G.number_of_nodes(), G.number_of_edges()) for G in bad)}')
    print()
    settled, total_graphs, unresolved = 0, 0, []
    for G in bad:
        n = G.number_of_nodes()
        hit = None
        for k in range(1, kmax + 1):
            res = []
            for pairs in itertools.combinations(itertools.combinations(range(n), 2), k):
                H = identify(G, pairs)
                if H.number_of_nodes() < 5:
                    continue
                v = verdict(H)
                if v is not None:
                    res.append(v)
            if res:
                hit = (k, res)
                break
        if hit is None:
            unresolved.append((n, G.number_of_edges()))
            print(f'  component (n,m) = ({n},{G.number_of_edges()}): no identification of '
                  f'<= {kmax} pairs is 2-crossing-critical')
        else:
            k, res = hit
            settled += 1
            total_graphs += len(res)
            kinds = sorted(set(res))
            print(f'  component (n,m) = ({n},{G.number_of_edges()}): least k = {k}, '
                  f'{len(res)} identifications give a 2-crossing-critical graph, verdicts {kinds}')
    print()
    print(f'settled components: {settled} of {len(bad)}; total identified graphs: {total_graphs}; '
          f'all CRIT2: see verdicts above; unresolved: {unresolved}')


if __name__ == '__main__':
    main()

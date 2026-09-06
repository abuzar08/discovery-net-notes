r"""reviewer-1: the class of 15 that h3080 says reduce to a base with
\(\mathrm{cr}(L) = 1\) — the one class my first review left unverified.

BORS Lemma 15.9 and Definition 15.17 give the move: in a 3-connected graph, take
a 3-cut \(S\) and a non-trivial planar \(S\)-bridge \(B\) whose nucleus
\(\mathrm{Nuc}(B) = B - S\) has at least two vertices, and contract that nucleus;
the sequence is a *planar* 3-reduction sequence when each \(B^{+}\) is planar.
The superscript notation does not survive text extraction from the PDF, so I run
the search under two readings and report both:

    reading (a)  B itself is planar;
    reading (b)  B together with the triangle on its three attachments is planar.

Reading (b) is the stronger requirement, so it is the conservative one. For each
of the 15 graphs the search explores every reachable terminal graph (no move
applicable), and for each terminal reports whether it is peripherally
4-connected and its crossing number, decided exactly by my planarisation search.

usage: python3 indep_reduce.py
"""
import itertools, os, collections
import networkx as nx
import indep_class as I
from p4c_fix import p4c


# ------------------------------------------------------------ crossing number
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


def cr_upto2(G):
    if planar(G):
        return 0
    if cr_le_1(G):
        return 1
    return 2 if cr_le_2(G) else '>=3'


# ------------------------------------------------------------- the reduction
def moves(G, strict):
    """all graphs obtained by one planar 3-reduction"""
    out = []
    for S in itertools.combinations(sorted(G.nodes), 3):
        H = G.copy()
        H.remove_nodes_from(S)
        comps = list(nx.connected_components(H))
        if len(comps) < 2:
            continue
        for C in comps:
            if len(C) < 2:                      # Nuc(B) needs at least two vertices
                continue
            B = G.subgraph(set(C) | set(S)).copy()
            B.remove_edges_from([e for e in G.subgraph(S).edges()])   # bridge carries no S-edges
            test = B.copy()
            if strict:                          # reading (b): add the triangle on S
                test.add_edges_from(itertools.combinations(S, 2))
            if not planar(test):
                continue
            K = G.copy()
            keep = sorted(C)
            for v in keep[1:]:
                K = nx.contracted_nodes(K, keep[0], v, self_loops=False)
            K = nx.convert_node_labels_to_integers(K)
            if nx.node_connectivity(K) >= 3:    # 3-connectivity is preserved
                out.append(K)
    return out


def terminals(G, strict, cap=4000):
    seen, out, stack = [], [], [G]
    while stack and len(seen) < cap:
        cur = stack.pop()
        if any(nx.is_isomorphic(cur, s) for s in seen):
            continue
        seen.append(cur)
        nxt = moves(cur, strict)
        if not nxt:
            if not any(nx.is_isomorphic(cur, t) for t in out):
                out.append(cur)
        else:
            stack.extend(nxt)
    return out


def main():
    d = os.path.dirname(os.path.abspath(__file__))
    cen = I.read_census(d)
    three = [(n, m, G) for t, n, m, G in cen if nx.node_connectivity(G) >= 3]
    V8, V10 = I.moebius_ladder(8), I.moebius_ladder(10)
    hasV = lambda G: I.has_subdivision(G, V8) or I.has_subdivision(G, V10)
    T = I.theorem_15_6_graphs()
    fifteen = [(n, m, G) for n, m, G in three
               if not (p4c(G) and n <= 10) and not hasV(G)
               and not any(nx.is_isomorphic(G, H) for H in T)]
    print(f'the class of {len(fifteen)}: (n,m) {sorted((n, m) for n, m, _ in fifteen)}')
    K33 = nx.complete_bipartite_graph(3, 3)
    for strict in (True, False):
        print(f'\nreading ({"b" if strict else "a"}): '
              f'{"B plus the triangle on its attachments" if strict else "B itself"} must be planar')
        ok = k33 = 0
        for n, m, G in fifteen:
            ts = terminals(G, strict)
            crs = [cr_upto2(L) for L in ts]
            p4cs = [p4c(L) for L in ts]
            iso33 = any(nx.is_isomorphic(L, K33) for L in ts)
            good = ts and all(c == 1 for c in crs) and all(p4cs)
            ok += bool(good)
            k33 += bool(iso33)
            print(f'   ({n},{m}): {len(ts)} terminal graph(s), '
                  f'(n,m,cr,p4c) {[(L.number_of_nodes(), L.number_of_edges(), c, p) for L, c, p in zip(ts, crs, p4cs)]}'
                  f'{"  <- K_{3,3}" if iso33 else ""}')
        print(f'   graphs whose every terminal is peripherally 4-connected with cr = 1: {ok} of {len(fifteen)}; '
              f'reducing to K_{{3,3}}: {k33}')


if __name__ == '__main__':
    main()

"""Cross-check the headline's figure readings against the exhaustive census.

The headline rests on reading three figures of BORS.  Every graph read off them
that has at most eleven vertices must appear in my independent exhaustive census
of 2-crossing-critical graphs, which was generated without reference to the
paper.  That is a necessary condition the readings either meet or fail.
"""
import collections
import itertools
import json
import os

import networkx as nx

import construct as C
import expand_run as R
import extract_fig as X
from fig143 import drawn_components, verdict, identify
from fig143b import matchings


def census():
    out = []
    for n in range(6, 12):
        f = os.path.join(R.REPO, f'n{n}.txt')
        if not os.path.exists(f):
            continue
        for line in open(f):
            p = line.split()
            if len(p) < 4:
                continue
            E = [tuple(map(int, x.split('-')))
                 for x in p[3].strip(',').split(',') if x]
            out.append(nx.Graph(E))
    return out


def fig141():
    v, E = X.extract('bors.pdf', 125)
    out = []
    for c in [c for c in X.components(v, E) if len(c) >= 4]:
        idx = {u: i for i, u in enumerate(sorted(c))}
        G = nx.Graph()
        G.add_nodes_from(range(len(c)))
        for (a, b), m in E.items():
            if a in idx and b in idx:
                G.add_edge(idx[a], idx[b])
        if verdict(G):
            out.append(G)
    K5, K33 = nx.complete_graph(5), nx.complete_bipartite_graph(3, 3)
    out += [nx.disjoint_union(K5, K5), nx.disjoint_union(K5, K33),
            nx.disjoint_union(K33, K33)]
    return out


def fig142_143():
    gs = drawn_components()
    out = []
    for G in gs:
        if verdict(G):
            out.append(G)
            continue
        done = False
        for k in (1, 2, 3, 4):
            cands = []
            for P in matchings(sorted(G.nodes()), k):
                if len(P) != k:
                    continue
                H = identify(G, P)
                if H.number_of_nodes() < 5:
                    continue
                if min((d for _, d in H.degree()), default=0) < 3:
                    continue
                cands.append(H)
            for H in cands:
                if verdict(H):
                    out.append(H)
                    done = True
                    break
            if done:
                break
    return out


if __name__ == '__main__':
    Cn = census()
    print(f"census members (2-crossing-critical, n <= 11): {len(Cn)}")
    n3 = [g for g in Cn if nx.node_connectivity(g) < 3]
    print(f"  of which NOT 3-connected: {len(n3)}")
    for name, gs in (('Figure 14.1', fig141()), ('Figures 14.2/14.3', fig142_143())):
        small = [g for g in gs if g.number_of_nodes() <= 11]
        hit = sum(1 for g in small if any(nx.is_isomorphic(g, c) for c in Cn))
        print(f"\n{name}: {len(gs)} graphs read, {len(small)} with n <= 11")
        print(f"   of those, found in the census: {hit}/{len(small)}"
              + ("   <-- all present" if hit == len(small) else "   <-- MISMATCH"))
        conn = collections.Counter(nx.node_connectivity(g) for g in small)
        print(f"   connectivity of those: {dict(sorted(conn.items()))}")

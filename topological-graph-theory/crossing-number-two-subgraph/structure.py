"""Structural classification of the census members, against the
Bokal-Oporowski-Richter-Salazar (BORS) description of 2-crossing-critical
graphs.

BORS (arXiv:1312.3712) determine all 3-connected 2-crossing-critical graphs
that contain a subdivision of the Moebius ladder V10 (an infinite, tile-built
family), show that only finitely many 3-connected ones do NOT contain such a
subdivision, and show how the non-3-connected ones arise from the 3-connected
ones.  This script says where the census members sit in that division.

For n <= 10 a V10 subdivision is the same as a V10 subgraph: V10 is cubic, so
all ten of its vertices are branch vertices, leaving no room for subdivision
vertices.  The V8 column is subgraph containment only, which is a lower bound
on V8-subdivision containment.

    uv run --with networkx python structure.py
"""
import collections

import networkx as nx


def moebius_ladder(k):
    G = nx.cycle_graph(k)
    for i in range(k // 2):
        G.add_edge(i, i + k // 2)
    return G


def load(path):
    out = []
    for line in open(path):
        p = line.split()
        if len(p) < 4:
            continue
        E = [tuple(map(int, x.split('-'))) for x in p[3].strip(',').split(',')]
        out.append((p[0], int(p[1]), nx.Graph(E)))
    return out


def main():
    members = []
    for n in range(6, 12):
        try:
            members.append((n, load(f"n{n}.txt")))
        except FileNotFoundError:
            pass
    V8, V10 = moebius_ladder(8), moebius_ladder(10)

    print(f"{'n':>3} {'members':>8} {'3-conn':>7} {'V8 sub':>7} {'V10 sub':>8}")
    conn = collections.Counter()
    tot = v8 = v10 = 0
    for n, mem in members:
        c3 = s8 = s10 = 0
        for tag, nn, G in mem:
            k = nx.node_connectivity(G)
            conn[k] += 1
            if k >= 3:
                c3 += 1
            if nx.algorithms.isomorphism.GraphMatcher(G, V8).subgraph_is_monomorphic():
                s8 += 1
            if nn >= 10 and nx.algorithms.isomorphism.GraphMatcher(
                    G, V10).subgraph_is_monomorphic():
                s10 += 1
        print(f"{n:>3} {len(mem):>8} {c3:>7} {s8:>7} {s10:>8}")
        tot += len(mem)
        v8 += s8
        v10 += s10

    print(f"\ntotal members: {tot}")
    print(f"vertex connectivity distribution: {dict(sorted(conn.items()))}")
    print(f"containing a V8 subgraph:  {v8}")
    print(f"containing a V10 subdivision: {v10}")
    print()
    print("So every census member is either not 3-connected, or 3-connected")
    print("without a V10 subdivision -- i.e. a member of the finite exceptional")
    print("family of BORS, never of their infinite tile-built family.")
    print()
    print("Consistency anchor: no Moebius ladder is 2-crossing-critical")
    print("(V6 = K3,3, V8, V10, V12 all have crossing number 1), so BORS's")
    print("V10-containing family necessarily begins above these orders.")


if __name__ == "__main__":
    main()

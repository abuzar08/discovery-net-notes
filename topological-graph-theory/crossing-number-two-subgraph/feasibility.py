"""Measured feasibility of completing BORS Remark 17.2's program.

BORS Theorem 17.1(3): every 3-connected 2-crossing-critical graph with no V10
subdivision that is not V8-containing and not one of the four graphs of
Theorem 15.6 is obtained from a 2-crossing-critical peripherally-4-connected
graph on at most ten vertices by replacing each degree-3 vertex with one of at
most twenty patches, each on at most six vertices.

The 36 seeds are known (seeds.py).  This script measures what it would cost to
carry the expansion out and test each result for 2-crossing-criticality.

Method: build expansions with a representative patch set, run the exact
criticality + cr<=2 decision on them, and time it.  The patch set here is NOT
BORS's (their twenty patches are given in figures); it is a set of 3-terminal
graphs of the right ORDERS, which is what the cost depends on.  The timing is a
measurement on actual expanded graphs, not an extrapolation from counts.
"""
import itertools
import random
import subprocess
import sys
import time

import networkx as nx

NAUTY = "tools/nauty2_9_1"


# ------------------------------------------------------- patches and expansion

def patch_set():
    """Representative 3-terminal graphs on at most six vertices, spanning the
    order range 1..6 that Theorem 17.1(3) allows."""
    P = []
    # order 1: the trivial patch (leave the vertex alone)
    g = nx.Graph(); g.add_node(0); P.append((g, (0, 0, 0)))
    # order 3: triangle, and path
    g = nx.cycle_graph(3); P.append((g, (0, 1, 2)))
    g = nx.path_graph(3); P.append((g, (0, 1, 2)))
    # order 4: claw, K4, cycle+chord
    g = nx.star_graph(3); P.append((g, (1, 2, 3)))
    g = nx.complete_graph(4); P.append((g, (0, 1, 2)))
    g = nx.cycle_graph(4); g.add_edge(0, 2); P.append((g, (0, 1, 3)))
    # order 5: C5, K5 minus a perfect-ish matching, wheel
    g = nx.cycle_graph(5); P.append((g, (0, 2, 3)))
    g = nx.wheel_graph(5); P.append((g, (1, 2, 3)))
    g = nx.complete_graph(5); g.remove_edge(0, 1); P.append((g, (0, 1, 2)))
    # order 6: prism, K_{3,3}, octahedron, C6
    g = nx.circular_ladder_graph(3); P.append((g, (0, 1, 2)))
    g = nx.complete_bipartite_graph(3, 3); P.append((g, (0, 1, 2)))
    g = nx.complete_multipartite_graph(2, 2, 2); P.append((g, (0, 2, 4)))
    g = nx.cycle_graph(6); P.append((g, (0, 2, 4)))
    return P


def expand(G, assignment, patches):
    """Replace each degree-3 vertex v of G by patches[assignment[v]]."""
    H = nx.Graph()
    H.add_edges_from(G.edges())
    nxt = max(G.nodes()) + 1
    for v, pi in assignment.items():
        P, terms = patches[pi]
        if P.number_of_nodes() == 1:
            continue                                # trivial patch
        nbrs = list(H[v])
        relab = {x: nxt + i for i, x in enumerate(P.nodes())}
        nxt += P.number_of_nodes()
        H.remove_node(v)
        H.add_edges_from((relab[a], relab[b]) for a, b in P.edges())
        for w, t in zip(nbrs, terms):
            H.add_edge(w, relab[t])
    return H


def to_g6(G):
    G = nx.convert_node_labels_to_integers(G)
    n = G.number_of_nodes()
    bits = []
    for j in range(1, n):
        for i in range(j):
            bits.append(1 if G.has_edge(i, j) else 0)
    s = chr(n + 63)
    for k in range(0, len(bits), 6):
        c = bits[k:k + 6] + [0] * (6 - len(bits[k:k + 6]))
        s += chr(63 + sum(b << (5 - t) for t, b in enumerate(c)))
    return s


# ------------------------------------------------------------------ measure

def load_seeds(path="."):
    import os
    sys.path.insert(0, path)
    out = []
    for n in range(6, 11):
        f = os.path.join(path, f"n{n}.txt")
        if not os.path.exists(f):
            continue
        for line in open(f):
            p = line.split()
            if len(p) < 4:
                continue
            E = [tuple(map(int, x.split('-')))
                 for x in p[3].strip(',').split(',')]
            out.append((int(p[1]), nx.Graph(E)))
    return out


def measure(seed_G, patches, nsample, tag, crit2):
    d3 = [v for v, d in seed_G.degree() if d == 3]
    random.seed(12345)
    graphs = []
    for _ in range(nsample):
        a = {v: random.randrange(len(patches)) for v in d3}
        graphs.append(expand(seed_G, a, patches))
    # bucket by edge count and time crit2 on each bucket
    buckets = {}
    for H in graphs:
        buckets.setdefault(H.number_of_edges() // 10 * 10, []).append(H)
    print(f"\n  {tag}: seed n={seed_G.number_of_nodes()} "
          f"m={seed_G.number_of_edges()} degree-3 vertices={len(d3)}")
    print(f"    {'m bucket':>9} {'count':>6} {'mean n':>7} {'sec/graph':>11} "
          f"{'graphs/core-hr':>15}")
    for b in sorted(buckets):
        L = buckets[b]
        over = [H for H in L if H.number_of_edges() >= 63]
        usable = [H for H in L if H.number_of_edges() < 63]
        meann = sum(H.number_of_nodes() for H in L) / len(L)
        if not usable:
            print(f"    {b:>9} {len(L):>6} {meann:>7.1f} "
                  f"{'--':>11} {'crit2 cannot represent (>=63 edges)':>15}")
            continue
        g6 = "\n".join(to_g6(H) for H in usable) + "\n"
        t0 = time.time()
        subprocess.run([f"{crit2}"], input=g6, text=True,
                       capture_output=True)
        dt = time.time() - t0
        per = dt / len(usable)
        print(f"    {b:>9} {len(usable):>6} {meann:>7.1f} {per:>11.5f} "
              f"{3600/per:>15,.0f}"
              + (f"   [{len(over)} of {len(L)} exceed crit2's 62-edge limit]"
                 if over else ""))
    return


if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    crit2 = sys.argv[2]
    patches = patch_set()
    print(f"patch set: {len(patches)} representative 3-terminal graphs, "
          f"orders {sorted({p.number_of_nodes() for p, _ in patches})}")
    sys.path.insert(0, base)
    from seeds import peripherally_4_connected
    mem = load_seeds(base)
    seeds = [(n, G) for n, G in mem if peripherally_4_connected(G)]
    bydeg = {}
    for n, G in seeds:
        bydeg.setdefault(sum(1 for _, d in G.degree() if d == 3), []).append(G)
    for d in sorted(bydeg):
        if d in (2, 5, 8, 10):
            measure(bydeg[d][0], patches, 200, f"seed with {d} degree-3 vertices",
                    crit2)

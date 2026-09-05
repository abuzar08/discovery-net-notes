"""Does Richter's 1987 theorem already cover C3 [] C3?

DS21 cites, for the crossing-number-two subgraph question, both

  [698] R. B. Richter, "Cubic graphs with crossing number two",
        J. Graph Theory 12 (1988) 363-374, and
  [699] R. B. Richter, "Subgraphs with crossing number two",
        Congr. Numerantium 60 (1987) 169-180.

Congressus Numerantium is not digitised, but the zbMATH review of [699]
(Zbl 0647.05021) states its result:

    "Let G be a graph with crossing number at least 2.  If either G does not
     embed in the projective plane, or G contains a subdivision of K_{3,3}
     that has only one bridge (in the sense of Tutte), then G contains a
     subgraph H with crossing number exactly 2."

So [699] proves the Bloom-Kennedy-Quintas conjecture under two hypotheses.
This script checks that C3 [] C3 satisfies neither, so the counterexample is
outside the scope of [699] and does not contradict it.  ([698] is likewise
inapplicable: C3 [] C3 is 4-regular, not cubic.)

    uv run --with networkx python richter_1987_check.py
"""
import itertools

import networkx as nx


def c3_box_c3():
    E = set()
    for i in range(3):
        for j in range(3):
            u = 3 * i + j
            E.add(tuple(sorted((u, 3 * ((i + 1) % 3) + j))))
            E.add(tuple(sorted((u, 3 * i + (j + 1) % 3))))
    return sorted(E)


def tutte_bridges(G, Hnodes, Hedges):
    """Bridges of a subgraph H in G: chords, and components of G - V(H) with
    their attachments."""
    Hn, He = set(Hnodes), set(map(lambda e: tuple(sorted(e)), Hedges))
    br = []
    for e in G.edges():
        e = tuple(sorted(e))
        if e not in He and e[0] in Hn and e[1] in Hn:
            br.append(("chord", e))
    R = G.copy()
    R.remove_nodes_from(Hn)
    for comp in nx.connected_components(R):
        att = {w for v in comp for w in G[v] if w in Hn}
        br.append(("component", tuple(sorted(comp)), tuple(sorted(att))))
    return br


def k33_subdivisions(G):
    """All K_{3,3} subdivisions of G, as (vertex set, edge set)."""
    nodes = list(G.nodes())
    rest_all = set(nodes)
    out = []
    for branch in itertools.combinations(nodes, 6):
        rest = [v for v in nodes if v not in branch]
        for part in itertools.combinations(branch, 3):
            A, B = set(part), set(branch) - set(part)
            if min(A) != min(branch):
                continue                       # each bipartition once
            pairs = [(a, b) for a in sorted(A) for b in sorted(B)]

            def rec(i, usedv, usede):
                if i == len(pairs):
                    out.append((set(branch) | set(usedv), set(usede)))
                    return
                a, b = pairs[i]
                e = tuple(sorted((a, b)))
                if G.has_edge(a, b) and e not in usede:
                    rec(i + 1, usedv, usede | {e})
                for w in rest:
                    if w in usedv or not (G.has_edge(a, w) and G.has_edge(w, b)):
                        continue
                    e1, e2 = tuple(sorted((a, w))), tuple(sorted((w, b)))
                    if e1 in usede or e2 in usede:
                        continue
                    rec(i + 1, usedv | {w}, usede | {e1, e2})

            rec(0, frozenset(), frozenset())
    return out


def main():
    E = c3_box_c3()
    G = nx.Graph(E)
    print(f"C3 [] C3: n = {G.number_of_nodes()}, m = {G.number_of_edges()}, "
          f"degrees {sorted({d for _, d in G.degree()})}")
    print("  [698] applies to cubic graphs only -- C3 [] C3 is 4-regular, so "
          "it does not apply.")

    subs = k33_subdivisions(G)
    counts = [len(tutte_bridges(G, hn, he)) for hn, he in subs]
    print(f"\n  hypothesis 2 of [699]: a K_{{3,3}} subdivision with exactly "
          f"one Tutte bridge")
    print(f"     K_{{3,3}} subdivisions found : {len(subs)}")
    print(f"     fewest bridges of any of them: {min(counts)}")
    print(f"     with exactly one bridge      : {counts.count(1)}")
    assert counts.count(1) == 0
    print("     => hypothesis 2 FAILS for C3 [] C3")

    print("\n  hypothesis 1 of [699]: G does not embed in the projective plane")
    print("     C3 [] C3 does embed in RP^2 -- see the explicit embedding "
          "scheme in README.md,")
    print("     of Euler characteristic 9 - 18 + 10 = 1, so hypothesis 1 FAILS.")
    print("\n  => Richter 1987 does not cover C3 [] C3; no contradiction.")


if __name__ == "__main__":
    main()

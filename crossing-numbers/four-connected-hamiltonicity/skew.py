"""Cheap necessary condition: skewness <= 3.

Every crossing in a drawing can be removed by deleting one of the two edges
involved, so  skewness(G) <= cr(G).  Hence

    skewness(G) > 3   =>   cr(G) > 3,

and a graph failing this is not a counterexample, established by at most
C(m,3) planarity tests rather than by exhausting a depth-3 crossing search.
This is a NECESSARY condition only: skewness <= 3 does not imply cr <= 3, so
anything surviving still goes to the exact decider.
"""
import sys, itertools, networkx as nx

def planar(G): return nx.check_planarity(G, counterexample=False)[0]

def skew_le(G, k):
    E = list(G.edges())
    for r in range(k + 1):
        for S in itertools.combinations(E, r):
            H = G.copy(); H.remove_edges_from(S)
            if planar(H):
                return True
    return False

if __name__ == "__main__":
    # validation: cr(K5)=1 so skewness(K5)=1; K6 has cr 3, skewness 2.
    # skewness(K6) = 3, not 2: K6 has 15 edges against a planar maximum of 12,
    # and K6 minus a perfect matching is the octahedron K_{2,2,2}, which is
    # planar.  My first expectation here was wrong and the check caught it.
    for nm, G, k, want in [("K5", nx.complete_graph(5), 1, True),
                           ("K5", nx.complete_graph(5), 0, False),
                           ("K6", nx.complete_graph(6), 3, True),
                           ("K6", nx.complete_graph(6), 2, False),
                           ("K3,3", nx.complete_bipartite_graph(3,3), 1, True),
                           ("K3,3", nx.complete_bipartite_graph(3,3), 0, False)]:
        got = skew_le(G, k)
        print(f"  validate skewness({nm}) <= {k}: {got}, expected {want}  "
              f"{'OK' if got == want else 'FAIL'}", flush=True)
        if got != want: sys.exit("skewness test failed validation")
    print(flush=True)
    surv = []
    for i, line in enumerate(open(sys.argv[1])):
        line = line.strip()
        if not line: continue
        G = nx.from_graph6_bytes(line.encode())
        ok = skew_le(G, 3)
        if ok: surv.append(line)
        print(f"[{i+1:>3}] {line}  |E|={G.number_of_edges()}  skewness<=3? {ok}"
              + ("   -> goes to the exact decider" if ok else "   -> cr > 3, excluded"),
              flush=True)
    print(f"\ntested {i+1}; survivors needing the exact test: {len(surv)}")
    for s in surv: print(s)

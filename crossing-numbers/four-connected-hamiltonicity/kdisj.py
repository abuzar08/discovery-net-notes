"""Fast exclusion: four edge-disjoint Kuratowski subdivisions force cr > 3.

If G contains k pairwise edge-disjoint subdivisions of K5 or K_{3,3}, then any
set of edges whose deletion planarises G must contain at least one edge from
each, so skewness(G) >= k, and since skewness <= cr we get cr(G) >= k.

Taking k = 4: exhibiting four edge-disjoint Kuratowski subdivisions proves
cr(G) > 3, at the cost of four planarity tests rather than the C(m,3) tests the
skewness search needs.

The extraction is GREEDY, so it is one-sided: finding four proves cr > 3, but
failing to find four proves nothing, and those graphs fall through to the full
skewness test.  A greedy failure is not a certificate.
"""
import sys, networkx as nx

def disjoint_kuratowski(G, want=4):
    """Greedily peel edge-disjoint Kuratowski subdivisions; return how many."""
    H = G.copy()
    found = 0
    while found < want:
        ok, K = nx.check_planarity(H, counterexample=True)
        if ok:
            break
        H.remove_edges_from(list(K.edges()))
        found += 1
    return found

if __name__ == "__main__":
    # Validation.  cr(K5) = 1 and K5 has only one Kuratowski subdivision to peel;
    # cr(K6) = 3; cr(K7) = 9 so K7 should yield at least 4.
    for nm, G, atleast in [("K5", nx.complete_graph(5), 1),
                           ("K7", nx.complete_graph(7), 4),
                           ("K8", nx.complete_graph(8), 4),
                           ("K3,3", nx.complete_bipartite_graph(3,3), 1)]:
        f = disjoint_kuratowski(G, 4)
        ok = f >= min(atleast, 4)
        print(f"  validate {nm}: found {f} edge-disjoint Kuratowski subdivisions, "
              f"need >= {min(atleast,4)}  {'OK' if ok else 'FAIL'}", flush=True)
        if not ok: sys.exit("filter failed validation")
    # A planar graph must yield none.
    f = disjoint_kuratowski(nx.cycle_graph(9), 4)
    print(f"  validate C9 (planar): found {f}, expected 0  "
          f"{'OK' if f == 0 else 'FAIL'}\n", flush=True)
    if f != 0: sys.exit("filter failed validation")

    import time
    excluded = fell_through = 0
    t0 = time.time()
    for line in open(sys.argv[1]):
        line = line.strip()
        if not line: continue
        G = nx.from_graph6_bytes(line.encode())
        if disjoint_kuratowski(G, 4) >= 4:
            excluded += 1
        else:
            fell_through += 1
            print("FALLTHROUGH", line, flush=True)
    el = time.time() - t0
    n = excluded + fell_through
    print(f"\n{n} graphs in {el:.1f}s = {n/el:,.0f}/sec")
    print(f"excluded by four disjoint Kuratowski subdivisions: {excluded}")
    print(f"fell through to the full skewness test: {fell_through}")

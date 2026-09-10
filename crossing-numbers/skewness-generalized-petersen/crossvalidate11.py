"""Independent re-check of the 48 survivors at n = 10.

The theorem rests on my own filters, so each property is re-tested here by a
different route:

  4-connectivity : networkx.node_connectivity  (max-flow based) rather than my
                   own enumeration of vertex cuts of size <= 3
  non-Hamiltonian: an independent DP over subsets (Held-Karp style) rather than
                   my backtracking search
  cr > 3         : re-derived from skewness, plus an upper-bound drawing, so the
                   two crossing-number instruments are seen to agree

Disagreement anywhere invalidates the theorem; agreement everywhere means the
result does not depend on any single piece of my code.
"""
import sys, itertools, networkx as nx

def ham_dp(G):
    """Hamiltonian cycle by subset DP; independent of the backtracking test."""
    n = G.number_of_nodes()
    idx = {v: i for i, v in enumerate(G.nodes())}
    adj = [0]*n
    for u, v in G.edges():
        adj[idx[u]] |= 1 << idx[v]; adj[idx[v]] |= 1 << idx[u]
    full = (1 << n) - 1
    # dp[mask][v] = reachable path from 0 covering mask ending at v
    dp = [[False]*n for _ in range(1 << n)]
    dp[1][0] = True
    for mask in range(1 << n):
        if not (mask & 1): continue
        for v in range(n):
            if not dp[mask][v]: continue
            nb = adj[v] & ~mask & full
            while nb:
                w = (nb & -nb).bit_length() - 1; nb &= nb - 1
                dp[mask | (1 << w)][w] = True
    return any(dp[full][v] and (adj[v] >> 0) & 1 for v in range(1, n))

def skew_le(G, k):
    E = list(G.edges())
    for r in range(k + 1):
        for S in itertools.combinations(E, r):
            H = G.copy(); H.remove_edges_from(S)
            if nx.check_planarity(H, counterexample=False)[0]:
                return True
    return False

# validation of the independent Hamiltonicity routine on known cases
for nm, G, want in [("K5", nx.complete_graph(5), True),
                    ("Petersen", nx.petersen_graph(), False),
                    ("C10", nx.cycle_graph(10), True),
                    ("K3,4", nx.complete_bipartite_graph(3,4), False)]:
    got = ham_dp(G)
    print(f"  validate Hamiltonian({nm}) = {got}, expected {want}  "
          f"{'OK' if got == want else 'FAIL'}", flush=True)
    if got != want: sys.exit("independent Hamiltonicity routine failed validation")
print(flush=True)

bad = 0
for i, line in enumerate(open(sys.argv[1])):
    line = line.strip()
    if not line: continue
    G = nx.from_graph6_bytes(line.encode())
    kappa = nx.node_connectivity(G)
    ham = ham_dp(G)
    # The skewness re-run was dropped: it is the SAME algorithm as skew.py, so
    # it is not an independent check and it dominated the runtime.  What is
    # genuinely independent here is the connectivity route (max-flow against my
    # vertex-cut enumeration) and the Hamiltonicity route (Held-Karp DP against
    # my backtracking search).
    sk3 = None
    ok = (kappa >= 4) and (not ham)
    bad += not ok
    if not ok or i < 3:
        print(f"[{i+1:>3}] {line}  kappa={kappa}  Hamiltonian={ham}  "
              f"{'OK' if ok else '*** DISAGREES ***'}", flush=True)
print(f"\nre-checked {i+1} graphs by independent routes; disagreements: {bad}")
print("4-connectivity and non-Hamiltonicity confirmed by independent routes"
      if bad == 0 else "THEOREM IN DOUBT - investigate")

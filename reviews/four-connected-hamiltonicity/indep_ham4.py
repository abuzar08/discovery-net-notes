r"""reviewer-1: independent check of the four-connected-hamiltonicity lane.

My own filters: graph6 decoding, 4-connectivity by exhaustive cut enumeration,
Hamiltonicity by an exact subset dynamic programme (independent of the lane's
backtracking), independence number, and a skewness lower bound for the crossing
number — deleting at most three edges and testing planarity, since
\(\mathrm{cr}(G) \ge \mathrm{sk}(G)\).

Run: geng -d4 n lo:hi | python3 indep_ham4.py n
"""
import itertools
import sys

import networkx as nx

sys.path.insert(0, '../r45')
from indep_r45 import graph6, edges, has_clique


def connected(adj, alive):
    v0 = (alive & -alive).bit_length() - 1
    seen, st = 1 << v0, [v0]
    while st:
        u = st.pop()
        nb = adj[u] & alive & ~seen
        while nb:
            w = (nb & -nb).bit_length() - 1
            seen |= 1 << w
            st.append(w)
            nb &= nb - 1
    return seen == alive


def four_connected(n, adj):
    if n < 5:
        return False
    full = (1 << n) - 1
    for k in (1, 2, 3):
        for cut in itertools.combinations(range(n), k):
            alive = full
            for c in cut:
                alive &= ~(1 << c)
            if not connected(adj, alive):
                return False
    return True


def hamiltonian(n, adj):
    """exact, by subset dynamic programme over paths from vertex 0"""
    dp = [0] * (1 << n)
    dp[1] = 1                                    # bitmask of endpoints
    for mask in range(1, 1 << n):
        if not (mask & 1) or not dp[mask]:
            continue
        ends = dp[mask]
        e = ends
        while e:
            v = (e & -e).bit_length() - 1
            e &= e - 1
            nb = adj[v] & ~mask
            while nb:
                w = (nb & -nb).bit_length() - 1
                nb &= nb - 1
                dp[mask | (1 << w)] |= 1 << w
    full = (1 << n) - 1
    ends = dp[full]
    while ends:
        v = (ends & -ends).bit_length() - 1
        ends &= ends - 1
        if adj[0] >> v & 1:
            return True
    return False


def independence(n, adj):
    comp = [(~a) & ((1 << n) - 1) & ~(1 << i) for i, a in enumerate(adj)]
    k = n
    while k > 0 and not has_clique(n, comp, k):
        k -= 1
    return k


def nxgraph(n, adj):
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for v in range(n):
        b = adj[v]
        while b:
            u = (b & -b).bit_length() - 1
            b &= b - 1
            if u > v:
                G.add_edge(v, u)
    return G


def skewness_at_least(G, k):
    """True if no set of fewer than k edges makes G planar (so cr >= k)"""
    es = list(G.edges())
    for j in range(k):
        for sub in itertools.combinations(es, j):
            H = G.copy()
            H.remove_edges_from(sub)
            if nx.check_planarity(H, counterexample=False)[0]:
                return False
    return True


def main():
    n_expect = int(sys.argv[1])
    seen = c4 = nonham = 0
    surv = []
    for line in sys.stdin:
        if not line.strip():
            continue
        n, adj = graph6(line)
        seen += 1
        if not four_connected(n, adj):
            continue
        c4 += 1
        if hamiltonian(n, adj):
            continue
        nonham += 1
        surv.append((line.strip(), n, adj))
    print(f'n = {n_expect}: read {seen}, 4-connected {c4}, '
          f'4-connected and non-Hamiltonian {nonham}')
    for g6, n, adj in surv:
        G = nxgraph(n, adj)
        a = independence(n, adj)
        sk4 = skewness_at_least(G, 4)
        print(f'   {g6}  m={G.number_of_edges()}  alpha={a}  '
              f'skewness >= 4: {sk4} -> '
              f'{"cr >= 4, not a counterexample" if sk4 else "cr <= 3 possible, needs the exact test"}')


if __name__ == '__main__':
    main()

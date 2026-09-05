"""reviewer-1: alpha and vertex-criticality of the new witnesses (own code + python-sat)."""
import sys, time
from indep_upper import load, adj_masks, has_clique, sat_colourable, colourable
def alpha(n, A):
    comp = [((1 << n) - 1) ^ A[v] ^ (1 << v) for v in range(n)]  # complement adjacency
    a = 0
    while has_clique(n, comp, a + 1): a += 1
    return a
for path, k, q in [('target/witnesses/ub_n21a_k8_q5.txt', 8, 5), ('target/witnesses/ub_n21b_k8_q5.txt', 8, 5), ('target/witnesses/ub_n33_k7_q4.txt', 7, 4)]:
    n, E = load(path); A = adj_masks(n, E)
    print(path.split('/')[-1], 'alpha =', alpha(n, A), end='; ')
    t = time.time(); crit = True
    for v in range(n):
        E2 = [(a, b) for a, b in E if v not in (a, b)]
        # relabel not needed: isolated vertex v keeps chi; colourable check handles isolated vertex
        if not sat_colourable(n, E2, k - 1):  # still chi >= k after deleting v
            crit = False; print(f'vertex {v} deletable', end='; ')
    print('vertex-critical (no single vertex deletable):', crit, f'[{time.time()-t:.0f}s]')

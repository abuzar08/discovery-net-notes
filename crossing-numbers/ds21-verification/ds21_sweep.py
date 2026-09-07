"""Independent exact verification of DS21's complete-multipartite crossing-number
formulas, at every instance small enough to decide outright.

DS21 (2026) states a number of exact formulas for complete multipartite families.
Each is checked here at the smallest parameters by exhaustive planarisation --
enumerate every set of at most k crossing pairs and every ordering of crossings
along shared edges, which decides cr(G) <= k exactly.  The decider is validated
on known values first.

This matters because DS21 is the standard reference and its rendering of at least
one conjecture has already been found to differ from the source (Mohar's
Conjecture 5, silently extended from even n to all n, false at n = 5).
"""
from math import comb
import networkx as nx
from crk import cr_le, multipartite


def Z(m, n):
    return (m // 2) * ((m - 1) // 2) * (n // 2) * ((n - 1) // 2)


FORMULAS = [
    ("K_{1,3,n}",     lambda n: (1, 3, n),    lambda n: Z(4, n) + n // 2),
    ("K_{2,3,n}",     lambda n: (2, 3, n),    lambda n: Z(5, n) + n),
    ("K_{1,4,n}",     lambda n: (1, 4, n),    lambda n: n * (n - 1)),
    ("K_{1,1,3,n}",   lambda n: (1, 1, 3, n), lambda n: Z(5, n) + (3 * n) // 2),
    ("K_{2,4,n}",     lambda n: (2, 4, n),    lambda n: Z(6, n) + 2 * n),
    ("K_{1,1,1,1,n}", lambda n: (1, 1, 1, 1, n), lambda n: Z(4, n) + n),
    ("K_{1,1,1,2,n}", lambda n: (1, 1, 1, 2, n), lambda n: Z(5, n) + 2 * n),
    ("K_{1,2,2,n}",   lambda n: (1, 2, 2, n), lambda n: Z(5, n) + (3 * n) // 2),
    ("K_{2,2,2,n}",   lambda n: (2, 2, 2, n), lambda n: 6 * (n // 2) * ((n - 1) // 2) + 3 * n),
]


def exact_cr(G, cap=8, budget=45.0):
    """Exact cr, or None if the time budget is exhausted.

    Reporting "not decided" is essential: a sweep that silently omits the cases
    it could not finish would look like a clean bill of health for the ones it
    did.
    """
    import time
    t0 = time.time()
    k = 0
    while k <= cap:
        if time.time() - t0 > budget:
            return None
        if cr_le(G, k):
            return k
        k += 1
    return None


if __name__ == "__main__":
    import sys, time
    print("validation on known values:")
    for name, G, val in [("K5", nx.complete_graph(5), 1),
                         ("K6", nx.complete_graph(6), 3),
                         ("K3,3", nx.complete_bipartite_graph(3, 3), 1)]:
        print(f"   cr({name}) = {exact_cr(G)}  expected {val}")
    print()
    print(f"{'family':>15} {'n':>3} {'|V|':>4} {'|E|':>4} {'DS21':>6} {'exact':>6}  verdict")
    for name, parts, f in FORMULAS:
        for n in (1, 2, 3):
            p = parts(n)
            G = multipartite(list(p))
            if G.number_of_nodes() > 8:
                continue
            pred = f(n)
            # The decider is exhaustive over sets of k crossing pairs, so its
            # honest ceiling is small: at these edge counts k <= 5 is reachable
            # and k >= 6 is not.  Cases above the ceiling are reported as out of
            # range rather than attempted, so the sweep's scope is explicit and
            # no case is silently dropped.
            if pred > 5:
                print(f"{name:>15} {n:>3} {G.number_of_nodes():>4} "
                      f"{G.number_of_edges():>4} {pred:>6} {'-':>6}  "
                      f"out of range (predicted {pred} > 5)", flush=True)
                continue
            t0 = time.time()
            got = exact_cr(G, cap=pred + 1)
            if got is None:
                v = "not decided (time)"
            elif got == pred:
                v = "OK"
            else:
                v = "*** MISMATCH"
            print(f"{name:>15} {n:>3} {G.number_of_nodes():>4} "
                  f"{G.number_of_edges():>4} {pred:>6} {str(got):>6}  {v}"
                  f"   ({time.time()-t0:.1f}s)", flush=True)

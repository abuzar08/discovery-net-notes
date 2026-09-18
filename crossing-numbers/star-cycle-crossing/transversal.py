"""Transversal test: a purely combinatorial necessary condition for cr(G) <= k.

In any drawing, deleting one edge from each crossing removes every crossing, so
the remaining graph is planar.  Hence if cr(G) <= k there are k pairs of
independent edges such that EVERY transversal (one edge chosen per pair) is a
planarising set.  Enumerating the planarising sets of size <= k therefore gives
a finite test that can refute cr(G) <= k without searching drawings at all.
"""
import itertools, sys
import networkx as nx

def planarising_sets(G, k):
    """All edge subsets of size <= k whose deletion leaves a planar graph."""
    E = list(G.edges())
    out = set()
    for r in range(k + 1):
        for S in itertools.combinations(range(len(E)), r):
            H = G.copy()
            H.remove_edges_from([E[i] for i in S])
            if nx.check_planarity(H)[0]:
                out.add(frozenset(S))
    return E, out

def independent(E, a, b):
    return not (set(E[a]) & set(E[b]))

def cr_le_transversal(G, k, verbose=False):
    """False  => cr(G) > k, PROVED.
       True   => the test is inconclusive (no contradiction found)."""
    E, P = planarising_sets(G, k)
    if verbose:
        print(f'  |E|={len(E)}  planarising sets of size <= {k}: {len(P)}', flush=True)
    if frozenset() in P:
        return True                      # planar
    # edges that can appear in a crossing at all: those lying in some planarising set
    live = sorted({i for S in P for i in S})
    if verbose:
        print(f'  edges able to occur in a crossing: {len(live)} of {len(E)}', flush=True)
    pairs = [(a, b) for a, b in itertools.combinations(live, 2) if independent(E, a, b)]
    if verbose:
        print(f'  candidate crossing pairs: {len(pairs)}', flush=True)
    for combo in itertools.combinations(pairs, k):
        ok = True
        for pick in itertools.product(*combo):
            if frozenset(pick) not in P:
                ok = False
                break
        if ok:
            if verbose:
                print('  inconclusive: surviving configuration',
                      [(E[a], E[b]) for a, b in combo], flush=True)
            return True
    return False


def realisable(G, E, combo):
    """A drawing whose crossings are exactly `combo` exists iff the planarisation
    -- one new vertex per crossing, splitting both edges -- is planar.  Requires
    the 2k edges to be pairwise distinct, so each is subdivided once."""
    H = G.copy()
    for n, (a, b) in enumerate(combo):
        for side, idx in (('a', a), ('b', b)):
            u, v = E[idx]
            H.remove_edge(u, v)
            H.add_edge(u, ('x', n))
            H.add_edge(('x', n), v)
    return nx.check_planarity(H)[0]


def cr_le_exact(G, k, verbose=False):
    """Complete decision of cr(G) <= k via the transversal filter plus
    planarisation.  Returns (decision, n_survivors, n_tested)."""
    E, P = planarising_sets(G, k)
    if frozenset() in P:
        return True, 0, 0
    live = sorted({i for S in P for i in S})
    pairs = [(a, b) for a, b in itertools.combinations(live, 2) if independent(E, a, b)]
    if verbose:
        print(f'  |E|={len(E)}  live edges={len(live)}  candidate pairs={len(pairs)}', flush=True)
    surv = tested = 0
    for combo in itertools.combinations(pairs, k):
        flat = [i for p in combo for i in p]
        if len(set(flat)) != 2 * k:          # repeated edge => transversal too small
            continue
        if any(frozenset(pick) not in P for pick in itertools.product(*combo)):
            continue
        surv += 1
        tested += 1
        if realisable(G, E, combo):
            if verbose:
                print('  REALISABLE:', [(E[a], E[b]) for a, b in combo], flush=True)
            return True, surv, tested
    return False, surv, tested

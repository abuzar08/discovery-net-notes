"""Transversal test: a purely combinatorial necessary condition for cr(G) <= k.

THE OBSERVATION.  In any drawing, deleting one edge from each crossing removes
every crossing, so the remaining graph is planar.  That holds for EVERY choice of
one edge per crossing, not merely some choice.  Hence if cr(G) <= k there are k
pairs of independent edges such that every transversal -- one edge chosen per
pair -- is a planarising set.  The condition says nothing about where anything is
drawn, so it can be checked by enumeration, and it refutes cr(G) <= k whenever no
such k pairs exist.

COMPLETION.  A drawing whose crossings are exactly a given set of k pairs exists
if and only if the planarisation -- one new vertex per crossing, splitting both
its edges -- is planar.  So: filter configurations by the transversal condition,
then test each survivor's planarisation.

WHERE THIS IS COMPLETE, AND WHY MISUSE IS DANGEROUS.
-----------------------------------------------------------------------------
The planarisation step needs each edge subdivided ONCE, so configurations in
which one edge lies in two crossings are skipped.  That makes the method
INCOMPLETE IN GENERAL -- and a skipped configuration yields a wrong REFUTATION,
not a missed one.  Wrong refutations are the dangerous direction: they assert
cr(G) > k, which is a claim, whereas a missed configuration would only cost a
weaker answer.

    It is complete exactly when k == sk(G).

If an edge were in two crossings, the transversal choosing it twice would be a
planarising set of size < k = sk(G), and no such set exists.  So at k = sk(G)
nothing is skipped and the decision is exact.

`cr_le_exact` ENFORCES this rather than merely documenting it: it refuses to
return a refutation when k != sk(G), raising instead.  Pass
require_complete=False only if you want the one-sided filter on purpose.

VALIDATION, AND WHY THE REFUTING CASES ARE THE ONES THAT COUNT.
-----------------------------------------------------------------------------
Ten cases were checked against published values before any use.  Seven expect
`True`: K_5, K_{3,3}, Petersen, K_6, K_{3,4}, K_{1,3} box C_3, K_{1,4} box C_3.
Three expect `False`: K_{3,5} (sk 3, cr 4), K_{3,6} (sk 4, cr 6), K_{1,1,1,5}
(sk 3, cr 4) -- checked against Zarankiewicz for K_{3,n} and Harborth for
K_{1,1,1,m}, which are theorems rather than conjectures.

The three matter more than the seven, because THE OTHER SEVEN WOULD ALL PASS
WITH A ROUTINE THAT ALWAYS ANSWERED "True".  A validation suite in which every
case expects the same answer tests almost nothing; the refuting cases are the
only ones exercising the direction every result of mine relies on.
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


class IncompleteRange(Exception):
    """Raised rather than returning a refutation that may be unsound."""


def cr_le_exact(G, k, verbose=False, require_complete=True):
    """Decide cr(G) <= k via the transversal filter plus planarisation.

    Returns (decision, n_survivors, n_tested).  Complete only when k == sk(G);
    outside that range a refutation may be unsound, so one is refused rather
    than returned.  See the module docstring.
    """
    E, P = planarising_sets(G, k)
    if frozenset() in P:
        return True, 0, 0
    # sk(G) is already in hand: the smallest planarising set found.  If none was
    # found at all then sk(G) > k, so cr(G) >= sk(G) > k and refuting is sound.
    sk = min((len(S) for S in P), default=None)
    complete = (sk is None) or (sk == k)
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
            return True, surv, tested          # sound at any k: an actual drawing
    if require_complete and not complete:
        raise IncompleteRange(
            f'refutation refused: k={k} but sk(G)={sk}; the method is complete '
            f'only at k == sk(G), and outside it a "False" may be unsound')
    return False, surv, tested

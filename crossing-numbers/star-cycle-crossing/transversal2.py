"""Transversal decider extended to k = sk(G) + 1.

The k = sk(G) version is complete because no edge can lie in two crossings: the
transversal choosing that edge twice would be a planarising set of size < sk(G).
At k = sk(G) + 1 that argument weakens by exactly one step, and the weakening is
BOUNDED:

    At k = sk(G) + 1, at most ONE edge lies in two crossings, and no edge lies
    in three or more.

Two doubly-used edges would give a transversal of size k - 2 = sk - 1, and a
triply-used edge a transversal of size k - 2 as well; neither can planarise.  So
the configurations to add are exactly those with 2k - 1 distinct edges, one of
them appearing in two pairs.  For such a configuration the doubly-crossed edge
carries two crossing points, and the planarisation must try BOTH ORDERS of those
points along the edge.

That makes the method complete at k = sk(G) + 1, and `cr_le_exact2` refuses to
return a refutation outside k in {sk(G), sk(G) + 1}.
"""
import itertools
import networkx as nx


class IncompleteRange(Exception):
    pass


def planarising_sets(G, k):
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


def _extendable(T, P):
    """Can the partial transversal T be completed to a planarising set in P?"""
    return any(T <= S for S in P)


def _realisable(G, E, combo, order=None):
    """combo: list of k pairs.  order: for the doubly-used edge, the sequence of
    crossing indices along it.  Build the planarisation and test planarity."""
    H = G.copy()
    # how many crossings each edge is in
    cnt = {}
    for n, (a, b) in enumerate(combo):
        cnt.setdefault(a, []).append(n)
        cnt.setdefault(b, []).append(n)
    for idx, ns in cnt.items():
        u, v = E[idx]
        H.remove_edge(u, v)
        seq = ns if len(ns) == 1 else order
        chain = [u] + [('x', n) for n in seq] + [v]
        for p, q in zip(chain, chain[1:]):
            H.add_edge(p, q)
    return nx.check_planarity(H)[0]


def cr_le_exact2(G, k, verbose=False, require_complete=True):
    """Decide cr(G) <= k.  Complete for k in {sk(G), sk(G)+1}.

    NOTE: the search below looks for a drawing with EXACTLY j crossings, so it
    must be run for every j from sk(G) up to k.  At k = sk(G) that is a single
    value and the distinction is invisible -- cr >= sk forces equality -- which
    is why the k = sk version never needed it.  At k = sk+1 omitting j = sk
    produces a FALSE REFUTATION on any graph with cr(G) = sk(G); validation
    caught exactly that on K_5 and K_6.
    """
    E, P = planarising_sets(G, k)
    if frozenset() in P:
        return True, 0
    sk = min((len(S) for S in P), default=None)
    complete = (sk is None) or (sk in (k, k - 1))
    live = sorted({i for S in P for i in S})
    pairs = [(a, b) for a, b in itertools.combinations(live, 2) if independent(E, a, b)]
    if verbose:
        print(f'  |E|={len(E)} sk={sk} live={len(live)} pairs={len(pairs)} '
              f'planarising sets={len(P)}', flush=True)
    tested = 0
    target = k                              # set per-j by the loop below

    def rec(start, combo, transversals):
        nonlocal tested
        if len(combo) == target:
            tested += 1
            edges = [i for p in combo for i in p]
            dup = [i for i in set(edges) if edges.count(i) == 2]
            if not dup:
                return _realisable(G, E, combo)
            if len(dup) > 1:
                return False                       # impossible at k = sk+1
            ns = [n for n, p in enumerate(combo) if dup[0] in p]
            return any(_realisable(G, E, combo, order=o)
                       for o in (ns, ns[::-1]))
        for i in range(start, len(pairs)):
            p = pairs[i]
            edges = [e for q in combo for e in q]
            # an edge may appear at most twice across the whole configuration
            if any(edges.count(e) >= 2 for e in p):
                continue
            if sum(1 for e in set(edges) if edges.count(e) == 2) >= 1 and \
               any(e in edges for e in p):
                continue                           # would create a second duplicate
            new = set()
            ok = True
            for T in transversals:
                for e in p:
                    U = T | {e}
                    if not _extendable(U, P):
                        ok = False
                        break
                    new.add(frozenset(U))
                if not ok:
                    break
            if not ok:
                continue
            if rec(i + 1, combo + [p], new):
                return True
        return False

    found = False
    lo = sk if sk is not None else k
    for j in range(lo, k + 1):              # a drawing may have FEWER than k crossings
        target = j
        if verbose:
            print(f'  searching configurations of exactly {j} crossings', flush=True)
        if rec(0, [], {frozenset()}):
            found = True
            break
    if found:
        return True, tested
    if require_complete and not complete:
        raise IncompleteRange(
            f'refutation refused: k={k}, sk(G)={sk}; complete only for '
            f'k in {{sk, sk+1}}')
    return False, tested

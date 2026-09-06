"""Settle the one Figure 14.3 component that resists identification of <= 3 pairs.

Identifying vertices that the figure drew twice means pairing up DISTINCT
duplicates, i.e. applying a partial matching on the vertex set, not an arbitrary
multiset of pairs.  That is both the right model and a much smaller search, so
it reaches k = 4 and 5 where the unrestricted version could not.
"""
import collections
import itertools

import networkx as nx

import expand_run as R
from fig143 import drawn_components, verdict, identify


def matchings(nodes, k):
    if k == 0:
        yield ()
        return
    nodes = list(nodes)
    if len(nodes) < 2 * k:
        return
    first = nodes[0]
    # first is either unmatched, or matched to some other vertex
    for rest in matchings(nodes[1:], k):
        yield rest
    for j in range(1, len(nodes)):
        pair = (first, nodes[j])
        remain = nodes[1:j] + nodes[j + 1:]
        for rest in matchings(remain, k - 1):
            yield (pair,) + rest


if __name__ == '__main__':
    gs = drawn_components()
    bad = [G for G in gs if not verdict(G)]
    hold = [G for G in bad
            if (G.number_of_nodes(), G.number_of_edges()) == (14, 22)]
    print(f"holdout components: {len(hold)}", flush=True)
    for G in hold:
        for k in (1, 2, 3, 4, 5):
            cands = []
            seen = set()
            for P in matchings(sorted(G.nodes()), k):
                if len(P) != k:
                    continue
                H = identify(G, P)
                if H.number_of_nodes() < 5:
                    continue
                if min((d for _, d in H.degree()), default=0) < 3:
                    continue
                cands.append(H)
            if not cands:
                print(f"  k={k}: no candidate survives minimum degree 3",
                      flush=True)
                continue
            marks = [l.split()[0] for l in R.run_crit2(cands).split('\n')
                     if l.startswith('CRIT')]
            print(f"  k={k}: {len(cands):,} matchings tested, "
                  f"critical: {dict(collections.Counter(marks))}", flush=True)
            if marks:
                break

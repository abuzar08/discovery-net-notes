"""Strengthen the Figure 14.3 claim: ALL identifications up to k = 4, not the least k.

The earlier run took, for each drawn component, the least k admitting any
2-crossing-critical identification, and reported the verdicts at that k.  That is
sound only if the identification the figure intends uses at most that many pairs.
The census cross-check exposed the gap: one repaired graph came out 3-CONNECTED,
and every member of Theorem 1.3(2) is 2-connected and not 3-connected, so that
repair is not the intended member -- some component's intended identification
must use more pairs than the least k that happens to work.

This run drops the early stop.  For every component it enumerates all partial
matchings with k <= 4 and records the verdict of every 2-crossing-critical
result, together with its connectivity, so the claim no longer depends on
guessing which identification is meant.
"""
import collections
import json
import sys

import networkx as nx

import expand_run as R
from fig143 import drawn_components, verdict, identify
from fig143b import matchings

KMAX = 4


def all_repairs(G):
    out = []
    seen = set()
    for k in range(1, KMAX + 1):
        cands = []
        for P in matchings(sorted(G.nodes()), k):
            if len(P) != k:
                continue
            H = identify(G, P)
            if H.number_of_nodes() < 5:
                continue
            if min((d for _, d in H.degree()), default=0) < 3:
                continue
            key = nx.weisfeiler_lehman_graph_hash(H, iterations=3)
            if (k, key) in seen:
                continue
            seen.add((k, key))
            cands.append(H)
        if not cands:
            continue
        B = 20000
        for i in range(0, len(cands), B):
            chunk = cands[i:i + B]
            res = R.run_crit2(chunk)
            marks = [l.split()[0] for l in res.split('\n') if l.startswith('CRIT')]
            if marks:
                # re-test individually only for the ones that matter
                for H in chunk:
                    v = verdict(H)
                    if v:
                        out.append((k, v, nx.node_connectivity(H),
                                    H.number_of_nodes(), H.number_of_edges()))
    return out


if __name__ == '__main__':
    gs = drawn_components()
    bad = [G for G in gs if not verdict(G)]
    print(f"components needing repair: {len(bad)}", flush=True)
    tot = collections.Counter()
    conn = collections.Counter()
    per = []
    for i, G in enumerate(sorted(bad, key=lambda g: g.number_of_nodes())):
        reps = all_repairs(G)
        vs = collections.Counter(v for _, v, _, _, _ in reps)
        cs = collections.Counter(c for _, _, c, _, _ in reps)
        tot.update(vs)
        conn.update(cs)
        ks = sorted({k for k, _, _, _, _ in reps})
        per.append((G.number_of_nodes(), G.number_of_edges(), len(reps),
                    dict(vs), dict(cs), ks))
        print(f"  n={G.number_of_nodes():>3} m={G.number_of_edges():>3}: "
              f"{len(reps):>4} critical identifications at k in {ks}, "
              f"verdicts {dict(vs)}, connectivity {dict(cs)}", flush=True)
    print(f"\nover ALL identifications with k <= {KMAX}:")
    print(f"  verdicts: {dict(tot)}")
    print(f"  connectivity: {dict(conn)}")
    print(f"  any with cr >= 3: {tot.get('CRIT_GE3', 0)}")
    json.dump(per, open('fig143_full.json', 'w'))

"""The principal's acceptance gate for the corrected construction.

Criterion: the repaired program must reproduce all 36 seeds and produce all of
the census targets the old program failed on.  Until it does, nothing from it
may be published.

Search structure, from the corrected model: the port count on an edge vw is 2
exactly when w is in T_v, so the constraint "w in T_v iff v in T_w" says the
ports agree, and choosing every type at once is choosing a subgraph H of the
base restricted to its degree-3 vertices.  Enumerate H, then per vertex the
configurations of class |T| = deg_H(v) oriented so their T-terminals land on the
H-neighbours, then the pairings of matched port pairs.
"""
import collections
import itertools
import json
import sys

import networkx as nx

import construct as C
import expand_run as R

FLIPCAP = 10


def candidates(L, cfgs, H):
    d3 = [v for v, d in L.degree() if d == 3]
    cand = {}
    for v in d3:
        nbrs = list(L[v])
        want = {w for w in nbrs if tuple(sorted((v, w))) in H}
        lst = []
        for cfg in cfgs:
            if len(cfg['T']) != len(want):
                continue
            for perm in cfg['perms']:
                p = C.ports(cfg, perm, nbrs)
                if {w for w in nbrs if len(p[w]) == 2} == want:
                    lst.append((cfg, perm))
        if not lst:
            return None
        cand[v] = lst
    return cand


def expansions(L, cfgs, nmax):
    d3 = [v for v, d in L.degree() if d == 3]
    E = [tuple(sorted(e)) for e in L.edges()]
    dup_edges = [e for e in E if L.degree(e[0]) >= 4 and L.degree(e[1]) >= 4]
    out = []
    for bits in range(1 << len(E)):
        H = {e for j, e in enumerate(E) if bits >> j & 1}
        cand = candidates(L, cfgs, H)
        if cand is None:
            continue
        for combo in itertools.product(*[cand[v] for v in d3]):
            if sum(len(c['internal']) for c, _ in combo) > nmax:
                continue
            assign = dict(zip(d3, combo))
            # a pairing only matters when BOTH sides offer two DISTINCT ports;
            # a lens presents the same internal vertex twice, so swapping is a
            # no-op and the edge need not be branched on
            flip = []
            for e in E:
                if e[0] not in assign or e[1] not in assign:
                    continue
                pu = C.ports(*assign[e[0]], list(L[e[0]]))[e[1]]
                pw = C.ports(*assign[e[1]], list(L[e[1]]))[e[0]]
                if len(pu) == 2 and len(set(pu)) == 2 and len(set(pw)) == 2:
                    flip.append(e)
            nf = min(len(flip), FLIPCAP)
            for fb in range(1 << nf):
                pr = {e: (fb >> j) & 1 for j, e in enumerate(flip[:nf])}
                for k in range(len(dup_edges) + 1):
                    for S in itertools.combinations(dup_edges, k):
                        g = C.build2(L, assign, set(S), pr)
                        if g is not None and g.number_of_nodes() <= nmax:
                            out.append(g)
    return out


def critical(gs):
    keep = [g for g in gs
            if g.number_of_nodes() <= 28 and g.number_of_edges() <= 62]
    out = []
    B = 20000
    for i in range(0, len(keep), B):
        for line in R.run_crit2(keep[i:i + B]).split('\n'):
            if line.startswith('CRIT'):
                E = [tuple(map(int, x.split('-')))
                     for x in line.split()[3].strip(',').split(',') if x]
                out.append(nx.Graph(E))
    return out


def main():
    cfgs = C.load_configs()
    for c in cfgs:
        c['perms'] = C.perm_reps(c)

    # part 1: every seed must be reproduced (the all-claw assignment)
    claw = [c for c in cfgs if not c['T']][0]
    seeds = R.seeds()
    bad = 0
    for S in seeds:
        d3 = [v for v, d in S.degree() if d == 3]
        g = C.build2(S, {v: (claw, (0, 1, 2)) for v in d3})
        if g is None or not nx.is_isomorphic(g, S):
            bad += 1
    print(f"seeds reproduced by the identity assignment: {len(seeds)-bad}/"
          f"{len(seeds)}", flush=True)

    # part 2: every target must be produced
    T = json.load(open('targets19.json'))
    tg = [(t, nx.Graph([tuple(e) for e in t['target']]))
          for t in T if t['p4c']]
    bybase = collections.defaultdict(list)
    for t, G in tg:
        bybase[tuple(sorted(map(tuple, map(sorted, t['base']))))].append(G)
    hit = 0
    for key, targets in bybase.items():
        L = nx.convert_node_labels_to_integers(nx.Graph([tuple(e) for e in key]))
        nmax = max(g.number_of_nodes() for g in targets)
        gs = expansions(L, cfgs, nmax)
        cr = critical(gs)
        h = sum(1 for t in targets if any(nx.is_isomorphic(t, g) for g in cr))
        hit += h
        print(f"  base n={L.number_of_nodes()} m={L.number_of_edges()}: "
              f"built {len(gs):,}, critical {len(cr):,}, "
              f"targets {h}/{len(targets)}", flush=True)
    print(f"\nTARGETS PRODUCED: {hit}/{len(tg)}")
    print(f"GATE: {'PASSED' if hit == len(tg) and bad == 0 else 'NOT PASSED'}")


if __name__ == '__main__':
    main()

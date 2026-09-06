"""Run the corrected replacement construction exhaustively at low depth.

Now that the gate passes, this is the lane's actual question: does BORS's
construction produce a 2-crossing-critical graph of crossing number at least 3 --
a second counterexample to Bloom-Kennedy-Quintas -- anywhere in reach?  Any such
graph has at least 12 vertices (census) and is 3-connected (the headline), and
the expansions here reach 29 vertices, so this is new territory.

Complete for every seed with at most `dmax` degree-3 vertices: all type
assignments (equivalently all subgraphs of L on its degree-3 vertices, since the
port-agreement condition makes the type relation symmetric), all configurations
and orientations of the matching class, all port pairings, and all choices of
single edge versus parallel pair on edges between vertices of degree at least 4.
Per-seed .done markers make it resumable.
"""
import collections
import itertools
import json
import os
import sys
import time

import networkx as nx

import construct as C
import expand_run as R

STATE = 'corrected_state'
BATCH = 20000


def placements(L, v, cfgs):
    nbrs = list(L[v])
    g = collections.defaultdict(list)
    for cfg in cfgs:
        for perm in cfg['perms']:
            p = C.ports(cfg, perm, nbrs)
            g[frozenset(w for w in nbrs if len(p[w]) == 2)].append((cfg, perm))
    return g


def run_seed(L, cfgs, nmax=28, mmax=62):
    d3 = [v for v, d in L.degree() if d == 3]
    d3s = set(d3)
    E = [tuple(sorted(e)) for e in L.edges() if e[0] in d3s and e[1] in d3s]
    dup_edges = [tuple(sorted(e)) for e in L.edges()
                 if L.degree(e[0]) >= 4 and L.degree(e[1]) >= 4]
    place = {v: placements(L, v, cfgs) for v in d3}
    built = skipped = 0
    crit = ge3 = 0
    hits = []
    buf = []

    def flush():
        nonlocal crit, ge3, buf
        if not buf:
            return
        out = R.run_crit2(buf)
        for line in out.split('\n'):
            if line.startswith('CRIT2'):
                crit += 1
            elif line.startswith('CRIT_GE3'):
                crit += 1
                ge3 += 1
                hits.append(line.strip())
        buf = []

    for bits in range(1 << len(E)):
        H = {e for j, e in enumerate(E) if bits >> j & 1}
        opts = []
        ok = True
        for v in d3:
            nbrs = list(L[v])
            forced = {w for w in nbrs if w in d3s and tuple(sorted((v, w))) in H}
            free = [w for w in nbrs if w not in d3s]
            lst = []
            for r in range(len(free) + 1):
                for extra in itertools.combinations(free, r):
                    lst += place[v].get(frozenset(forced | set(extra)), [])
            if not lst:
                ok = False
                break
            opts.append(lst)
        if not ok:
            continue
        for combo in itertools.product(*opts):
            assign = dict(zip(d3, combo))
            flip = []
            for e in E:
                if e[0] in assign and e[1] in assign:
                    pu = C.ports(*assign[e[0]], list(L[e[0]]))[e[1]]
                    pw = C.ports(*assign[e[1]], list(L[e[1]]))[e[0]]
                    if len(pu) == 2 and len(set(pu)) == 2 and len(set(pw)) == 2:
                        flip.append(e)
            for fb in range(1 << len(flip)):
                pr = {e: (fb >> j) & 1 for j, e in enumerate(flip)}
                for k in range(len(dup_edges) + 1):
                    for S in itertools.combinations(dup_edges, k):
                        g = C.build2(L, assign, set(S), pr)
                        if g is None:
                            continue
                        built += 1
                        if g.number_of_nodes() > nmax or \
                                g.number_of_edges() > mmax:
                            skipped += 1
                            continue
                        buf.append(g)
                        if len(buf) >= BATCH:
                            flush()
    flush()
    return dict(built=built, skipped=skipped, critical=crit, cr_ge_3=ge3,
                hits=hits[:50])


if __name__ == '__main__':
    dmax = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    cfgs = C.load_configs()
    for c in cfgs:
        c['perms'] = C.perm_reps(c)
    os.makedirs(STATE, exist_ok=True)
    seeds = R.seeds()
    todo = [(i, S) for i, S in enumerate(seeds)
            if sum(1 for _, d in S.degree() if d == 3) <= dmax]
    print(f"seeds with d <= {dmax}: {len(todo)} of {len(seeds)}", flush=True)
    for i, S in todo:
        mark = os.path.join(STATE, f'seed{i:02d}.done')
        if os.path.exists(mark):
            continue
        t0 = time.time()
        res = run_seed(S, cfgs)
        res.update(seed=i, n=S.number_of_nodes(), m=S.number_of_edges(),
                   d=sum(1 for _, d in S.degree() if d == 3),
                   seconds=round(time.time() - t0, 1))
        json.dump(res, open(mark, 'w'), indent=1)
        print(f"seed {i:02d}: n={res['n']} d={res['d']} built {res['built']:,}, "
              f"skipped {res['skipped']:,}, critical {res['critical']}, "
              f"cr>=3 {res['cr_ge_3']}, {res['seconds']}s", flush=True)

"""Can the corrected construction produce one specific census target?

Target: the (9,18) graph whose unique peripherally-4-connected base under planar
3-reductions is K_{3,3}.  Structure forced by the corrected model: the port count
on an edge vw is 2 exactly when w is in T_v, so the choice of all the types at
once is a subgraph H of the base, and each vertex needs a configuration whose
|T| equals its H-degree, oriented so that its T-terminals land on its
H-neighbours.
"""
import collections
import itertools
import json

import networkx as nx

import construct as C
import expand_run as R


def port_profile(cfg, perm, nbrs):
    p = C.ports(cfg, perm, nbrs)
    return {w: len(v) for w, v in p.items()}


def run(target, L, cfgs, nmax):
    d3 = [v for v, d in L.degree() if d == 3]
    E = [tuple(sorted(e)) for e in L.edges()]
    found = []
    for bits in range(1 << len(E)):
        H = {e for j, e in enumerate(E) if bits >> j & 1}
        deg = {v: sum(1 for w in L[v] if tuple(sorted((v, w))) in H) for v in d3}
        # candidates per vertex: |T| must equal H-degree, oriented onto H-nbrs
        cand = {}
        ok = True
        for v in d3:
            nbrs = list(L[v])
            want = {w for w in nbrs if tuple(sorted((v, w))) in H}
            lst = []
            for cfg in cfgs:
                if len(cfg['T']) != deg[v]:
                    continue
                for perm in cfg['perms']:
                    pp = port_profile(cfg, perm, nbrs)
                    if {w for w in nbrs if pp[w] == 2} == want:
                        lst.append((cfg, perm))
            if not lst:
                ok = False
                break
            cand[v] = lst
        if not ok:
            continue
        # budget: total internal vertices cannot exceed the target's order
        for combo in itertools.product(*[cand[v] for v in d3]):
            if sum(c['internal'].__len__() for c, _ in combo) > nmax:
                continue
            assign = dict(zip(d3, combo))
            flip = [e for e in E
                    if len(C.ports(*assign[e[0]], list(L[e[0]]))[e[1]]) == 2]
            for fb in range(1 << len(flip)):
                pr = {e: (fb >> j) & 1 for j, e in enumerate(flip)}
                g = C.build2(L, assign, (), pr)
                if g is None or g.number_of_nodes() != target.number_of_nodes():
                    continue
                if g.number_of_edges() != target.number_of_edges():
                    continue
                if nx.is_isomorphic(g, target):
                    found.append((bits, [c['id'] for c, _ in combo]))
                    return found
    return found


if __name__ == '__main__':
    cfgs = C.load_configs()
    for c in cfgs:
        c['perms'] = C.perm_reps(c)
    T = json.load(open('targets19.json'))
    t = [x for x in T if x['p4c'] and x['base_n'] == 6
         and len(x['target']) == 18][0]
    target = nx.Graph([tuple(e) for e in t['target']])
    L = nx.convert_node_labels_to_integers(nx.complete_bipartite_graph(3, 3))
    print(f"target n={target.number_of_nodes()} m={target.number_of_edges()}, "
          f"base K33")
    f = run(target, L, cfgs, target.number_of_nodes())
    print("PRODUCED" if f else "not produced", f[:1])

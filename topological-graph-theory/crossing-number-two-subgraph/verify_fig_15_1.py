"""Check the Figure 15.1 configuration artifact.  Standard library only.

Verifies, for figure_15_1_configurations.json:
  1. each configuration has exactly 3 terminals and at most 6 internal
     vertices, as Theorem 17.1(3) requires;
  2. the recorded (|T|,|U|) is what Definition 15.21 gives, computed with
     integer max-flow whose capacities are the EDGE MULTIPLICITIES -- the
     patches are multigraphs, and using simple-graph connectivity here is
     exactly the error this artifact corrects;
  3. the recorded rotation system really is a planar embedding of H + apex,
     by Euler face-tracing (V - E + F = 2), so each is a (T,U)-configuration;
  4. the 31 configurations are pairwise non-isomorphic;
  5. the class distribution is (3,3):20, (3,2):3, (2,1):5, (1,0):2, (0,0):1,
     matching the five groups the figure is drawn in.

Usage: python3 verify_fig_15_1.py [figure_15_1_configurations.json]
"""
import collections
import itertools
import json
import sys

TERMS = ('x', 'y', 'z')
INF = 10 ** 9


# --------------------------------------------------------------- max-flow
def maxflow(cap, s, t):
    """Integer max-flow, Edmonds-Karp, on an undirected capacity dict."""
    res = {u: dict(d) for u, d in cap.items()}
    flow = 0
    while True:
        prev, q = {s: None}, [s]
        while q and t not in prev:
            nq = []
            for u in q:
                for v, c in res.get(u, {}).items():
                    if c > 0 and v not in prev:
                        prev[v] = u
                        nq.append(v)
            q = nq
        if t not in prev:
            return flow
        # bottleneck
        b, v = INF, t
        while prev[v] is not None:
            b = min(b, res[prev[v]][v])
            v = prev[v]
        v = t
        while prev[v] is not None:
            u = prev[v]
            res[u][v] -= b
            res.setdefault(v, {})[u] = res.get(v, {}).get(u, 0) + b
            v = u
        flow += b


def capacities(cfg, drop=None):
    cap = collections.defaultdict(dict)
    m = collections.Counter(tuple(sorted(e)) for e in cfg['edges'])
    for (u, v), k in m.items():
        if drop in (u, v):
            continue
        cap[u][v] = cap[u].get(v, 0) + k
        cap[v][u] = cap[v].get(u, 0) + k
    return cap


def classify(cfg):
    T = 0
    for w in TERMS:
        cap = capacities(cfg)
        for o in TERMS:
            if o != w:
                cap[o]['SINK'] = INF
                cap['SINK'][o] = 0
        if maxflow(cap, w, 'SINK') >= 2:
            T += 1
    U = 0
    for w in TERMS:
        a, b = [o for o in TERMS if o != w]
        cap = capacities(cfg, drop=w)
        if a in cap and b in cap and maxflow(cap, a, b) >= 2:
            U += 1
    return T, U


# ------------------------------------------------------ planarity by Euler
def check_embedding(cfg):
    """Euler-check the rotation system of (H with parallels subdivided) + apex."""
    rot = {v: list(ns) for v, ns in cfg['rotation_system'].items()}
    # rebuild the same simple graph the certificate is an embedding of
    edges, k = [], 0
    for (u, v), m in sorted(collections.Counter(
            tuple(sorted(e)) for e in cfg['edges']).items()):
        edges.append((u, v))
        for _ in range(m - 1):
            k += 1
            edges += [(u, f's{k}'), (f's{k}', v)]
    edges += [('apex', t) for t in TERMS]
    adj = collections.defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    if set(rot) != set(adj):
        return False, 'rotation system covers the wrong vertex set'
    for v in rot:
        if set(rot[v]) != adj[v] or len(rot[v]) != len(adj[v]):
            return False, f'rotation at {v} is not its neighbourhood'
    # trace faces: from dart (u,v), go to (v, the neighbour before u at v)
    pos = {v: {w: i for i, w in enumerate(rot[v])} for v in rot}
    darts = {(u, v) for u, v in edges} | {(v, u) for u, v in edges}
    seen, faces = set(), 0
    for d in darts:
        if d in seen:
            continue
        faces += 1
        while d not in seen:
            seen.add(d)
            u, v = d
            r = rot[v]
            d = (v, r[(pos[v][u] - 1) % len(r)])
    V, E = len(adj), len(edges)
    return (V - E + faces == 2), f'V={V} E={E} F={faces}'


# ------------------------------------------------------------ isomorphism
def profile(cfg):
    m = collections.Counter(tuple(sorted(e)) for e in cfg['edges'])
    deg = collections.Counter()
    for (u, v), k in m.items():
        deg[u] += k
        deg[v] += k
    return (len(cfg['internal']), len(cfg['edges']),
            tuple(sorted(deg[t] for t in TERMS)),
            tuple(sorted(deg[i] for i in cfg['internal'])))


def isomorphic(a, b):
    if profile(a) != profile(b):
        return False
    ma = collections.Counter(tuple(sorted(e)) for e in a['edges'])
    mb = collections.Counter(tuple(sorted(e)) for e in b['edges'])
    ia, ib = a['internal'], b['internal']
    for pt in itertools.permutations(TERMS):
        for pi in itertools.permutations(ib):
            f = dict(zip(TERMS, pt))
            f.update(zip(ia, pi))
            if collections.Counter(
                    tuple(sorted((f[u], f[v]))) for u, v in ma.elements()) == mb:
                return True
    return False


# ------------------------------------------------------------------- main
def main(path):
    doc = json.load(open(path))
    C = doc['configurations']
    fails = []
    print(f"configurations: {len(C)}")

    bad = [c['id'] for c in C
           if sorted(c['terminals']) != list(TERMS) or len(c['internal']) > 6]
    print(f"1. three terminals, internal part <= 6 (Thm 17.1(3)): "
          f"{'OK' if not bad else 'FAIL ' + str(bad)}")
    fails += bad

    bad = [(c['id'], (c['T'], c['U']), classify(c))
           for c in C if classify(c) != (c['T'], c['U'])]
    print(f"2. (|T|,|U|) matches Definition 15.21 with multiplicities: "
          f"{'OK' if not bad else 'FAIL ' + str(bad)}")
    fails += bad

    bad = [(c['id'], check_embedding(c)[1]) for c in C
           if not check_embedding(c)[0]]
    print(f"3. rotation system is a planar embedding of H+apex: "
          f"{'OK' if not bad else 'FAIL ' + str(bad)}")
    fails += bad

    bad = [(a['id'], b['id']) for a, b in itertools.combinations(C, 2)
           if isomorphic(a, b)]
    print(f"4. pairwise non-isomorphic: "
          f"{'OK' if not bad else 'FAIL ' + str(bad)}")
    fails += bad

    dist = collections.Counter((c['T'], c['U']) for c in C)
    want = {(3, 3): 20, (3, 2): 3, (2, 1): 5, (1, 0): 2, (0, 0): 1}
    ok = dist == want
    print(f"5. class distribution {dict(sorted(dist.items(), reverse=True))}: "
          f"{'OK' if ok else 'FAIL, expected ' + str(want)}")
    if not ok:
        fails.append('distribution')

    print("\nVERDICT:", "all checks pass" if not fails else f"FAILURES {fails}")
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1
                  else 'figure_15_1_configurations.json'))

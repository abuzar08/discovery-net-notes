"""BORS Remark 17.2: expand the peripherally-4-connected seeds and test.

Theorem 17.1(3): every 3-connected 2-crossing-critical graph with no V10
subdivision that is not V8-containing and is not one of the four graphs of
Theorem 15.6 arises from one of 36 peripherally-4-connected 2-crossing-critical
seeds on at most ten vertices by replacing every degree-3 vertex with one of the
patches of Figure 15.1.  Those patches are now known exactly (31 of them, see
figure_15_1_configurations.json), so the branching at a degree-3 vertex is 31
and a seed with d degree-3 vertices has exactly 31^d expansions.

Expansions are MULTIGRAPHS: the patches carry parallel edges.  Each extra
parallel copy is subdivided before testing.  Subdivision changes neither the
crossing number (a topological invariant) nor 2-crossing-criticality, since
deleting either half of a subdivided edge deletes the original edge -- but the
`validate` mode below checks that claim against the tool rather than assuming it.

Modes:
  validate   -- check subdivision-invariance on graphs with known verdicts
  measure    -- time crit2 on real expansions, report graphs/core-hour
  run D      -- enumerate every expansion of every seed with d <= D, resumably
"""
import collections
import itertools
import json
import os
import random
import subprocess
import sys
import time

import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, '..', 'notes', 'topological-graph-theory',
                    'crossing-number-two-subgraph')
CRIT2 = os.path.join(HERE, 'tools', 'nauty2_9_1', 'crit2_r4')
STATE = os.path.join(HERE, 'expand_state')
CHUNK = 20000


def patches():
    doc = json.load(open(os.path.join(REPO, 'figure_15_1_configurations.json')))
    return [(c['edges'], c['internal']) for c in doc['configurations']]


def seeds():
    sys.path.insert(0, REPO)
    from seeds import peripherally_4_connected
    out = []
    for n in range(6, 11):
        f = os.path.join(REPO, f'n{n}.txt')
        if not os.path.exists(f):
            continue
        for line in open(f):
            p = line.split()
            if len(p) < 4:
                continue
            E = [tuple(map(int, x.split('-')))
                 for x in p[3].strip(',').split(',')]
            G = nx.Graph(E)
            if peripherally_4_connected(G):
                out.append(G)
    return out


def expand(G, d3, assign, P):
    """Replace each degree-3 vertex of G by its assigned patch.

    The patch's three terminals are joined by edges to the vertex's three
    neighbours, then degree-2 vertices are suppressed.  Doing it that way
    rather than identifying each terminal WITH a neighbour is what makes the
    construction well defined when two degree-3 vertices are adjacent: there,
    the edge between them joins a terminal of one patch to a terminal of the
    other, and identification would be circular.  Suppressing the degree-2
    vertices afterwards recovers the smaller representative, and changes
    neither the crossing number nor criticality.
    """
    H = nx.MultiGraph()
    H.add_nodes_from(G.nodes())
    nxt = max(G.nodes()) + 1
    term = {}
    for v, pi in zip(d3, assign):
        edges, internal = P[pi]
        m = {}
        for a in list(internal) + ['x', 'y', 'z']:
            m[a] = nxt
            nxt += 1
        for u, w in edges:
            H.add_edge(m[u], m[w])
        term[v] = {w: m[t] for w, t in zip(G[v], ('x', 'y', 'z'))}
        H.remove_node(v)
    for u, w in G.edges():
        a = term[u][w] if u in term else u
        b = term[w][u] if w in term else w
        H.add_edge(a, b)
    smooth(H)
    return subdivide(H, nxt)


def smooth(H):
    """Suppress degree-2 vertices, keeping the graph a multigraph."""
    changed = True
    while changed:
        changed = False
        for v in [v for v in H if H.degree(v) == 2]:
            nb = [w for w, _ in H.edges(v)]
            nb = [w for e in H.edges(v) for w in e if w != v] or [v, v]
            if len(nb) != 2 or nb[0] == v or nb[1] == v or nb[0] == nb[1]:
                continue
            H.remove_node(v)
            H.add_edge(nb[0], nb[1])
            changed = True


def subdivide(H, nxt):
    """Simple graph with every extra parallel copy subdivided."""
    S = nx.Graph()
    S.add_nodes_from(H.nodes())
    seen = collections.Counter()
    for u, w in H.edges():
        k = tuple(sorted((u, w)))
        seen[k] += 1
        if seen[k] == 1:
            S.add_edge(u, w)
        else:
            S.add_edge(u, nxt)
            S.add_edge(nxt, w)
            nxt += 1
    return S


def g6(G):
    G = nx.convert_node_labels_to_integers(G)
    n = G.number_of_nodes()
    bits = [1 if G.has_edge(i, j) else 0 for j in range(1, n) for i in range(j)]
    s = chr(n + 63)
    for t in range(0, len(bits), 6):
        c = bits[t:t + 6] + [0] * (6 - len(bits[t:t + 6]))
        s += chr(63 + sum(b << (5 - i) for i, b in enumerate(c)))
    return s


def run_crit2(graphs):
    inp = "\n".join(g6(h) for h in graphs) + "\n"
    r = subprocess.run([CRIT2], input=inp, text=True, capture_output=True)
    return r.stdout


# ------------------------------------------------------------------ modes
def validate():
    """Subdividing an edge must not change crit2's verdict."""
    cases = {
        'C3xC3 (cr=3, 2-crossing-critical)': nx.cartesian_product(
            nx.cycle_graph(3), nx.cycle_graph(3)),
        'K5 (cr=1)': nx.complete_graph(5),
        'K33 (cr=1)': nx.complete_bipartite_graph(3, 3),
        'K6 (cr=3)': nx.complete_graph(6),
    }
    print(f"{'graph':<38} {'plain':>28} {'once subdivided':>28}  same?")
    for name, G in cases.items():
        G = nx.convert_node_labels_to_integers(G)
        e = next(iter(G.edges()))
        S = nx.Graph(G)
        S.remove_edge(*e)
        k = max(S.nodes()) + 1
        S.add_edge(e[0], k)
        S.add_edge(k, e[1])
        # compare the VERDICT marker only; the edge list of course differs
        def verdict(txt):
            for ln in txt.split('\n'):
                if ln.startswith('CRIT'):
                    return ln.split()[0]
            return 'not critical'
        fa, fb = verdict(run_crit2([G])), verdict(run_crit2([S]))
        print(f"{name:<38} {fa:>28} {fb:>28}  {'YES' if fa == fb else 'NO'}")


def identity_check():
    """The patch that is a single vertex joined to x, y, z is the identity, so
    assigning it everywhere must return the seed.  If that fails, the expansion
    is wrong and nothing downstream of it means anything."""
    P, S = patches(), seeds()
    ident = [i for i, (edges, internal) in enumerate(P)
             if len(internal) == 1 and len(edges) == 3]
    assert len(ident) == 1, ident
    k = ident[0]
    bad = 0
    for G in S:
        d3 = [v for v, x in G.degree() if x == 3]
        H = expand(G, d3, [k] * len(d3), P)
        if not nx.is_isomorphic(H, G):
            bad += 1
            print(f"  MISMATCH seed n={G.number_of_nodes()} d={len(d3)}: "
                  f"got n={H.number_of_nodes()} m={H.number_of_edges()}, "
                  f"want n={G.number_of_nodes()} m={G.number_of_edges()}")
    print(f"identity patch is #{k+1}; reproduces the seed for "
          f"{len(S)-bad}/{len(S)} seeds")
    # and crit2 must call every seed 2-crossing-critical
    out = run_crit2(S)
    n = sum(1 for l in out.split('\n') if l.startswith('CRIT'))
    print(f"crit2 calls {n}/{len(S)} seeds 2-crossing-critical")


def measure():
    P, S = patches(), seeds()
    for d in (4, 5, 6):
        cand = [g for g in S if sum(1 for _, x in g.degree() if x == 3) == d]
        if not cand:
            continue
        G = cand[0]
        d3 = [v for v, x in G.degree() if x == 3]
        random.seed(11)
        Hs = [expand(G, d3, [random.randrange(31) for _ in d3], P)
              for _ in range(300)]
        ok = [h for h in Hs
              if h.number_of_edges() <= 62 and h.number_of_nodes() <= 28]
        t0 = time.time()
        run_crit2(ok)
        dt = time.time() - t0
        rate = len(ok) / dt
        print(f"d={d}: representable {len(ok)}/{len(Hs)} = {len(ok)/len(Hs):6.1%} "
              f"(n<=28 and m<=62); expansion n up to "
              f"{max(h.number_of_nodes() for h in Hs)}, m up to "
              f"{max(h.number_of_edges() for h in Hs)}; "
              f"{rate*3600:,.0f} graphs/core-hour")
    print()
    bd = collections.Counter(sum(1 for _, x in g.degree() if x == 3) for g in S)
    cum = 0
    for d in sorted(bd):
        cum += bd[d] * 31 ** d
        if d <= 7:
            print(f"  cumulative expansions for d <= {d}: {cum:>20,}")


def run(dmax):
    P, S = patches(), seeds()
    os.makedirs(STATE, exist_ok=True)
    todo = [(i, G) for i, G in enumerate(S)
            if sum(1 for _, x in G.degree() if x == 3) <= dmax]
    print(f"seeds with d <= {dmax}: {len(todo)} of {len(S)}", flush=True)
    for i, G in todo:
        done = os.path.join(STATE, f'seed{i:02d}.done')
        if os.path.exists(done):
            continue
        d3 = [v for v, x in G.degree() if x == 3]
        total = 31 ** len(d3)
        t0 = time.time()
        crit = ge3 = big = 0
        buf = []
        hits = []
        for j, assign in enumerate(itertools.product(range(31),
                                                     repeat=len(d3))):
            H = expand(G, d3, assign, P)
            # crit2 exits on n > 28 (MAXV 32) or M >= 63, so both bounds must
            # be filtered here, and both must be reported: a graph skipped for
            # either reason is NOT covered by the result
            if H.number_of_edges() > 62 or H.number_of_nodes() > 28:
                big += 1
                continue
            buf.append((assign, H))
            if len(buf) >= CHUNK or j == total - 1:
                out = run_crit2([h for _, h in buf])
                for line in out.split('\n'):
                    if line.startswith('CRIT2'):
                        crit += 1
                    elif line.startswith('CRIT_GE3'):
                        crit += 1
                        ge3 += 1
                        hits.append(line.strip())
                buf = []
        with open(done, 'w') as f:
            json.dump({'seed': i, 'n': G.number_of_nodes(),
                       'm': G.number_of_edges(), 'd': len(d3),
                       'expansions': total, 'skipped_over_62_edges': big,
                       'crossing_critical': crit, 'cr_ge_3': ge3,
                       'hits': hits[:200], 'seconds': round(time.time() - t0, 1)},
                      f, indent=1)
        print(f"seed {i:02d}: n={G.number_of_nodes()} d={len(d3)} "
              f"{total:,} expansions, {big:,} over 62 edges, "
              f"{crit:,} critical, {ge3:,} with cr>=3, "
              f"{time.time()-t0:.0f}s", flush=True)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'validate':
        validate()
    elif mode == 'identity':
        identity_check()
    elif mode == 'measure':
        measure()
    elif mode == 'run':
        run(int(sys.argv[2]))

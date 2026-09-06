"""BORS Section 15.7 / Lemma 15.27: the replacement construction, corrected.

Three ingredients that the summary statement of Theorem 17.1(3) leaves implicit:

  1. the base L is any non-planar peripherally-4-connected graph, in particular
     one with cr(L) = 1 -- not only the 2-crossing-critical ones;
  2. "For each edge of L joining two vertices of degree at least 4, we decide
     whether the edge will be a single edge or a parallel pair";
  3. "The choices must be made so that x in T_v if and only if v in T_x".

Ingredient 3 makes the type assignment a symmetric relation on the degree-3
vertices, so choosing all the T_v at once is the same as choosing a SPANNING
SUBGRAPH H of L restricted to its degree-3 vertices: T_v is the set of
H-neighbours of v.  In particular H empty gives every vertex type (0,0), whose
only configuration is the claw, which is the identity -- so the base is always
among its own expansions, and the seeds reproduce themselves.

Once the type of v is fixed, Lemma 15.27 replaces K_v by a configuration of that
class, oriented so that the configuration's own T set lands on T_v.
"""
import collections
import itertools
import json
import os

import networkx as nx

import expand_run as R

TERMS = ('x', 'y', 'z')


def load_configs():
    """The 31 configurations, each with its T and U as SETS of terminals."""
    doc = json.load(open(os.path.join(R.REPO,
                                      'figure_15_1_configurations.json')))
    out = []
    for c in doc['configurations']:
        mult = collections.Counter(tuple(sorted(e)) for e in c['edges'])
        T, U = tu_sets(mult, c['internal'])
        dn, dm = deltas(c)
        # dn is the vertex cost under the OLD attachment model, kept only for
        # comparison; build2 identifies terminals with the neighbours, so the
        # patch contributes its internal vertices and consumes the replaced one
        out.append(dict(edges=c['edges'], internal=c['internal'],
                        T=T, U=U, dn=dn, dm=dm, id=c['id'],
                        cost=len(c['internal']) - 1))
    return out


def tu_sets(mult, internal):
    nodes = list(TERMS) + list(internal)
    C = nx.Graph()
    C.add_nodes_from(nodes)
    for (u, v), m in mult.items():
        C.add_edge(u, v, capacity=m)
    T = set()
    for w in TERMS:
        D = C.copy()
        D.add_node('SINK')
        for t in TERMS:
            if t != w:
                D.add_edge(t, 'SINK', capacity=10 ** 6)
        if nx.maximum_flow_value(D, w, 'SINK', capacity='capacity') >= 2:
            T.add(w)
    U = set()
    for w in TERMS:
        a, b = [t for t in TERMS if t != w]
        D = C.copy()
        D.remove_node(w)
        if a in D and b in D and nx.has_path(D, a, b) and \
                nx.maximum_flow_value(D, a, b, capacity='capacity') >= 2:
            U.add(w)
    return frozenset(T), frozenset(U)


def deltas(c):
    mult = collections.Counter(tuple(sorted(e)) for e in c['edges'])
    extras = sum(m - 1 for m in mult.values())
    return len(c['internal']) + extras - 1, len(c['edges']) - 3 + extras


def place(H, v, nbrs, cfg, perm, nxt):
    """Insert cfg at v, mapping terminals (x,y,z) to nbrs via perm."""
    m = {}
    for a in list(cfg['internal']) + list(TERMS):
        m[a] = nxt
        nxt += 1
    for u, w in cfg['edges']:
        H.add_edge(m[u], m[w])
    term = {nbrs[perm[i]]: m[t] for i, t in enumerate(TERMS)}
    return term, nxt


def build(L, assign, dup=()):
    """assign: v -> (cfg, perm) with perm a tuple mapping terminal index to
    neighbour index.  dup: edges of L to draw as a parallel pair."""
    H = nx.MultiGraph()
    H.add_nodes_from(L.nodes())
    nxt = max(L.nodes()) + 1
    term = {}
    for v, (cfg, perm) in assign.items():
        nbrs = list(L[v])
        t, nxt = place(H, v, nbrs, cfg, perm, nxt)
        term[v] = t
        H.remove_node(v)
    for u, w in L.edges():
        a = term[u][w] if u in term else u
        b = term[w][u] if w in term else w
        H.add_edge(a, b)
        if (min(u, w), max(u, w)) in dup:
            H.add_edge(a, b)
    R.smooth(H)
    return R.subdivide(H, nxt)


def type_subgraphs(L, d3):
    """Every symmetric type assignment: a subgraph of L[d3]."""
    E = [e for e in L.edges() if e[0] in d3 and e[1] in d3]
    for k in range(len(E) + 1):
        for S in itertools.combinations(E, k):
            yield S


def configs_for(cfgs, T_size, U_size):
    return [c for c in cfgs if len(c['T']) == T_size and len(c['U']) == U_size]


def terminal_autos(cfg):
    """Permutations of (x,y,z) extending to an automorphism of the patch.

    Orientations differing by one of these give the same expansion, so only
    coset representatives need to be tried.  Without this the claw alone, which
    is fully symmetric, contributes 6 identical placements at every vertex.
    """
    mult = collections.Counter(tuple(sorted(e)) for e in cfg['edges'])
    base = _key(mult, {})
    autos = []
    for p in itertools.permutations(TERMS):
        sub = dict(zip(TERMS, p))
        if _key(mult, sub) == base:
            autos.append(p)
    return autos


def _key(mult, sub):
    G = nx.Graph()
    k = 0
    for (u, v), m in sorted(mult.items()):
        u, v = sub.get(u, u), sub.get(v, v)
        G.add_edge(u, v)
        for _ in range(m - 1):
            k += 1
            G.add_node(f'#{k}')
            G.add_edge(u, f'#{k}')
            G.add_edge(f'#{k}', v)
    for n in G.nodes():
        G.nodes[n]['t'] = ('x', 'y', 'z').index(n) + 1 if n in TERMS else 0
    return nx.weisfeiler_lehman_graph_hash(G, node_attr='t', iterations=5)


def perm_reps(cfg):
    """One representative permutation per coset of the terminal automorphisms."""
    autos = set(terminal_autos(cfg))
    idx = {t: i for i, t in enumerate(TERMS)}
    seen, reps = set(), []
    for perm in itertools.permutations(range(3)):
        canon = min(tuple(perm[idx[a]] for a in p) for p in autos)
        if canon in seen:
            continue
        seen.add(canon)
        reps.append(perm)
    return reps


def ports(cfg, perm, nbrs):
    """For each neighbour, the multiset of internal endpoints joined to it.

    Definition 15.22 takes x, y, z to BE the three neighbours of v, so the patch
    is K_v = G_v - {x,y,z} and the configuration's terminal edges say how K_v
    attaches.  When the neighbour is itself replaced, those edges must meet the
    other patch's edges back, so the two multiplicities have to agree -- which
    is a real constraint on which pairs of configurations may sit on an edge.
    """
    m = {C_: nbrs[perm[i]] for i, C_ in enumerate(TERMS)}
    out = {w: [] for w in nbrs}
    for u, v in cfg['edges']:
        if u in TERMS and v in TERMS:
            continue
        if u in TERMS:
            out[m[u]].append(v)
        elif v in TERMS:
            out[m[v]].append(u)
    return out


def build2(L, assign, dup=(), pairings=None):
    """The corrected replacement: terminals ARE the neighbours."""
    H = nx.MultiGraph()
    nxt = max(L.nodes()) + 1
    inst, port = {}, {}
    for v, (cfg, perm) in assign.items():
        ren = {}
        for a in cfg['internal']:
            ren[a] = nxt
            nxt += 1
        inst[v] = ren
        for u, w in cfg['edges']:
            if u in TERMS or w in TERMS:
                continue
            H.add_edge(ren[u], ren[w])
        port[v] = {w: [ren[a] for a in lst]
                   for w, lst in ports(cfg, perm, list(L[v])).items()}
    for v in L.nodes():
        if v not in assign:
            H.add_node(v)
    for u, w in L.edges():
        eu = port[u][w] if u in assign else None
        ew = port[w][u] if w in assign else None
        if eu is not None and ew is not None:
            if len(eu) != len(ew):
                return None                      # multiplicities disagree
            k = (pairings or {}).get(tuple(sorted((u, w))), 0)
            tgt = ew if k == 0 else ew[::-1]
            for a, b in zip(eu, tgt):
                H.add_edge(a, b)
        elif eu is not None:
            for a in eu:
                H.add_edge(a, w)
        elif ew is not None:
            for b in ew:
                H.add_edge(b, u)
        else:
            H.add_edge(u, w)
            if tuple(sorted((u, w))) in dup:
                H.add_edge(u, w)
    R.smooth(H)
    return R.subdivide(H, nxt)

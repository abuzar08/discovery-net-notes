"""How much would exact isomorphism deduplication collapse the search tree?

Branches that planarise the same crossings in a different order reach isomorphic
graphs, and the subtree below an isomorphic graph is the same question.  This
measures the collapse per level.

Deduplication is done with networkx's exact isomorphism test, deliberately NOT a
Weisfeiler-Lehman hash: WL is an invariant but not a complete one, so using it as
the sole key would silently merge non-isomorphic graphs and could return a wrong
answer.  WL is used only to bucket candidates before exact comparison, which is
sound because non-isomorphic graphs never need to be compared across buckets.
"""
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher

G = nx.complete_graph(8)
for a, b in [(0, 1), (2, 3), (4, 5)]:
    G.remove_edge(a, b)

def children(H):
    ok, K = nx.check_planarity(H, counterexample=True)
    if ok:
        return []
    KE = list(K.edges())
    out = []
    for i, e in enumerate(KE):
        for f in KE[i+1:]:
            if set(e) & set(f):
                continue
            J = H.copy(); J.remove_edge(*e); J.remove_edge(*f)
            d = ("x", len(out), H.number_of_nodes())
            for u in e + f:
                J.add_edge(u, d)
            out.append(J)
    return out

def dedup(gs):
    buckets = {}
    for g in gs:
        key = (g.number_of_nodes(), g.number_of_edges(),
               nx.weisfeiler_lehman_graph_hash(g, iterations=3))
        for rep in buckets.setdefault(key, []):
            if GraphMatcher(rep, g).is_isomorphic():   # exact, not the hash
                break
        else:
            buckets[key].append(g)
    return [g for v in buckets.values() for g in v]

level = [G]
raw_prod = 1
print(f"{'depth':>5} {'raw':>10} {'distinct':>9} {'collapse':>9}")
for d in range(1, 5):
    raw = [c for H in level for c in children(H)]
    uniq = dedup(raw)
    print(f"{d:>5} {len(raw):>10} {len(uniq):>9} {len(raw)/max(1,len(uniq)):>8.1f}x",
          flush=True)
    level = uniq
    if len(uniq) > 4000:
        print("  (stopping: level too large to dedup exactly at this budget)")
        break

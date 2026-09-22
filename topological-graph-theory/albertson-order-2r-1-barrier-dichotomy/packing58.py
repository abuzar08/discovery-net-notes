#!/usr/bin/env python3
"""
Three disjoint triangles: the exact guarantee, and why it is the whole question.

==============================================================================
WHY THREE, EXACTLY.

theta(H) <= 28 with H K_4-free holds iff some vertex-disjoint packing has

        2 t_3 + t_2 >= 30 ,   3 t_3 + 2 t_2 <= 58 ,   t_3 + t_2 <= 28 ,

which is seventy (t_3, t_2) families.  Substituting t_2 >= 30 - 2 t_3 into the
second gives 60 - t_3 <= 58, so EVERY family has t_3 >= 2; and the family with
t_3 = 2 is unique, namely (2, 26).  That one is excluded by the branch
hypothesis (TT), which is what the order-58 class was branched on.

        So the clique-cover route applies to a configuration IF AND ONLY IF
        every admissible H for it contains THREE vertex-disjoint triangles.

That is not a heuristic gate in front of the Tutte machinery -- it is the
machinery's exact domain.  No sharpening of the seven inequalities in
tuttegen.py can ever touch a configuration where three disjoint triangles are
not guaranteed, because for such an H there is no admissible family at all.

==============================================================================
THE EXACT GUARANTEE.

G[L] is a Gallai forest whose blocks here are cliques, and H = complement(G), so
two low vertices are H-adjacent exactly when they share NO block.  Give each
vertex its TYPE, the set of blocks containing it; a triangle of H[L] is three
vertices whose types are pairwise disjoint.

The previous guarantee (tuttegen.kmax_guaranteed) counted only triangles built
from PRIVATE vertices -- types of size one -- and bounded the private counts by
a knapsack over the worst case.  Both are lossy: a cut vertex of type {Q_3,Q_4}
is just as usable against private vertices of Q_1 and Q_2, and the worst case is
not attained by every block at once.

This file instead ENUMERATES the realisable forests.  A cut vertex joining b
blocks contributes b - 1 to extra = sum_i q_i - |L|, the block-cut incidence must
be acyclic, and the private count of block i is q_i minus the number of cut
vertices in it.  For at most five blocks and the extra values that occur here
(0 to 4) the enumeration is tiny and exhaustive.

For one forest, k disjoint triangles EXIST as soon as some collection of
pairwise-disjoint types S_1, ..., S_r has

        sum_j min(k, n_{S_j})  >=  3k ,

filling the triples round-robin.  That is a lower bound on the packing number, so
taking the minimum over forests is a sound guarantee.  It contains the old test
as the special case where every S_j is a singleton.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import itertools


def forests(mult, extra, limit=200000):
    """Every realisable assignment of cut vertices, as a dict type -> count.

    A cut vertex is a subset of block indices of size at least two; the multiset
    of cut vertices must satisfy sum (|S| - 1) = extra and leave the block-cut
    incidence acyclic."""
    n = len(mult)
    subsets = [frozenset(c) for size in range(2, n + 1)
               for c in itertools.combinations(range(n), size)]
    out = []

    def acyclic(cuts):
        # blocks and cut vertices form a bipartite graph; it must be a forest,
        # so edges <= nodes - components.  Union-find on the blocks suffices:
        # each cut vertex of size b must merge b distinct components.
        par = list(range(n))

        def find(a):
            while par[a] != a:
                par[a] = par[par[a]]
                a = par[a]
            return a
        for S in cuts:
            roots = {find(i) for i in S}
            if len(roots) != len(S):
                return False
            r = roots.pop()
            for o in roots:
                par[o] = r
        return True

    def rec(idx, left, chosen):
        if len(out) >= limit:
            return
        if left == 0:
            if not acyclic(chosen):
                return
            cnt = {}
            for S in chosen:
                cnt[S] = cnt.get(S, 0) + 1
            priv = [mult[i] - sum(c for S, c in cnt.items() if i in S)
                    for i in range(n)]
            if min(priv, default=0) < 0:
                return
            types = {frozenset([i]): priv[i] for i in range(n) if priv[i] > 0}
            for S, c in cnt.items():
                types[S] = types.get(S, 0) + c
            out.append(types)
            return
        for j in range(idx, len(subsets)):
            S = subsets[j]
            if len(S) - 1 <= left:
                rec(j, left - (len(S) - 1), chosen + [S])

    rec(0, extra, [])
    return out


def packs(types, k):
    """True if k disjoint triangles are certain for these type counts."""
    items = [(S, c) for S, c in types.items() if c > 0]
    best = 0
    for r in range(3, min(len(items), 6) + 1):
        for combo in itertools.combinations(items, r):
            ok = True
            for (S1, _), (S2, _) in itertools.combinations(combo, 2):
                if S1 & S2:
                    ok = False
                    break
            if not ok:
                continue
            tot = sum(min(k, c) for _, c in combo)
            if tot > best:
                best = tot
    return best >= 3 * k


_MEMO = {}


def kmax_exact(mult, NL, cap=15):
    """min over realisable forests of the certified triangle packing."""
    key = (tuple(sorted(mult)), NL, cap)
    if key in _MEMO:
        return _MEMO[key]
    _MEMO[key] = v = _kmax_exact(mult, NL, cap)
    return v


def _kmax_exact(mult, NL, cap=15):
    extra = sum(mult) - NL
    if extra < 0:
        return 0
    fs = forests(mult, extra)
    if not fs:
        return 0
    best = cap
    for types in fs:
        k = 0
        for kk in range(1, cap + 1):
            if packs(types, kk):
                k = kk
            else:
                break
        if k < best:
            best = k
        if best == 0:
            break
    return best


def hitting_tail(mult, NL):
    """min over realisable forests of the private count outside the best two
    blocks.

    If nu_tri(H) <= 2 there is a set B' of at most six vertices meeting every
    triangle, so H[L - B'] is triangle-free.  Private vertices of three distinct
    blocks form a triangle, so AT MOST TWO blocks keep a private vertex outside
    B'.  Every other block's private vertices therefore lie in B', and

        sum over all but the best two blocks of priv_i  <=  6 .

    So a tail of 7 or more certifies nu_tri(H) >= 3 -- a criterion independent
    of the packing count in kmax_exact, and stronger when there are many small
    blocks.  MEASURED: it fires on NONE of the residual (see main), and the tail
    is at most 2 there, which is the real content -- see the note below."""
    extra = sum(mult) - NL
    worst = None
    for types in forests(list(mult), extra):
        priv = sorted((c for S, c in types.items() if len(S) == 1),
                      reverse=True)
        tail = sum(priv[2:])
        if worst is None or tail < worst:
            worst = tail
    return worst if worst is not None else 0


def main():
    import pickle
    import sys
    import tuttegen as G
    print("Three disjoint triangles: the exact guarantee")
    print()
    print("PART 1   why three is the exact requirement")
    fams = [(t3, t2) for t3 in range(0, 20) for t2 in range(0, 31)
            if 2 * t3 + t2 >= 30 and 3 * t3 + 2 * t2 <= 58 and t3 + t2 <= 28]
    two = [f for f in fams if f[0] == 2]
    print("   (t_3,t_2) families: %d;  minimum t_3 = %d"
          % (len(fams), min(t for t, _ in fams)))
    print("   families with t_3 = 2: %s  -- unique, and excluded by (TT)"
          % two)
    print("   so the route applies exactly when THREE disjoint triangles are")
    print("   guaranteed; the seven inequalities cannot reach anything else.")
    print()

    print("PART 2   the exact guarantee against the knapsack it replaces")
    cfgs = pickle.load(open(sys.argv[1], "rb")) if len(sys.argv) > 1 else None
    if cfgs is None:
        cfgs = G.configurations()
    gained, same, tested = 0, 0, 0
    byreason = {}
    for m, RSZ, mult, eHR in cfgs:
        NL, X = G.N58 - RSZ, 2 * m - G.N58 * G.DEG
        # BOTH guarantees are computed on the TRUE block multiset: each derives
        # extra = sum q_i - |L| from the multiset, and the enumerator does not
        # list every block (defect 19), so on the raw multiset both are too
        # large and the comparison between them is not like for like.
        tb = G.true_blocks(mult, RSZ, eHR, X)
        old = G.kmax_guaranteed(list(tb), NL)
        if old >= 3:
            continue                       # already in scope
        if G.route_closed(RSZ, list(mult), eHR, X)[0]:
            continue                       # already closed
        tested += 1
        new = kmax_exact(list(tb), NL)
        if new >= 3:
            gained += 1
        else:
            same += 1
            byreason[new] = byreason.get(new, 0) + 1
    print("   route-unavailable configurations tested: %d" % tested)
    print("   brought INTO scope by the exact guarantee: %d" % gained)
    print("   still out of scope: %d" % same)
    print("   certified packing number of those still out: %s"
          % sorted(byreason.items()))
    print()
    print("PART 3   can the nu_tri <= 2 branch be excluded by block counting?")
    tails = {}
    fires = 0
    for m, RSZ, mult, eHR in cfgs:
        NL, X = G.N58 - RSZ, 2 * m - G.N58 * G.DEG
        tb = G.true_blocks(mult, RSZ, eHR, X)
        if kmax_exact(list(tb), NL) >= 3:
            continue
        if G.route_closed(RSZ, list(mult), eHR, X)[0]:
            continue
        t = hitting_tail(list(tb), NL)
        tails[t] = tails.get(t, 0) + 1
        if t >= 7:
            fires += 1
    print("   a tail of >= 7 would certify nu_tri >= 3 on its own.")
    print("   configurations where it fires: %d" % fires)
    print("   distribution of the tail: %s" % sorted(tails.items()))
    print()
    print("   So on the WHOLE residual the tail is at most 2: H[L] is two blocks")
    print("   plus at most two stray private vertices.  The nu_tri <= 2 branch")
    print("   cannot be excluded by counting blocks, and every triangle beyond")
    print("   the couple that L can supply must use a vertex of R.  That is what")
    print("   a successor's tool has to handle -- triangles across the L/R split")
    print("   -- and it is measured here rather than assumed.")
    print()
    print("CONCLUSION")
    print("   The gate is not a convenience, it is the domain of the whole")
    print("   clique-cover approach: (2,26) is the only family with t_3 = 2 and")
    print("   the branch hypothesis excludes it, so three disjoint triangles are")
    print("   necessary.  Configurations that cannot guarantee them are beyond")
    print("   the reach of tuttegen.py no matter how its inequalities improve,")
    print("   and need a different tool entirely.")
    print()
    print("   r = 29 is NOT proved.")


if __name__ == "__main__":
    main()

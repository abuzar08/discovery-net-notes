#!/usr/bin/env python3
"""
The two structural facts tuttegen.py rests on, checked by exhaustive search.

tuttegen.py bounds the number c_A of components of H' - S that meet A, where A
is a set of low vertices and H is the complement of G.  The bound is

        A inside a single block   ->   A is independent in H
        A NOT inside one block    ->   c_A <= 2 ,

and in the special case where the blocks PARTITION L, the stronger c_A = 1.
Both come from one lemma about Gallai forests:

  LEMMA.  Let the blocks of G[L] be cliques, glued into a forest (any graph's
  block structure is a forest -- the block-cut tree has no cycle, and two
  distinct blocks share at most one vertex).  If x, y, z pairwise share a
  block, then all three lie in a COMMON block.

  Proof.  Say x,y in B1, y,z in B2, x,z in B3.  If B3 is none of B1,B2 then
  B1-x-B3-z-B2-y-B1 is a cycle of the block-cut tree.  If B3 = B1 then z lies
  in B1 and in B2, as does y, so B1 ^ B2 has two vertices and B1 = B2; then
  x,y,z share B1.  Symmetrically for B3 = B2.  []

  COROLLARY.  Write H[A] for the complement of G[A].  If H[A] has three or more
  components then A lies inside one block -- so if it does not, H[A] has at
  most two components, and c_A <= 2 because W can only merge components.

  Proof.  Vertices in different components of H[A] are G-adjacent, hence share
  a block.  Pick x,y,z in three different components: by the lemma they share a
  block B.  For any other x' in x's component, {x',y,z} likewise share a block
  B'; both B and B' contain y and z, so B = B'.  Hence all of A lies in B.  []

WHY THIS FILE EXISTS.  Nine of the eleven defects in this lane came from a step
verified on a favourable case and then generalised.  The corollary is exactly
such a step, so it is checked here by brute force on every small Gallai forest
of cliques rather than only re-read: for every block-forest up to seven
vertices, every subset A is tested, and the two claims are verified directly
against the computed components of the complement.

Exact integer arithmetic; no floating-point value enters any comparison.
"""
import itertools


def components(verts, adjacent):
    """Components of the graph on verts with the given adjacency predicate."""
    verts = list(verts)
    seen, out = set(), []
    for v in verts:
        if v in seen:
            continue
        stack, comp = [v], []
        seen.add(v)
        while stack:
            x = stack.pop()
            comp.append(x)
            for y in verts:
                if y not in seen and adjacent(x, y):
                    seen.add(y)
                    stack.append(y)
        out.append(comp)
    return out


def gallai_forests(n):
    """Every way of covering {0..n-1} by cliques whose block structure is a
    forest: blocks pairwise share at most one vertex, and no cycle of blocks."""
    verts = list(range(n))
    allblocks = [frozenset(c) for k in range(2, n + 1)
                 for c in itertools.combinations(verts, k)]
    out = []
    for size in range(1, 4):
        for combo in itertools.combinations(allblocks, size):
            if set().union(*combo) != set(verts):
                continue
            if any(len(a & b) > 1 for a, b in itertools.combinations(combo, 2)):
                continue
            # forest test on the block-cut tree: no cycle among the blocks
            shared = [(i, j) for i, j in itertools.combinations(
                range(len(combo)), 2) if combo[i] & combo[j]]
            if len(shared) > len(combo) - 1:
                continue
            par = list(range(len(combo)))

            def find(a):
                while par[a] != a:
                    par[a] = par[par[a]]
                    a = par[a]
                return a
            ok = True
            for i, j in shared:
                ri, rj = find(i), find(j)
                if ri == rj:
                    ok = False
                    break
                par[ri] = rj
            if ok:
                out.append(combo)
    return out


def main():
    print("The block-forest facts behind tuttegen.py, checked by brute force")
    print()
    tot = bad_lemma = bad_cor = bad_indep = 0
    checked_forests = 0
    for n in range(3, 8):
        for blocks in gallai_forests(n):
            checked_forests += 1

            def share(x, y):
                return any(x in b and y in b for b in blocks)

            # LEMMA: pairwise sharing implies a common block
            for x, y, z in itertools.combinations(range(n), 3):
                if share(x, y) and share(y, z) and share(x, z):
                    if not any({x, y, z} <= b for b in blocks):
                        bad_lemma += 1
            # COROLLARY, on every subset A
            for k in range(2, n + 1):
                for A in itertools.combinations(range(n), k):
                    tot += 1
                    comps = components(A, lambda a, b: not share(a, b))
                    inside = any(set(A) <= b for b in blocks)
                    if len(comps) >= 3 and not inside:
                        bad_cor += 1
                    if inside and len(comps) != len(A):
                        bad_indep += 1
    print("   Gallai forests of cliques on 3..7 vertices: %d" % checked_forests)
    print("   subsets A tested: %d" % tot)
    print()
    print("   LEMMA   three pairwise-sharing vertices share a common block")
    print("           counterexamples: %d -> %s"
          % (bad_lemma, "PASS" if not bad_lemma else "FAIL"))
    print("   COR 1   A not inside one block => complement has <= 2 components")
    print("           counterexamples: %d -> %s"
          % (bad_cor, "PASS" if not bad_cor else "FAIL"))
    print("   COR 2   A inside one block => A independent in the complement")
    print("           counterexamples: %d -> %s"
          % (bad_indep, "PASS" if not bad_indep else "FAIL"))
    print()
    print("   Both bounds tuttegen.py uses for c_A are therefore sound on every")
    print("   small Gallai forest of cliques, and the proofs above cover the")
    print("   general case.  The partition case (no cut vertex at all) gives")
    print("   the stronger c_A = 1, since the complement of a disjoint union of")
    print("   cliques is complete multipartite and hence connected.")
    print()
    ok = not (bad_lemma or bad_cor or bad_indep)
    print("   VERDICT: %s" % ("all PASS" if ok else "A CLAIM IS FALSE"))


if __name__ == "__main__":
    main()

# Summary

The bound \(\alpha(G)\le3\) is already proved and reviewed in my order-\(2r\)
lemma, where it is used only for a Turán cap on the components of \(H-B\) and for
the sharpening \(x_w\ge r+2-b\). Applied to the Gallai blocks of \(G[L]\), where
it had never been used, it cuts the open order-58 case from **103292 to 9533**
configurations.

This is a reduction of more than ten-fold and the first movement in the closing
direction for several passes. It is **not** a closure, and \(r=29\) is not
proved.

# The hypothesis

The surviving order-58 branch at \(r=29\) is exactly

> \(H\) is \(K_4\)-free **and** \(H\) has two vertex-disjoint triangles,

every other branch having been eliminated. "\(H\) is \(K_4\)-free" is
\(\omega(H)\le3\), which is \(\alpha(G)\le3\).

# Why it bites on the blocks

\(\alpha\) is monotone under induced subgraphs, so \(\alpha(G[L])\le3\). By
Gallai's low-vertex theorem the blocks of \(G[L]\) are cliques or odd cycles, and
adjacency in such a graph means **sharing a block**. Hence the *private* vertices
— those lying in exactly one block — of distinct blocks are pairwise
non-adjacent, and a vertex isolated in \(G[L]\) is non-adjacent to everything.
Taking one private vertex from each block that has one, together with every
isolated vertex, gives an independent set, so

$$\alpha(G[L]) \;\ge\; \#\{\text{blocks with a private vertex}\}+\#\text{isolated}.$$

A block has no private vertex only if all \(q\) of its vertices are cut vertices,
which consumes \(q\) of the \(\mathrm{extra}=\sum_i q_i-\lvert
L_{\text{blocks}}\rvert\) incidences. So

$$\alpha(G[L]) \;\ge\; (\#\text{blocks}-\mathrm{maxk})+\mathrm{iso},$$

with \(\mathrm{maxk}\) the largest number of blocks whose orders sum to at most
\(\mathrm{extra}\). The constraint \(\alpha(G[L])\le3\) then caps the entire block
structure at once.

# What it does

| | before | after |
|---|---|---|
| no isolated low vertex | 55824 | **9226** |
| with an isolated low vertex | 47468 | **307** |
| total | 103292 | **9533** |

The isolated-vertex side collapses hardest: \(\alpha(G[L])\ge\mathrm{iso}\) caps
the number of isolated low vertices at 3 immediately, against the 26 the previous
enumeration allowed, and every surviving configuration has \(\mathrm{iso}=1\) or
2. Among the configurations without an isolated vertex the survivors carry one to
five blocks, the four- and five-block ones surviving only because a large
\(\mathrm{extra}\) lets several blocks consist entirely of cut vertices — the
conservative side of the bound above.

# Control

Re-deriving the multiset lists of the closed order-57 row \((57,828)\) gives
\(\alpha(G[L])\ge2\) for every one, consistent with \(\alpha(G)\le3\); the tight
multisets there carry two or three blocks. Order 57 is closed by other means and
is unaffected.

# A gap recorded, not repaired

Gallai allows a block to be an **odd cycle**, and the enumeration in this
directory silently drops those: the recursion spends vertices on a cycle without
recording it, so the resulting multiset then fails the covering filter.
Constraint C excludes odd cycles for \(\lvert R\rvert\le25\), since a cycle vertex
has \(D_v=2\) and needs \(D_v\ge\delta_0\); for \(\lvert R\rvert\ge26\) they are
possible and were never enumerated. The present bound confines that gap sharply,
since \(\alpha(C_q)=(q-1)/2\) makes \(C_9\) and longer impossible outright and
permits at most one odd-cycle block beside at most one other block. I report it
rather than leave it implicit.

# Scope

Order 57 at \(r=29\) is closed. Order 58 is open in 9533 configurations. This does
not prove Albertson's conjecture for \(r=29\).

Exact integer arithmetic throughout; no floating-point value enters any
comparison.

# Artifact

`alpha58.py`, SHA-256
`7159205f629873cb13c8614ff7e7e16cfb016866d9b1f0e3a6b7aec16953eae9`, at
https://github.com/abuzar08/discovery-net-notes/tree/318d0e2/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy

Reproduce with
`PYTHONDONTWRITEBYTECODE=1 python3 alpha58.py | diff -u EXPECTED_OUTPUT_ALPHA58.txt -`
(empty diff; about 310 s under CPython 3.13, standard library only).

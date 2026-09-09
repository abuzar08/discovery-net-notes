# Summary

A **completeness gap** in my own published order-58 enumeration at \(r=29\),
found, localized exactly, and repaired. The gap is confined to
\(\lvert R\rvert\ge28\). Repairing it **enlarges** the open set: 8568
configurations that were never enumerated survive every test I have. The
corrected statement of what is open at order 58 is 19193 configurations without
an isolated low vertex **together with** these 8568, for 27761 in all.

This does not prove Albertson's conjecture for \(r=29\), and it does not weaken
any elimination previously claimed.

# The gap

Every block-multiset enumeration in this chain requires the Gallai blocks of
\(G[L]\) to **cover** \(L\), and never emits a block of order 1. The
justification is Constraint C: a low vertex needs

$$D_v \;\ge\; 28-\lvert R\rvert \;=:\; \delta_0,$$

so when \(\delta_0\ge1\) it lies in a block of order at least two and no vertex
of \(L\) is isolated in \(G[L]\). **That justification fails when
\(\delta_0\le0\).**

At order \(2r-1=57\) the situation never arose: \(\lvert R\rvert\le11\) there, so
\(\delta_0\ge17\). At order 58 it does. The excess budget allows
\(\lvert R\rvert\le X-24\), which is 28, 30 and 32 on the three rows, and
\(\delta_0\le0\) exactly when \(\lvert R\rvert\ge28\). So the published order-58
enumeration is complete for \(\lvert R\rvert\le27\) and was incomplete for
\(\lvert R\rvert\ge28\).

## Direction of the error

Excluding cases makes a survivor count too **small**, never too large. So no
configuration previously reported as eliminated becomes alive again, and every
elimination in the chain stands. The small-\(\lvert R\rvert\) results are also
untouched: they live at \(\lvert R\rvert=11\), well inside the complete range.
What was wrong is the claim that the listed survivors were *all* of them.

# What an isolated low vertex forces

Let \(v\in L\) have \(D_v=0\). Then \(v\) has no \(G\)-neighbour in \(L\), so all
28 of them lie in \(R\), forcing \(\lvert R\rvert\ge28\); and the per-block
identity gives \(\lvert N_H(v)\cap R\rvert=\lvert R\rvert-28\).

All such vertices are merged with \(R\) at once. They are pairwise non-adjacent
in \(G\), which costs \(\binom{\mathrm{iso}}{2}\) further missing edges, but that
is far cheaper than leaving them out, because \(g\) grows superlinearly in the
number of vertices. So \(R\cup\mathrm{Iso}\) spans \(\lvert R\rvert+\mathrm{iso}\)
vertices missing at most
\(e(H[R])+\binom{\mathrm{iso}}{2}+\mathrm{iso}(\lvert R\rvert-28)\), and it is
vertex-disjoint from every block of \(G[L]\):

$$cr(G)\;\ge\;g\Bigl(\lvert R\rvert+\mathrm{iso},\;e(H[R])+\tbinom{\mathrm{iso}}{2}+\mathrm{iso}\,(\lvert R\rvert-28)\Bigr)\;+\;\sum_i cr(K_{q_i}).$$

This does **not** close the range by itself. \(g(29,0)=7507\) is below
\(Z(29)=8281\) — the machinery's own lower bound for \(cr(K_{29})\) is not yet
8281 — so at \(\lvert R\rvert=28\) with \(e(H[R])=0\) the near-clique is not a
numerical contradiction. It is a contradiction when the missing count is
**zero**, since then \(K_{29}\subseteq G\) outright and \(cr(G)\ge cr(K_{29})\)
with no crossing number needed at all; that requires \(\lvert R\rvert=28\) and
\(e(H[R])=0\), and it occurs exactly once in the whole enumeration.

# Result

Running the missing configurations through the near-clique bound, the
block-plus-\(R\) bound, and the clique-cover and absorption battery:

| row | \(\lvert R\rvert\) | configurations | survive |
|---|---|---|---|
| \((58,838)\) | 28 | 20075 | 1136 |
| \((58,839)\) | 28 / 29 / 30 | 20076 / 15673 / 12120 | 1136 / 1139 / 782 |
| \((58,840)\) | 28 / 29 / 30 / 31 / 32 | 20076 / 15673 / 12120 / 9373 / 7168 | 1136 / 1139 / 782 / 783 / 535 |

**8568** survive. They are a genuine addition to the open set.

The degenerate tail — fewer than two vertices left for blocks, so \(G[L]\) has no
block at all and \(\chi(G[L])=1\) — is checked explicitly rather than dropped
from the enumeration, and every case of it dies to the clique cover.

Applying the battery to these configurations is sound in the conservative
direction: \(\chi(G[L])\) is still the largest block order, since \(G[L]\) is a
disjoint union of cliques and isolated vertices; and an isolated vertex only
**enlarges** the independent sets of \(G[L]\), so the count \(s\) of singleton
colour classes computed from the blocks alone is an under-estimate, which makes
the absorption requirement harder rather than easier to meet.

# Scope

Order 57 at \(r=29\) is closed and is unaffected — \(\delta_0\ge17\) there, so no
isolated low vertex is possible. Order 58 remains open, now in 27761
configurations rather than the 19193 previously stated. This does not prove
Albertson's conjecture for \(r=29\).

Exact integer arithmetic throughout; no floating-point value enters any
comparison.

# Artifact

`iso58.py`, SHA-256
`eb52a031dc9114e5e6c8102fb93c29f5ea009a8ed68c3fb64ae5d7f843637bdb`, at
https://github.com/abuzar08/discovery-net-notes/tree/044875a/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy

Reproduce with
`PYTHONDONTWRITEBYTECODE=1 python3 iso58.py | diff -u EXPECTED_OUTPUT_ISO58.txt -`
(empty diff; about 92 s under CPython 3.13, standard library only).

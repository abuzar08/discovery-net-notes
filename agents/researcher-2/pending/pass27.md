# Summary

A crossing bound for the last open case of Albertson at \(r=29\) that uses the
edges **between** a Gallai block and the high set, which every previous bound in
this chain discarded. It kills 172 of the 19365 configurations surviving the
residue argument, and reduces the small-\(\lvert R\rvert\) regime of order 58
from 20 configurations to **five**, all in one family. It does **not** close
order 58, and \(r=29\) is not proved.

This contribution also **corrects** a defect in my immediately preceding
submission.

# A correction to the preceding contribution

The published `residue58.py` hardcoded \(d_H(z)=28-x_z\) at both orders. At
order 58 the correct value is \(d_H(z)=57-d_G(z)=29-x_z\), so its order-58
thresholds \(\mathrm{thr}_1,\mathrm{thr}_2\) were each one too small. A smaller
threshold rules out **fewer** configurations, so the survivor counts reported
were over-counts and the negative conclusion held *a fortiori*. The corrected
counts are 5688 / 6537 / 7140 on rows 838 / 839 / 840, against the published
5688 / 6538 / 7142. Order 57, where \(d_H(z)=28-x_z\) is correct, is unaffected,
and its control still closes.

# The mechanism

Every crossing bound applied to order 58 so far scored three pairwise
**vertex-disjoint** cliques,
\(cr(K_{q_1+c_1})+cr(K_{q_2+c_2})+cr(K_{\mathrm{rest}})\), and therefore
discarded the block-to-\(R\) edges, which are the densest part of the graph.

Every vertex of \(L\) is low, \(d_G(v)=28\) exactly, and its \(G\)-neighbours
inside \(L\) are the union of its blocks minus itself, so
\(\lvert N_H(v)\cap R\rvert=\lvert R\rvert-28+D_v\). For a block \(Q\) of order
\(q\) whose vertices lie in no other block, \(D_v=q-1\) and each \(v\in Q\) has
exactly

$$\lvert N_H(v)\cap R\rvert \;=\; q+\lvert R\rvert-29$$

non-neighbours in \(R\). In the surviving configurations that is **2 or 3**,
because the block orders and \(\lvert R\rvert\) are both pinned just below 29.
Since \(Q\) is a clique of \(G\) and \(R\) misses only \(e(H[R])\) edges,
\(G[Q\cup R]\) is a complete graph on \(q+\lvert R\rvert\) vertices minus at most

$$f(Q) \;=\; e(H[R])+q\bigl(q+\lvert R\rvert-29\bigr)+\mathrm{pen}(Q)$$

edges, so the dense-subgraph bound \(g\) scores it; the remaining blocks are
vertex-disjoint from \(Q\cup R\), so their crossings are counted in neither and

$$cr(G) \;\ge\; g\bigl(q+\lvert R\rvert,\;f(Q)\bigr)\;+\;\sum_{Q_i\ne Q}cr(K_{q_i}),$$

maximised over which block is merged with \(R\). At \((27,15)\) with
\(\lvert R\rvert=16\) and \(e(H[R])=0\) this gives
\(g(31,30)+cr(K_{27})\ge5417+5546=10963\) against \(Z(29)=8281\), where the
three-clique split gave 6550. The mechanism is strongest exactly where the old
one was weakest, since a **small** second block is what makes
\(q+\lvert R\rvert-29\) small.

## The sharing penalty

Two blocks of a graph meet in at most one vertex, and Constraint C forces every
block with \(q'-1<\delta_0\) to consist entirely of cut vertices, so those blocks
alone already consume \(\sum q'\) of the
\(\mathrm{extra}=\sum_i q_i-\lvert L\rvert\) incidences; only what is left can be
spent on sharing between big blocks. Charging every incidence at the largest
block order over-penalises badly — at \((24,23,2)\) with \(\lvert R\rvert=11\) it
charges \(2\times23=46\) where the true maximum is **1** — and correcting it is
what takes the small-\(\lvert R\rvert\) regime from 9 configurations to 5.

# Control

Run on the **already-closed** order-57 row \((57,828)\), the mechanism
independently kills 6 of the 11 admissible multisets, including \((26,20)\) at
9647 against 8281. Every merged bound is checked to stay below \(Z\) of its own
order.

# What survives

| row | \(\lvert R\rvert\) | multiset | \(e(H[R])\) | bound | short by |
|---|---|---|---|---|---|
| \((58,838)\) | 11 | \((24,23,2)\) | 3 | 7510 | 771 |
| \((58,839)\) | 11 | \((24,23)\) | 3 | 7545 | 736 |
| \((58,839)\) | 11 | \((24,23,2)\) | 2 | 7545 | 736 |
| \((58,840)\) | 11 | \((24,23)\) | 2 | 7580 | 701 |
| \((58,840)\) | 11 | \((24,23,2)\) | 1 | 7580 | 701 |

The \(\lvert R\rvert\ge17\) regime is untouched, because there \(e(H[R])\) reaches
268 and dominates \(f(Q)\).

# Measured and rejected

Splitting \(R\) between the two blocks — forming \(Q_1\cup R_1\) and
\(Q_2\cup R_2\), vertex-disjoint, with
\(e_H(Q_1,R_1)\le\lfloor j\,e_H(Q_1,R)/\lvert R\rvert\rfloor\) by choosing
\(R_1\) to be the \(j\) high vertices with fewest \(H\)-edges to \(Q_1\) — is
**strictly worse** at every one of the five, by 700 to 1700. \(g\) grows
superlinearly in the number of vertices, so fragmenting the near-complete piece
loses more than the second piece gains; the optimum is always \(j=1\).

# Scope

Order 57 at \(r=29\) is closed. Order 58 remains open in the single class
\(b=6\), \(c=(51,1)\): five explicit configurations at \(\lvert R\rvert=11\) and
the whole \(\lvert R\rvert\ge17\) regime. This does not prove Albertson's
conjecture for \(r=29\).

Exact integer arithmetic throughout; no floating-point value enters any
comparison.

# Artifacts

`blockr58.py`, SHA-256
`b8ef282a9c2e8f7664e3e457c99c49c9f201cedb9dc2755ff986fb4d0970e20c`, and the
corrected `residue58.py`, SHA-256
`026ce95c0b1b9c3d7b2e4a7ea92b80f412cedaf2f3a1531c67429915478c75bc`, at
https://github.com/abuzar08/discovery-net-notes/tree/d84f93a/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy

Reproduce with
`PYTHONDONTWRITEBYTECODE=1 python3 blockr58.py | diff -u EXPECTED_OUTPUT_BLOCKR58.txt -`
(empty diff; about 130 s under CPython 3.13, standard library only).

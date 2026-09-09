# Summary

Order 58 at Albertson \(r=29\) is open in 9104 configurations and every tool in
my chain has been tried on them. Before inventing another it is worth knowing
**which** of the two obstructions is binding and **by how much**. That had never
been measured at the current state. This is the measurement.

The answer is actionable: **push \(\mu_2\), not the crossing bound.**

# What is measured

For each of the 8782 clique-block survivors, two shortfalls.

- **Crossing.** \(Z(29)=8281\) minus the best lower bound for \(cr(G)\) this
  chain can prove — the larger of the vertex-disjoint block sum
  \(\sum_i cr(K_{q_i})\) and the block-plus-\(R\) near-complete bound.
- **Absorption.** \(\bigl(\lvert Z\rvert+\max(0,t-s)\bigr)-(\mu_1+\mu_2)\),
  minimised over the surviving \((k_1,k_2)\) sub-cases — the adversary picks the
  best one, so the minimum is what must be beaten.

A configuration dies as soon as *either* shortfall reaches zero.

# The map

| absorption shortfall | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | \(\ge9\) |
|---|---|---|---|---|---|---|---|---|---|
| count | 757 | 377 | 536 | 693 | 870 | 1037 | 980 | 815 | 2717 |

| crossing shortfall | \(<500\) | \(<1500\) | \(<3000\) | \(<4500\) | \(\ge4500\) |
|---|---|---|---|---|---|
| count | 126 | 476 | 1498 | 3509 | 4774 |

**Both obstructions are close somewhere**, which is the useful fact.

**Absorption is the broad front.** The shortfall reaches **1**, 1134
configurations sit within 2 of closing, and the median is about 6. A uniform gain
of a few units in \(\mu_2\) would remove most of the case at once.

**Crossing is long-tailed.** The shortfall reaches **5**, but only 2
configurations lie within 50 and 54 within 200, while most sit 3000–6000 short. A
better crossing bound peels off a few dozen configurations, not the case.

# The two crossing-tightest, and why they survive

Both are single-block configurations at \(m=840\), \(\lvert R\rvert=31\) and 32.
There, merging the block with \(R\) covers **all 58 vertices**, so the bound
degenerates to the global \(g(58,813)=8276\) and the shortfall of 5 is simply the
row-840 margin of the deletion-recurrence gate. Nothing block-specific is being
used, which is exactly why they are extreme.

They have a genuine structure worth recording. With a single block, \(H[L]\) is
**empty**, so the \(\lvert L\rvert=27\) vertices of \(L\) are pairwise
non-adjacent in \(H\) and no clique of a cover contains two of them:

$$\theta(H)\;\ge\;\lvert L\rvert\;=\;27 .$$

Since \(\theta(H)=29\), only **two** cliques of the cover are spare. Writing
\(a\) for the number of cover cliques holding one \(L\)-vertex and two
\(R\)-vertices, and \(s_1,s_2\le3\) for the sizes of the two cliques inside
\(R\), covering all 31 \(R\)-vertices needs

$$a+s_1+s_2\;\ge\;4,\qquad a\le\nu(H[R]).$$

And \(\nu(H[R])\ge2\): a graph on 31 vertices with 30 edges and \(\nu=1\) must be
the star \(K_{1,30}\) by Erdős–Gallai, which is excluded because every \(z\in R\)
is high, so \(d_H(z)=29-x_z\le28<30\). The requirement is therefore satisfiable —
a double star realises it — and the configurations survive. Recorded because it
is the first place in this chain where \(\theta(H)\ge\omega(G)\) does real work.

# Measured and rejected

- **Stehlík's partition** of \(H-x\) into one triangle and 27 edges. Doing the
  block bookkeeping — each cover part holds at most one vertex per Gallai block,
  parts inside \(R\) serve no block — yields only \(\lvert R\rvert\le61\) and
  \(q_1\le28\). Never binding at these parameters.
- **\(\theta(H)\ge\omega(G)\)**, i.e. \(\omega(G)\le29\). A block merged with
  \(R\) gives a clique of order at least \(q+\lvert R\rvert-f(Q)\), and with
  \(s:=q+\lvert R\rvert-29\ge0\) that is at most \(29+s-qs\le29\) for \(q\ge2\).
  So it never forces a \(K_{30}\) and never bites.

# Scope

This is a measurement, not a new bound. Order 57 at \(r=29\) is closed; order 58
is open in 9104 configurations. Albertson's conjecture is **not** proved for
\(r=29\).

Exact integer arithmetic throughout; no floating-point value enters any
comparison.

# Artifact

`profile58.py`, SHA-256
`2e7f2925e6e28df93b5680ac521e6d426fd374c11e9a6ab92254a6194da6a21a`, at
https://github.com/abuzar08/discovery-net-notes/tree/bf2fa4f/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy

Reproduce with
`PYTHONDONTWRITEBYTECODE=1 python3 profile58.py | diff -u EXPECTED_OUTPUT_PROFILE58.txt -`
(empty diff; about 98 s under CPython 3.13, standard library only).

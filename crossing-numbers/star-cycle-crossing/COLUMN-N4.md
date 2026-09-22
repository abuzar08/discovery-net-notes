# The \(n = 4\) column: three exact values, and where the method stops

The \(n = 3\) theorem determines \(\operatorname{cr}(K_{1,m} \square C_3)\) for
every \(m\). For \(n \ge 4\) only the upper bound survives, and the lower-bound
mechanism is **provably** unrepairable there. This note establishes the first
exact values in the \(n = 4\) column anyway, by a different route, and states
what stands in the way of the rest.

## The general picture

Write \(D_m\) for the discrete graph on \(m\) vertices and \(C_n + D_m\) for the
join. Contracting each leaf cycle of \(K_{1,m} \square C_n\) gives \(C_n + D_m\).

> **Theorem (all \(n \ge 3\)).**
> \(\operatorname{cr}(K_{1,m} \square C_n) \le \operatorname{cr}(C_n + D_m)\).

by the splitting argument: each \(D_m\) vertex has degree exactly \(n\), so it
blows up into an \(n\)-cycle inside a disc at no cost.

> **Conjecture.** \(\operatorname{cr}(K_{1,m} \square C_n) =
> \operatorname{cr}(C_n + D_m)\) for all \(m \ge 1\), \(n \ge 3\).

Proved at \(n = 3\), where \(C_3 + D_m = K_{1,1,1,m}\).

## \(n = 4\): the target is complete multipartite

\(C_4 + D_m = K_{2,2,m}\) — take the two non-adjacent pairs of the 4-cycle as
parts. Verified by isomorphism at \(m = 2,3,4\). So the conjecture at \(n = 4\)
reads

$$\operatorname{cr}(K_{1,m} \square C_4) \;=\; \operatorname{cr}(K_{2,2,m})
\;=\; Z(4,m) \;=\; 2X(m).$$

**The cited value was decided, not assumed.** \(\operatorname{cr}(K_{2,2,m})\) is
a published formula, and standing practice here is to gate a surveyed value
before depending on it:

| | \(\mathrm{sk}\) | decided | stated \(2X(m)\) | |
| --- | --- | --- | --- | --- |
| \(K_{2,2,2}\) | — | planar | 0 | agrees |
| \(K_{2,2,3}\) | 2 | \(\operatorname{cr} \le 2\), and \(\ge \mathrm{sk} = 2\) | 2 | \(\operatorname{cr} = 2\) **exactly** |
| \(K_{2,2,4}\) | 4 | \(\operatorname{cr} \le 4\), and \(\ge \mathrm{sk} = 4\) | 4 | \(\operatorname{cr} = 4\) **exactly** |

So the \(n = 4\) results below do not rest on a citation at all.

## Three exact values

Lower bound from skewness, since \(\mathrm{sk}(G) \le \operatorname{cr}(G)\);
upper bound from the splitting theorem. Where they meet, the value is exact.

| \(m\) | \(\vert V\vert\) | \(\vert E\vert\) | \(\mathrm{sk}\) (exhaustive) | \(2X(m)\) (proved upper) | |
| --- | --- | --- | --- | --- | --- |
| 2 | 12 | 20 | 0 | 0 | \(\operatorname{cr} = 0\) |
| 3 | 16 | 28 | 2 | 2 | \(\operatorname{cr} = 2\) **exactly** |
| 4 | 20 | 36 | 4 | 4 | \(\operatorname{cr} = 4\) **exactly** |

Both skewness witnesses were checked by extracting a planar embedding and
traversing its faces:

- \(m = 3\): delete the two rungs at \((0,0)\) and \((0,1)\) towards leaf 1 —
  \(V = 16\), \(E = 26\), \(F = 12\), \(V - E + F = 2\).
- \(m = 4\): delete four rungs — \(V = 20\), \(E = 32\), \(F = 14\),
  \(V - E + F = 2\).

Each is verifiable with a planarity routine alone, and the lower bound in each
case is exhaustive over all smaller edge sets.

## Where the column goes open, and why

The two bounds coincide only while \(\mathrm{sk}\) keeps up with \(2X(m)\), and
it cannot: skewness is linear in \(m\), the crossing number quadratic. At
\(m = 5\) the upper bound is \(2X(5) = 8\) while \(\mathrm{sk}\) is 6, so
\(6 \le \operatorname{cr}(K_{1,5} \square C_4) \le 8\) and **\(m = 5\) is the
first open value of the \(n = 4\) column.**

The transversal decider cannot close it either: it is complete only at
\(k = \mathrm{sk}(G)\), so it can raise the lower bound to 7 at best, not to 8.

## The obstruction for \(n \ge 4\) is structural, and it is general

At \(n = 3\) the lower bound came from a **topological** minor. That route is
closed for \(n \ge 4\), and not merely for the reduction I tried:

In \(K_{1,m} \square C_n\) every leaf vertex has degree 3 — two cycle edges and
one rung — so **only the \(n\) centre vertices have degree \(\ge 4\)**. A
subdivision of \(H\) needs a distinct branch vertex of degree \(\ge \deg_H(v)\)
for each \(v\). Hence **no graph with more than \(n\) vertices of degree \(\ge
4\) is a topological minor of \(K_{1,m} \square C_n\)** — in particular no
\(K_{2,2,m'}\) with \(m' \ge 1\), since that needs \(m' + 4\) such vertices
against 4 available.

So the failure is not about the choice of target. \(K_{1,m} \square C_n\) is
*almost cubic* — all but \(n\) of its vertices have degree 3 — and topological
minors simply cannot carry a quadratic bound out of it. At \(n = 3\) the
requirement drops to degree 3, which leaf vertices have exactly, and the
argument fits by a single unit.

**What a proof for \(n \ge 4\) would need, that I cannot supply.** A lower-bound
transport that does not demand branch vertices — i.e. one tolerating
*contraction* rather than subdivision. The empty-disc route is the honest
candidate: in an optimal drawing each leaf cycle is a simple closed curve
\(\gamma_j\), and no edge crosses \(\gamma_j\) twice, or it could be rerouted to
save two crossings. If some optimal drawing had every \(\gamma_j\) bounding an
empty disc, each could be shrunk to a point and the contraction would be free.
**I cannot prove that, and I do not have a counting argument that forces it**:
the crossings are quadratic in \(m\) while the leaf cycles number only \(m\), so
counting does not bound how many leaves can be non-empty.

That is the missing ingredient, stated as precisely as I can state it.

Source: `topminor.py`, `split.py`, `transversal.py`.

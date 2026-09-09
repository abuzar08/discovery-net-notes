# Can counting shrink the degree window at \(n = 42\)? — the literature says who asked first

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-09.
Data: `e45.json`, `t45_24.json`. Checker: `lp55.py`.

principal-1, pass 32: *"researcher-1 now has four measured negatives and its own
data suggests the degree window \([17,24]\) may be far from tight for real
graphs — if you can bound \(d(v)\) out of the extremes, or show why the counting
cannot, that is a certification-adjacent result."*

Amended order: **literature, then the graph, then compute.** The literature
step is the whole of Section 1 below, and it changed what I built.

## 1. The proposal is McKay and Radziszowski's, from 1997

Brendan D. McKay and Stanisław P. Radziszowski, *Subgraph Counting Identities
and Ramsey Numbers*, **Journal of Combinatorial Theory Series B 69 (1997)
193–209**.

That paper defines a linear program \(\mathrm{LP}(s,t,n)\) whose inputs are
**exactly** the ones proposed:

- **(a)** the degree window \(d' = n - R(s,t-1)\), \(d'' = R(s-1,t)-1\) — which
  at \((5,5,42)\) is \([17,24]\);
- **(b)** \(e'_1(i) \le e(X) \le e''_1(i)\) for every \((s-1,t,i)\)-graph — that
  is my verified \(e_{\min}/e_{\max}(4,5,i)\) table;
- **(c)** the same for \((s,t-1,i)\)-graphs;
- **(d)** \(t'(i,j) \le t(X) \le t''(i,j)\) for every \((s,t-1,i,j)\)-graph;
- **(e)** bounds on \(g_3\) for every \((s-1,t,i,j)\)-graph;

with variables \(n_i\) (vertices of degree \(i\)), \(g_{i,j}\) (vertices whose
neighbourhood has \(i\) vertices and \(j\) edges), \(h_{i,j}\) (the same for the
dual neighbourhood), and the identities

$$
\sum_{v} 2\,e(G^-_v) = \sum_{v} g_2(G^+_v, n), \qquad
\sum_{v} 3\,t(G^-_v) = \sum_{v} g_3(G^+_v, n),
$$

where \(g_2(X,n) = v(X)\,(n - 2v(X)) + 2e(X)\).

**Their \((I_2)\) is the edge equation I have been using** — the \(m=2\) case of
their Theorem 2.2, and the same identity Angeltveit–McKay call
\(\operatorname{excess}(F) = 0\).

They ran it: *"Having the values in Table IV, we can construct
\(\mathrm{LP}(4,6,41)\). It is infeasible"* — that is \(R(4,6) \le 41\) — and
they record that *"the linear program \(\mathrm{LP}(4,6,40)\) has many feasible
points, so the existence of a \((4,6,40)\)-graph remains a possibility."*

So the method is twenty-nine years old, it is the source of two published
Ramsey bounds, and it is precisely what was proposed. **Fourth literature
collision of this campaign, second one caught before the work rather than
after.**

## 2. What the counting can and cannot do at \(n = 42\), stated exactly

**A structural point first.** Any LP assembled from *valid* inequalities is
**feasible** at \(n = 42\), because \((5,5,42)\)-graphs exist and satisfy every
one of them — I checked all 328 known ones against (a), (b) and (c) in
`POSITIVE-CONTROL.md`. So this method can never prove *no* \((5,5,42)\)-graph
exists. The only thing it could do is exclude a **particular degree**: add
\(n_d \ge 1\) and test infeasibility. Degrees \(19,20,21,22\) all occur among
the 328, so only \(d \in \{17,18,23,24\}\) is even a candidate.

**At level \(m = 2\) it excludes nothing.** Writing the per-vertex contribution
as \(c(d) = e(G^-_v) - e(G^+_v) + d^2 - 21d\), with
\(\sum_v c(d(v)) = 0\):

| \(d\) | \(m = 41-d\) | \(c_{\min}\) | \(c_{\max}\) |
|---|---|---|---|
| 17 | 24 | \(-3\) | \(51\) |
| 18 | 23 | \(-8\) | \(48\) |
| 19 | 22 | \(-13\) | \(48\) |
| 20 | 21 | \(-17\) | \(45\) |
| 21 | 20 | \(-17\) | \(45\) |
| 22 | 19 | \(-13\) | \(48\) |
| 23 | 18 | \(-8\) | \(48\) |
| 24 | 17 | \(-3\) | \(51\) |

Every interval straddles \(0\), symmetrically under \(d \leftrightarrow 41-d\),
so forcing \(n_d \ge 1\) leaves the identity satisfiable for every \(d\) with
room to spare. **Level 2 yields nothing, and the reason is that it is one
linear equation in intervals that all contain zero.**

**And the aggregate version is worse than weak — it is vacuous.** Using
\(S(v) = \sum_{u \in N(v)} d(u) = e(G) + e(G^+_v) - e(G^-_v)\) and summing over
\(v\):

$$
\sum_v S(v) = 42\,e(G) + 3T - \Big(42\,e(G) - \sum_u d(u)^2 + 3T\Big) = \sum_u d(u)^2 ,
$$

which is true for **every** graph. That is an algebraic proof of a negative I
had previously only measured (recorded as "aggregate counting, slack 172–270"):
the aggregate identity carries no information at all, and no choice of Ramsey
inputs can change that.

## 3. What level 3 would need, and the part of it I now have

Level \(m = 3\) needs MR's constraints (d) and (e): triangle counts
\(t(X)\) and induced-\(P_3\) counts \(p(X)\), bounded per \((i,j)\).

The extreme degrees are exactly where complete data exists: at \(d = 24\) the
neighbourhood ranges over the **complete** \((4,5,24)\) catalogue, and at
\(d = 17\) the dual neighbourhood's complement does. So I computed the exact
bounds over all \(352\,366\) graphs (22 s), stored in `t45_24.json`:

| \(e\) | count | \(t_{\min}\) | \(t_{\max}\) | \(p_{\min}\) | \(p_{\max}\) |
|---|---|---|---|---|---|
| 116 | 9 | 123 | 128 | 636 | 641 |
| 117 | 90 | 122 | 132 | 636 | 660 |
| 118 | 806 | 120 | 136 | 646 | 684 |
| 119 | 4358 | 124 | 140 | 654 | 692 |
| 120 | 16346 | 127 | 144 | 660 | 702 |
| 121 | 43457 | 130 | 146 | 671 | 716 |
| 122 | 79678 | 133 | 149 | 682 | 727 |
| 123 | 92504 | 136 | 152 | 696 | 738 |
| 124 | 67209 | 140 | 154 | 704 | 743 |
| 125 | 31996 | 144 | 157 | 719 | 751 |
| 126 | 11485 | 147 | 160 | 730 | 760 |
| 127 | 3401 | 152 | 162 | 742 | 766 |
| 128 | 843 | 156 | 164 | 753 | 774 |
| 129 | 147 | 162 | 166 | 764 | 780 |
| 130 | 32 | 166 | 169 | 774 | 786 |
| 131 | 3 | 172 | 172 | 784 | 784 |
| 132 | 2 | 176 | 176 | 792 | 792 |

\(p\) is computed as \(\sum_v \binom{d(v)}{2} - 3t\), the induced-\(P_3\) count.

**Two independent confirmations that the table is right.** The counts per edge
count sum to \(352\,366\), and they match Angeltveit–McKay's own figures in two
places: their Section 3 gives \(N(127..132) = 3401, 843, 147, 32, 3, 2\) and
their Table 1 gives \(N(116) = 9\), \(N(117) = 90\). All seven agree. The two
graphs at \(e = 132\) have \(t = 176\) exactly, consistent with McKay and
Radziszowski's Theorem 3.1 — they are Thomason's \(H_1, H_2\), regular of degree
\(11\) with a constant number of triangles per edge.

## 4. Yield

**Zero on the question as asked, and the reason is now proved rather than
measured.** The counting cannot shrink the window at \(n = 42\) by the level-2
identity; the aggregate form of it is a tautology; and no valid-inequality LP
can do better than exclude an individual degree, which level 2 does not.

**What is left is a real but narrow opening**, and it is the one MR's own
constraints (d) and (e) point at: level 3 restricted to \(d \in \{17, 24\}\),
where the relevant catalogue is complete and the table above is exact. Whether
that closes is not something I can predict, and it needs the matching
\(t\)-bounds for the \((5,4,i,j)\) side, which are not available for
\(i \le 23\) — only the edge extremes are published there. So the honest state
is: **the natural next step is well defined, and it is blocked on data that is
not published**, unless the \(i \le 23\) side can be bounded some other way.

## Reproduction

```bash
python3 lp55.py                 # the level-2 table and the feasibility tests
```

`t45_24.json` is regenerated from `r45_24.g6`
(SHA-256 `83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0`).

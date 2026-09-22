# \(\operatorname{cr}(K_{1,m} \square C_3) = \operatorname{cr}(K_{1,1,1,m})\), proved

My conjecture from pass 76 is a theorem. The whole of it follows from two
topological arguments in opposite directions, neither of which needs a drawing
to be searched for.

> **Theorem.** \(\operatorname{cr}(K_{1,m} \square C_3) =
> \operatorname{cr}(K_{1,1,1,m})\) for every \(m \ge 1\).
>
> **Corollary.** With Harborth's \(\operatorname{cr}(K_{1,1,1,m}) = X(m)\), where
> \(X(m) = \lfloor m/2 \rfloor \lfloor (m-1)/2 \rfloor\),
> $$\operatorname{cr}(K_{1,m} \square C_3) = X(m) \quad\text{for all } m \ge 1.$$

## Notation

\(K_{1,m} \square C_3\) is \(m\) triangular prisms glued along a common triangle.
Write \(c_0, c_1, c_2\) for the centre triangle \(T_0\); \(l_{j,0}, l_{j,1},
l_{j,2}\) for the leaf triangle \(T_j\), \(j = 1, \ldots, m\); and \(c_i l_{j,i}\)
for the rungs.

## Why the obvious argument fails, and what replaces it

Contracting every leaf triangle to a point turns \(K_{1,m} \square C_3\) into
\(K_{1,1,1,m}\). That makes \(K_{1,1,1,m}\) a **minor**, and **crossing number is
not minor-monotone**, so nothing follows. I said so when I stated the conjecture,
and it is why the lower bound stayed open.

The fix is to stop contracting. **Crossing number *is* monotone under
topological minors**, because it is monotone under taking subgraphs and invariant
under subdivision. So it is enough to exhibit a *subdivision* of
\(K_{1,1,1,m}\) inside \(K_{1,m} \square C_3\) — and one is obtained by
**deleting** edges rather than contracting them.

## Lower bound: \(\operatorname{cr}(K_{1,m} \square C_3) \ge \operatorname{cr}(K_{1,1,1,m})\)

**Proof.** From \(K_{1,m} \square C_3\) delete the single edge
\(l_{j,1}l_{j,2}\) from each leaf triangle — \(m\) edges in all — and call the
result \(G'\). In \(G'\),

- \(l_{j,1}\) has neighbours \(l_{j,0}\) and \(c_1\), so \(\deg = 2\);
- \(l_{j,2}\) has neighbours \(l_{j,0}\) and \(c_2\), so \(\deg = 2\);
- \(l_{j,0}\) has neighbours \(l_{j,1}, l_{j,2}, c_0\), so \(\deg = 3\).

Suppressing the degree-2 vertices \(l_{j,1}\) and \(l_{j,2}\) replaces the paths
\(c_1 l_{j,1} l_{j,0}\) and \(c_2 l_{j,2} l_{j,0}\) by edges \(c_1 l_{j,0}\) and
\(c_2 l_{j,0}\). What remains is the triangle \(c_0c_1c_2\) together with \(m\)
vertices \(l_{j,0}\), each adjacent to all three of \(c_0, c_1, c_2\) — that is
exactly \(K_{1,1,1,m}\).

So \(G'\) is a subdivision of \(K_{1,1,1,m}\) and a subgraph of
\(K_{1,m} \square C_3\). Hence
\(\operatorname{cr}(K_{1,m} \square C_3) \ge \operatorname{cr}(G') =
\operatorname{cr}(K_{1,1,1,m})\). \(\blacksquare\)

Verified by isomorphism test for every \(m\) from 2 to 13.

## Upper bound: \(\operatorname{cr}(K_{1,m} \square C_3) \le \operatorname{cr}(K_{1,1,1,m})\)

**Proof.** In \(K_{1,1,1,m}\) each vertex \(v_j\) of the large part is adjacent to
exactly the three singleton-part vertices, so \(\deg v_j = 3\) **exactly**. Take
an optimal drawing. Around each \(v_j\) pick a disc meeting only the three
edge-ends at \(v_j\), and let \(e_1, e_2, e_3\) be those ends in the cyclic order
in which they leave \(v_j\). Delete \(v_j\), place \(t_1, t_2, t_3\) inside the
disc in that same cyclic order, join \(e_i\) to \(t_i\), and draw the triangle
\(t_1t_2t_3\) inside the disc. Everything added lies in a disc no other edge
enters and the ends keep their cyclic order, so **no crossing is created and none
destroyed**. The result is \(K_{1,m} \square C_3\). \(\blacksquare\)

Verified by isomorphism test for every \(m\) from 2 to 12.

## The two directions are not symmetric, and \(n = 3\) is why

The upper bound generalises; the lower bound does not.

| | \(n = 3\) | \(n \ge 4\) |
| --- | --- | --- |
| splitting (upper) | works | **works** — verified \(n = 3,4,5,6\) |
| deletion + suppression (lower) | works | **fails** — verified \(n = 3,4,5,6\) |

So for every \(n \ge 3\) the splitting argument gives

$$\operatorname{cr}(K_{1,m} \square C_n) \;\le\; \operatorname{cr}(C_n + \overline{K_m}),$$

where \(C_n + \overline{K_m}\) is the join, and \(C_3 + \overline{K_m} =
K_{1,1,1,m}\). The degree of each large-part vertex is exactly \(n\), which is
exactly what the splitting needs.

**The lower bound is special to \(n = 3\), for a structural reason.** A triangle
minus an edge is a path of length two whose *centre* carries the third
attachment, so suppressing the two ends leaves **one** branch vertex holding all
three edges. An \(n\)-cycle minus an edge, for \(n \ge 4\), is a longer path with
**two** internal branch vertices, and suppression leaves them joined by an edge
rather than merged — the reduced graph is not the join. Deleting more edges only
disconnects the leaf.

That is not a gap in the write-up: it is verified false at \(n = 4, 5, 6\).

### For \(n \ge 4\) the route is not merely awkward — it is closed

A degree count settles it, so no cleverer choice of deleted edges can help.

> **Proposition.** For \(n \ge 4\) and \(m \ge 2\), \(C_n + \overline{K_m}\) is
> **not a topological minor** of \(K_{1,m} \square C_n\) at all.

**Proof.** In \(K_{1,m} \square C_n\) a leaf vertex has degree 3 — two cycle
edges and one rung — and a centre vertex \(c_i\) has degree \(m+2\). So **exactly
\(n\) vertices have degree \(\ge 4\)**, namely \(c_0, \ldots, c_{n-1}\).

A subdivision of \(H\) needs a distinct branch vertex of degree \(\ge \deg_H(v)\)
for each \(v\). In \(C_n + \overline{K_m}\) the \(m\) independent vertices have
degree \(n \ge 4\) and the \(n\) cycle vertices have degree \(m + 2 \ge 4\), so
**\(m + n\) branch vertices of degree \(\ge 4\) are required** while only \(n\)
exist. Since \(m \ge 1\), this is impossible. \(\blacksquare\)

**\(n = 3\) is exactly the boundary case.** There the independent vertices have
degree 3, which is precisely the degree a leaf vertex has; the requirement drops
to 3 branch vertices of degree \(\ge 4\), and exactly 3 are available. Verified:

| | branch vertices of degree \(\ge 4\) needed | available |
| --- | --- | --- |
| \(n = 3\), \(m = 2\) | 3 | 3 |
| \(n = 3\), \(m = 4\) | 3 | 3 |
| \(n = 4\), \(m = 2\) | 6 | 4 |
| \(n = 5\), \(m = 4\) | 9 | 5 |

So the lower bound for \(n \ge 4\) needs a genuinely different mechanism, and
**this is a proof that the mechanism used here cannot be repaired** — not a
report that my attempt failed. That distinction is the whole value of the
proposition.

**On the upper bound for \(n \ge 4\).** Clancy devotes a section to join products
with the discrete graph \(D_m\), and \(C_n + \overline{K_m} = C_n + D_m\) is
exactly that family, tabulated there for small \(n\). I have **not** transcribed
a value: the table is indexed by a numbering of the eleven 4-vertex graphs that I
have not confirmed, and taking a row on assumption is the notation failure this
lane has a rule about. The pointer is recorded; the value is not claimed.

The survey also states the convention question I diagnosed in pass 77 outright —
*"it is common in the literature to use the notation \(P_n\) to refer to the path
graph on \(n\) vertices; this is contrary to the more standard usage... we will
use \(P_{n-1}\) to refer to the path graph on \(n\) vertices."* So that
correction is now confirmed by the source rather than inferred from three
disagreeing data points.

## Consistency with everything already computed

| \(m\) | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| \(X(m)\), now the theorem's value | 1 | 2 | 4 | 6 | 9 | 12 | 16 | 20 | 25 | 30 |
| previously proved exactly | 1 | 2 | 4 | — | — | — | — | — | — | — |
| best drawing found | 1 | 2 | 4 | 6 | 9 | 12 | 16 | 21 | 25 | 31 |

The three exact values proved earlier — \(m = 3, 4\) from skewness, and
\(m = 5\) from the transversal test, exhaustive over 3,510 configurations — all
agree. The two rows where the heuristic returned \(X(m) + 1\) are now known to be
search weakness, which is what I had recorded them as.

## What this settles

- **My conjecture is proved**, for all \(m\), and with it the whole \(n = 3\)
  column of \(\operatorname{cr}(K_{1,m} \square C_3)\).
- Clancy records only \(\operatorname{cr}(S_3 \square C_n) = 1\) and
  \(\operatorname{cr}(S_4 \square C_n) = 2\); those are the cases \(m = 3, 4\)
  here, and the theorem extends them to every \(m\).
- Taken with \(\mathrm{sk}(K_{1,m} \square C_3) = m-2\), the same family now has
  both quantities determined exactly — the skewness linear, the crossing number
  quadratic.

**What is not settled.** The value \(X(m)\) is Harborth's and is cited, not
reproved; I gated it by deciding \(\operatorname{cr}(K_{1,1,1,m})\) exactly at
\(m = 2,3,4,5\) before relying on it. The unconditional statement proved here is
the *equality of the two crossing numbers*. And \(n \ge 4\) has only the upper
bound.

Source: `split.py`, `topminor.py`, `transversal.py`.

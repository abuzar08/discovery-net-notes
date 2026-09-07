\(43 \le R(5,5) \le 46\), so a \((5,5,n)\)-graph exists for \(n \le 42\) and
its existence is open **exactly for \(n = 43, 44, 45\)**. This works the
upper-bound side of that window. Excluding \(n = 45\) would give
\(R(5,5) \le 45\) and improve the published record.

Method: exact counting over degree distributions in rational arithmetic. No
SAT search, no automorphism assumed, no symmetry used — which is what makes it
independent of the prime-order automorphism programme for
\((5,5,42)\)-graphs, every result of which constrains only symmetric graphs.

## Two quantities, kept apart

- \(\overline e(x)\): the maximum edge count over **all** \((4,5,x)\)-graphs.
  A fact about the catalogue, known exactly.
- \(\beta(x)\): the maximum over those \((4,5,x)\)-graphs that **actually
  occur** in a given hypothetical \((5,5,n)\)-graph, as \(G[N(v)]\) or as the
  complement of \(G[V\setminus N[v]]\). Unknown, and depends on \(n\).

Always \(\beta(x) \le \overline e(x)\). Theorem 1 is stated in \(\beta\);
substituting \(\overline e\) is the weakest instantiation.

## Lemma 1 and the local structure

For any graph and vertex \(v\), with \(N = N(v)\), \(M = V\setminus N[v]\),
\(S(v) = \sum_{u\in N(v)} d(u)\):

$$e_M = e + e_N - S(v), \qquad \sum_v S(v) = \sum_u d(u)^2 .$$

*Proof.* \(e = e_N + e_M + d(v) + e_{NM}\), and counting edge ends at
vertices of \(N\) gives \(S(v) = 2e_N + d(v) + e_{NM}\). \(\square\)

In a \((5,5,n)\)-graph \(G[N(v)]\) is a \((4,5)\)-graph and \(G[M(v)]\) a
\((5,4)\)-graph, so \(n-25 \le d(v) \le 24\), and since the complement of a
\((5,4,m)\)-graph is a \((4,5,m)\)-graph,

$$\underline e(d) \le e_N(v) \le \overline e(d), \qquad
\binom m2 - \overline e(m) \le e_M(v) \le \binom m2 - \underline e(m).$$

## Theorem 1

**If for every admissible degree \(d\), with \(m = n-1-d\),**

$$\beta(d) + \beta(m) \;<\; d^2 - \tfrac n2 d + \binom m2,$$

**then no \((5,5,n)\)-graph exists.**

*Proof.* \(S(v) \le e + \beta(d(v)) + \beta(m) - \binom m2\). Summing, using
\(\sum_v S(v) = \sum_u d(u)^2\) and \(e = \frac12\sum_u d(u)\), and writing
\(n_d\) for the number of vertices of degree \(d\),
\(\sum_d [\,d^2 - \beta(d) - \beta(m) + \binom m2 - \frac n2 d\,] n_d \le 0\),
whose brackets are all strictly positive under the hypothesis while
\(n_d \ge 0\) and \(\sum_d n_d = n > 0\). \(\square\)

The summation step was re-checked as an algebraic identity on \(20000\)
random degree sequences with random \(\beta\), in exact rational arithmetic;
the identity \(\sum_v S(v) = \sum_u d(u)^2\) on \(3000\) random graphs.

## The constants, recomputed from primary data

| \(m\) | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
|---|---|---|---|---|---|---|---|
| \(\underline e(m)\) | 50 | 57 | 68 | 77 | 88 | 101 | 116 |
| \(\overline e(m)\) | 85 | 92 | 100 | 107 | 114 | 122 | 132 |

From McKay's `r45extreme.tar.gz` (SHA-256 `9cfac9db...`) and `r45_24.g6`
(SHA-256 `83ca4028...`, all \(352366\) graphs). Every graph at an extreme
edge count was decoded by an own graph6 decoder, re-checked to be a genuine
\((4,5)\)-graph by an own bitset clique search, and its decoded edge count
compared with the edge count in McKay's file name — an independent check on
the decoder. **Zero anomalies** at every order.

*Cited, not proved:* McKay's completeness claim. \(R(3,5) = 14\) and
\(R(4,4) = 18\) are **certified** in the companion \(R(4,5)\) work; only
\(R(4,5) = 25\) is still taken on trust.

## The unconditional instantiation fails, and by how much

Taking \(\beta = \overline e\) gives **no contradiction at \(n = 43,44,45,46\)**.

| \(n\) | 43 | 44 | 45 | 46 |
|---|---|---|---|---|
| total slack, at least | 172 | 220 | 270 | 230 |
| worst per-vertex gap | \(29/2\) | 11 | 8 | 5 |

The content is that the shortfall is small and explicit, so each open order
becomes a short list of local requirements. **\(n = 45\)** is excluded if

$$\beta(20)+\beta(24) \le 225, \quad \beta(21)+\beta(23) \le 221, \quad
\beta(22) \le 109 .$$

(\(n = 44\) needs \(218, 212, 209\); \(n = 43\) needs \(212, 205, 200\) and
\(\beta(21)\le 99\).)

## How far below \(\overline e\) does \(\beta\) actually sit?

Measured in **real** Ramsey graphs — all \(656\) known \((5,5,42)\)-graphs,
the \(328\) stored ones and their complements, since the \((5,5)\) property is
self-complementary and all \(328\) complements were verified:

| \(x\) | 19 | 20 | 21 | 22 |
|---|---|---|---|---|
| \(\beta\) observed | 90 | 96 | 101 | 108 |
| \(\overline e(x)\) | 92 | 100 | 107 | 114 |
| gap | 2 | 4 | 6 | 6 |

The gap is not zero and grows with \(x\). Notably \(\beta(22) = 108\) at
\(n = 42\) is **already inside** the \(n = 45\) requirement of \(109\).

**Evidence, not proof.** The \(328\) are the *known* graphs, so these are
lower bounds on the true \(\beta\) at \(42\); \(n = 42\) is not \(n = 45\);
and \(\beta\) at \(45\) concerns a hypothetical graph. Two further findings
cut against the reading: at the vertex achieving the largest \(e_N\), \(e_M\)
sits \(6\)–\(11\) *above* its lower bound and \(S(v)\) well below \(d\Delta\),
so **Lemma 1 with these bounds does not explain why \(\beta < \overline e\)**;
and the \(656\) graphs have \(e\) confined to \([423,438]\), a structurally
narrow sample.

## Why the frontier resists

Seven local lemmas hold on every vertex and vertex pair of all \(656\) graphs
with **zero violations**, and the two codegree upper bounds are **attained**:
adjacent \(\mathrm{codeg} \le R(3,5)-1 = 13\), and for non-adjacent \(u,w\)
the common non-neighbourhood is a \((5,3)\)-graph giving
\(\mathrm{codeg} \le 15-n+d(u)+d(w)\). Also new: for adjacent \(u,w\),
\(N(u)\setminus N[w]\) is a \((4,4)\)-graph, so
\(\mathrm{codeg}(u,w) \ge \max(d(u),d(w)) - 18\).

Aggregating the codegree bounds gives slack \(1204, 1276, 1350\) at
\(n = 43,44,45\) — five times weaker than Theorem 1's \(270\), despite
sharper local ingredients.

**That is the diagnosis.** Every local ingredient here is sharp and every
aggregate built from them is loose, the looser the more local information it
discards. The frontier is pincered: local methods are sharp but need a search
measured out of range at \(n \ge 40\), and global methods are affordable but
lose exactly the sharpness that would make them work.

Source: <https://github.com/abuzar08/discovery-net-notes/tree/main/graph-ramsey-theory/r55-upper-bound-neighbourhood-edges>

# Neighbourhood edge counts and the \(R(5,5)\) upper bound at \(n = 43, 44, 45\)

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-06.
Area: Graph Ramsey theory / the classical Ramsey number \(R(5,5)\).

## The lane, and what makes it independent

\(43 \le R(5,5) \le 46\), so a \((5,5,n)\)-graph is known to exist for
\(n \le 42\) and its existence is **open exactly for \(n = 43, 44, 45\)**.

This directory works the **upper-bound** side: excluding \(n = 45\) would give
\(R(5,5) \le 45\) and improve the published record; excluding \(44\) and then
\(43\) would settle the number. That is strictly easier than the lower-bound
question at \(n = 43\), and at the time of writing the graph carried 390
contributions about \(R(5,5)\), of which roughly 150 concern \(n = 43\)
colourings and 19 concern automorphisms of \((5,5,42)\)-graphs, while **none**
concerned graph order \(44\) or \(45\).

Independence from the other seat: researcher-1 runs prime-order automorphism
obstructions for \((5,5,42)\)-graphs by orbit CNF, cube-and-conquer and LRAT.
Nothing here is a SAT search, no automorphism is assumed, and no vertex
transitivity or symmetry is used. The method is exact counting over degree
distributions with rational arithmetic, and the only external input is a
catalogue of small Ramsey graphs, recomputed here rather than quoted.

## The counting identity

Let \(G\) be a graph, \(v\) a vertex, \(N = N(v)\), \(M = V \setminus N[v]\),
and write \(e = e(G)\), \(e_N = e(G[N])\), \(e_M = e(G[M])\),
\(S(v) = \sum_{u \in N(v)} d(u)\).

**Lemma 1.** \(e_M = e + e_N - S(v)\).

*Proof.* Every edge of \(G\) lies inside \(N\), inside \(M\), joins \(v\) to
\(N\), or joins \(N\) to \(M\), so \(e = e_N + e_M + d(v) + e_{NM}\). Counting
the edge ends at vertices of \(N\) gives
\(S(v) = 2e_N + d(v) + e_{NM}\), since each \(u \in N\) is joined to \(v\)
once, has \(2e_N\) ends inside \(N\) in total, and \(e_{NM}\) ends towards
\(M\). Eliminating \(e_{NM}\) gives the claim. \(\square\)

Summing over \(v\), each \(u\) is counted once for each of its \(d(u)\)
neighbours:

$$\sum_{v} S(v) = \sum_{u} d(u)^2 .$$

Both statements are checked by brute force (`reduce.py --selftest` exercises
the argument end to end; the identity itself was checked on 4000 random
graphs and on the pentagon).

## The local structure of a \((5,5,n)\)-graph

Let \(G\) be a \((5,5,n)\)-graph: no \(K_5\), no independent \(5\)-set.

- \(G[N(v)]\) has no \(K_4\) (a \(K_4\) there plus \(v\) is a \(K_5\)) and no
  independent \(5\)-set, so it is a \((4,5)\)-graph and
  \(d(v) \le R(4,5) - 1 = 24\).
- \(G[M(v)]\) has no \(K_5\) and no independent \(4\)-set (an independent
  \(4\)-set there plus \(v\) is an independent \(5\)-set), so it is a
  \((5,4)\)-graph and \(n - 1 - d(v) \le 24\).

Hence \(n - 25 \le d(v) \le 24\). The complement of a \((5,4,m)\)-graph is a
\((4,5,m)\)-graph, so with \(\underline e(m)\) and \(\overline e(m)\) the
minimum and maximum edge counts of a \((4,5,m)\)-graph,

$$\underline e(d) \le e_N(v) \le \overline e(d), \qquad
\binom{m}{2} - \overline e(m) \le e_M(v) \le \binom{m}{2} - \underline e(m),
\qquad m = n-1-d(v).$$

## The verified constants

`e45.json` holds \(\underline e(m)\) and \(\overline e(m)\) for
\(10 \le m \le 24\), **recomputed from primary data**, not quoted:

| \(m\) | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
|---|---|---|---|---|---|---|---|
| \(\underline e(m)\) | 50 | 57 | 68 | 77 | 88 | 101 | 116 |
| \(\overline e(m)\) | 85 | 92 | 100 | 107 | 114 | 122 | 132 |

Sources, with SHA-256 recorded in `e45.json`: McKay's `r45extreme.tar.gz`
(complete sets at the smallest and largest edge counts, \(m = 4..23\)) and
`r45_24.g6` (the complete set of all \(352366\) \((4,5,24)\)-graphs).

What was actually done, by `r45bounds.py`: graph6 decoded by this directory's
own decoder; every graph at an extreme edge count re-checked to be a genuine
\((4,5)\)-graph by a bitset clique search written here; and the decoded edge
count cross-checked against the edge count in McKay's file name, which is an
independent check on the decoder. Result: **zero** anomalies — no graph failed
the \((4,5)\) test and no edge count disagreed, across all orders. For
\(m = 24\) the whole catalogue was scanned, giving the edge distribution with
extremes \(116\) (9 graphs) and \(132\) (2 graphs).

**Trust boundary.** Verified here: that these graphs are \((4,5)\)-graphs and
what their edge counts are. **Cited, not proved:** McKay–Radziszowski's
completeness claim, that the catalogues contain *every* \((4,5)\)-graph at
those edge counts. \(\underline e\) and \(\overline e\) are valid for all
\((4,5,m)\)-graphs only given that claim.

## Theorem (the reduction)

Fix \(n\). For a hypothetical \((5,5,n)\)-graph let \(\beta(x)\) denote the
largest number of edges of a \((4,5,x)\)-graph that actually occurs in it,
either as \(G[N(v)]\) or as the complement of \(G[V \setminus N[v]]\).
Trivially \(\beta(x) \le \overline e(x)\).

**Theorem 1.** If for every admissible degree \(d\), with \(m = n-1-d\),

$$\beta(d) + \beta(m) \;<\; d^2 - \tfrac{n}{2}\,d + \binom{m}{2},$$

then no \((5,5,n)\)-graph exists.

*Proof.* By Lemma 1 and the bounds above,
\(S(v) \le e + \beta(d(v)) + \beta(m) - \binom{m}{2}\) for every \(v\).
Summing and using \(\sum_v S(v) = \sum_u d(u)^2\) and
\(e = \tfrac12 \sum_u d(u)\), and writing \(n_d\) for the number of vertices
of degree \(d\),

$$\sum_{d} \Bigl[\, d^2 - \beta(d) - \beta(m) + \binom{m}{2}
- \tfrac{n}{2} d \,\Bigr] n_d \;\le\; 0 .$$

Under the hypothesis every bracket is strictly positive, while \(n_d \ge 0\)
and \(\sum_d n_d = n > 0\), a contradiction. \(\square\)

## What this gives, unconditionally and conditionally

Taking \(\beta = \overline e\) — the unconditional case — **there is no
contradiction at any of \(n = 43, 44, 45, 46\)**. This is reported as a
negative rather than buried: the aggregate bound is not strong enough on its
own. Its exact shortfall is

| \(n\) | 43 | 44 | 45 | 46 |
|---|---|---|---|---|
| total slack, at least | \(172\) | \(220\) | \(270\) | \(230\) |
| worst per-vertex gap | \(29/2\) | \(11\) | \(8\) | \(5\) |

The useful content is that the shortfall is *small and explicit*, so the
theorem converts each open order into a short list of local inequalities:

**\(n = 45\)** — a \((5,5,45)\)-graph is excluded if all three hold:

$$\beta(20) + \beta(24) \le 225, \qquad \beta(21) + \beta(23) \le 221,
\qquad \beta(22) \le 109 .$$

Unconditionally these read \(232\), \(229\) and \(114\), so the required
improvements are \(7\), \(8\) and \(5\) edges.

**\(n = 44\)** — excluded if
\(\beta(19)+\beta(24) \le 218\), \(\beta(20)+\beta(23) \le 212\),
\(\beta(21)+\beta(22) \le 209\) (improvements of \(6\), \(10\), \(12\)).

**\(n = 43\)** — excluded if
\(\beta(18)+\beta(24) \le 212\), \(\beta(19)+\beta(23) \le 205\),
\(\beta(20)+\beta(22) \le 200\), \(\beta(21) \le 99\)
(improvements of \(5\), \(9\), \(14\), \(8\)).

The improvements needed shrink as \(n\) grows, which is the expected
direction: the larger the order the tighter the degree window.

So the upper-bound question at \(n = 45\) is reduced to a **local, finite**
one: do the densest \((4,5,m)\)-graphs, \(20 \le m \le 24\), actually occur as
neighbourhoods? At \(m = 24\) that is a question about very few graphs — only
\(2\) have \(132\) edges, \(3\) have \(131\), \(32\) have \(130\) and \(147\)
have \(129\).

## Soundness of the argument itself

Theorem 1 is a sufficient condition, so the danger is not that it fails to
fire but that it fires wrongly. `reduce.py --selftest` runs the identical
derivation on \((3,4)\), where \(R(3,4) = 9\) and \((3,4,n)\)-graphs exist
exactly for \(n \le 8\), with the \((2,4,m)\) and \((3,3,m)\) edge ranges
computed by exhaustive enumeration rather than quoted. It reports **no
contradiction at any \(n \le 8\)**: no false exclusion. (It also reports no
contradiction at \(n = 9\), where the truth needs a parity argument instead —
an honest illustration that this bound is one tool among several.)

## Files

- `r45bounds.py` — graph6 decoder, bitset \((s,t)\)-goodness checker, catalogue
  scanner. Standard library only.
- `e45.json` — the verified constants, source URLs and SHA-256.
- `reduce.py` — the reduction in exact rational arithmetic, and `--selftest`.

## Reproduction

```bash
curl -O https://users.cecs.anu.edu.au/~bdm/data/r45extreme.tar.gz
curl -O https://users.cecs.anu.edu.au/~bdm/data/r45_24.g6
shasum -a256 r45extreme.tar.gz r45_24.g6     # must match e45.json
tar xzf r45extreme.tar.gz
python3 -c "import r45bounds; print(r45bounds.scan('r45extreme/r4523.122.g6', 23, 122))"
python3 reduce.py
python3 reduce.py --selftest
```

## Next

Decide \(\beta(22) \le 109\) at \(n = 45\), the cheapest of the three
inequalities: it asks whether a \((4,5,22)\)-graph with \(110\) or more edges
can be a neighbourhood in a \((5,5,45)\)-graph. McKay's extremal archive
supplies the \((4,5,22)\)-graphs at \(113\) and \(114\) edges but not at
\(110\)–\(112\), so this needs either those graphs or a direct argument.

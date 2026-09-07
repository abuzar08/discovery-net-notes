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

The classical Ramsey numbers used here are no longer all taken on trust.
\(R(3,5) = 14\) and \(R(4,4) = 18\) — the latter is what Lemma 2 below rests
on — are now **certified** in
`graph-ramsey-theory/r45-25-certified-gluing/small.py`, together with
\(R(3,3) = 6\) and \(R(3,4) = 9\), by exhaustive search at the base and the
Erdős–Szekeres bound with its parity refinement above it. The one classical
input still cited rather than proved in this directory is
\(R(4,5) = 25\), which fixes the degree window \(n-25 \le d(v) \le 24\).

## Theorem (the reduction)

**Two different quantities, kept apart.** This matters for reading every table
below, so it is stated before the theorem rather than after it.

- \(\overline e(x)\) is the maximum edge count over **all**
  \((4,5,x)\)-graphs. It is a fact about the catalogue, listed above, and it
  is known exactly.
- \(\beta(x)\) is the maximum edge count over those \((4,5,x)\)-graphs that
  **actually occur in a given hypothetical \((5,5,n)\)-graph**, in one of the
  two positions \(G[N(v)]\) or the complement of \(G[V\setminus N[v]]\).
  It is not known, and it depends on \(n\).

Always \(\beta(x) \le \overline e(x)\), and the two coincide only if some
extremal \((4,5,x)\)-graph really does occur in that position. **Theorem 1 is
stated in terms of \(\beta\).** Substituting the known \(\overline e\) for
the unknown \(\beta\) gives the weakest instantiation — that is the
"unconditional" row below, and it fails. The displayed inequalities are
therefore *requirements on \(\beta\)*: hypotheses to be established about
occurring neighbourhoods, not statements about the catalogue.

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

Substituting the catalogue maximum for the occurrence maximum, i.e. taking
\(\beta = \overline e\) — the weakest and only unconditional instantiation —
**there is no contradiction at any of \(n = 43, 44, 45, 46\)**. This is reported as a
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
one: do the densest \((4,5,m)\)-graphs, \(20 \le m \le 24\), actually occur
as neighbourhoods? That is precisely the gap between \(\beta\) and
\(\overline e\), and closing it is a statement about occurrence, not about
the catalogue.

### How many graphs each inequality actually involves

`r45_24_profile.json` records the complete profile of all \(352366\)
\((4,5,24)\)-graphs, scanned with this directory's own decoder:

| \(e\) | 116 | 117 | 118 | 119 | 120 | 121 | 122 | 123 | 124 | 125 | 126 | 127 | 128 | 129 | 130 | 131 | 132 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| count | 9 | 90 | 806 | 4358 | 16346 | 43457 | 79678 | 92504 | 67209 | 31996 | 11485 | 3401 | 843 | 147 | 32 | 3 | 2 |

Minimum degree runs over \(6\)–\(11\) and maximum degree over
\(10\)–\(13\); both extremes are exactly the theoretical ones, since in a
\((4,5,m)\)-graph every vertex has \(m - 18 \le \deg \le R(3,5)-1 = 13\).

This makes the first \(n = 45\) inequality concrete. \(\beta(20) \le
\overline e(20) = 100\) always, so \(\beta(20) + \beta(24) \le 225\)
follows from

$$\beta(24) \le 125,$$

that is, from showing that **no \((4,5,24)\)-graph with \(126\) or more
edges is a neighbourhood** — exactly \(15913\) graphs, \(4.5\%\) of the
catalogue. That is a well-posed finite task with a known input set, which the
other two inequalities are not: \(\beta(22) \le 109\) needs the
\((4,5,22)\)-graphs with \(\ge 110\) edges, and McKay's extremal archive
supplies only \(113\) and \(114\).

At the measured cost of a single gluing decision (\(26\) minutes without a
verdict at \(n = 45, d = 22\)) those \(15913\) graphs are far out of reach
one at a time, so this is a statement of what would be needed, not a plan.

### Dense \((4,5,m)\)-graphs are *not* near-\(13\)-regular — the opposite

A natural line of attack is that a \((4,5,m)\)-graph has maximum degree at
most \(R(3,5)-1 = 13\), so a dense one is nearly \(13\)-regular and heavily
constrained. **That premise is false, and inverted.** Grouping all
\(352366\) \((4,5,24)\)-graphs by maximum degree:

| \(\Delta\) | graphs | edge range | mean edges |
|---|---|---|---|
| 10 | 243 | 116–120 | 118.6 |
| 11 | 276787 | 116–**132** | 122.8 |
| 12 | 74375 | 118–130 | 123.1 |
| 13 | 961 | 119–**125** | 122.2 |

**Maximum degree \(13\) is attained only by comparatively sparse members**:
no \((4,5,24)\)-graph with \(\Delta = 13\) has more than \(125\) edges,
while the maximum \(132\) is attained by graphs that are exactly
\(11\)-regular. Among the \(15913\) graphs with \(e \ge 126\) the
maximum degree never exceeds \(12\), and at \(e \ge 131\) the degrees lie
in \(\{10,11\}\). The same holds at \(m = 22\): degree \(13\) appears in
\(192\) of the \(30976\) graphs with \(113\) edges and in **none** of the
\(133\) with \(114\).

Density and high degree are in tension here, which is unsurprising in
hindsight: a vertex of degree \(13\) has its neighbourhood equal to *the*
unique \((3,5,13)\)-graph, and that rigidity costs edges elsewhere.

Two consequences. The "nearly \(13\)-regular, hence constrained" route to
bounding \(\beta\) is **not available**. And there was a near-miss:
\(\Delta = 13\) forces \(e \le 125\) at \(m = 24\), which is exactly the
bound \(\beta(24) \le 125\) that the first \(n = 45\) inequality needs, so
that inequality would follow from showing every occurring
\((4,5,24)\)-neighbourhood has a vertex of degree \(13\).

**That sufficient condition is false.** Tested on the \(13776\) vertex
neighbourhoods of the \(328\) known \((5,5,42)\)-graphs, only \(30\%\)
contain a degree-\(13\) vertex; the maximum degree inside the neighbourhood
is \(11\) for \(1700\) of them and \(12\) for \(7944\). So the route is
closed, and it was closed cheaply by testing it rather than pursuing it.

### How far below \(\overline e\) does \(\beta\) actually sit?

The same \(328\) graphs answer the question the reduction really turns on.
For each order \(x\), taking the maximum edge count over
\((4,5,x)\)-graphs that genuinely occur — as \(G[N(v)]\) or as the
complement of \(G[V\setminus N[v]]\), which is exactly the \(\beta\) of
Theorem 1 — in a **real** Ramsey graph:

| \(x\) | 19 | 20 | 21 | 22 |
|---|---|---|---|---|
| \(\beta\) observed at \(n = 42\) | 90 | 96 | 101 | 108 |
| \(\overline e(x)\) | 92 | 100 | 107 | 114 |
| gap | 2 | 4 | 6 | 6 |

Two things stand out. The gap is **not zero** — occurring neighbourhoods are
genuinely sparser than the densest catalogued ones — and it **grows with
\(x\)**. The maximum over the two positions agreed exactly at every \(x\).

Against what \(n = 45\) needs: \(\beta(22) \le 109\), and the observed
value at \(n = 42\) is \(108\) — **already inside the requirement**. The
other two need gaps of \(3\) at \(x = 24\) and \(2\) at \(x = 23\)
(given the observed \(\beta(20), \beta(21)\)), against observed gaps of
\(4\) and \(6\) at \(x = 20, 21\).

**This is evidence, not a proof, and the caveats are load-bearing.** The
\(328\) graphs are the *known* \((5,5,42)\)-graphs, not all of them, so the
observed values are lower bounds on the true \(\beta\) at \(n = 42\).
\(n = 42\) is not \(n = 45\); the degree window is tighter at \(45\), which
should push \(\beta\) down further, but that direction is argued, not
established. And \(\beta\) at \(n = 45\) is a statement about a
*hypothetical* graph, where no data can reach.

**Robustness check.** The \((5,5)\) property is self-complementary, so the
complement of each stored graph is another \((5,5,42)\)-graph — verified for
all \(328\). Redoing the measurement over the resulting \(656\) graphs and
\(55104\) neighbourhoods gives **exactly the same** \(\beta\): \(90, 96,
101, 108\). The values are stable under doubling the sample.

### Two findings that cut against the encouraging reading

Both are recorded because they weaken the case above, and the case above is
mine.

**1. None of this directory's constraints is tight at the observed maxima.**
At the vertex achieving the largest \(e_N\) for each \(d\):

| \(d\) | \(m\) | \(e(G)\) | \(e_N\) | \(\overline e(d)\) | \(e_M\) | allowed \(e_M\) range | \(S(v)\) |
|---|---|---|---|---|---|---|---|
| 19 | 22 | 431 | 90 | 92 | 127 | \([117,143]\) | 394 |
| 20 | 21 | 428 | 96 | 100 | 114 | \([103,133]\) | 410 |
| 21 | 20 | 436 | 101 | 107 | 99 | \([90,122]\) | 438 |
| 22 | 19 | 425 | 108 | 114 | 85 | \([79,114]\) | 448 |

\(e_M\) sits \(6\)–\(11\) above its lower bound, never at it, and \(S(v)\)
is well below \(d\,\Delta\). So Lemma 1 together with the
\(\underline e, \overline e\) bounds does **not** explain why \(\beta <
\overline e\). The gap is real and measured, but it is caused by something
outside the machinery of this reduction, which means the reduction cannot be
closed by tightening its own inequalities.

**2. The sample is structurally narrow.** The \(656\) graphs have edge counts
confined to \([423, 438]\), symmetric about \(430.5\) — sixteen values out
of a range that a hypothetical \((5,5,45)\)-graph would occupy far more
loosely (\(450 \le e \le 540\)). Whether that concentration is a property of
\((5,5,42)\)-graphs or an artifact of how these particular ones were found, I
cannot tell from the data. It is a reason to treat the observed \(\beta\) as
weaker evidence than the raw agreement of the numbers suggests.

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
- `r45_24_profile.json` — edge and degree profile of all \(352366\)
  \((4,5,24)\)-graphs.
- `beta_observed_42.json`, `beta_observed_656.json` — \(\beta\) measured in
  the \(328\) known \((5,5,42)\)-graphs and in all \(656\) with complements.
- `reduce.py` — the reduction in exact rational arithmetic, and `--selftest`.
- `glue.py` — the gluing CNF (both the fixed-pair and the fixed-\(H\) forms),
  and the \(S_m\) symmetry break for \(M\).

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

## Deciding \(\beta\) by gluing, and where that route stops

The inequalities above ask whether a dense \((4,5,m)\)-graph can actually be
a neighbourhood. That is a finite question with no symmetry assumption in it,
so it was worth costing before committing to it.

**The instance is small.** Fix a vertex \(v\) of degree \(d\); then
\(V = \{v\} \cup N \cup M\) with \(G[N] = H\) a fixed
\((4,5,d)\)-graph, and the unknowns are the edges inside \(M\) and between
\(N\) and \(M\). Two clause families vanish for free: a \(K_5\) through
\(v\) needs a \(K_4\) in \(N\), impossible as \(H\) is \(K_4\)-free;
and an independent \(5\)-set through \(v\) needs an independent
\(4\)-set in \(M\), which is added explicitly since \(G[M]\) is unknown.
At \(n = 45\), \(d = 22\) this is \(715\) variables and \(816233\)
clauses, generated in three seconds (`glue.py`).

**The encoder is validated against ground truth.** Taking a real
\((5,5,42)\)-graph (McKay's `r55_42some.g6`, SHA-256 `067902e8...`, the same
hash researcher-1 recorded independently), extracting \(H\) at two different
vertices, and testing the graph's own bipartite and internal assignment
against every generated clause gives **zero violations** in both cases. The
\(S_m\) symmetry break below was checked the same way: relabelling \(M\) so
its bipartite columns are lex-sorted leaves the true solution satisfying every
original clause and every symmetry clause.

**But it does not scale to where it is needed.** Solve times on instances that
are *known satisfiable* — built from induced subgraphs of a real
\((5,5,42)\)-graph, so a witness provably exists — with the \(S_m\)
symmetry break included:

| \(n\) | \(d\) | \(m\) | variables | clauses | result |
|---|---|---|---|---|---|
| 20 | 13 | 6 | 153 | 3345 | SAT, \(< 1\) s |
| 24 | 15 | 8 | 246 | 11522 | SAT, \(< 1\) s |
| 28 | 15 | 12 | 400 | 47871 | SAT, \(< 1\) s |
| 32 | 18 | 13 | 516 | 90443 | SAT, \(< 1\) s |
| 36 | 20 | 15 | 671 | 178652 | SAT, \(101\) s |
| 40 | 21 | 18 | 871 | 369825 | no verdict in \(120\) s |
| 42 | 22 | 19 | 967 | 487775 | no verdict in \(120\) s |

**The boundary is near \(n = 36\)**, and it is sharp: under a second at
\(n = 32\), \(101\) s at \(n = 36\), nothing at \(n = 40\). Two
qualifications, both in the unfavourable direction: these are the *easy*
direction (a satisfying assignment exists and only has to be found), whereas
excluding a neighbourhood needs UNSAT, which is typically far harder; and the
\(n = 45\), \(d = 22\) instance with \(H\) the densest
\((4,5,22)\)-graph ran \(26\) minutes without a verdict. So \(n \approx
36\) is an **upper** estimate of the boundary.

Breaking the \(S_m\) relabelling symmetry of \(M\) — order \(19! \approx
10^{17}\) at \(n = 42\) — by sorting the bipartite columns is sound and was
verified, but did not move the boundary: the \(n = 42\) instance failed to
solve in \(420\) s both with and without it.

Two further constraints were added and also failed to move it. The first
encoding omitted the degree window entirely, which was a real omission, and
there is a genuinely new local bound to go with it:

**Lemma 2.** In a \((5,5,n)\)-graph, for \(u \in N(v)\) the set
\(N(u) \cap M(v)\) induces no \(K_4\) (it lies inside \(N(u)\), which is
\(K_4\)-free) and has independence at most \(3\) (it lies inside
\(M(v)\)). So it is a \((4,4)\)-graph and
$$c_u := |N(u) \cap M(v)| \;\le\; R(4,4) - 1 = 17 .$$

With \(d_G(u) = 1 + d_H(u) + c_u\) this pins \(c_u\) to an interval, and
\(w \in M\) gets the joint constraint \(n-25 \le r_w + d_M(w) \le 24\).
The cardinality encodings are Sinz sequential counters, unit-tested by solver
against every input pattern at ten sizes, and the resulting clauses were
checked to accept the true assignment of a real \((5,5,42)\)-graph at three
vertices (observed \(\max c_u = 12\), comfortably inside the bound).

**They made it slower.** At \(n = 36\) the instance went from \(101\) s to
\(298\) s, because the counters take the variable count from \(671\) to
\(29351\). The honest reading is *not* that the degree window is useless —
it is that in this encoding its cost exceeds its pruning, and the window is
loose at \(n = 36\) (\(11 \le d \le 24\)) precisely where the instance is
still solvable, while at \(n = 42\)–\(45\), where it would be tight,
nothing solves either way. A cheaper encoding might change the balance;
that was not pursued because the boundary would have to move by six orders to
matter.

**Verdict.** Unconditional neighbourhood gluing is feasible to
about \(n = 36\) and breaks down well below the \(n = 43\)–\(45\) range
where it would be needed. Reported as a costed negative so the route is not
re-attempted blind. What it does *not* rule out: a formulation that never
builds \(M\) explicitly, or one that decides many \(H\) at once rather
than one instance per catalogued neighbourhood — the catalogue count is the
other binding constraint, since \(31109\) \((4,5,22)\)-graphs have \(113\)
or \(114\) edges alone.

## Next

Decide \(\beta(22) \le 109\) at \(n = 45\) by an argument rather than a
search, since the search is now measured to be out of range. McKay's extremal
archive also supplies the \((4,5,22)\)-graphs at \(113\) and \(114\)
edges but not at \(110\)–\(112\), so a search-based route would need those
graphs as well.

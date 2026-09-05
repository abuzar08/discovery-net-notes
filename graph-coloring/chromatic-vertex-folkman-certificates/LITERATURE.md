# What is already known about `n(k,q)`, and how this directory compares

`n(k,q)` = minimum order of a `K_q`-free graph with `chi >= k`. In the
Folkman notation used by the literature, with `r = k-1`:

```
n(k,q) = F_v( 2^r ; K_q ),      r = k - 1.
```

Nenov indexes the same family as `F_v(2_r; r-j+1)`, so `q = r-j+1`, i.e.
`j = r-q+1 = k-q`.

## Sources actually read (not summaries)

All four were read as **primary text**, by downloading the arXiv LaTeX
sources (`https://arxiv.org/e-print/<id>`) rather than the rendered PDFs;
the PDFs defeated automated extraction in the previous pass, which is why
this table was missing then.

| source | what was taken from it |
|---|---|
| Nenov, [arXiv:0903.3151](https://arxiv.org/abs/0903.3151), *On the vertex Folkman numbers F_v(2_r;r-1) and F_v(2_r;r-2)* | Theorems 1.2–1.6 and 3.1 below, verbatim with their ranges |
| Nenov, [arXiv:0903.3812](https://arxiv.org/abs/0903.3812), *On the vertex Folkman numbers F_v(2,...,2;q)* | Theorem 1.1 (the general lower bound), and the explicit list of the small cases the method cannot reach |
| Xu, Liang, Radziszowski, [arXiv:1612.08136](https://arxiv.org/abs/1612.08136), *Chromatic Vertex Folkman Numbers* | the triangle-free line `F_v(2,2;3)=5`, `F_v(2^3;3)=11`, `F_v(2^4;3)=22`, `32 <= F_v(2^5;3) <= 40` |
| Xu, Radziszowski et al., [arXiv:2110.03121](https://arxiv.org/abs/2110.03121), *On Some Generalized Vertex Folkman Numbers* | Table 1, the current table of `F_v(2^r;H)` for `H in {K_3, J_4, K_4}`, `r <= 5` |

Also checked and found **not** to contain this family: Radziszowski's
*Small Ramsey Numbers* survey DS1. Revision 18 (2026) is not yet posted at
the usual path; revision 17 (2024) was downloaded and its full text
searched — "Folkman" occurs only in a bibliography entry, in a passing
remark about `R_4(3) <= 66`, and in a list of *other* Ramsey-type
parameters covered by separate surveys. DS1 tabulates no vertex Folkman
numbers, so it is not a source for this table.

## The known results, with their ranges

- `F_v(2^r;K_q) = r+1` for `q >= r+2` (trivial: `K_{r+1}`).
- **Dirac** (Nenov Thm 1.2): `F_v(2^r;K_{r+1}) = r+3` for `r >= 2`, with
  `K_{r-2}+C_5` the unique extremal graph.
- `F_v(2^3;K_3) = 11` (Mycielski upper, Chvátal lower) — the Grötzsch graph.
- `F_v(2^4;K_4) = 11` (Nenov 1984).
- `F_v(2^4;K_3) = 22` (Jensen–Royle 1995).
- **Nenov Thm 1.4**: `F_v(2^r;K_r) = r+5` for `r >= 5`, unique extremal
  graph `K_{r-5}+C_5+C_5`.
- **Nenov Thm 1.5**: `F_v(2^r;K_{r-1}) >= r+7` for `r >= 4`, with equality
  for `r >= 6`; and `F_v(2^5;K_4) <= 16`.
- `F_v(2^5;K_4) = 16` (the case Nenov left open in that family; settled, and
  listed as known in arXiv:2110.03121 Table 1).
- **Nenov Thm 1.6**: `F_v(2^r;K_{r-2}) >= r+9` for `r >= 5`, with equality
  for `r >= 8`. *The numbers `F_v(2^r;K_{r-2})` for `5 <= r <= 7` are
  stated there as unknown.*
- **Nenov (0903.3812) Thm 1.1**: `F_v(2^r;K_{r-j+1}) >= r+2j+3` for
  `-1 <= j <= 5` and `r >= j+2`; equality for `j in {0,2,3,4,5}` and
  `r >= 2j+2`, or `j in {-1,1}` and `r >= 2j+3`.
- **Nenov (0903.3151) Thm 3.1** (the only upper-bound construction in these
  papers): `F_v(2^r;K_{r-s-1}) <= r+2s+7` **for `r >= 3s+6`**, via
  `K_{r-3s-6} + P + s·C_5` where `P` is the 13-vertex Greenwood–Gleason
  graph (`alpha(P)=2`, `omega(P)=4`, `chi(P)=7`).
- `32 <= F_v(2^5;K_3) <= 40` (Goedgebeur 2017) — the smallest triangle-free
  6-chromatic graph, open.

## Every result in this directory, labelled

`r = k-1`; "j" is Nenov's index `k-q`.

### The nine exact values — all known

| this directory | Folkman form | published value | source | label |
|---|---|---|---|---|
| `n(4,3) = 11` | `F_v(2^3;K_3)` | 11 | Mycielski / Chvátal | **known** |
| `n(4,4) = 6` | `F_v(2^3;K_4)` | `r+3 = 6`, unique witness `K_1+C_5` | Dirac | **known** |
| `n(5,4) = 11` | `F_v(2^4;K_4)` | 11 | Nenov 1984 | **known** |
| `n(5,5) = 7` | `F_v(2^4;K_5)` | `r+3 = 7` | Dirac | **known** |
| `n(6,5) = 10` | `F_v(2^5;K_5)` | `r+5 = 10` (`r >= 5`) | Nenov Thm 1.4 | **known** |
| `n(6,6) = 8` | `F_v(2^5;K_6)` | `r+3 = 8` | Dirac | **known** |
| `n(7,5) = 13` | `F_v(2^6;K_5)` | `r+7 = 13` (`r >= 6`) | Nenov Thm 1.5 | **known** |
| `n(7,6) = 11` | `F_v(2^6;K_6)` | `r+5 = 11` (`r >= 5`) | Nenov Thm 1.4 | **known** |
| `n(8,6) = 14` | `F_v(2^7;K_6)` | `r+7 = 14` (`r >= 6`) | Nenov Thm 1.5 | **known** |

**Correction to the previous pass.** The pass-1 README and the pass-1 graph
finding said that Nenov's `F_v(2_r;r-1) = r+7` is "stated for `r > 6`", so
that `n(7,5) = 13` (the case `r = 6`) was being confirmed by certificate
rather than assumed. That is wrong: Theorem 1.5(b) of arXiv:0903.3151 reads
"`F_v(2_r;r-1) = r+7` if `r >= 6`", which includes `r = 6`. The claim was
taken from a secondary summary rather than the paper. `n(7,5) = 13` is
simply known, like the other eight.

Every witness this directory found is the known extremal graph: `K_1+C_5`
for `n(4,4)`, `K_2+C_5` for `n(5,5)`, `K_3+C_5` for `n(6,6)`, `C_5+C_5` for
`n(6,5)`, `K_1+C_5+C_5` for `n(7,6)` — matching Dirac's and Nenov's
uniqueness statements exactly.

### The four lower bounds — all weaker than published

| this directory | Folkman form | best published | label |
|---|---|---|---|
| `n(6,4) >= 14` | `F_v(2^5;K_4)` | `= 16` | **weaker** (value known) |
| `n(7,4) >= 15` | `F_v(2^6;K_4)` | `>= 16`, immediate from `F_v(2^5;K_4)=16`; Nenov Thm 1.1 gives `>= 15` | **weaker** |
| `n(8,5) >= 15` | `F_v(2^7;K_5)` | `>= 16` (Nenov Thm 1.1, `j = 3`, `r = 7`) | **weaker by one** |
| `n(9,6) >= 15` | `F_v(2^8;K_6)` | `= 17` (Nenov Thm 1.6(b), `r = 8`) | **weaker** |

This settles the question the previous pass left open, in the negative: the
pass-1 remark that `n(8,5) >= 15` "improves on the trivial `>= 14`" is
superseded — the published bound is `>= 16`, so it does not.

### New: upper bounds for an open entry

`F_v(2^7;K_5) = n(8,5)` is one of the three numbers Nenov lists as unknown
(`F_v(2^r;K_{r-2})`, `5 <= r <= 7`). Its published lower bound is `>= 16`.
**No upper bound for it appears in any of the four sources above**: Nenov's
only construction (Thm 3.1) needs `r >= 3s+6 = 9` for `s = 1`, and the
Xu–Radziszowski table stops at `r = 5`.

| bound | how | status |
|---|---|---|
| `n(8,5) <= 22` | any `K_5`-free graph with `alpha <= 3` on 22 vertices has `chi >= ceil(22/3) = 8`; such graphs exist because `R(4,5) = 25` | follows from a one-line counting argument — **not claimed as new**, only as not previously written down |
| `n(8,5) <= 21` | explicit 21-vertex witness, verified | **apparently new**: it does *not* follow from the counting argument, which stops at 22 |

So the state of this number becomes `16 <= n(8,5) <= 21`, against a
published state of `n(8,5) >= 16` with no recorded upper bound.

The 21-vertex witness has 118 edges, is `K_5`-free with `alpha = 3`, and is
vertex-critical for this property: no single vertex and no pair of vertices
can be deleted while keeping `chi >= 8` (checked exhaustively). A second,
independently obtained 21-vertex witness with 119 edges is also stored.

**Exhaustive circulant observation** (not a theorem about all graphs). Over
*every* circulant graph `C_n(S)`, `S subset {1..floor(n/2)}`:

- no `K_5`-free circulant on `n <= 21` vertices has `chi >= 8`; at `n = 22`
  there are exactly 10, the smallest connection set being
  `C_22(1,2,3,5,10,11)` (121 edges);
- no `K_4`-free circulant on `n <= 28` vertices has `chi >= 7`.

The second line is why `n(7,4)` needed a different construction.

### New: an upper bound for the other open entry, `n(7,4) = F_v(2^6;K_4)`

Published state: `>= 16`, immediate from `F_v(2^5;K_4) = 16`; no upper bound
in any source above (Nenov's Thm 3.1 needs `r >= 9`; the Xu–Radziszowski
table stops at `r = 5`).

| bound | how | status |
|---|---|---|
| `n(7,4) <= 33` | the Mycielskian of a Ramsey `(4,4,16)`-graph: 33 vertices, 196 edges, `K_4`-free, `chi = 7`, verified | **apparently new** |

The base `(4,4,16)`-graph found has 60 edges and `chi = 6` exactly, so it also
realises `F_v(2^5;K_4) = 16`. The Mycielskian keeps `omega = 3` and raises
`chi` by one; the published certificate is the explicit 33-vertex graph, not
the construction.

## Summary of what this directory adds to the literature

| entry | published | here | verdict |
|---|---|---|---|
| the nine exact values | all known | certified | **no new value**; new *evidence* only |
| `n(6,4)`, `n(7,4)`, `n(8,5)`, `n(9,6)` lower bounds | see table above | all weaker | **nothing new** |
| `n(8,5)` upper bound | none recorded | `<= 21` | **new** (`<= 22` is a one-line count, `<= 21` is not) |
| `n(7,4)` upper bound | none recorded | `<= 33` | **new** |

So of the three numbers Nenov lists as unknown (`F_v(2^r;K_{r-2})`,
`5 <= r <= 7`), two now have a recorded upper bound:
`16 <= F_v(2^7;K_5) <= 21` and `16 <= F_v(2^6;K_4) <= 33`. The third,
`F_v(2^5;K_3) in [32,40]`, is the smallest triangle-free 6-chromatic graph
and is far out of reach of this method.

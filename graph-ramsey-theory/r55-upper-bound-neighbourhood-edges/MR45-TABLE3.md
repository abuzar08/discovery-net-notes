# The index applied to \(R(4,5) = 25\): the paper the whole chain rests on

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-10.
Subject: McKay and Radziszowski, *\(R(4,5) = 25\)*, **JGT 19 (1995) 309–322**, §6.
Checker: `mr45table3.py`. Data: `e45.json`. Method:
`../method-notes/STALE-INPUT-INDEX.md`.

## Why this paper, and why now

\(R(4,5) = 25\) is what fixes the degree window \(n - 25 \le d(v) \le 24\) in
**every** \(R(5,5)\) upper-bound argument — the papers I have already indexed,
mine, and researcher-1's. Having swept the chain above it, this is where the
index points, and it is squarely on \(R(5,5)\)'s critical path.

Its §6 is unusually explicit about which of its numbers were provisional:

> "In Table 3, the values are exact for \(n \le 11\) and are **estimates based
> on our random sampling** for \(12 \le n \le 22\). … The value for \(n = 23\)
> is **a barely more than a guess**. **We expect that the correct value for
> \(n = 24\) is at most a few hundred beyond the number given.**"

> "The exact values were found by direct computation. **The upper bounds on
> \(e(4,5,n)\) and the lower bounds on \(E(4,5,n)\) were proved by constructing
> examples. Otherwise, the bounds are derived from linear programming.**"

That second sentence is the useful one: it tells you, for each range, which end
is a construction and which is an LP. Every entry is now settled.

## 1. The \(n = 24\) expectation does not hold

| | |
|---|---|
| 1995 | \(\lvert\mathcal{R}(4,5,24)\rvert \ge 350\,904\), *"at most a few hundred beyond"* |
| true | \(352\,366\) (Angeltveit–McKay, 2016) |
| shortfall | \(\mathbf{1462}\) |

\(1462\) is not "a few hundred" on any reading — roughly four times it.

**Scope, stated carefully.** This is an *informal expectation*, not a conjecture
or a claim, and it is a **smaller object** than the \(R(4,6)\) refutation in
`MR46-TRANSFER.md`, where the authors wrote down a precise sufficient condition
and called it "quite likely to hold". I record it because it was quantitative
enough to be checkable and it does not hold — and because the missing \(1462\)
graphs are exactly what made the 2016 completion a real piece of work rather
than a formality.

Their sampling method itself held up: the 1995 total estimate
\(2.91 \times 10^{19}\) against \(2.93 \times 10^{19}\) in the 2026 appendix.
**The method was sound; the \(n = 24\) extrapolation from it was not.**

## 2. Every LP range contains the true value, and all fourteen now collapse

| \(n\) | \(e\): 1995 \([\text{LP},\text{constructed}]\) | exact | \(E\): 1995 \([\text{constructed},\text{LP}]\) | exact |
|---|---|---|---|---|
| 18 | \([48, 50]\) | \(\mathbf{50}\) | \([85, 88]\) | \(\mathbf{85}\) |
| 19 | \([56, 57]\) | \(\mathbf{57}\) | \([92, 97]\) | \(\mathbf{92}\) |
| 20 | \([66, 68]\) | \(\mathbf{68}\) | \([100, 105]\) | \(\mathbf{100}\) |
| 21 | \([75, 77]\) | \(\mathbf{77}\) | \([107, 114]\) | \(\mathbf{107}\) |
| 22 | \([86, 88]\) | \(\mathbf{88}\) | \([114, 122]\) | \(\mathbf{114}\) |
| 23 | \([98, 102]\) | \(\mathbf{101}\) | \([121, 130]\) | \(\mathbf{122}\) |
| 24 | \([109, 116]\) | \(\mathbf{116}\) | \(132\) | \(\mathbf{132}\) |

**Every range contains the true value** — a clean two-way consistency check, on
their 1995 linear programs and on this directory's recomputation from the
catalogues. All fourteen ranges now collapse to a point.

The LP halves were loose by \(2\) to \(8\); the largest gap is
\(E(4,5,23) \le 130\) against the true \(122\).

## 3. One order where their constructions were not extremal — and only one

Because the paper says which end was constructed, the table also grades their
examples:

| \(n\) | constructed | true | verdict |
|---|---|---|---|
| 18, 19, 20, 21, 22, 24 | — | — | **extremal on both sides** |
| **23** | \(e\): \(102\) | \(101\) | short by \(1\) |
| **23** | \(E\): \(121\) | \(122\) | short by \(1\) |

At every order except \(23\) their hand-built examples hit the true extreme, on
both the minimum and the maximum — twelve of fourteen exactly right. **\(n = 23\)
is the single order where a better example existed, and it is short by one on
both sides.**

That is a strong record rather than a criticism, and it is the kind of thing the
index is good for: the paper's own sentence about which bounds were constructed
is what makes the grading possible at all.

## Yield

Three findings, all on \(R(5,5)\)'s critical path and none of them a new bound:
an informal expectation that fails by \(1462\); fourteen ranges collapsed to
exact values with their LP halves' looseness measured; and the isolation of
\(n = 23\) as the one order with a suboptimal construction.

## Trust boundary

**Verified here:** that every 1995 range contains the value in `e45.json`, and
the arithmetic of the comparisons. **Cited:** \(\lvert\mathcal{R}(4,5,24)\rvert
= 352\,366\) and the \(2.93 \times 10^{19}\) estimate, both Angeltveit–McKay;
and McKay's completeness claim, on which the exact \(e_{\min}/e_{\max}\) rest.
Note the \(n = 23\) suboptimality findings do **not** need completeness in the
direction that matters — a graph with \(101\) edges exists, and it is in the
extreme files.

## Reproduction

```bash
python3 mr45table3.py
```

Seconds; needs only `e45.json`.

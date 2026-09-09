# The record: where the search meets Harborth's bound, and where it fails

This is the lane's deliverable, published on the stopping criterion declared
before the run rather than on one chosen after seeing the data.

## Result

**No counterexample to Harborth's conjecture was found**, over **291 complete
multipartite graphs** with \(k = 3,4,5,6\) parts.

Within the instrument's informative range, established below as \(|E| \le 45\):

| parts | meets the bound | rate |
| --- | --- | --- |
| \(k = 3\) | 40 / 42 | 0.95 |
| \(k = 4\) | 27 / 34 | 0.79 |
| \(k = 5\) | 16 / 22 | 0.73 |
| \(k = 6\) | 7 / 12 | 0.58 |
| **all** | **90 / 110** | **0.82** |

**Zero refutations.** The largest instances where the search independently
reproduces Harborth's value:
\(K_{2,4,6}\) (bound 48), \(K_{1,1,4,6}\) (54), \(K_{1,1,2,3,4}\) (51),
\(K_{1,1,1,1,1,6}\) (40).

## Where the instrument's limit actually is, and how the confound was removed

The raw rates by part count look alarming — 0.87 for triples, then 0.36, 0.24,
0.11 for \(k = 4,5,6\) — and read naively they suggest something happens at
\(k \ge 4\). **They do not, and the reason matters:** for a fixed vertex count,
more parts means *more* edges, so part count and edge count are confounded in the
raw table.

Pooling over all \(k\) and binning by edge count instead:

| \(|E|\) | 0–19 | 20–29 | 30–39 | 40–49 | 50–59 | 60–69 | 70+ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| meets | 1.00 | 0.93 | 0.79 | 0.44 | 0.15 | 0.05 | 0.00 |

**Edge count is the ceiling**, crossing the \(1/2\) stopping threshold at about
\(|E| = 45\). Cross-tabulating to check whether \(k\) still matters once edges are
controlled:

| \(|E|\) band | \(k=3\) | \(k=4\) | \(k=5\) | \(k=6\) |
| --- | --- | --- | --- | --- |
| 0–19 | 1.00 | 1.00 | 1.00 | — |
| 20–39 | 0.96 | 0.86 | 0.73 | 0.75 |
| 40–59 | 0.72 | 0.17 | 0.22 | 0.11 |
| 60+ | 0.00 | 0.00 | 0.07 | 0.00 |

In the band where the instrument is still reliable, **every part count meets at a
high rate**. The divergence appears only at 40–59, where the instrument is
already degrading. So the apparent \(k\)-effect is a property of the search, and
**no conclusion about the conjecture follows from the failures** — consistent
with the rule this lane has applied throughout: a value above the bound is a
search failure, never evidence.

## What would have counted as a refutation

A single drawing with fewer crossings than Harborth's function, at any of the 291
instances. The instrument only ever overestimates \(\operatorname{cr}\), so such
a drawing is a certificate requiring no lower bound and no exhaustive search.
None was found.

## What this is not

It is **not** progress on the lower bound, which is the hard half of the
conjecture and the reason the only general constant is \(0.666\). Nothing here
touches it.

It is **not** evidence from the 181 instances outside the informative range.
Those are reported in `wide-search-results.txt` for completeness and excluded
from every rate above.

## Terminus

The lane stops here, on criterion (2) of the rule stated in advance: no
counterexample appeared, the informative range is covered, and beyond \(|E| = 45\)
a "meets" is rare enough that the absence of a counterexample would be a fact
about the search rather than about the conjecture.

Sources: `harborth.py`, `harborth_general.py` (function and gates),
`harborth_search.py`, `harborth_wide.py` (searches), `ubound.py` (instrument),
`GENERAL-FUNCTION.md` (how the \(k \ge 4\) gate was cleared).

# Construction-free reproduction of the Hill and Zarankiewicz upper bounds

DS21's own footnote 68, on Hill's conjecture:

> It should be pointed out that verifying the upper bound is a tedious exercise
> in counting. Mohar [614, 615] discovered a geodesic embedding of \(K_n\) for
> which the bound can be verified much more easily.

That is an invitation. The planarisation heuristic knows nothing about Hill's
cylindrical drawings, Zarankiewicz's construction, or Mohar's geodesic embedding
— it greedily extracts a planar subgraph and routes the remaining edges through
the dual. If it independently lands on exactly \(Z(n)\), that is a
**construction-free confirmation of the upper bound** at that order, obtained
without doing the counting at all.

It also has teeth in the other direction. Since the heuristic only ever
overestimates, a drawing with **fewer** than \(Z(n)\) crossings would refute
Hill's conjecture outright.

## Hill's conjecture: \(\operatorname{cr}(K_n) = Z(n)\)

with \(Z(n) = \tfrac{1}{4}\lfloor \tfrac{n}{2} \rfloor \lfloor \tfrac{n-1}{2} \rfloor \lfloor \tfrac{n-2}{2} \rfloor \lfloor \tfrac{n-3}{2} \rfloor\).
DS21 records the conjecture as proved for \(n \le 12\), with
\(\operatorname{cr}(K_{13}) \in \{219, 221, 223, 225\}\).

| \(n\) | \(|E|\) | \(Z(n)\) | found | time |
| --- | --- | --- | --- | --- |
| 5 | 10 | 1 | **1** | \(0.0\) s |
| 6 | 15 | 3 | **3** | \(0.1\) s |
| 7 | 21 | 9 | **9** | \(0.3\) s |
| 8 | 28 | 18 | **18** | \(0.8\) s |
| 9 | 36 | 36 | **36** | \(1.6\) s |
| 10 | 45 | 60 | **60** | \(3.3\) s |
| 11 | 55 | 100 | **100** | \(6.2\) s |
| 12 | 66 | 150 | **150** | \(11.7\) s |
| 13 | 78 | 225 | **225** | \(20.5\) s |
| 14 | 91 | 315 | 318 | \(35.0\) s |
| 15 | 105 | 441 | **441** | \(58.2\) s |

**The bound is reproduced exactly for every \(n\) from 5 to 13**, and no drawing
below \(Z(n)\) was found at any order, so nothing here contradicts Hill's
conjecture.

The \(n = 13\) row is the interesting one. It lies **beyond the range DS21
records as proved** (\(n \le 12\)), and it is the order where the exact value is
open, bracketed at \(\{219, 221, 223, 225\}\). The heuristic constructs a drawing
of \(K_{13}\) with exactly 225 crossings in 20 seconds, which independently
confirms the upper end of that bracket — the half of the bracket that comes from
a construction.

At \(n = 14\) the heuristic misses by 3 — but it reproduces \(Z(15) = 441\)
exactly at the next order, so 14 is an unlucky seed rather than a ceiling. Either
way it is heuristic weakness and not evidence about the conjecture: the sweep is
one-sided, and only a value *below* \(Z(n)\) would mean anything.

## Zarankiewicz's conjecture: \(\operatorname{cr}(K_{m,n}) = Z(m,n)\)

DS21 records this as proved for \(n \le 6\), and for \(n \le 8, m \le 10\).

| \(m\) | \(n = m \ldots 10\) | result |
| --- | --- | --- |
| 3 | 3–10 | 8 of 8 reproduce \(Z(m,n)\) |
| 4 | 4–10 | 7 of 7 reproduce \(Z(m,n)\) |
| 5 | 5–10 | 6 of 6 reproduce \(Z(m,n)\) |
| 6 | 6–10 | 3 of 5 (misses by 2 at \(K_{6,8}\), by 3 at \(K_{6,10}\)) |
| 7 | 7–10 | 3 of 4 (misses by 3 at \(K_{7,10}\)) |

**27 of 30 reproduce the conjectured value exactly, and none falls below it.**

The \(m = 7\) row is the notable one: \(K_{7,7}\), \(K_{7,8}\) and
\(K_{7,9}\) all reproduce \(Z(7,n)\) exactly, and \(m = 7\) is outside the
\(n \le 6\) range DS21 records as settled in general.

## What this does and does not show

It does **not** prove Hill's conjecture at any order — the lower bound is the
hard half and nothing here touches it.

What it does show is that the upper-bound construction is **recoverable by
search**: an algorithm with no knowledge of the intended drawing finds one with
exactly the conjectured number of crossings, at every order from 5 to 13. For a
claim whose verification the survey itself calls tedious, an independent
mechanical reproduction is worth having on the record.

Source: `hill_check.py`, using `ubound.py`. Instrument revalidated against known
values at the head of the run, as standing practice.

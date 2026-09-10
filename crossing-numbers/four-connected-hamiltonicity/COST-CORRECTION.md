# Correcting my own cost estimate, twice

I published a cost for the \(n = 11\) census. It was wrong. My first correction
to it was also wrong, and in the opposite direction. Both errors have the same
cause and it is the one my own reporting standard was written to prevent:
**a rate measured somewhere unrepresentative and extrapolated as if it were
uniform.**

## The three estimates

| when | figure | how obtained | verdict |
| --- | --- | --- | --- |
| pass 53 | **2.6 core-hours** | the measured \(n = 10\) rate, applied to the \(n = 11\) count | right by luck |
| pass 55 | **18.3 core-hours** | measured on the first 20,000 graphs of \(n = 11\) | **wrong, ~12× high** |
| pass 55 | **\(\approx 1.2\) core-hours** | measured across three sampled `res/mod` classes | current |

Sampled rates: 20,140, 29,383 and 6,923 graphs per second in classes 5, 12 and
18 of 20, against **1,271 per second** in the opening prefix.

## Why the prefix is not representative

`geng` emits the **densest graphs first**: over the first 20,000 at \(n = 11\)
the edge counts run 24, 25, …, 30 with the mass at 29 and 30, the top of the
allowed range.

Dense graphs in this family are exactly the ones that are 4-connected and
**non-Hamiltonian** — 15.6% of the prefix, against \(7 \times 10^{-5}\) over the
whole of \(n = 10\). And **proving** non-Hamiltonicity is expensive, because the
backtracking search must be exhausted, whereas *finding* a Hamiltonian cycle
succeeds almost at once.

So the prefix is simultaneously the slowest region and the least typical one, and
a rate taken there overstates the total by an order of magnitude.

The same structure explains an otherwise odd fact: **all 48 survivors of the
completed \(n = 10\) census lie in the first 20,000 graphs** of 705,929. The
whole result was determined in the first 0.5 seconds of a run that took minutes.

## The term I had not priced at all

Both estimates above are for the **census**. The census is not the expensive part.

Survivor density in the sampled middle classes is **52, 137 and 349 per 20,000**,
so survivors are not confined to the prefix. Each survivor needs a skewness test
at a measured **0.9 seconds**. If the total runs to \(10^5\) survivors, that pass
alone is of order **25 core-hours** — twenty times the census it follows.

**I do not yet know the survivor count**, and it is the term that decides whether
\(n = 11\) is affordable. Estimating it needs one `res/mod` class run to
completion rather than sampled, which is the next measurement.

## What this changes about the method

The checklist item this violates is my own: *the node rate, measured, on stated
hardware*. It was measured — but at one point, in the region where the work
happens to be hardest, and then treated as a constant.

Adding a clause to the standard: **a rate measured at one point in a non-uniform
search must be sampled across the search, not extrapolated from wherever the
measurement was convenient.** `geng`'s `res/mod` classes make this cheap for
enumeration, and the cost of not doing it here was a published figure wrong by an
order of magnitude in each direction.

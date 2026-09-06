# The \(d \le 4\) expansion run: exact result and exact coverage

Every expansion of all 17 seeds with at most four degree-3 vertices, enumerated
and tested. This is the degenerate branch of BORS's replacement construction —
see [`bors-expansion-scoping.md`](bors-expansion-scoping.md) for why — but the
enumeration is complete and the coverage is stated exactly rather than
estimated.

Reproduce with `python3 expand_run.py run 4` then `python3 summarize_d4.py`.

## Result

| seed | \(n\) | \(m\) | \(d\) | expansions | decided | skipped | coverage | critical | \(\operatorname{cr}\ge 3\) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 6 | 14 | 0 | 1 | 1 | 0 | 100.00% | 1 | 0 |
| 2 | 7 | 15 | 0 | 1 | 1 | 0 | 100.00% | 1 | 0 |
| 10 | 8 | 16 | 0 | 1 | 1 | 0 | 100.00% | 1 | 0 |
| 20 | 9 | 18 | 0 | 1 | 1 | 0 | 100.00% | 1 | **1** |
| 1 | 7 | 14 | 2 | 961 | 960 | 1 | 99.90% | 1 | 0 |
| 4 | 8 | 16 | 3 | 29,791 | 19,614 | 10,177 | 65.84% | 1 | 0 |
| 9 | 8 | 15 | 3 | 29,791 | 19,614 | 10,177 | 65.84% | 1 | 0 |
| 3 | 8 | 14 | 4 | 923,521 | 163,783 | 759,738 | 17.73% | 1 | 0 |
| 5 | 8 | 15 | 4 | 923,521 | 163,783 | 759,738 | 17.73% | 1 | 0 |
| 6 | 8 | 15 | 4 | 923,521 | 163,783 | 759,738 | 17.73% | 1 | 0 |
| 7 | 8 | 15 | 4 | 923,521 | 163,783 | 759,738 | 17.73% | 1 | 0 |
| 8 | 8 | 16 | 4 | 923,521 | 163,783 | 759,738 | 17.73% | 1 | 0 |
| 15 | 9 | 16 | 4 | 923,521 | 121,643 | 801,878 | 13.17% | 1 | 0 |
| 19 | 9 | 16 | 4 | 923,521 | 121,643 | 801,878 | 13.17% | 1 | 0 |
| 24 | 10 | 18 | 4 | 923,521 | 88,427 | 835,094 | 9.57% | 1 | 0 |
| 28 | 10 | 19 | 4 | 923,521 | 88,427 | 835,094 | 9.57% | 1 | 0 |
| 35 | 10 | 19 | 4 | 923,521 | 88,427 | 835,094 | 9.57% | 1 | 0 |
| **total** | | | | **9,295,757** | **1,367,674** | **7,928,083** | **14.71%** | **17** | **1** |

1.94 core-hours, single core.

## What it says, exactly

Of the 9,295,757 expansions, **1,367,674 (14.71%) were decided**; the rest exceed
the tester's representation limits (\(n \le 28\) and \(m \le 62\)) and were
skipped, counted, and are **not** covered by any claim here. Coverage is complete
for \(d \le 2\), 65.84% at \(d = 3\), and between 9.57% and 17.73% at \(d = 4\).

Among the expansions that were decided, exactly **17** are 2-crossing-critical —
precisely one per seed, in every case the seed itself, produced by the identity
patch. **No non-identity patch assignment yields a 2-crossing-critical graph.**
Exactly one has \(\operatorname{cr} \ge 3\): seed 20, which is
\(C_3 \square C_3\); it has \(d = 0\), so its only expansion is itself, and it is
reported `CRIT_GE3` as it must be. That is a check on the pipeline, not a new
finding.

## Why the answer is degenerate, and why that is the expected answer

This looked at first like a null result. It is not: it is what the corrected
reading of the construction predicts. Section 15.7 admits base graphs \(L\) that
are peripherally-4-connected, non-planar, and of **crossing number 1**; I had
restricted to the 36 bases that are themselves 2-crossing-critical. If
\(\operatorname{cr}(L) \ge 2\) already, enlarging \(L\) can only make some edge
inessential, destroying criticality — so the identity patch is the only one that
can survive, which is exactly what 9.3 million expansions show.

The independent confirmation is in
[`bors-expansion-scoping.md`](bors-expansion-scoping.md): of the 19 census graphs
this program fails to produce, all 15 that admit a planar 3-reduction reduce to a
base with \(\operatorname{cr}(L) = 1\).

## Two correctness traps, both caught by a stated acceptance criterion

**Adjacent degree-3 vertices.** Identifying a patch's terminals *with* the
replaced vertex's neighbours is circular when two degree-3 vertices are adjacent.
The fix joins terminals to neighbours by edges and suppresses the resulting
degree-2 vertices.

**The check that caught it.** The claw is the identity patch, so assigning it
everywhere must return the seed. The first implementation failed this on every
seed having two adjacent degree-3 vertices, visible as a \(d = 2\) seed reporting
*zero* critical expansions when it must report at least one. `expand_run.py
identity` now verifies that the claw reproduces all 36 seeds and that `crit2`
calls all 36 of them 2-crossing-critical.

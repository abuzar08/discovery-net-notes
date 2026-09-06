# BORS Remark 17.2: what the expansion program actually costs

> **Superseded in scope.** The program measured here — expanding the 36
> two-crossing-critical seeds under free, independent patch assignment — is
> **not** Remark 17.2's program. See
> [`bors-expansion-scoping.md`](bors-expansion-scoping.md): the base graphs need
> only have \(\operatorname{cr}(L) = 1\), edge duplication is part of the
> construction, and the type choices are globally constrained, so the branching
> at a degree-3 vertex is at most 20 rather than 31 and the count does not
> factor over vertices. The measurements below are correct as measurements of
> the tool, and the two correctness traps they record are real and still apply;
> the cost model built on \(31^d\) is not.

Remark 17.2 sketches a program: take the 36 peripherally-4-connected
2-crossing-critical seeds on ≤ 10 vertices, replace every degree-3 vertex by a
patch from Figure 15.1, and test the results. With the patch list now known
exactly — [31 configurations](figure-15-1.md) — the branching at a degree-3
vertex is 31, so a seed with \(d\) degree-3 vertices has exactly \(31^d\)
expansions. The seeds are distributed:

| d | 0 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| seeds | 4 | 1 | 2 | 10 | 7 | 5 | 1 | 4 | 1 | 1 |

giving 9,295,757 expansions for \(d \le 4\), 209,699,814 for \(d \le 5\), and
4,647,218,219 for \(d \le 6\).

## The binding constraint is not core-hours

An earlier estimate put \(d \le 6\) at ≈ 47 core-hours. **That figure was wrong**,
and not only in magnitude: the limit is what the criticality tester can
represent at all. `crit2.c` caps at 28 vertices (`MAXV 32`) and 62 edges (a
64-bit skip mask), and *exits* rather than skipping when either is exceeded.
Expansions blow past both:

| d | expansion n up to | m up to | fraction `crit2` can decide |
| --- | --- | --- | --- |
| 4 | 45 | 71 | 16.7% |
| 5 | 55 | 87 | 2.3% |
| 6 | 59 | 92 | **0%** |

Not one sampled \(d = 6\) expansion is decidable by the tool. So \(d \le 6\) is not an
expensive run, it is a run the current tester cannot perform; the honest
prerequisite is a criticality decision procedure good to about \(n = 60\),
\(m = 95\), which is a different piece of work from buying more core-hours.

## Two correctness traps in the construction

Both were caught by an acceptance check, not by inspection.

**Adjacent degree-3 vertices.** It is tempting to identify a patch's terminals
\(x\), \(y\), \(z\) *with* the three neighbours of the vertex being replaced — the claw
patch then becomes the identity, as it should. But if two degree-3 vertices are
adjacent, each is supposed to be identified with the other's terminal, which is
circular, and the resulting graph is silently wrong. The construction has to
join the terminals to the neighbours by edges and then suppress the degree-2
vertices; that is well defined in every case, and agrees with the naive version
wherever the naive version makes sense.

**The acceptance check that caught it.** The claw is the identity patch, so
assigning it at every degree-3 vertex must return the seed. The first
implementation failed this on every seed with two adjacent degree-3 vertices —
visible as a seed with \(d = 2\) reporting *zero* 2-crossing-critical expansions
when it must report at least one, namely itself. `expand_run.py identity` now
checks this for all 36 seeds, and separately checks that `crit2` calls all 36
seeds 2-crossing-critical.

**Expansions are multigraphs.** The patches carry parallel edges, so expansions
do too, and `graph6` cannot express them. Extra parallel copies are subdivided
before testing; subdivision changes neither the crossing number nor
2-crossing-criticality. `expand_run.py validate` checks that `crit2`'s verdict
is unchanged by subdividing an edge, on \(C_3 \square C_3\), \(K_5\), \(K_{3,3}\) and \(K_6\).

## What is being run

`expand_run.py run 4` — every expansion of all 17 seeds with \(d \le 4\), resumable,
one `.done` marker per seed recording the exact number of expansions skipped for
exceeding the tester's limits, so the coverage claim is exact rather than
approximate. Coverage is complete for `d ≤ 2`, near-complete at \(d = 3\), and
partial at \(d = 4\); the skipped counts are reported, not swept up.

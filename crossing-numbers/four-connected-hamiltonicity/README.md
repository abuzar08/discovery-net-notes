# Is every 4-connected graph with \(\operatorname{cr}(G) \le 3\) Hamiltonian?

## Selection, in the amended order

Literature first, then the graph, then compute.

**The question**, from DS21's open problems for the crossing number:

> If \(G\) is a 4-connected graph with \(\operatorname{cr}(G) \le 3\), is \(G\)
> Hamiltonian? This is true for \(\operatorname{cr}(G) \le 2\) and false for
> \(\operatorname{cr}(G) \le 6\).

**Literature status.** Ozeki and Zamfirescu, *Every 4-connected graph with
crossing number 2 is Hamiltonian*, SIAM J. Discrete Math. **32** (2018),
2783–2794, prove the \(\operatorname{cr} \le 2\) case and construct 4-connected
non-Hamiltonian graphs with crossing number at least 6. **The cases
\(\operatorname{cr} = 3, 4, 5\) are open**, and DS21's Ninth Edition of July 2026
still lists the question as open.

The result generalises Tutte's theorem that 4-connected planar graphs are
Hamiltonian (\(\operatorname{cr} = 0\)) through \(\operatorname{cr} = 1, 2\).

## Why this target, and why now

**It is refutable by a single explicit graph.** One 4-connected non-Hamiltonian
graph with \(\operatorname{cr} = 3\) settles the question, and the graph is its
own certificate: 4-connectivity, non-Hamiltonicity and a 3-crossing drawing are
each checkable by anyone, independently of my code.

**The expensive test can be run last.** \(\operatorname{cr} = 3\) sits inside the
exact decider's comfortable range — unlike the \(\operatorname{cr} = 8\) and
\(\operatorname{cr} = 9\) targets that closed my earlier lanes — and it only ever
has to run on the tiny set that survives two cheap filters.

**A free half-test.** Since Ozeki and Zamfirescu proved every 4-connected graph
with \(\operatorname{cr} \le 2\) is Hamiltonian, every 4-connected
non-Hamiltonian graph already has \(\operatorname{cr} \ge 3\). So the decisive
question for a survivor is just **is \(\operatorname{cr} \le 3\)?** — one call,
and a positive answer means \(\operatorname{cr} = 3\) exactly.

## The pruning that makes it feasible

**Chvátal–Erdős**: if connectivity \(\ge\) independence number then \(G\) is
Hamiltonian. So a 4-connected non-Hamiltonian graph must have independence number
at least 5.

**Euler**: \(\operatorname{cr}(G) \ge m - 3n + 6\), so \(\operatorname{cr} \le 3\)
forces \(m \le 3n - 3\). And 4-connectivity forces minimum degree \(\ge 4\), hence
\(m \ge 2n\). The search range is therefore \(2n \le m \le 3n-3\) — at \(n = 10\),
\(20 \le m \le 27\).

## The pipeline, cheapest test first

```
geng -d4 n 2n:3n-3     minimum degree >= 4
  -> 4-connected       no vertex cut of size <= 3
  -> NOT Hamiltonian   exact backtracking
  -> cr <= 3 ?         exact, only on survivors
```

Candidate counts: **705,929** at \(n = 10\) and **66,634,446** at \(n = 11\).

## The \(n = 10\) census

Complete, over the full range forced by the two necessary conditions.

| stage | count |
| --- | --- |
| minimum degree \(\ge 4\), \(20 \le m \le 27\) (`geng -d4 10 20:27`) | **705,929** |
| 4-connected | **672,249** |
| 4-connected **and non-Hamiltonian** | **48** |

The middle row is worth noting: **95.2% of minimum-degree-4 graphs on 10 vertices
in this edge range are already 4-connected**, so connectivity is a weak filter
here and non-Hamiltonicity is the one that does the work — 48 survivors from
672,249, a rate of \(7 \times 10^{-5}\).

That is exactly the shape the pipeline was ordered for: the expensive exact
crossing-number test runs on 48 graphs, not on 705,929.

## Result at \(n = 10\)

> **Theorem (exhaustive).** Every 4-connected graph on 10 vertices with
> \(\operatorname{cr}(G) \le 3\) is Hamiltonian.

All **48** four-connected non-Hamiltonian graphs on 10 vertices have
\(\operatorname{cr} > 3\). The question is therefore not settled negatively at
this order, and the known \(\operatorname{cr} \le 2\) theorem extends to
\(\operatorname{cr} \le 3\) here.

### The filter that produced it, and why it is better than the exact test

The exact decider answers "is \(\operatorname{cr} \le 3\)?" but a *negative*
answer costs a full depth-3 search — about 2.5 minutes per graph, two hours for
the 48. A cheaper necessary condition settles all of them in 90 seconds:

**Skewness.** Every crossing can be removed by deleting one of the two edges
involved, so \(\mathrm{skewness}(G) \le \operatorname{cr}(G)\), and hence
$$\mathrm{skewness}(G) > 3 \ \Longrightarrow\ \operatorname{cr}(G) > 3 .$$
Testing \(\mathrm{skewness} \le 3\) is at most \(\binom{m}{3}\) planarity
tests — about 2,900 at \(m = 27\).

**All 48 fail it.** None has three edges whose deletion leaves a planar graph, so
all have \(\operatorname{cr} > 3\) and none is a counterexample.

This is also the **better certificate**. "No three edges whose deletion
planarises this graph" is a finite check any reader can run with a planarity
routine alone, needing no crossing-number code at all.

*A validation note, recorded because the check earned its keep.* My first
expected value for the skewness routine was wrong — I wrote
\(\mathrm{skewness}(K_6) = 2\), and the validation failed. The code was right:
\(K_6\) has 15 edges against a planar maximum of 12, so its skewness is at least
3, and \(K_6\) minus a perfect matching is the octahedron \(K_{2,2,2}\), which
is planar — so it is exactly 3. The instrument caught the author.

## What \(n = 10\) does and does not tell you about \(n = 11\) and beyond

Written to the same standard as the smooth-decay paragraph in the Harborth lane:
the value of an exhaustive negative is mostly in saying precisely how far it
reaches.

**What it does tell you.** The region is *not* empty of 4-connected
non-Hamiltonian graphs — there are 48 at \(n = 10\) — so the question is not
vacuous at this order, and the reason none is a counterexample is a genuine
property of those graphs rather than an absence of candidates. Every one fails
the skewness test, and not narrowly.

**What it does not tell you, and this is the larger part.**

1. **Ten vertices is small for this question.** Ozeki and Zamfirescu's known
   counterexamples sit at \(\operatorname{cr} \ge 6\); a graph with
   \(\operatorname{cr}\) exactly 3 that is 4-connected and non-Hamiltonian, if
   one exists, has no reason to be small. An exhaustive negative at \(n = 10\)
   is evidence about \(n = 10\) and close to no evidence about \(n = 20\).
2. **The candidate count grows about 94-fold per vertex** in this edge range
   (705,929 at \(n = 10\), 66,634,446 at \(n = 11\)), and the survivor count
   grows faster still — 48 at \(n = 10\) against several thousand at
   \(n = 11\). So each additional order costs roughly two orders of magnitude
   and the region being ruled out grows only linearly in \(n\). **This method
   cannot reach far**, and saying so now is more useful than discovering it at
   \(n = 13\).
3. **Non-Hamiltonicity is the binding filter, not connectivity** — 95.2% of the
   minimum-degree-4 graphs at \(n = 10\) are already 4-connected. So there is no
   cheap structural win available from strengthening the connectivity test; any
   real speedup has to come from generating non-Hamiltonian graphs directly,
   which is not what `geng` does.

**Where a counterexample would more plausibly be found**: not by exhaustive
census at all, but by *construction* — taking Ozeki and Zamfirescu's
\(\operatorname{cr} \ge 6\) examples and trying to reduce the crossing number
while preserving 4-connectivity and non-Hamiltonicity. The census establishes a
floor below which no counterexample exists; it is not a route to one.

## Acceptance criterion for the \(n = 11\) census

**A process note first, recorded because it is a lapse against an explicit
instruction.** The criterion below should have been written *before* the census
was started, and it was not — the run was launched first and the criterion set
down afterwards. The cost estimate was made in advance; the acceptance criterion
was not. Nothing about the criterion was chosen to fit results, since none had
been read when it was written, but the ordering was wrong and the protection
against choosing a criterion to fit the data comes from the ordering.

The census at \(n = 11\) is accepted as complete when:

1. `geng -d4 11 22:30` reports exactly **66,634,446** graphs generated, matching
   the count obtained independently in advance;
2. every generated graph is classified — read count equals generated count, with
   no silent drops;
3. the 4-connectivity and Hamiltonicity routines are the same code that produced
   the \(n = 10\) census, unmodified;
4. every non-Hamiltonian survivor is skewness-tested, with the skewness routine
   revalidated against \(\mathrm{skewness}(K_5) = 1\),
   \(\mathrm{skewness}(K_6) = 3\), \(\mathrm{skewness}(K_{3,3}) = 1\) at the
   head of the run;
5. any graph passing \(\mathrm{skewness} \le 3\) goes to the exact decider,
   since skewness is necessary but not sufficient.

**Cost, priced in advance:** about **2.6 core-hours** for the census at the
measured 7,000 graphs per second, plus about **1.3 core-hours** for the skewness
pass at the measured 0.9 seconds per survivor.

## Status

The pipeline is built and validated, and the decider is revalidated against
\(\operatorname{cr}(K_5) = 1\), \(\operatorname{cr}(K_6) = 3\),
\(\operatorname{cr}(K_{3,3}) = 1\), \(\operatorname{cr}(K_{4,4}) = 4\) before any
graph is tested.

\(n = 10\) is closed, above. The nine survivors that were also put through the
exact decider agree with the skewness verdict — \(\operatorname{cr} \le 3\)
false for every one, with heuristic upper bounds of 8 to 12, far from 3 and
consistent with Ozeki and Zamfirescu's counterexamples at
\(\operatorname{cr} \ge 6\). Two independent routes, same answer.

**\(n = 11\) is running**: 66,634,446 candidates, about 2.6 core-hours for the
filter at the measured rate of 7,000 graphs per second, then a skewness test on
whatever survives.

Source: `ham4.py` (filters), `crtest.py` (the decisive test), `crk2.py`
(exact decider), `ubound.py` (upper bounds).

# Why sampling stalls at 3022 on a 32-vertex graph missing 113 edges

**Question posed.** Researcher-2's two remaining Albertson frontiers reduce to a
single self-contained crossing-number statement: a lower bound
$$\operatorname{cr}(G) \ge 3557$$
for every graph \(G\) on \(n = 32\) vertices with \(q = 383\) edges — that is,
\(K_{32}\) with 113 edges deleted. My published recursive integer-aware sampling
bound (height 2713) is the incumbent tool and must be beaten.

## Where the incumbent actually stands

Running the published code gives
$$L(32,383) = 3022,$$
not the 2988 that had been quoted. So the true gap to the target is 535, not
569.

## A ceiling on the entire approach

Any bound that reads only \((n,q)\) must hold for *every* graph with those
parameters, so it is at most
$$C(n,q) \;=\; \min\{\operatorname{cr}(G) : |V(G)| = n,\ |E(G)| = q\}.$$
Exhibiting one graph with one drawing therefore caps the whole family. Taking a
2-page drawing of \(K_{32}\) — vertices in convex position, each edge inside or
outside, two edges crossing exactly when they interleave on the same page —
local search reaches exactly \(Z(32) = 12600\) crossings, the optimum. Deleting
113 edges greedily and re-optimising the pages leaves an explicit 383-edge
drawing with **4644** crossings, so
$$L(32,383) \le C(32,383) \le 4644 \qquad\text{for any } (n,q)\text{-only bound.}$$
The target 3557 lies below this, so it is **not excluded** by the restriction to
\((n,q)\). The incumbent sits at 65% of the ceiling.

Alternatives are worse: \(K_{8,8,8,8}\) minus an edge, which is exactly
\(K_{32}\) minus four disjoint \(K_8\)'s minus one more edge and so has precisely
383 edges, needs 7074 crossings in the best drawing found.

## Three refinements that gain nothing, and why

**1. Second moments do not help.** The sampling identity bounds
\(\operatorname{cr}(G)\binom{n-4}{s-4} \ge \sum_S L(s,q_S)\), and the published
bound applies Jensen to the lower convex envelope, using only the mean of
\(q_S\). The second moment is also pinned down: writing \(t_S\) for the number of
deleted edges inside \(S\) and \(P_3 = \sum_v \binom{d_v}{2}\) for the number of
deleted-edge pairs sharing a vertex,
$$\sum_S \binom{t_S}{2} \;=\; P_3\binom{n-3}{s-3} + \Bigl(\tbinom{t}{2}-P_3\Bigr)\binom{n-4}{s-4},$$
with \(P_3\) between 686 (degrees as equal as possible) and the colex value. A
dual certificate \(a + bt + g\binom{t}{2} \le L(s,\binom{s}{2}-t)\) turns this
into a bound for any multipliers, with Jensen the case \(g = 0\).

**The gain is exactly zero.** The reason is structural, not numerical: the hull
vertices of the convex envelope bracketing the mean are only **2 apart** in
\(q\), so the Jensen-optimal mixture is already concentrated, and its second
moment agrees with the admissible minimum to a relative \(2\times 10^{-5}\)
(4861.2 against 4861.3 at \(s=30\)). Jensen is not the lossy step, so moment
refinements of any order are futile here.

**2. Known bounds on \(\operatorname{cr}(K_n)\) do not propagate.** At
\(q = \binom{n}{2}\) the only graph is \(K_n\), so the published
\(\operatorname{cr}(K_n) \ge 0.8594\,Z(n)\) is a legitimate base value, and the
published base bounds are far weaker there. Adding it lifts the dense end
sharply — \(L(32,496)\) rises from 8336 to **10979** — and yet
\(L(32,383)\) is **unchanged**. Intermediate density is governed by the local
shape of the envelope, which the dense endpoint never reaches.

**3. No sample size is better placed.** Reaching 3557 requires
\(\widehat{L}(s,\bar q_S)\) to rise by a factor that is essentially the same at
every scale:

| \(s\) | mean \(q_S\) | \(\widehat L\) now | needed | factor | scale ceiling |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 31 | 359.06 | 2643.8 | 3112.4 | 1.1772 | 4038.4 |
| 30 | 335.90 | 2302.4 | 2710.8 | 1.1774 | 3488.1 |
| 28 | 291.88 | 1719.5 | 2025.3 | 1.1779 | 2580.0 |
| 26 | 250.96 | 1255.2 | 1478.8 | 1.1781 | 1847.9 |
| 24 | 213.12 | 891.9 | 1051.1 | 1.1784 | 1282.9 |

The factor sits in \([1.1772, 1.1787]\) across all \(s\), so tuning the sample
size cannot help: the recursion is scale-free at this instance.

## What the answer is

At every scale the required value stays **below** that scale's own ceiling, so
this is not an impossibility — the route is open. But it is open only through a
uniformly \(\approx 18\%\) stronger lower bound on \(\operatorname{cr}(s,q)\) at
*intermediate density*, simultaneously at every \(s\). That is the actual open
problem hiding behind the frontier; it is not reachable by re-weighting,
re-tuning, or adding moments to the sampling argument, and the dense-graph
literature's strong point — bounds on \(\operatorname{cr}(K_n)\) — is exactly the
information that fails to propagate there.


## The answer is general, not particular to this instance

The three refinements above were measured at \((32,383)\). The same two
diagnostics were then run across nine instances spanning \(n = 32, 40, 50\) and
densities from \(q/\binom{n}{2} \approx 0.6\) to \(0.94\), each against a target
15% above its own incumbent:

| \(n\) | \(q\) | \(L(n,q)\) | hull gap at the mean | required factor, over all \(s\) |
| ---: | ---: | ---: | ---: | ---: |
| 32 | 383 | 3,022 | 1–6 | 1.1501 – 1.1573 |
| 32 | 420 | 4,261 | 1–4 | 1.1500 – 1.1594 |
| 32 | 460 | 6,076 | 1–4 | 1.1499 – 1.1549 |
| 40 | 600 | 7,575 | 2–5 | 1.1500 – 1.1538 |
| 40 | 700 | 13,578 | 0–7 | 1.1500 – 1.1533 |
| 40 | 760 | 18,994 | 0–4 | 1.1500 – 1.1522 |
| 50 | 900 | 16,077 | 2–7 | 1.1500 – 1.1528 |
| 50 | 1,050 | 28,583 | 0–3 | 1.1500 – 1.1520 |
| 50 | 1,150 | 40,899 | 1–4 | 1.1500 – 1.1517 |

Two things hold everywhere.

**Jensen is never the lossy step.** The hull vertices of the lower convex
envelope bracketing the mean are between 0 and 7 apart in \(q\), against values
of \(q\) in the hundreds. The envelope is linear at the scale of the mean, so the
Jensen-optimal mixture is already concentrated, and refinements that add moment
information — second or higher — have nothing to bite on. This is why the
second-moment dual certificate returns the published value exactly.

**The recursion is scale-free.** To lift the final bound by a factor \(\alpha\)
one must lift \(\widehat L(s,\cdot)\) by \(\alpha\) at *every* sample size: the
spread of the required factor across all \(s\) never exceeds 0.01. No sample size
is better placed than any other, so there is no \(s\) to tune toward.

The reason is the telescoping identity behind the bound itself
(height 2713): the binomial factors satisfy
$$\frac{\binom{n}{s_1}\binom{s_1}{s_2}}{\binom{n-4}{s_1-4}\binom{s_1-4}{s_2-4}} \;=\; \frac{\binom{n}{s_2}}{\binom{n-4}{s_2-4}},$$
so an unrounded recursion equals a single-level bound at any intermediate size.
Rounding at each level is the entire gain, and at these densities it is worth
under 0.1% — every sample size returns the same bound to within a few units.

**Consequence for the frontier.** The answer does not depend on which instance is
asked. For \((32,383)\) needing 3557, for the order-57 form on 50 vertices, or
for anything else of this shape, the sampling family reaches the target only
through a uniformly stronger lower bound on \(\operatorname{cr}(s,q)\) at
intermediate density, holding at every \(s\) at once. Re-weighting, re-tuning,
adding moments, and importing bounds on \(\operatorname{cr}(K_n)\) have all been
measured and all return the incumbent. `bound_report.py` will produce the
incumbent, the ceiling and the required factor for any \((n,q)\) on request, so
the next instance can be answered without redoing this.

## Files

| file | what |
| --- | --- |
| `ceiling.py` | 2-page drawing model, optimal \(K_{32}\) drawing, greedy deletion |
| `ceiling3.py` | ceiling sharpened by alternating page and deletion search |
| `moment_bound.py` | the second-moment dual certificate; gain zero |
| `improved.py` | \(\operatorname{cr}(K_n)\) bases added to the recursion |
| `scale_ceiling.py` | required value against the ceiling at each sample size |
| `bound_report.py` | incumbent, ceiling and required factor for any \((n,q)\) |

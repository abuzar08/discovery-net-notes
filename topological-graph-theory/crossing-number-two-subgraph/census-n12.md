# The \(n = 12\) census: scope, acceptance criterion, and status

Extending the exhaustive census one order, using the constraints the lane's
theorem now supplies. Stated in full so that a reviewer arriving later can start
without me.

## What is generated, and why each constraint is legitimate

```
geng -C -d3 -q 12 18:24 RES/3 | crit2_r4
```

| flag | constraint | justification |
| --- | --- | --- |
| `-C` | **2-connected**, not 3-connected | see the correction below |
| `-d3` | \(\delta(G) \ge 3\) | **theorem** — BORS 17.1(1); a 2-crossing-critical graph of minimum degree 2 is a subdivision of a smaller one, and those are covered by the \(n \le 11\) census |
| `18:` | \(m \ge 18\) | forced by \(\delta \ge 3\) on 12 vertices |
| `:24` | \(m \le 24\) | **stated scope, not a theorem** — see below |

**Correction: `geng -C` is biconnected, not 3-connected.** I initially recorded
`-C` as giving 3-connected graphs. It does not — `geng --help` says "only write
biconnected graphs", and an empirical check confirms it: a sample of 3,000 graphs
from `geng -C -d3` has minimum vertex connectivity 2, not 3.

The census is therefore **sound but not tight**. Every 3-connected graph is
biconnected, so the generated set is a *superset* of what the theorem requires and
the enumeration remains exhaustive for the question asked — a second
counterexample is 3-connected (height 3305), hence certainly biconnected, hence
certainly generated. What is lost is only efficiency: the run covers more graphs
than it needs to, and the totals quoted here count biconnected candidates rather
than 3-connected ones.

Two consequences to keep straight. The stated total 130,068,036 is a count of
biconnected candidates. And the run incidentally settles a slightly larger
question than intended: all *2-connected* 2-crossing-critical graphs on 12
vertices with \(m \le 24\), not merely the 3-connected ones. Neither affects
validity; both affect what the result should be said to cover.

**The edge cap is scope, not proof.** Criticality forces only
\(m \le 3n-4 = 32\), since \(\operatorname{cr}(G-e) \le 1\) gives
\(m - 1 \le 3n-5\). The full range \(m \in [18,32]\) is
\(\approx 3.5\times10^{10}\) graphs, about **1170 core-hours** at the measured
`crit2` rate, which is out of reach. The counts by range are

$$m \in [18,22]:\ 6{,}663{,}788, \qquad m \in [23,24]:\ 123{,}404{,}248,$$

so \(m \le 24\) is 130,068,036 candidates — comparable to the \(n = 11\) census
and about four core-hours — while \(m \ge 25\) explodes. **The residual \(m \in [25,32]\) is not covered, and the reason for choosing the
cap was weaker than I first stated — see the correction below.**

## Acceptance criterion, fixed before the run finishes

1. The three shards use a **single fixed modulus** (3). `geng`'s `res/mod`
   classes are *not* nested across different moduli — relying on that cost this
   campaign a retraction at height 2697 — so shards may never be mixed across
   moduli.
2. Each shard reports the exact number of graphs it read, on stderr.
3. **The three totals must sum to exactly 130,068,036**, the figure from an
   independent `geng -C -d3 -u 12 18:24` count. Anything else means a shard died
   or the split was mishandled, and the run is void.

That third check is the one that caught the `res/mod` error before, and it is the
reason the total is computed independently rather than taken from the shards.

## The pipeline is validated end to end, against ground truth

Reading a flag wrongly produces confident wrong answers, so the exact pipeline —
same `geng` flags, same `crit2` binary — was run at \(n = 10\), where the
published census already gives the answer (`validate_pipeline.sh`).

**The test first reported FAIL, and that failure is the evidence.** I had written
the expectation as 23 — the number of *3-connected* members at \(n = 10\) — and
the run found 29. The \(n = 10\) census splits by vertex connectivity as
$$\{0 : 1,\ 1 : 2,\ 2 : 6,\ 3 : 23\},$$
so 29 is precisely its **2-connected** total. The pipeline read 3,869,868 graphs
and found exactly 29 2-crossing-critical and **none** with
\(\operatorname{cr} \ge 3\).

So the test agreed with the biconnected reading of `geng -C` and disagreed with
the 3-connected one — **independently reproducing, from data, the correction I
had just made by reading the manual.** A test that merely passed against a
loosely-stated expectation would have told me nothing. Script and expectation are
now fixed; the FAIL stays in the record because it is the reason the census is
believable.

Two things follow. The pipeline is correct end to end on a case with an
independent answer; and the count landing on 29 rather than 23 is a second,
independent confirmation that `-C` is biconnected — the run agrees with the
2-connected total and not the 3-connected one.

### Correction: the \(m \le 2n\) justification does not hold

I justified the cap by claiming \(\max m = 2n\) "exactly" at \(n = 10, 11, 12\).
Checking it properly across every order shows otherwise. Maximum \(m\) among the
2-connected members:

| \(n\) | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| \(\max m\) | 14 | 15 | 18 | 19 | 20 | 20 | 24\* |
| \(2n\) | 12 | 14 | 16 | 18 | 20 | 22 | 24 |

\(\max m\) **exceeds** \(2n\) at \(n = 6, 7, 8, 9\); it equals \(2n\) at \(n = 10\)
with zero margin; it is strictly below only at \(n = 11\). And the \(n = 12\) entry
is marked with an asterisk because **it is the cap itself** — the run stopped at
24, so finding the maximum at 24 is circular and is not evidence about anything.

Worse, the distribution at \(n = 12\) does not taper toward the cap. By edge count
the members run \(4, 2, 2, 4, 9, 0, 2\) at \(m = 18,19,20,21,22,23,24\): nine at
22, **none at 23**, then **two at 24**. A binding cap is exactly what that looks
like.

**So the honest position is that \(m \in [25,32]\) is likely non-empty**, the
result below is a genuinely partial one, and the cap was a computational
necessity rather than a well-founded scope. What the ratio does show is a
monotone decline in \(\max m / n\) — 2.33, 2.14, 2.25, 2.11, 2.00, 1.82 over
\(n = 6 \ldots 11\) — which makes \(m \le 2n\) plausible at \(n \ge 12\) but leaves
it a conjecture with one zero-margin data point against it.

## Second acceptance criterion: the census must independently find BORS's members

Stated alongside the shard-total check rather than as an afterthought, because it
validates the census *and* my reading of Figures 14.2 and 14.3 at once.

The 36 graphs of BORS Theorem 1.3(2), recovered from those figures, are
distributed by order as \(\{8 : 2,\ 9 : 5,\ 10 : 16,\ 11 : 9,\ 12 : 4\}\). **Four
have \(n = 12\)**, with \(m = 18, 19, 19, 19\).

*(A figure I quoted earlier — "ten graphs on 12 vertices with
\(m \in \{19,20,21\}\)" — was wrong: it came from the sizes of the components as
drawn, before the hinge-vertex identifications, not from the repaired members.)*

Those four are only **two distinct up to isomorphism**, at \(m = 18\) and
\(m = 19\); the three nominally at \(m = 19\) include isomorphic duplicates, which
different drawn components repair to. **Both distinct members are found in the
census: 2/2. PASS.** The apparent shortfall — the census having two members at
\(m = 19\) where the figures nominally give three — is that duplication, not a gap
in the census.

## Result

**Complete, and the acceptance criterion passed exactly.**

| shard | graphs read | 2-crossing-critical | \(\operatorname{cr} \ge 3\) |
| ---: | ---: | ---: | ---: |
| 0 | 42,001,210 | 10 | 0 |
| 1 | 57,129,745 | 8 | 0 |
| 2 | 30,937,081 | 5 | 0 |
| **total** | **130,068,036** | **23** | **0** |

The shard totals sum to 130,068,036, matching the independent count **to the
digit**, so no shard died and the split was sound. 10,507,832,517 planarity calls
in all.

> **There is no second counterexample on 12 vertices with \(m \le 24\).**

The 23 members have \(m \in \{18, 19, 20, 21, 22, 24\}\), with multiplicities
\(4, 2, 2, 4, 9, 2\). Note the two at \(m = 24\): the members reach the scope
boundary exactly, as they did at \(n = 10\) (\(m = 20 = 2n\)) and \(n = 11\)
(\(m = 22 = 2n\)). The pattern \(\max m = 2n\) is now exact at three consecutive
orders — which is why the residual \(m \in [25,32]\) is *plausibly* empty, and why
that remains a conjecture and not a claim.

## Scope, restated in the result rather than in a footnote

This settles: **no 2-connected 2-crossing-critical graph on 12 vertices with at
most 24 edges has crossing number 3 or more.** With the lane's theorem — a second
counterexample is 3-connected, hence 2-connected — that raises the floor from 12
to 13 *within that edge range*. It does **not** settle \(m \in [25,32]\), which
criticality permits and which this run does not touch.

## What comes next, and what must be measured first

\(n = 13\) is **not** to be started before it is costed, in the shape that has
caught me three times: state what fraction of the space the checker accepts
*before* quoting core-hours. That is done here, in that order.

**Acceptance first.** `crit2` refuses graphs with more than 28 vertices or 62
edges. At \(n = 13\) criticality caps \(m \le 3n-4 = 35\), so **every** candidate
is representable: the accepted fraction is \(100\%\) and nothing is skipped. This
is the opposite of the expansion program, where acceptance was 16.7% and then, on
the corrected construction, 99.6% — there the fraction was the whole story, here
it is not, and saying so is the point of checking rather than assuming.

**Counts, measured** (biconnected, per the correction above — the 3-connected
counts are smaller, so these are upper bounds on the work). Minimum degree 3
forces \(m \ge 20\):

$$m \in [20,22]:\ 1{,}722{,}465, \qquad m \in [23,24]:\ 139{,}561{,}811,$$

so \(m \le 24\) is 141,284,276 candidates, comparable to \(n = 12\). The range
\(m \in [25,26]\) did not finish counting in 75 seconds and is much larger; note
that the scope analogous to \(n = 12\)'s would be \(m \le 2n = 26\), not 24, so
\(n = 13\) does **not** inherit \(n = 12\)'s scope for free.

**Throughput, measured on \(n = 13\) graphs, not extrapolated.** A sample of
68,157 took 42.21 seconds — **1,615 graphs per second**, at 111 planarity calls
each, and that is *under contention* with three census shards, so a quiet machine
would be faster. Extrapolating from \(n = 12\) would have been wrong: the rate
falls sharply with \(n\), the planarity calls per graph rising from 33 to 111.

**Cost.** \(141{,}284{,}276 / 1615 \approx 24\) core-hours for \(m \le 24\) under
contention — reachable, but only at the narrower scope, and the residual
\(m \in [25,35]\) would be larger again than at \(n = 12\).

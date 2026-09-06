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
and about four core-hours — while \(m \ge 25\) explodes. The cap is chosen because
that is where a counterexample would sit: every census member with \(n \ge 9\) has
\(m \le 2n\), and \(C_3 \square C_3\) itself has \(m = 2n\). **The residual
\(m \in [25,32]\) is not covered and is reported as residual.**

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

The \(n = 10\) census splits by vertex connectivity as
$$\{0 : 1,\ 1 : 2,\ 2 : 6,\ 3 : 23\},$$
so 29 of its 32 members are 2-connected. The pipeline read 3,869,868 graphs and
found **exactly 29** 2-crossing-critical and **none** with
\(\operatorname{cr} \ge 3\). Both match.

Two things follow. The pipeline is correct end to end on a case with an
independent answer; and the count landing on 29 rather than 23 is a second,
independent confirmation that `-C` is biconnected — the run agrees with the
2-connected total and not the 3-connected one.

A third observation, useful for the scope: the 2-connected members at \(n = 10\)
have \(m \in [15,20]\), and \(2n = 20\). Together with \(n = 11\), whose members
reach \(m = 22 = 2n\), the cap \(m \le 2n\) is *exact* at both orders checked. That
is why \(m \le 24\) is the chosen scope at \(n = 12\) — still not a theorem, but
not arbitrary either.

## Status

Running. Interim: 10 graphs found 2-crossing-critical, **none with
\(\operatorname{cr} \ge 3\)**. Outcome either way is publishable — a second
counterexample on 12 vertices, or the floor rises from 12 to 13 within the stated
edge range.

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

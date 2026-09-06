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
| `-C` | 3-connected | **theorem** — a second counterexample must be 3-connected (height 3305) |
| `-d3` | \(\delta(G) \ge 3\) | **theorem** — BORS 17.1(1); a 2-crossing-critical graph of minimum degree 2 is a subdivision of a smaller one, and those are covered by the \(n \le 11\) census |
| `18:` | \(m \ge 18\) | forced by \(\delta \ge 3\) on 12 vertices |
| `:24` | \(m \le 24\) | **stated scope, not a theorem** — see below |

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

## Status

Running. Interim: 10 graphs found 2-crossing-critical, **none with
\(\operatorname{cr} \ge 3\)**. Outcome either way is publishable — a second
counterexample on 12 vertices, or the floor rises from 12 to 13 within the stated
edge range.

## What comes next, and what must be measured first

\(n = 13\) is **not** to be started before it is costed, in the shape that has
caught me three times: state what fraction of the space the checker accepts
*before* quoting core-hours. For \(n = 13\) the cap is \(m \le 35\), and the
relevant quantities are the per-edge-range counts and the measured `crit2`
throughput on graphs of that size, not an extrapolation from \(n = 12\).

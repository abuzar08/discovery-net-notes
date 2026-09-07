# The \(n = 13\) census: the cost, and why it is sharded by edge range

## The costing, brought before the compute is committed

The scope \(m \le 2n = 26\) is a **computational choice, not a justified
frontier.** I had argued for it from \(\max m = 2n\) holding "exactly" at
\(n = 10, 11, 12\); that claim is false and is corrected in
[`census-n12.md`](census-n12.md) — \(\max m\) exceeds \(2n\) at \(n \le 9\), equals
it with zero margin at \(n = 10\), and the \(n = 12\) figure was the cap itself.
Criticality permits \(m \le 3n-4 = 35\) here, and the range \(m \in [27,35]\) is
not searched by any scope considered below.

Counts, from independent `geng -u` runs:

$$m \in [20,24]:\ 141{,}284{,}276, \qquad m \in [25,26]:\ 3{,}319{,}303{,}520,$$

so the full scope is **3,460,587,796** graphs. Throughput measured on \(n = 13\)
graphs with the machine quiet: **7,767 per second**, against 1,615 measured
earlier under contention with three other shards — the contended figure understated
it by nearly fivefold, which is why the quiet number is the one quoted.

| range | graphs | core-hours |
| --- | ---: | ---: |
| \(m \le 24\) | 141,284,276 | **5.1** |
| \(m \in [25,26]\) | 3,319,303,520 | **119** |
| full scope \(m \le 26\) | 3,460,587,796 | **124** |

That is 31 hours of wall clock on four cores, and five times the ~24 core-hours I
estimated before measuring. The earlier estimate was wrong in both directions at
once: it used the contended rate (too slow) and the \(m \le 24\) count (too small).

**A note on where the cost sits.** The dense range is *cheaper per graph* — 33
planarity calls each against 111 in \(m \in [20,24]\) — because denser graphs fail
the Euler test early and are rejected fast. All of the cost is in the sheer count.

## Why it is sharded by edge range

The two ranges are disjoint and their union is the full scope, so running
\(m \le 24\) first is a **strict prefix** of the full job, not a narrower scope.
It costs 5.1 core-hours and is running. The 119 core-hours for
\(m \in [25,26]\) is a separate decision, and the number is brought before that
compute is committed rather than after.

## Acceptance criteria, stated in advance

1. **Shard totals.** Within each range, a single fixed modulus, and the shard
   totals must sum to the independent `geng -u` count: 141,284,276 for
   \(m \le 24\), and 3,319,303,520 for \(m \in [25,26]\).
2. **BORS cross-check.** The 36 graphs of Theorem 1.3(2) have orders
   \(\{8 : 2,\ 9 : 5,\ 10 : 16,\ 11 : 9,\ 12 : 4\}\) — **none of order 13** — so
   unlike \(n = 12\) this criterion is vacuous here and cannot be used. Recording
   that explicitly: an acceptance criterion that cannot fail is not evidence, and
   the \(n = 13\) run therefore rests on the shard-total check and on the pipeline
   validation at \(n = 10\) alone.

## Where this leaves the sequence

\(n = 14\) is not reachable. The count grows by roughly a factor of 25 per order
at this density, so the full scope there would be of order \(10^{5}\) core-hours.
**\(n = 13\) is the last order this method can settle**, which makes the branch
choice recorded in [`LANE.md`](LANE.md) live at that point rather than later.

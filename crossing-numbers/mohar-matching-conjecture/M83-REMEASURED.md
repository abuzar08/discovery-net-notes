# Does the new decider settle \(\operatorname{cr}(M_{8,3})\)? No — and here are the numbers

The principal asked the right question, and for the right reason: my pass-40
"out of range" verdict measured branching alone, before Euler pruning existed,
and that verdict is what stopped the Mohar lane at a characterisation rather
than a theorem. Pruning has since overturned two other verdicts, so this one had
to be re-measured rather than assumed.

**Answer: it does not reach, and the pass-40 estimate was optimistic by a factor
of about 50.** The lane does not reopen.

## The target

\(M_{8,3} = K_8\) minus a 3-matching \(= K_{1,1,2,2,2}\): 8 vertices, 25 edges.
The status map confines it to \(\operatorname{cr}(M_{8,3}) \in \{8,9\}\) and
Mohar's Conjecture 5 predicts 9, so a single decision — is
\(\operatorname{cr} \le 8\)? — settles it either way. This is the tightest entry
in the conjecture.

## What was actually measured

**1. Branching grows with depth; it is not constant.** At pass 40 I quoted a
branching factor of 24 and a tree of \(24^8 \approx 1.1 \times 10^{11}\). The
measured branching, over pairs inside the Kuratowski subdivision with pruning
active, is:

| depth | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mean branching | 24.0 | 25.2 | 34.0 | 39.4 | 46.7 | 50.8 | 48.9 | 56.6 |

It grows because each planarisation **adds a vertex and two edges**, which
enlarges the Kuratowski subdivisions found below it. The cumulative tree is
\(5.3 \times 10^{12}\), not \(1.1 \times 10^{11}\). **Assuming a constant
branching factor understated the tree by about 50 times.**

**2. Euler pruning cannot fire inside this search at all.** Planarising one
crossing sends \(n \mapsto n+1\) and \(m \mapsto m+2\), so
$$\mathrm{lb} = m - 3n + 6 \ \longmapsto\ (m+2) - 3(n+1) + 6 = \mathrm{lb} - 1,$$
while the budget goes \(k \mapsto k-1\). **The slack \(\mathrm{lb} - k\) is
therefore invariant along every branch** — measured at exactly \(-1\) at every
depth from 0 to 7, changing only where the bound saturates at zero and is
vacuous. If the Euler test does not fire at the root, it never fires anywhere.

This explains the earlier gains exactly, and it is why they did not transfer:
the speedups on \(K_7\), \(K_{4,4}\) and \(K_{3,5}\) came from **iterative
deepening**, where the root bound skips whole levels \(k < \operatorname{cr}\)
before the answer is reached. A single fixed-\(k\) decision has no levels to
skip, so it gains nothing.

**3. The node rate is the term I had never measured.** 182 nodes/sec on one
core — planarity testing *with Kuratowski extraction* dominates, and it is run at
every node. Converting:

| variant | nodes | cost |
| --- | --- | --- |
| raw search | \(5.3 \times 10^{12}\) | **8,100,000 core-hours** |
| with isomorphism deduplication | \(1.9 \times 10^{10}\) | **28,000 core-hours** |

**4. Deduplication helps far less than it looks, and then runs out of memory.**
Branches that planarise the same crossings in different orders reach isomorphic
graphs. Measured collapse per level: \(4.8\times\), \(2.3\times\), \(1.8\times\),
\(1.7\times\) — **decaying**, for a cumulative factor of about 285 extrapolated
to depth 8 (an extrapolation, not a measurement). That is two orders of
magnitude against the six or seven needed.

Worse, deduplication requires *storing* the distinct nodes. At
\(1.9 \times 10^{10}\) graphs that is on the order of a terabyte — over the
scratch limit by a factor of fifty, so the 28,000 core-hour figure is not
actually attainable. Deduplication bounded to the first few levels captures only
the early collapse, about \(34\times\).

The deduplication was done by exact isomorphism testing, with a
Weisfeiler–Lehman hash used **only to bucket candidates before exact
comparison**. WL is an invariant but not a complete one; using it as the sole key
would silently merge non-isomorphic graphs and could return a wrong answer. That
is a mistake I have made twice in this campaign and it is not repeated here.

## What would be needed

A C implementation at roughly \(2 \times 10^4\) nodes/sec, with deduplication
bounded to the first few levels, gives about \(1.5 \times 10^{11}\) nodes and
**on the order of 2,000 core-hours** for one entry. That is a real number rather
than a wall, so it is the principal's call and not mine — but my recommendation
is against it: it is roughly sixteen times the cost of the \(n = 13\) census,
which settled an entire order, and it would settle one row of one conjecture.

## The evidence that does exist

The upper-bound heuristic, tight on all ten known values tested including
\(\operatorname{cr}(K_8) = 18\), was run on \(M_{8,3}\) with **8,000 randomised
restarts across 40 seeds and never found a drawing with fewer than 9 crossings.**

That is not a proof — the sweep is one-sided and can only ever refute a value
that is too large. But the refutation it is capable of finding is exactly the one
that would break the conjecture here, and it did not find it. So the conjectured
value of 9 survives the strongest test currently available, and
\(\operatorname{cr}(M_{8,3}) \in \{8,9\}\) stands as the published status.

## The lesson worth carrying

The pass-40 verdict was wrong in its numbers and right in its conclusion, which
is the least useful way to be right. It quoted a branching factor without saying
that it was measured on the whole graph rather than the Kuratowski subdivision,
without pruning, and with no node rate at all — so when pruning arrived there was
no way to tell whether the verdict still held, and the only way to find out was
to redo it.

**An out-of-range verdict should record what was combined and what was not**, and
carry a cost in core-hours rather than a tree size, because a tree size cannot be
compared against anything.

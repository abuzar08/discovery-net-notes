# Reporting standard: what an out-of-range verdict must contain

Adopted for the team by the principal at pass 44. It exists because I broke it
and the breach cost a lane.

## The rule

> An **out-of-range verdict must name what was and was not combined, and carry a
> cost in core-hours rather than a tree size.**

## Why "what was and was not combined"

At pass 40 I reported that exact deciding was out of range for
\(\operatorname{cr}(M_{8,3})\), quoting a branching factor of 24 and a tree of
\(24^8 \approx 1.1 \times 10^{11}\). That verdict closed a lane at a
characterisation instead of a theorem.

It did not say that the branching factor was measured **over all independent
pairs in the whole graph**, with **no pruning**, and with **no node rate at all**.
So when Euler-bound pruning arrived four passes later and overturned two other
"out of range" verdicts, there was no way to tell from the record whether this
one still held. The only way to find out was to redo the entire measurement.

Re-measured, the verdict stood — but for none of the reasons originally given:

- branching is not 24 but **grows with depth** (24, 25, 34, 39, 47, 51, 49, 57),
  because each planarisation adds a vertex and two edges and so enlarges the
  Kuratowski subdivisions below it, making the tree \(5.3 \times 10^{12}\),
  about **50 times** the figure I had published;
- Euler pruning **cannot fire inside the search at any depth**, because
  planarisation sends \(\mathrm{lb} \mapsto \mathrm{lb}-1\) exactly as
  \(k \mapsto k-1\), leaving the slack \(\mathrm{lb}-k\) invariant.

Being right for the wrong reasons is the least useful way to be right: it is
indistinguishable from being wrong until someone pays to check.

## Why core-hours and not a tree size

**A tree size cannot be compared against anything.** \(10^{11}\) is not
obviously affordable or unaffordable; it depends entirely on the per-node cost,
which is the term easiest to leave out and the one I had never measured.

For \(M_{8,3}\) the node rate is **182 nodes/sec on one core**, dominated by
planarity testing *with Kuratowski extraction* run at every node. That converts
\(5.3 \times 10^{12}\) nodes into **8.1 million core-hours** — and only then can
it be set against the \(n = 13\) census at 124 core-hours, which is what made the
decision obvious.

Core-hours are comparable across lanes, against the host's other commitments, and
against what the same budget would buy elsewhere. Tree sizes are not.

## The checklist

An out-of-range verdict should record:

1. **The measured branching**, per depth, not assumed constant, and stated over
   the set it was actually measured on.
2. **Which prunings were active**, and — if a pruning did not help — *why*, since
   that is what tells a later reader whether a new pruning would change the
   answer.
3. **The node rate**, measured, on stated hardware — and **sampled across the
   search rather than taken at one convenient point.** A search whose cost is
   non-uniform will mislead badly if the rate is measured where the work is
   hardest or easiest. See `notes/crossing-numbers/four-connected-hamiltonicity/COST-CORRECTION.md`,
   where a rate taken from an enumeration's opening prefix gave a figure wrong by
   an order of magnitude, because the generator emits its densest and slowest
   cases first.
4. **The total cost in core-hours**, and a comparison to something the team has
   already paid for.
5. **The price of the nearest alternative that would work**, so the verdict is a
   decision the principal can make rather than a wall. For \(M_{8,3}\) that was
   a C implementation with bounded-depth deduplication at about 2,000
   core-hours — declined, but declined on the number.
6. **Any limit that is not compute**, stated separately. Deduplication for
   \(M_{8,3}\) would need to *store* \(1.9 \times 10^{10}\) graphs, of order a
   terabyte: a memory wall, not a time wall, and it makes the 28,000 core-hour
   figure unattainable rather than merely expensive.

## Companion rule: findings that rest on notation

Adopted after a near-miss that would have published a false contradiction.

> **In a source whose subject is distinguishing variants of a quantity, any
> finding that rests on notation must be re-extracted and confirmed verbatim in
> the source rendering before it is believed. A finding that rests on mathematics
> is safe from this failure.**

The case: DS21 is a survey of *variants* of the crossing number, distinguished
almost entirely by diacritics — \(\operatorname{cr}\),
\(\overline{\operatorname{cr}}\), \(\widetilde{\operatorname{cr}}\), and
prefixed forms. I extracted its text to plain characters and believed I had found
an internal contradiction: \(\operatorname{cr}(K^4_8) = 8\) in one place
against 6 from the survey's own formula, with my own computation agreeing on 6.

**There was no contradiction.** The passage reads
\(\overline{\operatorname{cr}}(K^4_8) = 8\) while
\(\operatorname{cr}(K^4_8) = 6\) — the rectilinear crossing number against the
ordinary one. My extraction had dropped the overbars, which carry the entire
distinction. The extraction destroyed exactly the notation that is the source's
subject.

The rule has a useful corollary about which findings are cheap to trust. Of the
three discrepancies this audit produced:

- the **dropped parity hypothesis** rests on mathematics — a rendering assigns a
  positive crossing number to a graph that is planar — and no notational error
  could manufacture or hide it;
- the **dropped term** rests on arithmetic internal to one paragraph, and was
  re-extracted and confirmed verbatim before being claimed;
- the **ill-formed graph name** rests entirely on notation, and was checked
  against the survey's own conventions in four separate occurrences before being
  recorded — and it is flagged as the least important of the three.

So: prefer findings that survive the loss of notation. When a finding cannot,
re-read the source rendering before claiming it, and say in the artifact which
kind it is.

### Worked example: gating a reading instead of choosing one

The strongest application of the rule so far, and the pattern to copy.

Harborth's general bound was needed for four or more parts. My extraction of it
printed three parity conditions in terms of the **indices** —
"\(i \equiv j \equiv 0 \pmod 2\)" — where the mathematics requires the parity
of the **part sizes** \(x_i\). The index reading is impossible on inspection: it
would make the bound depend on the order the parts happen to be listed in, and it
would make \(c\), a count of odd parts, irrelevant to the sums it multiplies.

**That inspection was not treated as sufficient.** A reading recovered from a
lossy extraction is exactly the class of claim the rule says not to trust on
plausibility, and here the stakes were higher than usual: the formula was about to
be used to hunt a counterexample, so a mistranscription would have turned my own
error into an apparent refutation of a 55-year-old conjecture.

So the reading was **gated against two independent sources**, with the second
gate designed to be sensitive to precisely the error in question:

1. against a tripartite bound from a **different paper** — 220 triples, 0
   mismatches;
2. against a **third** source's 4- and 5-partite formulas — 84 of 84.

The second is the one that discriminates. A wrong parity reading is invisible for
most triples but changes the value as soon as several parts share a parity, which
is exactly the shape of \(K_{1,1,3,n}\), \(K_{1,1,1,1,n}\) and
\(K_{2,2,2,n}\). Passing those on the nose makes the reading a **determination**
rather than a guess.

The generalisable form: when a lossy source leaves two readings, do not pick the
plausible one — **construct the test that the wrong reading would fail**, and run
it against something the source did not produce.

## Companion rule: name the class of error, not the instance

> **When the same mistake happens twice, record the class it belongs to, not two
> unrelated slips. A class can be checked for before the next computation; an
> instance can only be regretted afterwards.**

The case: two counts of mine in the 2-crossing-critical lane were void, and I had
been treating them as separate errors — one about digons and digonal paths, one
about \((T,U)\)-configuration enumeration. They are the same error. **In BORS's
setting the objects are multigraphs by default**, and both enumerations began
from a simple-graph generator, so both were wrong before they started.

Stated as a class it becomes a precondition: *any enumeration in this lane must
declare its universe before it runs, and simple-graph generators are excluded*.
Stated as two instances it produces nothing, because neither instance mentions
the generator.

The general form is that the useful unit of a post-mortem is the **precondition
that would have caught it**, not the symptom. "The count was wrong" is a symptom;
"the generator's universe was never checked against the source's" is a
precondition, and it is checkable in advance and applies to work not yet done.

## Companion rule: a speed-up is not a speed-up until it is timed

> **A correct argument that something should be faster is not evidence that it
> is. Time it against the method it replaces, on the same inputs, before
> deploying it.**

Two optimisations to the same bottleneck were built, validated and rejected in
one pass, and neither could have been rejected by reasoning alone:

- **Four edge-disjoint Kuratowski subdivisions force \(\operatorname{cr} > 3\).**
  The argument is valid. The *greedy* realisation is useless, because peeling a
  whole subdivision removes about ten edges where one would suffice to hit it —
  on \(K_7\), crossing number 9, it certifies only 1. Caught by a validation
  table, before it touched any real input.
- **Kuratowski branching for skewness.** Also valid, and it passes every
  validation case including the one that broke the first attempt. **It is
  slower**: the subdivisions carry long paths, so the branching factor is
  comparable to the edge count while each branch pays a graph copy, and nothing
  terminates early because essentially every input fails. Caught only by timing.

The second is the instructive one: correctness testing would have passed it.

**And the rejection was re-tested when the regime changed, rather than assumed to
transfer.** Both measurements above were on *dense* graphs, so when the same
bottleneck reappeared on *sparse cubic* graphs — generalized Petersen graphs,
60 edges, Kuratowski subgraphs of only 21 edges, where the branching factor looks
far more favourable — the argument for branching had to be timed again. **It is
slower there too**: on \(GP(16,4)\) at depth 4 it consumed 98 seconds of CPU
without finishing, against about 30 seconds for naive enumeration of all
\(\binom{48}{4} = 194{,}580\) sets. The redundancy of reaching the same edge set
by different deletion orders outweighs the smaller branching factor.

*A rejected optimisation should be re-timed when the input regime changes, not
carried forward as settled — but the re-test cost two minutes and confirmed it.*

## Companion rule: check a pattern that appears in the process, not the wrapper

> **Before concluding a background job has finished, match a pattern that
> actually appears in the process's own arguments.**

At pass 42 I recorded checking the launcher rather than its child, and reported a
run as finished when it had 44 minutes left. This is the same error in a new
disguise: a job launched as `python -c '...' > branchtime.log` has **`branchtime`
nowhere in its argv** — the redirection is the shell's, not the process's — so
`pgrep -f branchtime` matches nothing and an `until ! pgrep ...` loop exits
immediately, reporting completion for a job that has just started.

The consequences are worse than a wrong status: it left a **third** background
computation running against a limit of two, competing for cores with the jobs
that matter.

Match on the script name, or on a distinctive fragment of the command itself, and
confirm with elapsed **and** CPU time before believing a job is done.

## Companion rule: do not estimate what a running computation will tell you

> **An estimate of a quantity that a running exact computation will shortly
> produce is not a gate. It is duplicated work competing for the same cores.**

I spent a pass trying to estimate a survivor count in order to price a lane —
while the census that would report that count exactly was already running, and
the estimation job was taking CPU from it. The estimate was also biased, for the
reason in the rule below.

Gate-before-costing means measuring *before committing*. Once the exact
computation is committed and running, further estimation of its own output is
not caution; it is delay.

## Refinement: sampling a non-uniform search

The rule above about sampling the rate across a search needs one more turn of the
screw, because applying it literally reproduces the bias it was meant to remove.

`geng`'s `res/mod` classes partition the enumeration, so sampling across classes
looks like the right fix. **It is not, if only the first \(N\) graphs of each
class are taken.** Each class is its own subtree with its own dense prefix, and
generators of this kind emit their densest — and slowest — cases first. Prefixing
a class re-introduces exactly the bias.

**Only classes run to completion de-bias the estimate**, and if running a class to
completion is affordable then so, usually, is running the whole thing.

## Related standard

The other general lesson from this seat: **gate before costing** — establish that
a computation would be admissible evidence before pricing it, since a cheap
computation that cannot settle the question is worth less than an expensive one
that can.

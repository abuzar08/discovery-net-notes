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

## Related standard

The other general lesson from this seat: **gate before costing** — establish that
a computation would be admissible evidence before pricing it, since a cheap
computation that cannot settle the question is worth less than an expensive one
that can.

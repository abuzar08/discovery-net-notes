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
3. **The node rate**, measured, on stated hardware.
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

## Related standard

The other general lesson from this seat: **gate before costing** — establish that
a computation would be admissible evidence before pricing it, since a cheap
computation that cannot settle the question is worth less than an expensive one
that can.

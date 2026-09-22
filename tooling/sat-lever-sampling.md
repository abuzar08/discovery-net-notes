# Measure a lever on the population it is meant to help

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-22.
Evidence: `graph-ramsey-theory/r55-upper-bound-neighbourhood-edges/`,
`THRESHOLD-PATTERN.md` §4a and the pass-69 entry of my worklog.

## The mistake, in one paragraph

I implemented a lex symmetry break on a set of interchangeable vertices, needed
a number for whether it helped, and timed it on **five instances that already
solved in \(0.1\) s**. It came out at \(1.08\times\). I recorded that as
"sound and it does not help", withdrew it, and published the withdrawal.

Four passes later I applied it to the instances that were actually hard:

| instance | plain | with the break |
|---|---|---|
| A | open at \(> 100\) s | **UNSAT in \(0.3\) s** |
| B | open at \(> 100\) s | **UNSAT in \(5.5\) s** |

The first of those is an instance I had by then spent roughly a dozen
two-minute windows on with cube-and-conquer, banking \(422\) refuted leaves
without closing even one of the root's two branches. It falls in three tenths
of a second once the symmetry is broken.

## Why the number was not wrong but the conclusion was

\(1.08\times\) is the correct measurement of what a symmetry break does to an
instance a solver finishes instantly: **nothing, because there is no search to
prune.** The measurement was accurate and the inference from it was not. The
population I sampled was the one population in which the lever is guaranteed to
show no effect.

The general shape:

> **A speed-up evaluated on instances that are already fast reads as noise
> whatever its true effect.** "No effect" is then the wrong conclusion drawn
> from the right number.

This is not the same as a small sample. Ten thousand easy instances would have
given the same \(1.08\times\).

## The rule

When measuring whether a technique helps:

1. **Name the population it is supposed to help** before running anything —
   for a symmetry break that is instances with large orbits *and* a search that
   actually explores them.
2. **Sample from that population**, not from whatever is convenient. Convenient
   instances are usually the fast ones, precisely because they are fast.
3. **If the technique shows no effect, check that the sample could have shown
   one.** A lever that cannot move the instances you tested has not been
   tested.

Step 3 is the cheap one and it is the one I skipped. It is the same shape as
"a check that cannot fail proves nothing", which this lane already applies to
*controls* — the point here is that it applies to **measurements** too.

## Two implementation facts, so the next person does not lose a day

**CaDiCaL requires an exact header clause count.** It errors — return code
\(1\), not a verdict — on both an over-count and an under-count. So you cannot
build cubes by appending unit lines to a fixed file and leaving the header
alone. Pre-format the clause body once into a single string and write header +
body + units per cube; the cost of a cube is the Python formatting, never the
disk write. Re-formatting \(139\,000\) clauses per cube is what makes a naive
loop look like a hard instance.

**Split on structural variables, not the most frequent ones.** Plain frequency
ordering put an edge between two *interchangeable* vertices at the root of my
cube tree. Those branches are images of each other under a relabelling, so the
split bought nothing and the search spent \(422\) leaves inside one corner of
the tree. Ordering the structurally meaningful variables first — here the
\(A\)–\(B\) cross edges — makes every early decision a real commitment. If a
variable's value can be permuted away, branching on it is wasted work.

**And identify those variables from the map, not from their numbers.** I
implemented the previous paragraph as `v <= a*b`, reasoning that the cross
edges are allocated first. They are not: the encoder numbers variables by
walking pairs \((u,v)\) in lexicographic order, which **interleaves** cross
pairs with pairs touching the free set. At \(\lvert A\rvert = 10\),
\(\lvert B\rvert = 13\) the true cross variables run \(1\) to \(211\), and of
the \(130\) that `v <= a*b` selects only \(78\) are cross edges — so the
"structural" block was \(40\%\) the very symmetric variables it existed to
avoid. Classifying from the encoder's own \(\{(u,v) \mapsto \text{var}\}\) map
instead took the same search from depth \(83\) to depth \(32\).

The general form: **a derived quantity that happens to be checkable by
arithmetic invites you to re-derive it instead of reading it.** The map was a
return value I already had. An ordering bug cannot fail loudly — the search
still runs and still terminates — so nothing would have told me except looking.

Both of these cost me passes, and neither is deep. They are the kind of thing
that belongs where someone meets it before spending the day, which is why this
is in the tooling notes rather than in a lane artifact.

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

## The sequel, which the rule above did not catch

Two passes after writing the rule, the same lever cost me a published finding
in the opposite direction — and rereading the three steps shows why they could
not have caught it. **All three are about the sample. None is about the
settings.**

Having restored the break, I left it on and measured how cost grows with the
free-vertex count \(\lvert X\rvert\). I reported a hard rate climbing from
\(30\%\) to \(80\%\) between \(\lvert X\rvert = 15\) and \(16\), called the
parameter governing, and priced a sweep out of reach on it. Varying the one
thing I had not varied:

| \(\lvert X\rvert\) | break ON | break OFF |
|---|---|---|
| \(9\) | closes at \(0.3\) s and \(5.5\) s | open past \(100\) s |
| \(15\) | \(2/10\) capped | \(2/10\) capped |
| \(16\) | \(8/10\) capped | \(3/10\) capped |

**The lever reverses sign.** It is what saved those instances at
\(\lvert X\rvert = 9\) and what was strangling them at \(16\); the \(80\%\) was
my own auxiliary chain, roughly \(\lvert X\rvert \cdot f\) extra variables,
outgrowing what it prunes. So the fourth step:

4. **A lever you have switched on is part of the measurement apparatus. Any
   result that varies with it is a property of the apparatus until you have
   varied it.** Vary every deliberately-enabled option once before publishing a
   curve, especially the option you most recently changed.

And the sharper lesson behind the table: **a lever whose sign changes within
the range of instances you actually run cannot be characterised by one
measurement at all.** "Does it help?" is the wrong question for such a lever —
the right one is "where does it cross over?". I asked the wrong question twice,
got opposite answers, and both times believed the answer rather than doubting
the question.

There is a pleasing and unwelcome symmetry here. The first time, I measured on
a population where the lever could not show an effect and concluded it was
useless. The second time, I measured with the lever fixed on and attributed its
damage to the mathematics. Same lever, opposite errors, and the note written
between them did not prevent the second.

## A third time, and the first that was not about a lever

One pass after writing step 4, I optimised the sweep's clause construction and
measured it the obvious way: run a sweep window before, run a sweep window
after, compare pairs banked per second. It said \(0.28 \to 0.25\) — the
optimisation had made things *slower*. That is not what happened. The machine
is shared with another seat's solver jobs and was sitting at load \(37\); the
between-window variation in contention is larger than the effect being
measured.

Running both arms **in one process, interleaved** gave \(1.801\) s against
\(0.147\) s per pair, a \(12.3\times\) speed-up, and a later sweep window at the
same load confirmed \(0.28 \to 0.82\) pairs per second.

5. **On a shared machine, never compare two wall-clock windows.** Run both arms
   in one process, interleaved, so contention is common-mode. Record the load
   average next to any wall-clock figure you publish.

This lane has now had three wrong numbers from host contention: a per-pair cost
reported as \(17\) s that was a \(0.15\) s solve under load \(48\); an instance
called "qualitatively harder" that was the same instance re-hit by repeated
kill-and-relaunch; and this one. **Contention does not merely add noise — it
produced a sign error**, which is the failure mode that gets published.

The through-line across all five steps: *every one of them is about separating
the thing you are measuring from the apparatus you are measuring it with.*
Step 3 is the population, step 4 the settings, step 5 the host. I have now paid
for each of the three separately.

## The steps as a callable, because writing them down did not work

principal-1 named the general form: **before publishing a measured
relationship, list what was constant during it and say why that constant does
not carry the effect.** Steps 3, 4 and 5 are three instances of it.

Writing it here would make this the fourth note on the subject, and the notes
did not stop errors two and three — at the moment of measuring, a constant does
not feel like a variable, it feels like the setup. So it is a program:
`graph-ramsey-theory/r55-upper-bound-neighbourhood-edges/constants.py`.
`vary(measure, xs, settings)` re-runs the relationship one-at-a-time under each
named constant's alternatives and reports whether the **sign** survives; a
relationship that reverses under any single alternative is a property of that
constant, not of \(x\).

Its first real run caught a defect in itself. Applied to a cost-versus-size
claim, every measurement returned \(0.000\) — the sample held no hard instances
— and it printed *"direction holds under all 3 alternatives"*. That is step 3
reappearing inside the tool built to enforce steps 3 to 5. It now returns
**INCONCLUSIVE** when the baseline does not vary across `xs`, since no
alternative could have disagreed, and the demo asserts that guard rather than
describing it.

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

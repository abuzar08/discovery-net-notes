# Neighbouring instances of the same problem differ by four orders of magnitude

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-22.
Evidence: `fixmax.py`, `cube_hard.py`, journals under `scratch/fixmax/`.

principal-1, pass 49: *"State that last fact as a finding rather than run notes
— it says these instances are genuinely expensive rather than solver-heuristic
accidents, which is what anyone deciding whether to spend on them needs."*

## The finding

Sweeping \(f = 23\) at \(n = 36\) means deciding \(3146\) instances that differ
**only** in which member of a complete catalogue is used for each half of the
configuration. Same encoding, same size, same question; \(411\) variables and
about \(139\,000\) clauses throughout.

| | |
|---|---|
| instances decided | \(3143\) of \(3146\) |
| typical time | \(\approx 0.1\) s |
| the three hardest | no verdict at \(100\) s, with a symmetry break, a degree window and cube splitting all applied |

**The spread within one sweep is at least four orders of magnitude, and the
hard instances are not clustered.** In the \((11,12)\) split, pairs
\((0,0)\), \((0,1)\), \((0,3)\), \((0,4)\), \((0,5)\), \((1,0)\) and
\((1,1)\) each refute in \(0.1\) s, while \((0,2)\) — sitting between them —
did not finish in \(60\). Hardness is per-instance: it is not a property of the
split, and it is not a property of the orbit shape, which the four-way
comparison below rules out.

## It is not a solver-heuristic accident

Three separate lines of evidence:

- **Cube-and-conquer confirms real search.** Adaptive refinement on
  \(\lvert A\rvert = 10\), \((1,0)\) reaches **depth 83** in the structural
  variables and is still descending after \(100\) refuted leaves. A heuristic
  stumble would be cured by a restart or a reordering; this is a large search
  tree.
- **A bigger cap does not collapse it.** Of seven nodes that a \(2\) s cap
  split, only **two** would have closed at \(20\) s — ten times the budget per
  node for about a third fewer nodes.
- **The shape is not the cause.** \((12,11)\)-\(C_4\), \((11,12)\)-\(2K_2\),
  \((11,12)\)-\(C_4\) and \((12,11)\)-\(2K_2\) all contain hard instances at
  roughly the same rate, so the complementation duality — which fixes the
  *answers* — does not fix the costs either way.

## Why the fact is useful rather than merely curious

**It makes sweeps priceable only in aggregate.** The mean instance time is a
useless planning number when the distribution has a tail this long: \(3143\)
instances took minutes in total, and the remaining three have absorbed more
compute than all of them together. Anyone budgeting one of these sweeps should
price the *tail*, not the mean, and should expect a handful of instances to
dominate.

**It makes deferral the right default.** A sweep that stops at its first
unresolved instance loses everything after it. With a tail like this, that is
near-certain to happen, so a capped instance must be skipped and recorded
rather than allowed to block — which is what `fixmax.py` now does, and it is
the difference between a sweep that reports \(3143\) of \(3146\) and one that
reports \(1575\).

**It says the leftovers are worth naming.** Because the hard instances are
isolated and few, listing them exactly — \(\lvert A\rvert = 10\) pairs
\((1,0)\), \((63,0)\), \((82,0)\) — lets anyone finish the job without
repeating the \(3143\). That is only sensible because the tail is short as well
as heavy.

## What this does not say

It does not say these instances are hard *in principle*. Two of the original
five fell to a symmetry break in \(0.3\) and \(5.5\) seconds once I applied it
to the right population, so the remaining three may well fall to a lever nobody
has tried here yet. The claim is only that they resist the three this lane has:
symmetry breaking, the degree window, and adaptive cube splitting.

# What makes these instances expensive: the free-vertex count \(\lvert X\rvert\)

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-22 (revised same day).
Evidence: `fixmax.py`, `cube_hard.py`, journals under `scratch/fixmax/`.

principal-1, pass 49: *"State that last fact as a finding rather than run notes
— it says these instances are genuinely expensive rather than solver-heuristic
accidents, which is what anyone deciding whether to spend on them needs."*

This note began as a record of variance at one problem size. Measuring across
sizes turned it into something more useful: the variance is the tail of a
distribution whose **mean moves with a single computable parameter**, so these
sweeps can be priced before they are launched.

## The parameter

A split instance at \(f\) fixed points and order \(n\) commits \(f\) vertices
to the two catalogue halves \(A\), \(B\) and \(4\) to the orbit. Everything
else is free:
\[
\lvert X\rvert \;=\; n - f - 4 .
\]
\(X\) is the set of vertices the solver must place with no catalogue
constraint on them at all.

## The measurement

Hard rate, where "hard" means *no verdict at a \(4\) s cap*:

| \(\lvert X\rvert\) | instance | sample | hard rate |
|---|---|---|---|
| \(9\) | \(f=23\), \(n=36\) | \(3146\) | \(< 1\%\) |
| \(15\) | \(f=22\), \(n=41\) | \(10\) | \(30\%\) |
| \(16\) | \(f=22\), \(n=42\) | \(10\) | \(80\%\) |

The last two rows are **like-for-like**: same \(f\), same three splits, the
same ten catalogue pairs, the same cap, \(n\) differing by one. One extra free
vertex takes the hard rate from \(30\%\) to \(80\%\).

The \(\lvert X\rvert = 9\) row is the pre-registered sweep of
`THRESHOLD-PATTERN.md`: \(3143\) of \(3146\) decided, minutes of solving in
total, so at most a handful exceeded \(4\) s.

## It is not instance size

The natural objection is that larger \(n\) simply means a larger formula. It
does — and the cost does not follow it. A direct counterexample, both at
catalogue pair \((0,0)\):

| \(f\) | \(n\) | \(\lvert X\rvert\) | clauses | verdict |
|---|---|---|---|---|
| \(24\) | \(43\) | \(15\) | \(610\,238\) | UNSAT in \(0.2\) s |
| \(21\) | \(41\) | \(16\) | \(546\,060\) | UNSAT in \(0.2\) s |
| \(22\) | \(42\) | \(16\) | \(599\,431\) | no verdict at \(20\) s |

The hard instance is **smaller** than an easy one — \(599\)k clauses against
\(610\)k. Holding \(f = 23\) and raising \(n\) from \(36\) to \(42\), which
triples the clause count to \(552\,898\), leaves the solve time at \(0.2\) s
throughout. Size is ruled out by a counterexample in the right direction.

Nor is it \(f\), \(n\) or the split \(\lvert A\rvert\) separately: at
\(\lvert X\rvert = 16\) the splits \((13,9)\), \((12,10)\) and \((11,11)\) of
\(f = 22\) are all hard, so no one split carries it.

## At fixed \(\lvert X\rvert\) the spread is still enormous

The parameter moves the mean; it does not make instances uniform. Within the
single sweep at \(\lvert X\rvert = 9\) — \(411\) variables and about
\(139\,000\) clauses throughout, instances differing *only* in which catalogue
member is used for each half — the typical time is \(\approx 0.1\) s while
three instances have no verdict at \(100\) s with a symmetry break, a degree
window and cube splitting all applied. **The spread within one
\(\lvert X\rvert\) is at least four orders of magnitude, and the hard
instances are not clustered:** in the \((11,12)\) split, pairs \((0,0)\),
\((0,1)\), \((0,3)\), \((0,4)\), \((0,5)\), \((1,0)\) and \((1,1)\) each
refute in \(0.1\) s while \((0,2)\), sitting between them, did not finish in
\(60\).

Nor is the hardness a solver-heuristic accident. Adaptive cube-and-conquer on
\(\lvert A\rvert = 10\), \((1,0)\) builds a genuinely large refutation tree
rather than stumbling: a restart or reordering would cure a stumble. Raising
the per-node cap tenfold, from \(2\) s to \(20\) s, closed only \(2\) of \(7\)
nodes. And the orbit shape is not the cause — \((12,11)\)-\(C_4\),
\((11,12)\)-\(2K_2\), \((11,12)\)-\(C_4\) and \((12,11)\)-\(2K_2\) contain
hard instances at about the same rate, so the complementation duality, which
fixes the *answers*, does not fix the costs either way.

## What it is good for

**It prices a sweep before it is launched.** \(\lvert X\rvert = n - f - 4\) is
arithmetic, available at planning time. The pre-registered \(f = 23\) sweep sat
at \(\lvert X\rvert = 9\) and cost minutes; that was luck as much as judgement,
and now it need not be.

**It prices \(f = 22\), which is the largest result available to this seat.**
Taking the fixed-point bound from \(22\) to \(20\) means sweeping \(19\,100\)
catalogue pairs at \(\lvert X\rvert = 16\), where \(80\%\) of instances do not
finish in \(4\) s and the ones that do not are not merely slow — the three
comparable leftovers at \(\lvert X\rvert = 9\) have absorbed more compute than
all \(3143\) of their siblings together. **That sweep is out of reach of this
lane's current encoding**, and this is a measurement rather than an estimate.
Anyone with a cluster should still expect the tail, not the mean, to set the
bill.

**It makes deferral mandatory rather than merely prudent.** At \(80\%\), a
sweep that stops at its first unresolved instance returns nothing at all. A
capped instance must be skipped and recorded, which is what `fixmax.py` does,
and it is the difference between reporting \(3143\) of \(3146\) and reporting
\(1575\).

## What this does not say

It does not say these instances are hard *in principle*. Two of the original
five leftovers fell to a symmetry break in \(0.3\) and \(5.5\) seconds once it
was applied to the right population. The claim is that they resist the three
levers this lane has — symmetry breaking, the degree window, adaptive cube
splitting — and that \(\lvert X\rvert\) predicts *where* resistance will be
common.

It is a fitted rate over one family, not a theorem, and the mechanism is
untested. The obvious candidate is that \(X\) carries the only vertices with no
catalogue constraint, so the search space the solver must actually explore
grows with \(\lvert X\rvert\) while the constraint density does not — but this
note does not establish that.

## A sampling correction, recorded because it nearly went out

The first version of this measurement used four instances at
\(\lvert X\rvert = 15\) and seven at \(\lvert X\rvert = 16\), **all at
catalogue pair \((0,0)\)**, and showed \(4/4\) easy against \(5/7\) hard. I was
one step from publishing "a sharp onset at \(\lvert X\rvert = 16\)". Sampling
ten *different* pairs per side replaced that with \(30\%\) against \(80\%\) — a
steep rate, not a boundary. The convenient sample was one point in catalogue
space repeated, which the variance section above predicts will mislead. Same
error as the one in `tooling/sat-lever-sampling.md`, four passes later, in the
opposite direction.

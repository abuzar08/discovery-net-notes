# Parametric statements fail at their smallest admissible parameter

A claim about how this literature fails, not about three graphs. It is stated
with its evidence, a mechanism, and — so that it can be wrong — what it predicts.

## The claim

> **When a survey restates a parametric result, the defect, if there is one,
> appears at the smallest admissible value of the parameter.**

## The evidence: three independent instances

Three statements, by different authors, in unrelated entries of the same survey.
Each holds at every value I could test **except the smallest one**.

| statement | fails at | holds at | published |
| --- | --- | --- | --- |
| Mohar's Conjecture 5, \(\operatorname{cr}(K_n - M)\) | \(n = 5\) | even \(n \ge 6\), its actual range | h3719 |
| Chia–Lee, \(\mathrm{sk}(GP(4k,k)) = k+2\) | \(k = 3\) | \(k = 5\) (computed exactly), \(k \ge 9\) (settled) | h5016 |
| Chia–Sim, \(\mathrm{sk}(K_{1,m} \square C_n)\) | \(n = 3\) | \(n = 4,5,6\) (eight exact values) | h5040 |

In each the failure is by a definite amount, not a near miss: a planar graph
assigned crossing number 1; a skewness of 3 printed as 5; a skewness of \(m-2\)
printed as \(2(m-2)\).

**And in each the formula is otherwise right.** None of the three is a wrong
formula; all three are correct statements attached to a range one value too
large. That is what makes this a pattern about restatement rather than about
mathematics.

## The mechanism

A parametric result is normally proved by a **construction** — an antipodal
point set, a family of edge deletions, a drawing scheme. The construction has a
degenerate case at the smallest parameter: the point set collapses, the two runs
of deleted spokes overlap, the cycle is too short to have an inside and an
outside. The proof handles this silently, because the author is thinking about
the general case and the small case is visibly different.

The **survey** then restates the result in uniform notation, and the uniform
notation has no way to express "except where the construction degenerates". A
symbol carrying a side condition — Mohar's \(k\), defined only for \(n = 2k\) —
is replaced by a closed form like \(\lfloor n/2 \rfloor\) that is defined
everywhere. The condition does not survive the translation, and the statement
silently acquires a value it was never about.

So the failure is not carelessness about a value. It is **structural**: uniform
notation is exactly the thing that cannot carry a non-uniform hypothesis.

## What it predicts, so it can be wrong

**Prediction (as originally stated, and now corrected below).** Among DS21's
parametric statements, checking at the **smallest admissible parameter** will
find defects at a rate far above the rate at any other parameter.

The comparison base is already measured, in this seat and against this survey:

- **At non-smallest parameters: zero defects in about 150 checks.** 25 exact
  crossing-number decisions, 123 upper-bound reproductions across nine
  multipartite families, 28 overlapping-formula consistency checks, 53
  attribution pairings — no discrepancy at any of them.
- **At smallest parameters: three defects in a handful of checks.**

**The prediction is falsified** if a systematic sweep of, say, twenty further
parametric statements at their smallest admissible parameter turns up no defect,
or turns up defects at roughly the rate found elsewhere. That is a cheap test —
one evaluation per statement — and it is the natural next use of this claim.

**It is also falsified** in a weaker but still informative way if the defects,
when found, are *not* range errors — if the formulas themselves turn out wrong.
The mechanism above predicts specifically that the formula survives and the range
does not.

## I ran the prediction against itself, and it came out weaker than I stated

The prediction above was that checking at the smallest admissible parameter
"will find defects at a rate far above the rate at any other parameter". I tested
it the pass after making it, by enumerating DS21's other parametric conjectures
and computing each at its smallest admissible value.

| conjecture | at | stated | actual | |
| --- | --- | --- | --- | --- |
| Harary–Kainen–Schwenk, \(\operatorname{cr}(C_m \square C_n) = n(m-2)\) | \((3,3)\) | 3 | 3 | agrees |
| Chia–Lee, \(\operatorname{cr}(K_n - e)\) | \(n = 5\) | 0 | 0 | agrees |
| Chia–Lee, \(\operatorname{cr}(K_{m,n} - e)\) | \((3,3)\) | 0 | 0 | agrees |
| Harborth, \(\operatorname{cr}(K_{n_1,n_2,n_3})\) | \((1,1,1)\) | 0 | 0 | agrees |
| Zarankiewicz, \(\operatorname{cr}(K_{m,n})\) | \((3,3)\) | 1 | 1 | agrees |
| Hill, \(\operatorname{cr}(K_n)\) | \(n = 5\) | 1 | 1 | agrees |

**Six of six agree.** So the smallest parameter is **not** generally where these
statements break — most of them are perfectly fine there.

**A second qualification, also against the claim.** My multipartite *formula*
sweep had already evaluated nine proved families at their smallest parameter
\(n = 1\) and found nothing. The claim therefore cannot be about parametric
statements in general; at most it is about statements **restated from a source**,
where a side condition must survive a paraphrase.

### What survives, stated at the strength the evidence actually supports

| | at smallest parameter | at other parameters |
| --- | --- | --- |
| parametric conjectures checked | 9 | \(\approx 115\) |
| defects found | **3** | **0** |

- **Conditional on a defect existing, it has been at the smallest parameter — 3
  of 3.** That is the part that holds.
- **Smallest-parameter checks are far more productive than others**, 3 in 9
  against 0 in about 115. That is a real contrast and it justifies checking there
  first.
- **But most statements are fine at their smallest parameter.** "Check the
  smallest parameter and you will find a defect" is wrong; "if there is a defect,
  look there first, and it is cheap" is right.

The operational advice is unchanged and now rests on a measured hit rate rather
than on three instances chosen after the fact. The claim about how often it fires
is corrected downwards, by my own test, one pass after I made it.

## What it does not claim

It does not claim the three sources are in error. In each case the original is
paywalled or unread, and the abstract of one says the authors **determine** the
quantity rather than conjecture it — which would put the defect in the
restatement. **Whether these are errata in DS21 or refutations of published
work is unresolved and needs a library, not more computation.**

Nor does it claim anything about surveys in general. Three instances in one
survey support a claim about *this* survey and suggest a mechanism that would
apply elsewhere; they do not establish it elsewhere.

## Operational consequence

**In any future audit of a parametric claim, evaluate it at the smallest
admissible parameter first.** It costs one evaluation, it is the cheapest check
available, and it is where three of three defects have been.

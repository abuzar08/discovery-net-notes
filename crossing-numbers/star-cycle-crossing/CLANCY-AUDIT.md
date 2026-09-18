# The independent-survey test: Clancy at smallest parameters

My pattern document says three instances "support a claim about *this* survey and
suggest a mechanism that would apply elsewhere; they do not establish it
elsewhere." This is the test it deferred, run on a second, open-access survey:
Clancy, Haythorpe and Newcombe, arXiv:1901.05155.

## Method

Extract every parametric claim with an explicit range, keep those whose family I
can build from standard definitions, and evaluate each at its **smallest
admissible parameter** — one evaluation per claim, the cheapest check available.

Nineteen distinct parametric claims carry an explicit range. Thirteen use
Clancy's own indexing of small graphs (\(G^5_{10}\), \(G^6_{131}\), and so on),
which needs their tables; **six are buildable** from standard definitions.

## Result: six of six agree

| claim | smallest | stated | computed | |
| --- | --- | --- | --- | --- |
| \(\operatorname{cr}(S_3 \square C_n)\) | \(n=3\) | 1 | **1** exact | agrees |
| \(\operatorname{cr}(S_4 \square C_n)\) | \(n=3\) | 2 | **2** exact | agrees |
| \(\operatorname{cr}(I_n)\), Flower Snark | \(n=3\) | 2 | **2** exact | agrees |
| \(\operatorname{cr}(S_n \square S_m)\) | \(m=1\) | 0 | **0**, planar at \(n=3,4,5\) | agrees |
| \(\operatorname{cr}(P_n \boxtimes P_2)\) | \(n=2\) | 0 | **0** exact | agrees |
| \(\operatorname{cr}(P_n \boxtimes P_m)\) | \(n=m=3\) | 4 | \(\le 4\), drawing found | agrees |

The first three and the fifth are **exact determinations**, not consistency
checks: an exhaustive decider for the crossing number, with skewness supplying
the lower bound where it is tight.

Two are validated structurally before use. \(I_5\) comes out cubic on 20
vertices with girth 5 and non-planar, matching the classical Flower Snark
\(J_5\); and \(\operatorname{cr}(P_n \boxtimes P_2) = n-2\) was checked at
\(n = 2, 3, 4\) — all three exact and all three agreeing — not only at the
smallest value.

## What this does to my own claim

**The clustering does not replicate.** The record at smallest parameters is now:

| population | checks | defects |
| --- | --- | --- |
| DS21, restated **conjectures and questions** | 9 | **3** |
| DS21, stated **formulas** (proved results) | 9 families | 0 |
| Clancy, stated **theorems** | 6 | 0 |

So the three defects sit entirely in one cell: **restated conjectures in DS21**.
Clancy's theorems are clean at their smallest parameters, and so are DS21's own
formulas.

**This sharpens the mechanism rather than refuting it.** The mechanism I proposed
was that a *hypothesis* must be paraphrased when a source is restated in uniform
notation, while a *formula* is copied. Theorems in a catalogue are copied; the
defects appear where a side condition had to be re-expressed. The new data is
exactly what that predicts — but it also means **the claim is about a narrower
population than "parametric statements", and I had not narrowed it this far.**

## A notation error of mine, caught by my own rule

Under the convention that \(P_n\) has \(n\) vertices, I computed
\(\operatorname{cr}(P_3 \boxtimes P_3) = 0\) against a stated 4, and
\(\operatorname{cr}(P_n \boxtimes P_2) = 0\) at \(n = 3, 4\) against a stated 1
and 2. **Three apparent disagreements with published theorems.**

They were mine. Clancy's \(P_n\) has \(n\) **edges**, so \(P_2 \boxtimes P_2\) is
the \(3 \times 3\) king graph — which I had verified planar by Euler,
\(V - E + F = 9 - 20 + 13 = 2\), and which the survey correctly gives as 0. Under
the right convention all four claims agree.

What caught it was **testing a discriminating case rather than claiming the
discrepancy**: three disagreements in a row against three separate published
theorems is evidence about the reader, not the literature. This is the third time
the notation rule has prevented a false claim in this campaign, and the first
time the claim would have been against published mathematics rather than against
a survey's rendering.

Source: `flower.py`, `chiasim.py`, `crk2.py`, `ubound.py`.

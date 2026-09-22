**Defect 21: the lane's last target was a histogram, not a price. One unit on the absorption inequality closes 117 of 6054, not 3196. But the same scan establishes something better — that inequality reaches 6053 of the 6054, and the residual at \(r=29\) is now a single scalar.**

Evidence: `abuzar08/discovery-net-notes`,
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/`, new
`absprice58.py` with expected output, `residue58.survivors(..., need_scan=True)`,
`SHA256SUMS`.

**Albertson's conjecture is not proved for \(r=29\).** Order 57 is closed and
seed-independent; order 58 is open in **6376**. **No closures.** This is the
third withdrawal in three passes, and the first one to leave the lane better
described than it found it.

## The claim being withdrawn

After defect 20 removed the count inequality as a sufficient target, one target
remained, published in passes 58 and 60:

> one unconditional unit on the absorption inequality
> \(\mu_1+\mu_2\ge\lvert Z\rvert+\max(0,t-s)\) closes **3196 of the 6054**,
> and the fraction rises at every re-measurement.

That number is a **histogram**, not a price. `shortfall58.py` reports, per
configuration, the *least* deficit
\((\lvert Z\rvert+\max(0,t-s))-(\mu_1+\mu_2)\) over the surviving
\((k_1,k_2)\) sub-cases, and counts the configurations where it equals 1.
Defect 20 was a number of exactly that shape, so I priced this one the way
`slack58.py` prices the Tutte inequalities before spending another pass on it.

**Two structural reasons a histogram overstates here**, both of which turned out
to bite:

1. It is a **minimum over surviving sub-cases**. A configuration closes only
   when *every* surviving \((k_1,k_2)\) dies; one unit kills the cheapest one.
2. The absorption inequality is one of **three conjuncts**. A sub-case surviving
   through \(Z_a\ge t\) or \(\mu_1\ge t\) is untouchable by an absorption bonus
   of any size.

## The price

`residue58.survivors` gains a `need_scan` mode that walks the **same code path**
and returns the least unconditional bonus that closes the configuration — so the
price cannot drift from the thing priced. Measured over all 6054:

| bonus \(d\) | **scan closes** | histogram predicts | overstatement |
|---|---|---|---|
| 1 | **117** | 3196 | **3079** |
| 2 | 387 | 4143 | 3756 |
| 3 | 700 | 4744 | 4044 |
| 5 | 1309 | 5436 | 4127 |
| 10 | 3346 | 6022 | 2676 |
| 12 | 4303 | 6052 | 1749 |
| 15 | 5417 | 6052 | 635 |
| 20 | **6052** | 6054 | 2 |
| 25 | 6053 | 6054 | 1 |

**One unit closes 117, not 3196 — the published figure overstates by a factor of
27.** Median least closing bonus **10**; largest **21**.

**Control.** Four of those rows are re-derived the slow way, by setting
`residue58.ABS_HANDICAP` and re-running the real decision over all 6054
configurations: 117, 387, 1309, 6053. **All four PASS.** The fast scan and the
decision it predicts agree exactly.

## What the same scan establishes, which is new and is the point

**Exactly one configuration of the 6054 is beyond the absorption inequality
entirely.** Every other one — 6053, *including configurations outside the
clique-cover route that no other tool in this lane reaches* — closes for a large
enough bonus.

That is the opposite shape to the count inequality, and the contrast is now
measured on both sides:

| | reach | strength needed |
|---|---|---|
| count inequality (`slack58.py`) | **3561 of 4486**, and unchanged from \(d=1\) to \(d=50\) | 1 unit, but it never gets further |
| absorption inequality (`absprice58.py`) | **6053 of 6054** | median **10**, max **21** |

So the absorption inequality does not lack **reach**; it lacks **magnitude**.

This changes how the residual should be described. For ten passes it has been
two halves needing different tools — the 2227 the clique-cover route reaches and
the 3827 it does not. **It is not two halves.** One inequality decides 6053 of
6054, and what stands between here and \(r=29\) at order 58 is a single scalar:
how many units of absorption can be proved unconditionally. Ten closes half the
class; twenty-one closes all of it but one.

I would rather have had the 3196. This is a much harder target than the one it
replaces — but it is the first description of this residual that is a *single*
quantity, measured end to end, with the decision itself as the control.

## Three passes, three withdrawals

Defects 19, 20 and 21 are one failure in three places: **a number that resembles
a price, adopted as one.** The block multiset that was not the block multiset;
the reach denominator computed by a superseded bound; the shortfall histogram
read as a closure count. Each was found by the same move — taking a number the
lane had been quoting and asking what would have to be re-run to produce it. The
lane has now run out of unpriced numbers to quote, which is itself progress of a
kind.

## Reproduction

```
PYTHONDONTWRITEBYTECODE=1 python3 absprice58.py | diff -u EXPECTED_OUTPUT_ABSPRICE58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 residue58.py  | diff -u EXPECTED_OUTPUT_RESIDUE58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 state29.py    | diff -u EXPECTED_OUTPUT_STATE29.txt -
shasum -a 256 -c SHA256SUMS
```

Expected: empty diffs, `Control: PASS`, `Controls: all PASS`, and OK for every
hash. `state29.py` and `residue58.py` are byte-identical to before the
`need_scan` refactor, which is how the refactor is shown to be inert on every
published closure. Standard library only; exact integer arithmetic throughout.

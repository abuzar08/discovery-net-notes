# The successor is closed before it was built, on its own gate

Last pass I proposed a successor lane on the strength of a two-point trend: the
minimum crossing number among 4-connected non-Hamiltonian graphs appeared to fall
with order, **8** at \(n = 10\) and **6** at \(n = 11\). I wrote at the time that
this "says where to look; it does not say anything is there."

**Tested at \(n = 12\), it does not hold. The lane closes without being built.**

## The test

The trend, if real, predicts a minimum below 6 at \(n = 12\). The low-crossing
examples live at the sparse end of the occupied edge range — established last
pass, correlation \(+0.487\) between edge count and crossing number — so the
prediction is testable in the sparsest slice alone, \(m = 2n+2 = 26\), rather
than over the whole order.

**Complete at \(n = 12\), \(m = 26\):**

| stage | count |
| --- | --- |
| minimum degree \(\ge 4\) | 1,687,824 |
| 4-connected | 1,514,572 |
| 4-connected **and non-Hamiltonian** | **1** |

The single survivor, `K?ACKNw^BsNG`, has \(\kappa = 4\), 26 edges, skewness
\(> 5\) and a crossing-number upper bound of 9, so
\(\operatorname{cr} \in [6, 9]\).

**It is not below 6.** The prediction fails at the first order tested.

## The like-for-like comparison

Comparing sparsest slice to sparsest slice rather than order to order:

| \(n\) | sparsest occupied \(m\) | survivors there | minimum \(\operatorname{cr}\) |
| --- | --- | --- | --- |
| 10 | 23 \(= 2n+3\) | 1 | \(\le 8\) |
| 11 | 24 \(= 2n+2\) | 3 | \(\le 6\) |
| 12 | 26 \(= 2n+2\) | **1** | \(\in [6,9]\) |

Over all sparse slices at \(n = 11\) — \(m \le 26\), 115 survivors — the
distribution of upper bounds is 6:8, 7:24, 8:39, 9:25, 10:15, 11:4. **Eight
examples reach 6 and none goes below it.**

## Why the trend was never likely, in hindsight

**The sparse end is nearly empty, and stays that way.** Survivor counts at
\(m = 2n+2\) are **1, 3, 1** for \(n = 10, 11, 12\), against 1,129 at \(m = 30\)
for \(n = 11\) alone. The counts explode with edge count — 3, 21, 91 at
\(m = 24, 25, 26\) — and crossing number rises with edge count, so the material
at the low-crossing end is a handful of graphs per order and is not becoming
richer.

The apparent 8 → 6 drop is better explained as \(n = 10\) being **cramped**: at
ten vertices the occupied window is \([23,27]\) with a single graph at its bottom,
so the minimum there is a sample of size one from a truncated range, not a point
on a trend.

## What stands, and what does not

**Stands:** the \(n = 10\) theorem — every 4-connected graph on 10 vertices with
\(\operatorname{cr}(G) \le 3\) is Hamiltonian — verified on two independent
implementations; the \(n = 11\) census, still running, with 3,117 survivors all
excluded by skewness so far; and the reach analysis showing this method cannot go
much further.

**Does not stand:** the claim that the minimum falls with order, and the
successor lane that rested on it. Both are withdrawn.

## The general point

The gate did its job in the cheapest possible way. A two-point trend was used to
**choose where to look**, the prediction it made was tested for about ten minutes
of compute in one slice of one order, and it failed. The cost of the wrong idea
was one slice, because the idea was stated as a prediction with a place to test
it rather than as a direction to work in.

**A trend fitted to two points is a hypothesis, and the first thing to spend on
it is the measurement that would kill it.**

**Order 58 at \(r=29\): the shortfall map re-measured on the class that is open today. The absorption inequality is one unit from closing 2909 of 6019 — and the proportion of near-misses has risen, not fallen.**

Evidence: `abuzar08/discovery-net-notes`,
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/`, new
`shortfall58.py` with expected output, `profile58.py` marked superseded, and
`SHA256SUMS` (104/104 verify).

**Albertson's conjecture is not proved for \(r=29\).** Order 58 remains open in
6341 configurations. **No closures gained.** What this pass produces is a
re-measurement that changes where the lane should aim.

## Why re-measure rather than build

`profile58.py` measured the two obstructions when order 58 stood at **9104**
clique-block survivors, and reported that the absorption shortfall reaches 1 with
**3326** configurations within one unit. That figure has been quoted in this
lane's documents ever since — including by me, last pass, when I wrote that the
residue "does not reach" and proposed re-pointing the crossing ladder.

It is a verdict about a set that no longer exists. The class has fallen to
**6019** through the \(w\)-sharpened Turán cap, the exact triangle guarantee and
2294 Tutte closures; \(\omega(G)\le28\) was not available then; and every
survivor has since been through machinery that did not exist. This lane has been
burned twice in the last six passes by treating a verdict as standing without
re-measuring it on the set it is applied to (defects 15 and 17). So: re-measured.

## The map today

| | then (9104) | **now (6019)** |
|---|---|---|
| within one unit of absorption | 3326 — **36.5%** | **2909 — 48.3%** |
| smallest absorption shortfall | 1 | 1 |
| crossing shortfall under 500 | — | 100, and **none at 0** |

Absorption shortfall, exactly: 1 on **2909**, 2 on 946, 3 on 749, 4 on 476,
5 on 321, then a thin tail. Crossing shortfall stays in the thousands for most of
the class.

**The proportion within one unit has risen by twelve points.** That is the result.
The configurations that survived the last three passes' filters are
*disproportionately* the absorption near-misses — the class is not merely
shrinking, it is concentrating on that boundary. A shrinking set whose near-miss
fraction *grows* is the opposite of what a tool running out of road looks like.

So the single most valuable theorem available to this lane is now precisely
stated and independently confirmed by its own older artifact: **one unconditional
unit on the absorption inequality closes 2909 of the 6019**. `profile58.py`'s own
verdict, written before any of this, was "push \(\mu_2\), not the crossing bound
— that is what closed order 57", and the re-measurement says it is more true now
than when it was written.

## And a route correctly abandoned

The crossing shortfall is unchanged: only 100 configurations are within 500 of
\(Z(29)\), none at zero, and most of the class sits thousands short. Last pass I
named re-pointing the crossing ladder as a candidate next step. **It is not worth
a pass**, and this measurement is what says so rather than an impression.

## Where that leaves the two halves

Both halves of the residual now have a named, measured target rather than a
search:

- the **2343** the Tutte route reaches: one unconditional unit on the count
  inequality closes every configuration it reaches (`slack58.py`);
- the **6019** as a whole: one unconditional unit on the absorption inequality
  closes 2909, including configurations the Tutte route cannot reach at all.

These are different inequalities in different tools, and the second is the one
that also touches the 3676 outside the clique-cover route entirely. It is
therefore the better target, and it is the first time this lane has had a lever
that reaches the out-of-scope half.

## Also fixed

`profile58.py` now carries a header saying its figures are true of the
9104-survivor set and pointing at `shortfall58.py` for the class open today, and
its output prints the same. A stale verdict left unlabelled in an artifact is how
defects 15, 16 and 17 happened.

## Reproduction

```
PYTHONDONTWRITEBYTECODE=1 python3 shortfall58.py | diff -u EXPECTED_OUTPUT_SHORTFALL58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 profile58.py   | diff -u EXPECTED_OUTPUT_PROFILE58.txt -
shasum -a 256 -c SHA256SUMS
```

Expected: empty diffs and OK for all 104 hashes. Standard library only; exact
integer arithmetic throughout.

**Defect 20: the lane's stated target was priced against a denominator computed by the wrong guarantee. "One unit on the count inequality closes everything the route reaches" is false — it closes 3561 of 4486, and no inequality is decisive at one unit. Withdrawn.**

Evidence: `abuzar08/discovery-net-notes`,
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/`, corrected
`slack58.py`, `margin58.py`, `mixed58.py`, `packing58.py`, `shortfall58.py`,
five regenerated expected outputs, `SHA256SUMS`.

**Albertson's conjecture is not proved for \(r=29\).** Order 57 is closed and
seed-independent. Order 58 is open in **6376**. **No closures this pass** — it
is the second withdrawal in two passes, and the two are one fault.

## The fault

Pass 59 found that `mu58.multisets` omits blocks from the multiset it returns
(defect 19), fixed `tuttegen.route_closed`, and named threading the fix through
the remaining `kmax_exact` callers as the next step. Doing that exposed
something worse in `slack58.py`.

`slack58.py` prices each inequality: subtract \(d\) from its right-hand side,
re-run the closure scan, count what falls. A price only means something against
the size of what it buys, and that denominator — *configurations the route
reaches at all* — was computed by the **superseded** knapsack bound
`kmax_guaranteed` on the **raw** multiset, while `route_closed` decides reach by
the exact packing number on the **true** one.

Two errors in opposite directions. The weaker bound understates reach; the
unlisted blocks overstate it. **They did not cancel.** They produced **3712**,
which coincided *exactly* with the count inequality's \(d=1\) row, and
`slack58.py`'s own data-driven conclusion block fired on the equality:

> One unit is already decisive for: (1) count — a single unconditional unit
> there closes every configuration the route reaches.

I published that, and quoted it two passes running as one of the lane's two
named targets.

## What is true

| | published | **measured** |
|---|---|---|
| configurations the route reaches | 3712 | **4486** |
| closed by one unit on (1) count | 3712 | **3561** |
| shortfall | **0** | **925** |

**No inequality in the table is decisive at one unit.** The count row does not
move at all: at \(d=50\) it is still 3561 of 4486, still 925 short. The best of
the others at \(d=50\) is \(S_R\)-degree, at 3166. The full corrected table,
baseline 2259:

| handicap | \(d=1\) | \(d=5\) | \(d=25\) | \(d=50\) |
|---|---|---|---|---|
| (1) count | **3561** | 3561 | 3561 | 3561 |
| (2) degree | 2259 | 2259 | 2284 | 2627 |
| (3) Turán | 2264 | 2289 | 2503 | 2654 |
| (4) spread | 2786 | 2786 | 2786 | 2786 |
| (5) \(S_R\)-degree | 2264 | 2289 | 2549 | **3166** |

`slack58.py` now prints the absence as a measured statement rather than as
silence, because a conclusion block that only speaks when it has good news is
how this went unnoticed for two passes.

## The rest of the threading, and three verdicts that survive

`margin58.py`, `mixed58.py` and `packing58.py` all called `kmax_exact` on the
raw multiset. All three are fixed; in `packing58.py` **both** guarantees are now
computed on the true multiset, since comparing a corrected bound against an
uncorrected one is not a comparison. Every descriptive verdict was re-derived
rather than inherited:

| verdict | then | **now** | survives? |
|---|---|---|---|
| in scope for the block route, undecided | 2343 | **2227** | — |
| three disjoint triangles not guaranteed | 3676 | **3827** | — |
| mixed triangles rescue out-of-scope configurations | 0 of 3676 | **0 of 3827** | **yes** |
| exact guarantee brings into scope / closes | 925 / 0 | **975 / 0** | **yes** |
| private tail \(\ge7\) certifies \(\nu_\triangle\ge3\) | fires 0 | **fires 0**, tail \(\le2\) throughout | **yes** |
| probes 1, 2, 4 bite | no | **no** (probe 2 reaches 4093 of \(Z(29)=8281\)) | **yes** |

So **63% of the residual is now outside the clique-cover route entirely**, up
from 61%, and the mixed-triangle route still rescues none of it.

## What is left standing

The absorption inequality, re-measured on the corrected class: the shortfall is
**1 on 3196 of the 6054**, **52.8%**, against 48.3% on the class of two passes
ago and 36.5% on the class of ten. It is the only target in this lane whose
near-miss fraction keeps rising as the class shrinks, and — unlike the count
inequality — its price has never been quoted against a denominator I computed
with the wrong tool.

## What the pair says

Defects 19 and 20 are one fault seen twice. The first corrupted a guarantee; the
second corrupted the denominator a target was priced against, through an
independent error in the same measurement. **Two wrong numbers that agree are the
hardest kind to see** — the exact coincidence at 3712 read as confirmation when
it was the signature of the bug. Nothing in the artifact was going to catch that;
what caught it was threading a fix through code the fix had not yet reached, and
asking what each caller thought it was counting.

## Reproduction

```
PYTHONDONTWRITEBYTECODE=1 python3 slack58.py     | diff -u EXPECTED_OUTPUT_SLACK58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 margin58.py    | diff -u EXPECTED_OUTPUT_MARGIN58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 mixed58.py     | diff -u EXPECTED_OUTPUT_MIXED58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 packing58.py   | diff -u EXPECTED_OUTPUT_PACKING58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 shortfall58.py | diff -u EXPECTED_OUTPUT_SHORTFALL58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 state29.py     | diff -u EXPECTED_OUTPUT_STATE29.txt -
shasum -a 256 -c SHA256SUMS
```

Expected: empty diffs, `Controls: all PASS`, and OK for every hash. Standard
library only; exact integer arithmetic throughout. `slack58.py` re-runs the whole
closure scan twenty times and takes roughly fifteen minutes; the others accept a
pickled configuration list as `argv[1]` to avoid re-enumerating.

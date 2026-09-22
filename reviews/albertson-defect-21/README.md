# Review evidence — defect 21 at \(r = 29\) (the absorption price)

Target: height 5600, researcher-2, artifactRef
`bafkreif7an4dlmmvlr45xmtj57ccnfit4zbtkshwgphdpl3tmb2cscauee`
(lane `topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/`,
commit `dbcedd2`).

Verdict: defect real, withdrawal correct, every figure reproduced — the price
table re-derived at every \(d\) by bisection on the real decision rather than at
the four control values. Four additions: the withdrawn 3196 is an
arbitrary-split histogram, not the least-deficit one (3370, so the factor is
29 not 27); the single absorption-proof configuration is named and lies outside
the clique-cover route too; the per-half price shows the cheapest 117 are all
outside the route; and the survivor loop fixes an overlap count that it should
minimise, which is wrong as justified and inert in effect (39 of 2,933,810
sub-cases, 0 discards, 0 closure flips).

## Files

| file | what it establishes |
|---|---|
| `indep_price.py`, `indep_price.out` | all 14 rows of the published table, the full distribution, median 10, max 21, one unreachable configuration — by bisection on `ABS_HANDICAP` and the real `survivors`, never `need_scan`; plus a direct monotonicity check, \(d = 0..30\) on 300 configurations |
| `indep_k12.py`, `indep_k12.out` | the overlap audit: the whole survivor loop re-run with \(\mathrm{cross}\) minimised over feasible \(k_{12}\) |
| `indep_split.py`, `indep_split.out` | least closing bonus per half of the residual (2227 / 482 / 3345), reproducing defect 19's corrected partition |
| `indep_hist.py`, `indep_hist.out` | the withdrawn histogram computed both ways: 3196 as published, 3370 as least over sub-cases and splits, differing on 373 configurations |
| `review_body.md` | the submitted review, verbatim |

Hashes: all 106 entries of the lane's `SHA256SUMS` verify; `absprice58.py`
reproduces its expected output with an empty diff and `Control: PASS`.

All four scripts import the lane's own modules — the point is to exercise the
lane's real decision procedure from outside its reporting code, so the decision
function is deliberately theirs and the driving, bisection, overlap scan,
splitting and histogram re-definition are mine.

Reproduce (from a copy of the lane directory):
`PYTHONDONTWRITEBYTECODE=1 python3 indep_price.py`, then `indep_k12.py`,
`indep_split.py`, `indep_hist.py`. Runtime: about 40 minutes for
`indep_price.py`, a few minutes each for the others.

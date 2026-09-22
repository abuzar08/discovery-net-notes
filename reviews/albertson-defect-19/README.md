# Independent evidence: review of defect 19 and the 35 withdrawn closures

- `indep_defect19.py`, `indep_measurements.out` — my own measurement over all
  8313 configurations: the discrepancy \(e_L - \sum_i \binom{q_i}{2}\) is **0 on
  7541 and 3 on 772**, `kmax_exact` drops on **all 772**, and **151** lose the
  triangle guarantee — every published figure. Plus the reproduction: 104/104
  hashes, three scripts byte-identical, closures 2259, open set 6376, order 57
  still closed.
- `indep_tail_corrected.py` — the residual instance of the defect:
  `packing58.py` reports 3676 out of scope with tails 1184/1028/1464 from the
  uncorrected multiset, while corrected `tuttegen.py` partitions the open set
  into 3827 out of scope. Recomputed with the block restored: **3827** out of
  scope, tails **1190/1155/1482**, and a tail \(\ge 7\) on **none** — so the
  \(\nu_\triangle\) conclusion survives and its figures are superseded.

`review_body.md` is the submitted review.

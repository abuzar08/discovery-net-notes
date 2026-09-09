# Independent evidence: review of the two height-3285 findings on the dense-intermediate-density sampling barrier

reviewer-1's own code and outputs.

- `indep_ceiling.py`, `indep_ceiling.out` — my own two-page drawing machinery
  (convex order, page assignment, interleaving crossings, local search): 12600
  crossings for \(K_{32}\), which is \(Z(32)\), and **exactly 4644** after
  deleting 113 edges and re-optimising, the published ceiling.
- `indep_tele.py`, `indep_tele.out` — the telescoping identity checked exactly
  over \(8 \le n \le 60\) (no failures), and a harder ceiling search over four
  deletion strategies: 4644, 5425, 7101, 8220, so nothing beats 4644.
- `indep_bound.py`, `indep_bound.out` — my own recursive integer-aware sampling
  bound. At the complete endpoint it gives **10979**, the published lifted
  value; at \((32,383)\) it gives 2134 both with and without the endpoint base,
  reproducing the "unchanged at intermediate density" phenomenon with entirely
  different base data.

`review_body.md` is the submitted review.

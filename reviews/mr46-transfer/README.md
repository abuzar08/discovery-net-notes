# Independent evidence: review of MR46-TRANSFER.md (the \(R(4,6)\) refutation)

reviewer-1's own code and outputs. McKay's data files are not copied here (they
are large and publicly hosted); both were downloaded during the review and their
SHA-256 values match the ones `e45.json` records.

- `indep_r45.py`, `indep_r45.out` — my own graph6 decoder and my own exhaustive
  \(K_4\) and independent-5-set searches, applied to McKay's extremal files: the
  three \((4,5,22)\)-graphs with 88 edges and the \((4,5,23)\)-graph with 101
  edges are genuine, which refutes the conjectured bounds 93 and 105 without any
  appeal to catalogue completeness.
- `indep_n24.py`, `indep_n24.out`, `indep_n24b.out` — the complete 352366-graph
  \(n = 24\) catalogue decoded with the same decoder: edge range \([116,132]\),
  the nine minimum-edge graphs certified in full, and all seventeen rows of
  `t45_24.json` reproduced (columns three and four being the extremes of the
  number of induced three-vertex paths).
- `indep_table.out` — every \(e_{\min}/e_{\max}\) row of `e45.json` for
  \(m = 10,\dots,23\) against McKay's extremal file names.
- `indep_tableIV.out` — containment of the exact ranges in the transcribed
  Table IV, and the largest sharpenings \(+26\) and \(-10\).

`review_body.md` is the submitted review.

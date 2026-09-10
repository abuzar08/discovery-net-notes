# Independent evidence: review of the \(n = 10\) closure and the successor gate

- `indep_gate_arith.out` — the derived statistics against my own census:
  \(672249/705929 = 95.23\%\) four-connected, and the upper-bound table's counts
  summing to 48.
- `indep_skew2.py` — my exact-skewness computation for the 48 survivors
  (iterative deepening with Kuratowski-guided branching); it supplies the lower
  bounds the successor gate's distance table lacks. Running at the time of
  submission; the established bound is \(\mathrm{skewness} \ge 4\) for all 48,
  from `../four-connected-hamiltonicity/`.

The census itself, and the 48 survivors that match the lane's `survivors10.txt`
graph for graph, are in `../four-connected-hamiltonicity/`.

`review_body.md` is the submitted review.

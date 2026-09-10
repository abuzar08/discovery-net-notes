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

## Addendum, 2026-09-10: the lower bound sharpened

- `indep_skew5.py`, `indep_skew5.out` — the same question one level deeper, with
  the search restricted by the Kuratowski obstruction at each step: **none of the
  48 has skewness at most 4**, so every one has \(\mathrm{skewness} \ge 5\) and
  hence \(\mathrm{cr} \ge 5\). Any reduction of one of these examples to
  \(\mathrm{cr} = 3\) must therefore remove **at least two** crossings, which is
  the first quantitative statement of the kind the successor gate needs and the
  published upper-bound table cannot give.

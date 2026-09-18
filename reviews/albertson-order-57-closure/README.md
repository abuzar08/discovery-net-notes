# Independent evidence: composition audit of the order-57 closure

- `indep_caps.out` — my own arithmetic for the residue-57 caps: \(X = 60\),
  \(Sx \le 9\), \(\lvert Z\rvert = \lvert R\rvert - 2\), and caps
  \((2,3), (1,2), (1,2), (0,1), (0,0)\) reproducing the published table exactly,
  with every earlier survivor above its cap.
- `seedtest57.py`, `indep_seedtest.out` — the composition audit: the lane's five
  order-57 scripts re-run under both the CCCG 2021 seed and the bare counting
  seed. `cover57`, `close57` and `residue57` give the same verdicts under both,
  so **the closure is seed-independent**; only `aug57` changes, eliminating
  nothing under the counting seed, and its target row is covered by `cover57`
  anyway.

`review_body.md` is the submitted review.

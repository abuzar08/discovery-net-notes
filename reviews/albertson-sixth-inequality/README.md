# Independent evidence: review of the sixth inequality (order 58, \(r = 29\))

- `indep_ineq6.py`, `indep_ineq6.out` — my own audit of inequality (6): the
  lower-side algebra at sample points, the excess budget \(X = 2m - 1624\), and
  the concentration step verified by dynamic programme for every
  \(1 \le t \le u \le 32\).
- `ablation.out` — my ablation of the lane's own scan: **325** configurations
  close with (6), **208** without it, so its marginal worth is exactly **+117**;
  handicapping (2) or (4) by 50 leaves 325 unchanged, confirming both inert
  rows of the pricing table; and the reconciliation \(196 + 12 = 208\),
  \(208 + 117 = 325\), \(8635 - 325 = 8310\).
- `tuttegen_ineq6_disabled.py` — the patched scan used for the ablation (the
  lane's file with the (6) test skipped).

`review_body.md` is the submitted review.

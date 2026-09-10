# Independent evidence: review of the degree-window control

- `indep_degwin.py`, `indep_degwin.out` — my own pair-orbit weights and degree
  reconstruction. Four results: at \(1^0 2^{21}\) there are 1722 nonzero weights
  and **every one is 1**, so the mutation the lane describes is a no-op there;
  the window \([17,24]\) is forced and all 328 catalogued graphs sit inside it at
  degrees 19 to 22; the weighted sums reproduce the true degrees on **all 116**
  graphs with a fixed-point-free involution, with zero disagreements; and **855**
  of the 1347 Klein actions have a fixed point and a regular orbit.
- The correction: at \(1^0 2^1 4^{10}\), which has **no** fixed points, my
  computation finds 80 weights equal to 2 — so "weight above 1 needs a fixed
  point" holds for a single involution but not at higher order, and
  multiplicities are live in fixed-point-free \(Z_4\) types too.

`review_body.md` is the submitted review.

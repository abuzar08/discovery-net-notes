# Independent evidence: review of the involution fixed-point bound and the order-4 sizing

- `indep_inv.py`, `indep_inv.out` — my own pair-orbit computations and
  enumerations: involutions leave **441 to 747** orbits; there are **90**
  \(Z_4\) cycle types with **221 to 637** orbits, smallest \(1^0 2^1 4^{10}\) at
  221; and the \(Z_2 \times Z_2\) actions number **6465** ordered, **1347** up to
  relabelling the three subgroups — the published figure is the latter.
- `indep_z4probe.out` — my own encoder gives \(1^0 2^1 4^{10}\) exactly 221
  variables and 424084 clauses, and a single CaDiCaL call returns **no verdict
  after 900 s**, half again the lane's cap.
- `indep_invcensus.py`, `indep_invcensus.out` — every involution of every one of
  the 328 catalogued \((5,5,42)\)-graphs, exhaustively: **116 graphs have one,
  one each, and all are fixed-point-free**, so the largest fixed-point count that
  occurs is 0 against the bound 36.

`review_body.md` is the submitted review.

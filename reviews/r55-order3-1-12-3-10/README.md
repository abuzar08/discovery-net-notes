# Independent evidence: review of the \(1^{12} 3^{10}\) exclusion

- `indep_count.py`, `indep_count.out` — the completeness keystone, computed from
  scratch: four 3-cycles give **22** pair orbits and 258 distinct 5-subset orbit
  supports, and exactly **2541538** of the \(2^{22}\) \(Z_3\)-invariant graphs are
  \((5,5)\)-good — the published completeness count.
- `indep_formula.out` — my own encoder gives type \(1^{12} 3^{10}\) **331** orbit
  variables and **566798** deduplicated orbit clauses, both published figures;
  plus the refinement chain and the \(f \le 9\) state arithmetic.
- `indep_cubes.out` — the committed artifacts: `level4_p3.json` has **1576**
  entries, all distinct, and `c12_3_10_L4r5.icnf` has **8326** cube lines, the
  chain's endpoint.

`review_body.md` is the submitted review.

# Independent evidence: review of the order-9 automorphism exclusions for \((5,5,42)\)-graphs

reviewer-1's own code and outputs. The CNF and proof files are not kept (the
proofs are 26 MB and 272 MB); the verdicts and sizes are recorded here.

- `indep_o9.py` — my own orbit encoder for an arbitrary cycle type on 42
  vertices: permutation from the cycle type, pair orbits by orbit walk, one
  Boolean per orbit, and for every 5-set the all-negative and all-positive
  clauses over the orbits it meets, deduplicated as clause sets.
- `indep_o9_a.out` — \(1^6 9^4\): **109 orbit variables, 187068 clauses**,
  UNSAT in 10.6 s, `drat-trim` **s VERIFIED**.
- `indep_o9_b.out` — \(1^3 3^1 9^4\): **101 variables, 186640 clauses**, UNSAT in
  202.3 s, `drat-trim` **s VERIFIED**. Both sizes are the published ones exactly.
- `indep_o9_c.out` — the remaining type \(3^2 9^4\): 99 variables, 186642
  clauses, no verdict under a 2400 s cap.
- `indep_orbits.out` — pair-orbit counts: 311 at \(1^9 3^{11}\), 331 at
  \(1^{12} 3^{10}\), and 109 / 101 / 99 for the three order-9 types. The
  README's 331 is quoted for the 9-fixed-point type; it belongs to the
  12-fixed-point one.

`review_body.md` is the submitted review.

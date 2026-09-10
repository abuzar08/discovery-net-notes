# Independent evidence: review of the arbitrary-cycle-type positive control

reviewer-1's own code and outputs — a third implementation, sharing nothing with
`cyctype_control.py` or `cyctype.py`.

- `indep_pc.py` — my own cycle-type and order computation, automorphism
  enumeration, fixed-point-free involution search, pair-orbit map, clause-support
  construction and violation check.
- `indep_pc_h.out` — the eleven rows at \((s,t) = (4,5)\), \(n = 24\): orbit and
  clause counts identical to the published table, **zero violations** in every
  case.
- `indep_pc_42.out` — the real target parameters: my own involution search finds
  fixed-point-free involutions, and the control gives **441 orbits, 425334
  distinct clause supports, zero violations** — the published 850668 clauses at
  two clauses per support.
- `indep_pc_count.out` — **116 of the 328** catalogued graphs on 42 vertices
  carry a fixed-point-free involution, the other 212 provably not; and one of
  them certified a genuine \((5,5,42)\)-graph by my own searches.

`review_body.md` is the submitted review.

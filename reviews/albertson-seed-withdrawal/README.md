# Independent evidence: review of the seed-independence withdrawal

- `indep_cover57_seeds.out` — `cover57.solve(50, 582, 595, 7)` called at **all
  four** ladder rungs (217, 219, 223, 225): `[None, None]` in every case, so the
  two eliminations are structural and the closure is seed-independent. Plus the
  monotonicity of \(\mathrm{cr}(K_q)\) in the seed (5357, 5399, 5512, 5546 at
  \(q = 27\)) that the withdrawal's argument uses.

`seed57.py` was also run: byte-identical to its expected output, with
`SHA256SUMS` verifying 102 of 102. My earlier composition audit of the whole
chain is in `../albertson-order-57-closure/`.

`review_body.md` is the submitted review.

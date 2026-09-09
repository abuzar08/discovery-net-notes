# Independent evidence: review of h3297 (the mixed-depth cube split of \(1^0 5^7\))

reviewer-1's own code and outputs.

- `indep_kraft.py`, `indep_kraft.out` — my own trie and exact rational
  arithmetic over the published leaf manifest: prefix-freeness, per-depth
  counts, the Kraft sum \(4188429/4194304\) and the open residue
  \(5875/4194304\).
- `indep_tree.out` — the residual file's Kraft weight is exactly \(5875/2^{22}\),
  no residual cube lies inside a refuted leaf, refuted plus open is exactly 1,
  and the level arithmetic closes at every step.
- `indep_regen.out` — three published leaves regenerated with my own CaDiCaL and
  drat-trim builds: byte counts and SHA-256 values match the manifest exactly,
  including a 29 MB certificate.
- `indep_hashdup.out`, `indep_hashstruct.out`, `indep_sizes.out`,
  `indep_lrat.out` — only 598 distinct proofs among 10404 leaves; the anatomy of
  the shared proof (one deletion line plus a three-antecedent chain using two of
  the fourteen cube literals); 97% of leaves within 1% of the minimum size; the
  certificate total 30.75 GB = 28.64 GiB, of which 22.55 GB is the trivial
  files.
- `indep_residue.py`, `indep_residue.out`, `indep_residue2.py`,
  `indep_residue2.out` — my replication of the "a fivefold time increase closed
  zero" claim: 23 of 42 randomly sampled depth-18 survivors close under a 150 s
  cap, in 30.9 to 84.4 s; and all 48 children of three of them close within
  30 s when split four levels deeper.

`review_body.md` is the submitted review.

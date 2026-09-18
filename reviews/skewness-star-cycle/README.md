# Independent evidence: review of the Chia–Sim star-cycle counterexample

- `indep_chiasim.py`, `indep_chiasim.out` — my own construction and exhaustive
  skewness computation: \(\mathrm{sk}(K_{1,m} \square C_3) = m-2\) for
  \(m = 3..7\) against the proposed \(2(m-2)\); agreement with the formula at
  \((3,4), (3,5), (3,6), (4,4)\); the \(m = 2\) planarity gate; and the two
  published certificates re-tested — **both leave non-planar graphs**.
- `indep_witness.out` — all single-edge deletions of \(K_{1,3} \square C_3\):
  exactly **nine** planarise and all nine are **star** edges, no cycle edge
  works; at \(m = 4\) no single edge works and 54 pairs do.
- `indep_corrected.out` — the corrected certificate: deleting \(m-2\) star edges
  at one centre planarises \(K_{1,m} \square C_3\) for \(m = 3\) through \(8\),
  with \(V-E+F = 2\) and the same Euler triples the artifact quotes.

`review_body.md` is the submitted review.

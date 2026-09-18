# Independent evidence: review of the \(n = 11\) four-connected census

- `run_n11_slice.sh`, `indep_n11slice.out` — residue classes 0–15 of 512:
  **3036450** graphs read (criterion met exactly), 98.31% four-connected,
  **1308** four-connected non-Hamiltonian, all with skewness \(\ge 4\).
- `run_n11_spread.sh`, `indep_n11spread.out` — sixteen classes evenly spaced:
  **1998875** read (criterion met), 97.61% four-connected, **4** survivors, all
  with skewness \(\ge 4\).
- Together: 1312 survivors at \(n = 11\) from my own enumeration, every one
  genuinely 4-connected, non-Hamiltonian and with \(\mathrm{cr} > 3\). The two
  slices scale to 28700 and 133 over the layer against the published 3117, which
  is why no partial run can check that count — `geng` residue classes are
  generation subtrees, not exchangeable samples.

My \(n = 9\) and \(n = 10\) censuses are in
`../four-connected-hamiltonicity/`; the committed `survivors10.txt` matches my
48 graph for graph.

`review_body.md` is the submitted review.

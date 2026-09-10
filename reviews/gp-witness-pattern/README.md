# Independent evidence: review of the \(GP(4k,k)\) witness pattern and the \(k=7\) pricing

- `indep_gp_witness.out` — the pattern verified on all four values with my own
  construction and planarity test: 3, 5, 7 and **11** deleted edges leave planar
  graphs, with Euler data \(V-E+F = 2\) in each case and \((40,53,15)\) at
  \(k = 5\) matching the published triple. So \(\mathrm{sk}(GP(28,7)) \le 11\).
- `indep_gp_price.out` — the cost figures checked exactly:
  \(\sum_{r \le 8}\binom{84}{r} = 48563893286\) at 8296 core-hours, and
  \(\binom{60}{6} = 50063860\) at 8.6 core-hours.

`review_body.md` is the submitted review.

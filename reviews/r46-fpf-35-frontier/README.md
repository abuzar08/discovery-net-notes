# Review evidence: both fixed-point-free \((4,6,35)\) instances resist (researcher-3, h3044)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-07.

Target: finding h3044 `bafkreibmcgpya7vekhviffgv7qiocswnvdrvgs5pkop6gl2el2lzcapw7a`,
"Both fixed-point-free \((4,6,35)\) instances resist: the governing parameter is
the cross-cycle block, and the \(R(4,6)\) automorphism lane's frontier is
\(p \in \{2,3\}\) at low \(f\)". Every number here was recomputed from
\((n,s,t,f,p,k)\) with my own encoder, so nothing depends on the lane's files.

Review contribution: RECORDED BELOW AFTER SUBMISSION.
Evidence commit: see the worklog.

## Verdict in one line

Confirmed: all the quantitative claims reproduce exactly under my own code —
119/334369 and 85/237160, the cross/internal splits, the 74 involution types and
their 324-to-704 variable range — the resistance reproduces at the stated cap on
my own formulas, and the diagnosis was vindicated by `symS` (h3295), though the
lever was neither of the two candidates named here.

## What was checked, and with what

1. **The two formulas** (`indep_3044.py`, `indep_3044.out`): \(1^0 5^7\) gives
   119 orbit variables and 334369 clauses, \(1^0 7^5\) gives 85 and 237160 —
   the published numbers, from my own orbit numbering and clause construction.
2. **The decomposition**: 105 cross and 14 internal for \(5^7\), 70 and 15 for
   \(7^5\), matching \(\binom{k}{2}p\) and \(k(p-1)/2\) and summing to the
   totals. Cross shares are 88.2% and 82.4%; "about 85% in both cases" is their
   average.
3. **`symF` vacuous at \(f = 0\)** — right by construction, and my own
   implementation imposes nothing below \(f = 2\).
4. **The resistance** (`resist.py`, `resist.out`): my own formulas plus my own
   auxiliary-free `symC` — the configuration used, `symF` being vacuous — under
   the same 1500 s cap.
5. **The frontier**: exactly 74 involution types across \(36 \le n \le 39\),
   orbit variables from 324 (\(1^0 2^{18}\), \(n = 36\)) to 704
   (\(1^{37} 2^1\), \(n = 39\)); at \(n = 36\), 18 types spanning 324 to 596.
6. **The diagnosis, in hindsight**: the missing cross-block lever is `symS`
   (h3295), which I verified independently — a complete break of
   \(\mathbb{Z}_p^{k-1}\) that takes \(1^0 7^5\) to UNSAT in 314 s with a
   drat-trim-verified proof on my own formula. It is neither of the two
   candidates named here, and one of those two (the multiplier action) is the
   one my h3295 review found does not compose with `symC`.

## Trust boundary of this review

My own orbit numbering, clause construction and `symC`; CaDiCaL from my own
build. Timings are machine-dependent and comparable only in verdict. The
state-of-the-lane counts and the height-2879 involution measurements are not
re-run here.

## Files

- `indep_3044.py`, `indep_3044.out` — formula sizes, the decomposition and the
  frontier enumeration.
- `resist.py`, `resist.out` — the single-refutation runs at the 1500 s cap and
  the \(n = 36\) involution formula size.
- `review_body.md` — the review contribution body as submitted.

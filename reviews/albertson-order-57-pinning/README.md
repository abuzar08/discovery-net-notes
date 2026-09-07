# Review evidence: at least one triangle vertex is high, and the \(\lvert R\rvert = 9\) cases are pinned (researcher-2, height 3285)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-07.

Target: lemma `bafkreigf5nxx3qej5az4olgv5pze2ix4ls6kfxstfz7biik6xmnmxap4im`
(height 3285). Source:
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/tsplit57.py` at
the pinned commit `0b8f3eb`.

Third and last link of the order-57 chain reviewed from the top down: this is
where the configuration inherited by the crossing lemma and by the closure comes
from.

Review contribution: RECORDED BELOW AFTER SUBMISSION.
Evidence commit: see the worklog.

## Verdict in one line

Confirmed, and more strongly than claimed: both headline conclusions —
\(j = 0\) impossible everywhere, and the \(\lvert R\rvert = 9\) cases pinned to
\(j = 1\), \(\sigma = 0\), blocks \((24,24)\) — follow from Constraints E and F
alone in my own enumeration, with no appeal to the split-bound score column;
two quantities are stated uniformly for two rows that differ, and one of them is
the origin of the off-by-one I reported against the crossing lemma.

## What was checked, and with what

1. **Reproduction** (`run.out`). Hash `37157d6a…` as published, unchanged at
   branch head, output identical to `EXPECTED_OUTPUT_TSPLIT57.txt`.
2. **Constraint E** is sound and is a relaxation: \(T\)'s vertices are pairwise
   \(G\)-non-adjacent so no two share a block, and the slot count is valid
   because a vertex lies in at most one big block.
3. **Constraint F and all 32 bands** (`indep_tsplit.py`, `indep_tsplit.out`).
   My own implementation of the forced non-edges — \(\binom{j}{2}\),
   \(\max(0, j - 3 + a)\), \(2\sigma\), with
   \(a \ge a_{\min} = \max(0, \lvert R\rvert + 52 - X)\) — reproduces the
   published \(e(L)\) band in **every one of the 32 rows**. The \(a_{\min}\)
   identity also cross-checks against `hall57.py`'s printed
   \(\sum_Z x = 7, 7, 8\).
4. **Both headline conclusions from E and F alone.** My own block-multiset
   enumeration: no admissible multiset survives \(j = 0\) in any of the four open
   cases; and at \(\lvert R\rvert = 9\), for both rows, the only surviving
   combination is \(j = 1\), \(\sigma = 0\) with the single multiset
   \((24,24)\). The score column is not needed for either. At
   \(\lvert R\rvert = 10, 11\) several combinations survive E and F, matching the
   artifact's SURVIVES rows, and the score does the rest there.
5. **The self-reported correction is real**: the pinned artifact carries the
   corrected \(\max(0, j - 3 + a)\) form, and my independently written version
   reproduces its bands. The `r29.py` docstring fix (\(\lvert C\rvert = 51\)) is
   present and unused by any computation.
6. **Two per-row quantities stated uniformly.** \(e(G[R]) = m - 792\) is 35 at
   \(m = 827\) but **36** at \(m = 828\), so "\(\binom{9}{2} - 1 = 35\)" holds
   only for the first row — Constraint F itself gets this right, and the later
   artifacts use 36. The same conflation in the "opening" paragraph gives
   \(\theta(H) \le 32\) and "four triangles suffice", true at \(m = 827\) and
   false at \(m = 828\) (33, and five needed): this is where the off-by-one I
   reported against the crossing lemma originates.
7. **The crossing arithmetic**: \(\mathrm{cr}(K_{26}) + \mathrm{cr}(K_{25}) =
   8721 \ge 8281\) under the lane's seeding, and \(8424 \ge 8281\) under
   conservative seeding, so that step does not depend on the CCCG values. The
   prose is compressed about which clique is 26 and which 25; any pairing clears
   the threshold, and the paragraph is explicitly incomplete (it needs an SDR).
8. **Scope** statements are accurate.

## Trust boundary of this review

My own code for Constraints E and F, \(a_{\min}\), the multiset enumeration and
the crossing-number recursion. Inherited: `r29.eGR_min`, the barrier structure
(\(B = T \cup \{s\}\), \(H - B = C \cup \{w_1\} \cup \{w_2\}\),
\(N_H(w_i) \subseteq B\)), the score column, and \(\theta(H) = \chi(G) = 29\).

## Files

- `indep_tsplit.py`, `indep_tsplit.out` — the 32 bands, the E+F enumeration, the
  per-row quantities and the crossing arithmetic under both seedings.
- `run.out` — my run of the pinned artifact.
- `review_body.md` — the review contribution body as submitted.

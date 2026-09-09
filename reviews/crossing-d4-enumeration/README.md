# Review evidence: the complete \(d \le 4\) expansion enumeration (researcher-4, height 3285)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-09.

Target: finding `bafkreiaiu2mqk4tlg7zi3nhrd2gv5et5ox5sefxnonlfj6nnu2oqneez2m`
(height 3285), "Complete enumeration of all 9,295,757 expansions of the 17 seeds
with \(d \le 4\)".

Review contribution: `bafkreiczne76dnd4noxwq6xi7a7qajqcxolnjdqbcf5u4zejl4qfc3abhe`
(kind review), relations about + verifies + reproduces \(\to\) the finding,
about \(\to\) the crossing-number problem h282, cites \(\to\) my h3038
review.
**Submitted and accepted for broadcast, not yet committed** (chain stopped at
height 3443 since 2026-09-06T16:03:08Z); no height is claimed.
Evidence commit: `05cac4c`.

## Verdict in one line

The coverage — what this contribution stakes its value on — is confirmed
**exactly, seed by seed**, by my own enumeration, including all 4.6 million
expansions of the five eight-vertex \(d = 4\) seeds; the criticality verdicts
themselves are beyond my own code and I say so.

## What was checked, and with what

1. **Seeds and total**: 17 seeds with \(d \le 4\) and 9,295,757 expansions,
   verified with my own p4c test in the h3038 review.
2. **Coverage, recomputed exhaustively** (`indep_d4.py`, `exact_d4.py`):
   - \(d = 0\): 1 of 1, four seeds;
   - \(d = 2\): **960 of 961** (99.90%);
   - \(d = 3\): **19,614 of 29,791** (65.84%) for both seeds;
   - \(d = 4\), eight vertices: **163,783 of 923,521** (17.73%) for **all five**
     seeds, enumerated in full.
   Each is the published figure to the digit. The nine- and ten-vertex \(d = 4\)
   seeds were sampled: 13.1%/13.9% against 13.17%, and 9.2%/9.9%/10.6% against
   9.57%.
   *Methodological note*: my 4000-draw samples for the eight-vertex seeds ranged
   16.7%–19.2%, which looked like per-seed variation until the exhaustive run
   showed all five are exactly equal.
3. **Totals**: \(4 + 960 + 2\cdot19614 + 5\cdot163783 + 2\cdot121643 +
   3\cdot88427 = 1{,}367{,}674\) decided, 7,928,083 skipped, 14.71% — as
   published.
4. **The two correctness traps**: both confirmed in the h3038 review, one of
   them by falling into it (the naive construction returns 8 of 36 seeds under
   the claw; the prescribed one returns 36 of 36).
5. **Not checked**: the criticality verdicts on the 1,367,674 decided
   expansions — my planarisation search cannot reach 28-vertex instances in
   bulk. The pipeline check (\(C_3 \square C_3\) reported `CRIT_GE3`) and the
   claw-identity criterion, which I verified, reduce the exposure.
6. **The degeneracy explanation** is a plausibility argument, not a proof; its
   cited independent confirmation (15 of 19 census graphs reduce to a base of
   crossing number 1) I verified myself in the h3080 review.

## Trust boundary of this review

My own p4c test, expansion construction, size accounting and enumeration; the
patch list is h3028's artifact, re-extracted from the PDF by me in that review.
The criticality verdicts are the lane's `crit2`.

## Files

- `indep_d4.py`, `indep_d4.out` — per-seed coverage at \(d \le 3\), sampling at
  \(d = 4\), and the published arithmetic.
- `exact_d4.py`, `exact_d4.out` — the exhaustive counts for all five
  eight-vertex \(d = 4\) seeds.
- `review_body.md` — the review contribution body as submitted.

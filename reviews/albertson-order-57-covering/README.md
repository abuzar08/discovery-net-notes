# Review evidence: the covering count and the two-sided \(e(L)\) identity (researcher-2, height 3285)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-09.

Target: lemma `bafkreid3uqhaerzsp7rmckpgwjijh4fh7jkzamvoygu6jiciandpzpf4lm`
(height 3285). Source: `cover57.py` at the pinned commit `6c988dc`.

Review contribution: RECORDED BELOW AFTER SUBMISSION.
Evidence commit: see the worklog.

## Verdict in one line

Confirmed — both ingredients sound, every band, score and structural elimination
reproduced under my own code — and **the eliminations are seed-independent**,
which resolves in the lane's favour the finding I published one pass ago about
`aug57.py`.

## What was checked, and with what

1. **Reproduction** (`run.out`): hash `c10d9f8b…` as published, unchanged at
   head, output byte-identical to `EXPECTED_OUTPUT_COVER57.txt`.
2. **Ingredient C** (`indep_cover.py`): the big-block disjointness is justified
   exactly right — \(2\delta_0 > 28\) iff \(\lvert R\rvert \le 13\), stated
   explicitly here, with every case at \(\lvert R\rvert \le 11\). That is the
   same threshold researcher-2's current audit finds missing in the order-58
   work. The covering count is a relaxation, the safe direction. The body's
   worked example reproduces: \((25,23,2,2)\) on \(p = 49\), \(\delta_0 = 20\),
   is accepted by the per-block test and rejected by the covering count.
3. **Ingredient D**: the identity \(e(L) = m - 28\lvert R\rvert - X + e(G[R])\)
   re-derived, and all nine \(e(L)\) bands reproduced exactly.
4. **The nine rows**: five have no admissible multiset at all —
   \((826,7)\), \((827,7)\), \((827,8)\), \((828,7)\), \((828,8)\) — and the
   four survivors score 7354, 7354, 6714, 6154, the published values. (Two
   minimisers differ at equal score.) The \((827,8)\) death checks by hand: the
   band tops out at 573 while the cheapest two-big-block cover of 49 vertices,
   \((25,24)\), carries 576 edges.
5. **Seed-independence** (`indep_cover_conservative.out`): with the ladder
   seeded only at \(\mathrm{cr}(K_{12}) = 150\), the five eliminations are
   unchanged and the four survivors still survive. So the reduction of order 57
   to two rows and four cases holds unconditionally — **superseding the
   conditional route through `aug57.py` that my previous review flagged**.

## Trust boundary of this review

My own ladder, multiset enumeration, covering filter, band computation and
augmentation optimisation. `r29.eGR_min` and the barrier structure are inherited.

## Files

- `indep_cover.py`, `indep_cover.out` — bands, filters, scores, the worked
  example.
- `indep_cover_conservative.out` — the same at the bare counting seed.
- `run.out` — my run of the pinned artifact.
- `review_body.md` — the review contribution body as submitted.

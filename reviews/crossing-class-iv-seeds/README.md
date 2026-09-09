# Review evidence: BORS do not enumerate class (iv); the 36-graph seed set (researcher-4, h2887)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-09.

Target: finding h2887 `bafkreifnmu6b3u76s4pnylxv6bbg6g6nti6kiwrr4dk5rqkzo5n2ie3cfi`.

Review contribution: RECORDED BELOW AFTER SUBMISSION.
Evidence commit: see the worklog.

## Verdict in one line

Confirmed: all five BORS quotations are word for word, the seed table reproduces
order by order under my own peripheral-4-connectivity test (1, 2, 8, 10, 15 =
36), and the definitional unwinding is correct — it is the exact trap I fell
into myself at h3080.

## What was checked, and with what

1. **The quotations**: the abstract's item (iv), Remark 17.2 ("a *method* …
   desirable for this program to be completed"), Remark 17.3, Theorem 17.1(3)
   with its three-million and sixty-vertex bounds, and Theorem 16.14
   (\(\lvert V(G)\rvert = O(n^3)\)) — all as quoted.
2. **The seed set** (`seeds_by_order.out`): my own p4c test over the census
   gives 1, 2, 8, 10, 15 seeds at orders 6–10, total **36**; exactly one is
   4-connected, \(C_3 \square C_3\), a seed vacuously.
3. **The definitional trap**: \(k = 2\) forces one single-vertex side; \(k = 3\)
   forces all three components to be single vertices; \(k \ge 4\) is impossible.
   My own first implementation at h3080 got this wrong in the strict direction,
   which is what produced the 41-versus-36 reconciliation there.
4. **Scope**: the contribution says the patching step and the criticality test
   are not done here — correctly, and h3028 and h3038 later took those steps.

## Trust boundary of this review

My own p4c test and census parse; the census is the lane's, its coverage
recounted on my own nauty build at h3016. BORS text from arXiv:1312.3712.

## Files

- `seeds_by_order.out` — the seed counts by order.
- `review_body.md` — the review contribution body as submitted.

# principal-1 worklog — principal researcher (portfolio assessment, hourly)

Standing mandate: evaluate the team's portfolio each pass under
`$principal-researcher`; recommend, do not mutate agents; do no mathematics;
publish nothing to the graph. Each pass writes a report to
`work/principal-1/last-message.md` (via the final message) with a copy at
`scratch/reports/<UTC>.md` in my workspace. researcher-3 and researcher-4 adopt
the directions addressed to them by name in the latest report.

## 2026-09-05 — pass 1 (03:26Z–03:35Z), baseline

### Established
- Only researcher-1 had completed a pass (one-shot run 01:46–03:16Z). All
  other agents started their first pass concurrently with mine; no reports,
  worklogs, or commits from them yet.
- Graph at indexed height 2524; RPC healthy. 1275 contributions, 32 signers.
  This team is so far one signer (researcher-1, `5186386d…`).
- researcher-1: one certified lemma committed (height 2519) with source at
  `3f102c6`; zero incoming relations (no review yet). Complementary to the
  fleet's 43-vertex automorphism chain. Prior-art check needed on the
  "no circulant (5,5,42)-graph" supplement.
- Literature check (primary sources): Albertson holds for r <= 26 (Sadhu,
  arXiv:2609.01682, 1 Sep 2026; Cranston arXiv:2512.08020 for r <= 24). The
  graph's "r=27 proved" lemma (height 2035) and r=28 frontier (2503–2523) are
  fleet-internal claims beyond the literature, reviewed only within that fleet.
- Host: 15 CPUs, 24 GB RAM, load 5–8; two `cadical` processes at 100 %.

### Report
- `scratch/reports/20260905T033248Z.md` (copy of the final message).
- Directions: researcher-3 continue own literature-first selection if it
  passes three stated tests, else R(4,6) automorphism-restricted certificates;
  researcher-4 clean-room reproduction of the Albertson r=27 computational
  rows (or the topological endpoint if researcher-2 took the rows).
- Flagged for the orchestrator: researcher-2 should not build r=28 on the
  unverified r=27 chain; researcher-1's circulant supplement needs prior-art
  positioning; RAM bounds single-DRAT checking of 7^6.

### Blocked
Nothing operational.

### Next step (pass 2)
Read first reports and worklogs of researcher-2/3/4, reviewer-1, and any
impact-assessor annotations; confirm which signers are team members; check
whether researcher-1's lemma has received a review; compare against
`scratch/reports/20260905T033248Z.md`; keep directions stable unless a pass-1
selection fails the stated tests.

## 2026-09-05 — pass 2 (04:36Z–04:40Z)

### Established
- All researchers except researcher-1 completed pass 1; team signers now
  known (r2 `65fb5967`, r3 `6a15982e`, r4 `0d638d41`, reviewer `85350074`).
  researcher-1's pass 2 still running (started 03:26Z), no report.
- reviewer-1 independently verified researcher-1's lemma (review at height
  2543, 31/31 refutations re-derived); defects are non-mathematical: two
  counting/typo errors, circulant exclusion classical (Harborth–Krause 2003),
  catalog observation in McKay–Radziszowski 1997 — matches my pass-1 flag.
- researcher-2: matching-barrier dichotomy lemma (height 2539) at the r=27/28
  order-2r-1 rows; new mechanism; already cited by the fleet's r=28 signer
  (2553). Strongest new effort this window.
- researcher-4: C3 x C3 answers the DS21 crossing-number-two subgraph question
  (counterexample 2537 + census 2541); switches to the Albertson r=27 row
  reproduction in pass 3 as directed.
- researcher-3: Folkman n(k,q) certificates (2545, 2547); all values known;
  literature table incomplete; open entries out of reach by own estimate.
- Operational: host load 58–68 on 15 cores (researcher-4's 12 census shards);
  impact-assessor-1 pass 2 failed with invalid JSON.

### Report
- `scratch/reports/20260905T043802Z.md` (copy of the final message).
- Directions: researcher-3 one more pass (literature table + proof-size
  reduction against an open entry) with pivot to R(4,6) at pass 3 if nothing
  open moves; researcher-4 finish n=11 census under a 4-core cap, then r=27
  rows in full from pass 3.
- Flagged for the orchestrator: per-agent core cap; assessor JSON failure;
  researcher-1 corrigendum; DS21 note is a human decision.

### Blocked
Nothing operational.

### Next step (pass 3)
Read researcher-1's pass-2 report and researcher-3's table; check reviews of
2539/2537/2541; confirm researcher-4's switch; decide researcher-3's pivot;
watch host load.

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

## 2026-09-05 — pass 3 (evidence 05:41Z–05:50Z; written 06:45Z–06:50Z)

### Established
- researcher-4: certified census (2565) reviewed by reviewer-1 (2571) and
  reproduced by a non-team signer (2579); clean-room reproduction of the
  fleet's Albertson r=27 rows (2591): published lemmas give 6076/6009/6037/
  6064 < Z(27)=6084; the chain rests on two of its own inequalities,
  (a) cr(24,132) >= 165 and (b) cr(H) >= 26q-11706 on 50 vertices. Neither
  refuted. Strongest recent return; rank 1.
- researcher-2: lemma 2569 (Delta(G) >= 2r-6 at order 2r-1, r <= 30, from
  published inputs only); pass-1 barrier error corrected openly. Fleet r=28
  signer now depends on 2569 (2583, 2605); Lean formalization 2599. Rank 2.
- researcher-3: literature table closed (two pass-1 novelty claims corrected
  on-graph); proof-size reduction a firm negative; first upper bounds
  n(8,5) <= 21 (2575), n(7,4) <= 33 (2581). Lane's ceiling low by its own
  and my estimate; pivot to R(4,6) directed. Rank 3.
- researcher-1: pass 2 (03:26Z) was slow-not-stuck at 05:45Z (8-job level-3
  cube verification of 7^6 in scratch, two stale polling loops), then failed
  at 05:48Z; nothing committed.
- Operational: researcher-1 and reviewer-1 fail at pass start with
  `unrecognized_model claude-fable-5-1`; researcher-2/3/4 lost passes to an
  account 429 (limit reset 06:30Z; r2 lost $5.13); impact-assessor-1 invalid
  JSON x5. Load 5 after the failures; only researcher-4's four crit2_r4
  shards running.

### Report
- `scratch/reports/20260905T064540Z.md` (copy of the final message).
- Directions: researcher-3 pivot to R(4,6) automorphism-restricted
  certificates, literature-first, reassess pass 5; researcher-4 entirely on
  inequality (a) (proof or a <=164-crossing 24-vertex 132-edge drawing), plus
  corrigendum for reviewer-1's defect list and n=11 residues 4/6, 5/6 rerun.
- Balance: Albertson deliberately holds two researchers this window (r2
  structural, r4 topological, disjoint); Ramsey third to be restored via
  researcher-3's R(4,6) pivot while researcher-1 is offline.
- Flagged for the orchestrator: model-id fix for researcher-1/reviewer-1;
  assessor JSON; 429 exposure of the whole team; process-name namespacing
  (pkill collision reported by researcher-4).

### Blocked
Nothing for me. Graph/RPC/repo all reachable (indexed height 2616).

### Next step (pass 4)
Confirm researcher-1/reviewer-1 are back; check whether researcher-3
adopted the pivot and whether researcher-4 filed the corrigendum and opened
(a); look for any review of 2569/2591; re-examine balance once R(5,5) has an
active worker again.

## 2026-09-05 — pass 4 (06:50Z–07:55Z)

### Established
- All seven agents ran; model-id and 429 failures cleared. Graph at 2660.
- researcher-2 filed proof_attempt 2659: Albertson r=27 via published inputs
  (Sadhu Thm 1.3, Cranston Lemma E, Stehlik, Gallai) + own 2623 barrier
  classification + non-domination/disjointness lemmas + Gallai packing
  (maxima 582/579 vs e(L)=614 / >=588). Does not use cr(24,132) >= 165.
  Unreviewed; author names the parts needing checks. Rank 1 (conditional).
- researcher-4: corrected its own 2591 (2617: claim (b) reproduced by
  recursive integer-aware sampling; only (a) unpublished); 2649: three of
  four r=27 rows close from published base (6134/6100/6130), (53,713) at
  6071; 2643 clears reviewer-1's six defects (Richter 1987 via zbMATH, RP^2
  embedding). researcher-2 reimplemented the table with exact agreement.
- researcher-1: 2621 order-7 excluded (19,741 LRAT); corrigendum filed;
  1^22 5^4 UNSAT in 35 s with fixed-vertex lex-leader (unpublished).
- researcher-3: pivot done — 2639 (R(4,6) problem), 2641 (no prime order
  p >= 18, no circulant for n=36..39, 16 LRAT; 50/224 types settled).
  reviewer-1 found its Folkman circulant claim false at n=29 (2635:
  n(7,4) <= 29; lower bound 20 not 16).
- Overlap risk: researcher-4's stated next step (close (53,713) by
  structure) duplicates 2659 — re-routed to clean-room reproduction of the
  computational content of 2623/2659.
- impact-assessor-1 now fails on schema string lengths (500/1500 chars).

### Report
- `scratch/reports/20260905T075300Z.md` (copy of the final message).
- Directions: researcher-3 acknowledge 2635 on 2575/2581 (state the
  circulant.py defect), then p=11/7 per-cube LRAT, reuse researcher-1's symF
  for p=5; researcher-4 reproduce 2623 + 2659 Steps 4-5 in own code, check
  Cranston Lemma E against the paper, publish reproduction or objection; no
  r=28, no cr(24,132). Both reassess at pass 6.
- Balance: Ramsey 2 (r1, r3), Albertson 2 (r2, r4); discretionary third
  split one per lane; revisit when 2659 has a review.
- Flagged for the orchestrator: assessor prompt should state the schema
  length limits; researcher-1's 5 h capped run + enumeration is at the
  two-background limit; r=28 coordination with the fleet's 3c2e signer
  will be needed at pass 5-6.

### Blocked
Nothing operational.

### Next step (pass 5)
Check whether 2659 received a review or objection; read researcher-4's
reproduction outcome and researcher-3's acknowledgement; check researcher-2's
r=28 move against the fleet signer; confirm researcher-1 published 1^22 5^4.

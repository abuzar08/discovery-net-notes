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

## 2026-09-05 — pass 5 (07:55Z–08:58Z)

### Established
- Graph at 2700. Albertson r=27 proof_attempt 2659 now has: team clean-room
  reproduction (r4, 2673: found the two-K25 sensitivity, 601 > 588),
  outside review (signer 3e05d982, 2679: verifies + reproduces), author
  refinements 2677 (split bound 8721/7994 removes block-order claim) and
  2683 (34-row Step-2 table; cr(K13)/cr(K14) dependency dropped). Essential
  preprint-only input: Sadhu Thm 1.3; Barat-Toth Cor. 7 wording unverified.
  Fleet r=28 signer verified r2's 2569 (2699) and closed row 769 (2671).
- researcher-4: 2697 geng res/mod hazard (general; invalidates its own n=11
  residue rerun); started BORS placement (7089009).
- researcher-1: 2689 six more prime types by fixed-vertex lex-leader; 7 open.
- researcher-3: 2675 Theorem 5 (p >= 11) reviewed and confirmed (2687);
  2641 reviewed (2661, circulant headline prior art); Folkman defect
  acknowledged (2667). Two headline errors, both corrected within a pass.
- impact-assessor-1 still failing on schema string lengths.

### Report
- `scratch/reports/20260905T085700Z.md` (copy of the final message).
- Directions: researcher-3 p=7 cubes, p=5 via symF by citation, then a
  concrete p=2 feasibility estimate for the pass-7 stop-or-go; researcher-4
  off Albertson — re-shard n=11 at mod 6, BORS placement finding, optional
  standalone recursive-sampling lemma; reassess pass 7.
- Balance restored toward thirds: Ramsey 2 (r1, r3), Albertson 1 (r2),
  discretionary 1 (r4).
- Flagged for the orchestrator: assessor schema limits; 2621/2689 unreviewed
  are the largest certified items without a review; Barat-Toth Cor. 7
  wording is the last textual gap in the r=27 dependency list.

### Blocked
Nothing operational.

### Next step (pass 6)
Check for reviews of 2621/2689 and 2677/2683; read researcher-2's r=28
other-orders move and any fleet coordination; confirm researcher-4's mod-6
re-shard and BORS finding; collect researcher-3's p=2 estimate for pass 7.

## 2026-09-05 17:02Z — pass 6 (window 08:58Z–17:02Z; host down ≈ 09:40Z–16:56Z)

### Established
- Graph at 2866 (+166 since pass 5; team: 2709 BORS placement, 2711 Albertson r=28 proof_attempt, 2713 consolidated sampling lemma, 2717 R(4,6) p=7 limit). Fleet: 79 during the gap (R(5,5) 36, Hadwiger–Nelson 19, Albertson 12); fleet at Albertson r=29 (2761, Lean gates 2767/2793) on top of 2713.
- 2711 reviewed within the hour by the fleet's r=28 signer (2725) — same signer whose lemmas 2711 cites; Part A (order reduction to 55) still lacks an arm's-length check.
- 2717: p=7 out of reach for orbit-CNF (per-cube proof size flat in depth); researcher-3 recommends stopping at the p ≥ 11 table. Accepted.
- Host rebooted ≈ 09:40Z; all seven agents restarted simultaneously 16:56Z. Background runs lost: r1 cnc1539 (1247/1576) and cnc258 (31/256); r4 n=11 residues 4/6, 5/6 at mod 6. impact-assessor-1 produced its first valid pass (16:57Z).

### Report
- `scratch/reports/20260905T170200Z.md`. Ranks: r2 1, r4 2, r1 3, r3 4. Balance after this pass: Ramsey 1 (r1), Albertson 1 (r2), discretionary 2 (r3 re-selecting, r4); no rebalance toward Albertson (three fleet signers, r=29 crowded).
- Directions: researcher-3 — close R(4,6) with the ten p=5, f>22 types via `symF` (1500 s cap each), then literature-first re-selection; two or three candidates with evidence due at pass 7, method other than orbit-CNF tables. researcher-4 — relaunch n=11 shards 4/6, 5/6 at mod 6, claim only at 312,416,755; then the class-(iv) piece of Vitray's claim (is C₃□C₃ the only cr ≥ 3 member of BORS class (iv)) as a finding about DS21; no n=12; reassess pass 8.

### Blocked
- Nothing for me. Flags for the orchestrator: synchronized restart (stagger passes); r2/fleet coordination at r=29; `pkill -f <driver>` leaves solver children alive (r3 fix documented); reviewer-1's pre-reboot failure again shows `unrecognized_model`.

### Next step (pass 7)
- Decide researcher-3's new problem from its candidates. Check n=11 totals and whether the class-(iv) finding is filed. Check for any review of 2711 Part A outside the r=28 pair, of 2621/2689, and whether r1 resumed 1^15 3^9 from the 1287 surviving certificates. Read researcher-2's r=29 positioning relative to 2761.

## 2026-09-05 18:08Z — pass 7 (window 17:02Z–18:08Z)

### Established
- Graph at 2898. Five team contributions this hour (highest rate so far): 2867 reviewer-1 review of 2689 (confirmed, high confidence, positive control on Exoo's (4,6,35)-graph, four hash-only LRATs regenerated bit for bit); 2871 r2 (review corrections incl. a real float-literal defect, cr(K13)/cr(K14) dependency removed for r=28, general e(G[R]) floor, rows (57,824)/(57,825) of the fleet r=29 frontier eliminated); 2873 r1 (new theorem: no (5,5,42)-graph has type 1^15 3^9; 1576 cubes, exact orbit-stabiliser completeness check; 6 prime types open); 2879 r3 (measured p=2 involution limit, retracts its own 2717 extrapolation); 2887 r4 (retracts 2709's "class (iv) determined completely" — BORS Rem. 17.2/17.3 leave classes (iii)/(iv) incomplete; supplies the complete 36-graph peripherally-4-connected seed set).
- r2 positioned r=29 as a refinement of the fleet frontier 2761 rather than a duplicate; the pass-6 overlap risk resolved itself. Its next step is order 2r via Stehlik's clique cover, which would retro-fit r=27/28.
- Host: boot 09:43Z, no reboot since (r1's report of a second reboot is unsupported). Load 33 on 15 CPUs, 21 solver processes — timing-based feasibility measurements taken now are inflated; r3's stop rests on proof size, which is load-independent.

### Report
- `scratch/reports/20260905T180800Z.md`. Cumulative ranks unchanged: r2 1, r4 2, r1 3, r3 4; r1 had the highest recent return and its cumulative now nearly matches r4's. Balance kept at Ramsey 1 / Albertson 1 / discretionary 2, justified: R(5,5) is compute-bound, not researcher-bound.
- Withdrew my pass-6 class-(iv) target for r4 on its own 2887 evidence; accepted its mod-24 deviation as justified.
- Directions: researcher-3 — finish the p=5 f>22 symF sweep, close the directory, then select AND start its next problem in the same pass without waiting for approval, under four tests (first result under a core-hour; not orbit-CNF automorphism tables; publishable either way; uncrowded). researcher-4 — finish n=11 at mod 24 (total exactly 312,416,755), publish with Prop 14.1 and the "second counterexample must be 2-connected on >= 11 vertices" narrowing as headline; then a measured feasibility estimate for the Remark 17.2 expansion program from the 36 seeds, measured on one or two seeds, published either way. Reassess r3 at pass 8, r4 at pass 9.

### Blocked
- Nothing for me. For the orchestrator: host oversubscription (stagger passes or drop core caps to 3); 2711 Part A still unreviewed outside the r=28 pair.

### Next step (pass 8)
- Judge researcher-3's self-selected problem against the four tests and redirect if needed. Check the n=11 total and whether the feasibility estimate is measured or extrapolated. Check whether 1^12 3^10 or 1^2 5^8 landed for r1 and whether the certificate sweep kept scratch bounded. Watch r2's order-2r attempt and any review of 2711 Part A, 2621, or the five fresh team contributions.

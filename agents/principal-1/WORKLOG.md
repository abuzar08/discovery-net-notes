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

## 2026-09-05 21:12Z — pass 8 (window 18:08Z–21:12Z; controller idle ~19:45Z–21:03Z, my 19:00Z and 20:00Z passes did not fire)

### Established
- Graph at 2952. Team: 2901 (rev1 review of 2873, completeness proved more strongly than claimed — orbit sets equal, all 1576 certificates replayed), 2903 (r2: Barat-Toth Cor. 5/7/11 read from the EJC PDF; Sadhu Thm 1.3 dropped from r=27, connected complement now derived; Cor. 5 collapses six orders of r=28), 2905 + 2929 (r4: measured Remark 17.2 feasibility — 1.09e13 expansions, 30 of 36 seeds ~9 core-hours, cubic seed ~40 core-years; blocked on Figure 15.1, patch list not intrinsically recoverable; truncation-artifact warning), 2919 (r3: symF closes 24 of 28 open p=5 types in 1-16 s; contradicts its own 2717), 2933 (r2: order-2r non-domination lemma; r=29 order 58 closed for alpha(G) >= 4), 2947 (rev1: confirms 2919, tests the retraction — four untried high-f p=7 types fall in 2-4 s, plus one low-f type).
- **Two of my judgments reversed by evidence.** (i) R(4,6) is not finished: r3's "out of reach" verdicts were measured at f=0/1, but for symF the governing parameter is f; my pass-6 acceptance of the stop and my pass-7 "no more orbit CNFs" instruction were both wrong. (ii) The Barat-Toth gap I had queued since pass 4 closed and removed the last essential preprint input from r=27.
- Fleet has published no Albertson contribution since 2793; r2 is now alone in that lane and the pass-6 overlap risk is gone.

### Report
- `scratch/reports/20260905T211200Z.md`. Ranks (cumulative, within noise for 2-4): r2 1, r4 2, r1 3, r3 4; r3 had the highest recent return. Balance back at nominal thirds by itself: Ramsey 2 (r1, r3), Albertson 1 (r2), discretionary 1 (r4).
- Directions: researcher-3 — reversal, stay on R(4,6), candidate list shelved until p=5/p=7 settle; take p=7 next but regenerate everything in its own pipeline (reviewer-1 deliberately left five p=7 exclusions unclaimed; a lemma resting on the reviewer's runs would invert the verification order); fix the two reporting defects; standing rule — identify the governing parameter and measure both ends before any "out of reach" claim. researcher-4 — finish and publish n=11; then stop waiting for a human on BORS Figure 15.1: render p.145 of arXiv:1312.3712 to an image, read the figure, gate every transcribed patch on its own Definition 15.21 implementation and BORS's class structure, then run d <= 7 (~9 core-hours) or publish the documented failure. Reassess both at pass 10.

### Blocked
- Nothing for me. For the orchestrator: controller idle ~80 min; all seven agents restart within 30 s of each other; the C3xC3 note to Schaefer still needs a human; `.gitignore`'s `*.log` silently untracked every log in every researcher-1 artifact (other agents should run `git check-ignore -v` on their own directories).

### Next step (pass 9)
- Check whether r3 published the p=7 row from its own runs and whether 2717 was retracted or caveated. Check the n=11 total and whether r4 read Figure 15.1 and what its gates said. Watch r2's alpha(G) <= 3 triangle-free stability attempt. Check whether 1^12 3^10 or 1^2 5^8 landed for r1. Note whether 2711 Part A or 2621 finally drew a review.

## 2026-09-05 22:15Z — pass 9 (window 21:12Z–22:15Z)

### Operational failure (reported, not fixed — outside my read-only mandate)
- **Discovery Net block production has halted.** Last block 2952 at 19:46:20Z. RPC responds, `catching_up` false, ledger reads fine; `dump_consensus_state` frozen at height 2953 round 0 step 4 (precommit wait) since 19:46:24Z, validator set 3, `n_peers` 0, 4 txs in the mempool. The node cannot reach a 2/3 quorum with no peers — the other validators are unreachable. Needs the human/orchestrator.
- Four team contributions are accepted for broadcast but uncommitted and not citable: r4's narrowing theorem, r3's Theorem 6, r2's order-58 branch lemma, reviewer-1's review of 2933. Every agent detected the stall independently and none resubmitted; all recorded pending refs for a check-before-resubmit.
- Committed graph unchanged from pass 8, so this assessment is from repository commits and agent reports.

### Established
- r4: **n=11 census complete** — 312,416,755 graphs, 24 two-crossing-critical, none with cr >= 3; acceptance criterion met exactly. A second BKQ counterexample suppresses to >= 12 vertices. Plus the structural narrowing (every 2-crossing-critical graph with cr >= 3 is 3-connected or one of BORS's 36; digonal paths consist of digons, so its own Lemma 2 gives cr = 2). Plus **Figure 15.1 read as directed**: 31 configurations in five groups (20,3,5,2,1), class map confirmed twice; the gate caught the first transcription because the configurations are multigraphs — which retro-corrects its own 2929 (that enumeration built simple graphs only). Revised branching 31, not 20: d <= 6 = 29 seeds ~47 core-hours.
- r3: regenerated the four large-f p=7 types itself (1-3 s each) rather than citing the reviewer, giving **Theorem 6** (36 <= n <= 39: no automorphism of prime order p >= 5 except possibly 1^{n-35}5^7 or 1^{n-35}7^5, 59 certificates) and the **pk = 35 reduction** — every survivor's moved set is a (4,6,35)-graph with fixed-point-free sigma, one smaller question dominating all eight. Two instances in flight.
- r2: order 58 at r=29 impossible when H has no two disjoint triangles (Stehlik + Cauchy-Schwarz + additivity of cr; 11092 vs Z(29)=8281, no barrier machinery). With 2933 the order-58 open set is a single branch: H K4-free with two disjoint triangles. Reported a clean negative (Turan cap closes nothing; b=30 short by 74).
- reviewer-1: first review of the Albertson lane, chosen as the largest unreviewed gap; confirmed 2933, checked Stehlik/Barat-Toth against primary sources, validated the cover construction on 687,829 instances, recomputed the order-58 table under weaker assumptions (all nine rows still impossible), flagged one compressed load-bearing step in the disjointness argument.
- r1: no theorem for a second window — slow, not stuck. Measured that refinement beats solver time (a cube unrefutable in 240 s under any preset splits into 0.1 s children); 1^2 5^8 reorganised into 5061 cubes, median 0.1 s, no timeouts; 1^12 3^10 at 976/1576 verified; cross-run verification bookkeeping so replayed-and-deleted certificates still count; scratch 14 GB -> 3.2 GB.

### Report
- `scratch/reports/20260905T221500Z.md`. Ranks: r2 1, r4 2, r3 3, r1 4 (r1 lowest recent return, explicitly slow not stuck). Balance at nominal thirds; no reallocation.
- Directions: researcher-3 — drive the two fixed-point-free (4,6,35) instances to a verdict; if both refute publish Theorem 6 unconditional, with the pk=35 reduction stated separately as the reusable step; then state the p in {2,3} low-f frontier plainly instead of re-estimating it; verify its queued tx committed before resubmitting; CANDIDATES.md stays shelved. researcher-4 — transcribe the remaining (3,3) group of 20 under the same gates, file the multigraph correction to 2929 as its own contribution, then run d <= 6 only (~47 core-hours) as a resumable, .done-marked, acceptance-criterion-first job; no d=7, no cubic seed, no n=12; keep the n=11 ">= 12 vertices" consequence at the front of the write-up.

### Blocked
- The chain. Nothing publishes until block production resumes.

### Next step (pass 10)
- First: check whether the chain advanced past 2952 and whether the four queued transactions committed (and whether any agent duplicated a submission on recovery). Then: the (4,6,35) verdicts and whether Theorem 6 became unconditional; whether r4 transcribed the (3,3) group and started d <= 6; r2's b=30 class; whether 1^12 3^10 or 1^2 5^8 landed. Watch for a review of 2711 Part A or the inherited Albertson filter/ceiling machinery.

## 2026-09-05 23:20Z — pass 10 (window 22:15Z–23:20Z)

### Established
- **Chain recovered** at \(\approx\) 22:30Z after 2 h 45 m stalled; indexed height 3049. Every queued transaction committed; **no agent resubmitted any of them** — each checked commitment first, so there are no duplicates. Fourteen team contributions landed (3013, 3014 \(\times\) 4, 3016, 3018, 3028, 3034, 3036, 3038, 3044, 3046, 3048).
- r3: both fixed-point-free \((4,6,35)\) instances driven to a verdict — both resist, measured at both ends. Governing parameter identified as the **cross-cycle block** (\(\approx 85\%\) of variables, untouched by symF at \(f=0\) or by symC or by a \(D=10\) split); formula size points the wrong way (\(7^5\) is smaller and cleared fewer cubes). Missing lever named: \(S_k\) lex-leader on cross blocks or \(\mathbb{Z}_p^{*}\) multiplier quotient. Theorem 6 (h3014) reviewed and confirmed at h3048; the four \(p=7\) certificates are byte-identical to reviewer-1's own from h2947.
- r4: all 31 configurations of BORS Figure 15.1 extracted **from the PDF vector path operators**, not by eye, with six independent gates and two encoding traps caught (h3028). Then corrected its own feasibility qualitatively (h3038): the binding constraint is `crit2`'s representation cap (28 vertices, 62 edges) against expansions reaching \(n=59, m=92\) — decidable fraction 16.7% at \(d=4\), 2.3% at \(d=5\), **0% at \(d=6\)**. My pass-9 "run \(d \le 6\), \(\approx 47\) core-hours" describes a run that cannot be performed.
- r2: second-level split bound (the barrier is a partition, so cr-additivity applies across \(A,R\) and Gallai inside \(R\)); the three surviving order-58 barriers rise to 3783/7354/7858 against \(Z(29)=8281\); none closed, \(s=23\) is \(\approx 423\) short. Self-corrected the Turán pinning that had made \(s=0\) look impossible.
- reviewer-1: four reviews on the ledger; found an **unflagged dependency** — unlike \(r=27\) and \(r=28\), the \(r=29\) reductions still rest on \(\mathrm{cr}(K_{13})/\mathrm{cr}(K_{14})\); on the \(\mathrm{cr}(K_{12})\)-only base rows (827,\(|R|=6\)) and (828,\(|R|=6\)) survive. Also confirmed r2 read the *published* EJC text (wording differs from arXiv).
- Fleet re-entered Albertson without overlap: a Lean formalization (2953) derives r2's order-\(2r\) lemma **without** its special-cover assumptions — an outside strengthening.

### Report
- `scratch/reports/20260905T232000Z.md`. Ranks: r2 1, r4 2, r3 3, r1 4. r1 slow-not-stuck for a third window but close (\(\approx 400\) cubes left on \(1^{12}3^{10}\)); checkpoint set at pass 12 — if the lemma has not landed, I want the obstruction named, not a progress count. Recorded a pattern for r4: two feasibility estimates revised downward in two passes, both self-caught, both from costing throughput before checking the checker's domain.
- Directions: researcher-3 — **reassigned** to build the lever its own 3044 named (\(S_k\) lex-leader on cross blocks vs \(\mathbb{Z}_p^{*}\) multiplier quotient, chosen by measurement), with a written soundness argument, exhaustive small-case checks, and an explicit verified composition order (per reviewer-1's symC/symF finding); run it on the two instances; if either refutes, Theorem 6 becomes unconditional; either way publish the lever and offer it to researcher-1 by citation for its low-\(f\) types. Hard reassessment at pass 12, fallback = cages. researcher-4 — publish \(d \le 4\) with exact decidable/skipped counts; **cost the tester rewrite before starting it** (prototype to \(n \approx 60, m \approx 95\), throughput vs `crit2`, core-hours for \(d \le 5,6\)) and bring me the number; settle Širáň additivity when a slot is free.

### Blocked
- Nothing for me. For the orchestrator, sixth request: the \(C_3 \square C_3\) note to Marcus Schaefer for DS21 needs a human — the only blocked item no agent can clear.

### Next step (pass 11)
- Check whether r3 chose a lever route and whether its soundness harness is exhaustive; whether \(1^{12}3^{10}\) landed for r1; r4's \(d \le 4\) coverage numbers and the rewrite cost measurement; r2's \(s=23\) attempt and whether it folded reviewer-1's \(\mathrm{cr}(K_{13})\) finding into the \(r=29\) statement. Watch for reviews of r4's eight-item block and of 2677/2683/2761.

## 2026-09-06 00:30Z — pass 11 (window 2026-09-05 23:20Z – 2026-09-06 00:30Z)

### Established
- Chain healthy, indexed height 3079. Team: 3064 (rev1), 3068 (r2), 3074 (r4); r3's `symS` pushed to the repo and deliberately unclaimed. r1 and r4 mid-pass (both started 23:57Z); no r1 report this window.
- r3: the reassignment produced a working lever in one pass — **`symS`, cycle-shift normalisation** (\(\Phi_b(v_{j,i}) = v_{j,i+b_j}\); commutes with \(\sigma\), fixes internal and fixed-vertex orbits, carries cross orbit \((j,j',d) \mapsto (j,j',d+b_{j'}-b_j)\); modulo the diagonal \(\mathbb{Z}_p^{k-1}\)). Breaks the group completely for 864 clauses (+0.36%) on \(1^0 7^5\): no verdict in 3600 s / 2111 MB \(\to\) **UNSAT in 600 s / 354 MB**. \(1^0 5^7\) still resists. **Neither route I named (nor either of r3's own in h3044) was the right one.** The composition harness I made non-negotiable found `symC + symM` **unsound** (2304 uncovered at \(p=7\); \(\mu_u\) permutes the codes symC sorts by); symS not implicated. Correctly withholding the \(1^0 7^5\) claim until drat-trim + its own replay.
- r2: found the scope defect in its own published closure — the \(\mathrm{cr}(K_q)\) recursion defaulted to CCCG 2021 values and **no file ever called `set_base`**; at the bare \(\mathrm{cr}(K_{12})=150\) seed the \(b=30\) class reopens at \(m=839,840\). Repaired rather than weakened: `crminus.py` (vertex-deletion averaging, \(g(28,3)=5324\)) closes it at every rung of a 217/219/223/225 ladder, so the published result is **strictly stronger than as filed** and needs nothing beyond \(\mathrm{cr}(K_{12})=150\). Literature established: \(\mathrm{cr}(K_{13})=225\) is Aichholzer CCCG 2021 (single-author, 1000+ CPU-years, absent from DS21 and from Clancy-Haythorpe-Newcombe); strongest refereed value is \(\ge 219\) (McQuillan-Pan-Richter, JCTB 2015).
- r4: **used its own census to falsify its own program** (3074) — 19 3-connected 2-crossing-critical graphs on \(n \le 11\) with no \(V_8\) and no \(V_{10}\) are not produced by the expansion program, against a theorem allowing four exceptions; all 19 non-peripherally-4-connected. Three omitted ingredients (cr = 1 bases, edge duplication, global type constraint \(x \in T_v \iff v \in T_x\)); branching corrected back to \(\le 20\). **Consequence: the in-flight \(d \le 4\) run enumerates the wrong space and its coverage is void.**
- rev1: 3064 confirms the order-58 pair as computed, finds the same seeding dependency independently (six minutes apart from r2, from the opposite direction) plus a description defect — the prose calls \(Y=52\) the minimiser when it is \(Y=48\), and at \(m=840\) the published margin is exactly zero.

### Report
- `scratch/reports/20260906T003000Z.md`. Ranks held: r2 1, r4 2, r3 3, r1 4 — r3 takes second the moment the \(1^0 7^5\) certificate replays. r1 checkpoint stands at pass 12; no evidence this window and none inferred from silence.
- Directions: researcher-3 — replay before claiming; publish `symS` as a lemma with soundness, the exhaustive orbit-cover check, the measured effect, and **the composition negative as its own result**; refine Theorem 6 to drop the \(7^5\) clause; measure rather than escalate on \(1^0 5^7\); **offer symS to researcher-1 by citation** (its hard types are exactly low-\(f\) semiregular); bring detached jobs from three to the cap of two. Pass-12 hard deadline discharged. researcher-4 — the in-flight run is void; rebuild the construction with the three omitted ingredients; **gate on the census (must produce all 19 and reproduce all 36 seeds)**; only then re-cost, answering representability before core-hours; publish one corrected feasibility statement rather than a third revision; Širáň additivity when a slot is free.

### Blocked
- Nothing for me. Orchestrator, seventh request: the \(C_3 \square C_3\) note to Marcus Schaefer for DS21.

### Next step (pass 12)
- Did the \(1^0 7^5\) certificate replay, and is symS a lemma with the composition negative published? Did r1's \(1^{12}3^{10}\) land — the checkpoint is due, and if not I want the obstruction named. Did r4 gate the repaired program on the 19? Did r2 finish the bare-seed audit of 2933 and the no-two-disjoint-triangles closure? Watch for reviews of 3046, r4's eight-item block, and 2711 Part A.

## 2026-09-06 01:35Z — pass 12 (window 00:30Z–01:35Z)

### Operational
- **Second chain stall in six hours, same signature.** No block since height 3095 at 00:38:04Z; consensus frozen at 3096/0/step 4 since 00:38:08Z; `n_peers` 0; five txs queued. First outage was 2952 \(\to\) 3031 (2 h 45 m, self-resolving). Recurring, not incidental — flagged to the orchestrator as a standing infrastructure problem. Every agent detected it and none resubmitted.
- Queued and uncommitted: r3's Theorem 7, r2's ladder audit, reviewer-1's h3013 review, r4's Figure 14.3 refinement.

### Established
- r3: **Theorem 7 certified** — `symS` refutes \(1^0 7^5\) (drat-trim `s VERIFIED`, 880 s, 0 RAT lemmas in core; own checker replayed the 511 MB LRAT to the empty clause at step 3233859 against a formula regenerated from \((n,s,t,f,p,k)\) alone). Four of eight survivors eliminated; one exception clause discharged. **And `symS` is NOT vacuous at \(p=2\)** — it breaks \(2^{17}\) on \(1^0 2^{18}\) for 102 clauses, verified sound exhaustively, so h2879's involution frontier was measured without the one lever that applies there. The \(p=2\) frontier — where all 37 known \((4,6,35)\)-graphs' symmetry lives — is live again. Third premature "finished" call on this lane (mine at pass 6, r3's h3044, r3's own mid-pass assertion).
- r2: **the order-58 reduction at \(r=29\) is unconditional** — `ladder.py` re-ran all three pieces at all four rungs (217/219/223/225); pieces 1 (2933) and 2 (3014) were never seed-sensitive, piece 3 repaired at 3068. Rests on nothing beyond \(\mathrm{cr}(K_{12})=150\). Sharp negative: `crminus` tops out at 3016 against the 3557 needed for \(s=23\) (gain 28, need 569) with the exact arithmetic of why. Three corrections caught before publishing.
- **r2's strategic finding:** both open Albertson frontiers reduce to one self-contained sub-problem — a crossing lower bound at intermediate density beating integer-aware sampling (77% of \(K_{32}\); 425 more on a 50-vertex Gallai forest). The team owns the bound to beat (r4's 2713).
- r4 (strongest window): verified BORS Theorem 17.1(3) exactly at \(n \le 11\), \(65 = 36+10+15+4\) with no residue (3080); connectivity-2 branch nearly closed via Theorem 14.5 and the Figure 14.3 vertex-identification convention — over all 55 identifications at the least workable \(k\), all CRIT2, none CRIT_GE3 (3084). **The lemma improves to "3-connected, or one specific graph."** My Širáň-additivity suggestion was wrong (Leaños-Salazar settles 2-*edge*-cuts, not 2-*vertex*-cuts) and r4 said so.
- reviewer-1: reviewed h3013, re-derived case (1) in full, checked BORS Thm 1.3 word-for-word against the 176-page source, and **re-confirmed \(\mathrm{cr}(C_3 \square C_3) \ge 3\) by its own exact planarisation search**, independent of the census program. Two independent confirmations now under the whole topological lane.
- r1: fourth window without a theorem; **checkpoint discharged** — obstruction named concretely (host contention, load 22-29 on 15 cores; hard tail needing a second refinement level) plus a real fix (the driver was re-attempting known-hard cubes at full limit on every resume).

### Report
- `scratch/reports/20260906T013500Z.md`. **Rank change as promised: r3 to 2, r4 to 3** — close call, basis recorded (r4's window and cumulative are at least as large; tiebreak is transferability, since `symS` moves two other lanes).
- Directions: researcher-3 — publish Theorem 7 and `symS` as a lemma in its own right with the `symC+symM` negative; **then \(p=2\) first**, treating h2879 as void rather than a baseline; keep \(1^0 5^7\) on cube-and-conquer reporting per-cube proof sizes; offer `symS` to researcher-1 by citation. researcher-4 — settle or abandon the \(n=14, m=22\) holdout; publish \(d \le 4\) stating whether the pre-correction enumeration survives the repaired scoping; **then take the dense crossing bound** (\(\mathrm{cr} \ge 3557\) on 32 vertices missing 113 edges) as its own problem — not Albertson machinery, and it is the author of the sampling bound to beat.
- Recorded for the orchestrator: R(5,5) is limited by host contention, not by r1; r1 should adopt `symS` by citation once it commits.

### Next step (pass 13)
- Did the chain recover and did the four queued items commit without duplication? Did r3 run \(p=2\) with `symS` and what did it measure? Did r4 close the holdout and publish \(d \le 4\) cleanly? Did r2 or r4 start on the dense crossing bound? Did \(1^{12}3^{10}\) land for r1, and did it pick up `symS`?

## 2026-09-06 06:35Z — pass 13 (window 01:35Z–06:35Z)

### Operational (dominant)
- **The chain has been dead 5 h 50 m and will not self-heal.** No block since height 3095 at 00:38:04Z; consensus frozen at 3096/0/step 4 since 00:38:08Z; validator set 3, `n_peers` 0. All local containers up, two healthy, RPC answers, ledger reads — the node is waiting on votes from two validators it cannot reach, and no local process can supply them. The first stall (2952 \(\to\) 3031) self-resolved; this failure mode does not.
- An additional RPC blip: r2 found the endpoint entirely unreachable at 04:52Z and stopped its pass per contract; it answers again now. Controller largely idle 01:40Z–06:25Z (one agent pass in that window; my 02:35–05:35 passes did not fire); all agents restarted within seconds at 06:25Z.
- **Six or more finished contributions unpublished**: r3's Theorem 7 (2 tx), r4's connectivity-2 closure and \(d \le 4\) run, reviewer-1's h3013 review, r2's ladder audit; r2's newest result not submitted at all. Mempool shows 5, fewer than accepted — **at least one tx was dropped; a mempool is not durable storage.** r4 reports an earlier resubmission caused a duplicate; I saw none at the pass-10 reconciliation and cannot check with the ledger frozen, so I record it without endorsing. Nothing is lost — all artifacts are on GitHub.

### Established
- r4: **connectivity-2 branch closed** — all 36 graphs of BORS Thm 1.3(2) have cr = 2; Fig. 14.1 gives Thm 1.3(1)'s thirteen as 10 connected + 3 disconnected, all CRIT2; Thm 14.5 returns the third branch. Holdout resolved at \(k=4\) (142,321 matchings, 64 critical, all CRIT2). **A second BKQ counterexample exists iff a 3-connected one exists**, and by the census it suppresses to \(\ge 12\) vertices. Also found its attachment model still wrong in a way the identity check could not catch (Def. 15.22 takes \(x,y,z\) to *be* the neighbours; \(w \in T_v \iff v \in T_w\) **is** port agreement, not an extra rule; a patch costs \(|\mathrm{internal}|-1\), so four configurations are free). Gate now informative: 36/36 seeds plus one of the 15 targets, the (9,18) graph over \(K_{3,3}\).
- **Ruling given on r4's retraction question: no retraction, and the inconsistency was mine** — I called the \(d \le 4\) counts void at pass 11, then asked for them published with a scoping statement at pass 12. Exact counts over a delimited enumeration with the scope stated are a publishable fact; what I was guarding against was a Remark 17.2 coverage claim, which r4 did not make. `refines` to relate the two enumerations once the gate passes.
- r3: **\(p=2\) tested with `symS` and reported negative** — no refutation either way on \(1^0 2^{18}\), and proof-production *slower* with the lever (98 vs 113 MB/min). Breaking \(2^{17}\) is not what \(p=2\) is waiting for; corrected its own optimistic framing. One pass from question to measured answer.
- r2: **order-57 frontier from three open rows to two** — row 826 and row 827 at \(|R|=7\) eliminated by two new ingredients (blocks are edge-disjoint so \(\sum \mathrm{cr}(Q_i) \le \mathrm{cr}(G)\) with no vertex-disjointness, allowing augmentation by \(w_1,w_2\); and low vertices force block degree). Two negatives recorded so they are not retried; two corrections caught first.
- r1: no report; controller idle for most of the window.

### Report
- `scratch/reports/20260906T063500Z.md`. **Ranks fixed at r2 1, r3 2, r4 3 and I will stop re-ordering 2 and 3 pass to pass** — they are tied on evidence and I have moved them past each other twice, which is noise; recent return is where a strong window belongs. r4's window was the stronger this time.
- Directions: researcher-3 — treat \(p=2\) as finished for now (the obstruction is not symmetry); finish \(1^0 5^7\) under cube-and-conquer with `symS` and report cubes cleared and per-cube proof size against the 259/1024-at-2.1 MB baseline; when the chain returns, verify before resubmitting and make `symS` citable first, since the transfer to researcher-1 is the largest thing the outage is blocking. researcher-4 — write the "iff 3-connected" statement up as the lane headline, independent of the expansion program; no retraction; finish the gate on all 15 targets; publish **one** corrected feasibility statement superseding 3028/3074, with the port-agreement insight stated explicitly.
- Raised a contract question for the orchestrator: the stop-on-unreachable-node rule was written for a transient fault and under a six-hour outage it costs research time (r2 stopped; r3/r4 continued with repository-only work). Suggest keeping the prohibition on unverifiable claims while stating explicitly that repository-only work continues.

### Blocked
- The chain, for the whole team. Restoring the peer validators is the highest-value action available to anyone. \(C_3 \square C_3\) note to Schaefer: ninth request.

### Next step (pass 14)
- Whether the chain returned, which of the queued transactions committed, whether any was lost with the mempool, and whether any duplicate appeared on recovery. Then: r4's gate on the 15 targets and the single feasibility statement; r3's \(1^0 5^7\) cube comparison and whether `symS` became citable; r2's row (57,827) at \(|R|=8\); whether r1 published \(1^{12}3^{10}\) or picked up `symS`.

## 2026-09-06 07:40Z — pass 14 (window 06:35Z–07:40Z)

### Operational (still dominant)
- **Chain dead 6 h 51 m** — no block since 3095 at 00:38:04Z, consensus 3096/0/step 4, `n_peers` 0, mempool grown 5 \(\to\) 9. All three containers up and healthy; consensus stalled inside a running node. **At least ten finished contributions unpublished** (r4 four verified absent plus new work, r2 three, reviewer-1 two, r3 one). Nothing lost — all artifacts on GitHub.
- **Recommendation given to the orchestrator:** restart `discovery-node-local-cometbft-1` (or restore the peer validators), then have every agent drain its queue against the committed ledger. The mempool will not survive the restart, and resubmission is now safe because of r4's new tool.

### Established
- r4: **acceptance gate passed, 36/36 seeds and 15/15 targets**, each target built with an explicit witness; the 4 h 57 m brute force was the wrong shape, and restructuring around each target's order and size finished all fifteen in minutes. All four of my pass-13 items delivered. **Major reversal: branching is 107 placements per degree-3 vertex** (20 is the count for a *fixed* type) and representability is **99.6% at \(d=4\), 41.3% at \(d=6\)**, against the 16.7% and 0% of h3038 — so the obstacle is search size, not the tester, and my relaying of h3038 as fact in three reports is retracted at source. Its resolution of the \(d \le 4\) question is sharper than mine: the old enumeration is a *different construction*, not a sub-case, and its finding survives because it concerns \(\mathrm{cr}(L) \ge 2\) bases.
- r4 also built **`publish_queue.py`** for the team — idempotent, checks the *committed ledger by title*, submits only what is genuinely absent. Recommended for every agent; it is what makes a node restart safe and it disposes of its own earlier duplicate worry.
- r2: **order 57 from nine open cases to four**; (57,827) at \(|R|=8\) dies **structurally** — \(e(L)\) is an identity, \(e(G[R]) \le \binom{|R|}{2}\) pins \(e(L) \in [555,573]\), and every cover of 49 vertices by two disjoint big blocks carries \(\ge 576\) edges, so no admissible block multiset exists. Also corrected its pass-15 plan as impossible in magnitude (would need \(e(G[R]) \ge 35\) while \(\binom82 = 28\)) — **I endorsed that plan in my pass-13 report without checking the magnitude.**
- r3: \(1^0 5^7\) measured on five axes; `symS` doubles the cleared cube fraction (259 \(\to\) 541 of 1024) leaving a 483-cube hard core at 2.1 MB median; complete \(D=10\) certificate \(\approx\) 4.1 GB / 13 core-hours, so the next step is a deeper split. Resolved a `drat-trim FAILED` scare correctly (load-related; verified instantly in isolation) and found stale pre-`symS` sources in scratch.
- **Cross-lane convergence:** r1 (R(5,5)) and r3 (R(4,6)) independently reached "refinement beats solver time" from the same evidence shape — a cube plateau with flat per-cube proof size.
- r1: native-LRAT driver (162 and 384 cubes in half an hour); found and contained a 12 GB stale-proof leak (root cause honestly recorded: `rm -f a/c*.lrat b/c*.lrat` aborted under zsh on the first non-matching glob); 60 s caps push hard cubes to refinement. 1887/3121 and 2620/5061.
- reviewer-1: confirmed h3080 with its own \(V_8\)/\(V_{10}\) detector and its own build of Theorem 15.6's four graphs, after correcting its own too-strict peripheral-4-connectivity test; noted the source's "36" needs its \(\le 10\)-vertex qualifier (a reader gets 41).

### Report
- `scratch/reports/20260906T074000Z.md`. Ranks held (r2 1, r3 2, r4 3) with the criterion made concrete: **r4 has had the strongest window twice running; if its next window is again the stronger of the two, it moves to second.** r1 sixth window without a theorem — slow not stuck, throughput materially changed, no intervention, but recorded that the mandated Ramsey third has gone six windows without a publication.
- Directions: researcher-3 — take the deeper split on the 483-cube core and cost it before running; state "refinement beats solver time" as a cross-lane finding jointly with r1's evidence; make the checker refuse to run from sources not matching the artifact hashes; when the chain returns publish `symS` citable **first**, using r4's queue. researcher-4 — put the gate-before-costing reasoning in the feasibility artifact explicitly; run \(d \le 3\) to completion and cost the \(2^k\) edge-duplication blow-up before \(d=4\); publish a bounded negative if \(d=4\) is out of reach; document `publish_queue.py` in the shared repository for the other agents.

### Blocked
- The chain. \(C_3 \square C_3\) note to Schaefer: tenth request.

### Next step (pass 15)
- Whether the node was restarted, which transactions committed, whether any were lost with the mempool, and whether `publish_queue.py` was adopted. Then r4's \(d \le 3\) result and the \(d=4\) cost; r3's deeper split and whether `symS` became citable; r2's remaining four order-57 cases and the C/D transfer to order 58; whether \(1^{12}3^{10}\) finally landed.

## 2026-09-06 08:45Z — pass 15 (window 07:40Z–08:45Z)

### Operational
- **Chain dead 7 h 55 m**; height 3095 since 00:38:04Z, `n_peers` 0, mempool **11**. My pass-14 restart recommendation was not acted on. Repeated with one addition: **the mempool will be lost on restart, so the resubmission list must be rebuilt from the agents' worklogs, not from the node.** ~15 contributions unpublished; ledger ~8 h behind the repository.
- r4 published `publish_queue.py` for the team at `notes/tooling/publication-queue/` with a README on why "accepted for broadcast" is not evidence of publication.

### Established
- r4: **\(d=4\) costed out before starting, as ordered** — the dominant term is edge duplication (\(2^k\), \(k\) up to 18), absent from *every* prior cost model. \(d \le 3\): \(5.65\times10^8\) builds \(\approx\) 56 core-hours; \(d \le 4\): \(1.34\times10^{11}\) \(\approx\) 13,300 core-hours, and a 100\(\times\) C speedup still leaves ~130. Supersedes all its published cost figures; stopped the 56-hour Python run. Its own summary is the campaign's best methodological line: *the old figures were coherent, reproducible, and wrong by an order of magnitude for three consecutive reports because nothing ever compared the program's output against something independently known.*
- r4 also caught a real gap in its own headline: one Figure 14.3 repair came out 3-connected, impossible for a member of Thm 1.3(2), exposing its "least \(k\)" heuristic as a guess. Replaced by enumerating **all** partial matchings at \(k \le 4\); 16/20 components done, every result CRIT2. The claim now rests on a stated hypothesis rather than a guess.
- r2: the pinned order-57 \(|R|=9\) case is now a finite question about seven vertices. \(H[L]\) is exactly \(K_{24,24}\); 188–189 edges across seven \(z\) each \(\le 27\) force every one \(\ge 26\), so \(\min(a_z,b_z) \ge 2\) — **no one-sided vertex**, the clique-building branch is vacuous, and the residue is \((\mu_1,\mu_2) \in \{(4,4),(4,5),(5,4),(4,6),(6,4),(5,5)\}\). Recorded that its own pass-17 plan targeted a branch that does not exist, and that the 200–300 margin needs a new idea.
- r1: **checker gap found, fixed, and controlled.** CaDiCaL's native LRAT can list a hint whose clause is already satisfied; the drat-trim-era checker rejected it, failing 17 of 3121 cubes. Now skips satisfied hints, with negative controls (flipped literal rejected; deleted empty clause returns false). All 17 verified. \(1^{12}3^{10}\): 2957/3121 replayed, 164 split into 2624 grandchildren, and the checker now verifies a **chain** of refinement levels — everything except the grandchildren replays is verified. \(1^2 5^8\) at 4732/5061.
- reviewer-1: closed the gap it had itself declared open in the h3080 review (the class of 15 planar 3-reductions) and settled (13,21) at \(k=3\).

### Report
- `scratch/reports/20260906T084500Z.md`. **Rank change on the criterion I set: researcher-4 to 2, researcher-3 to 3** — r4 had the stronger window for the third time; r3 filed no report this window (its pass has run 80 minutes, spawning solver jobs, so not hung).
- Directions: researcher-3 — pass-14 direction stands (cost the deeper split before running it; state the cross-lane refinement finding once; make the checker refuse mismatched sources); plus: a multi-hour computation belongs in a detached resumable job, not inside a pass that blocks reporting; publish `symS` citable first when the chain returns. researcher-4 — finish the \(k \le 4\) check and publish the headline with its hypothesis labelled as one; decide \(d \le 3\) by prototype measurement or publish the cost model as the closing negative on Remark 17.2; **then change target to the dense crossing bound** (\(\mathrm{cr} \ge 3557\) on 32 vertices missing 113 edges; sampling 2988, r2's averaging 3016; order-57 form needs 425 more on a 50-vertex Gallai forest) — r2 has now twice named it as where both frontiers bottleneck, r4 authored the sampling bound to beat, and it is a crossing-number lemma rather than r2's barrier/block work, so no overlap.

### Blocked
- The chain. \(C_3 \square C_3\) note to Schaefer: eleventh request.

### Next step (pass 16)
- Whether the node was restarted and the queues drained from worklogs; whether any contribution was lost. Then: r1's \(1^{12}3^{10}\) lemma (one run away); r3's costed split and the 80-minute pass; r4's headline hypothesis, the \(d \le 3\) decision, and whether it started the crossing bound; r2's \((\mu_1,\mu_2)\) residue.

## 2026-09-06 09:45Z — pass 16 (window 08:45Z–09:45Z)

### Operational
- **Chain recovered \(\approx\) 09:17Z after 8 h 39 m.** Indexed height 3290, mempool empty. **Thirteen team contributions committed at 3284–3285 with zero duplicate titles across the whole team's output** (checked the full ledger, not a sample). The verify-before-resubmit protocol plus r4's `publish_queue.py` held through a mempool loss and nine hours of held work. Standing practice.
- One open operational item: **r3's pass started 07:13:45Z and was still running at 09:37Z** (2 h 23 m against a typical 3–20 min). Not hung — controller alive, executing shell commands — but no report for two windows. Recommended to the orchestrator: a wall-clock cap on a pass with a forced report.

### Established
- r2: **order-57 row 827 eliminated; order 57 from nine open cases to one open row** ((57,828) at \(|R| \in \{10,11\}\)). Two unused facts did it: \(Z\) is a \(G\)-clique (so the König clique has order \(31-\mu_1\), not \(30-\mu_1\) — a whole crossing level), and the blocks *partition* \(L\), so every low vertex has exactly four \(H\)-neighbours in \(R\), making \(e_H(L,R)=192\) exact and forcing \(\sum_z a_z \ge 92\); König caps it at 14/36/58/80 for \(\mu_1=2..5\), so \(\mu_1,\mu_2 \ge 6\), five disjoint triangles, \(\theta(H) \le 28\) against 29.
- r2 corrected its own pass-18 verdict ("margin sits at 200–300, needs a new idea") — right about the crossing route, wrong as a verdict on the case, which closed from the clique-cover side. **I amplified that verdict in pass 15 and used it to justify redirecting r4**, so the correction lands on me too.
- r4: **the sampling barrier is structural and instance-independent** — measured over nine instances (\(n=32,40,50\), density 0.6–0.94): Jensen is never the lossy step (hull vertices bracketing the mean 0–7 apart in \(q\) against \(q\) in the hundreds), and the recursion is scale-free (spread over all \(s\) never exceeds 0.01). Both follow from the telescoping identity: unrounded recursion = single-level bound, rounding is the entire gain, worth <0.1% here. \((n,q)\)-only bounds capped at 4644 by an explicit drawing while refinements return 3022, so **structure beyond \(n\) and \(q\) is the only remaining lever**. `bound_report.py` answers any \((n,q)\).
- r4 also **justified** \(k \le 4\) from the hinge count rather than merely flagging it (Thm 14.3 fixes two hinges; Claim 1 puts the cycle at the internal node; the tree is a path, so at most four vertices are duplicated), and closed Remark 17.2 by measurement (networkx-free builder capped at 1.18\(\times\); \(d \le 4\) alone \(3.6\times10^4\) core-hours; seeds run to \(d=10\)).
- r1: seventh window without a theorem. \(1^2 5^8\) first level complete (4807/5061 replayed), second round launched (12,935 cubes); \(1^{12}3^{10}\) second round at 3667/5581, third needed. Hard-cube count per level is **falling** (164 \(\to\) 102), which is the number that decides convergence.
- reviewer-1 opened **h2621**, the oldest unreviewed item: formula set-equal to its own independent construction, level-2 layer verified exhaustively with its own group code (all \(2^{13}\) objects, 3378 good, 42 orbits), level-3 completeness sampled 60/60 with 1200 running, replay 2197/19741 with 0 failures and every hash matching bit for bit.

### Report
- `scratch/reports/20260906T094500Z.md`. Ranks: r2 1, r4 2, r3 3, r1 4.
- **Pattern recorded and acted on:** of my last four named targets for r4, one was withdrawn on its evidence, one used the wrong tool, one was unrunnable as scoped, and this one produced a negative — while its self-chosen steps (census cross-check, vector-art extraction, acceptance gate, edge-duplication term) were all right and decisive. **Its judgment in its own subject has been better than mine.**
- Directions: researcher-3 — end the long pass and report whatever state the split is in; put multi-hour work in a detached resumable job; **publish `symS` citable immediately** (Theorem 7 committed at 3285, so the four-pass transfer blocker is gone); then finish the split with the cost stated first. researcher-4 — finish \(d \le 2\) and write one consolidated statement of what the lane proves and leaves open, then **choose its own next target and start it in the same pass**, reporting the choice with evidence, under four tests (few core-hours; certificate-checkable; publishable either way; uncrowded); named option it may take instead — the structure-aware crossing bound its own finding points at.
- Checkpoint set for r1: if \(1^{12}3^{10}\) is not published by pass 18, I want an estimate of the total remaining rounds with the per-level hard-cube counts justifying it — not another progress count.

### Blocked
- Nothing for me. \(C_3 \square C_3\) note to Schaefer: twelfth request.

### Next step (pass 17)
- Whether r3 ended its pass, reported, and published `symS`; whether r1 picked up `symS` and how the refinement rounds are converging; r4's consolidated statement and its chosen target; r2's \((57,828)\) at \(|R| \in \{10,11\}\); reviewer-1's h2621 verdict and the three reviews it still has pending.

## 2026-09-06 18:40Z — pass 17 (window 09:45Z–18:40Z)

### Contract change
- The human raised the R(5,5) minimum to **two researchers by genuinely independent methods** and moved **researcher-3 into the second R(5,5) seat**, ruling explicitly that the compute-bound argument is answered by assigning distinct methods, not by removing a seat. I made that argument in passes 7, 12 and 14 and it was wrong in a specific way: I reasoned about cores when I should have reasoned about evidence — every error this campaign caught was caught because a second independent route existed. Allocation now: R(5,5) 2 (r1, r3), Albertson 1 (r2), discretionary 1 (r4). Not raising the minimum further.

### Operational
- Controller idle 09:40Z–18:28Z (8 h 48 m); my 10:45Z–17:45Z passes did not fire; all agents restarted 18:28Z. **Chain healthy** — four peers, height 3443, mempool empty; the absence of blocks since 16:03Z is an absence of transactions during the outage, not a fault.
- **Review capacity is now the binding constraint**: reviewer-1 reports **36 unreviewed team contributions** after the flush. One reviewer against four researchers cannot keep up. Recorded for the orchestrator (second reviewer, or an accepted and stated lag); no target named.

### Established
- r3 (final R(4,6) window): `symS` published as a standalone citable lemma at **h3295**, stated generically with Lemma S, the completeness proof, the composition matrix, the `symC + symM` unsoundness, **and a transfer table for r1's open types** (\(1^0 3^{14}\) breaks \(3^{13}=1594323\)); plus **99.86% of \(1^0 5^7\) refuted exactly** (prefix-free leaf tags: 4188429/4194304, 5875 open; all 10404 leaves replayed) at h3297, with the verifier printing `PARTIAL … is NOT refuted`. Declines to project a finish: survivors 483 \(\to\) 152 \(\to\) 382, *rising*.
- **A measured contradiction, and an instruction of mine withdrawn.** r3: a fivefold cap increase closed **zero** of 382 depth-18 survivors while one more level closed them immediately (and 400 s \(\to\) 30 s gave 18\(\times\) throughput). r1: at 60 s the hard fraction is 10–12% with 16 children per split, so the hard set multiplies by \(\approx 1.9\) per round while work multiplies by 16 — refinement **diverges** — and its 300 s runs had \(\approx\)5% hard, so most children just needed time. Both sound; the "refinement beats solver time" cross-lane finding I asked r3 to publish at passes 14–15 is **withdrawn**. The disagreement is itself the best argument for the human's ruling.
- r4: **closed the entire infinite \(V_{10}\) tile family from the literature with no computation** (BORS Cor. 2.13 + Thm 5.5 + Thm 2.14). New theorem: a second counterexample is 3-connected, has \(\ge 12\) vertices, and has no \(V_{10}\) subdivision — hence lies in a **finite** class. `LANE.md` consolidated. Chose its own target with evidence (the \(V_8\)-containing, \(V_{10}\)-free branch — the only survivor; BORS Rem. 17.3 calls it least explored), read Austin's thesis and found her definition is the correct one so her 312 graphs could contain a cr-3 example nobody has asked about, and started \(n=12\) with every constraint now a theorem (3-connected, \(\delta \ge 3\), \(m \le 3n-4 = 32\)) — strictly smaller than the \(n=11\) census. **Delegating the choice was right.**
- r2: the last order-57 row **does not close, by exactly one**, settled over every admissible multiset (short by 1 at (24,23) and (24,22), by 4 at (25,22)), with a structural account of why. Caught a bad call of its own: an aggregate bound returned 26 where the per-block truth is 145, and it was about to abandon the row on that number.
- r1: measured that its refinement strategy **diverges** and revised to bounded escalation (60 s, then 600 s on timeouts only, then refine). Replay is \(\approx\)1/3 of cost, so proof size matters as much as solve time.
- reviewer-1: three reviews committed (h3285, h3307, h3309); verified branch (1) of h3285 with its own code (16 components; ten of connectivity 1; the other six exactly \(3\times K_5\) and \(3 \times K_{3,3}\); \(10+3=13\) matching BORS Thm 1.3(1)); h2621 replay at 6322/19741, 0 failures.

### Report
- `scratch/reports/20260906T184000Z.md`. Ranks: r2 1, r4 2, r3 3, r1 4. r1's pass-18 checkpoint restated in the form the new evidence makes sensible: a stated estimate of when \(1^{12}3^{10}\) closes under escalation, with the numbers behind it.
- Directions: researcher-3 — close R(4,6) (no further compute on \(1^0 5^7\)); do **not** publish the withdrawn cross-lane finding; take the **unconditional neighbourhood-gluing attack** as leading candidate (neighbourhood is a (4,5)-graph, non-neighbourhood a (5,4)-graph; \(R(4,5)=25\) pins the degree range — verify from primary sources), because it assumes no symmetry at all whereas r1's programme constrains only symmetric graphs; its prefix-free tree accounting can report an **exact** refuted fraction of an unconditional search space, which nobody else here can; may choose a better independent method and report the evidence. **Overlap to avoid: r1's six open prime types (the tool moves, the instances do not) and the fleet's 43-vertex programme.** researcher-4 — lead `LANE.md` with the finite-class theorem; finish \(n=12\) with the n=11 acceptance discipline; use Austin's 312 as candidates never as a classification; cost \(n=13\) before starting; keep artifacts self-contained for a late reviewer.

### Blocked
- Nothing for me. \(C_3 \square C_3\) note to Schaefer: thirteenth request.

### Next step (pass 18)
- r3's method choice and its first measurement, and whether the crowding query was published with it. r1's escalation results and whether it picked up `symS` from h3295. r4's \(n=12\) verdict. r2's order-58 transfer. Whether the review backlog is closing or growing.

## 2026-09-06 19:45Z — pass 18 (window 18:40Z–19:45Z)

### Operational — third stall, different signature, and a correction of my own
- **My pass-17 reading was wrong.** I called the block gap since 16:03Z "an absence of transactions, not a fault". The consensus round state shows the node entered **height 3444, round 0, step 8 (commit) at 16:04:41Z** and never left — already true before the controller returned. I read a healthy `/status` instead of the round state, which is the check that diagnosed the first two stalls.
- This outage differs from the first two (step 4, `n_peers` 0): here there are **four peers** (node-abu-4..7), validator set 3, five txs queued, all containers up and healthy. The commit step blocks on the **application** answering, not on votes. Recommendation: **restart `discovery-node-local-application-1` first**, CometBFT only if that fails, then drain via `publish_queue.py`. Peers report `latest_block_height` null so I cannot tell read-only whether they are stuck too.
- Queued and uncommitted: r2's pass-21 lemma and pass-22 objection, r3's first R(5,5) lemma, r4's \(d \le 2\) contribution, reviewer-1's h2621 review.

### Established
- **r3's first R(5,5) pass is the best opening of a lane this campaign** — and it chose a better frontier than the one I named (I proposed \(n=42\) gluing). It took the **upper-bound side, \(n=44,45\)**: since \(43 \le R(5,5) \le 46\), excluding 45 improves the published record and is strictly easier than \(n=43\). Crowding query: of 390 R(5,5) contributions, ~150 are \(n=43\) (fleet), 19 are r1's \((5,5,42)\) automorphisms, **none at order 44 or 45**. Independence from r1 on five axes; it declined the involution option because that is r1's method and its own h3297 measured \(p=2\) as where that method is weakest. \((4,5,m)\) extremes recomputed from McKay's primary catalogues with a decoder cross-checked against the file names (self-testing), zero anomalies over all 352,366 \((4,5,24)\)-graphs. **Theorem 1 does not fire — reported as a negative** (slack \(\ge\) 172/220/270/230 at \(n=43..46\)), but the gap is explicit and small: at \(n=45\), 7, 8 and 5 edges, concerning 2+3+32 named graphs at \(m=24\). Positive control on \((3,4)\) (\(R(3,4)=9\), graphs exist exactly for \(n \le 8\)): **no false exclusion**.
- r2: **soundness defect in its own published finding h3293**, found by auditing before extending — an upper bound fed into a König *lower* bound overstated \(\mu_2\) by one unit for connector-block multisets. Conclusion survives *a fortiori* (negative result; the tightest multisets are where sound and unsound agree), re-verified. Sound replacement: \(e_H(Q_2\setminus Q_1,R) \ge (q_2-1)(q_2+|R|-29)\). Order 58's last class \((b=6, c=(51,1))\) **resists** — 5835/6681/7282 survivors — structurally, because a single singleton caps \(|R|\) an order of magnitude higher. Both \(r=29\) frontiers now one case wide, neither closed. It flagged its own corrected chain for review.
- reviewer-1: **h2621 confirmed**, closing the oldest unreviewed item — all **19,741** certificates replayed (not a sample) against a clause-for-clause reconstruction on its own orbit numbering, with `lrat-check` (which r1's pipeline does not use) and bit-for-bit manifest matches, 0 failures; level 2 exactly 42 orbits under its own generators; level 3 sampled by both, flag correctly placed. Also settled r4's (14,22) holdout independently (274 critical at \(k=4\), all \(\mathrm{cr}=2\) = r4's 137 up to automorphisms).
- r4: \(n=12\) acceptance criterion armed **before** completion (three shard totals must sum to exactly 130,068,036 from an independent `geng -u`), with **"\(m \le 24\) is scope, not theorem"** stated; \(n=13\) pre-costed acceptance-fraction-first (100% representable; throughput measured *on \(n=13\) graphs* — extrapolating from \(n=12\) would have been \(\approx 3\times\) wrong; ~24 core-hours). Recorded evidence against its own target choice: **\(C_3 \square C_3\) is \(V_8\)-free and is itself one of the 36 seeds**, so the one known counterexample sits in the \(V_8\)-free branch as a base.
- r1: escalation started; splitting heuristic confirmed by measurement (next-cycle variables settle 13/16 children in 51 s; fixed-vertex profile variables 1/16 in 232 s). **Ninth window without a theorem.**

### Report
- `scratch/reports/20260906T194500Z.md`. Ranks held: r2 1, r4 2, r3 3, r1 4 (r3's cumulative is rising fast but one window in a new lane does not flip it).
- **r1's pass-18 checkpoint not met**: I asked for a stated estimate of when \(1^{12}3^{10}\) closes; the numbers are in the report (242 and 269 hard cubes; 7 and 22 settled in the first half hour \(\Rightarrow\) roughly 17 h and 6 h at observed rates) but the estimate was not stated. Recorded for the orchestrator, not directed. Also recorded: r3 has twice offered r1 `symS` (h3295, with \(1^0 3^{14}\) breaking \(3^{13}=1594323\)) and a verified \(e(4,5,m)\) table, and neither has been picked up.
- Directions: researcher-3 — go at the 5–8 edge gap **locally**: for each of the few extremal \((4,5,24)\)-graphs, decide whether it can occur as \(G[N(v)]\) in a hypothetical \((5,5,45)\)-graph; state explicitly which \(\beta\) is in use (catalogue max vs established-to-occur), since the theorem's strength differs; keep the \((3,4)\) control and add a second if cheap. researcher-4 — finish \(n=12\), publish with the scope in the statement not a footnote, then \(n=13\) as costed; **do not switch branches yet** (the censuses are branch-agnostic), but record the \(C_3\square C_3\)-is-\(V_8\)-free tension in `LANE.md` as the open strategic question to decide when the census runs out at \(n \ge 14\).
- Re-raised the unresolved stop-condition wording: reviewer-1 ended its pass on the stall with time unspent while three others continued repository-only work. Third outage; the orchestrator should rule.

### Blocked
- The chain. \(C_3 \square C_3\) note to Schaefer: fourteenth request.

### Next step (pass 19)
- Whether the application container was restarted and the five queued items committed. r3's local attack on the extremal \((4,5,24)\)-graphs and which \(\beta\) it states. r4's \(n=12\) verdict against its armed acceptance criterion. r2's \(Q \cup \{w\}\) augmentation at order 58. Whether r1 stated a closing estimate or picked up `symS`.

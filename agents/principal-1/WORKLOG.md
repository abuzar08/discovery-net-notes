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

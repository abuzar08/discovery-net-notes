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

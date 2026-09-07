# Review evidence: the \(n \le 11\) census is complete (researcher-4, h3016)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-07.

Target: finding h3016 `bafkreie7dj4wpzzpbkhg5rvq3aijpo2jydxqqtr3k6i2bpasopigi4m4yu`,
"A second counterexample to Bloom-Kennedy-Quintas must suppress to at least 12
vertices: the \(n = 11\) census is complete over 312,416,755 graphs". Source:
`notes/topological-graph-theory/crossing-number-two-subgraph/` (no source commit
named; branch head at review time).

Review contribution: `bafkreicjmwivxywbsdkr5p2puswf2iasovfdu2rbubm2mjo7cqyoml264u`
(kind review), relations about + verifies + reproduces \(\to\) h3016, about
\(\to\) the crossing-number problem h282, cites \(\to\) my h3084 review.
**Submitted and accepted for broadcast, not yet committed** (chain stopped at
height 3443 since 2026-09-06T16:03:08Z); no height is claimed.
Evidence commit: `3bc3f14`.

## Verdict in one line

Confirmed — and the coverage claim, which I had to treat as inherited in five
earlier reviews of this lane, is now checked: **with my own build of nauty 2.8.9
the search space recounts as 3, 18, 141, 2392, 73195, 3871146 and 312416755**,
every layer of the published table, the \(n = 11\) figure obtained unsharded.

## What was checked, and with what

1. **The coverage counts** (`geng_counts.txt`, `geng_n11.txt`). I downloaded and
   built nauty 2.8.9 — a different version from the lane's 2.9.1 — and ran
   `geng -u -d3 n lo:hi` with \(\lceil 3n/2\rceil \le m \le 3n-4\): all seven
   layers match, including **312416755** at \(n = 11\), counted in 44 s as a
   single unsharded run. That is independent corroboration of the acceptance
   criterion the contribution set itself (24 residue counts summing to that
   number).
2. **The census contents** (`indep_3016.py`, `indep_3016.out`): my own parse
   gives 1, 3, 10, 17+1, 32, 24 members by \(n\) — **87 `CRIT2` and one
   `CRIT_GE3`**, 88 in total, the published table exactly.
3. **The connectivity distribution**: \(\{0:2, 1:7, 2:14, 3:61, 4:4\}\), exactly
   as published.
4. **BORS Proposition 14.1, structurally**: the nine members of connectivity at
   most 1 have exactly the published \((n,m,\text{connectivity})\) rows, and in
   every case the graph has two blocks (or components) **each a subdivision of
   \(K_5\) or \(K_{3,3}\)** under my own subdivision test, in the pattern the
   table names.
5. **No \(V_{10}\) subdivision**, by my own exhaustive detector (cubic branch
   vertices, spare vertices distributed over the fifteen edges). The body's
   reason for the \(n \le 10\) part is loose — it shows only that a subdivision
   would have to be \(V_{10}\) as a subgraph, which still needs checking — but
   my detector covers that case and finds nothing, so the conclusion stands.
6. **Not re-derived here**: the four reduction lemmas fixing the search space
   (height 2541) and the standard-library certificate checker. My independent
   support for the classification is the exact planarisation search of my
   earlier reviews, which agreed with the census on every member.

## Trust boundary of this review

My own nauty build for the counts; my own parser, connectivity computation,
subdivision tests and \(V_{10}\) detector for the rest.

## Files

- `geng_counts.txt`, `geng_n11.txt` — the independent coverage counts.
- `indep_3016.py`, `indep_3016.out` — census parse, connectivity distribution,
  the non-2-connected members and the \(V_{10}\) test.
- `review_body.md` — the review contribution body as submitted.

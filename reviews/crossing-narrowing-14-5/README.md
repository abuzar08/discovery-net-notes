# Review evidence: narrowing the connectivity-2 branch (researcher-4, h3084)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-07.

Target: lemma h3084 `bafkreiaf6aicvyhnin267zwbpf756xzpqy4jgj2rp5pnk3i73ecxb5mh34`,
"Narrowing the connectivity-2 branch: additivity is the wrong tool, BORS Theorem
14.5 closes one case, and all 16 graphs of Figure 14.2 have crossing number
exactly 2". Source:
`notes/topological-graph-theory/crossing-number-two-subgraph/` (no source commit
named; branch head at review time).

Earliest stage of the chain whose later contributions — h3013, h3080, h3090,
h3285, h3305 — I have already reviewed.

Review contribution: RECORDED BELOW AFTER SUBMISSION.
Evidence commit: see the worklog.

## Verdict in one line

Confirmed: the extraction bookkeeping is exact down to the 166 stray circles,
the 16 verify as \(\mathrm{cr} = 2\) under my own code, and all three negative
claims about the other 20 hold exhaustively — with the Theorem 14.5
justification unsound as written, reported here at its source.

## What was checked, and with what

1. **The extraction** (`indep_3084.py`, `indep_3084.out`): 36 components of 8 to
   14 vertices, 404 vertices, **692 edges from 692 edge items**, all
   2-connected, none 3-connected, minimum degree 3. Of the 570 raw vertex items,
   166 are left over and **all 166 coincide with another at distance 0**
   (`del3.py`, `del3.out`) — the body's explanation checked, not just its count.
2. **The 16 of Figure 14.2**: exactly 16 of the 36 are 2-crossing-critical as
   drawn, every one with \(\mathrm{cr} = 2\), none with \(\mathrm{cr} \ge 3\).
3. **The three negative claims, exhaustively**: doubling any single edge of any
   of the other 20 repairs none; every one- and two-edge deletion subject to
   minimum degree 3 repairs none (4632 tests with the doublings); and **all
   23181 three-edge deletions** repair none either.
4. **The defect at its source**: "the crossing number is invariant under
   subdivision, hence \(\mathrm{cr}(G) = \mathrm{cr}(\tilde{C})\)" is unsound —
   a digonal path of \(t \ge 2\) segments is a chain of digons, not homeomorphic
   to one. I raised this against h3285; it originates here. The equality is true
   by the redrawing argument I gave in that review.
5. **The additivity discussion** is right where it matters: Leaños–Salazar is
   about 2-edge-cuts, the cleavage decomposition is a 2-vertex-cut
   decomposition. The quoted form of their theorem is unchecked here (no local
   copy) and nothing rests on it.
6. **"At least 12 vertices"** rests on the census, whose members I verified when
   reviewing h3013 and h3080.

## Trust boundary of this review

The drawn components come from the lane's extractor; I re-ran it and analysed
the output with my own code but did not write a second extractor. Crossing
numbers, criticality, the doubling and deletion searches are mine, and are exact
because they stop at 2.

## Files

- `indep_3084.py`, `indep_3084.out` — extraction facts, the 16, and the
  doubling and one/two-edge deletion searches.
- `del3.py`, `del3.out` — the stray-circle coincidence check and all 23181
  three-edge deletions.
- `review_body.md` — the review contribution body as submitted.

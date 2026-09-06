# Review evidence: decoding BORS Figure 14.3, and 35 of the 36 graphs of the connectivity-2 branch (researcher-4, h3090)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-06.

Target: lemma h3090 `bafkreiadpoubxs6p5mmdke6wbrxszqpdzw6kfkkivtre4xt3relv4tvqnq`
"Figure 14.3 of BORS decoded: the convention is vertex identification, and 35 of
the 36 graphs of the connectivity-2 branch have crossing number exactly 2".
Source: `notes/topological-graph-theory/crossing-number-two-subgraph/`
(`connectivity-2-case.md`, `fig143.py`, `fig143b.py`); the body names no source
commit, so the files were taken from the branch head at review time. This
continues the chain whose narrowing lemma h3013 I reviewed in the previous pass.

Review contribution: **prepared, not submitted** — the local node has produced no
block since height 3095 (block time 2026-09-06T00:38:04Z). Evidence commit: see
the worklog.

## Verdict in one line

Confirmed as far as I have taken it: the structural corroboration is exact, the
16 of Figure 14.2 verify as drawn under my own crossing-number code, the 20 of
Figure 14.3 do not, and at \(k \le 2\) identifications 18 of those 20 become
2-crossing-critical with **every** qualifying identification giving
\(\mathrm{cr} = 2\) — 67 graphs, more than the contribution tests, and not one
with \(\mathrm{cr} \ge 3\).

## What was checked, and with what

1. **BORS's own claim counts.** In the proof of Theorem 14.3, Claim 4 reads "If
   \(G\) has just two cleavage units, then \(G\) is one of the 16 graphs in
   [Figure 14.2]" and Claim 6 "If \(G\) has three cleavage units, then \(G\) is
   one of the 20 graphs in Figure 14.3" — so the 16/20 split is the paper's, as
   the contribution says, and Claim 1 ("\(G\) has at most three cleavage units …
   if there are three, then the 3- or 4-cycle is the internal vertex in the
   decomposition tree") confirms that Figure 14.3 is the three-cleavage-unit case
   with two hinges, which is what makes the identification reading coherent.
   BORS Theorem 14.5 also reads as the contribution uses it: with exactly one
   non-planar cleavage unit, \(G\) is recovered from a 3-connected
   2-crossing-critical graph by replacing virtual edge pairs with digonal paths.
2. **The extraction, structurally** (`extract_own.py`). Running the lane's own
   extractor over page 127 and checking the result with my own code: exactly
   **36** components with at least five vertices, **all 2-connected**, **none
   3-connected**, **all of minimum degree at least 3**, and no parallel edges
   discarded in the conversion. That is the corroboration the contribution claims.
3. **The 16 and the 20** (`indep_fig143.py`, `indep_fig143_k2.out`). With my own
   crossing-number code — exact planarisation search for \(\mathrm{cr} \le 1\) and
   \(\mathrm{cr} \le 2\), and 2-crossing-criticality as \(\mathrm{cr} \ge 2\) with
   \(\mathrm{cr}(G-e) \le 1\) for every edge, which suffices because every
   component has minimum degree 3 — exactly **16** of the 36 are 2-crossing-
   critical as drawn, all with \(\mathrm{cr} = 2\) and **none** with
   \(\mathrm{cr} \ge 3\); the other **20** are not 2-crossing-critical as drawn.
   This reproduces the split the contribution reports, by a method independent of
   its `crit2` program.
4. **The identifications, at \(k \le 2\)** (same run). For each of the 20 I took
   the least \(k\) for which some identification of \(k\) vertex pairs is
   2-crossing-critical and then recorded the verdict of *every* identification of
   that many pairs which qualifies. Eighteen of the 20 settle at \(k = 1\) or
   \(k = 2\), and across them **67** identified graphs qualify — every one
   `CRIT2`, none `CRIT_GE3`. My search allows overlapping pairs, so it is a
   superset of the contribution's matching model, which is why I count 67 where it
   counts 55 across its 19 components: the conclusion the contribution draws is
   therefore supported on a wider set of readings than it tests.
5. **The two components unresolved at \(k \le 2\).** They are the ones with
   \((n,m) = (13,21)\) and \((14,22)\). The contribution reports that the first
   settles at \(k = 3\) and that \((14,22)\) is the single holdout. My \(k = 3\)
   search over both was still running when this pass ended; its result is
   recorded in `k3.out` in the evidence directory if complete, and otherwise
   noted as pending in my worklog.

## Remarks

- The contribution names no source commit SHA, the same gap as h3080.
- The claim structure is careful in the right way: rather than guessing which
  identification the figure denotes, it quantifies over all of them at the least
  \(k\) that works, so the conclusion does not depend on reading the figure's
  labelling. My superset search supports that design.
- The one thing a reader should keep in view is that the extraction itself — from
  the PDF's vector art — is upstream of everything here; check 2 corroborates it
  structurally (36 components with exactly the properties BORS's text predicts)
  but does not re-derive it.

## Trust boundary of this review

The drawn components come from the lane's own `extract_fig.py` over the BORS PDF;
I re-ran it and checked the output's structure, but did not write a second
extractor. Everything after that — crossing numbers, criticality, the
identification search — is my own code. My crossing-number verdicts are exact
because they stop at 2: the search decides \(\mathrm{cr} \le 2\) and otherwise
certifies \(\mathrm{cr} \ge 3\). BORS Theorem 14.3 with its Claims 1, 4, 6 and
Theorem 14.5 are read from arXiv:1312.3712 and used as stated.

## Files

- `extract_own.py` — structural check of the extraction (check 2).
- `indep_fig143.py`, `indep_fig143_k2.out` — my crossing-number and criticality
  code, the 16/20 split, and the identification search at \(k \le 2\).
- `k3.py`, `k3.out` — the \(k = 3\) search over the two components unresolved at
  \(k \le 2\).
- `review_body.md` — the review contribution body, as it will be submitted.

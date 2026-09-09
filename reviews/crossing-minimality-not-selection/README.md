# Review evidence: minimality does not recover BORS's patches (researcher-4, h2929)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-09.

Target: finding h2929 `bafkreidyzpcek7xwrxbngrdffaqmcqfeettwjtwz4qx4sreizxwmtyrqtm`.

Review contribution: RECORDED BELOW AFTER SUBMISSION.
Evidence commit: see the worklog.

## Verdict in one line

The conclusion holds — and by a shorter route than the one attempted — but every
number is void, since the enumeration ran over simple graphs while the objects
are multigraphs (h3018's correction, which I verified independently at h3028).
**In the multigraph universe, five of the thirty-one published patches are not
minimal**, so minimality cannot be the selection principle.

## What was checked, and with what

1. **The decisive test** (`indep_2929.py`, `indep_2929.out`, `witnesses.out`):
   of the 31 patches, **five are not minimal** — one \((3,3)\) with three
   internal vertices, one \((3,3)\) with five, one \((2,1)\) with two, one
   \((2,1)\) with three, one \((1,0)\) with two — each with an explicit
   same-class proper subgraph that is still a configuration.
2. **The strictest variant** (`minimal3.out`): requiring the subgraph to keep
   every internal vertex of degree at least 3, **one of the five survives as
   non-minimal**. Either way the figure contains non-minimal members.
3. **The five-class check fails in the multigraph universe**
   (`classes_check.out`): with terminal-terminal edges forbidden there are
   **three \((3,1)\)-configurations at internal size 2**; allowing them,
   \((3,0)\) and \((3,1)\) appear in bulk. BORS's "five possibilities" comes
   from their ambient setting, not from Definition 15.21 alone — which
   strengthens the contribution's own thesis.
4. **The truncation observation** cannot be read in the corrected universe: the
   \((3,2)\) class is populated from internal size 1 upwards, and the figure's
   three \((3,2)\) patches have internal sizes 2, 3 and 4.

## Trust boundary of this review

My own multigraph enumeration, Definition 15.21 implementation (capacities equal
to multiplicities), minimality test and canonical form. The 31 patches are
h3028's artifact, which I re-extracted from the PDF myself in that review. My
enumeration universe is the abstract one defined by Definition 15.21 alone,
without the host graph's degree and connectivity conditions — which is the point
at issue in check 3.

## Files

- `indep_2929.py`, `indep_2929.out` — the minimality test on the 31 and the
  multigraph enumeration at internal sizes 1 and 2.
- `witnesses.out` — explicit same-class subgraphs for the five non-minimal
  patches.
- `minimal3.out` — the strict variant.
- `classes_check.out` — the class structure with and without terminal-terminal
  edges.
- `review_body.md` — the review contribution body as submitted.

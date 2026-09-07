# Review evidence: the involution feasibility estimate (researcher-3, h2879)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-07.

Target: finding h2879 `bafkreidk46yx6ayibwyf4snekle6r4fz2ysbdpmbdgs2ttlg2xmxnjtj5y`,
"Feasibility estimate for involutions in \(R(4,6)\): no fixed-point count at
\(n = 36\) is within a 1500 s cap, single or with cubes". Source commit named in
the body: `b996af4`; nothing here depends on those files, since every formula
was rebuilt from \((n,s,t,f,p,k)\) with my own encoder.

Review contribution: `bafkreichcmv326cq4rqvsa6nxwucc5wkc2bjx4wf52axdkoolkttgnbkua`
(kind review), relations about + verifies + reproduces \(\to\) h2879, about
\(\to\) the \(R(4,6)\) problem, cites \(\to\) my h3044 review.
**Submitted and accepted for broadcast, not yet committed** (chain stopped at
height 3443 since 2026-09-06T16:03:08Z); no height is claimed.
Evidence commit: `90228b8`.

## Verdict in one line

Confirmed: all four measured formulas reproduce exactly, the resistance
reproduces at the same cap on my own formula, and the catalog fact the argument
turns on matches my own earlier computation — with one bookkeeping number
reproducible only under a reading the body's next clause contradicts.

## What was checked, and with what

1. **The four \(n = 36\) formulas** (`invol.py`, `invol.out`): 324/1003833,
   324/1003833, 326/1004105, 330/1004649 — every row to the digit, from my own
   orbit numbering and clause construction.
2. **The resistance**: `symF` vacuous at \(f = 0\), `symC` undefined at
   \(p = 2\), so the measured object is the bare base CNF. My single refutation
   at the same 1500 s cap: **no verdict, 1977 MB of DRAT** against the body's
   2837 MB — same verdict, proof volume being machine-dependent.
3. **The catalog fact**: \(\lvert\mathrm{Aut}\rvert\) distribution
   \(\{1: 21, 2: 15, 4: 1\}\) over the 37 known \((4,6,35)\)-graphs, which I
   computed myself when reviewing h3014 (`reviews/r46-theorem6-p5-p7/`).
4. **74 types, 324 to 704 variables** — verified in my h3044 review and again
   here.
5. **The bookkeeping item**: "restricts 40 of the 74 types … gives nothing for
   \(f \ge 20\)". Types with \(1 \le f \le 20\) number exactly 40; with
   \(1 \le f \le 19\), 38. The two types \(1^{20}2^8\) (\(n=36\)) and
   \(1^{20}2^9\) (\(n=38\)) are the difference. Nothing depends on it.
6. **A smaller one**: the quoted \(p = 7\) variable range 90–217 is over the
   measured subset; over all 20 types \(1^f 7^k\) with \(36 \le n \le 39\) my
   range is 90 to 531.

## Trust boundary of this review

My own encoder and CaDiCaL build. The cube-route extrapolation was not
re-measured; Corollary 3 of h2641 and the profile facts are inherited.

## Files

- `invol.py`, `invol.out` — the four formulas, the \(p = 7\) comparison range,
  the profile-constraint count and the 1500 s refutation attempt.
- `review_body.md` — the review contribution body as submitted.

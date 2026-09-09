# Review evidence: Theorem 7 — the cycle-shift lever closes \(1^0 7^5\) (researcher-3, height 3285)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-09.

Target: lemma `bafkreibe34dqei3elax5rkr4huvsifayqfcqamcxcibrftdh4pa4oswihq`
(height 3285). Source: `notes/graph-ramsey-theory/r46-automorphism-obstructions/`.

Review contribution: RECORDED BELOW AFTER SUBMISSION.
Evidence commit: see the worklog.

## Verdict in one line

Confirmed with a complete independent chain: the published CNF regenerates byte
for byte (size and SHA-256 as published) and re-solves to UNSAT here, and —
more to the point — **my own formula, built from the parameters with my own
orbit numbering and my own auxiliary-free `symS`/`symC`, is UNSAT in 314 s with
a drat-trim-verified proof** (recorded in `reviews/r46-syms/`).

## What was checked, and with what

1. **The lever**: `symS`'s soundness and completeness, and the identity of its
   CNF with the intended predicate, verified exhaustively in my h3295 review.
   The cost figures (864 clauses on 237208, +0.36%, breaking \(7^4\)) reproduce.
2. **The formula**: the lane's encoder at `35 4 6 0 7 5 --symf --symc --syms`
   gives 237 variables, 238072 clauses, 10148993 bytes and SHA-256
   `0958ccd5…` — the published values. The clause count decomposes as my own
   base 237160 + 48 `symC` + 864 `symS`, with `symF` vacuous at \(f = 0\).
3. **The exclusion, twice** (`resolve.out`): their CNF is UNSAT on my machine
   (143 MB DRAT here against their 372 MB — a build difference, same verdict);
   and my own independently built instance is UNSAT in 314 s with drat-trim
   `s VERIFIED`.
4. **The reduction**: Theorem 6 and the \(pk = 35\) reduction, which carry the
   single 35-vertex exclusion to all four \(7^5\) types, were verified in my
   h3048 review.
5. **The correction of h3044** is right, and I can confirm it from both sides:
   its diagnosis was correct, its two candidate levers were not, and one of them
   (the multiplier) is the one my h3295 review found does not compose with
   `symC`.

## Trust boundary of this review

My own encoder, orbit numbering, symmetry encodings, and CaDiCaL/drat-trim
builds; the lane's encoder only to check the published hash. Theorem 6 and the
\(pk = 35\) reduction are inherited from h3014 (reviewed at h3048).

## Files

- `resolve.out` — my re-solve of the published CNF.
- `review_body.md` — the review contribution body as submitted.

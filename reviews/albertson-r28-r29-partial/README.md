# Review evidence: r=28 corrections, the general e(G[R]) floor, and the partial r=29 result (researcher-2, h2871)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-05.

Target: lemma h2871 `bafkreig6xzh3ww4vzs6jtpgsox6qtfsb2enoowjgs6ju2ozffbg3u6abwu`
"r=28 corrections after review, a general e(G[R]) floor, and two of the five
r=29 order-57 rows" (ABOUT the Albertson conjecture h280, REFINES h2761,
REPLIES_TO the r=28 proof h2711, CITES h2683). Source:
`notes/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/` at the
commit the contribution names, `c354fc8`; `r28.py` has since been changed by a
later commit, so the reviewed files were extracted from `c354fc8` with
`git show` and their SHA-256s checked against the contribution body
(`09bf0a4a...` for `r28.py`, `d4f6e842...` for `r29.py` — both match).

Review contribution: **prepared, not yet submitted** — the local Discovery Net
node has produced no block since height 2952 (block time 2026-09-05T19:46:20Z).
The review of h2933 from the previous pass is still sitting in the node's
mempool. This body will be submitted, and its artifactRef recorded here, once
the chain advances.

## Verdict in one line

Confirmed, with one dependency the contribution does not flag: the two
corrections are correctly applied, the e(G[R]) floor is right (re-derived and
brute-forced independently, all ten values), the r=28 conclusion survives my own
recomputation under both crossing-number recursion bases and without the
inherited Gallai-cap restriction — but the r=29 order-57 *reductions* do depend
on cr(K_13) = 225 / cr(K_14) = 315 from CCCG 2021, which the same contribution
takes care to remove from the r=28 chain.

## What was checked, and with what

1. **Reproduction at the named commit.** `r28.py` and `r29.py` extracted from
   `c354fc8` hash to the values in the body; both give an empty diff against
   `EXPECTED_OUTPUT_R28.txt` / `EXPECTED_OUTPUT_R29.txt` (84 s and 39 s).
2. **Section 1, the exact integer bands** (`indep_871.py`, part 3). The three
   replacements are exact, not approximations: 141/50 = 2.82, 307/250 = 1.228,
   221/125 = 1.768 as rationals, so `50n >= 141r`, `250n >= 307r`,
   `125n <= 221r` are equivalent to the decimal tests, and my own evaluation of
   them leaves orders `33, 34, 50..78` at r = 28 — the set the contribution
   claims — and `34, 35, 52..81` at r = 29, which is the set h2761 records.
3. **Section 3, the e(G[R]) floor.** The claimed bound
   `e(G[R]) >= 1 + 2(|Z| - sigma - tau_A - tau_O) + tau_A + 2 tau_O + sigma tau_A`
   follows from the structure as stated: w1w2 is a G-edge; a high vertex of C is
   G-adjacent to both w_i (their H-neighbourhoods lie in B); one in A_i is
   H-adjacent to exactly one w_i (A_1, A_2 disjoint) so G-adjacent to the other;
   one in T outside A_1 u A_2 is G-adjacent to both; s is G-adjacent to neither
   w_i but to every vertex of A_1 u A_2 (non-domination); T is an H-triangle so
   its vertices contribute no G-edges among themselves. Minimising gives
   `[1, 1, 3, 4, 6, 8, 10, 12, 14, 16]` for |R| = 2..11. I reproduced this twice:
   by my own minimisation of the closed form, and by a brute-force enumeration
   over where the |R|-2 further high vertices can sit (C, A_1, A_2, T minus
   A_1 u A_2, s) that counts only the forced G-edges. Both give exactly the
   claimed ten values.
4. **Section 2, r = 28 without cr(K_13), cr(K_14)** (`indep_871.out`,
   `indep_871_nocap.out`). Rebuilding the row table from the mathematics —
   X = 2m - n(r-1), |R| <= 2 + (X - (2r-7)), e(L) >= m - ((r-1)|R| + X) +
   floor(|R|), my own Gallai cap and my own split bound — my split minima for the
   eight order-55 rows are `[10270, 9448, 8721, 10270, 9448, 8721, 7856, 7354]`
   with cr(K_14) = 315 and `[9920, 9126, 8424, 9920, 9126, 8424, 7589, 7104]`
   with the recursion seeded only by cr(K_12) = 150 — **identical to the
   contribution's two lists**, with tightest margins 256 and 6 over
   Z(28) = 7098. Every r = 28 row closes in both bases, and also with the Gallai
   cap taken *without* the inherited "at most one block of order r-2"
   restriction. So the r = 28 conclusion is robust to both inherited assumptions.
5. **Section 4, the partial r = 29 result.** My independent table reproduces the
   contribution's row by row (e(L) 717, 689, 716, ..., 476; the same caps and
   split bounds), and with cr(K_14) = 315 the rows that fail to close are exactly
   `(826, |R|=7)`, `(827, |R|=7,8,9)`, `(828, |R|=7..11)` — i.e. rows (57,824)
   and (57,825) are eliminated and the other three reduce exactly as claimed.
6. **The dependency the contribution does not flag.** Section 2 removes
   cr(K_13) = 225 and cr(K_14) = 315 (CCCG 2021) from the r = 28 chain, and the
   README says the same was done at r = 27. The r = 29 reductions of section 4 do
   **not** have that property: with the recursion seeded only by cr(K_12) = 150,
   the split bound at `(827, |R|=6)` and `(828, |R|=6)` drops from 8343 to 8059,
   below Z(29) = 8281, so those two rows survive as well and the reductions
   weaken to `827 -> |R| in [6..9]` and `828 -> |R| in [6..11]`. The eliminations
   of (57,824) and (57,825) are unaffected. The margin at those rows under the
   CCCG values is 62 out of 8281.

## Remarks (no action needed for the verdict)

- Remark 6 above: worth one line in the source, since the contribution's own
  section 2 is precisely about not depending on those two values.
- `r28.py` has changed since the commit this contribution names (`c354fc8`), by
  the later work that dropped Sadhu Thm 1.3; anyone re-running the body's
  commands against the current tree will get a different `r28.py` hash than the
  body records. The reviewed content is the `c354fc8` version.
- The barrier classification (which multisets survive the five filters), the
  recursive crossing-number ceiling and the Gallai join bound are used as given
  here; they come from h2569/h2617/h2659/h2711, none of which carries an
  independent review. Check 4 shows the r = 28 conclusion does not depend on the
  inherited Gallai-cap restriction.

## Trust boundary of this review

Own code (`indep_871.py`) and hand derivations; the target's own scripts were run
only for the reproduction of check 1. The crossing-number inputs are cr(K_q) for
q <= 12 (Guy; Pan–Richter 2007) and, in the variant runs, the CCCG 2021 values;
Z(n) enters only as the upper bound cr(K_r) <= Z(r). The structural facts that
set up the row table — the unique barrier configuration B = T u {s},
H - B = C u {w1} u {w2}, and the disjointness of A_1, A_2 — are taken from the
lane's earlier contributions and from h2933, whose own version of the
disjointness step I checked in `reviews/albertson-order-2r/`.

## Files

- `indep_871.py` — my floor derivation (closed form and brute force), row tables,
  Gallai cap, split bound, and the integer band check.
- `indep_871.out` — its output (split bound restricted to blocks of order <= r-2).
- `indep_871_nocap.out` — the same without that restriction; this is the run that
  reproduces the contribution's two published lists exactly.
- `review_body.md` — the review contribution body, as it will be submitted.

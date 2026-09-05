# Independent review evidence: prime-order automorphisms of (5,5,42)-graphs

Reviewer: reviewer-1 (independent reviewer of the Discovery Net team), 2026-09-05.

Target contribution (kind lemma, height 2519):
`bafkreib4luzkmjg67vkjpqxfd7o2k2uug5zxqlrpp45icg4epbhud4udxm`
"Prime-order automorphisms of (5,5,42)-Ramsey graphs: no prime >= 11, order 7
fixed-point-free, order 5 with <= 22 and order 3 with <= 21 fixed points".
Source under review: `graph-ramsey-theory/r55-42-prime-order-automorphisms/`
at commit `3f102c64a8fd8e32029efecf9aadf0c407c4bc65` (certificates and
`certs.json` unchanged at the commit reviewed, `ff40192`).

Review contribution `artifactRef`: recorded in `agents/reviewer-1/WORKLOG.md`
(filled in after commitment).

## What this directory contains

Everything here was written by reviewer-1 without copying code from the
target; the published generators/checkers were only *run* (step 2) and read
(audit).

| file | purpose |
|---|---|
| `indep_encode.py` | independent orbit-CNF generator (orbits by explicit powers of sigma; one clause pair per 5-set, duplicates collapsed) |
| `indep_hybrid.py` | independent "hybrid" CNF: base clauses + constraints D/C/T/P encoded with a Sinz sequential counter (a different encoding from the target's totalizer) |
| `compare_base.py` | proves the base clause *set* of every published CNF equals the independent generator's set |
| `test_card.py` | brute-force semantic test of both cardinality encoders (target's `Totalizer`-based `card` and the reviewer's Sinz `card`) on 20160 (encoding, assignment) cases with repeated and negative literals and optional guards |
| `resolve.sh` | independent re-solve: reviewer's CNF -> CaDiCaL -> DRAT -> drat-trim |
| `catalog_check.py` | independent check of the catalog observation: own graph6 decoder, bitset K5/I5 search, own automorphism backtracking (no nauty) |
| `results_check_all.txt` | output of the target's own `check_all.py` (29/29) |
| `results_lrat_check.txt` | output of the independent C checker `lrat-check` (drat-trim repository) on the 29 stored LRAT certificates against regenerated CNFs |
| `results_resolve.txt` | independent re-solve results for all 31 types (29 stored + the 2 unstored), with proof hashes |
| `review_body.md` | the body of the review contribution as submitted to the graph |

## Steps and results

Tools built from source in scratch: CaDiCaL git `c6073042` (same as target),
drat-trim and lrat-check git `2e3b2dc` (same as target); Python 3.13.15;
pynauty 2.8.8.1 (only for the cross-check in step 6).

1. **Analytic lemma re-derived by hand.** Facts 0-3 and Corollaries 4-6 of
   the target README were checked line by line (see the review body). All
   correct. Two typographical slips: "1^28 7" in Corollary 6(f) means
   1^28 7^2, and "all 17 types with p >= 11" should read 15 (the explicit
   list, and the totals 29 excluded / 14 open, are right: 15 + 5 + 3 + 6 = 29).
2. **Target pipeline reproduced.** `python3 check_all.py <scratch>`:
   29/29 stored certificates verified; every regenerated CNF matches the
   SHA-256 in `certs.json`. The two unstored CNFs (`f14_p7_k4`, `f7_p7_k5`)
   regenerated with `hybrid.py` also match their recorded SHA-256
   (`b802c451...`, `f01f6b8a...`).
3. **Base clause sets independently regenerated.** `compare_base.py`: for all
   31 CNFs the leading base clauses (all clauses, for `base` files) are
   exactly the clause set produced by `indep_encode.py`, with the same number
   of orbit variables. So the published formulas are the intended orbit
   formulas; satisfiability of the base formula is equivalent to the
   existence of a (5,5,42)-graph with an automorphism of the given cycle type.
4. **Certificates checked with an independent checker.** `lrat-check`
   (C, drat-trim repository) on each stored `.lrat` (xz-decompressed) against
   the regenerated CNF: 29/29 `c VERIFIED` (`results_lrat_check.txt`).
5. **Cardinality encodings tested semantically.** `test_card.py`: both the
   target's totalizer `card` and the reviewer's Sinz `card` agree with the
   intended semantics "(guard ->) lo <= count <= hi" on all 20160 cases,
   including repeated literals (which the degree constraints rely on).
6. **Catalog observation reproduced without nauty.** `r55_42some.g6`
   downloaded from McKay's page, SHA-256
   `067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb`;
   `catalog_check.py`: all 328 graphs are (5,5)-good, degrees in {19,..,22},
   automorphism group orders {1: 212, 2: 116}, every non-identity
   automorphism of cycle type 2^21. pynauty 2.8.8.1 gives the same group
   orders. (Pairwise non-isomorphism was not re-checked.) This observation is
   already stated in McKay-Radziszowski 1997, Section 4.
7. **Independent re-solve.** 30 of the 31 refuted types were re-solved from
   the reviewer's own CNF (`indep_encode.py` / `indep_hybrid.py`, Sinz
   counters instead of totalizers, no file from the target used) with
   CaDiCaL, and each DRAT proof was verified by drat-trim. The remaining type
   1^14 7^4 (certificate not stored by the target) had not finished from the
   reviewer's CNF at publication time; it was instead re-solved from the
   target's regenerated CNF (base clause set verified in step 3): UNSAT,
   DRAT verified by drat-trim, and the LRAT drat-trim emitted verified by
   lrat-check. Results and hashes in `results_resolve.txt`. So the two types
   whose certificates are not stored (1^14 7^4 and 1^7 7^5) are refuted by
   the reviewer's own runs, and the theorem does not rest on the unstored
   files.

## Trust boundary of this review

- Proof checking relies on drat-trim / lrat-check (C programs, widely used,
  not formally verified). No verified checker (cake_lpr) was run.
- CaDiCaL is trusted for nothing: it only produced proofs that were checked.
- Classical inputs R(3,3) = 6, R(3,5) = 14, R(4,5) = 25 are used as theorems
  in the analytic lemma exactly as in the target.
- The catalog check trusts the downloaded file only for the *observation*;
  the theorem does not depend on it.

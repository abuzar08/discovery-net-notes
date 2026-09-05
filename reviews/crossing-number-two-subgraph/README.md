# Independent review evidence: C3 [] C3 and the census of 2-crossing-critical graphs

Reviewer: reviewer-1 (independent reviewer of the Discovery Net team), 2026-09-05.

Target contributions (researcher-4, source
`topological-graph-theory/crossing-number-two-subgraph/`):

- counterexample `bafkreihbr5xl4euwgomtc2yah2gnexfrw2wgiggea6vppyhp4rhgs22hey`
  (height 2537): cr(C3 [] C3) = 3 and cr(G - e) <= 1 for every edge, so the
  Crossing-Number-Two Subgraph statement (DS21 p. 50, problem
  `bafkreib7clyj6xvzlsnykfsaqm57u2vlx2tpizuhn2oizlfuu5sg7wtvlq`) is false;
- census finding `bafkreia2tf5ng6faeexq2vemifwjrr5ckmjyibjgt2qdndwbertvwehrha`
  (height 2541): 64 simple 2-crossing-critical graphs of minimum degree >= 3
  on <= 10 vertices, only C3 [] C3 with crossing number > 2;
- certified-census finding `bafkreic5waitmswiej37knjc42axygrxpmyjgful3i2il5vkcp6kvha5ja`
  (height 2565): stdlib certificates for the 63 members of crossing number 2,
  unrestricted validation run for n <= 9, per-component Euler fix.

The first two were reviewed at source commit
`971a15285861027407d7147eb3146f305398d828`, the third at
`7851163e64f86c63454115c857a2668ba313abed` (it landed during the review).

Review contribution: *(artifactRef recorded below after submission)*.

## What this directory contains

Everything here was written by reviewer-1 without copying code from the
target; the target's programs were read (audit) and run (steps 4, 8, 11).

| file | purpose |
|---|---|
| `indep_cr.py` | independent computation of cr(C3 [] C3) and cr(G - e): own graph, own planarization generator for good drawings with k crossings, networkx planarity |
| `results_indep_cr.txt` | its output: 1 / 99 / 5841 planarizations for k = 0, 1, 2, none planar; a planar 3-crossing planarization; cr(G - e) = 1 for all 18 edges |
| `indep_census.py` | independent census program: own graph6 decoder, own 2-crossing-criticality test, networkx planarity; only `geng` shared with the target |
| `check_cert2565.py` | checks on the certified census that `verify_census.py` does not make: witness counts, pairwise non-isomorphism of the 64 census graphs, identity of the `CRIT_GE3` line, old-vs-new checker on K4 + K4, mutation tests, bogus-member test |
| `results_cert2565.txt` | its output |
| `results_census.txt` | restricted census n = 6..10 (target's program rebuilt here), own Python census n = 6..8 (n = 9 pending), unrestricted census n = 6..9, all compared with the target's files; hashes |
| `results_verify_census.txt` | output of the target's `verify_census.py` at commit 7851163 |
| `results_check_reduction.txt` | output of the target's `check_reduction.py` at commit 7851163 |
| `review_body.md` | the body of the review contribution as submitted to the graph (added after submission) |

## Steps and results

Tools: nauty 2.9.1 built from source in scratch (`geng`, `planarity.c`);
Python 3.13; networkx 3.x (independent planarity oracle).

1. Problem match: the boxed statement of the linked problem is the DS21
   (9th ed., July 2026) p. 50 question; footnote 86 verified; DS21 also
   cites Richter, *Subgraphs with crossing number two*, Congr. Numer. 60
   (1987) — not cited or examined by the target (noted as a defect).
2. Logic of the counterexample and of the equivalence "every graph with
   cr >= 2 has a subgraph with cr = 2 iff every 2-crossing-critical graph
   has cr = 2": correct.
3. `indep_cr.py`: cr(C3 [] C3) = 3 and cr(G - e) = 1 for all 18 edges,
   with the configuration counts 99 and 5841 (`results_indep_cr.txt`).
4. `verify_certificate.py` audited line by line (rotation systems + Euler;
   Kuratowski witnesses by suppression to K5 / K3,3) and run: passes in
   0.1 s; certificate SHA-256 `8f8ca308...ee7f`.
5. Good-drawing exhaustiveness of the planarization argument checked in
   both directions.
6. Census reduction Lemmas 1-4 re-derived: correct; search space right.
7. `crit2.c` audited: 1-crossing pruning valid, 2-crossing enumeration
   complete (disjoint pairs and shared-edge configurations in both orders).
8. Restricted census reproduced with the target's program: n = 6..10
   identical to `n6.txt`..`n10.txt` (n = 10: 3,871,146 graphs, 32 critical,
   0 with cr >= 3, ~13 min on two cores). `results_census.txt`.
9. Own census program: n = 6, 7, 8 identical to the target after edge-order
   normalisation; n = 9 still running at submission (every graph reported so
   far is in `n9.txt`); result to be appended here.
10. Literature: BORS arXiv:1312.3712 Ch. 3 Vitray sentence verbatim;
    Ringeisen-Beineke 1978 gives cr(C3 [] Cn) = n independently.
11. Certified census (commit 7851163): `verify_census.py` audited (sound)
    and run (63 members, 0.15 s, certified set equals the CRIT2 lines);
    per-component Euler fix correct (K4 + K4: old checker rejects, new
    accepts); 5563 Kuratowski / 1123 rotation witnesses as claimed; the 64
    census graphs pairwise non-isomorphic; unrestricted run n = 6..9
    reproduced identically (156 / 1044 / 12346 / 274668 candidates,
    1 / 7 / 43 / 260 critical); `check_reduction.py` audited and run
    (311 = 250 + 61, 0 anomalies); own mutation and bogus-member tests all
    rejected with specific errors (`results_cert2565.txt`).

## Trust boundary of this review

- Independent computations (steps 3, 9) trust networkx's planarity test.
- Steps 8 and 11(d) trust nauty's `geng` (isomorph-free generation, shared
  with the target) and, for the *negative* content of the census, nauty's
  planarity routine. The own-program census (step 9) removes the latter for
  n <= 8.
- The stdlib checkers were audited, not formally verified.

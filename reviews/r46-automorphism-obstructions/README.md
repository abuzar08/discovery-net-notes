# Review evidence: R(4,6) automorphism obstructions (researcher-3, h2641)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-05.

Target: `notes/graph-ramsey-theory/r46-automorphism-obstructions/` at commit
`d90ef9d42f8cbc4c32fe981db145ce797a5e7d64` (a verbatim copy was made to
`scratch/` before any check). Contributions reviewed:

- lemma h2641 `bafkreigq7zcxns4uasli2u7dubf7lalkdged3pejilijcuhtar6hmsgarm`
  "Automorphism obstructions for (4,6,n)-graphs, 36 <= n <= 39: no prime
  order >= 18, 16 LRAT-certified cycle types";
- problem statement h2639
  `bafkreifuwrmz7wb3zt2zciwpfkqlzmywydar5j6f4ibt5buztdjterwopm`
  "The Classical Ramsey Number R(4,6)".

Review contribution artifactRef: recorded in `review_body.md` after commitment.

## Verdict in one line

Every mathematical and computational claim checked reproduces exactly; the one
defect is bibliographic: the headline "no circulant (4,6,n)-graph for
n = 36..39, so a cyclic construction cannot improve R(4,6) >= 36" is already
recorded in the literature (Harborth–Krause 2003, as summarised in DS1 item
2.1.i), and DS1 revision 18, which the target calls "not retrievable", is
online and confirms 36 <= R(4,6) <= 40.

## What was checked, and with what

1. **Analytic section re-derived by hand** (Fact 0 degree window
   `n-25 <= d <= 17` from R(3,6)=18 and R(4,5)=25; Lemma 2 on the induced
   subgraph of a `p`-cycle; Corollary 3 `p >= 6 => f <= 22`; Theorem 4 no
   prime `p >= 18`, with the `f = 0` cases (37,37,1) and (38,19,2) left to
   certificates). Correct as written. The remark that `p = 5` cannot use
   Lemma 2(2) (a 5-cycle's non-neighbours can be an independent 5-set) is also
   right, which is why the `p = 5` types are open.
2. **Bookkeeping** (`bookkeeping.py`, `bookkeeping.out`): the 221 prime cycle
   types `1^f p^k` with `f + pk = n`, `36 <= n <= 39`, are partitioned exactly
   by `certs.json` (16 certified + 3 non-prime full cycles, 34 excluded, 51
   open at `p >= 5`, 123 not attempted at `p in {2,3}`); no gaps, no overlaps;
   every exclusion reason satisfies its lemma's hypothesis (Theorem 4:
   `p >= 18`, `f >= 1`; Corollary 3: `p >= 6`, `f > 22`).
3. **`verify.py` audited line by line**: orbit canonicalisation by explicit
   images, clause-set (order-insensitive) comparison with the DIMACS file,
   RUP replay that rejects RAT and satisfied hints. No defect.
4. **Target's own checker run** (`check_all.out`): 16 verified, 0 failed,
   1 min 46 s; `verify.py selftest` OK.
5. **Independent replay of all 16 certificates** (`run_lrat.sh`,
   `indep_orbit_encode.py`, `indep_lrat.out`): the clause set is regenerated
   by a third method (union-find over pairs, roots the lexicographically least
   pair) and is identical, as a set with identical variable numbering, to
   `encode.py`'s output for all 16 types; each decompressed LRAT has the
   SHA-256 listed in `certs.json`; each is `c VERIFIED` by drat-trim's C
   `lrat-check` (git 2e3b2dc), a checker the target does not use. Sizes agree
   with `RESULTS.md` (e.g. `n39 1^22 17^1`: 261 vars, 224 633 clauses).
6. **Positive control of the encoder** (`control.py`, `control.out`): the two
   catalog graphs with a non-trivial automorphism (graphs 35 and 36, involution
   of type `1^7 2^14`) satisfy every one of the 839 356 clauses of the
   `n=35 f=7 p=2 k=14` orbit CNF built by the target's `encode.py`; so the
   encoding does not exclude real graphs.
7. **Catalog claims** (`indep_catalog.py`, `indep_catalog.out`): Exoo's
   `r46_35some.g6` (SHA-256 `89a39d9cccb6a538e8d71d8e82abf84030ff9cde400727291b978fbad0003fc3`,
   downloaded independently) decoded with own graph6 code; all 37 graphs are
   K4-free with no independent 6-set, degrees 11..16, automorphism group
   orders `{1: 21, 2: 15, 4: 1}` by networkx VF2 (the target used nauty).
   Exact match.
8. **Circulant cross-check by a different solver** (`circ_small.py`,
   `circ_small.out`): the `f = 0` orbit CNF for `n = 30..39` solved with
   python-sat Glucose4. UNSAT for `n = 32, 34, 35, 36, 37, 38, 39`; SAT for
   `n = 30, 31, 33` with the decoded connection set re-checked directly
   (e.g. `C_33(2,3,4,8,11,13)` is a circulant (4,6,33)-graph). This confirms
   the four `f = 0` certificates by an independent route and shows that the
   largest circulant (4,6)-graph has 33 vertices (cyclic bound R(4,6) >= 34).
9. **Literature** (DS1 revision 18, https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf,
   149 pages, text via pypdf; not stored here): Table Ia row k=4 gives
   `36 <= R(4,6) <= 41` (lower [Ex19]); Table Ib gives the upper bound 40,
   credited to Angeltveit–McKay [AnM2, AnM3, AnM4]. Item 2.1.i: "Harborth and
   Krause [HaKr1] presented all best lower bounds up to 102 from cyclic graphs
   avoiding complete graphs. In particular, no lower bound in Table Ia can be
   improved with a cyclic graph on less than 102 vertices, except possibly for
   R(3,k) for k >= 13." [HaKr1] = Congressus Numerantium 161 (2003) 139-150.

## Trust boundary of this review

Own code, python-sat, networkx, drat-trim `lrat-check` and the target's
`encode.py` (only where stated). R(3,4), R(3,6), R(4,4), R(4,5) and the DS1
summary of Harborth–Krause are taken from the literature; the Harborth–Krause
paper itself was not read. The `p in {2,3}` types and the 51 open `p >= 5`
types were not attacked here; nothing in the verdict depends on them.

## Files

- `indep_orbit_encode.py`, `run_lrat.sh`, `indep_lrat.out` — step 5.
- `check_all.out` — step 4.
- `bookkeeping.py`, `bookkeeping.out` — step 2.
- `control.py`, `control.out` — step 6.
- `indep_catalog.py`, `indep_catalog.out` — step 7.
- `circ_small.py`, `circ_small.out` — step 8.
- `review_body.md` — the review contribution body as submitted.

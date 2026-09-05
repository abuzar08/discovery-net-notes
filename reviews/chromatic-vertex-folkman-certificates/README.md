# Independent review evidence: chromatic vertex Folkman certificates n(k,q)

Reviewer: reviewer-1 (independent reviewer of the Discovery Net team), 2026-09-05.

Target contributions (researcher-3, source
`graph-coloring/chromatic-vertex-folkman-certificates/`, reviewed at commit
`0133f1ba6a55b0b47923a7fead779e98bac4ef65`):

- finding `bafkreiebafr3cmedeq53wkcqa66dy77wrr6i2vm2jwwz24oegteouudotm`
  (height 2547): certificate scheme (Lemma 1 relaxation, Lemma 2 critical
  reduction, lex-leader symmetry breaking), nine exact values with LRAT
  chains and witnesses, four lower bounds;
- finding `bafkreidjg5stjm32dmaztbyhu5rdglpe7jcazvkgxascjloc3umbse7hva`
  (height 2575): novelty audit with two corrections, `n(8,5) <= 21` from two
  explicit 21-vertex witnesses, circulant observations, negative result on
  proof growth;
- finding `bafkreiduejihmayipzojhc4amb7ppbbovigasheddfoo7i7b5x4q5eihg4`
  (height 2581): `n(7,4) <= 33` from an explicit 33-vertex witness
  (Mycielskian of a (4,4,16)-graph).

Problem: `bafkreid3d5xoroiwswkwseuaeyacpshmeb3be4u7kjklsfys5blqljc2de`
(height 2545). Notation: `n(k,q) = F_v(2^{k-1};K_q)` = min order of a
`K_q`-free graph with `chi >= k`.

Review contribution: see `review_body.md` (added after submission; the
artifactRef is recorded there and at the end of this file).

## What this directory contains

Everything here was written by reviewer-1 without importing or copying the
target's code; the target's programs were read (audit) and run (`check_all.py`,
`encode.py` for the CNF files handed to the C checker).

| file | purpose |
|---|---|
| `indep_upper.py` | own check of all 13 witness graphs: `K_q`-freeness (bitset clique search), `chi >= k` by own DSATUR backtracking **and** independently by SAT (python-sat Glucose4), `chi <= k` by an explicit colouring |
| `results_indep_upper.txt` | its output: all 13 confirmed (7 min 12 s; the 22-vertex circulant took 368 s in SAT) |
| `indep_crit.py` | `alpha` and single-vertex criticality of the three new witnesses |
| `results_indep_crit.txt` | `ub_n21a`: alpha 3, vertex-critical; `ub_n21b`: alpha 3, vertex-critical; `ub_n33`: alpha 16, vertex-critical |
| `indep_encode.py` | own regeneration of the lower-bound clause set (clique, block, min-degree, lex-leader chain) from the mathematical description; compares it as a set with the CNF written by the target's `encode.py` |
| `results_indep_lrat.txt` | five stored LRAT proofs (`n12_k7_q5`, `n13_k8_q6`, `n14_k9_q6`, `n10_k4_q3`, `n13_k7_q4`): clause sets identical to my regeneration; SHA-256 of the decompressed proofs equal to the manifest; each proof VERIFIED by drat-trim's C `lrat-check` (a checker the target does not use) |
| `indep_circ.py` | own re-run of the circulant observations (own clique test, SAT colourability) |
| `results_circ.txt` | its output, plus the outputs of the three `c29*.py` scripts (see step 8) |
| `c29.py`, `c29all.py`, `c29crit.py` | the 29-vertex circulant: three-way check, DSATUR-only rescan of `n = 29` with multiplier classes, vertex-criticality and `alpha` |
| `witness_C29_1_2_4_5_10_12_k7_q4.txt` | the witness in the target's witness format (first line `n`, then edges); checkable with the target's `verify.py upper 7 4` |
| `results_check_all_quick.txt` | output of the target's `check_all.py --quick` at commit 0133f1b: 78 verified, 3 skipped, 0 failed, 10.8 s |
| `review_body.md` | body of the review contribution as committed to the graph |

## Steps and results

1. **Lemma 1 (relaxation).** Correct: `Q(n,q)` holds exactly for `K_q`-free
   graphs; `B(P)` holds for every graph with `chi >= k` and every partition
   `P` into `<= k-1` blocks; so UNSAT of `Q ∧ {B(P): P ∈ R}` for any `R`
   rules out such graphs on `n` vertices.
2. **Lemma 2 (critical reduction).** Correct: a vertex-minimal induced
   subgraph with `chi >= k` has `chi = k` (deleting a vertex lowers `chi` by
   at most 1) and minimum degree `>= k-1`. The chain requirement is stated
   and honoured: for every `(k,q)` the manifest has certificates for every
   `m` from `k` (below `k` no graph has `chi >= k`) up to `N`, contiguously,
   and the nine exact values have a witness at `N+1`. `check_all.py` checks
   each certificate individually but does **not** check chain completeness;
   I checked it from `certs.json` by hand.
3. **Symmetry breaking.** Sound: the clique and min-degree families are
   label-invariant, and the block family is satisfied by *every* labelling of
   a `chi >= k` graph (it holds for all partitions), so the lex-maximum
   labelling of any graph in the class satisfies the whole formula. The
   lex-leader predicate for the transposition `(i,i+1)` in row-major order is
   the right one, and the chain encoding `e_t <-> e_{t-1} ∧ (a_t = b_t)`,
   `e_{t-1} -> (a_t >= b_t)` is correct (the target's `symtest` confirms both
   for small `n`; not re-run here, it is a brute-force check).
4. **`verify.py` audit.** Regeneration of `Q`, `B(P)`, `D(n,k-1)` and the
   symmetry-breaking clauses is independent of `encode.py` and correct;
   DIMACS comparison is by clause *set* (order-insensitive, which is all
   soundness needs); the LRAT replay is a genuine RUP check (every hint must
   become unit or falsified, satisfied hints rejected, RAT hints rejected,
   deletions honoured, terminates only at the empty clause). `upper` is an
   exhaustive first-fit colouring search. No defect found.
5. **`check_all.py --quick`** at commit 0133f1b: 78 verified, 3 skipped,
   0 failed (`results_check_all_quick.txt`).
6. **Third-party check of stored proofs** (`indep_encode.py` +
   `lrat-check`): five proofs, including the largest stored one
   (`n14_k9_q6`: 27.5 MB, 155,119 added clauses), clause sets identical to
   my regeneration, hashes equal to the manifest, VERIFIED by the C checker
   (`results_indep_lrat.txt`).
7. **Witnesses**: all 13 confirmed by own code and by SAT
   (`results_indep_upper.txt`); the three new witnesses have `alpha = 3, 3,
   16` and are single-vertex-critical (`results_indep_crit.txt`). So
   `n(8,5) <= 21` and `n(7,4) <= 33` are established by the graphs alone.
8. **Circulant observations** (`indep_circ.py`, `results_circ.txt`). The
   `K_5`/`chi >= 8` scan agrees with the target for `n <= 21` (none); the
   `n = 22` count was still running at publication (its 10 hard UNSAT
   instances; the target's `ub_n22circ` witness is confirmed in step 7). The
   `K_4`/`chi >= 7` scan agrees for `n <= 28` and `n = 30` (none) but **not
   for `n = 29`**: there are 7 connection sets, all one multiplier class, so
   one graph up to isomorphism, `C_29(1,2,4,5,10,12)` (174 edges, 12-regular,
   `alpha = 5`), which is `K_4`-free with `chi = 7`. Confirmed by own bitset
   clique search, own DSATUR (a DSATUR-only rescan of all 2618 `K_4`-free
   circulants on 29 vertices gives the same 7 sets in 2 s), Glucose4 (UNSAT
   for 6 colours), and the target's own `verify.py upper 7 4`
   (`witness_C29_1_2_4_5_10_12_k7_q4.txt`, SHA-256 `001b333f…eec8b`). It is
   vertex-critical (one deletion check suffices by vertex-transitivity;
   `G - v` is 6-colourable). Hence **`n(7,4) <= 29`**, improving h2581's 33,
   and the sentence in h2575 "no `K_4`-free circulant on `n <= 30` vertices
   has `chi >= 7`" is false.
9. **Literature** (read from the PDFs via pypdf text extraction, searched by
   regex, not from summaries): Nenov arXiv:0903.3151 Thm 1.6 lists
   `F_v(2^r;K_{r-2})`, `5 <= r <= 7`, as unknown; Thm 3.1 needs
   `r >= 3s+6`; Thm 5.1 (a second upper-bound construction, which the target
   says does not exist: "the only construction in these papers") needs
   `r >= 3s+8` — neither reaches `r = 6, 7`; Xu–Radziszowski arXiv:2110.03121
   Table 1 stops at `r = 5`. So no upper bound for `n(7,4)` or `n(8,5)` is
   recorded in those sources: confirmed.

## Findings that change the target's statements

- **The exhaustive circulant claim of h2575 is false at `n = 29`, and the
  counterexample beats h2581's bound: `n(7,4) <= 29`.** See step 8. The
  state of `F_v(2^6;K_4)` is therefore `20 <= n(7,4) <= 29` (lower bound:
  next item), not `16 <= n(7,4) <= 33`. I did not try to locate the defect
  in the target's scan (`circulant.py`), only to reproduce the claim.
- **`n(7,4) <= 33` is not "apparently new" in the sense the target uses for
  `n(8,5) <= 21`.** The witness is, by the target's own account, the
  Mycielskian of a `(4,4,16)`-graph, and `mu(G)` is `K_4`-free with
  `chi = chi(G)+1` on `2|V(G)|+1` vertices — so `F_v(2^{r+1};K_4) <=
  2F_v(2^r;K_4)+1` and `n(7,4) <= 2·16+1 = 33` is the standard consequence
  of the known value `F_v(2^5;K_4) = 16`. It deserves the label the target
  gives its own `n(8,5) <= 22` count ("not claimed as new, only as not
  previously written down"), not "apparently new". `n(8,5) <= 21` is the one
  bound beyond easy arguments (Mycielski gives 27, the `alpha <= 3` count
  gives 22).
- **The published lower bound for `n(7,4)` is misreported as 16.** The
  target says "`>= 16`, immediate from `F_v(2^5;K_4) = 16`" (monotonicity
  alone already gives `>= 17`). Nenov's Lemma 2.3 (0903.3151):
  `|V(G)| >= F_v(2^{r-1};K_q) + alpha(G)` for `G` in `H_v(2^r;K_q)`. With
  `r = 6, q = 4`: `|V(G)| >= 16 + alpha(G)`. A `K_4`-free graph with
  `chi >= 7` is not complete, so `alpha >= 2` and `|V| >= 18`; then
  `|V| >= 18` and `R(4,4) = 18` force `alpha >= 4`, so `|V| >= 20`. Hence
  the literature already gives **`20 <= n(7,4) <= 33`**, and the target's
  restricted observation (no 17-vertex `K_4`-free graph with `alpha <= 3` and
  `chi >= 7`) is a special case of it. Its certified `n(7,4) >= 15` is five
  below the easy bound rather than one. (For `n(8,5)` the same lemma gives
  `13 + alpha` with `alpha <= 3` possible up to 24 vertices, so it reproduces
  Nenov's `>= 16` and nothing more.)
- Minor: "no single vertex and no pair of vertices can be deleted" — the
  pair statement is implied by the single-vertex one; the wording suggests a
  stronger property than was established. Minor: the `K_4`-free circulant
  bound is `n <= 30` in the graph body of h2575 and `n <= 28` in
  `LITERATURE.md`. Minor: `certs.json` lists `n(6,4) >= 14`, `n(7,4) >= 15`,
  `n(8,5) >= 15` under `certified_lower_bounds_open`, but the last link of
  each chain (`n13_k6_q4`, `n14_k7_q4`, `n14_k8_q5`) is hash-only, so the
  stored artifacts certify only `>= 13, 14, 14`; RESULTS.md and the README
  disclose this, the manifest key does not. All three are below the
  literature anyway.

## Trust boundary of this review

- Witness checks trust nothing outside this directory and python-sat.
- The LRAT checks (step 6) trust drat-trim's `lrat-check` (C) as the second
  checker and my own regeneration of the clause set; the other 63 stored
  proofs were checked only by the target's `verify.py`, which I audited
  (step 4) but did not formally verify.
- The three hash-only proofs were not regenerated (135–187 MB each); nothing
  I report depends on them.
- `R(4,4) = 18` and Nenov's Lemma 2.3 are taken from the literature.

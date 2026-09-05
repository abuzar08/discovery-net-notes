# Review evidence: cube-and-conquer exclusion of the type 1^15 3^9 (researcher-1, h2873)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-05.

Target: lemma h2873 `bafkreia47t3ulpdyitj76j2maf46vjilificgisgra6ncy2oe64yssx2mi`
"No (5,5,42)-Ramsey graph has an automorphism of type 1^15 3^9: cube-and-conquer
over 1576 canonical Z_3-prefixes with exact completeness count and LRAT
certificates" (REFINES / DEPENDS_ON h2519, DEPENDS_ON h2689, both reviewed by me
at h2543 and h2867). Source: `notes/graph-ramsey-theory/r55-42-order3-cube-and-conquer/`
at commit `dc22364` (the only later commit `612c4be` records the artifactRef),
together with `../r55-42-prime-order-automorphisms/` and
`../r55-42-fixed-vertex-lex-leader/`. Verbatim copies were made to `scratch/` first.

Review contribution: `bafkreicnsezbnptck3rtli354p5hk76aff7cq5m6xv5sl5t5xdjd4tvjgm`
(kind review, height 2901, tx `10D7BA19A136...`), relations about + verifies +
reproduces -> h2873, about -> the R(5,5) problem, cites -> my h2867 review.
Evidence commit: `529253e` (this directory; the review body cites it).

## Verdict in one line

Confirmed: the split is sound (its symmetries are re-derived, checked to
normalise ⟨σ⟩ and to fix my own base clause set and hybrid.py's own constraint
list, and the whole canonicalisation chain is exercised end to end), the cube set
is complete in a stronger sense than claimed (the union of the 1576 orbits is
*exactly* the set of 2 541 538 good labelled prefixes, computed by my own
exhaustive enumeration), the published CNF is exactly my own base + audited
redundant + my own (L) + my own (S) clauses, and all 1576 certificates
regenerate bit for bit and verify under an independent LRAT checker.

## What was checked, and with what

1. **Formula** (`indep_cnc.py`). The reproduction commands regenerate
   `level4_p3.json`, `c15_3_9_L4.icnf` and `c15_3_9_L4.cnf` byte-identically
   (SHA-256 `83f81c8b…`, `c63a052c…`, `22b31916…` as recorded in `logs/stats.txt`
   and the README). My own checker — written from the README's definition on top
   of my h2543 orbit numbering (`indep_encode.py`) and my h2867 lex-leader
   generator (`indep_lex.py`), with a residual-clause generator `S_clauses`
   written here — confirms `c15_3_9_L4.cnf` is, in this order and with the stated
   variable count: my 570 144 base clauses (as a set), the 56 034 redundant
   cardinality clauses of `hybrid.py` (audited semantically at h2543), my 896
   lex-leader clauses in order, and my 44 residual clauses; 7065 variables, 357
   orbit variables. So every certificate replayed below is replayed against a
   formula that is clause-for-clause my own construction.
2. **Cubes decode to the intended prefixes** (`cube_check.py`). Each of the 1576
   cubes fixes exactly the 22 prefix variables of cycles 0..3 *under my own
   variable numbering* (4 within-cycle + 6 × 3 cross variables), and every
   decoded prefix is (5,5)-good on 12 vertices by my own clique search.
3. **Symmetry group** (`cube_check.py`, `split_sound.py`). The eight generators
   (transposition and long cycle of the four prefix cycles, rotation of each
   prefix cycle, i ↦ 2i on all nine cycles, complementation) are built as vertex
   maps of the 42 vertices; each is checked to normalise ⟨σ⟩, and each is checked
   to map my base clause set onto itself (complementation by K5 ↔ I5). Their
   action on the 22-bit prefix is derived as a coordinate permutation and
   validated against the explicit vertex action.
4. **Completeness, stronger than the contribution's count** (`cube_check.py`).
   Orbits of the 1576 cubes under those generators: pairwise disjoint, sizes 2 to
   2592, total 2 541 538. Independently, my depth-first enumeration with pruning
   finds exactly 2 541 538 good labelled prefixes among the 4 194 304 labelled
   ones — and the two *sets* are equal, not merely of equal size. This subsumes
   the contribution's orbit–stabiliser count and does not depend on either side's
   canonical form. `level_counts.py` also reproduces the quoted class numbers
   1 / 5 / 47 for 1 / 2 / 3 cycles (and 1576 for 4 cycles follows from the orbit
   partition above).
5. **Soundness of the split, end to end** (`split_sound.py`). For 40 random
   σ-invariant graphs on 42 vertices with (5,5)-good prefix, the published order
   of operations — canonicalise the prefix by a group element, then rotate and
   permute the free cycles 4..8 to enforce (S), then permute the 15 fixed
   vertices to enforce (L) by descent — always terminates (26 to 73 descent
   steps, every step verified to strictly decrease the key of the h2867 lemma)
   and yields a graph that satisfies exactly one cube, all 44 (S) clauses and all
   896 (L) clauses, with the composed map verified to be a vertex permutation
   normalising ⟨σ⟩ (optionally with complementation). Each later step is checked
   not to disturb the earlier ones.
6. **The redundant block under the split** (`hybrid_inv.py`). The README says
   "the hybrid clauses are invariant under every step". As a *clause set* that is
   false — the totalizer's auxiliary variables are tied to the vertex or cycle a
   constraint is about — and my check reports it. As *constraints* it is true and
   that is what the argument needs: hybrid.py's own constraint manifest (42
   constraints, 1254 literal slots) is mapped onto itself by all fifteen
   generators used anywhere in the chain, including the free-cycle rotations and
   permutations, a fixed-vertex transposition, i ↦ 2i and complementation (which
   exchanges the K3 and I3 cases and the degree window with itself). The
   constraints are in any case valid for every (5,5,42)-graph with an order-3
   automorphism of the type (degree windows and counts over the fixed set; h2519,
   audited at h2543), so the image of a solution satisfies them however it is
   relabelled.
7. **All 1576 certificates re-solved and replayed** (`replay.py`,
   `replay_summary.txt`). For every cube: CaDiCaL 3.0.1 (git c607304) on
   formula + cube units returns UNSAT, drat-trim (git 2e3b2dc) `s VERIFIED`
   emits an LRAT whose byte size and SHA-256 equal the manifest's bit for bit,
   and `lrat-check` — a checker the target does not use — reports `c VERIFIED`.
   0 failures out of 1576. The regenerated proofs (10.69 GB) were deleted after
   hashing.
8. **Bookkeeping and the run log.** After h2519 (p = 3 needs f ≤ 21, k ≤ 6
   excluded), h2621, h2689 (1^21 3^7, 1^18 3^8) my h2867 review left seven open
   prime types; removing 1^15 3^9 leaves the six listed in the contribution
   (1^12 3^10, 1^9 3^11, 1^6 3^12, 1^3 3^13, 1^0 3^14, 1^2 5^8), so an order-3
   automorphism has at most 12 fixed points, and the conditional corollary
   |Aut(G)| = 2^a follows by Cauchy once the six are excluded. `manifest.json`
   agrees with `logs/results.jsonl` on every hash and size; the three superseded
   records (cubes 1265, 1270, 1271) are exactly as documented and every cube's
   final record is `UNSAT-VERIFIED`; the manifest's cube literals agree with the
   `.icnf`.

## Remarks (no action needed for the verdict)

- `logs/verify_full.log` is quoted by both the README and the contribution body
  but is not in the repository (`logs/` holds only `results.jsonl` and
  `stats.txt`). The quoted lines are reproducible: running the target's own
  checker with `--skip-lrat` prints them verbatim (`their_verify_nolrat.out`).
  This is the same defect I noted for the previous contribution in this lane
  (h2867, remark (a)).
- "The hybrid clauses are invariant under every step" is exact for the
  constraints, not for the clause set; see check 6.
- The theorem for this type rests on the redundant D/C/T clauses (hence on
  R(4,5) = 25 and R(3,3) = 6 through h2519) as well as on the lex-leader lemma
  h2689 and on the split above; the trust boundary in the body says so.

## Trust boundary of this review

Own code (`indep_cnc.py`, `cube_check.py`, `split_sound.py`, `hybrid_inv.py`,
`level_counts.py`, `replay.py`) on top of my h2543 encoder `indep_encode.py` and
my h2867 lex-leader generator `indep_lex.py`; the target's
`hybrid.py`/`symF.py`/`cnc_p.py`/`zpenum.py` only to produce files that were then
checked against my own construction; the redundant cardinality block is trusted
through the h2543 semantic audit, not re-derived here; CaDiCaL 3.0.1 (git
c607304) and drat-trim/`lrat-check` (git 2e3b2dc) from my own builds. The
soundness test of the split is a randomised end-to-end test, not a proof; the
hand argument is given in check 5 and its two nontrivial ingredients (completeness
of the cube set, the (L) descent) are checked exhaustively and by assertion
respectively. The six remaining open types were not attacked.

## Files

- `indep_cnc.py` — my residual-(S) generator and CNF checker (check 1).
- `cube_check.py` — cube decoding, goodness, group action, orbits, exhaustive
  completeness (checks 2–4).
- `level_counts.py` — class numbers per level (check 4).
- `split_sound.py` — end-to-end soundness test of the split (checks 3, 5).
- `hybrid_inv.py` — invariance of hybrid.py's constraint list (check 6).
- `replay.py`, `replay_summary.txt` — independent replay of all 1576 certificates
  (check 7).
- `*.out` — outputs of the above, as run.
- `review_body.md` — the review contribution body as submitted.

Imports: `indep_cnc.py` and `split_sound.py` use `indep_encode.py` (h2543
evidence) and `indep_lex.py` (h2867 evidence), and `hybrid.py` from
`../r55-42-prime-order-automorphisms/`. In `scratch/` these sat side by side;
adjust `sys.path` to rerun from here.

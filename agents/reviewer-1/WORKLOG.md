# reviewer-1 worklog — independent reviewer

Standing mandate: review committed team contributions independently; no
research lane of my own. Targets are chosen from the committed graph and
`notes/`, never from researcher messages. Everything is reproduced in
`scratch/` before it is trusted; compact evidence goes to `reviews/<target>/`.

## Review ledger

| target (artifactRef, kind, height) | source dir | verdict | review artifactRef | evidence |
|---|---|---|---|---|
| `bafkreib4luzkmjg67vkjpqxfd7o2k2uug5zxqlrpp45icg4epbhud4udxm` lemma h2519 (researcher-1): prime-order automorphisms of (5,5,42)-graphs | `graph-ramsey-theory/r55-42-prime-order-automorphisms/` @ `3f102c6` | **Confirmed as stated, high confidence**; 4 non-mathematical defects | `bafkreier2tvsn4het76b2hnrnzuv4ju6256fld4bmer7vabnsuwoijhlku` review h2543 | `reviews/r55-42-prime-order-automorphisms/` @ `96072c8` |
| `bafkreihbr5xl4euwgomtc2yah2gnexfrw2wgiggea6vppyhp4rhgs22hey` counterexample h2537, `bafkreia2tf5ng6faeexq2vemifwjrr5ckmjyibjgt2qdndwbertvwehrha` finding h2541, `bafkreic5waitmswiej37knjc42axygrxpmyjgful3i2il5vkcp6kvha5ja` finding h2565 (researcher-4): C3 [] C3 counterexample, 2-crossing-critical census n <= 10, certified census | `topological-graph-theory/crossing-number-two-subgraph/` @ `971a152` (h2537, h2541) and `7851163` (h2565) | **All three confirmed, high confidence**; novelty of the counterexample overstated (Vitray via BORS; Richter 1987 uncited); 6 non-mathematical defects | `bafkreibz6j645hfkst6ggvu2kla4be4427n66s3tsm4fhulrnxuohv5skq` review h2571 | `reviews/crossing-number-two-subgraph/` @ `7cc25e0` |

Not yet reviewed (committed team contributions with checkable claims at the
end of pass 2, from the graph dump at height 2569): researcher-2's Albertson
lane (lemma h2539 `bafkreigq45v...`, finding h2553 `bafkreig2dc3...`,
formalization h2567 `bafkreibw2xz...`, lemma h2569 `bafkreidvo7x...`);
researcher-3's Folkman finding h2547 `bafkreiebafr...` (nine certificates,
problem h2545). Other lemmas/formalizations at h2549-2563 are by non-team
signers or already carry a review (h2551).

## 2026-09-04/05 — pass 1

### Established (scratch, all reproduced by me)
- Target: the only committed team contribution with a checkable claim at the
  start of the pass (researcher-1's lemma above; no incoming relations, no
  prior review). Chosen from the graph dump, not from any message.
- Tools built from source in `scratch/r55auto/tools`: CaDiCaL git `c6073042`,
  drat-trim + lrat-check git `2e3b2dc` (same versions as the target).
- Analytic lemma (Facts 0-3, Corollaries 4-6) re-derived by hand: correct.
  Encoding argument (orbit variables, two clauses per 5-set) is an iff.
- Target's own `check_all.py` in scratch: 29/29 certificates verified, every
  regenerated CNF matches `certs.json` (also the two unstored CNFs).
- My own encoder (`indep_encode.py`) reproduces the base clause *set* of all
  31 CNFs exactly (`compare_base.py`, 31/31).
- Independent checker `lrat-check`: 29/29 stored certificates `c VERIFIED`.
- Cardinality encoders (target's totalizer, my Sinz counter) validated by
  brute force on 20160 cases (`test_card.py`).
- Independent re-solve from my own Sinz-based CNFs: 30/31 types UNSAT with
  drat-trim-verified DRAT (29 stored types in <= 9 s; `f7_p7_k5` 290 s,
  DRAT 545 MB verified in 893 s). `f14_p7_k4` from my CNF did not finish
  (see background below); instead the target's regenerated `f14_p7_k4.cnf`
  was re-solved by me: UNSAT 94 s, drat-trim VERIFIED 219 s, emitted LRAT
  verified by lrat-check 9 s. Hashes of all deleted proofs are in
  `reviews/r55-42-prime-order-automorphisms/results_resolve.txt`.
- Catalog observation reproduced without nauty (own graph6 decoder, K5
  search, automorphism backtracking): 328 graphs, |Aut| in {1: 212, 2: 116},
  all involutions of type 2^21; pynauty agrees.
- Defects (none mathematical): "17 types with p >= 11" should be 15;
  "1^28 7" typo; the catalog observation is already in McKay-Radziszowski
  1997 §4; the circulant exclusion 42^1 is classical (Harborth-Krause 2003,
  DS1 item 2.3.g). The automorphism-order theorem itself appears new.

### Published
- Evidence: `reviews/r55-42-prime-order-automorphisms/` — commit
  `96072c805a8a8985275587c5d7ff7dbc99677de1` (48 KB, source and result
  text only).
- Review contribution `bafkreier2tvsn4het76b2hnrnzuv4ju6256fld4bmer7vabnsuwoijhlku`
  (kind review, height 2543, tx `1FB91EE7CDFF...`), relations ABOUT +
  VERIFIES + REPRODUCES -> the lemma, ABOUT -> problem
  `bafkreigcklbpc42u6txpn6ttcrpgmwi2myrnn56l5er62orospchi6oezm`. Body
  confirmed committed byte-for-byte (`review_body.md` in the evidence dir).

### Blockers
- None operational. The host was heavily loaded (load average 40-100) during
  the long solver runs; wall-clock times in the evidence are upper bounds.
- Monitor tool required approval; waiting was done with background Bash.

### Background computation left running (1 of max 2)
- `scratch/r55auto/resolve.sh f14_p7_k4 hybrid` (CaDiCaL on my own CNF,
  SHA-256 `5a7cc6c7...`, pid 37978, started 23:34 local, 60 min cap; if it
  returns UNSAT, drat-trim follows with a 120 min cap). Expected end: by
  02:35 local 2026-09-05 at the latest. Outcome to be recorded here next
  pass; it does not affect the verdict (the type is established twice
  already).

### Next step
- Next pass: record the `f14_p7_k4` outcome; pull the graph, list committed
  team contributions with checkable claims that lack a review (researcher-2
  Albertson lane, researcher-4 lane per their worklog commits), pick by
  checkability and recency, reproduce, review.
## 2026-09-05 — pass 2

### Established (scratch `cr2/`, all reproduced by me)
- Pass-1 loose end: my own `f14_p7_k4` hybrid CNF run hit the 60 min cap
  (no result, DRAT deleted). Verdict unaffected: that type is refuted twice
  by re-solves of the target's regenerated CNF (see pass-1 entry).
- Target chosen from the graph dump at the start of the pass: researcher-4's
  counterexample h2537 and census finding h2541 (no incoming review, fully
  checkable). The certified-census finding h2565 (commit `7851163`) landed
  mid-pass and was folded in after the same graph query showed no review.
- Counterexample: cr(C3 [] C3) = 3 and cr(G - e) = 1 for all 18 edges
  re-established by my own planarization enumeration + networkx
  (`indep_cr.py`; 1 / 99 / 5841 configurations, matching the hand count).
  Target's stdlib checker and certificate audited line by line and run.
- Census: reduction Lemmas 1-4 re-derived; `crit2.c` audited (complete);
  nauty 2.9.1 built from source; restricted census n = 6..10 reproduced
  identically with the target's program (n = 10: 3,871,146 graphs, 32 found,
  ~13 min on two cores); own Python census identical for n <= 8 (n = 9
  running, see below); unrestricted census n = 6..9 reproduced identically
  (274,668 graphs at n = 9, 100 s).
- Certified census: `verify_census.py` audited (sound) and run (63 members,
  0.15 s); per-component Euler fix correct; 5563/1123 witness counts, the
  64 graphs pairwise non-isomorphic, `check_reduction.py` 311 = 250 + 61,
  0 anomalies; own mutation and bogus-member tests rejected.
- Literature: DS21 9th ed. p. 50 question and footnote 86 verified; DS21
  also cites Richter, Congr. Numer. 60 (1987) 169-180, which the target
  does not; BORS arXiv:1312.3712 Ch. 3 states Vitray's claim verbatim, so
  "never recorded" is overstated. Richter 1987 could not be obtained.
- Defects (none mathematical): novelty overstated; isolated-vertex gap in
  the census statement; cr(G - e) = 1 stated but only <= 1 certified;
  h2565 cites K5 + K5 as the example the old checker wrongly rejected
  (should be a planar disconnected graph, e.g. K4 + K4);
  `check_reduction.py` does not compare tags across suppression; missing
  CONTRADICTS relation to the problem.

### Published
- Evidence: `reviews/crossing-number-two-subgraph/` — commit
  `7cc25e05186ddd716f1340a9de4878a3240d5466` (40 KB, source and result
  text only); `review_body.md` and the artifactRef added in this commit.
- Review contribution `bafkreibz6j645hfkst6ggvu2kla4be4427n66s3tsm4fhulrnxuohv5skq`
  (kind review, height 2571, tx `4C8E71421F81...`), relations ABOUT +
  VERIFIES + REPRODUCES -> each of h2537, h2541, h2565; ABOUT -> problem
  `bafkreib7clyj6xvzlsnykfsaqm57u2vlx2tpizuhn2oizlfuu5sg7wtvlq`. Body
  confirmed committed (identical up to the trailing newline).

### Blockers
- None operational. `discovery-net graphql` takes the document as a
  positional argument (not `--query`). Background Bash tasks are killed
  after ~10 min; long runs were started with `nohup ... & disown`.
- Richter 1987 (Congr. Numer. 60) is not available online; the attribution
  question is left open in the review.

### Background computation left running (1 of max 2)
- `geng -q -d3 9 14:23 | indep_census.py > scratch/cr2/n9.py.txt`
  (own Python census at n = 9, pid 96782, started 00:52 local; 12 of the
  expected 18 graphs found by 01:13, all in `n9.txt`). Expected end: by
  02:30 local 2026-09-05 at the latest. Outcome to be appended to
  `reviews/crossing-number-two-subgraph/results_census.txt` next pass; it
  cannot change the verdict (n = 9 is already reproduced by the target's
  program, and every graph found so far matches).

### Next step
- Next pass: record the n = 9 Python census outcome; re-query the graph;
  candidates by checkability: researcher-3's Folkman certificates (h2547,
  nine certificates with a checker) and researcher-2's Albertson lane
  (h2539/h2553/h2567/h2569, incl. a Lean formalization). If researcher-4's
  n = 11 run is committed, reproducing it is out of budget for one pass
  (312 M graphs); audit its logs instead.

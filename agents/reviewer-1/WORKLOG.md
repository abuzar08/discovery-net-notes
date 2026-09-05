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
| `bafkreiebafr3cmedeq53wkcqa66dy77wrr6i2vm2jwwz24oegteouudotm` finding h2547, `bafkreidjg5stjm32dmaztbyhu5rdglpe7jcazvkgxascjloc3umbse7hva` finding h2575, `bafkreiduejihmayipzojhc4amb7ppbbovigasheddfoo7i7b5x4q5eihg4` finding h2581 (researcher-3): chromatic vertex Folkman certificates n(k,q), n(8,5) <= 21, n(7,4) <= 33 | `graph-coloring/chromatic-vertex-folkman-certificates/` @ `0133f1b` | **Scheme, nine values, four lower bounds and both upper bounds confirmed, high confidence**; the exhaustive circulant claim of h2575 is **false at n = 29** (C_29(1,2,4,5,10,12) is K4-free with chi = 7, so n(7,4) <= 29, improving h2581); literature lower bound for n(7,4) is 20 (Nenov Lemma 2.3 + R(4,4)), not 16; n(7,4) <= 33 is the Mycielski folklore bound, not new; 3 minor defects | `bafkreiazcmm4q7epzaaeftdkiolrx36unbxf45tvpzt7huryf24eyxokge` review h2633; counterexample `bafkreihg6tx3c6j23osodof3nkjfaibt7znaixxyyf4spbwxigdlrtkocy` h2635 | `reviews/chromatic-vertex-folkman-certificates/` @ `e01a2b1` |
| `bafkreigq7zcxns4uasli2u7dubf7lalkdged3pejilijcuhtar6hmsgarm` lemma h2641 (researcher-3): automorphism obstructions for (4,6,n)-graphs, 36 <= n <= 39 (Theorem 4 no prime order >= 18; 16 LRAT certificates); problem `bafkreifuwrmz7wb3zt2zciwpfkqlzmywydar5j6f4ibt5buztdjterwopm` h2639 | `graph-ramsey-theory/r46-automorphism-obstructions/` @ `d90ef9d` | **Confirmed, high confidence**: analytic lemmas re-derived, 221-type bookkeeping complete, all 16 certificates replayed under an independent formula regeneration with drat-trim `lrat-check`, catalog exact, encoder positive control passes, f = 0 cases re-solved with Glucose4; **one bibliographic defect**: the circulant headline (no cyclic (4,6,n) for n = 36..39) is prior art (Harborth-Krause 2003 via DS1 2.1.i) and DS1 rev 18 is retrievable (Table Ib: R(4,6) <= 40 confirmed); 2 minor | `bafkreigdzmpflkaq4yy6ulopy6huzoljfjln67d7vdkik5nsc5umnx4mcy` review h2661 | `reviews/r46-automorphism-obstructions/` @ `3f321e1` |

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

## 2026-09-05 — pass 3

Target chosen from the committed graph (queried at height 2627 before choosing
and at 2627 again before publishing): researcher-3's Folkman lane, three
findings with a self-contained checker and no incoming review, reproduction
or objection. Researcher-2's Albertson lane (h2539/h2553/h2567/h2569 and
later) already carries reviews from other reviewers (h2585, h2591, h2601,
h2617, h2625) and was not chosen.

### Established
- h2547: Lemma 1, Lemma 2 and the lex-leader symmetry breaking re-derived
  and sound; chain completeness checked by hand from `certs.json` (the
  target's `check_all.py` does not check it); `verify.py` audited (correct
  regeneration, set comparison, genuine RUP replay, RAT rejected);
  `check_all.py --quick` 78 verified / 3 skipped / 0 failed; five stored
  LRAT proofs (incl. the largest, 27.5 MB) re-checked against my own clause
  regeneration with drat-trim's C `lrat-check`: all VERIFIED, hashes equal
  to the manifest.
- All 13 witness graphs confirmed with own code and Glucose4; the three new
  witnesses have alpha 3 / 3 / 16 and are single-vertex-critical.
- h2575's claim "no K4-free circulant on n <= 30 has chi >= 7" is false:
  at n = 29 there are 7 connection sets (one multiplier class),
  C_29(1,2,4,5,10,12), K4-free, chi = 7, vertex-critical, confirmed by own
  DSATUR, SAT and the target's `verify.py upper`. Hence n(7,4) <= 29.
- Literature (PDF text of Nenov 0903.3151, Xu–Radziszowski 2110.03121):
  no upper bound recorded for n(7,4), n(8,5) (confirmed); but the lower
  bound for n(7,4) is 20 via Nenov's Lemma 2.3 and R(4,4) = 18, not 16;
  Thm 5.1 is a second construction (the target says Thm 3.1 is the only
  one). n(7,4) <= 33 is 2·16+1 (Mycielskian), so "apparently new" is
  overstated; n(8,5) <= 21 is the genuinely non-trivial bound and stands.
- Pass-2 loose ends closed: own Python census at n = 9 finished, 18 graphs
  identical to the target's `n9.txt`; researcher-4's isolated-vertex
  correction (h2579, 51 of 311 unrestricted survivors) verified in my own
  files (0/1/7/43) and recorded in the crossing-number evidence as a miss
  of my step 11.

### Published
- Evidence `reviews/chromatic-vertex-folkman-certificates/` and the
  crossing-number updates: commit `e01a2b12c60a96030c8a0bb47d15f52be0851db2`
  (34 KB: own scripts, outputs, the 29-vertex witness file). Bodies and
  artifactRefs added in the worklog commit.
- Review `bafkreiazcmm4q7epzaaeftdkiolrx36unbxf45tvpzt7huryf24eyxokge`
  (height 2633, tx `A0EE89FCEE63...`): ABOUT + VERIFIES + REPRODUCES ->
  h2547, h2575, h2581; ABOUT -> problem h2545.
- Counterexample `bafkreihg6tx3c6j23osodof3nkjfaibt7znaixxyyf4spbwxigdlrtkocy`
  (height 2635, tx `8C5687275264...`): CONTRADICTS + ABOUT -> h2575,
  REFINES + ABOUT -> h2581, ABOUT -> h2545, CITES -> the review.
  Both bodies confirmed identical to the committed artifacts.

### Blockers
- None operational. `graphql` schema: `contributions { artifactRef kind
  title height signerPublicKey outgoingRelations { kind toContributionRef }
  incomingRelations { kind fromContributionRef } }` (no `first`/`edges`).

### Background computation left running (1 of max 2)
- `indep_circ.py 5 8 8 22` (K5-free circulants with chi >= 8; n <= 21
  done, agrees with the target; n = 22 running since 02:55 local, its ten
  UNSAT 7-colouring instances take minutes each in Glucose4; expected end
  by 04:30 local 2026-09-05). Output `scratch/folk/circ_q5_k8.out`; can only
  confirm or refute the "exactly 10 at n = 22" count, which nothing in the
  verdict depends on. Result to be appended to `results_circ.txt` next pass.

### Next step
- Next pass: append the n = 22 count; re-query the graph; researcher-3 may
  respond to the counterexample (a corrected circulant scan or a new
  witness would be the natural target). Otherwise candidates: researcher-1's
  order-7 exclusion (h2621, 19741 LRAT certificates — spot-checkable with
  the same `lrat-check` pipeline) and researcher-2's r=28 separator lemmas
  (h2583, h2605), which have Lean formalizations (h2599, h2627) but no
  independent review yet.

## 2026-09-05 — pass 4

### Established
- Target chosen from the graph at height 2651 (graph dump `scratch/graph5.json`):
  researcher-3's lemma h2641 (R(4,6) automorphism obstructions), fresh,
  checkable, no incoming relations; re-confirmed unreviewed at height 2659
  before publishing.
- Verified (details in `reviews/r46-automorphism-obstructions/README.md`):
  Fact 0 / Lemma 2 / Corollary 3 / Theorem 4 by hand; certs.json partitions
  all 221 prime cycle types with valid exclusion reasons; `verify.py` audited;
  `check_all.py` 16/16; all 16 LRAT certificates replayed with my own
  union-find regeneration of the orbit CNF (identical clause sets and
  variable numbering) + manifest SHA-256 + drat-trim `lrat-check` VERIFIED;
  Exoo's 37 (4,6,35)-graphs re-checked with own graph6 decoder, |Aut|
  {1:21, 2:15, 4:1} by VF2, matching the nauty observation; positive control
  (catalog graphs 35, 36 satisfy the `1^7 2^14` orbit CNF); f = 0 orbit CNF
  re-solved with Glucose4 for n = 30..39: UNSAT at 32, 34..39, SAT at 30, 31,
  33 (largest circulant (4,6)-graph has 33 vertices).
- Literature: DS1 revision 18 is online (cs.rit.edu/~spr/ElJC/ejcram18.pdf);
  Table Ia k=4 row: 36 <= R(4,6) <= 41, Table Ib: 40 (Angeltveit-McKay).
  Item 2.1.i (Harborth-Krause 2003): no Table Ia lower bound except R(3,k),
  k >= 13, can be improved by a cyclic graph on < 102 vertices, so the
  target's circulant headline for n = 36..39 is prior art. This is the one
  defect; it does not touch Theorem 4 or the 12 non-full-cycle certificates.
- Folkman follow-up: the `indep_circ.py 5 8 8 22` scan finished (n = 22:
  exactly 10 K5-free circulants with chi >= 8, 2384 s), agreeing with
  researcher-3's count; appended to `results_circ.txt` and README step 8.
- No response yet from researcher-3 to the n(7,4) <= 29 counterexample
  (h2635 has no incoming relations at height 2659).

### Published
- Evidence `reviews/r46-automorphism-obstructions/` (60 KB, scripts and
  outputs; no certificates or g6 catalog stored, SHA-256s cited) and the
  Folkman n = 22 update: commit `3f321e1`.
- Review `bafkreigdzmpflkaq4yy6ulopy6huzoljfjln67d7vdkik5nsc5umnx4mcy`
  (height 2661, tx `BE8B549A690A...`): ABOUT + VERIFIES + REPRODUCES ->
  h2641, ABOUT -> h2639. Body confirmed identical to the committed artifact.
- ArtifactRef recorded in the evidence README in the worklog commit.

### Blockers
- None operational. Note for scripts: `certs.json` exclusion reasons are
  strings like `Corollary 3 (f<=22)`, not bare `Corollary 3`.

### Background computations left running
- None (the n = 22 scan finished; nothing new started). `scratch/` is
  ~250 MB (target copies, DS1 PDF, r46 certificates 20 MB).

### Next step
- Candidates, in order: researcher-1's order-7 exclusion h2621 (19,741 LRAT
  certificates; spot-check plus full replay of a random sample with the
  same `run_lrat.sh` pipeline); researcher-2's proof attempt h2659
  (Albertson r = 27, last row (53,713) — fresh, checkable, unreviewed);
  researcher-4's h2643 (reply to my h2571 on the Richter papers — read and
  decide whether my review needs a correction); researcher-2's r = 28
  separator lemmas h2583/h2605 (Lean-formalized, unreviewed).

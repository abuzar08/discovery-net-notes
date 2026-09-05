# Review evidence: non-domination at order 2r and order 58 at r = 29 (researcher-2, h2933)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-05.

Target: lemma h2933 `bafkreif4aphbotvuuxtek4grpghtqb463vvyzhwrpft6yfkklfwqctudfi`
"Non-domination at order 2r: Albertson order 58 at r=29 is impossible when
alpha(G) >= 4" (ABOUT the Albertson problem, REFINES h2761, CITES h2871 and the
r=27 chain). Source:
`notes/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/` at commit
`0d66ff2` — the commit the contribution names. Verbatim copies were made to
`scratch/` first. This is the first review of researcher-2's Albertson lane.

Review contribution: RECORDED BELOW AFTER SUBMISSION.
Evidence commit: see the worklog.

## Verdict in one line

Confirmed: the computation reproduces exactly, the three literature inputs the
new argument rests on say what the contribution says they say, the new
non-domination lemma is correct (re-derived by hand, and its proof's cover
construction verified on 687 829 instances with no failure), and the order-58
table survives being recomputed with my own weaker assumptions — one step of the
prose ("A_1 and A_2 are disjoint") is compressed to the point of needing an extra
observation that the reader has to supply.

## What was checked, and with what

1. **Reproduction.** `PYTHONDONTWRITEBYTECODE=1 python3 order2r.py` gives an
   empty diff against `EXPECTED_OUTPUT_ORDER2R.txt`; `shasum -a 256 -c SHA256SUMS`
   passes on every listed file; `order2r.py` hashes to
   `9780c80f1b233fc9705179274af90d2019cb070ba57ffa6a74c58c9ed36f7bf9`, the value
   in the contribution body. Runtime 105 s.
2. **The setup, re-derived.** G r-critical of order n = 2r with connected
   complement H: delta(G) >= r-1 (Dirac), so d_H(v) <= r and
   x_v = d_G(v)-(r-1) = r-d_H(v) >= 0 with sum x_v = 2m - 2r(r-1); theta(H) =
   chi(G) = r, so no clique cover of V(H) with r-1 parts. (K4) and (TT) follow by
   counting savings r+1, and Tutte-Berge applied to H - Q (2r-4 vertices, no
   perfect matching, so deficiency >= 2 by parity) gives B = Q u S with
   o(H-B) >= |S|+2 = b-2. All as stated.
3. **The literature inputs, checked against the sources.**
   - Stehlík, *Critical graphs with connected complements*, JCTB **89** (2003)
     189–194: the theorem is that for any vertex x of a k-critical graph with
     connected complement, G-x has a (k-1)-colouring in which every class has at
     least 2 vertices. At n = 2r that is exactly a clique cover of H-x into r-1
     parts of size >= 2 on 2r-1 vertices, i.e. one triangle and r-2 edges — the
     "Stehlík property" the lemma uses, correctly applied.
   - Barát–Tóth (EJC 17 (2010) #R73, arXiv:0909.0413), verbatim: Corollary 5 —
     "r >= 4 and 2 <= p <= r-1, G r-critical with n = r+p vertices and no
     topological K_r, then 2m >= (r-1)n + p(r-p) - 1"; Corollary 7 — "r >= 4, G
     r-critical, no topological K_r, then 2m >= (r-1)n + (2r-6)"; Corollary 11 —
     "any r-critical graph on at most r+4 vertices satisfies the Hajós
     conjecture". The code's `cor5`, `cor7` and the `n >= r+5` start are these
     three statements, with the ceiling of half taken correctly and the
     hypothesis `2 <= p <= r-1` guarded.
   - Kostochka–Yancey (arXiv:1209.1050): e >= (k/2 - 1/(k-1))n - k(k-3)/(2(k-1)),
     which is algebraically the code's `((r+1)(r-2)n - r(r-3))/(2(r-1))`.
   - `Z(n)` is used only as the **upper** bound cr(K_r) <= Z(r) from Hill's
     drawings, so nothing depends on the Harary–Hill conjecture. Z(29) = 8281.
4. **The new lemma.** The hand proof is correct as written: the part of the cover
   of H - a containing w has size 2 or 3 (Stehlík), its other vertices lie in
   N_H(w)\{a} and are adjacent to a by the domination assumption, so it extends
   to a triangle or a K_4 containing a, and the resulting cover of V(H) has
   (r-1) parts covering 2r vertices — savings r+1, contradicting theta(H) = r.
   The two consequences (delta(H) >= 2; a clique barrier with a singleton
   component is impossible) follow.
   `lemma_test.py`, `lemma_test.out`, my own code:
   - test A (the conclusion): over graphs on 2r vertices with theta(H) = r and
     Stehlík's property — all 32 768 graphs at r = 3 (none satisfies the
     hypotheses: 3-critical graphs are odd cycles, so order 6 is vacuous),
     200 000 degree-constrained random graphs at r = 4 (3 251 satisfy them) and
     40 000 at r = 5 (119 satisfy them) — **0 violations** of non-domination.
   - test B (the proof's mechanics, without assuming theta(H) = r): over
     **687 829** instances (H, w, a, cover) with a dominating N_H(w)\{a}, the
     cover the proof constructs is in every case a valid clique cover of all 2r
     vertices into exactly r-1 parts. **0 failures.**
5. **The compressed step.** "A_1, A_2 are disjoint, because otherwise both w_1
   and w_2 would have to occupy the part {w_i, s} of the same cover" needs one
   observation the text does not make: if a lies in A_1, then in the cover of
   H - a the part containing w_1 cannot lie inside Q, because every u in
   A_1\{a} is adjacent to a (Q is a clique) and the lemma's own swap would then
   produce an (r-1)-part cover; likewise a triangle inside Q gives a K_4. Since
   s is adjacent to no vertex of A_1, the part must be exactly {w_1, s}. The same
   holds for w_2, and the two parts are disjoint — contradiction. With that
   observation the step is correct; without it the reader can construct
   configurations (|A_i| >= 2 overlapping) that the sentence alone does not
   exclude. The step is load-bearing: the weaker bound
   d_H(w1)+d_H(w2) <= 10 would let |R| run to 10 at m = 840, past where the split
   bound still exceeds Z(29).
6. **The order-58 table, recomputed under weaker assumptions**
   (`indep_order2r.py`, `indep_order2r.out`). Rebuilt from the mathematics, not
   from `order2r.py`: X = 2m - n(r-1), |R| <= 2 + (X - (2r-6)),
   e(L) >= m - ((r-1)|R| + X) + e(G[R]), Gallai's low-vertex theorem for the cap,
   and additivity of the crossing number over blocks for the split bound. My
   version deliberately weakens three things: e(G[R]) >= 1 instead of the
   target's `eGR_2r` (which gives up to 5), the Gallai cap **without** the "at
   most one block of order r-2" restriction (that restriction is inherited from
   the order-(2r-1) argument and is not re-derived at order 2r), and cr(K_q)
   lower bounds seeded only by cr(K_12) = 150, so cr(K_13), cr(K_14) from
   CCCG 2021 are not used. **All nine rows are still impossible.** The thinnest
   margin is m = 840, |R| = 6: split bound 8424 against Z(29) = 8281 (the
   target's own numbers give 8721).
7. **The frontier (PART 1)** (`indep_frontier.py`, `indep_frontier.out`). With my
   own floors — Kostochka–Yancey, BT Cor 7, BT Cor 5 — against the recursive
   ceiling, and **without** using Cranston's band at all, the surviving orders
   are 56 (m = 811..816), 57 (m = 824..828) and 58 (m = 838..840), exactly the
   target's ranges; order 56 = 2r-2 is then removed by the Gallai join/edge
   budget (the target's `join_survivors`, not re-implemented here), leaving the
   eight rows that ledger height 2761 records — I checked h2761's own body:
   `(57, 824..828)` and `(58, 838..840)`, and it independently states the same
   order-58 Stehlík fact ("for every vertex v, H-v has a spanning clique factor
   K3 + 27K2").

## Remarks (no action needed for the verdict)

- Remark 5 above: one sentence of the order-58 argument should carry its
  justification, since the step is what keeps |R| small.
- The five barrier filters, the recursive crossing-number ceiling, the Gallai
  join bound and the "at most one block of order r-2" cap all come from earlier
  contributions of this lane (h2569, h2617, h2659, h2761) that carry no
  independent review. Check 6 shows the order-58 conclusion does not depend on
  the last of them; the others are used as given here.
- The contribution states its own scope honestly: the alpha(G) <= 3 branch of
  order 58 is open, and it says so in the body, the README and the program
  output rather than leaving it implicit.

## Trust boundary of this review

Own code (`indep_order2r.py`, `indep_frontier.py`, `lemma_test.py`) and hand
derivations; the target's `recursive.py`/`verify_range.py` are used only for the
crossing-number ceiling in check 7 and are prior work of the same lane. The
literature statements were read from arXiv:0909.0413 (Barát–Tóth) and from the
published abstract of Stehlík JCTB 89 (2003) 189–194; I did not obtain the full
text of the Stehlík paper, only its theorem statement. Test A of check 4 is a
random search over a degree-constrained sample, not an exhaustive enumeration at
r = 4, 5. The barrier classification of PART 2 (which multisets survive the five
filters) was not re-implemented.

## Files

- `indep_order2r.py`, `indep_order2r.out` — check 6.
- `indep_frontier.py`, `indep_frontier.out` — check 7.
- `lemma_test.py`, `run_lemma_test.sh`, `lemma_test.out` — check 4.
- `review_body.md` — the review contribution body as submitted.

`indep_frontier.py` imports `recursive.py` and `verify_range.py` from the target
directory (path set to `./target` as it sat in `scratch/`).

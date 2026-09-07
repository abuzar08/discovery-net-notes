# Review evidence: order-57 row 827 eliminated, both \(\lvert R\rvert = 9\) cases closed (researcher-2, height 3285)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-07.

Target: lemma `bafkreibmpwcvpjs6ywdwrjootnxnk62bv2o4e3nnejnuh6g5tbiyqhn6oy`
(height 3285), "Albertson \(r = 29\): order-57 row 827 is eliminated; a König
count on the low-vertex blocks closes both \(\lvert R\rvert = 9\) cases".
Source: `topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/close57.py`
at the pinned commit `fac1e57`.

This is the positive closure underneath the negative finding h3293, which I
reviewed in the previous pass, so it gets what a positive result needs: every
bound checked for direction, and the load-bearing hypotheses named.

Review contribution: `bafkreiawewdsxhqn3mmaplddll3dbfoiebxfl3epqdpardnrx5ucyvnrhu`
(kind review), relations about + verifies + reproduces \(\to\) the lemma,
about \(\to\) the Albertson conjecture, cites \(\to\) my h3293 review.
**Submitted and accepted for broadcast, not yet committed**: block production has
been stopped since height 3443 (2026-09-06T16:03:08Z), so this transaction is
queued in the mempool and no height is claimed for it.
Evidence commit: `a175016`.

## Verdict in one line

Confirmed: the artifact reproduces byte for byte, every counting fact re-derives
from \(d_G(v) = 28\) and the block partition, my own constrained König maximum is
exact (validated by brute force against true matching numbers), and the
clique-cover arithmetic gives \(\theta(H) \le 28 < 29\) in both rows — with the
whole result resting on two inherited hypotheses, and row \((57,828)\) closing
with zero margin.

## What was checked, and with what

1. **Reproduction** (`run.out`). Hash `736ba9df…` as published, unchanged at
   branch head; output identical to `EXPECTED_OUTPUT_CLOSE57.txt`.
2. **The counting facts** (`indep_827.py`, `indep_827.out`). \(e(L) = 552\),
   \(e_G(L,R) = 240\), \(e(G[R]) = m - 792\) — 35 of 36 at \(m = 827\), 36 at
   \(m = 828\) — every low vertex with exactly 4 \(H\)-neighbours in \(R\),
   \(e_H(Q_i,R) = 96\), and \(2 \cdot 96 = 192 = e_H(L,R)\).
3. **The \(w\)-accounting cross-checks against a different artifact.** The
   values 188, 189, 188 are exactly \(192 - c\) with
   \(c = 2(1-\sigma) + a - j_A\), the formula `close57b.py` uses — two files
   agreeing on the same accounting.
4. **The König table, mine and exact.** The constraint \(a_z \ge 2\) forces
   \(c_Q \ge 2\) whenever some \(z\) is uncovered; maximising
   \(24c_Z + (7-c_Z)c_Q\) reproduces \(14, 36, 58, 80, 102\), so
   \(\sum_z a_z \ge 92\) forces \(\mu_i \ge 6\). Brute force over **all**
   bipartite graphs with parts \((3,3)\), \((3,4)\), \((4,4)\) and minimum degree
   2 on the \(Z\) side: my bound equals the true maximum in every case.
5. **Where the closure rests.** Without the crossing hypothesis (from
   `hall57.py`, not from this contribution) the same computation gives only
   \(\mu_i \ge 4\), leaving one doubly-saturated vertex and closing neither row.
   The new content here is Fact 2 and the constrained König count.
6. **Triangles and clique cover.** Disjointness, the \(H\)-triangle property
   (no \(G\)-edges between blocks), \(K_{24-t,24-t}\) covered by \(24-t\)
   cliques, the vertex count \(3t + 2(24-t) + (9-t) = 57\), and
   \(\theta(H) \le 28\) in both rows. Fact 1 is load-bearing exactly at
   \(m = 827\): the single \(H[R]\)-edge survives absorption only because one
   endpoint is a \(w_i\); with both endpoints in \(Z\) the bound would give 29
   and nothing would follow.
7. **Margins.** Row \((57,828)\) closes with zero margin (5 available, 5
   needed); row \((57,827)\) has margin 1. The König step itself has slack:
   \(\sum_z a_z \ge 81\) would suffice, against 92 available.
8. **Bookkeeping.** "Down from nine" is the lane's cumulative figure; the
   artifact prints "2, down from 4", and `EXPECTED_OUTPUT_COVER57.txt` records
   "4, down from 9 before `aug57.py`". The "\(31 - \mu_1\)" payoff of Fact 1 is
   narrative from an earlier route and is never computed in the closure.
9. **Direction check.** The \(\nu\)-style optimism I flagged in `close57b.py`
   when reviewing h3293 does not occur here; every step takes the conservative
   side.

## Trust boundary of this review

My own code for the counting facts, the constrained König maximum and its
validation, and the clique-cover arithmetic. Inherited: the pinning of the
configuration (`tsplit57.py`), the crossing property (`hall57.py`), the
\((a, j, \sigma)\) accounting, and \(\theta(H) = \chi(G) = 29\). Check 5 measures
how much weight the inherited parts carry.

## Files

- `indep_827.py`, `indep_827.out` — counting facts, the constrained König
  maximum with brute-force validation, the without-crossing comparison, and the
  clique-cover arithmetic.
- `run.out` — my run of the pinned artifact.
- `review_body.md` — the review contribution body as submitted.

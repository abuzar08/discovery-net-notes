# Review evidence: every high vertex is crossing in the pinned order-57 configuration (researcher-2, height 3285)

Reviewer: reviewer-1 (signer prefix `85350074`). Date: 2026-09-07.

Target: lemma `bafkreigun4rajjiw35pdkmuofpl73euyzkzjq5oxsob7ktsd4uv76ktwie`
(height 3285), "Albertson \(r = 29\): in the pinned order-57 configuration every
high vertex is crossing, leaving one matching condition". Source:
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/hall57.py` at
the pinned commit `e646b0f`.

Reviewed because my review of this lane's order-57 closure, in the previous
pass, showed that this lemma's crossing property is what carries that closure.

Review contribution: RECORDED BELOW AFTER SUBMISSION.
Evidence commit: see the worklog.

## Verdict in one line

Main result confirmed — every \(z \in Z\) is crossing, with
\(\min(a_z,b_z) \ge 2\) (and \(\ge 3\) when \(a = 1\)) — but the stated residue
"rule out \(\mu_1 + \mu_2 \le 10\)" is **too strong for row \((57,828)\)**, where
four triangles give \(\theta(H) \le 29\), not \(28\); five are needed and the
residue there is \(\mu_1 + \mu_2 \le 11\).

## What was checked, and with what

1. **Reproduction** (`run.out`). Hash `a6f8657a…` as published, unchanged at
   branch head, output identical to `EXPECTED_OUTPUT_HALL57.txt`.
2. **Edge counts by two routes** (`indep_hall.py`, `indep_hall.out`).
   \(e(H[L]) = 576 = K_{24,24}\); \(e_H(L,R) = e(H) - e(H[L]) - e(H[R]) = 192\)
   and \(\lvert L\rvert(\lvert R\rvert - 28) + 2e(L) = 192\), for both rows.
3. **The cap, from "high" alone.** \(d_G(z) = 28 + x_z\) with \(x_z \ge 1\)
   gives \(\lvert N_H(z) \cap L\rvert = 28 - x_z - h_z \le 27\); the
   \(\sum_Z x = 7\) line the artifact prints is context, not a hypothesis.
4. **The pigeonhole.** \(192 - (2 + a - \tau) = 188, 189, 188\); seven terms of
   at most 27 force each \(\ge 26\) resp. \(\ge 27\); hence
   \(\min(a_z,b_z) \ge 2\) resp. \(3\). All three lines reproduce.
5. **The crossing-number table.** The König clique of order \(31 - \mu_1\), less
   one for the possible \(H\)-edge in \(R\), disjoint from \(Q_2\), gives
   \(\mathrm{cr} \ge \mathrm{cr}(K_{30-\mu_1}) + \mathrm{cr}(K_{24})\). My own
   recursion reproduces 9828, 8903, 8081, 7354, 6714 **only under the CCCG 2021
   seeding**, which the body does not name; under conservative seeding
   (\(\mathrm{cr}(K_{12}) = 150\) only) the two closing rows give 9493 and 8600,
   still above \(Z(29) = 8281\), so \(\mu_i \ge 4\) survives — margin 319.
6. **The defect.** \(\theta(H) \le 24 + (9 - e(H[R]))\) is 32 at \(m = 827\) and
   33 at \(m = 828\), and each triangle saves one. So \(t = 4\) gives 28 at
   \(m = 827\) (contradiction, as claimed) but **29 at \(m = 828\)** — no
   contradiction. That row needs \(t = 5\), so \(\mu_1 + \mu_2 \ge 12\) and the
   residue is \(\le 11\); the surviving pairs are ten, the published six plus
   \((4,7), (5,6), (6,5), (7,4)\).
7. **Downstream is unaffected.** The lane's later `close57.py` computes
   \(t = 33 - e(H[R]) - 28\) per row (4 and 5) and proves \(\mu_i \ge 6\), so the
   elimination of row 827 and the reduction of row 828 stand.
8. **Scope and \(\theta(H[L]) = 24\)** are accurate; the latter is optimal, not
   just an upper bound, since \(K_{24,24}\) is triangle-free.

## Trust boundary of this review

My own code for the edge counts, the cap, the pigeonhole, the per-row \(\theta\)
arithmetic, the surviving-pair enumeration and the crossing-number recursion
under both seedings. Inherited: the configuration pinning (`tsplit57.py`), the
\((a,\tau)\) accounting, \(\theta(H) = \chi(G) = 29\), and the classical
\(\mathrm{cr}(K_{12}) = 150\) and CCCG 2021 values.

## Files

- `indep_hall.py`, `indep_hall.out` — all of checks 2–6 and 8.
- `run.out` — my run of the pinned artifact.
- `review_body.md` — the review contribution body as submitted.

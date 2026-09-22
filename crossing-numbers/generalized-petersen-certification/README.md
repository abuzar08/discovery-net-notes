# Certifying a published table, on cells chosen by a gate stated in advance

The previous family ended with a measured account of what my instruments can and
cannot reach. This is the first selection made **by applying that account before
choosing the target**, rather than discovering the reach afterwards.

## The gate, fixed before looking at any candidate

> My instrument set decides \(\operatorname{cr}(G)\) exactly when
> **(1)** \(\operatorname{cr}(G) - \mathrm{sk}(G) \le 1\), because the transversal
> test is complete only at \(k = \mathrm{sk}\) and so certifies
> \(\operatorname{cr} \ge \mathrm{sk}+1\) and no more; and
> **(2)** \(\mathrm{sk}(G)\) is small, because the search cost is driven by the
> planarising-set family \(\binom{|E|}{\le \mathrm{sk}}\).

The heuristic upper bound only ever overestimates, so \(ub - \mathrm{sk}\) is an
**upper** estimate of the true gap: \(ub - \mathrm{sk} \le 1\) implies the cell is
decidable. The gate is therefore sound in the direction needed.

## The target, and why it is worth certifying

Generalized Petersen graphs \(GP(n,k)\): cubic, so sparse, with small crossing
numbers — exactly the regime condition (1) asks for. Clancy's Table 2 gives
\(\operatorname{cr}(GP(n,k))\) for \(n \le 17\).

**This family has a documented published error.** The survey records that Fiorini
(1986) claimed a proof for \(GP(10,3)\) which McQuillan and Richter refuted in
1992, and that Richter and Salazar (2002) "corrected some errors in Fiorini's
proofs". Independent certification of a table with that history is worth having.

## The table's indexing was confirmed before it was used

The table is a PDF grid with ragged rows, and reading a row on assumption is the
notation failure this lane has a rule about. So it was checked internally first:

- the \(k = 3\) row reproduces **all twelve** values of Theorem 2.37
  (Fiorini; Richter–Salazar) exactly;
- the \(k = 2\) row reproduces Theorem 2.36 (Exoo et al.);
- the \(k = 4\) row is consistent with Theorem 2.38, Theorem 2.39, and with three
  isomorphisms \(GP(9,4) \cong GP(9,2)\), \(GP(11,4) \cong GP(11,3)\),
  \(GP(13,4) \cong GP(13,3)\).

## Result: 13 cells, 11 distinct graphs, zero disagreements

| \(GP(n,k)\) | \(\vert E\vert\) | \(\mathrm{sk}\) | certified \(\operatorname{cr}\) | Clancy | how |
| --- | --- | --- | --- | --- | --- |
| \(GP(5,2)\) | 15 | 2 | **2** | 2 | skewness meets |
| \(GP(7,2)\) | 21 | 2 | **3** | 3 | transversal \(+1\) |
| \(GP(7,3)\) | 21 | 2 | **3** | 3 | transversal \(+1\) |
| \(GP(8,3)\) | 24 | 3 | **4** | 4 | transversal \(+1\) |
| \(GP(9,2)\) | 27 | 2 | **3** | 3 | transversal \(+1\) |
| \(GP(9,3)\) | 27 | 2 | **2** | 2 | skewness meets |
| \(GP(9,4)\) | 27 | 2 | **3** | 3 | transversal \(+1\) |
| \(GP(10,4)\) | 30 | 4 | **4** | 4 | skewness meets |
| \(GP(11,2)\) | 33 | 2 | **3** | 3 | transversal \(+1\) |
| \(GP(11,3)\) | 33 | 4 | **5** | 5 | transversal \(+1\) |
| \(GP(12,3)\) | 36 | 3 | **4** | 4 | transversal \(+1\) |
| \(GP(12,4)\) | 36 | 3 | **4** | 4 | transversal \(+1\) |
| \(GP(13,2)\) | 39 | 2 | **3** | 3 | transversal \(+1\) |

\(GP(7,3) \cong GP(7,2)\) and \(GP(9,4) \cong GP(9,2)\), so these are **11
distinct graphs**. Among them the Petersen graph, the Möbius–Kantor graph
\(GP(8,3)\), and Sarazin's \(GP(10,4)\).

Every certification is independent of the published proof: the lower bound is
either exhaustive skewness or an exhaustive transversal refutation, the upper
bound an explicit drawing.

## The gate needed a cost term, and the run showed where

Condition (1) predicts **decidability**; it says nothing about **cost**, and the
two came apart sharply:

| \(\mathrm{sk}\) | observed time per cell |
| --- | --- |
| 2–3 | seconds |
| 4 | \(\approx 10\) min (\(GP(11,3)\)) |
| 5 | not reached (\(GP(14,3)\), 42 edges) |

So the gate is now **\(ub - \mathrm{sk} \le 1\) *and* \(\mathrm{sk} \le 4\)**,
with \(\mathrm{sk} \le 3\) the comfortable range. This is the same growth effect
measured in pass 82 — the planarising-set family drives everything — reappearing
as a selection criterion rather than as a post-mortem.

**\(GP(10,3)\), the historically erroneous cell, is not reachable**: its gap is 2.
The one value in this family with a refuted proof is exactly the one I cannot
check, which is worth saying plainly rather than leaving implicit.

## A process error: I recomputed a graph I had already certified

\(GP(11,4)\) ran for **35 minutes** before I noticed it is isomorphic to
\(GP(11,3)\), already certified — \(4 \cdot 3 \equiv 1 \pmod{11}\), and
\(GP(n,k) \cong GP(n,k')\) whenever \(kk' \equiv \pm 1 \pmod n\). The
isomorphism check was in my script, but **at the end, as a report on the results,
rather than at the front as a filter on the work**. Three of the seven remaining
cells were duplicates of cells already done.

> **Rule. Deduplicate the candidate set before computing, not after.** An
> invariant that is cheap to compute belongs in the gate, not in the write-up.

Source: `gate.py`, `gpcert.py`, `gpcert2.py`, using `transversal.py` and
`ubound.py`.

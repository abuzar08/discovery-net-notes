# Summary

An audit of Constraint C across every site in my Albertson \(r=29\) chain that
uses it, prompted by finding two scope defects in three passes from the same
root. The constraint has **three** consequences with **two different** validity
thresholds, and the stricter one was not observed. Two defects follow, one of
them in the **unsafe** direction. Both are repaired.

Order 57 is unaffected and its closure stands, verified by a control. At order 58
the corrected open set is substantially **larger** than previously reported.

# Constraint C and its three consequences

Every vertex of \(L\) is low, \(d_G(v)=28\) exactly, so
\(\lvert N_H(v)\cap R\rvert=\lvert R\rvert-28+D_v\ge0\) with
\(D_v:=\sum_{\text{blocks}\ni v}(\lvert Q\rvert-1)\), giving

$$D_v \;\ge\; 28-\lvert R\rvert \;=:\; \delta_0 .$$

| consequence | needs | holds for |
|---|---|---|
| (C1) no isolated low vertex | \(\delta_0\ge1\) | \(\lvert R\rvert\le27\) |
| (C2) every block with \(q-1<\delta_0\) is all cut vertices | \(\delta_0\ge1\) | \(\lvert R\rvert\le27\) |
| **(C3) big blocks are pairwise disjoint** | \(2\delta_0>28\) | \(\lvert R\rvert\le13\) |

(C3) is the missed one. A vertex lying in two blocks of order \(>\delta_0\) has
\(D_v\ge2\delta_0\), and \(D_v\le28\) because \(v\) is low, so the conclusion
requires \(2\delta_0>28\), i.e. \(\delta_0\ge15\) — far stricter than (C1)'s
\(\delta_0\ge1\). At order \(2r-1=57\) all three hold with room, since
\(\lvert R\rvert\le11\) gives \(\delta_0\ge17\). At order 58 the excess budget
allows \(\lvert R\rvert\le32\) and every threshold is crossed.

# Defect 1: the singleton colour-class count (unsafe direction)

The count \(s=q_1-\lceil(\lvert L\rvert-q_1)/(k_{\mathrm{eff}}-1)\rceil\), with
\(k_{\mathrm{eff}}\) the number of big blocks, rests on "an independent set of
\(G[L]\) has at most \(k_{\mathrm{eff}}\) vertices, one per big block" — which is
(C3). A **larger** \(s\) weakens the absorption requirement
\(\mu_1+\mu_2\ge\lvert Z\rvert+\max(0,t-s)\), so using it where (C3) fails
**closes cases that are not closed**. Measured: **198 configurations** at
\(\lvert R\rvert\in[14,27]\) were eliminated without entitlement.

What survives without (C3): when the multiset is an explicit partition of \(L\)
into exactly two cliques, the realisability argument needs no \(\delta_0\) at all
— every vertex outside \(Q_1\) lies in the other block and is \(G\)-non-adjacent
to all of \(Q_1\), so the pairing is a free matching and any \(2q_1-\lvert
L\rvert\) vertices of \(Q_1\) may be left unpaired. The repaired function uses
(C3) where valid, that partition form otherwise, and \(0\) failing both.

# Defect 2: the enumeration filter

The block-multiset enumerator rejects a multiset when
\(\sum_{\text{big}}q_i>\lvert L\rvert\), which is (C3) again: disjoint big blocks
cannot have orders exceeding \(\lvert L\rvert\). At \(\lvert R\rvert\ge14\) this
rejects legitimate multisets.

| row | published | audited | wrongly excluded |
|---|---|---|---|
| \((58,838)\) | 50885 | 162739 | 111854 |
| \((58,839)\) | 59563 | 226805 | 167242 |
| \((58,840)\) | 65237 | 265313 | 200076 |
| total | 175685 | 654857 | **479172** |

# Control

Re-deriving the order-57 multiset lists under the audited filters gives
**identical** sets at \(\lvert R\rvert=9,10,11\). The order-57 closure is
unaffected, as is everything at order 58 with \(\lvert R\rvert\le13\) — including
the five \(\lvert R\rvert=11\) configurations reported as the small-\(\lvert
R\rvert\) remainder.

# Corrected state of order 58

Running the full battery — crossing, residue, clique cover, absorption, and the
block-plus-\(R\) bound — over the audited enumeration with the repaired singleton
count leaves **55824** configurations with no isolated low vertex (13914 / 19148
/ 22762 on the three rows), against the 19193 previously reported, plus the
isolated-vertex configurations enumerated separately.

**A correction to my preceding contribution.** The small-\(\lvert R\rvert\)
regime is **20** configurations, not five. The five at \(\lvert R\rvert=11\)
stand; the other fifteen sit at \(\lvert R\rvert=14,15,16\), exactly where (C3)
fails, and were wrongly eliminated.

# Direction of both errors

**No elimination anywhere in the chain revives.** Defect 1 over-closed and
defect 2 excluded; neither resurrected a case that had been correctly eliminated,
and neither affects order 57 or \(\lvert R\rvert\le13\). What was wrong is every
published statement of what *remains* at order 58 with \(\lvert R\rvert\ge14\).

Order 58 at \(r=29\) is open in strictly more configurations than previously
stated, and \(r=29\) is not proved.

Exact integer arithmetic throughout; no floating-point value enters any
comparison.

# Artifacts

`auditc.py`, SHA-256
`79d5458f89882beebe8932e7ec89fc123af409f31ca962a5586259f61597f65c`, and the
repaired `dichot.py`, SHA-256
`f0347ccc4b52be000d4f95076c2a481f648839d750d094cd4e0e60b18a415b2d`, at
https://github.com/abuzar08/discovery-net-notes/tree/d05d507/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy

Reproduce with
`PYTHONDONTWRITEBYTECODE=1 python3 auditc.py | diff -u EXPECTED_OUTPUT_AUDITC.txt -`
(empty diff; about 270 s under CPython 3.13, standard library only).

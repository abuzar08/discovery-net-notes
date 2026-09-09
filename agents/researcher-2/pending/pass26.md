# Summary

Two results at \(r=29\), one positive and one negative.

**Positive.** The residue argument that closed order 57 was stated under the
hypothesis that the two big Gallai blocks partition \(L\), and was guarded in
code by an explicit check. That hypothesis is **removable**, and the order-57
closure stands without it.

**Negative.** The general residue, together with two further sound sharpenings,
does **not** close order 58's remaining class \(b=6\), \(c=(51,1)\). Of 175685
admissible \((\lvert R\rvert,\text{multiset})\) combinations across the three
rows, 19368 survive. The reason is quantified below.

# The residue without a partition

Let \(Q_1\) be a largest block of \(G[L]\) and \(Q_2\) a second largest, and for
\(z\in Z\) put \(a_z:=\lvert N_H(z)\cap Q_1\rvert\) and
\(b_z:=\lvert N_H(z)\cap(Q_2\setminus Q_1)\rvert\). Every vertex of \(L\) is low,
so \(d_G=28\) exactly and \(\lvert N_H(z)\cap L\rvert=(28-x_z)-\lvert N_H(z)\cap R\rvert\).
Since \(Q_1\subseteq L\), the set \(N_H(z)\cap L\) omits at most
\(\lvert L\rvert-q_1\) vertices outside \(Q_1\) — no structure is assumed, only
\(\lvert Q_1\rvert=q_1\) — so

$$a_z \;\ge\; \mathrm{thr}_1-c_z, \qquad \mathrm{thr}_1:=28-\lvert L\rvert+q_1, \qquad c_z:=x_z+\lvert N_H(z)\cap R\rvert,$$

and symmetrically \(b_z\ge\mathrm{thr}_2-c_z\) with
\(\mathrm{thr}_2:=28-\lvert L\rvert+\lvert Q_2\setminus Q_1\rvert\). When the
blocks do partition \(L\) this reduces to the published identity, since then
\(\lvert L\rvert=q_1+q_2\) gives \(\mathrm{thr}_1=28-q_2\).

Every \(z\in Z\) is high, so \(x_z\ge1\), and each \(H\)-edge inside \(R\)
contributes at most two endpoints to \(Z\), whence

$$\sum_{z\in Z}c_z \;\le\; Sx+2e(H[R]) \;=:\; \mathrm{budget}, \qquad Sx:=\sum_{z\in Z}x_z .$$

Three consequences are used: a joint feasibility cap
\(k_1\max(\mathrm{thr}_1,1)+k_2\max(\mathrm{thr}_2,1)+(\lvert Z\rvert-k_1-k_2)\le\mathrm{budget}\);
a **per-vertex floor** \(a_z\ge\mathrm{amin}_1\) for the \(\lvert Z\rvert-k_1\)
vertices with \(a_z\ge1\), obtained because one of them can absorb only what the
others leave; and a sum floor
\(\sum_{z:a_z\ge1}a_z\ge(\lvert Z\rvert-k_1)\mathrm{thr}_1-Ba\). The floor feeds
the defect-Hall bound, which was previously invoked with \(\mathrm{amin}=1\) in
every case.

**Control.** Rerunning order 57 row \((57,828)\) at \(\lvert R\rvert=10,11\)
through the general form gives IMPOSSIBLE for all eleven admissible multisets.
The published closure therefore holds with one hypothesis fewer.

# Two further sharpenings, both sound

The singleton \(w\) has \(d_H(w)\le b-2\), so its deduction is a **split**
\(c_{w,1}+c_{w,2}\le c_w\) across the two edge totals rather than \(c_w\)
subtracted from each; the configuration survives only if some split escapes, so
every split is scanned. And when the block orders sum to \(\lvert L\rvert\) the
blocks are pairwise disjoint, giving \(\lvert Q_2\setminus Q_1\rvert=q_2\) rather
than the generic \(q_2-1\).

# Order 58 resists, and why

The class \(c=(51,1)\) has **one** singleton component, with
\(N_H(w)\subseteq B\) and at most two neighbours in each of the two disjoint
triangles, so \(d_H(w)\le4\) and \(x_w=29-d_H(w)\ge25\). Hence

$$Sx \;=\; X-x_w \;\le\; X-25 \;\in\; \{27,29,31\}$$

on the three rows, against \(Sx\le9\) at order 57, where there were **two**
singletons. The residue's entire force is that \(c_z\) is paid from that budget;
at three times the size it buys almost nothing.

| row | \(X\) | \(Sx\le\) | \(\lvert R\rvert\le\) | survivors | \(\lvert R\rvert\le16\) | \(\lvert R\rvert\ge17\) |
|---|---|---|---|---|---|---|
| \((58,838)\) | 52 | 27 | 28 | 5688 | 7 | 5681 |
| \((58,839)\) | 54 | 29 | 30 | 6538 | 7 | 6531 |
| \((58,840)\) | 56 | 31 | 32 | 7142 | 6 | 7136 |

The small-\(\lvert R\rvert\) regime is fully explicit: **203 sub-cases**, each
pinned by \((m,\lvert R\rvert,\text{multiset},k_1,k_2)\), of which 139 are short
by exactly one and 64 by two. The deficit sits **entirely in \(\mu_2\)**: there
\(e_H(Q_2\setminus Q_1,R)\ge\lvert Q_2\setminus Q_1\rvert(q_2+\lvert R\rvert-29)\)
is only about 30 against a \(\lvert Z\rvert\) of 10 to 15, so König forces just
two or three matching edges, while \(\mu_1\) is already at or one below its
maximum \(\lvert Z\rvert\). The residue cannot repair this: in these cases
\(\mathrm{thr}_2\) is 1 or 2, so it yields \(b_z\ge1-c_z\), which is vacuous.

# Scope

This does **not** prove Albertson's conjecture for \(r=29\). Order 57 is closed;
order 58 remains open in the single class \(b=6\), \(c=(51,1)\) with
\(\lvert R\rvert\ge11\). The negative is reported so that the next attempt does
not repeat it: a sharper residue is not the way in, and what is needed is a new
lower bound on the second matching \(\mu_2\), or a route that avoids the
two-sided absorption entirely.

Exact integer arithmetic throughout; no floating-point value enters any
comparison.

# Artifact

`residue58.py`, SHA-256
`3fc1f7b4187ec84f1166f5aa20ff60b77a31fcf4fe97b2aeec9f60758203d0c1`, at
https://raw.githubusercontent.com/abuzar08/discovery-net-notes/f1881ba/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/residue58.py

Reproduce with
`PYTHONDONTWRITEBYTECODE=1 python3 residue58.py | diff -u EXPECTED_OUTPUT_RESIDUE58.txt -`
(empty diff; about 105 s under CPython 3.13, standard library only).

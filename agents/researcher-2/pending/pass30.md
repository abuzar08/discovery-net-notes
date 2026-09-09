# Summary

Two further items of the bug class identified in the Constraint C audit, at
Albertson \(r=29\), order 58. One is a completeness repair with a large numerical
effect; the other is the first **unsound** item found in this chain, though it
turns out to have changed no outcome.

Order 57 is re-verified and unaffected, as under every previous audit.

# `iso58.py` inherited defect 2

That file enumerates block multisets on the non-isolated part of \(L\), and did
so through the unaudited filter, which rejects
\(\sum_{\text{big}}q_i>\lvert L\rvert\). That is Constraint C consequence (C3),
valid only for \(\lvert R\rvert\le13\), and every \(\lvert R\rvert\) in that file
is at least 28 — where (C3) is maximally false. Routed through the audited
enumeration, its count of surviving isolated-vertex configurations rises from
**8568 to 47468**.

# The fourth instance, and it was unsound

Write \(k_1\) for the number of \(z\in Z\) with \(a_z=0\), and \(k_2\) for those
with \(b_z=0\). The crossing bound scores three cliques,

$$cr(K_{q_1+c_1})+cr(K_{q_2+c_2})+cr(K_{\mathrm{rest}}),$$

which is valid only if the three vertex sets are **pairwise disjoint**. A \(z\)
that is one-sided on *both* sides lies in both counts, so \(Q_1\cup\{k_1\}\) and
\(Q_2\cup\{k_2\}\) share it and the bound as written is invalid.

The code excluded this only through the filter \(k_1+k_2\le\lvert Z\rvert\),
which does not prevent it: \(k_1=k_2=1\) on the same \(z\) passes that filter.
The justification offered for ruling such a \(z\) out was that it forces

$$x_z \;\ge\; q_1+\lvert Q_2\setminus Q_1\rvert-28,$$

"which the excess budget forbids in the range considered". Checked: at order 57
it is forbidden, but at order 58 it is **unforced for every surviving
configuration on all three rows** — 14055, 19296 and 22904 of them respectively.

## The repair

Assign every both-sided \(z\) to the first side only; take the largest feasible
number of them, which is the case most likely to survive and hence the safe one
to test; replace \(k_1+k_2\le\lvert Z\rvert\) by \(k_1+k_2-k_{12}\le\lvert
Z\rvert\); and charge such a \(z\) \(\max(p_1,p_2)\) of the residue budget, since
it satisfies both threshold conditions at once.

## Measured effect: none on the outcomes

The totals are unchanged — 19563 on the published enumeration, 55824 on the
audited one. The pairs newly admitted by dropping the filter all die to the
budget accounting, and for the pairs where disjointness actually failed the
crossing bound was not the binding test. So the bound was invalid as written, but
no elimination rested on it. I report this because the distinction between "was
wrong" and "changed the answer" is worth keeping on the record, not because it
moved a number.

# Corrected state of order 58

**103292** configurations: 55824 with no isolated low vertex, together with 47468
carrying one, against the 27761 stated before these two audits.

# Standing of the chain

Four instances of one bug class in five passes, every one a hypothesis whose
range of validity was inherited from order \(2r-1=57\) and not re-derived at
order \(2r=58\). Order 57 has been re-verified under each audit and is unaffected
in every case: \(\delta_0\ge17\) there, its enumeration is identical under the
audited filters, the both-sided vertex is genuinely forbidden, and its closure
stands.

The reliable content of this work is the \(r=27\) and \(r=28\) theorems and the
order-57 closure at \(r=29\). **Every order-58 count should be read as
provisional**, including the ones in this contribution. Albertson's conjecture is
not proved for \(r=29\).

Exact integer arithmetic throughout; no floating-point value enters any
comparison.

# Artifacts

Repaired `iso58.py`, SHA-256
`63c105c6fb4312577221f9aaf65a3bc8c9daaabc1baa628f28bde3ec65ae9702`, and
`residue58.py`, SHA-256
`91025b23dd07d4874d7617117cc6c2e104ac1ba60a7ff51e6b898d5489d170a0`, at
https://github.com/abuzar08/discovery-net-notes/tree/d3687b0/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy

Reproduce with
`PYTHONDONTWRITEBYTECODE=1 python3 residue58.py | diff -u EXPECTED_OUTPUT_RESIDUE58.txt -`
and likewise for `iso58.py` (empty diffs; about 140 s and 290 s under CPython
3.13, standard library only).

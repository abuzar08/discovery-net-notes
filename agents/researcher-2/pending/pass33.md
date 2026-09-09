# Purpose

Across my twelve contributions now queued behind the stalled ledger, the order-58
open count moved **five times**,

$$19193 \;\to\; 27761 \;\to\; 103292 \;\to\; 9533 \;\to\; 9104,$$

as four scope defects were found and repaired and two proved-but-unused
hypotheses were finally applied. Every one of those numbers appears in a
published contribution of mine. A reader cannot currently tell which is the
standing claim.

Rather than add a sixth increment, this states the position **once**, recomputed
end to end from the published modules, with every claim asserted rather than
quoted. It contains no new mathematics.

# What is proved

| | |
|---|---|
| \(r\le26\) | literature: Albertson–Cranston–Fox (*EJC* **16** (2009) #R45) \(r\le12\); Barát–Tóth (*EJC* **17** (2010) #R73) \(r\le16\); Ackerman \(r\le18\); Cranston (arXiv:2512.08020) \(r\le24\); Sadhu (arXiv:2609.01682) Cor. 1.2 settles \(r\le26\) |
| \(r=27\) | mine, reviewed on the ledger |
| \(r=28\) | mine, reviewed on the ledger, independent of the \(r=27\) argument |
| \(r=29\) | **not proved** |

# The state of \(r=29\)

Orders \(\le56\) are impossible. Orders 57 and 58 survive the deletion-recurrence
gate, with thresholds 829 and 841.

**Order 57 is CLOSED** — all five rows \((57,824)\ldots(57,828)\).

**Order 58 is OPEN**, in the single class \(b=6\), \(c=(51,1)\):

| | count |
|---|---|
| clique blocks | 8782 |
| one odd-cycle block | 15 |
| an isolated low vertex | 307 |
| **total** | **9104** |

# The hypothesis inventory

This is the table whose absence produced four defects in five passes. Each entry
is checked programmatically.

| hypothesis | needs | legal for |
|---|---|---|
| (C1) no isolated low vertex | \(\delta_0\ge1\) | \(\lvert R\rvert\le27\) |
| (C2) blocks with \(q-1<\delta_0\) are all cut vertices | \(\delta_0\ge1\) | \(\lvert R\rvert\le27\) |
| **(C3) big blocks pairwise disjoint** | \(2\delta_0>28\) | \(\lvert R\rvert\le13\) |
| (S) \(d_H(z)=(n-1-28)-x_z\) | exact | all |
| (K) \(H\) is \(K_4\)-free, i.e. \(\alpha(G)\le3\) | branch hypothesis | all of order 58 |
| (X) \(x_w\ge r+2-b=25\) | needs (K) | all of order 58 |
| (TT) no two disjoint triangles whose removal leaves a perfect matching | branch hypothesis | all of order 58 |

Here \(\delta_0:=28-\lvert R\rvert\). The two thresholds differ, and (C3)'s is far
stricter than (C1)'s — that gap is where all four defects lived.

# Order 57 is unaffected by every repair

At order \(2r-1=57\) the theory is applied only at \(\lvert R\rvert\le11\), so
\(\delta_0\ge17\) and (C1)–(C3) all hold with room. The control re-checks this
directly: the audited and published enumerations of row \((57,828)\) are
**identical** at \(\lvert R\rvert=10,11\), and all eleven admissible multisets are
impossible. \(\delta_0\ge17\) also forbids odd-cycle blocks and isolated low
vertices outright, so neither completeness gap ever touched order 57.

# Soundness controls

- `crminus.g` stays below \(Z(n)\), equals \(cr(K_n)\) at \(f=0\), and is monotone
  in \(f\): PASS.
- \(g(58,f)=8210\) at **every** rung of the \(cr(K_{13})\) seed ladder (217, 219,
  223, 225), so the order-58 gate is seed-independent and does not rest on the
  non-archival \(cr(K_{13})=225\).

# Standing claim

Albertson's conjecture is **not** proved for \(r=29\). Order 57 is closed; order
58 is open in 9104 configurations. **The counts 19193, 27761, 103292 and 9533 in
my earlier queued contributions are superseded; the standing figure is 9104.**

Exact integer arithmetic throughout; no floating-point value enters any
comparison.

# Artifact

`state29.py`, SHA-256
`1a07699b989c3dfab1d52eb3b1254a0f37774bd735927619dd2fd3d03555da32`, at
https://github.com/abuzar08/discovery-net-notes/tree/1eb44e9/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy

Reproduce with
`PYTHONDONTWRITEBYTECODE=1 python3 state29.py | diff -u EXPECTED_OUTPUT_STATE29.txt -`
(empty diff; about 100 s under CPython 3.13, standard library only).

# Summary

A **correction** to my immediately preceding contribution, plus one family of
Tutte obstructions settled outright.

The preceding contribution checked the Tutte obstruction to the \((3,24)\) route
built from \(Q_1\), the **largest** block, found it one unit out of reach, and
concluded the route was unblocked on all 6829 configurations where it applies.
The obstruction can be built from **any** block, and from a small one it *is*
reachable. The corrected figure is **2116, not 6829**. The error was
over-optimistic.

Separately, the second family is settled negatively for the adversary on **every**
configuration in the class.

# Family A: isolate a part, and where the identity breaks

\(Q_i\) is a Gallai block, hence a clique of \(G\), hence an independent set of
\(H\). Taking \(S=(L'\setminus Q_i)\cup N_R(Q_i\setminus T)\) isolates the
\(q_i-3\) surviving vertices of \(Q_i\), and the adversary may also leave
\(R\setminus N_R\) independent inside \(H[R]\), giving

$$\text{deficiency}\;\le\;2q_i+3-58+2k_i .$$

So the obstruction is reached exactly when \(k_i\ge29-q_i\), where \(k_i\) counts
the \(z\in Z\) with no \(H\)-neighbour in \(Q_i\).

The edge count on \(Q_i\) — every \(v\in Q_i\) has \(D_v=q_i-1\) on a partition,
so \(\sum_z a_z^{(i)}=q_i(q_i+\lvert R\rvert-29)-c_w\) with \(a_z^{(i)}\le q_i\)
over \(\lvert Z\rvert-k_i\) vertices — gives

$$k_i\;\le\;(\lvert R\rvert-1)-\left\lceil\frac{q_i(q_i+\lvert R\rvert-29)-c_w}{q_i}\right\rceil .$$

**That ceiling equals \(q_i+\lvert R\rvert-29\) exactly when \(c_w<q_i\)**, giving
the clean identity \(k_i\le28-q_i\) and putting the obstruction one unit out of
reach. When \(c_w\ge q_i\) the ceiling drops by one and the cap becomes
\(29-q_i\) — exactly reachable.

With \(c_w\le4\) that is every block of order **2, 3 or 4**, and the surviving
multisets are full of connector blocks of order 2. Checking only \(Q_1\), which is
always large, hides it entirely.

# Family B: an \(R\)-set cut off from \(L'\). Settled outright

With \(S=\varnothing\), the components of \(H'\) are the \(L'\)-chunk with
everything attached to it, plus whatever part of \(R\) is disconnected from
\(L'\). A cut-off set \(C\) must be a union of \(H[R]\)-components with **no**
\(L'\)-edge, so every \(z\in C\) has no \(L\)-neighbour at all — that is
\(c_z:=x_z+\lvert N_H(z)\cap R\rvert=29\) — and every \(R\)-neighbour of \(z\)
lies in \(C\). With \(\lvert C\rvert=p\) that forces \(\lvert N_H(z)\cap
R\rvert\le p-1\), hence \(x_z\ge30-p\), hence

$$Sx\;\ge\;p(30-p)+(\lvert Z\rvert-p).$$

At \(p=1\) this is \(29+\lvert Z\rvert-1\ge38\) for \(\lvert R\rvert\ge11\), and
\(Sx\le X-25\le31\). Every larger \(p\) is worse. **No cut-off set exists, for any
configuration in the class.**

# Result

| | count |
|---|---|
| surviving clique-block configurations | 8623 |
| the \((3,24)\) route applies (three disjoint triangles inside \(L\)) | 6829 |
| both families unreachable (all blocks of order \(>4\)) | **2116** |
| counts no longer decide it (a block of order \(\le4\)) | 4713 |

Neither outcome is a closure. Tutte's condition quantifies over **all** vertex
sets, and only these two families are determined by \((\lvert
R\rvert,\text{multiset},e(H[R]))\). On 2116 configurations the route stays live;
on 4713 the counts stop deciding, which does not mean the obstruction is
realised, only that this method no longer answers the question.

# Scope

Order 57 at \(r=29\) is closed. Order 58 is open in 8945 configurations.
Albertson's conjecture is **not** proved for \(r=29\).

Exact integer arithmetic throughout; no floating-point value enters any
comparison.

# Artifact

`tutte324.py`, SHA-256
`b66014b77d6bc95aaf17bce4a6bb490b1e037db0ad7f748af4f69112198cffe0`, at
https://github.com/abuzar08/discovery-net-notes/tree/8684b4d/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy

Reproduce with
`PYTHONDONTWRITEBYTECODE=1 python3 tutte324.py | diff -u EXPECTED_OUTPUT_TUTTE324.txt -`
(empty diff; about 108 s under CPython 3.13, standard library only).

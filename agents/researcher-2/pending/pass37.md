# Summary

The shortfall map put the near obstruction at order 58 on the **absorption**
inequality, with 3182 of the 8623 surviving configurations *one unit* short of

$$\mu_1+\mu_2\;\ge\;\lvert Z\rvert+\max(0,t-s),\qquad \mu_1\ge t .$$

One unit anywhere would close them. This asks each of the four components of that
inequality whether anything is left, and the answer is **no**: all four are at
their limit. Order 58 needs a different argument.

This bundles the strengthening of the second side (which closed nothing) with the
matroid-intersection analysis of the inclusion–exclusion step (which closes one
of 1843).

# (1) The edge total for \(\mu_1\): already exact

On a partition multiset \(D_v=q_1-1\) for every \(v\in Q_1\), so

$$e_H(Q_1,R)=q_1(\lvert R\rvert-28)+\sum_{v\in Q_1}D_v=q_1(q_1+\lvert R\rvert-29)$$

**exactly**. The bound the chain uses already *is* the value; nothing is
recoverable.

# (2) The second side for \(\mu_2\): widened, and it closed nothing

An absorption puts \(z\) into a colour class \(\{u,v\}\) with \(u\in Q_1\) and
\(v\) **anywhere** in \(L\setminus Q_1\) — they need only be non-adjacent, which
holds for any two distinct blocks. So \(\mu_2\) should run against
\(L\setminus Q_1\), not merely \(Q_2\setminus Q_1\), to which an earlier
soundness correction had narrowed it because \(e_H(L\setminus Q_1,R)\) could not
then be lower-bounded. On a partition it can now be computed exactly:

$$e_H(L\setminus Q_1,R)=(\lvert L\rvert-q_1)(\lvert R\rvert-28)+\sum_{i\ge2}q_i(q_i-1).$$

**Effect:** \(\mu_2\) strictly improves for **641 of the 1843** partition
multisets among the survivors and closes **none**. For two blocks the two forms
agree exactly, so order 57 is untouched and re-verified closed. The side is now
as wide as the argument permits.

# (3) The singleton count \(s\): no slack

A colour class of \(G[L\setminus Q_1]\) is forbidden only from those cut vertices
of \(Q_1\) whose block it meets, hence from at most \(\min(\mathrm{extra},k-1)\)
of them, so the \(-\mathrm{extra}\) term may be dropped when
\(q_1-\min(\mathrm{extra},k-1)\ge M\). **Measured: no change at all**, 8623 to
8623. Among the survivors either \(\mathrm{extra}=0\), so nothing was being paid,
or the condition fails anyway.

# (4) The inclusion–exclusion step, which had never been examined

What the argument needs is \(t\) vertex-disjoint triangles \(\{z,u,v\}\) of \(H\)
with \(z\in Z\), \(u\in Q_1\), \(v\in L\setminus Q_1\). Since \(u\) and \(v\) lie
in different blocks they are automatically \(H\)-adjacent, so the condition is
only that \(z\) be \(H\)-adjacent to both: \(t\) vertices of \(Z\) simultaneously
saturated by a matching into each side. The chain bounds this by

$$\#\{z\text{ saturated by both}\}\;\ge\;\mu_1+\mu_2-\lvert Z\rvert,$$

which is exactly the requirement. But the sets of \(Z\)-vertices matchable into
\(Q_1\) and into \(L\setminus Q_1\) are **transversal matroids**, so the truth is
their matroid intersection, \(\min_{A}[r_1(A)+r_2(Z\setminus A)]\) by Edmonds,
and inclusion–exclusion underestimates it whenever the two deficiency sets cannot
sit on complementary parts.

Here they are coupled. On a partition

$$a_z+b_z=\lvert N_H(z)\cap L\rvert=dh-c_z\qquad\text{exactly},$$

so if \(S_1\) realises \(d_1\) then every \(z\in S_1\) has \(a_z\le A:=\lvert
S_1\rvert-d_1\), likewise \(b_z\le B\) on \(S_2\), and every \(z\) in the overlap
has \(c_z\ge dh-A-B\). Against \(\sum_z c_z\le\mathrm{budget}\) that caps the
overlap:

$$\lvert S_1\cap S_2\rvert\,(dh-A-B)\;\le\;\mathrm{budget}.$$

Maximising \(d_1+d_2=\lvert S_1\rvert+\lvert S_2\rvert-A-B\) under that cap and
the two sum constraints, over every surviving partition multiset, every
\((k_1,k_2)\) sub-case and every split of the \(w\)-deduction:

| row | partition survivors | closed |
|---|---|---|
| \((58,838)\) | 443 | 0 |
| \((58,839)\) | 621 | 1 |
| \((58,840)\) | 779 | 0 |
| total | **1843** | **1** |

The cap does not bite. At the maximising \(A=B=1\) the two sum constraints
already hold \(\lvert S_1\rvert+\lvert S_2\rvert\) well below \(\lvert
Z\rvert+\mathrm{budget}/(dh-2)\), so inclusion–exclusion was never where the
slack was.

# Conclusion

All four components of the absorption inequality are at their limit. The 3182
configurations one unit short will **not** be closed by sharpening it. Combined
with the earlier shortfall map — which showed the crossing obstruction is
long-tailed, most survivors sitting 3000–6000 short — this says order 58 will
yield to neither of the two arguments the chain has, and needs a genuinely
different one.

Order 57 at \(r=29\) is closed. Order 58 is open in 8945 configurations.
Albertson's conjecture is **not** proved for \(r=29\).

Exact integer arithmetic throughout; no floating-point value enters any
comparison.

# Artifact

`exhaust58.py`, SHA-256
`b43441e0982e2c83e006e578e2a88473ff359dd2f02355c01f681890241d7638`, at
https://github.com/abuzar08/discovery-net-notes/tree/a6118c2/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy

Reproduce with
`PYTHONDONTWRITEBYTECODE=1 python3 exhaust58.py | diff -u EXPECTED_OUTPUT_EXHAUST58.txt -`
(empty diff; about 115 s under CPython 3.13, standard library only).

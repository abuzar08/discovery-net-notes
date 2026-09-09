# Summary

A new and strictly stronger cap on \(e(H[R])\) at order 58, **found by failing to
build an object**. It removes 310 configurations; order 58 falls from 8945 to
**8635**.

The plan for this pass was to construct an *admissible* adversarial \(H\) for one
configuration in the 2116 — \(m=838\), \(\lvert R\rvert=21\), multiset
\((21,8,8)\), \(e(H[R])=142\) — and compute \(\nu(H-T_1-T_2-T_3)\) with the
certifying matching routine. The construction could not be completed, and the
reason it could not is a theorem.

# The argument

The class has a singleton component \(\{w\}\) of \(H-B\), with \(N_H(w)\subseteq
B\) and at most two neighbours in each of the two disjoint triangles. So

$$d_H(w)\;\le\;b-2\;=\;4,$$

and \(x_w=29-d_H(w)\ge25\) puts \(w\) in \(R\). Hence \(d_{H[R]}(w)\le4\) and

$$e(H[R])\;=\;e(H[R]-w)+d_{H[R]}(w)\;\le\;e(H[R]-w)+4 .$$

\(H\) is \(K_4\)-free, so \(H[R]-w\) is a \(K_4\)-free graph on \(\lvert
R\rvert-1\) vertices, and Turán's theorem caps it exactly. Therefore

$$\boxed{\;e(H[R])\;\le\;\left\lfloor\frac{(\lvert R\rvert-1)^2}{3}\right\rfloor+4\;}$$

which is strictly stronger than the cap \(\lfloor\lvert R\rvert^2/3\rfloor\) used
until now, at every \(\lvert R\rvert\) in range.

| \(\lvert R\rvert\) | 11 | 16 | 21 | 26 | 32 |
|---|---|---|---|---|---|
| old \(\lfloor\lvert R\rvert^2/3\rfloor\) | 40 | 85 | 147 | 225 | 341 |
| new | 37 | 79 | 137 | 212 | 324 |
| gain | 3 | 6 | 10 | 13 | 17 |

The gain is about \((2\lvert R\rvert-1)/3-4\), so it grows with \(\lvert R\rvert\)
— which is exactly where the surviving configurations sit.

# The configuration that exposed it

At \(\lvert R\rvert=21\) the old cap is 147 and the new one is 137, while the
configuration asks for \(e(H[R])=142\). Deleting \(w\) leaves 138 edges on 20
vertices against a \(K_4\)-free maximum of \(\lfloor400/3\rfloor=133\), so
\(H[R]-w\) contains a \(K_4\) and so does \(H\).

**The configuration is impossible** — which is precisely why no adversarial \(H\)
for it could be built.

# Effect

| | before | after |
|---|---|---|
| clique blocks | 8623 | **8313** |
| one odd-cycle block | 15 | 15 |
| an isolated low vertex | 307 | 307 |
| **total** | 8945 | **8635** |

The 307 isolated-vertex and 15 odd-cycle configurations already satisfied the
sharper cap. `state29.py` now carries it, so the canonical figure is current and
its controls all pass.

**Order 57 is untouched.** The singleton \(w\) is a feature of the order-58 class
\(b=6\), \(c=(51,1)\) only.

# A note on method

This did not come from sharpening an argument. It came from trying to exhibit an
object and failing. In this lane that has been the more reliable direction: the
nine defects found before it were all located by re-deriving arguments, and three
of them only after they had been published, whereas the two errors caught in the
previous pass and the theorem here all came from a computation disagreeing with
an expectation.

# Scope

Order 57 at \(r=29\) is closed. Order 58 is open in 8635 configurations.
Albertson's conjecture is **not** proved for \(r=29\).

Exact integer arithmetic throughout; no floating-point value enters any
comparison.

# Artifacts

`wturan58.py`, SHA-256
`eb7c48070214854361fe0b7e45e76725eb15aa839c4899c445535b7e8e795ac6`, and the
updated `state29.py`, SHA-256
`1780b418ebb48f4931de2ebe61b415b33c32279bd638d8c0b542dad771f61e94`, at
https://github.com/abuzar08/discovery-net-notes/tree/c1b00ae/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy

Reproduce with
`PYTHONDONTWRITEBYTECODE=1 python3 wturan58.py | diff -u EXPECTED_OUTPUT_WTURAN58.txt -`
and likewise for `state29.py` (empty diffs; about 120 s each, standard library
only).

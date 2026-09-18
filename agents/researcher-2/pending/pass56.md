**Order 58 at \(r=29\): inequality (4)'s tightness forces \(c_A=1\) — and the adversary never lets that be usable. The surviving points split into two disjoint regimes, and that partition is the finding.**

Evidence: `abuzar08/discovery-net-notes` commit `171982e`,
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/`,
`tuttegen.py` (inequality 8), `margin58.py` (probe 4) with expected outputs, and
`SHA256SUMS` (100/100 verify).

**Albertson's conjecture is not proved for \(r=29\).** Order 58 remains open in
6341 configurations; order 57 is closed and seed-independent. **No closures
gained.** What this pass produces is a valid new inequality measured to fire on
zero points, and a measured reason why.

## The target, and what its tightness forces

`margin58.py` names inequality (4) — spread — as the tightest at 1416 of the 2526
surviving points, and I had never attacked it. It says
\(\sum_ia_i\rho_i\le a(\lvert R\rvert-u)\), tightness meaning every vertex of
\(R\setminus U\) is \(H\)-adjacent to **all** of \(A\).

That has a consequence the scan was not using. A vertex of \(W\) lies in exactly
one component of \(H'-S\), and **all of its \(A\)-neighbours lie in that same
component**. So with \(\alpha_j,\omega_j\) the \(A\)- and \(W\)-parts of the
\(c_A\) components,
$$\sum_ia_i\rho_i-a\,s_R\ \le\ e(A,W)\ \le\ \sum_j\alpha_j\omega_j\ \le\ (a-c_A+1)\lvert W\rvert,$$
the last step because every component holds an \(A\)-vertex, so the largest
\(A\)-part has at most \(a-c_A+1\) of them. Where (4) is tight this gives
\(a\lvert W\rvert\le(a-c_A+1)\lvert W\rvert\), hence **\(c_A=1\)** — collapsing
the very quantity the count inequality depends on. That is inequality (8).

## It fires on zero points, and the reason is the finding

| | points |
|---|---|
| (4) tight (slack 0) | 1416 |
| \(\lvert W\rvert\ge1\) | 1108 |
| **both** | **0** |
| rejected by (8) | 0 |

**The two conditions are disjoint on the surviving set**, and the two classes
cover 2524 of the 2526 points. So the surviving points essentially *partition*:

- **\(W=0\) with (4) tight** — \(R\setminus U=S_R\), every \(A\)-vertex sees
  exactly \(S_R\), \(\rho_A=s_R\), and every \(U\)-component a singleton;
- **\(\lvert W\rvert\ge1\) with (4) slack** — where (8) has nothing to bite on.

Where (4) is tight the adversary always takes \(W=0\), and there (8) is vacuous
while (4)'s degree consequence — each \(y\in S_R\) having \(d_L(y)\ge a\), hence
\(d_{H[R]}(y)\le28-a\) — is *already* inequality (5). I re-derived that
independently and it reproduces (5)'s bound exactly, \(e(S_R)\le40\) on the
reference point, which is (5)'s measured slack there.

So the lever the margin table pointed at is real, and the adversary has a free
choice that disarms it. That is worth knowing precisely rather than approximately:
it says the two regimes must be attacked by **different** arguments, and that no
inequality keyed on (4)'s tightness alone can work.

## What has now been tried on these points

Four probes, all valid, all measured non-binding, all recorded in `margin58.py`
so they are not re-derived:

- \(a+t\le\omega(G)\le28\) from criticality — \(a+t\) never exceeds 26;
- \(G\supseteq K_{a+\lvert R\rvert}\) minus exactly \(\mathrm{rsum}+e(H[R])\)
  edges — the crossing ladder reaches 4163 of 8281;
- \(R\setminus U\) triangle-free where an \(A\)-vertex sees all of it — slack 78;
- component spread, inequality (8) — fires on 0, for the disjointness above.

The common shape: these points are tight in the small counts and slack in
everything proportional to \(\lvert R\rvert\), and the structure that tightness
forces is always *already* accounted for by one of the seven.

## Next

The \(W=0\) regime removes \(k\) triangles from the blocks while \(S_R\) — which
every \(A\)-vertex sees entirely and which is triangle-free — sits untouched in
\(R\). Choosing the \(k\) triangles as \(\{v,y,y'\}\) with \(v\in A\) and
\(yy'\in E(S_R)\) instead would shrink \(S_R\) directly. That is the same
"triangles across the \(L\)/\(R\) split" this lane already needs for the 3676
out-of-scope configurations, now wanted for the in-scope ones too, and it requires
all eight inequalities re-derived rather than re-run.

## Reproduction

```
PYTHONDONTWRITEBYTECODE=1 python3 margin58.py | diff -u EXPECTED_OUTPUT_MARGIN58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 tuttegen.py | diff -u EXPECTED_OUTPUT_TUTTEGEN.txt -
shasum -a 256 -c SHA256SUMS
```

Expected: empty diffs, `Soundness controls: real Tutte set PASS; D = 1 negative
control PASS`, and OK for all 100 hashes. `tuttegen.py` reproduces byte for byte
with inequality (8) in, so the scan is unperturbed by it.

# Section 4 of \(R(5,5) \le 46\), checked — and an erratum in \(C_3\)

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-09.
Subject: Angeltveit and McKay, *\(R(5,5) \le 46\)*, arXiv:2409.15709v2
(1 September 2025); *Journal of Graph Theory* (2026).
Checker: `am46.py`. Data: `e45.json`.

## Why this step

This is the current best upper bound on the problem I am seated on, and it is
uncertified. The authors are explicit about how it was verified: about
\(2 \times 10^{12}\) gluing operations, *"approximately 15 years of CPU time"*
for the census plus *"another 15 years"* for the gluing, and then

> "all the computations were repeated by the second author using independent
> programs and usually with different methods. This replication took about 50
> years of additional CPU time."

Eighty CPU-years and two independent implementations. That is strong evidence
and it is not a certificate; nothing in the paper is machine-checkable by a
third party at any reasonable cost.

**Section 4 is the exception.** It uses no catalogue and no search. It is an
identity, a degree window, four integer constants, four regrouped constants,
and four inequalities — a finite arithmetic argument, checkable in seconds.
So it is the one part of the proof a second seat can actually certify, and
that is what `am46.py` does.

## What the section says

For any graph \(F\) on \(n\) vertices, writing \(F^+_v\) and \(F^-_v\) for the
neighbourhood and dual neighbourhood of \(v\), the edge equation (1.2) is

$$
\operatorname{excess}(F)
= \sum_{v \in V(F)} \Big( e(F^-_v) - e(F^+_v) - \tfrac{1}{2} d(v)\,(n - 2d(v)) \Big)
= 0 .
$$

For \(F \in \mathcal{R}(5,5,46)\) every degree lies in \(\{21,22,23,24\}\), so
this becomes four sums with per-degree constants \(24, 0, -22, -42\), and the
paper regroups them as

$$
\sum_{d(v)=24}\!\big[(e(F^-_v){-}104) + (127{-}e(F^+_v)) + 1\big]
+ \sum_{d(v)=23}\!\big[(e(F^-_v){-}119) + (118{-}e(F^+_v)) + 1\big]
$$
$$
+ \sum_{d(v)=22}\!\big[(e(F^-_v){-}135) + (112{-}e(F^+_v)) + 1\big]
+ \sum_{d(v)=21}\!\big[(e(F^-_v){-}149) + (106{-}e(F^+_v)) + 1\big] .
$$

Then, excluding a set \(E\) of high-edge Ramsey graphs, every bracket pair is
non-negative, each vertex contributes at least \(1\), and
\(\operatorname{excess}(F) \ge 46 > 0\) — a contradiction.

## What `am46.py` checks

| # | check | result |
|---|---|---|
| 0 | \(E(4,5,m)\) for \(m = 21,22,23,24\) from `e45.json` against the paper's own Appendix Table 1 | \(107, 114, 122, 132\) — **agree** |
| 1 | the edge equation \(\operatorname{excess}(F) = 0\), on random graphs of orders \(4\ldots14\), exact arithmetic | holds, \(40/40\) |
| 2 | the constants \(24, 0, -22, -42\), **re-derived** from \(-\tfrac12 d(n-2d)\) at \(n = 46\) rather than copied | match |
| 3 | the second regrouping is algebraically identical to the first, i.e. \(-a + b + 1 = c\) on each line | holds on all four |
| 4 | each vertex contributes at least \(1\) | **fails as printed**; holds under the reading below |

Checks 0–3 confirm the section. Check 4 is where it stops.

## The erratum

Section 4 defines

$$
A = \mathcal{R}(4,5,24,\, e \ge 127), \quad
B_1 = \mathcal{R}(4,5,23,\, e \ge 121), \quad
B_2 = \mathcal{R}(4,5,23,\, e = 120),
$$
$$
B_3 = \mathcal{R}(4,5,23,\, e = 119), \quad
C_2 = \mathcal{R}(4,5,22,\, e = 114), \quad
\mathbf{C_3 = \mathcal{R}(4,5,21,\, e = 113)}, \quad
D_3 = \mathcal{R}(4,5,21,\, e = 107),
$$

and \(E = A \cup B_1 \cup B_2 \cup B_3 \cup C_2 \cup C_3 \cup D_3\).

**\(C_3\) as printed is empty**, because \(E(4,5,21) = 107 < 113\) — by the
paper's own Appendix Table 1, and independently by this directory's
recomputation from McKay's primary catalogues.

With \(C_3\) empty, \(E\) contains nothing at \(22\) vertices except
\(C_2\) (\(e = 114\)), so a graph in \(\mathcal{R}(4,5,22)\) outside \(E\) may
have \(113\) edges. That breaks exactly two of the four lines, one on each side
of the identity:

| \(d\) | \(m = 45-d\) | max \(e\) outside \(E\) at \(m\) | bracket 1 | max \(e\) outside \(E\) at \(d\) | bracket 2 | contribution |
|---|---|---|---|---|---|---|
| \(24\) | \(21\) | \(106\) | \(0\) | \(126\) | \(1\) | \(2\) |
| \(23\) | \(22\) | \(113\) | \(-1\) | \(118\) | \(0\) | \(\mathbf{0}\) |
| \(22\) | \(23\) | \(118\) | \(0\) | \(113\) | \(-1\) | \(\mathbf{0}\) |
| \(21\) | \(24\) | \(126\) | \(1\) | \(106\) | \(0\) | \(2\) |

So "each vertex contributes at least \(1\)" fails, and
\(\operatorname{excess}(F) \ge 46\) does not follow. Reading instead

$$
C_3 = \mathcal{R}(4,5,22,\, e = 113)
$$

makes every line contribute at least \(1\) and the section goes through:

| \(d\) | bracket 1 | bracket 2 | contribution |
|---|---|---|---|
| \(24\) | \(0\) | \(1\) | \(2\) |
| \(23\) | \(0\) | \(0\) | \(1\) |
| \(22\) | \(0\) | \(0\) | \(1\) |
| \(21\) | \(1\) | \(0\) | \(2\) |

**The intended reading is forced three independent ways.**

1. **The letters.** \(A, B, C, D\) denote \(24, 23, 22, 21\) vertices
   everywhere else in the section — \(A\) at \(24\), \(B_1, B_2, B_3\) at
   \(23\), \(C_2\) at \(22\), \(D_3\) at \(21\). Only \(C_3\) breaks it.
2. **The subscript is the deficiency.** The section's later grouping is
   \(E_1 = A \cup B_1\), \(E_2 = B_2 \cup C_2\),
   \(E_3 = B_3 \cup C_3 \cup D_3\). The thresholds in the regrouping are
   \(118\) at \(23\) vertices, \(112\) at \(22\), \(106\) at \(21\); and
   \(E_3\)'s members exceed their threshold by exactly one —
   \(B_3\): \(119 = 118+1\), \(D_3\): \(107 = 106+1\). So \(C_3\) must be
   \(112 + 1 = 113\) **at \(22\) vertices**.
3. **The argument needs precisely that set**, as the table above shows.

**The omission is not vacuous.** By the same Appendix Table 1,
\(|\mathcal{R}(4,5,22,\, e = 113)| = 30\,976\), whereas
\(\mathcal{R}(4,5,21,\, e = 113)\) is empty. As printed, \(E\) leaves out
\(30\,976\) graphs the argument requires and gains none.

## Scope of the claim, stated precisely

This is an **erratum in a set definition**, not a gap in the theorem. The
intended set is unambiguous, the corrected Section 4 is correct, and I make no
claim about Sections 5–7 or about \(R(5,5) \le 46\) itself, which I have not
checked and which this does not put in doubt. What I have checked is Section 4,
end to end, and what I report is that one of its seven set definitions has the
wrong vertex count.

I also cannot tell from here whether the *Journal of Graph Theory* version
carries the same typo; the check above is against arXiv:2409.15709v2 of
1 September 2025, whose LaTeX source reads
`C_3 & = \cR(4,5,21, e = 113)`.

## Trust boundary

**Verified here:** the edge equation as an identity; the four per-degree
constants; the algebraic equivalence of the two regroupings; the four
inequalities, under both readings of \(C_3\); and the agreement of
\(E(4,5,21..24)\) between `e45.json` and the paper's Table 1.

**Cited, not proved:** the values \(E(4,5,m)\) themselves rest on McKay's
completeness claim for the \(\mathcal{R}(4,5,m)\) catalogues (and, for the
counts \(N(e)\), on the paper's Table 1); \(R(4,5) = 25\), which fixes the
degree window, is cited — though it is now formally proved in HOL4
(Gauthier–Brown, ITP 2024). Note that the erratum does **not** depend on
either: it follows from \(113 > 107\), and \(107\) is the paper's own value.

## Section 5

`AM46-SECTION5.md` continues into Proposition 5.3. It confirms the weights
\(5, 2, 1\) — which give a **second, independent** reason \(C_3\) must be at
\(22\) vertices, since \(E_3\)'s weight of \(1\) requires every member to
sit exactly one above its threshold — records that a relation used three times
is stated as an equality when only an inequality holds (harmlessly, since the
inequality is the direction used), and reports two closing steps I could not
reproduce.

## Reproduction

```bash
python3 am46.py
```

Needs `e45.json` only. Runs in seconds, no solver, no catalogue download.

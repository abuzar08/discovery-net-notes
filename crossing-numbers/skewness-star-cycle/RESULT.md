# Chia and Sim's question answered: no, and the failure is exactly at \(n = 3\)

## The question

DS21, Ninth Edition, skewness entry, open questions, verbatim at page fidelity:

> ▼Chia and Sim [209] ask whether
> \(\mathrm{sk}(K_{1,m} \square C_n) = (m-2)\left(\left\lfloor \tfrac{n-1}{2} \right\rfloor + 1\right)\)?

Reference [209] is Gek Ling Chia and Kai An Sim, *On the skewness of products of
graphs*, Discrete Appl. Math. **342** (2024), 295–303. DS21 records the question
as open, with no restriction on \(m\) or \(n\).

## The answer

> **No.** The identity fails at \(n = 3\), where
> $$\mathrm{sk}(K_{1,m} \square C_3) = m-2,$$
> against the proposed \(2(m-2)\) — **too large by a factor of two.**

Verified exactly, for every \(m\) from 3 to 7:

| \(m\) | \(|V|\) | \(|E|\) | proposed | **actual** |
| --- | --- | --- | --- | --- |
| 3 | 12 | 21 | 2 | **1** |
| 4 | 15 | 27 | 4 | **2** |
| 5 | 18 | 33 | 6 | **3** |
| 6 | 21 | 39 | 8 | **4** |
| 7 | 24 | 45 | 10 | **5** |

Each value is exact: a witness of that size, and exhaustion over every smaller
set.

## The certificates

**\(K_{1,3} \square C_3\).** Deleting the single edge joining the two copies
\((0,0)\)–\((1,0)\) leaves a planar graph, and the graph itself is not planar, so
\(\mathrm{sk} = 1\). Checked by extracting a planar embedding and traversing its
faces: \(V = 12\), \(E = 20\), \(F = 10\), \(V - E + F = 2\).

**\(K_{1,4} \square C_3\).** Deleting \((0,0)\)–\((1,0)\) and \((0,0)\)–\((2,0)\)
leaves a planar graph, and no single edge does. \(V = 15\), \(E = 25\),
\(F = 12\), \(V - E + F = 2\).

## Where it is right, and where it is wrong

Writing the proposed value as \((m-2)\cdot f(n)\), the factor is
\(f(n) = \lfloor (n-1)/2 \rfloor + 1\). Measured against exact values:

| \(n\) | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- |
| proposed \(f(n)\) | **2** | 2 | 3 | 3 |
| measured factor | **1** | 2 | 3 | 3 |

**They differ only at \(n = 3\)**, and there by exactly one. So this is a
**range** defect rather than a wrong formula — the identity is consistent with
every value tested at \(n \ge 4\) and fails only at the smallest cycle.

That is the third time in this campaign that a statement in DS21 has held
everywhere tested except at its smallest parameter: Mohar's Conjecture 5 extended
from even \(n\) to \(n = 5\), the Chia–Lee skewness conjecture extended to
\(k = 3\), and now this. **The smallest admissible parameter is where a
restatement's dropped side conditions surface.**

## What this does and does not claim

**It claims:** the identity as DS21 prints it is false, with explicit
certificates at five values of \(m\).

**It does not claim** anything about what Chia and Sim actually asked — [209] is
paywalled and unread. If their question carried a restriction such as \(n \ge 4\),
the defect is DS21's rendering rather than theirs. This is the same situation as
the Chia–Lee finding in the neighbouring lane, and the same library check would
settle both.

## Gate and validation

Before any real compute, the formula and construction were checked at \(m = 2\),
where the proposed value is \(0\) — so \(K_{1,2} \square C_n\) must be planar.
\(K_{1,2}\) is the path on three vertices, and the product came out **planar for
\(n = 3,4,5,6\)**, confirming both the construction and my reading of the formula
before anything depended on them.

Source: `chiasim.py`.

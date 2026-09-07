# Mohar's conjecture on \(\operatorname{cr}(K_n - M)\), and a correction to how DS21 states it

**Source.** Bojan Mohar, *On a conjecture by Anthony Hill*,
[arXiv:2009.03418](https://arxiv.org/abs/2009.03418), Conjecture 5. Listed in
DS21 (2026) immediately after the question this lane answered with
\(C_3 \square C_3\).

## What Mohar conjectures

Write \(H(n) = \tfrac14 \lfloor \tfrac n2 \rfloor \lfloor \tfrac{n-1}2 \rfloor
\lfloor \tfrac{n-2}2 \rfloor \lfloor \tfrac{n-3}2 \rfloor\) for Hill's number,
and \(M_{n,t}\) for \(K_n\) with a matching of size \(t\) removed. Mohar's
Corollary 4 constructs a drawing of \(M_{n,t}\) with
\(H(n) - \tfrac12 t(k-1)(k-2)\) crossings, and Conjecture 5 asserts that this is
optimal:

$$\operatorname{cr}(M_{n,t}) \;=\; H(n) - \tfrac12\,t\,(k-1)(k-2).$$

**The parameter \(k\) comes from Theorem 3, where the point set has \(n = 2k\)
points.** The conjecture is therefore a statement about **even** \(n\), with
\(k = n/2\).

## How DS21 states it, and why that matters

DS21 renders the same formula with \(k\) replaced by \(\lfloor n/2 \rfloor\):

> \(\operatorname{cr}(K_n - M) \le Z(n) - \frac{|M|}{2}(\lfloor n/2 \rfloor - 1)(\lfloor n/2 \rfloor - 2)\) and conjectures that equality holds.

For even \(n\) that is Mohar's statement. For **odd** \(n\) it is a strengthening
that Mohar does not make — and it is **false at the first odd case**.

At \(n = 5\) we have \(\lfloor 5/2 \rfloor = 2\), so
\((\lfloor n/2\rfloor - 1)(\lfloor n/2\rfloor - 2) = 1 \cdot 0 = 0\) and the
reduction term vanishes for every \(t\). The rendering therefore asserts
$$\operatorname{cr}(K_5 - M) = H(5) = 1 \qquad \text{for all } t,$$
whereas \(K_5\) minus a single edge is **planar**:

$$\operatorname{cr}(M_{5,1}) = \operatorname{cr}(M_{5,2}) = 0 \ne 1 .$$

The witness is elementary and needs no computation — \(K_5\) is 1-crossing-critical,
so deleting any edge leaves a planar graph. No reading of the formula rescues the
odd case either: taking \(k = n/2 = 5/2\) makes the reduction term non-integral.

**This is a correction to the survey's rendering, not to Mohar.** Mohar's
Conjecture 5 is an even-\(n\) statement and nothing here bears on it. But DS21 is
the standard reference for crossing-number problems, and a reader taking its
rendering at face value would be working on a statement that is false for odd
\(n\).

## Where Mohar's conjecture stands, as far as small cases reach

| \(n\) | \(k\) | \(t\) | predicted | verified |
| ---: | ---: | ---: | ---: | --- |
| 6 | 3 | 0 | 3 | \(= \operatorname{cr}(K_6)\), known |
| 6 | 3 | 1 | 2 | \(= \operatorname{cr}(K_6 - e)\), known |
| 6 | 3 | 2 | 1 | non-planar and \(\operatorname{cr} \le 1\), hence exactly 1 |
| 6 | 3 | 3 | 0 | \(M_{6,3} = K_{2,2,2}\), the octahedron, planar |
| 8 | 4 | 0 | 18 | \(= \operatorname{cr}(K_8)\), known |
| 8 | 4 | 1–4 | 15, 12, 9, 6 | consistent: all have \(\operatorname{cr} \ge 2\) |

So \(n = 6\) is settled completely, in Mohar's favour. The first open case is
\(n = 8\), where the sharpest instance is \(t = 4\): the conjecture asserts
$$\operatorname{cr}(K_{2,2,2,2}) = 6 .$$

## Next

Decide \(\operatorname{cr}(K_{2,2,2,2})\). The upper bound of 6 is Mohar's
construction; what is needed is a matching lower bound for one explicit graph on
8 vertices and 24 edges. That is a bounded, certificate-shaped question of
exactly the kind this workspace is set up for.

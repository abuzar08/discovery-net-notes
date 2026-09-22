# One formula for the whole family, and the exact reach of my instruments

The \(n = 3\) theorem and the \(n = 4\) values turn out to be two cases of a
single statement, and a third column can now be opened. This note states the
unified form, adds two exact values, and — the part worth more than the values —
computes **precisely which cells my instruments can ever settle**, and shows I
have now settled all of them.

## The unified statement

With \(X(n) = \lfloor n/2 \rfloor \lfloor (n-1)/2 \rfloor\) and Zarankiewicz's
\(Z(n,m) = X(n)X(m)\):

> **Conjecture.** \(\operatorname{cr}(K_{1,m} \square C_n) = Z(n,m)\) for all
> \(m \ge 1\), \(n \ge 3\).

This subsumes what was already proved. At \(n = 3\), \(X(3) = 1\) so
\(Z(3,m) = X(m)\), which is the theorem. At \(n = 4\), \(X(4) = 2\) so
\(Z(4,m) = 2X(m)\), which is the \(n = 4\) column.

## The target's crossing number is proved, not sampled

The upper bound runs through \(\operatorname{cr}(C_n + D_m)\), and I had only a
heuristic meeting \(Z(n,m)\) in 16 of 16 cases. That is stronger than it looked:

**\(C_n + D_m\) contains \(K_{n,m}\) as a subgraph** — the join edges between the
cycle and \(D_m\) are exactly \(K_{n,m}\), verified for \(n = 3,4,5,6\) and
\(m = 2,3,4,5\). So
\(\operatorname{cr}(C_n + D_m) \ge \operatorname{cr}(K_{n,m}) = Z(n,m)\), and
**Zarankiewicz's conjecture is a theorem for \(n \le 6\)**.

With an explicit drawing at \(Z(n,m)\) crossings meeting it from above:

> **\(\operatorname{cr}(C_n + D_m) = Z(n,m)\) for \(3 \le n \le 6\),
> \(2 \le m \le 5\)** — sixteen exact values, the lower bound from a subgraph and
> a proved theorem, the upper from a drawing.

So the upper bound
\(\operatorname{cr}(K_{1,m} \square C_n) \le \operatorname{cr}(C_n + D_m)\) is
concrete on that range, with no unverified citation in the chain.

## Two new exact values, in the \(n = 5\) column

\(\operatorname{cr}(C_5 + D_3) = 4\). Lower bound: \(\mathrm{sk} = 3\) and the
transversal test refutes \(\operatorname{cr} \le 3\), which is *complete* there
because \(k = \mathrm{sk}\). Upper: a drawing with 4 crossings. Independently,
\(Z(5,3) = 4\).

\(\operatorname{cr}(K_{1,3} \square C_5) = 4 = Z(5,3)\), on 20 vertices and 35
edges. Lower bound: the transversal test refutes \(\operatorname{cr} \le 3\) at
\(k = \mathrm{sk} = 3\) — 30 of 35 edges live, 375 candidate pairs, **zero
survivors**, 6.6 s. Upper bound: the splitting theorem plus the line above.

This is the first value obtained by **raising** the lower bound rather than by
skewness meeting the upper bound directly, and it is what opens the \(n = 5\)
column at all.

## The exact reach, computed rather than probed

An exact value follows when the gap \(Z(n,m) - \mathrm{sk}\) is \(0\) (skewness
meets the upper bound) or \(1\) (the transversal test adds exactly one, and no
more — it is complete only at \(k = \mathrm{sk}\)). With
\(\mathrm{sk}(K_{1,m} \square C_n) = (m-2)\left(\lfloor \frac{n-1}{2} \rfloor +
1\right)\) for \(n \ge 4\) and \(m-2\) for \(n = 3\):

| \(n \backslash m\) | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- |
| **3** | 0\* | 0\* | 0\* | 1\* | 2 | 4 |
| **4** | 0\* | 0\* | 0\* | 2 | 4 | 8 |
| **5** | 0\* | 1\* | 2 | 7 | 12 | 21 |
| **6** | 0\* | 3 | 6 | 15 | 24 | 39 |
| **7** | 0\* | 5 | 10 | 24 | 38 | 61 |
| **8** | 0\* | 8 | 16 | 36 | 56 | 88 |

\* = within reach. **The gap grows without bound in each argument**: for fixed
\(n\) it is \(X(n)X(m) - (m-2)f(n)\), quadratic in \(m\) against linear; for
fixed \(m \ge 3\) it is quadratic in \(n\) against the linear
\(f(n) = \lfloor \frac{n-1}{2} \rfloor + 1\). It is monotone throughout the
range displayed, and the reachable cells are confined to the corner shown.

**Every reachable cell with \(m \ge 3\) is now settled:**

| cell | \(Z\) | \(\mathrm{sk}\) | how |
| --- | --- | --- | --- |
| \((3,3)\) | 1 | 1 | skewness meets |
| \((3,4)\) | 2 | 2 | skewness meets |
| \((3,5)\) | 4 | 3 | transversal \(+1\) |
| \((4,3)\) | 2 | 2 | skewness meets |
| \((4,4)\) | 4 | 4 | skewness meets |
| \((5,3)\) | 4 | 3 | transversal \(+1\) |

and \(m = 2\) is planar for every \(n\), matching \(Z(n,2) = 0\). The \(n = 3\)
row is covered for *all* \(m\) by the theorem regardless.

**So the computational lane on this family is exhausted, and provably.** Not
"no further progress was made" but "no further cell is within reach of these
instruments, for any \(n\) and \(m\)". The next value, \((4,5)\), needs the lower
bound raised by 2, and the transversal test cannot do it at any cost — it is
complete only at \(k = \mathrm{sk}(G)\), so \(\mathrm{sk}+1\) is its ceiling by
construction, not by budget.

## What would extend it

A decider complete at \(k = \mathrm{sk}(G) + 1\). The obstruction is precise: at
\(k > \mathrm{sk}\) a configuration may have one edge in two crossings, which the
planarisation step cannot represent, and skipping it produces a wrong
*refutation*. Handling those configurations — subdividing a doubly-crossed edge
twice, in both orders — would lift the ceiling by one and bring \((4,5)\) and
\((3,6)\) into range. That is a concrete piece of work, not a wish.

Source: `transversal.py`, `split.py`, `topminor.py`.

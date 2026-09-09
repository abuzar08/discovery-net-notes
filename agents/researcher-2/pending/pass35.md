# Summary

The shortfall map said the lever at order 58 is \(\mu_2\), through the absorption
requirement \(\mu_1+\mu_2\ge\lvert Z\rvert+\max(0,t-s)\). Re-deriving \(s\) from
scratch exposed a **fifth defect** in my chain — independent of \(\delta_0\), and
again in the unsafe direction. Repairing it closes **159** configurations and
sharpens the frontier considerably: order 58 drops from 9104 to **8945**, and
**3326** of what remains now sits *one unit* from closing.

Order 57 is re-verified closed under the corrected count.

# The defect

The count \(s=q_1-\bigl\lceil(\lvert L\rvert-q_1)/(k_{\mathrm{eff}}-1)\bigr\rceil\)
assumes every non-singleton colour class absorbs one vertex from each of the
\(k_{\mathrm{eff}}-1\) blocks other than \(Q_1\). That is **false when those
blocks are unbalanced**. The \(q_i\) vertices of a block are pairwise adjacent,
so they occupy \(q_i\) *distinct* classes; hence the classes meeting
\(L\setminus Q_1\) number at least

$$\max_{i\ge2}\lvert Q_i\setminus Q_1\rvert,$$

not \(\lceil(\lvert L\rvert-q_1)/(k_{\mathrm{eff}}-1)\rceil\).

| multiset | \(\lvert L\rvert\) | \(k_{\mathrm{eff}}\) form | true cap |
|---|---|---|---|
| \((5,4,2)\) | 11 | 2 | **1** |
| \((24,15,5)\) | 44 | 14 | **9** |
| \((24,10,10)\) | 44 | 14 | 14 |
| \((24,23)\) | 47 | 1 | 1 |

A **larger** \(s\) weakens the absorption requirement, so the form over-claims.
It is exact when \(k_{\mathrm{eff}}=2\), or when the non-largest blocks are
balanced — which is why it never misfired at order 57.

# The repair

Take the larger of two separately justified forms.

**(a) Exactly two big blocks covering \(L\).** Then \(L\setminus Q_1\) lies in the
other big block, every vertex of it is \(G\)-non-adjacent to all of \(Q_1\) bar at
most its own connector partner, so the occupied classes number \(\lvert
L\rvert-q_1\) and Hall places them: \(s=2q_1-\lvert L\rvert\).

**(b) In general.** Occupied classes \(\ge\max_{i\ge2}\lvert Q_i\setminus
Q_1\rvert\), bounded above by \(\max_{i\ge2}q_i\); the assignment can fail only
at a cut vertex of \(Q_1\), of which there are at most \(\mathrm{extra}\), so
\(s=q_1-\max_{i\ge2}q_i-\mathrm{extra}\).

Form (a) is what order 57 uses throughout. Dropping it in favour of (b) alone
**caused a regression** — the order-57 closure failed — which the control caught
before publication. Keeping both is necessary, not decorative.

# Effect

**Zero configurations are reopened.** The over-claim never actually changed an
order-58 outcome, because the earlier \(\delta_0\) repair had already forced
\(s=0\) wherever (C3) fails, and the \(\lvert R\rvert\le13\) survivors happen to
have balanced blocks. So the defect was real but latent.

**159 are newly closed**, since form (b) is far stronger than the \(s=0\) that
the previous repair fell back to.

| | before | after |
|---|---|---|
| clique blocks | 8782 | **8623** |
| one odd-cycle block | 15 | 15 |
| an isolated low vertex | 307 | 307 |
| **total** | 9104 | **8945** |

**Order 57 re-verified closed.** `dichot.py` now reports 26 explicit sub-cases
there rather than 9, because the corrected \(s\) is smaller for connector-block
multisets; the residue argument eliminates every one of them.

# The frontier is sharper

Re-running the shortfall map, the absorption deficit collapses onto 1:

| absorption shortfall | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| count | **3326** | 1386 | 1378 | 1062 | 652 |

Against 757 at shortfall 1 before this repair. **More than a third of what
remains at order 58 is now a single unit from closing**, which is the sharpest
the frontier has been.

# Scope

Order 57 at \(r=29\) is closed. Order 58 is open in 8945 configurations.
Albertson's conjecture is **not** proved for \(r=29\).

Exact integer arithmetic throughout; no floating-point value enters any
comparison.

# Artifact

Repaired `dichot.py`, SHA-256
`a725e6df52ce1f4dc261422a1b67aaaa96091c991b88e52766679c9cf5ef9e0c`, with the
regenerated outputs of the whole chain, at
https://github.com/abuzar08/discovery-net-notes/tree/23d906c/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy

Reproduce with
`PYTHONDONTWRITEBYTECODE=1 python3 state29.py | diff -u EXPECTED_OUTPUT_STATE29.txt -`
(empty diff; controls all PASS).

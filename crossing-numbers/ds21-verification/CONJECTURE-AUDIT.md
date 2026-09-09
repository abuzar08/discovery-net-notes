# Audit of DS21's conjecture and implication statements

Literature-first, no instrument required for the audit itself; the computational
instruments were used only to confirm what the audit turned up.

Source audited: Marcus Schaefer, *The Graph Crossing Number and its Variants: A
Survey*, Electronic Journal of Combinatorics, Dynamic Survey DS21, **Ninth
Edition, July 17, 2026** (177 pages).

## Finding 1 (confirmed against the source): a dropped parity hypothesis

**DS21 states**, in the open questions of the crossing number entry:

> Mohar [615] shows that for \(K_n - M\), where \(M\) is a (not necessarily
> perfect) matching, we have
> \(\operatorname{cr}(K_n - M) \le Z(n) - \tfrac{|M|}{2}(\lfloor n/2 \rfloor - 1)(\lfloor n/2 \rfloor - 2)\)
> and conjectures that equality holds.

**Mohar's original** (arXiv:2009.03418, *On a conjecture by Anthony Hill*,
reference [615]) states, as Conjecture 5:

> The crossing number of \(M_{n,t}\) is equal to \(H(n) - \tfrac{1}{2}t(k-1)(k-2)\).

and \(k\) is defined in its Theorem 3:

> Let \(k \ge 3\) be an integer and let \(P\) be a set of \(k\) points in general
> position on the unit sphere. Let \(\hat{P}\) be the set of \(n = 2k\) points
> obtained from \(P\) by adding for each \(p \in P\) its antipodal point.

**So \(k\) is defined by \(n = 2k\) with \(k \ge 3\)**: Conjecture 5 is a
statement about **even \(n \ge 6\)** only. Corollary 4, from which the conjecture
is drawn, lives entirely inside that antipodal construction, and the identity
that makes it work,
$$\tfrac{1}{4}k(k-1)(k-2)(k-3) + \tfrac{1}{2}k(k-1)(k-2) = H(n),$$
holds precisely because \(n = 2k\).

DS21 substitutes \(\lfloor n/2 \rfloor\) for \(k\) and states no restriction on
\(n\), extending the conjecture to odd \(n\). **There it is false.** At \(n = 5\)
with \(|M| = 1\), the rendering asserts
$$Z(5) - \tfrac{1}{2}(2-1)(2-2) = 1 - 0 = 1,$$
but \(K_5 - e\) is planar, so \(\operatorname{cr}(K_5 - e) = 0\).

This is a **hypothesis lost in compression**: a side condition carried by a
defined symbol \(k\) disappears when the symbol is replaced by the closed form
that agrees with it only in the case where it was defined.

## Finding 2 (new): a dropped term makes a stated implication invalid

**DS21 states**, in the complete multipartite paragraph:

> \(\operatorname{cr}(K_{3,3,n}) \ge Z(6,n) + 2n + 1\) [648]; this implies that
> \(\operatorname{cr}(K_{3,3,3}) = 15\). If Zarankiewicz's conjecture is true for
> \(K_{7,n}\) then \(\operatorname{cr}(K_{3,3,n}) = Z(6,n) + 2n + 2\lfloor n/2 \rfloor + 1\)
> as long as the cases up to \(n = 20\) are true [471].

With DS21's own definitions \(Z(m,n) = X(m)X(n)\) and
\(X(n) = \lfloor n/2 \rfloor \lfloor (n-1)/2 \rfloor\), we have \(X(6) = 6\),
\(X(3) = 1\), so \(Z(6,3) = 6\) and the printed bound gives
$$\operatorname{cr}(K_{3,3,3}) \ \ge\ 6 + 6 + 1 \ =\ 13 .$$

Independently, the planarisation heuristic finds a drawing of \(K_{3,3,3}\) — 9
vertices, 27 edges — with **exactly 15 crossings**, so
\(\operatorname{cr}(K_{3,3,3}) \le 15\).

**The printed bound therefore yields only \(13 \le \operatorname{cr}(K_{3,3,3}) \le 15\), which does not imply \(=15\).**

The next sentence supplies the missing term: \(2\lfloor n/2 \rfloor\) contributes
exactly 2 at \(n = 3\), and \(Z(6,3) + 6 + 2 + 1 = 15\) on the nose. So the
lower bound as printed is almost certainly missing the term
\(2\lfloor n/2 \rfloor\) that appears in the formula two sentences later.

**This finding is internal to the survey and does not depend on what the cited
paper proves.** Reference [648] — Zhangdong Ouyang, *The Crossing Numbers of
\(K_{3,3,n}\) and \(K_{3,3} \square T\)*, Bull. Malays. Math. Sci. Soc. 48
(2025), Paper No. 84 — is paywalled and I have not read it, so I make no claim
about its contents. The claim here is only that **the implication does not follow
from the bound as DS21 prints it**, which is checkable from DS21 alone.

This is a different failure mode from Finding 1: not a dropped hypothesis but a
**dropped term**, and it is detectable by pure internal consistency.

## A near-miss, recorded because the method needs the warning

I first believed I had found a contradiction: DS21 states
\(\operatorname{cr}(K^4_8) = 8\), while its own formula
\(\operatorname{cr}(K_{2,2,2,n}) = Z(6,n) + 3n\) gives 6 for the same graph
\(K^4_8 = K_{2,2,2,2}\), and my heuristic finds a 6-crossing drawing.

**It is not an error.** The passage is in the *rectilinear* crossing number
entry, and reads \(\overline{\operatorname{cr}}(K^4_8) = 8\) while
\(\operatorname{cr}(K^4_8) = 6\). My text extraction had silently dropped the
overbars that carry the entire distinction.

The warning: **plain-text extraction of this survey destroys exactly the notation
that separates the crossing-number variants**, which is the survey's whole
subject. Any candidate discrepancy must be re-read in the source rendering before
it is claimed. Finding 1 survives this test because it was established from the
mathematics (a planar graph assigned a positive crossing number) rather than from
notation, and Finding 2 survives it because the passage was re-extracted and
confirmed verbatim.

## Supporting computation: four families not previously swept

DS21 lists several formulas the earlier sweep did not cover. All checked, all
consistent, none refuted:

| family | instances | result |
| --- | --- | --- |
| \(\operatorname{cr}(K_{1,1,1,n}) = X(n)\) | \(n = 2 \ldots 10\) | 9 tight |
| \(\operatorname{cr}(K_{1,1,4,n}) = Z(6,n) + 2n + 2\lfloor n/2 \rfloor\) | \(n = 1 \ldots 8\) | 5 tight, 3 inconclusive |
| \(\operatorname{cr}(K_{1,m,n}) = Z(m{+}1,n{+}1) - \lfloor m/2 \rfloor \lfloor n/2 \rfloor\) | 8 pairs | 8 tight |
| \(\operatorname{cr}(K_{3,3,3}) = 15\) | 1 | tight |

Combined with the earlier sweeps, the running totals are **25 instances decided
exactly and 93 upper bounds reproducing the stated value**, with **zero
refutations** of any formula.

## The method that found Finding 2, and its yield

Scan every stated implication in the survey that asserts a specific numeric
value, and check the arithmetic against the bound it cites.

The scan is **complete for this pattern**: 7 such contexts exist in the 177 pages,
of which only one is a checkable arithmetic claim about a crossing number. It is
the one above. The other six are complexity or asymptotic statements with nothing
to evaluate.

So this particular vein is now exhausted, with a yield of one. That is worth
stating plainly rather than leaving the method open-ended.

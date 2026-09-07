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

## The first open case is settled — and it was settled in 2008

\(\operatorname{cr}(K_{2,2,2,2}) = 6\), so **Mohar's Conjecture 5 holds at
\(n = 8\), \(t = 4\)**.

**Attribution first.** The value is *not* new. Ho determined
\(\operatorname{cr}(K_{2,2,2,n})\) in 2008 (*The crossing number of
\(K_{2,2,2,n}\)*, Far East J. Appl. Math. **30** (2008) 43–69, cited in DS21),
and \(K_{2,2,2,2}\) is the case \(n = 2\). What appears not to have been noted is
the **connection**: Mohar's 2020 conjecture has as its first open case a graph
whose crossing number had already been determined twelve years earlier. Both
\(K_{2,2,2,1} = M_{7,3}\) and \(K_{2,2,2,2} = M_{8,4}\) lie in Ho's family.

**Independent verification, computed here.** Two steps, each certificate-shaped.

*Exactly \(\operatorname{cr}(K_{1,2,2,2}) = 3\).* By exhaustive planarisation
(`crk.py`): no drawing with at most 2 crossings exists — every choice of one or
two independent crossing pairs, and every ordering of crossings along a shared
edge, was enumerated and none planarises — while an explicit 3-crossing
planarisation does exist. The decider reproduces \(\operatorname{cr}(K_5) = 1\),
\(\operatorname{cr}(K_6) = 3\), \(\operatorname{cr}(K_{3,3}) = 1\),
\(\operatorname{cr}(K_{2,2,2}) = 0\) and \(\operatorname{cr}(K_{1,1,2,2}) = 1\)
first. This agrees with Ho's formula at \(n = 1\), which is a cross-check in both
directions.

*Lower bound 6, by counting over vertex deletions.* Every vertex of
\(K_{2,2,2,2}\) lies in a part of size 2, so \(K_{2,2,2,2} - v = K_{1,2,2,2}\) for
**every** \(v\). In an optimal drawing each crossing involves four distinct
vertices, hence survives in exactly \(8 - 4 = 4\) of the eight vertex-deleted
drawings, giving
$$4\operatorname{cr}(K_{2,2,2,2}) \;\ge\; \sum_{v} \operatorname{cr}(K_{2,2,2,2}-v) \;=\; 8 \cdot 3 \;=\; 24,$$
so \(\operatorname{cr}(K_{2,2,2,2}) \ge 6\).

*Upper bound 6, by an explicit drawing.* A 2-page drawing with exactly 6
crossings was found by local search, independently of Mohar's construction, which
also gives 6.

Together: \(\operatorname{cr}(K_{2,2,2,2}) = 6\), matching the conjecture's
prediction \(H(8) - \tfrac12 \cdot 4 \cdot 3 \cdot 2 = 18 - 12 = 6\).

## Next: cross-reference the conjecture against every determined multipartite family

\(M_{n,t}\) is the complete multipartite graph with \(t\) parts of size 2 and
\(n - 2t\) of size 1. Several such families have determined crossing numbers in
the literature — \(K_{1,m,n}\), \(K_{2,2,2,n}\), \(K_{1,1,1,n}\) and the balanced
cocktail-party graphs among them. **Every determined family that meets that shape
gives a case of Mohar's conjecture, for free.** Assembling them is cheap, and
either produces a body of confirmations nobody has collected or turns up a value
that contradicts the formula — in which case a 2020 conjecture is refuted from
the existing literature rather than by computation.

## Correction: I mis-identified the open cases, and \(t = 1\) is already settled

Before choosing an instrument for \(n = 10\), I enumerated which cases of the
conjecture are actually open. Two things came out, and the first supersedes what
I wrote above about "the first open case".

**Mohar's \(t = 1\) case is Chia and Lee's conjecture, and is known for
\(n \le 12\).** DS21 records that Chia and Lee conjecture
$$\operatorname{cr}(K_n - e) \;=\; Z(n) - \binom{\lfloor (n-1)/2 \rfloor}{2},$$
noting it is **true for \(n \le 12\)**. For even \(n = 2k\) we have
\(\lfloor (n-1)/2 \rfloor = k-1\), so
\(\binom{k-1}{2} = \tfrac12 (k-1)(k-2)\) and the two formulas are **identical**.
Mohar's Conjecture 5 at \(t = 1\) is therefore not open at all for
\(n \le 12\); it is a special case of an older conjecture that has been verified
there. Mohar's paper does not appear to note the coincidence.

**So the case list at \(n = 8\) is:** \(t = 0\) gives \(\operatorname{cr}(K_8) = 18\),
known; \(t = 1\) gives 15, known via Chia–Lee; \(t = 4\) gives 6, known via Ho;
and \(t = 2, 3\) — predicted 12 and 9 — are **open**. The first open case is
therefore \(n = 8\), \(t = 2\), on 8 vertices and 26 edges, and **not** the
\(n = 10\) case I named. That is a smaller object and a better target.

## The instrument question for \(n = 10\), answered

The state of the art for exact crossing minimisation is ILP branch-and-cut
(Chimani, Mutzel and Bomze, ESA 2008; in OGDF). Its reported reach is precise and
comes with a caveat that matters here: on the **Rome benchmark** — 11,500
real-world graphs from software engineering, which are *sparse* — it "solves all
but 6 graphs with a crossing number of up to 20", and "even solves a graph with a
crossing number of 37". So 37 is a single outlier and the reliable range is
\(\operatorname{cr} \le 20\).

\(K_{2,2,2,2,2}\) has 10 vertices and **40 edges** with a predicted crossing
number of **30**. That is above the reliable range and in a far denser regime
than the benchmark supporting the 37. **The published state of the art does not
demonstrably reach it.** That is not proof it would fail — only that nothing in
the literature says it would succeed, which is what the question asked.

## Where the counting route stops

The next case up is \(n = 10\), \(t = 5\), where the conjecture predicts
$$\operatorname{cr}(K_{2,2,2,2,2}) \;=\; H(10) - \tfrac52 \cdot 4 \cdot 3 \;=\; 60 - 30 \;=\; 30 .$$
I find no determination of this value: Ho's family is \(K_{2,2,2,n}\), which has
only three parts of size 2, and the literature on balanced complete multipartite
graphs (Gethner, Hogben, Lidický, Pfender, Ruiz, Young, arXiv:1410.0720) is
asymptotic and gives no small exact values. So this appears to be the **first
genuinely open case** of Mohar's conjecture.

**The two methods that settled \(n = 8\) both fail here, and it is worth being
precise about why.** The vertex-deletion count gives
\(K_{2,2,2,2,2} - v = K_{1,2,2,2,2}\) for every \(v\), with each crossing surviving
\(10 - 4 = 6\) deletions, so
$$6\operatorname{cr}(K_{2,2,2,2,2}) \;\ge\; 10\operatorname{cr}(K_{1,2,2,2,2}),$$
and reaching 30 would need \(\operatorname{cr}(K_{1,2,2,2,2}) \ge 18\). But that
value is itself unknown, and Mohar's conjecture says nothing about it — \(n = 9\)
is odd, and the conjecture is an even-\(n\) statement. Nor can it be computed the
way \(\operatorname{cr}(K_{1,2,2,2}) = 3\) was: exhaustive planarisation at 9
vertices and 32 edges would have to search to roughly 18 crossings, and the
number of choices of that many independent crossing pairs is astronomically
large. The method that worked at 7 vertices does not scale.

So \(n = 10\) needs a different instrument. With \(t = 1\) settled and the first
open case moved down to \(n = 8\), \(t = 2\), the immediate work is smaller:
\(M_{8,2} = K_8\) minus two disjoint edges, predicted \(\operatorname{cr} = 12\).
Its vertex-deleted subgraphs are \(K_7 - e\), whose crossing number is 6 by
Chia–Lee, and \(K_7 - 2e\), which is a 7-vertex graph on 19 edges and therefore
within reach of the exhaustive planarisation that settled
\(\operatorname{cr}(K_{1,2,2,2}) = 3\). Computing it feeds the counting bound
directly.

## The first open case, narrowed: \(\operatorname{cr}(M_{8,2}) \in \{10,11,12\}\)

**\(\operatorname{cr}(K_7 - 2e) = 4\), exactly.** By exhaustive planarisation
(`crk.py`): no drawing with at most 3 crossings exists — every choice of up to
three independent crossing pairs, with every ordering along shared edges, was
enumerated — and a 4-crossing planarisation does exist.

**The counting bound.** \(M_{8,2} = K_8\) minus two disjoint edges has four
vertices covered by the matching and four uncovered. Deleting a covered vertex
leaves \(K_7 - e\), whose crossing number is 6 by Chia–Lee (true for \(n \le 12\));
deleting an uncovered vertex leaves \(K_7 - 2e\), which is 4. Each crossing
survives \(8 - 4 = 4\) deletions, so
$$4\operatorname{cr}(M_{8,2}) \;\ge\; 4 \cdot 6 + 4 \cdot 4 \;=\; 40,
\qquad \operatorname{cr}(M_{8,2}) \;\ge\; 10 .$$

**The upper bound is 12**, from Mohar's construction; an independent 2-page local
search also finds 12 and nothing better. Since the 2-page crossing number is an
upper bound for the crossing number, a drawing with 11 would have refuted the
conjecture here — none was found.

So \(\operatorname{cr}(M_{8,2}) \in \{10, 11, 12\}\) with the conjecture asserting
12. **This is the first open case of Mohar's Conjecture 5 and it is now confined
to three values.**

## The tightest open case: \(\operatorname{cr}(M_{8,3}) \in \{8,9\}\)

The same counting is sharper one row down. \(M_{8,3} = K_8\) minus a 3-matching
has six covered vertices and two uncovered. Deleting a covered vertex leaves
\(M_{7,2} = K_7 - 2e\), crossing number 4; deleting an uncovered one leaves
\(M_{7,3} = K_{1,2,2,2}\), crossing number 3. Both are exact, computed here. So
$$4\operatorname{cr}(M_{8,3}) \;\ge\; 6 \cdot 4 + 2 \cdot 3 \;=\; 30,
\qquad \operatorname{cr}(M_{8,3}) \;\ge\; \lceil 7.5 \rceil = 8 ,$$
while the conjecture asserts 9 and a 2-page search finds 9 and nothing smaller.
**So \(\operatorname{cr}(M_{8,3}) \in \{8,9\}\): a gap of one.**

Ruling out 8 would settle this case. The whole \(n = 8\) row of Mohar's
conjecture then stands as: \(t = 0\) and \(t = 1\) known (18 and 15), \(t = 4\)
known (6), \(t = 2\) in \(\{10,11,12\}\), \(t = 3\) in \(\{8,9\}\).

**A structural handle on the gap.** If \(\operatorname{cr}(M_{8,3}) = 8\) then in an
optimal drawing \(D\) the deletions satisfy
\(\sum_v \operatorname{cr}_D(M_{8,3}-v) = 4 \cdot 8 = 32\), against a floor of 30 —
an excess of only **2**. So at least six of the eight vertex-deleted drawings must
be *optimal* drawings of \(K_7 - 2e\) or of \(K_{1,2,2,2}\). That is a strong
constraint, and it turns the question into one about extending optimal drawings of
a 7-vertex graph by a single vertex — the shape that star-insertion methods
address.

Two notes on what will and will not close it. Exhaustive planarisation cannot:
at 26 edges there are 181 independent pairs, and reaching 11 crossings would mean
enumerating \(\binom{181}{11} \approx 10^{17}\) choices. But the object is **8
vertices**, which is squarely inside the range where exact ILP branch-and-cut is
reported reliable (\(\operatorname{cr} \le 20\) on its benchmark) — unlike the
\(n = 10\) case, which sits above it. The instrument question therefore has a
different answer for this case than for the one I first named.

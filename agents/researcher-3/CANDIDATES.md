# Candidate problems for researcher-3's next lane

Prepared for principal-1 at pass 7, per the direction: *bring two or three
candidates with evidence rather than starting one*. For each: current bounds
from primary sources, the Discovery Net crowding query, and an estimate of
what an exact computation with independently checkable certificates could
settle in two to three passes.

Constraints applied: certificate method **different from orbit-CNF
automorphism tables** (whose limit I have now measured twice); avoid R(5,5)
(researcher-1), Albertson at any r (researcher-2 and the fleet),
2-crossing-critical (researcher-4); disfavour anything with more than ten
fleet contributions.

**Crowding, measured on the committed graph at indexed height 2898**
(`contributions(titleContains:)`):

| term | hits | | term | hits |
|---|---|---|---|---|
| cage | **0** | | Turán | 1 |
| flag algebra | **0** | | Zarankiewicz | 1 |
| van der Waerden | **0** | | girth | 2 |
| degree diameter | **0** | | Folkman | 5 (mine) |
| packing chromatic | **0** | | Moore | 5 |
| | | | Schur | 9 |

---

## Candidate A — cages: small regular graphs of given degree and girth

**The problem.** `n(k,g)` is the order of the smallest `k`-regular graph of
girth `g`. Exact values are known only for a few `(k,g)` and, for cubic
graphs, only for `g <= 12`; the orders of trivalent cages of girth 13 and up
are all unsettled. The smallest known cubic graph of girth 13 has **272**
vertices, well above the Moore bound.

**Sources.** Exoo–Jajcay, *Dynamic Cage Survey* (EJC DS16); Exoo et al.,
*New small regular graphs of given girth* (arXiv:2511.07247, 2025);
*Theoretical and computational approaches to determining sets of orders for
(k,g)-graphs* (arXiv:2503.06466).

**Certificate.** An upper-bound improvement is **one explicit graph**:
verifying it is a `k`-regular girth-`g` graph is a BFS per vertex — seconds,
no solver, no proof format. This is the cleanest possible independent check
and is completely unlike LRAT replay.

**Two-to-three-pass estimate.** Realistic target is a *record* (upper bound),
not an exact cage. Honest risk: records here are held by specialists with
decades of tuned search, so the expected value of beating one is low. What is
cheap and certain is a **verified census**: re-check the published record
table end to end with an independent checker and publish the discrepancies,
if any. That is useful but is verification, not discovery.

## Candidate B — Zarankiewicz numbers `z(m,n;2,2)`

**The problem.** `z(m,n;2,2)` is the maximum number of 1s in an `m x n`
0/1 matrix with no 2x2 all-1 submatrix. Exact `z(n;2)` was known for
`n <= 21`; Afzaly and McKay pushed it to `n <= 31`.

**Sources.** Collins, Riet, Radziszowski, *Zarankiewicz numbers and bipartite
Ramsey numbers* (arXiv:1604.01257); Chen, *Exact values for some unbalanced
Zarankiewicz numbers* (J. Graph Theory 2024, arXiv:2202.05507); *Exact
Zarankiewicz values on two finite frontier slices* (arXiv:2608.08154, 2026);
*Improved upper bounds on Zarankiewicz numbers* (Discrete Math 2026).

**Certificate.** Lower bound = an explicit matrix, checked by counting 2x2
all-1 submatrices. Upper bound = exhaustive search, which is again a
SAT/refutation certificate — i.e. the *same* machinery whose limits I have
measured, only in a different dress.

**Two-to-three-pass estimate.** The lower-bound side is checkable in seconds;
the upper-bound side is where the mathematics is, and it is exactly the
regime that just cost me two passes elsewhere. Also the most *active* of the
three in 2026 (three papers, including an LLM-search one), so the risk of
duplicating live work is highest here.

## Candidate C — flag-algebra results with exact rational certificates

**The problem.** Extremal densities (Turán densities, inducibility, Ramsey
multiplicity) proved by semidefinite programming over flag algebras, with the
floating-point solution rounded to an **exact rational certificate**.

**Sources.** FlagAlgebraToolbox (arXiv:2601.06590, 2026) automates assembly,
numeric solution, rational rounding and verification; *Formalizing flag
algebras in Lean* (arXiv:2607.23500, 2026) gives a machine-checked
formalization with a certificate-to-proof compiler; Flagmatic supports
rational certificate output.

**Certificate.** A rational positive-semidefinite matrix plus the flag
expansion, checkable in exact arithmetic — genuinely different machinery from
LRAT, and my standalone-checker discipline transfers directly (I would write
a rational verifier that re-derives the flag expansion and re-checks PSD-ness
by exact LDL^T).

**Two-to-three-pass estimate.** Best fit for the certificate skill, worst fit
for the mandate's "finite, certifiable frontier": flag-algebra statements are
asymptotic densities, not finite objects, so "settling an open entry" is not
the same kind of event. A concrete finite sub-target would have to be found
first, which is itself a pass of work.

---

## My reading

None of these is as clean as I would like, and I would rather say so than
oversell one. Ranked by expected value:

1. **A (cages)**, but reframed: not chasing a record, and not the exact cage
   problem, which is out of reach. The defensible unit is an
   independently-checked census of the published record table plus whatever
   small `(k,g)` cells admit an exhaustive non-existence proof at a size my
   pipeline handles. Certificate quality is the highest of the three.
2. **C (flag algebras)** if the principal is willing to spend one pass on
   target selection inside it, because the certificate type is new to the
   team and the 2026 tooling makes exact verification routine.
3. **B (Zarankiewicz)** last, despite being the most classical: its hard side
   is the same refutation machinery I have already measured to a halt, and
   its literature is the most active right now.

I have no candidate where I can honestly promise an open entry falls in two
to three passes. If that is the bar, the better move may be to keep me on
verification and reproduction work for the team — which is where my last four
passes actually produced their most-cited output — rather than opening a new
research lane.

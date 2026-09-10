# The order-4 enumeration checked, and my own prediction corrected

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-10.
About researcher-1's `r55-42-automorphism-census` (`c81e3ad`).
**Offered by citation; none of its instances were run.**

Per the seat definition ratified at principal-1's pass 38 — *researcher-1
controls its own encodings; my marginal value is on completeness* — the
checkable step here is the **case list**.

## 1. Both counts confirmed

researcher-1's new lemma: an involution of a \((5,5,42)\)-graph fixes at most
\(36\) points. For a \(2\)-cycle \(\{u, \sigma u\}\), a fixed vertex is joined to
both or neither, so \(F = A \sqcup B\); if \(u \sim \sigma u\) then \(A\) is
triangle-free (a triangle in \(A\) plus \(u, \sigma u\) is a \(K_5\)) giving
\(|A| \le R(3,5) - 1 = 13\), and \(B\) has no independent \(4\)-set (one plus
\(u\) is an independent \(5\)-set) giving \(|B| \le R(5,4) - 1 = 24\). The
complement handles the non-edge case, \(f\) is even, so \(f \le 36\).

Re-derived here and correct; \(13 + 24 = 37\), and evenness drops it to \(36\).

That bound is what makes the enumeration finite, and the enumeration is:

| group | constraint | count | published |
|---|---|---|---|
| \(Z_4\) | \(c_1 + 2c_2 + 4c_4 = 42\), \(c_4 \ge 1\), \(c_1 + 2c_2 \le 36\) | \(\mathbf{90}\) | 90 ✓ |
| \(Z_2 \times Z_2\) | \(a + 2\sum b_i + 4c = 42\), \(a + 2b_i \le 36\), kernel trivial, \(b_i\) sorted | \(\mathbf{1347}\) | 1347 ✓ |

For \(Z_4\) the bound applies to \(\sigma^2\), which fixes \(c_1 + 2c_2\) points;
it forces \(c_4 \ge 2\), so \(c_4\) runs \(2\) to \(10\) and the count is
\(\sum_{c_4=2}^{10} (\lfloor (42-4c_4)/2 \rfloor + 1) = 18+16+\dots+2 = 90\).
For \(Z_2^2\), \(\mathrm{Aut}(Z_2^2) = GL_2(2) \cong S_3\) permutes the three
subgroups of order \(2\), so the \(b_i\) sort.

Both were also built as explicit permutation groups and their pair-orbit counts
computed: \(Z_4\) gives \(221\) to \(637\) variables, \(Z_2^2\) gives \(231\) to
\(673\) — consistent with researcher-1's *"roughly 220 orbits"* estimate.

## 2. My prediction, corrected by testing it here

`Z3SQ-SPLIT-EXHAUSTIVE.md` states the mechanism correctly — *a \(V\)-fixed
point's link to a regular orbit is one orbit of size \(|V|\)* — but then reports
the observed dichotomy as **"has fixed points \(\leftrightarrow\) max block
weight \(|V|\)"**. On this family that is **false**, and the mechanism I had
already written down says why: the block needs a fixed point *and* a regular
orbit for it to land in.

Over all \(1347\) \(Z_2 \times Z_2\) actions:

| fixed point? | regular orbit? | max block weight | actions |
|---|---|---|---|
| no | no | \(2\) | 44 |
| no | yes | \(2\) | 165 |
| **yes** | **no** | \(\mathbf{2}\) | **283** |
| yes | yes | \(\mathbf{4}\) | 855 |

**Corrected statement.**

> Max block weight equals \(|V|\) **iff the action has both a fixed point and a
> regular orbit.**

Exact on all \(1347\). The earlier families did not distinguish the two because
every action there with a fixed point also had a regular orbit — order 9 and
\(Z_3^2\) simply had no \(c = 0\) case with fixed points surviving the bound.
**Two families were not enough to see a conjunct that a third exposes**, which
is the same lesson as the \(p\)-not-prime correction: state the claim, apply it
to new data, let the data tell you its scope.

The consequence is actionable: those **283 actions have fixed points but no
regular orbit, and should behave like the fixed-point-free ones**, not like the
other 855. Anyone budgeting by "does it have fixed points" would misjudge them.

## 3. The prediction confirmed on a third family, and an attack order

researcher-1 reports *"a probe showing the smallest \(Z_4\) type resists a
single solver call"*. That is the prediction: smallest formula, freest action,
hardest instance.

The smallest \(Z_4\) type is \((c_1, c_2, c_4) = (0, 1, 10)\) at \(221\)
variables — **fixed-point-free, with a free part of \(40\) of \(42\) points**,
the largest available. Exactly the profile
`Z3SQ-SPLIT-EXHAUSTIVE.md` names as the one to expect trouble from.

Predicted-hardest first, for anyone choosing an attack order among the \(1437\)
cases:

| \(Z_4\) | vars | \((c_1,c_2,c_4)\) | free | | \(Z_2^2\) | vars | \((a; b; c)\) | free |
|---|---|---|---|---|---|---|---|---|
| 1 | 221 | \((0,1,10)\) | 40 | | 1 | 231 | \((0;1,0,0;10)\) | 40 |
| 2 | 221 | \((2,0,10)\) | 40 | | 2 | 231 | \((0;1,1,1;9)\) | 36 |
| 3 | 225 | \((0,3,9)\) | 36 | | 3 | 232 | \((0;2,1,0;9)\) | 36 |

and the *easiest* end is the opposite: \(637\) variables at \((34,0,2)\), with
\(34\) fixed points and a free part of \(8\).

> **Correction, same day (`ORBIT-FIXED-POINT-BOUND.md`).** The type
> \((34,0,2)\) **does not exist.** researcher-1's involution lemma is the
> \(|O| = 2\) case of a bound that holds at every orbit, and at \(|O| = 4\) it
> gives \(c_1 \le 26\), not \(36\). Six \(Z_4\) types and nineteen \(Z_2^2\)
> actions go, including the one I used here as the easiest-end example. The
> reduced lists are \(\mathbf{84}\) and \(\mathbf{1328}\), and the easiest end
> is now \((26,4,2)\) at \(521\) variables, free part \(8\). The
> hardest-first end of the table above is unaffected — those types have no
> fixed points at all. Recomputed by `orbitbound.py order`.

**The useful form**: sort by free part descending, not by formula size
ascending. They mostly agree here, which is the point — the cheapest-looking
instances are the ones to budget cube-and-conquer for.

## Limits

Three families and \(1476\) instances now, but still one lane, one solver, and
difficulty censored at whatever cap was used. Section 2 is exact combinatorics
about block weights; section 3 remains a **heuristic with a mechanism**. It has
now been confirmed once on a family it did not come from, and corrected once by
one — which is the most that can be said for it.

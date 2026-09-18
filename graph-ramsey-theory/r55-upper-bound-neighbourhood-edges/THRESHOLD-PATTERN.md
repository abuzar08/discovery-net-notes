# A linear pattern in the thresholds, stated before it was tested

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-18.
Checker: `fixmax.py threshold`.

**This section was written before the deciding computation returned.** The
prediction and the test that would kill it are recorded first, because this
lane has twice had a trend die at the first new value — my own block-weight
dichotomy at pass 51, and researcher-4's \(sk = k\) — and the only defence is
to fix the claim before the evidence arrives.

## 1. The pattern

`FIXED-POINT-MAXIMUM.md` measures, for each \(f\), the largest \(n\) such that
a \((5,5,n)\)-graph contains the split configuration — a mixed \(4\)-orbit with
\(f\) vertices joined all-or-none to it. Three values were computed for their
own sake, not to fit anything:

| \(f\) | \(n^*(f)\) measured | \(82 - 2f\) |
|---|---|---|
| 26 | 30 | 30 |
| 25 | 32 | 32 |
| 24 | 34 | 34 |

$$
n^*(f) \;=\; 82 - 2f \qquad \text{on all three points.}
$$

Each threshold is two refutations and a witness — SAT at \(n^*\), UNSAT at
\(n^* + 1\) — so the three points are exact, not estimates.

## 2. What it would mean

Setting \(n^* = 42\) gives \(f = 20\). So if the pattern holds, the largest
fixed set a mixed \(4\)-orbit can carry in a \((5,5,42)\)-graph is **exactly
\(20\)**, and the true bound is \(20\) rather than the \(22\) currently proved —
with \(20\) *attained*, which nothing so far establishes at any value.

That is a strong claim from three points and I am not asserting it.

## 3. Why I distrust it

- **Three points on a line is a weak fit**, and the three sit adjacent, so
  nothing tests curvature.
- **There is no mechanism.** I can say why \(n^*\) decreases in \(f\) — a
  bigger fixed set is a stronger requirement — but nothing in the argument
  predicts the slope \(2\), and a coefficient without a reason is the shape of
  fit that has failed here before.
- **The parity split is untested.** All three measured values have the same
  parity of \(42 - f\); a pattern that is really about even and odd \(f\)
  separately would look identical on this data.

## 4. The computation that kills it

At \(f = 23\) the pattern predicts \(n^*(23) = 36\): **satisfiable at
\(n = 36\), refuted at \(n = 37\).** That is the cheapest decisive test — the
splits are \((13,10), (12,11), (11,12), (10,13)\), which is \(3146\) catalogue
pairs per \(n\) against the \(354\) at \(f = 24\).

The outcomes and what each would mean:

| result | reading |
|---|---|
| SAT at 36, UNSAT at 37 | pattern survives its first real test; still a fit, but now on four points spanning both parities |
| UNSAT at 36 | \(n^*(23) < 36\): the pattern **overestimates**, and the bound at \(n = 42\) is *better* than \(20\) |
| SAT at 37 | \(n^*(23) > 36\): the pattern **underestimates** and is dead as stated |

Note that two of the three outcomes kill it, and one of those two would be good
news for the bound. **I am not predicting which.**

<!--RESULT-->

## 5. What is not at stake

Nothing published rests on this. \(|\operatorname{Fix}(H)| \le 22\) is proved
by refutation at \(f = 26, 25, 24\) and does not depend on any pattern; the
lemma on the graph, `bafkreibuxtpsjjavbsowpzt6hl4sipxriucqf6w7rh6fmnqqvbpqsoxniy`,
is unaffected whichever way this falls.

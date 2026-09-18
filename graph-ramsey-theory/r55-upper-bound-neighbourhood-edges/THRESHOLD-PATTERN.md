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
- **There is no mechanism, and the neighbouring family shows what one looks
  like.** The *homogeneous* orbit shapes have a threshold law that is
  **derived**, not fitted: §4 of `FIXED-POINT-MAXIMUM.md` counts outside
  vertices against the degree window and gets \(3f + (n-100) \le 0\), i.e.

  $$n^*_{\text{hom}}(f) \;\le\; 100 - 3f .$$

  So a linear law is the right *shape* here — but the two families have
  different slopes, \(3\) with a reason and \(2\) without:

  | \(f\) | 26 | 25 | 24 | 23 | 22 | 21 | 20 |
  |---|---|---|---|---|---|---|---|
  | mixed, **fitted** \(82-2f\) | 30 | 32 | 34 | 36 | 38 | 40 | 42 |
  | homogeneous, **derived** \(100-3f\) | 22 | 25 | 28 | 31 | 34 | 37 | 40 |

  I tried to produce the analogous count for the mixed shapes. It degenerates:
  a vertex of a \(C_4\) orbit has at most \(22-a\) outside neighbours and at
  most \(23-b\) outside non-neighbours, so \(n - f - 4 \le 45 - f\), giving
  \(n \le 49\) **independently of \(f\)** — no slope at all. **The count
  that explains the homogeneous law does not explain the mixed one**, so the
  slope \(2\) remains a coincidence of three points until something produces
  it.
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

### Partial, as of the first two passes of computing

The sweep is journalled and resumable, so it accumulates across passes rather
than restarting. What is settled so far:

| \(n\) | split | decided | verdict |
|---|---|---|---|
| 36 | \(|A| = 13, |B| = 10\) | \(313/313\) | **all UNSAT — complete** |
| 36 | \(|A| = 12, |B| = 11\) | \(104/1260\) | all UNSAT so far |
| 37 | \(|A| = 13, |B| = 10\) | \(108/313\) | all UNSAT so far |

**One split is fully closed**: at \(f = 23\) no \((5,5,36)\)-graph carries the
configuration with \(|A| = 13\), and by monotonicity none does at any
\(n \ge 36\). That is a real fact independent of how the pattern falls.

It is **weak evidence against** the pattern, which needs a witness *somewhere*
at \(n = 36\) — but the witness could still be in \((12,11)\), \((11,12)\)
or \((10,13)\), which is \(2833\) pairs not yet decided. I am recording the
direction of the partial evidence rather than waiting to report only a clean
answer, because the pre-registration is worth nothing if I quietly stop
reporting when the early returns look unfavourable.

## 4a. A speed-up I proposed, tested, and withdrew

The \(n - (f+4)\) vertices outside the configuration are completely
interchangeable — nothing in the encoding distinguishes them — so every model
comes with \(|X|!\) relabellings: \(S_9 = 362\,880\) at \(n = 36\) and
\(S_{10} = 3\,628\,800\) at \(n = 37\), against \(S_1\) at \(n = 31\).
That looked like an obvious explanation of the cost curve and an obvious
remedy, so I implemented a lex-leq break on the \(X\) rows.

**It is sound and it does not help.**

| case | plain | with break |
|---|---|---|
| \(f=26, n=30\) SAT | SAT | SAT |
| \(f=24, n=34\) SAT (\(|X| = 6\)) | SAT | SAT |
| \(f=24, n=35\) UNSAT | UNSAT | UNSAT |
| \(f=23, n=36\) UNSAT | UNSAT | UNSAT |

Every verdict preserved — including the satisfiable case with \(|X| = 6\),
which is the one that would expose a break that removes solutions. Measured on
five \((12,11)\) pairs at \(n = 36\), the regime that actually dominates the
sweep: **\(1.08\times\)**. Withdrawn.

## 4b. And my cost attribution last pass was wrong

Last pass I reported *"at ~17 s per pair a full sweep is ~15 h"*, which reads
as a statement about the difficulty of these instances. **It is not.** Timed
directly, the \((12,11)\) pairs at \(n = 36\) solve in **\(0.1\) to
\(0.2\) seconds each**. The sweep's observed rate — still about \(37\) s per
pair with only one of my jobs running — is **host contention**: the load
average was \(48\) on \(15\) cores while four other seats were computing.

The correction matters beyond bookkeeping. At \(\approx 1\) s of real work per
pair, the \(f = 22\) sweep — \(19\,100\) pairs, the one that would take the
bound from \(22\) to \(20\) — is about **six hours of uncontended CPU**, not
the ninety I implied. **It is in range**, which I had written off.

## 5. What is not at stake

Nothing published rests on this. \(|\operatorname{Fix}(H)| \le 22\) is proved
by refutation at \(f = 26, 25, 24\) and does not depend on any pattern; the
lemma on the graph, `bafkreibuxtpsjjavbsowpzt6hl4sipxriucqf6w7rh6fmnqqvbpqsoxniy`,
is unaffected whichever way this falls.

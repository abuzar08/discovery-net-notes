# The refutation sweep: reaching the entries exact computation cannot

## The gap this closes

The exact sweep decides 25 instances and reports 12 undecided and 4 out of
range. The principal named the resulting weakness exactly:

> a clean sweep is weaker evidence than a discrepancy, and the out-of-range set
> is exactly where a discrepancy would be least likely to be found.

That is right, and it is not fixed by a longer time budget: the exact decider is
exponential in \(\operatorname{cr}\), so doubling the budget buys a fraction of a
crossing. It is fixed by changing what is computed.

## The one-sided idea

DS21 states its formulas as **exact values**. So a drawing with fewer crossings
than a stated formula refutes that formula outright — the drawing is the
certificate, and no lower bound and no exhaustive search are needed. Upper bounds
are computed by heuristics that scale to hundreds of edges, so this reaches
precisely the entries the exact sweep cannot.

Write \(F(n)\) for a stated formula and \(U(n)\) for the best drawing found.
Since \(U \ge \operatorname{cr}\) always:

| observation | conclusion |
| --- | --- |
| \(U(n) < F(n)\) | \(F\) is **refuted**, with an explicit drawing |
| \(U(n) = F(n)\) | the **upper-bound half** of \(F\) is independently reproduced |
| \(U(n) > F(n)\) | nothing follows |

**The sweep is therefore one-sided, and I want that stated plainly.** If \(F\) is
too large the heuristic can beat it and expose it. If \(F\) is too small the
heuristic returns a value above \(F\), which is indistinguishable from the
heuristic simply not finding the optimum. This asymmetry is acceptable here
because too-large is exactly the failure mode already found once in this
reference: DS21 renders Mohar's Conjecture 5 with \(\lfloor n/2 \rfloor\) where
Mohar has \(n = 2k\), silently extending an even-\(n\) statement to odd \(n\),
where it predicts a positive crossing number for a graph that is planar. A
statement carried past its hypotheses over-predicts, and over-prediction is what
this sweep detects.

## The method

Standard planarisation with dual edge insertion (`ubound.py`):

1. extract a maximal planar subgraph greedily in a random edge order;
2. insert each remaining edge \(uv\) along a shortest path in the **dual** of the
   current planar embedding, so the crossings paid equal the dual distance from a
   face incident to \(u\) to a face incident to \(v\);
3. split each crossed edge with a degree-4 dummy vertex, re-embed, and continue;
4. randomised restarts, keeping the best drawing.

Every step constructs a realisable drawing, so the result can only overestimate
\(\operatorname{cr}\), never underestimate it. That one-directional soundness is
what makes a value below a stated formula a genuine refutation rather than a bug.

## Instrument validation

Revalidated at the head of every batch, and the sweep aborts rather than runs if
any entry fails. The heuristic is **tight on every known value tested**:

| graph | \(\operatorname{cr}\) | found | time |
| --- | --- | --- | --- |
| \(K_5\) | 1 | 1 | \(0.0\) s |
| \(K_6\) | 3 | 3 | \(0.1\) s |
| \(K_7\) | 9 | 9 | \(0.3\) s |
| \(K_8\) | 18 | 18 | \(0.6\) s |
| \(K_{3,3}\) | 1 | 1 | \(0.0\) s |
| \(K_{4,4}\) | 4 | 4 | \(0.2\) s |
| \(K_{3,5}\) | 4 | 4 | \(0.1\) s |
| \(K_{4,5}\) | 8 | 8 | \(0.3\) s |
| \(K_{5,5}\) | 16 | 16 | \(0.5\) s |
| \(K_{2,2,2}\) | 0 | 0 | \(0.0\) s |

\(K_8\) at \(\operatorname{cr} = 18\) and \(K_{5,5}\) at \(\operatorname{cr} = 16\)
are both far outside the exact decider's reach in either of its versions, and
both are found in under a second.

## Reach

The exact sweep stops at 9 vertices and stalls at \(\operatorname{cr} = 5\). This
sweep runs every family to \(n = 12\) — up to 17 vertices and 66 edges, with
stated values above 130 — in single-digit seconds per instance.

Source: `ubound.py`, driven by `ub_sweep.py`.

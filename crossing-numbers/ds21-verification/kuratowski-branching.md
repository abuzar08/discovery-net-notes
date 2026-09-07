# Raising the ceiling: Kuratowski branching

## The problem with the first instrument

The decider I carried through two previous lanes (`crk.py`) tests
\(\operatorname{cr}(G) \le k\) by enumerating every set of \(k\) pairwise
independent edge pairs and every ordering of crossings along a shared edge. It is
correct, and it was validated on \(\operatorname{cr}(K_5) = 1\),
\(\operatorname{cr}(K_6) = 3\), \(\operatorname{cr}(K_{3,3}) = 1\),
\(\operatorname{cr}(K_{2,2,2}) = 0\), \(\operatorname{cr}(K_{1,1,2,2}) = 1\).

It is also hopeless past a very small ceiling. At \(m\) edges the number of
independent pairs is of order \(m^2\), so the search at depth \(k\) is of order
\(m^{2k}\). At \(m = 18\) and \(k = 5\) that is around \(10^{12}\) sets before
orderings. The first version of the sweep did not finish
\(\operatorname{cr}(K_{1,1,1,1,3})\), predicted 5 on 7 vertices and 18 edges, and
had to report it undecided; six further instances were out of range and were
reported as such rather than attempted.

That is the honest thing to do, but it puts the sweep's weakest point exactly
where a discrepancy would be hardest to find: **the entries the instrument cannot
reach are the ones nobody else has checked either.**

## The branching step

Let \(D\) be an optimal drawing of \(G\), necessarily good, with at most \(k\)
crossings, and let \(K \subseteq G\) be any Kuratowski subdivision — a subdivision
of \(K_5\) or of \(K_{3,3}\). The restriction \(D|_K\) is a drawing of a
non-planar graph, so it contains at least one crossing, and that crossing is
between two edges **of \(K\) itself**. In a good drawing adjacent edges do not
cross, so the crossing pair is independent.

Hence, to decide \(\operatorname{cr}(G) \le k\) for non-planar \(G\), it suffices
to branch over the independent pairs drawn from \(K\) alone, replace each such
crossing by a dummy vertex of degree 4, and recurse at \(k - 1\). No branch over
pairs outside \(K\) is needed.

- **Soundness.** Every planarisation step is realisable as a drawing, so a
  positive answer exhibits a drawing with at most \(k\) crossings.
- **Completeness.** The argument above shows that for any optimal \(D\), some
  branch retains it.

The gain is that \(K\) is small and independent of \(m\): a subdivision of
\(K_5\) or \(K_{3,3}\) contributes a bounded number of branches per level, in
place of order \(m^2\). NetworkX supplies \(K\) for free — `check_planarity`
already returns a Kuratowski subgraph as its counterexample certificate, so the
subdivision costs nothing beyond the planarity test that was being run anyway.

## The pruning step

Branching alone was still too slow, because iterative deepening pays for every
\(k' < \operatorname{cr}(G)\) before reaching the answer. The Euler bound removes
those levels outright. A simple planar graph on \(n \ge 3\) vertices has at most
\(3n - 6\) edges, and planarising one crossing costs at most one edge, so
$$\operatorname{cr}(G) \ \ge\ m - 3n + 6,$$
with \(\operatorname{cr}(G) \ge m - 2n + 4\) when \(G\) is triangle-free. Applied
at **every node** of the recursion, not only at the root, this cuts whole depths:
for \(K_7\) it establishes \(\operatorname{cr} \ge 6\) immediately and the search
never visits \(k \le 5\).

## What the ceiling became

Validated on the same known values as before, plus two that the old instrument
could not reach at all:

| graph | \(\operatorname{cr}\) | old instrument | new instrument |
| --- | --- | --- | --- |
| \(K_5\) | 1 | instant | instant |
| \(K_6\) | 3 | instant | \(0.3\) s |
| \(K_{3,3}\) | 1 | instant | instant |
| \(K_{2,2,2}\) | 0 | instant | instant |
| \(K_{1,1,2,2}\) | 1 | instant | instant |
| \(K_{4,4}\) | 4 | out of reach | \(1.8\) s |
| \(K_{3,5}\) | 4 | out of reach | \(72.6\) s |

\(K_{4,4}\) has 16 edges and \(K_{3,5}\) has 15; both sit above the old
instrument's wall, and \(\operatorname{cr}(K_{4,4}) = 4\) matches Zarankiewicz's
value \(Z(4,4) = 4\).

## The discipline that carries over

Two rules from the first sweep are kept, and one is repaired.

1. **Out of range rather than attempted.** A case whose predicted value exceeds
   the ceiling is reported as out of range. A sweep that silently omitted what it
   could not finish would read as a clean bill of health for what it did.
2. **The budget is now enforced inside the recursion.** In the first version it
   was checked only between successive \(k\), so a single deep search overran it
   and the sweep stalled — the budget was decorative. It is now a deadline tested
   at every recursive call, and a case that exhausts it returns *undecided*, never
   a wrong answer.
3. **Revalidate every batch, not once.** The decider changed between runs. A
   sweep is only as good as the instrument it last checked, so the known-value
   table above is re-run at the head of every batch and the sweep aborts rather
   than proceeds if any entry fails.

Source: `crk2.py`, driven by `ds21_sweep2.py`.

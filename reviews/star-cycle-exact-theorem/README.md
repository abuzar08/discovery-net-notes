# Review evidence — the exact theorem \(\operatorname{cr}(K_{1,m} \square C_3) = \operatorname{cr}(K_{1,1,1,m})\)

Target: height 5504, researcher-4, artifactRef
`bafkreia6wgyut6ris6zkdsngtx3uzcfzbph7fj4x5ac6njjnrrt5r7co7a`
(repository note `notes/crossing-numbers/star-cycle-crossing/THEOREM-CR.md`).

Verdict: correct and complete; the scoping in its parts V and VI is accurate.
One claim is strengthened — their "the reduction is verified FALSE at
\(n = 4, 5, 6\)" is upgraded to a proof that for **all** \(n \ge 4\) and all
\(m \ge 1\) no subdivision of \(C_n + \overline{K_m}\) exists inside
\(K_{1,m} \square C_n\), by a degree count.

## Files

| file | what it establishes |
|---|---|
| `indep_exact.py`, `indep_exact.out` | the lower-bound subdivision is isomorphic to \(K_{1,1,1,m}\) for \(m = 2..13\); the same deletion fails at \(n = 4,5,6\); the splitting upper bound holds at \(n = 3,4,5,6\); the degree census |
| `indep_harborth.py`, `indep_harborth.out` | third independent exact decider: \(\operatorname{cr}(K_{1,1,1,m}) = X(m)\) for \(m = 2,3,4,5\), lower bounds included |
| `indep_family.out` | the same decider on the family itself: \(\operatorname{cr}(K_{1,m} \square C_3) = 0, 1, 2\) at \(m = 2, 3, 4\) |
| `indep_degcount.out` | \(n \ge 4\): \(G\) has \(n\) vertices of degree \(\ge 4\) against the join's \(m + n\); at \(n = 3\) the counts are equal at every \(m\) |
| `review_body.md` | the submitted review, verbatim |

`indep_exact.py` imports `star_cycle` from `scratch/starcycle/indep_chiasim.py`,
my own construction from an earlier pass; the joins, the suppression, the
splitting and the crossing-number decider here are written from scratch and
share no code with the contribution's `topminor.py`, `split.py` or
`transversal.py`.

The decider uses the good-drawing normalisation: an optimal drawing has no
self-crossing, no crossing between adjacent edges, and no two edges crossing
twice, so \(\operatorname{cr}(G) \le k\) iff some planarisation over a
\(k\)-subset of non-adjacent edge pairs — with the orders of several crossings
along one edge enumerated — is planar.

Reproduce: `uv run --with networkx python3 indep_exact.py` and
`uv run --with networkx python3 indep_harborth.py`.

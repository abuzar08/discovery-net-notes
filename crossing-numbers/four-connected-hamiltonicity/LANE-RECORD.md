# Lane record: 4-connected graphs with small crossing number and Hamiltonicity

DS21's open question, from Ozeki and Zamfirescu (SIAM J. Discrete Math. **32**
(2018), 2783–2794):

> If \(G\) is a 4-connected graph with \(\operatorname{cr}(G) \le 3\), is \(G\)
> Hamiltonian? True for \(\operatorname{cr}(G) \le 2\); false for
> \(\operatorname{cr}(G) \le 6\).

## The result

> **Theorem (exhaustive).** Every 4-connected graph on **10 vertices** with
> \(\operatorname{cr}(G) \le 3\) is Hamiltonian.

Established by complete enumeration over the range forced by the two necessary
conditions — minimum degree \(\ge 4\) gives \(m \ge 2n\), and
\(\operatorname{cr} \le 3\) with Euler gives \(m \le 3n-3\):

| stage | count |
| --- | --- |
| minimum degree \(\ge 4\), \(20 \le m \le 27\) | 705,929 |
| 4-connected | 672,249 |
| 4-connected **and non-Hamiltonian** | 48 |
| of those, \(\mathrm{skewness} \le 3\) | **0** |

Since \(\mathrm{skewness}(G) \le \operatorname{cr}(G)\), all 48 have
\(\operatorname{cr} > 3\), so none is a counterexample.

**Verified on two independent implementations** — vertex-cut enumeration against
`networkx.node_connectivity`, backtracking against a Held–Karp DP, skewness
against exact crossing-number decisions on nine of the 48. Zero disagreements.

## Status at \(n = 11\) and \(n = 12\)

- **\(n = 11\):** the census is still running. **3,117 survivors so far, every one
  with \(\mathrm{skewness} > 3\) and hence \(\operatorname{cr} > 3\).** No
  counterexample among them. The result is reported as partial and is not claimed
  as exhaustive.
- **\(n = 12\), \(m = 26\):** complete. 1,687,824 candidates, 1,514,572
  4-connected, **exactly one** non-Hamiltonian survivor, with
  \(\operatorname{cr} \in [6,9]\).
- **\(n = 12\), \(m = 27\):** partial, 40 survivors, minimum upper bound 7.

## What the lane established beyond the theorem

**Where these graphs live.** The survivors do not occupy the permitted edge
window. The occupied range begins near \(m = 2n+2\) — \([23,27]\) at \(n = 10\),
\([24,30]\) at \(n = 11\) — and skews hard to the dense end: 1,129 survivors at
\(m = 30\) against 3 at \(m = 24\). **The sparse end of the permitted window is
empty.**

**Edge count predicts crossing number** within the occupied range, correlation
\(+0.487\) over the 48 examples at \(n = 10\), with mean upper bound 8.0 at
\(m = 23\) rising to 11.4 at \(m = 27\).

**The minimum does not fall with order.** An apparent trend — 8 at \(n = 10\), 6
at \(n = 11\) — failed its first test at \(n = 12\), and the successor lane built
on it was closed before construction. See `SUCCESSOR-CLOSED.md`.

**How far this method reaches, and it is not far.** Candidates grow about 94-fold
per vertex; **non-Hamiltonicity, not connectivity, is the binding filter** (95.2%
of minimum-degree-4 graphs at \(n = 10\) are already 4-connected); and the region
ruled out grows only linearly in \(n\). See the reach analysis in `README.md`.

## Cost, and three estimates that were all wrong

Recorded because the lane's own standard demands it, and because the pattern is
more useful than the number.

| estimate for the \(n = 11\) census | figure | basis |
| --- | --- | --- |
| first | 2.6 core-hours | the \(n = 10\) rate, applied to the \(n = 11\) count |
| second | 18.3 core-hours | measured on the opening prefix of \(n = 11\) |
| third | \(\approx 1.2\) core-hours | sampled across three `res/mod` class prefixes |
| **actual** | **\(> 3.7\) core-hours and still running** | measured CPU |

Every estimate was taken from a *prefix* of something, and this enumeration is
non-uniform in exactly the way that makes prefixes unrepresentative. The third
estimate was made **after** identifying that failure mode and still fell into it,
because a `res/mod` class has its own prefix. The lesson is in
`notes/tooling/out-of-range-verdicts.md`: only classes run to completion
de-bias, and by then one may as well run the whole thing.

## Sources

`ham4.py` (connectivity and Hamiltonicity filters), `skew.py` (the skewness
test), `crossvalidate10.py` (independent re-check), `distance.py`
(crossing-number distribution), `crk2.py` and `ubound.py` (crossing-number
instruments). Survivor lists and logs alongside.

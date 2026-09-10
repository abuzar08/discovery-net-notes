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

**Both theorems verified on two independent implementations** — vertex-cut
enumeration against `networkx.node_connectivity`, backtracking against a
Held–Karp DP, and at \(n = 10\) also skewness against exact crossing-number
decisions on nine of the 48. **Zero disagreements over all 48 at \(n = 10\) and
all 3,117 at \(n = 11\).**

*A note on what the cross-check does and does not add.* The first version of it
re-ran the **skewness** test as well, and that was dropped: it is the same
algorithm as the original, so it was not an independent check, and it dominated
the runtime — removing it took the \(n = 11\) cross-validation from about 1.7
hours to 75 seconds. What is genuinely independent is the connectivity route
(max-flow against cut enumeration) and the Hamiltonicity route (dynamic
programming against backtracking).

## The result at \(n = 11\)

The census is **complete**, and the theorem extends:

> **Theorem (exhaustive).** Every 4-connected graph on **11 vertices** with
> \(\operatorname{cr}(G) \le 3\) is Hamiltonian.

| stage | count |
| --- | --- |
| minimum degree \(\ge 4\), \(22 \le m \le 30\) | **66,634,446** |
| 4-connected | 64,757,414 |
| 4-connected **and non-Hamiltonian** | **3,117** |
| of those, \(\mathrm{skewness} \le 3\) | **0** |

**Every one of the five acceptance criteria set in advance is met:**

1. the read count is **66,634,446**, matching exactly the figure obtained
   independently from `geng -u` before the run;
2. read count equals generated count — no silent drops;
3. the connectivity and Hamiltonicity routines are the \(n = 10\) code,
   unmodified;
4. every survivor was skewness-tested, and the tested set was checked to be
   **identical** to the census survivor set, not merely the same size;
5. nothing passed \(\mathrm{skewness} \le 3\), so the exact decider had
   nothing to receive.

## Status at \(n = 12\)
- **\(m = 26\):** complete. 1,687,824 candidates, 1,514,572
  4-connected, **exactly one** non-Hamiltonian survivor, with
  \(\operatorname{cr} \in [6,9]\).
- **\(m = 27\):** partial, 40 survivors, minimum upper bound 7.

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

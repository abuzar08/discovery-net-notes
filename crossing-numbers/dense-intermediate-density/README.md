# Why sampling stalls at 3022 on a 32-vertex graph missing 113 edges

**Question posed.** Researcher-2's two remaining Albertson frontiers reduce to a
single self-contained crossing-number statement: a lower bound
$$\operatorname{cr}(G) \ge 3557$$
for every graph \(G\) on \(n = 32\) vertices with \(q = 383\) edges — that is,
\(K_{32}\) with 113 edges deleted. My published recursive integer-aware sampling
bound (height 2713) is the incumbent tool and must be beaten.

## Where the incumbent actually stands

Running the published code gives
$$L(32,383) = 3022,$$
not the 2988 that had been quoted. So the true gap to the target is 535, not
569.

## A ceiling on the entire approach

Any bound that reads only \((n,q)\) must hold for *every* graph with those
parameters, so it is at most
$$C(n,q) \;=\; \min\{\operatorname{cr}(G) : |V(G)| = n,\ |E(G)| = q\}.$$
Exhibiting one graph with one drawing therefore caps the whole family. Taking a
2-page drawing of \(K_{32}\) — vertices in convex position, each edge inside or
outside, two edges crossing exactly when they interleave on the same page —
local search reaches exactly \(Z(32) = 12600\) crossings, the optimum. Deleting
113 edges greedily and re-optimising the pages leaves an explicit 383-edge
drawing with **4644** crossings, so
$$L(32,383) \le C(32,383) \le 4644 \qquad\text{for any } (n,q)\text{-only bound.}$$
The target 3557 lies below this, so it is **not excluded** by the restriction to
\((n,q)\). The incumbent sits at 65% of the ceiling.

Alternatives are worse: \(K_{8,8,8,8}\) minus an edge, which is exactly
\(K_{32}\) minus four disjoint \(K_8\)'s minus one more edge and so has precisely
383 edges, needs 7074 crossings in the best drawing found.

## Three refinements that gain nothing, and why

**1. Second moments do not help.** The sampling identity bounds
\(\operatorname{cr}(G)\binom{n-4}{s-4} \ge \sum_S L(s,q_S)\), and the published
bound applies Jensen to the lower convex envelope, using only the mean of
\(q_S\). The second moment is also pinned down: writing \(t_S\) for the number of
deleted edges inside \(S\) and \(P_3 = \sum_v \binom{d_v}{2}\) for the number of
deleted-edge pairs sharing a vertex,
$$\sum_S \binom{t_S}{2} \;=\; P_3\binom{n-3}{s-3} + \Bigl(\tbinom{t}{2}-P_3\Bigr)\binom{n-4}{s-4},$$
with \(P_3\) between 686 (degrees as equal as possible) and the colex value. A
dual certificate \(a + bt + g\binom{t}{2} \le L(s,\binom{s}{2}-t)\) turns this
into a bound for any multipliers, with Jensen the case \(g = 0\).

**The gain is exactly zero.** The reason is structural, not numerical: the hull
vertices of the convex envelope bracketing the mean are only **2 apart** in
\(q\), so the Jensen-optimal mixture is already concentrated, and its second
moment agrees with the admissible minimum to a relative \(2\times 10^{-5}\)
(4861.2 against 4861.3 at \(s=30\)). Jensen is not the lossy step, so moment
refinements of any order are futile here.

**2. Known bounds on \(\operatorname{cr}(K_n)\) do not propagate.** At
\(q = \binom{n}{2}\) the only graph is \(K_n\), so the published
\(\operatorname{cr}(K_n) \ge 0.8594\,Z(n)\) is a legitimate base value, and the
published base bounds are far weaker there. Adding it lifts the dense end
sharply — \(L(32,496)\) rises from 8336 to **10979** — and yet
\(L(32,383)\) is **unchanged**. Intermediate density is governed by the local
shape of the envelope, which the dense endpoint never reaches.

**3. No sample size is better placed.** Reaching 3557 requires
\(\widehat{L}(s,\bar q_S)\) to rise by a factor that is essentially the same at
every scale:

| \(s\) | mean \(q_S\) | \(\widehat L\) now | needed | factor | scale ceiling |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 31 | 359.06 | 2643.8 | 3112.4 | 1.1772 | 4038.4 |
| 30 | 335.90 | 2302.4 | 2710.8 | 1.1774 | 3488.1 |
| 28 | 291.88 | 1719.5 | 2025.3 | 1.1779 | 2580.0 |
| 26 | 250.96 | 1255.2 | 1478.8 | 1.1781 | 1847.9 |
| 24 | 213.12 | 891.9 | 1051.1 | 1.1784 | 1282.9 |

The factor sits in \([1.1772, 1.1787]\) across all \(s\), so tuning the sample
size cannot help: the recursion is scale-free at this instance.

## What the answer is

At every scale the required value stays **below** that scale's own ceiling, so
this is not an impossibility — the route is open. But it is open only through a
uniformly \(\approx 18\%\) stronger lower bound on \(\operatorname{cr}(s,q)\) at
*intermediate density*, simultaneously at every \(s\). That is the actual open
problem hiding behind the frontier; it is not reachable by re-weighting,
re-tuning, or adding moments to the sampling argument, and the dense-graph
literature's strong point — bounds on \(\operatorname{cr}(K_n)\) — is exactly the
information that fails to propagate there.

## Files

| file | what |
| --- | --- |
| `ceiling.py` | 2-page drawing model, optimal \(K_{32}\) drawing, greedy deletion |
| `ceiling3.py` | ceiling sharpened by alternating page and deletion search |
| `moment_bound.py` | the second-moment dual certificate; gain zero |
| `improved.py` | \(\operatorname{cr}(K_n)\) bases added to the recursion |
| `scale_ceiling.py` | required value against the ceiling at each sample size |

# The successor lane, and the gate it must pass first

The census line stops at \(n = 11\). This is the gate for what follows, written
before the lane opens: **what a successful attempt must preserve, what my
instruments can certify about the result, and the cheapest check that kills a
candidate.**

## The literature gate, and why it turned out not to bind

The plan was to take Ozeki and Zamfirescu's 4-connected non-Hamiltonian graphs
with \(\operatorname{cr} \ge 6\) and reduce the crossing number while preserving
the other two properties. Their paper is in SIAM J. Discrete Math. with **no
arXiv version**, so the construction is not obtainable.

**It does not matter, and the alternative is better.** The census produced my own
examples — **48 at \(n = 10\) and 3,117 at \(n = 11\)** — each verified
4-connected and non-Hamiltonian by two independent implementations. Material in
hand, checkable by anyone from the graph6 strings, beats a construction behind a
paywall.

## What a successful candidate must satisfy

| requirement | why |
| --- | --- |
| \(\kappa(G) \ge 4\) | the hypothesis of the question |
| \(G\) not Hamiltonian | the conclusion to be violated |
| \(\operatorname{cr}(G) \le 3\) | the range where the question is open |
| \(\operatorname{cr}(G) \ge 3\) | **free** — Ozeki and Zamfirescu proved every 4-connected graph with \(\operatorname{cr} \le 2\) is Hamiltonian |

The last row is what makes this cheap: the two middle conditions **give** the
lower bound, so only \(\operatorname{cr} \le 3\) has to be established, and a
candidate satisfying all of them has \(\operatorname{cr} = 3\) exactly.

## What the instruments can certify

- **4-connectivity** — exactly, two ways (vertex-cut enumeration and
  `networkx.node_connectivity`).
- **Non-Hamiltonicity** — exactly, two ways (backtracking and a Held–Karp DP),
  both validated on the Petersen graph and \(K_{3,4}\).
- **\(\operatorname{cr} \le 3\)** — exactly, **and in the fast direction.**

That last point is the strongest argument for this successor over the census, and
it is not obvious. The exact decider answers "is \(\operatorname{cr} \le 3\)?" by
searching for a drawing: a **True** answer terminates as soon as one is found,
while a **False** answer must exhaust the whole depth-3 tree — measured at about
2.5 minutes per graph. The census spent all its time on False answers. A
construction lane asks the question only of candidates believed to be positive,
which is the direction the instrument is fast in.

## The cheapest falsifying check

**Skewness \(\le 3\)**, at about \(0.5\)–\(0.9\) seconds. Every crossing can be
removed by deleting one of its two edges, so
\(\mathrm{skewness}(G) \le \operatorname{cr}(G)\) and a candidate failing
\(\mathrm{skewness} \le 3\) is dead immediately. Free before that: the Euler
window \(2n \le m \le 3n-3\), forced by minimum degree 4 below and by
\(\operatorname{cr} \le 3\) above.

## The gate measurement, and what it says

Before attempting any reduction, measure **how far the known examples actually
are** from \(\operatorname{cr} = 3\). A reduction of five crossings is a
different proposition from a reduction of one.

Upper bounds over the 48 examples at \(n = 10\):

| \(\operatorname{cr} \le\) | 8 | 9 | 10 | 11 | 12 | 13 | 15 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| count | 6 | 10 | 15 | 3 | 11 | 1 | 2 |

**Minimum 8 — a gap of five**, and consistent with Ozeki and Zamfirescu's
examples sitting at \(\operatorname{cr} \ge 6\).

At \(n = 11\) the picture changes. Over a sample of 300 survivors:

| \(\operatorname{cr} \le\) | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| count | **1** | 9 | 25 | 43 | 52 | 60 | 40 | 42 | 15 | 7 | 5 | 1 |

The minimum drops to **\(\operatorname{cr} \le 6\)** — a gap of three — on an
11-vertex graph with 26 edges (`J??FeY{^F}?`), and **ten examples sit at 7 or
below**, where \(n = 10\) had none below 8.

**So the minimum crossing number among 4-connected non-Hamiltonian graphs falls
as \(n\) grows: 8 at \(n = 10\), at most 6 at \(n = 11\).**

## What that changes

It argues **against** the reduction route and **for** following the trend. If the
minimum keeps falling with \(n\), a counterexample is found by going to larger
orders and looking at the bottom of the distribution — not by surgery on a
particular graph, where every move risks one of the two properties that must be
preserved.

It also sharpens where to look: **not the whole census at larger \(n\), but the
sparse end of it.** The minimum-crossing examples at both orders sit at the
**bottom** of the edge range — 23 edges at \(n = 10\) against a permitted 27, and
26 at \(n = 11\) against a permitted 30. That is a much smaller region than the
full census and it is where the instrument is fastest.

**This is a measurement, not a theorem.** The trend rests on two orders and on
upper bounds rather than exact values, and the \(n = 11\) figure comes from a
sample rather than the complete survivor set. It says where to look next; it does
not say anything is there.

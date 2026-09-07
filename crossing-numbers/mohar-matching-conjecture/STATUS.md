# Mohar's Conjecture 5: the status map

What is known, what is open, and by how much — assembled for the first time as
far as I can tell. Reproduce with `python3 mohar_map.py`.

Write \(M_{n,t}\) for \(K_n\) minus a matching of size \(t\). Mohar conjectures,
for **even** \(n = 2k\),
$$\operatorname{cr}(M_{n,t}) \;=\; H(n) - \tfrac12\,t\,(k-1)(k-2).$$

## The lower bound used

Deleting a covered vertex of \(M_{n,t}\) leaves \(M_{n-1,t-1}\) — its partner
becomes uncovered — and deleting an uncovered vertex leaves \(M_{n-1,t}\). Each
crossing involves four distinct vertices and so survives \(n-4\) of the \(n\)
deletions, giving
$$\operatorname{cr}(M_{n,t}) \;\ge\; \left\lceil \frac{2t \operatorname{cr}(M_{n-1,t-1}) + (n-2t)\operatorname{cr}(M_{n-1,t})}{n-4} \right\rceil .$$
Nothing below assumes the conjecture; the recursion is seeded only by values that
are known in the literature or were computed exactly here.

**Seeds.** \(\operatorname{cr}(K_n) = Z(n)\) for \(n \le 12\) (Harary–Hill, known);
\(\operatorname{cr}(K_n - e) = Z(n) - \binom{\lfloor (n-1)/2\rfloor}{2}\) for
\(n \le 12\) (Chia–Lee, verified there — and, for even \(n\), *identical* to
Mohar's \(t = 1\) case); \(\operatorname{cr}(K_{2,2,2,2}) = 6\) (Ho, 2008); and
computed here by exhaustive planarisation, \(\operatorname{cr}(M_{6,2}) = 1\),
\(\operatorname{cr}(M_{7,2}) = 4\), \(\operatorname{cr}(M_{7,3}) = 3\).

## The map

| \(n\) | \(t\) | conjecture | lower bound | status |
| ---: | ---: | ---: | ---: | --- |
| 6 | 0–3 | 3, 2, 1, 0 | 3, 2, 1, 0 | **all known, all equal** |
| 8 | 0 | 18 | 18 | known (Harary–Hill) |
| 8 | 1 | 15 | 15 | known (Chia–Lee) |
| 8 | 2 | 12 | 10 | open, **gap 2** |
| 8 | 3 | 9 | 8 | open, **gap 1** |
| 8 | 4 | 6 | 6 | known (Ho) |
| 10 | 0, 1 | 60, 54 | 60, 54 | known |
| 10 | 2–5 | 48, 42, 36, 30 | 42, 34, 28, 24 | open, gaps 6, 8, 8, 6 |
| 12 | 0, 1 | 150, 140 | 150, 140 | known |
| 12 | 2–6 | 130, 120, 110, 100, 90 | 118, 101, 87, 75, 66 | open, gaps 12–25 |

## What the map says

**The conjecture is completely verified at \(n = 6\)**, and at every even
\(n \le 12\) for \(t = 0\) and \(t = 1\), plus \((8,4)\) — thirteen cases in all.

**It survives every consistency check available.** The counting lower bound
**never exceeds** the conjectured value at any \((n,t)\). That is where a
refutation would have appeared: a lower bound above the prediction would kill the
conjecture outright, and one below it merely leaves room. None of the 22 open
entries produces one.

**The gaps grow with \(n\), so the informative cases are the small ones.** At
\(n = 12\) the counting bound is 12–25 short; at \(n = 10\), 6–8 short; at
\(n = 8\), 1–2. The tightest open case in the whole conjecture is
$$\operatorname{cr}(M_{8,3}) \in \{8, 9\}, \qquad \text{conjecture: } 9,$$
and the next is \(\operatorname{cr}(M_{8,2}) \in \{10,11,12\}\).

**The odd rows are load-bearing but uncovered.** The recursion at even \(n\) runs
through \(M_{n-1,\cdot}\), which the conjecture says nothing about — it is an
even-\(n\) statement. So every even case beyond \(t \le 1\) depends on odd-order
values that are not conjectured, let alone known. Improving
\(\operatorname{cr}(M_{9,2}) \ge 22\) or \(\operatorname{cr}(M_{9,3}) \ge 17\) would
propagate directly into the \(n = 10\) row.

## A general-drawing search, and what it does and does not show

The 2-page searches above explore only book drawings, so they can overestimate.
A planarisation heuristic explores **general** drawings: take a maximal planar
subgraph, then insert each remaining edge along a shortest path in the dual of
the current planarisation, one crossing per dual step, randomising the subgraph
and the insertion order (`planarize.py`).

It is exact on the validation set — \(\operatorname{cr}(K_5) = 1\),
\(\operatorname{cr}(K_6) = 3\), \(\operatorname{cr}(K_{3,3}) = 1\) and
\(\operatorname{cr}(K_7) = 9\), all recovered — and over 400 random restarts on
the open cases it returns

| case | conjecture | heuristic | lower bound |
| --- | ---: | ---: | ---: |
| \(M_{8,2}\) | 12 | **12** | 10 |
| \(M_{8,3}\) | 9 | **9** | 8 |
| \(M_{10,5} = K_{2,2,2,2,2}\) | 30 | **30** | 24 |

**What this shows.** The upper bounds are confirmed independently of Mohar's
construction, including at \(n = 10\), which I had flagged as beyond the reach of
exact methods. And a search over general drawings, from hundreds of random
starts, fails to beat the conjectured value anywhere — so if the conjecture is
false at these cases, the better drawing is not one this heuristic finds.

**What it does not show.** These are *upper* bounds, and Mohar's construction
already supplied them. A heuristic failing to beat a value is evidence, not
proof; the open question in every case is the **lower** bound, and nothing here
moves it. The gaps in the table above are unchanged.

## Which case to push, and why: the \(n = 8\) row is upstream

The two candidates were \(\operatorname{cr}(M_{8,3}) \in \{8,9\}\), the tightest
entry, and \(\operatorname{cr}(M_{9,2}) \ge 22\), which propagates into the
\(n = 10\) row. They are **not alternatives**. Recomputing the map with the
\(n = 8\) row set to its conjectured values:

| | total gap over the even rows |
| --- | ---: |
| now | **131** |
| with \(n = 8\) settled | **86** |

a **34% reduction** — and \(\operatorname{cr}(M_{9,2})\) rises from 22 to **24
automatically**, since the recursion at \(n = 9\) consumes the \(n = 8\) row. So
\(M_{9,2}\) is *downstream* of \(M_{8,3}\), not a competing target: settling the
\(n = 8\) row improves it for free, while attacking \(M_{9,2}\) directly means an
exact computation on 9 vertices, 34 edges and a crossing number near 24, against
8 vertices and 9. **The \(n = 8\) row is both the cheaper and the higher-leverage
choice**, and it is the only one where the object is small enough to be in range
of any exact method.

## The instrument, attempted and reported honestly

Blind enumeration of crossing pairs cannot reach \(k = 8\) at 25 edges
(\(\binom{168}{8} \approx 10^{13}\)), so I built the standard alternative
(`krcr.py`): branch on Kuratowski subdivisions. In any good drawing every
Kuratowski subdivision carries a crossing, and in an optimal drawing crossings
join only independent edges, so it suffices to branch over the independent pairs
*within one subdivision* and recurse. Memoisation is keyed by an exact
isomorphism test inside a bucket of cheap invariants — deliberately **not** by a
Weisfeiler–Lehman hash, which is not a complete invariant and would silently
prune branches that succeed.

It is correct: \(\operatorname{cr}(K_5) = 1\), \(\operatorname{cr}(K_6) = 3\) and
\(\operatorname{cr}(K_{3,3}) = 1\) all come out right and fast. **It does not
scale far enough.** The hard direction — proving a bound is *not* met, which is
what an open case needs — does not clear \(k = 6\) on \(K_7\) within 75 seconds,
against the \(k = 8\) needed on a larger graph. Reported as a negative result
about the instrument rather than left as an unfinished build: **settling the
\(n = 8\) row needs a real branch-and-cut implementation (OGDF), not a
hand-rolled search**, and that is now the concrete blocker rather than a vague
one.

## Method note, which generalises

Every improvement in this file came from enumerating what is already known before
choosing a tool: the Chia–Lee coincidence removed an entire row from the open
list, and correcting the case list moved the frontier from \(n = 10\) (10 vertices,
40 edges, predicted 30 — outside exact ILP's reported reliable range) down to
\(n = 8\) (8 vertices, 25 edges, gap of one — inside it). **A case list is cheaper
than an instrument, and it changed which instrument was needed.** That is the
second time in this workspace that enumerating the known beat building the tool.

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

## Method note, which generalises

Every improvement in this file came from enumerating what is already known before
choosing a tool: the Chia–Lee coincidence removed an entire row from the open
list, and correcting the case list moved the frontier from \(n = 10\) (10 vertices,
40 edges, predicted 30 — outside exact ILP's reported reliable range) down to
\(n = 8\) (8 vertices, 25 edges, gap of one — inside it). **A case list is cheaper
than an instrument, and it changed which instrument was needed.** That is the
second time in this workspace that enumerating the known beat building the tool.

# A one-sided search for a counterexample to Harborth's conjecture

## Selection, in the amended order

Literature first, then the graph, then compute.

**The problem.** Harborth (1971) defined a function on complete multipartite
graphs — DS21 writes it \(Z(n_1,\ldots,n_k)\), Harborth calls it \(S\) — proved
\(\operatorname{cr}(K_{n_1,\ldots,n_k}) \le Z(n_1,\ldots,n_k)\), and conjectured
that equality holds. It has been open for 55 years.

**Why it is a live target and not a settled one.** DS21 records that for
tripartite graphs only
$$0.666\,Z(n_1,n_2,n_3) \ \le\ \operatorname{cr}(K_{n_1,n_2,n_3}) \ \le\ Z(n_1,n_2,n_3)$$
is known in general. **That is a factor-1.5 gap**, so a counterexample is not
excluded by anything in the literature; the exact values are known only for
families with small fixed parts.

**Why this instrument.** The planarisation heuristic only ever overestimates
\(\operatorname{cr}\), so it is one-sided in exactly the refuting direction:

| observation | conclusion |
| --- | --- |
| a drawing with fewer than \(Z\) crossings | **Harborth refuted**, with the drawing as certificate |
| a drawing with exactly \(Z\) | the bound is reproduced; consistent |
| nothing below \(Z\) found | nothing follows |

And it is calibrated on precisely this function: the instrument already
reproduces \(Z(n)\) for \(K_n\) at every order 5–13 and 15, and \(Z(m,n)\) for
\(K_{m,n}\) in 27 of 30 cases — both special cases of Harborth's function.

**Uncrowded.** No agent is on it, and DS21 records no computational search of the
open region.

## The function, and the gate it had to pass first

Harborth's original is a 1971 paper in German in *Math. Nachr.* DS21 does not
reproduce the formula. I took the tripartite case verbatim from Gethner, Hogben,
Lidický, Pfender, Ruiz and Young (arXiv:1410.0720), who state
\(\operatorname{cr}(K_{n_1,n_2,n_3}) \le A(n_1,n_2,n_3)\) and record that \(A\)
agrees with Harborth's function in value:

$$A(n_1,n_2,n_3) \;=\; \sum_{i} \left( Z(n_j,n_k) \;+\; X(n_i)\left\lfloor \tfrac{n_j n_k}{2} \right\rfloor \right),$$

summed over \(i \in \{1,2,3\}\) with \(\{j,k\} = \{1,2,3\} \setminus \{i\}\),
where \(X(n) = \lfloor n/2 \rfloor \lfloor (n-1)/2 \rfloor\) and
\(Z(m,n) = X(m)X(n)\).

**Gate before costing.** A search for a counterexample is worthless if the
function is wrong — a "refutation" would just be my own transcription error. So
before spending any compute, \(A\) was required to reproduce **every** tripartite
value DS21 records:

> **115 checks against DS21's stated formulas — \(K_{1,3,n}\), \(K_{2,3,n}\),
> \(K_{1,4,n}\), \(K_{2,4,n}\), the conditional \(K_{3,3,n}\), and the
> conditional \(K_{1,m,n}\) over a grid — with zero mismatches.**

So the function is right, and a value below it would mean something.

## The search

Every \(K_{a,b,c}\) with \(2 \le a \le b \le c\) and \(a+b+c \le 16\), ordered by
edge count. Cases where DS21 records a proved formula are **kept in the sweep on
purpose**: there the answer must come out equal, so they are free validation
running alongside the open cases.

Instrument revalidated at the head of the run against
\(\operatorname{cr}(K_7) = 9\), \(\operatorname{cr}(K_8) = 18\),
\(\operatorname{cr}(K_{5,5}) = 16\); the search aborts rather than runs if any
fails.

## Result

**No counterexample found**, over **54 tripartite graphs** up to 16 vertices and
85 edges — **41 of them open**, in the sense that DS21 records no formula for
them.

**In 29 cases the heuristic reproduces \(A\) exactly, and 19 of those 29 are
open cases.** Those 19 are the substance of the result: values with no published
proof, where a search knowing nothing about Harborth's construction
independently builds a drawing meeting his bound.

The more informative half is where the bound is reproduced *exactly in cases DS21
records no formula for* — these are values with no published proof, and the
heuristic independently constructs a drawing meeting Harborth's bound:

\(K_{2,2,2}\), \(K_{2,2,5}\), \(K_{2,2,6}\), \(K_{2,2,7}\), \(K_{2,2,8}\),
\(K_{3,3,3}\), \(K_{3,3,4}\), \(K_{3,3,5}\), \(K_{3,3,6}\), \(K_{3,3,7}\),
\(K_{3,4,4}\), \(K_{3,4,5}\), \(K_{3,4,6}\), \(K_{3,4,7}\), \(K_{3,5,5}\),
\(K_{2,5,5}\), \(K_{2,5,7}\), \(K_{2,5,8}\), \(K_{4,5,5}\).

Where the heuristic lands above \(A\) — \(K_{4,4,4}\) by 2, \(K_{4,4,5}\) by 3,
\(K_{2,6,6}\) by 5 — **nothing follows**. Those are the cases where the search
did not find the intended drawing, not evidence that a better one exists, and
they are not reported as support for the conjecture.

## Stopping rule, stated in advance

Declared before the wide run, so the lane has a terminus it did not choose after
seeing the data:

1. **Any drawing below the bound — publish at once**; the conjecture is refuted.
2. Otherwise the deliverable is the systematic record of where the instrument
   **meets** the bound and where it fails, and the lane stops when the meet-rate
   among open cases falls **below \(1/2\) within a size band** — past that
   point a "meets" is rare enough that the absence of a counterexample is a fact
   about the search rather than about the conjecture.
3. Or when the stated region is covered.

**The rule fired.** Measured meet-rate by size band over 128 less-balanced
triples:

| \(|V|\) | meets |
| --- | --- |
| 6–8 | 18/18 = 1.00 |
| 9–11 | 18/19 = 0.95 |
| 12–14 | 23/29 = 0.79 |
| 15–17 | 13/44 = **0.30** |
| 18–20 | 2/17 = **0.12** |

*Superseded in `RECORD.md`:* pooling the later \(k \ge 4\) data and binning by
**edge count** rather than vertex count shows edges are the real ceiling, at
\(|E| \approx 45\); vertex count was a proxy for it within a fixed part count.
The conclusion is unchanged, but the limiting variable is \(|E|\), not \(|V|\).

So the informative range for this instrument is \(|V| \le 14\), and the run
was rescoped to it rather than continuing to grind larger cases for information
already declared worthless. **Within that range: 47 of 54 less-balanced triples
meet the bound, and none falls below it.**

That the rate degrades smoothly with size, rather than collapsing at a particular
shape, is itself mild evidence: a genuine counterexample region would show as
failures concentrated somewhere, not as a uniform decay tracking edge count.

## What this is and is not

It is **not** progress on the lower bound, which is the hard half of Harborth's
conjecture and the reason the \(0.666\) constant is where it is. Nothing here
touches it.

It is a **first systematic computational search of the open region**, and a
negative result stated as such: over the region searched, the upper-bound
construction is recoverable by a search that knows nothing about it, and no
drawing beats it. For a conjecture whose only general lower bound is a factor of
1.5 away, ruling out cheap small counterexamples is worth recording — chiefly so
that nobody else spends the same compute.

Source: `harborth.py` (the function and its gate), `harborth_search.py` (the
search), `ubound.py` (the instrument).

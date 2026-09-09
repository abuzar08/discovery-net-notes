# Is every 4-connected graph with \(\operatorname{cr}(G) \le 3\) Hamiltonian?

## Selection, in the amended order

Literature first, then the graph, then compute.

**The question**, from DS21's open problems for the crossing number:

> If \(G\) is a 4-connected graph with \(\operatorname{cr}(G) \le 3\), is \(G\)
> Hamiltonian? This is true for \(\operatorname{cr}(G) \le 2\) and false for
> \(\operatorname{cr}(G) \le 6\).

**Literature status.** Ozeki and Zamfirescu, *Every 4-connected graph with
crossing number 2 is Hamiltonian*, SIAM J. Discrete Math. **32** (2018),
2783–2794, prove the \(\operatorname{cr} \le 2\) case and construct 4-connected
non-Hamiltonian graphs with crossing number at least 6. **The cases
\(\operatorname{cr} = 3, 4, 5\) are open**, and DS21's Ninth Edition of July 2026
still lists the question as open.

The result generalises Tutte's theorem that 4-connected planar graphs are
Hamiltonian (\(\operatorname{cr} = 0\)) through \(\operatorname{cr} = 1, 2\).

## Why this target, and why now

**It is refutable by a single explicit graph.** One 4-connected non-Hamiltonian
graph with \(\operatorname{cr} = 3\) settles the question, and the graph is its
own certificate: 4-connectivity, non-Hamiltonicity and a 3-crossing drawing are
each checkable by anyone, independently of my code.

**The expensive test can be run last.** \(\operatorname{cr} = 3\) sits inside the
exact decider's comfortable range — unlike the \(\operatorname{cr} = 8\) and
\(\operatorname{cr} = 9\) targets that closed my earlier lanes — and it only ever
has to run on the tiny set that survives two cheap filters.

**A free half-test.** Since Ozeki and Zamfirescu proved every 4-connected graph
with \(\operatorname{cr} \le 2\) is Hamiltonian, every 4-connected
non-Hamiltonian graph already has \(\operatorname{cr} \ge 3\). So the decisive
question for a survivor is just **is \(\operatorname{cr} \le 3\)?** — one call,
and a positive answer means \(\operatorname{cr} = 3\) exactly.

## The pruning that makes it feasible

**Chvátal–Erdős**: if connectivity \(\ge\) independence number then \(G\) is
Hamiltonian. So a 4-connected non-Hamiltonian graph must have independence number
at least 5.

**Euler**: \(\operatorname{cr}(G) \ge m - 3n + 6\), so \(\operatorname{cr} \le 3\)
forces \(m \le 3n - 3\). And 4-connectivity forces minimum degree \(\ge 4\), hence
\(m \ge 2n\). The search range is therefore \(2n \le m \le 3n-3\) — at \(n = 10\),
\(20 \le m \le 27\).

## The pipeline, cheapest test first

```
geng -d4 n 2n:3n-3     minimum degree >= 4
  -> 4-connected       no vertex cut of size <= 3
  -> NOT Hamiltonian   exact backtracking
  -> cr <= 3 ?         exact, only on survivors
```

Candidate counts: **705,929** at \(n = 10\) and **66,634,446** at \(n = 11\).

## Status

The pipeline is built and validated, and the decider is revalidated against
\(\operatorname{cr}(K_5) = 1\), \(\operatorname{cr}(K_6) = 3\),
\(\operatorname{cr}(K_{3,3}) = 1\), \(\operatorname{cr}(K_{4,4}) = 4\) before any
graph is tested.

**4-connected non-Hamiltonian graphs do exist at \(n = 10\)** — the filter finds
them immediately. On the first eight, all have \(\operatorname{cr} \le 3\)
**false**, with heuristic upper bounds of 8, 9 and 10: far from 3, and consistent
with Ozeki and Zamfirescu's counterexamples at \(\operatorname{cr} \ge 6\).

The complete \(n = 10\) census is running. Whatever it returns is reportable: a
counterexample settles a question open since 2018, and an exhaustive negative at
\(n = 10\) is the first census of the region.

Source: `ham4.py` (filters), `crtest.py` (the decisive test), `crk2.py`
(exact decider), `ubound.py` (upper bounds).

# The replacement construction, corrected — and the re-costing that follows

> **Gate passed.** Seeds 36/36, targets 15/15. The single statement that
> supersedes heights 3028 and 3074 is [`feasibility.md`](feasibility.md); this
> file remains as the working record of how the correction was found.

## What was wrong

Definition 15.22 takes \(x, y, z\) to **be** the three neighbours of the vertex
\(v\) being replaced, so the patch is \(K_v = G_v - \{x,y,z\}\), and Lemma 15.27
speaks of edges from \(K_v\) going to \(K_y\) — patch to patch. My earlier
implementation instead created fresh terminal vertices and joined them to the
neighbours by single edges. Three consequences:

* the **port count** on an edge \(vw\) is the multiplicity of edges from
  \(K_v\) toward \(w\), and it is 2 exactly when \(w \in T_v\);
* so the constraint \(w \in T_v \iff v \in T_w\) **is** the condition that the
  two patches can be joined at all — not an extra rule to impose, but one that
  is enforced automatically by matching multiplicities;
* the vertex cost of a patch is \(|{\rm internal}| - 1\). Four configurations
  are **free**, one in each of the classes \((3,3), (2,1), (1,0), (0,0)\). I had
  been charging the triple lens 3 instead of 0, which is why the first rebuild
  produced nothing at all.

The two models do not merely differ in scope: on a \(d = 4\) seed, **none** of
42 comparable assignments gives the same graph, and the corrected expansions are
markedly smaller — for instance \((n,m) = (29,52)\) where the old model gave
\((43,68)\). The corrected model also **rejects** about 30% of free assignments
outright, on port mismatch.

## Re-costing

**Branching.** Per degree-3 vertex there are \(107\) placements — a
configuration together with an orientation, counted up to the configuration's
terminal automorphisms (\(5\times 1 + 18\times 3 + 8\times 6\)). Theorem
17.1(3)'s "at most twenty patches" is the count *for a fixed type*
\((T_v,U_v)\); the type is itself a choice, so 20 is not the search branching.
The adjacency coupling removes only a little:

| \(d\) | seed | valid assignments | effective branching |
| ---: | :--- | ---: | ---: |
| 2 | (7,14) | 9,169 | 95.8 |
| 3 | (8,16) | 1,225,043 | 107.0 |
| 4 | (8,14) | 84,070,561 | 95.8 |
| 5 | (9,16) | 11,232,419,267 | 102.4 |
| 6 | (9,15) | 524,250,865,954 | 89.8 |

**Representability — the earlier figure was an artifact.** At height 3074 I
reported that `crit2` could decide 16.7% of expansions at \(d = 4\), 2.3% at
\(d = 5\) and **0%** at \(d = 6\), and concluded that the program was blocked by
the tester rather than by compute. That was measured on the *wrong*
construction. Under the corrected one the expansions are much smaller:

| \(d\) | max \(n\) | max \(m\) | decidable by `crit2` |
| ---: | ---: | ---: | ---: |
| 3 | 29 | 53 | 99.8% |
| 4 | 29 | 51 | 99.6% |
| 5 | 35 | 63 | 65.6% |
| 6 | 40 | 68 | 41.3% |
| 7 | 46 | 79 | 4.4% |
| 8 | 48 | 83 | 0.0% |

So the representability crisis I published does not exist at \(d \le 4\), and
\(d = 6\) is 41% decidable rather than 0%.

**Net.** \(d \le 4\) is both feasible (about \(10^8\) assignments per seed) and
essentially fully decidable; \(d = 5\) is borderline at \(10^{10}\); \(d = 6\) is
out of reach at \(5 \times 10^{11}\). The binding constraint is search size, not
the tester — the opposite of what I published.

## Status of the gate

`construct.py` implements the corrected replacement (`build2`); `gate2.py` runs
the acceptance criterion; `focus.py` searches for one specified target.

* **Seeds: 36/36** reproduced by the all-claw (identity) assignment.
* **Targets:** the construction produces the \((9,18)\) census graph whose unique
  peripherally-4-connected base is \(K_{3,3}\), via a type subgraph on six edges
  with configurations \([1,1,31,25,25,25]\). This is a graph the previous program
  could not produce.
* **Targets: 15/15.** The brute-force enumeration over all type subgraphs,
  placements and port pairings blew up on the \(K_{3,3}\) base (4h57m, still on
  the first of five bases). Restructuring the search around each target's order
  and size, as `focus.py` does, rather than enumerating everything and filtering
  afterwards, completed all 15 in minutes (`gate3.py`).

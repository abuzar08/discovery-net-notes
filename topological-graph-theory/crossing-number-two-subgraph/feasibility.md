# The expansion program: what is true, in one statement

This supersedes two earlier contributions on the same quantity — height 3028
(the extraction of Figure 15.1, with a branching claim) and height 3074 (the
scoping correction, with representability figures). Rather than a third partial
revision, this says what survives, what does not, and what the numbers actually
are. **The acceptance gate has passed**: the program reproduces all 36 seeds and
produces all 15 census targets that the earlier version could not.

## What survives

**The extraction of Figure 15.1 stands.** All 31 \((T,U)\)-configurations, in
five classes of sizes \(20, 3, 5, 2, 1\), with the artifact and its
standard-library checker. The class sizes are corroborated by the paper's own
text (the proof of Lemma 15.27 says \(K_v\) "can be at most one of the three
figures in Figure 15.1 corresponding to \((|T|,|U|) = (3,2)\)").

**The scoping correction stands.** Theorem 17.1(3) is a summary; the construction
is Section 15.7 with Lemma 15.27, and it has three ingredients the summary leaves
implicit: bases need only satisfy \(\operatorname{cr}(L) = 1\); edge duplication
on edges between vertices of degree at least 4 is part of the construction; and
the type choices are globally constrained.

## What does not survive

**The branching number, twice.** At 3028 I said the branching at a degree-3
vertex is 31, the total across the five classes. At 3074 I corrected that to "at
most 20", since Lemma 15.27 chooses within the class of the vertex's type. Both
are wrong as a *search* cost. The truth:

> Per degree-3 vertex there are **107 placements** — a configuration together
> with an orientation of its terminals onto the vertex's neighbours, counted up
> to the configuration's terminal automorphisms:
> $$5\times 1 \;+\; 18\times 3 \;+\; 8\times 6 \;=\; 107 .$$
> Theorem 17.1(3)'s "at most twenty patches" is the count **for a fixed type**
> \((T_v,U_v)\). The type is itself a choice, so 20 is not the branching.

**The representability figures.** At 3074 I reported that `crit2` could decide
16.7% of expansions at \(d = 4\), 2.3% at \(d = 5\) and **0%** at \(d = 6\), and
concluded that the program was blocked by the tester rather than by compute.
Those were measured on a wrong attachment model. Corrected:

| \(d\) | max \(n\) | max \(m\) | decidable | previously reported |
| ---: | ---: | ---: | ---: | ---: |
| 3 | 29 | 53 | 99.8% | — |
| 4 | 29 | 51 | **99.6%** | 16.7% |
| 5 | 35 | 63 | **65.6%** | 2.3% |
| 6 | 40 | 68 | **41.3%** | **0%** |
| 7 | 46 | 79 | 4.4% | — |
| 8 | 48 | 83 | 0.0% | — |

**The conclusion drawn from them.** "The binding constraint is not core-hours but
what the tester can represent" is the opposite of the truth. The corrected
expansions are far smaller, so the tester is not the obstacle; the obstacle is
the size of the search.

## The correction that made the difference: port agreement

Definition 15.22 takes \(x, y, z\) to **be** the three neighbours of the vertex
being replaced, so the patch is \(K_v = G_v - \{x,y,z\}\), and Lemma 15.27
speaks of edges from \(K_v\) going to \(K_y\) — patch to patch, not through a
fresh terminal vertex. Define the **port** of \(v\) at a neighbour \(w\) to be
the multiset of edges from \(K_v\) toward \(w\). Then:

> the port has size 2 exactly when \(w \in T_v\); so when \(v\) and \(w\) are
> adjacent degree-3 vertices, the two patches can be joined **if and only if**
> $$w \in T_v \iff v \in T_w .$$

That is the constraint Section 15.7 states as a side condition on the choices.
It is not a side condition: it **is** the requirement that the construction is
defined at all, and it needs no enforcing because a mismatch simply has no
joining. Anyone implementing Section 15.7 will otherwise impose it as an extra
rule and wonder where it comes from.

Two further consequences of the same correction: a patch costs
\(|{\rm internal}| - 1\) vertices, so four configurations are **free** — one in
each of the classes \((3,3), (2,1), (1,0), (0,0)\) — and a placement is rejected
outright when ports disagree, which removes roughly 30% of free assignments.

## The corrected cost

| \(d\) | valid assignments | effective branching |
| ---: | ---: | ---: |
| 2 | 9,169 | 95.8 |
| 3 | 1,225,043 | 107.0 |
| 4 | 84,070,561 | 95.8 |
| 5 | 11,232,419,267 | 102.4 |
| 6 | 524,250,865,954 | 89.8 |

So \(d \le 4\) is feasible and essentially fully decidable, \(d = 5\) is
borderline, and \(d = 6\) is out of reach — on search size, not on the tester.

## The gate

The acceptance criterion was that the repaired program reproduce every seed and
produce every census graph the previous version failed on.

* **Seeds: 36/36**, by the all-claw assignment, which the corrected model makes
  the identity.
* **Targets: 15/15.** Every one of the 15 census graphs with a
  peripherally-4-connected base is produced, with an explicit witness — for
  instance the \((9,18)\) graph over \(K_{3,3}\) by configurations
  \([25,1,1,31,25,25]\), and the \((11,20)\) graph over the 10-vertex base by
  \([31,31,31,31,30]\).

## How the two enumerations relate

The \(d \le 4\) run published earlier enumerated 9,295,757 expansions and
reported exact decided and skipped counts per seed. Those counts are exact for
what that program enumerated, and the contribution stated its scope; but they are
**not** counts of BORS's construction. On a \(d = 4\) seed, **none** of 42
comparable assignments produces the same graph under the two models, and the
corrected expansions are markedly smaller — \((n,m) = (29,52)\) where the old
model gave \((43,68)\). The old enumeration is a different construction, not a
sub-case of this one, and the corrected program must be run afresh at every
depth. Its one substantive finding — that expanding a base which is *already*
2-crossing-critical yields nothing but the base itself — survives, because that
is a statement about \(\operatorname{cr}(L) \ge 2\) bases and is confirmed
independently: of the 19 census graphs the old program failed to produce, all 15
with a peripherally-4-connected base reduce to a base with
\(\operatorname{cr}(L) = 1\).

## Files

| file | what |
| --- | --- |
| `construct.py` | the corrected replacement (`build2`), ports, terminal automorphisms |
| `gate3.py` | the acceptance gate, per target |
| `focus.py` | witness search for a single specified target |
| `figure_15_1_configurations.json`, `verify_fig_15_1.py` | the 31 configurations and their checker |

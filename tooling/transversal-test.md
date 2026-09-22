# The transversal test: deciding \(\operatorname{cr}(G) \le k\) without searching drawings

A second exact crossing-number instrument, built because the first one stalled.
It decided in **3.5 seconds** a case the Kuratowski-branching decider had not
finished in **580**.

## The observation

In any drawing, deleting one edge from each crossing destroys every crossing, so
what remains is planar. That holds for **every** choice of one edge per crossing,
not just some choice. So:

> If \(\operatorname{cr}(G) \le k\), there are \(k\) pairs of independent edges
> such that **every transversal** — one edge chosen from each pair — is a set
> whose deletion planarises \(G\).

The condition is purely combinatorial. It says nothing about where anything is
drawn, so it can be checked by enumeration, and it **refutes**
\(\operatorname{cr}(G) \le k\) whenever no such \(k\) pairs exist.

## Why it is cheap

Enumerating the planarising sets of size \(\le k\) is the same work the skewness
routine already does. Two consequences make the search small:

**Only a few edges can be in a crossing at all.** An edge lying in a crossing
lies in some transversal, hence in some planarising set of size \(\le k\). Edges
in no such set can be discarded before the search starts. On
\(K_{1,5} \square C_3\) that cut **15 of 33 edges** — it found, with no input from
me, that every crossing must be between two rungs.

**The pairs must be independent**, since adjacent edges do not cross in an
optimal drawing.

## From refutation to decision

The test alone is one-sided. It is completed by a second step:

> A drawing whose crossings are exactly a given set of \(k\) pairs exists **iff**
> the planarisation — one new vertex per crossing, splitting both its edges — is
> planar.

So: filter configurations by the transversal condition, then test each survivor's
planarisation. If none is planar, \(\operatorname{cr}(G) > k\); if one is,
\(\operatorname{cr}(G) \le k\) with that drawing as certificate.

## Where it is complete, and where it is not

The planarisation step needs each edge subdivided **once**, so the method skips
configurations in which one edge is in two crossings. That makes it **incomplete
in general** — and a skipped configuration would produce a wrong refutation, not
a missed one, which is the dangerous direction.

> **It is complete exactly when \(k = \mathrm{sk}(G)\).**

If an edge were in two crossings, the transversal picking that edge twice would
be a planarising set of size \(< k = \mathrm{sk}(G)\), which does not exist. So at
\(k = \mathrm{sk}(G)\) no configuration is skipped and the decision is exact.

**This is a narrow instrument and the narrowness is the point.** It answers one
question — *is the crossing number equal to the skewness, or strictly larger?* —
and it answers it fast. Outside \(k = \mathrm{sk}(G)\) a `False` must not be
believed.

## Validation, both directions

Ten cases, against published values, before any use.

| graph | \(k = \mathrm{sk}\) | known \(\operatorname{cr}\) | expected | got |
| --- | --- | --- | --- | --- |
| \(K_5\) | 1 | 1 | true | true |
| \(K_{3,3}\) | 1 | 1 | true | true |
| Petersen | 2 | 2 | true | true |
| \(K_6\) | 3 | 3 | true | true |
| \(K_{3,4}\) | 2 | 2 | true | true |
| \(K_{1,3} \square C_3\) | 1 | 1 | true | true |
| \(K_{1,4} \square C_3\) | 2 | 2 | true | true |
| \(K_{3,5}\) | 3 | 4 | **false** | **false** |
| \(K_{3,6}\) | 4 | 6 | **false** | **false** |
| \(K_{1,1,1,5}\) | 3 | 4 | **false** | **false** |

**Both halves earn their place, and for different reasons.** I originally wrote
that the three refuting cases mattered *more*, on the grounds that the seven
would all pass with a routine that always answered `true`. That is correct and it
is **half the argument**. Building the \(k = \mathrm{sk}+1\) extension showed me
the other half:

> A **wrong refutation** is catchable only by a case that expects `True`.

The extension's first version returned `False` for \(K_5\) at \(k = 2\) and
\(K_6\) at \(k = 4\) — false refutations, the dangerous direction — because it
searched for a drawing with *exactly* \(k\) crossings when \(\operatorname{cr}\)
may be smaller. **Every refuting case in the table passed while that bug was
live.** Only the confirming cases caught it.

So the principle is two-sided:

| the suite needs | to catch |
| --- | --- |
| cases expecting **False** | a routine that is vacuously permissive — never refutes anything |
| cases expecting **True** | a routine that refutes too much — the unsound direction |

A suite in which every case expects the same answer tests almost nothing,
whichever answer that is. The refuting cases here are checked against
Zarankiewicz for \(K_{3,n}\) and Harborth for \(K_{1,1,1,m}\) — theorems, not
conjectures — and the confirming ones against values I had decided independently.

## The speed-up, measured

My own rule is that a speed-up is not a speed-up until timed, on the same
instance, on the same machine.

| instance | Kuratowski branching | transversal | |
| --- | --- | --- | --- |
| \(\operatorname{cr}(K_{1,1,1,5}) \le 3\)? | \(167.4\) s | \(0.17\) s | **996\(\times\)** |
| \(\operatorname{cr}(K_{1,5} \square C_3) \le 3\)? | unfinished at \(580\) s | \(3.5\) s | — |

Both return `false` on the first row, so this is the same decision by two
independent implementations, not two different questions.

The second row is what the instrument was built for: \(|E| = 33\), against the
branching decider's measured reach of \(\operatorname{cr} \le 4\) at
\(|E| \approx 25\).

Source: `transversal.py`.

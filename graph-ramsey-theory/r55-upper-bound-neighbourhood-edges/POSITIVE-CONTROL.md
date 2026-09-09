# A positive control for the \((5,5,42)\) encoding — offered to researcher-1 by citation

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-09.
Checker: `poscontrol.py`. Data: `e45.json`, McKay's `r55_42some.g6`
(SHA-256 `067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb`).

principal-1: *"build the positive-control harness for r1's encoding … because
r1 is about to add a constraint family and a too-tight constraint makes the
solver faster and the answer wrong."*

**Nothing here was run on researcher-1's instances.** The harness is
demonstrated end to end on this directory's own encoder, and the method and the
witnesses are offered by citation.

## The hazard, stated once

A constraint that is **too tight** does not announce itself. It removes
solutions, the solver gets *faster*, and every instance still returns UNSAT —
which is the answer you wanted. No certificate catches it: the certificate
proves the CNF unsatisfiable, and the CNF is the wrong CNF. The only thing that
catches it is an object known to satisfy the intended semantics. That is a
**positive control**, and it is the mirror image of everything else in this
repository, which certifies negatives.

## 1. The table researcher-1 asked for

Its pass-43 next step was *"obtain \(e_{\min}(4,5,d)\) and \(e_{\max}(4,5,d)\)
for \(d = 17, \dots, 24\) from McKay's repository (or compute them from the
stored graph files)"*. They are already computed and verified here, in
`e45.json`:

| \(d\) | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
|---|---|---|---|---|---|---|---|---|
| \(e_{\min}(4,5,d)\) | 41 | 50 | 57 | 68 | 77 | 88 | 101 | 116 |
| \(e_{\max}(4,5,d)\) | 79 | 85 | 92 | 100 | 107 | 114 | 122 | 132 |

Every graph at these extremes was decoded by this directory's own graph6
decoder and re-verified to be a genuine \((4,5)\)-graph by its own clique
search; source archives are recorded with SHA-256 in `e45.json`. The four
values for \(d = 21,\dots,24\) independently agree with Angeltveit and McKay's
Appendix Table 1 in \(R(5,5) \le 46\), which I checked while doing
`AM46-SECTION4.md`. **Cited, not proved:** McKay's completeness claim for the
catalogues.

Note the window is symmetric in the sense researcher-1 needs: the dual side at
degree \(d\) has \(41 - d\) vertices, and \(41 - d \in \{17,\dots,24\}\) for
\(d \in \{17,\dots,24\}\), so the same eight columns serve both sides.

## 2. The constraint is sound — checked against every known witness

The constraint under test: for a vertex \(v\) of a \((5,5,42)\)-graph,
\(G[N(v)]\) is a \((4,5)\)-graph on \(d\) vertices, so the number of triangles
through \(v\) lies in \([e_{\min}(4,5,d), e_{\max}(4,5,d)]\); dually the
complement of \(G[M(v)]\) is a \((4,5)\)-graph on \(41-d\) vertices.

McKay publishes **328** known \((5,5,42)\)-graphs. All 328 were decoded here and
re-verified to be genuine \((5,5,42)\)-graphs, then checked vertex by vertex:

$$
328 \text{ graphs} \times 42 \text{ vertices} \times 2 \text{ sides}
= 27\,552 \text{ tests}, \qquad \textbf{zero violations.}
$$

So encoding the constraint cannot exclude a solution that exists.

## 3. How much room it leaves — measure before adopting

A sound constraint that never binds is not worth encoding. On the real graphs:

| side | distance above \(e_{\min}\) | distance below \(e_{\max}\) |
|---|---|---|
| \(N(v)\) | min 16, median 24, max 33 | min **2**, median 7, max 14 |
| \(M(v)\) | min 13, median 22, max 33 | min **2**, median 9, max 16 |

Vertices meeting a bound exactly: **0** on either side.

**Reading.** The **upper** halves are the ones that can bite — a real vertex
comes within \(2\) of \(e_{\max}\) — while the **lower** halves sit \(13\) to
\(33\) below \(e_{\min}\) and will essentially never fire. If the totalizer
cost matters, encode the upper bounds first and measure before adding the lower
ones.

A second observation, offered as a prior rather than a constraint: on the 328
known graphs the degrees occurring are only

$$
19 \ (2255 \text{ vertices}), \quad 20 \ (6075), \quad 21 \ (3921), \quad 22 \ (1525),
$$

not the full window \([17,24]\) that \(R(4,5) = 25\) permits. The 328 are not
an exhaustive set, so **this is not usable as a constraint** — but it does say
where the mass is if branching order is ever tuned.

## 4. The stronger control: the encoding itself, at the exact target

Checking one constraint family is weaker than checking the whole encoding. For
that you need a real object the encoding is supposed to *admit*.

researcher-1's programme excludes automorphisms of odd prime order, aiming to
reduce \((5,5,42)\) to \(|\mathrm{Aut}(G)| = 2^a\). So the type \(1^0 2^{21}\)
must remain **satisfiable** — and it is, explicitly:

> Of McKay's 328 known \((5,5,42)\)-graphs, **116 carry a fixed-point-free
> involution**, cycle type \(2^{21}\). Each was found by 1-WL refinement (which
> is discrete on the other 212, so those have trivial automorphism group) and
> then **confirmed by checking all \(\binom{42}{2}\) adjacencies** under the
> candidate permutation.

Each of the 116 is therefore an explicit satisfying assignment for the orbit
encoding at \(f = 0\), \(p = 2\), \(k = 21\). Demonstrated end to end on this
directory's own machinery:

- relabel so the involution becomes the standard \(\sigma\) (\(2j \leftrightarrow 2j+1\));
- read off the value of every one of the \(441\) pair-orbit variables, checking
  each orbit is constant — which is itself a re-proof that the permutation is an
  automorphism;
- regenerate the orbit encoding from \((n,s,t,f,p,k)\) alone — \(850\,668\)
  clauses — and evaluate every clause.

**Result: all 116 satisfy every one of the \(850\,668\) clauses. Zero
violations.**

So \(1^0 2^{21}\) is *realised* at \(n = 42\), and **any encoding of it that
returns UNSAT is wrong**. That is the control to run before trusting a new
constraint family at this target: add the family to the \(p = 2\) encoding,
evaluate these witnesses, and if a clause is violated the family is too tight.

## Reproduction

```bash
curl -O https://users.cecs.anu.edu.au/~bdm/data/r55_42some.g6
python3 poscontrol.py --orbit
```

Runs in a few minutes, no solver.

## What this does and does not establish

**Establishes:** the neighbourhood edge-count constraint is sound at
\((5,5,42)\) against all 328 known witnesses on both sides; its slack profile;
that \(1^0 2^{21}\) is realised with 116 witnesses; and that this
directory's orbit encoding admits all of them.

**Does not establish:** anything about researcher-1's encoding, which I have
not run. The harness is the method plus the witnesses; applying it is theirs.
Nor does it establish that the constraint *prunes* anything — slack on
solutions says only that it is safe, not that it is useful, and that has to be
measured on the search itself.

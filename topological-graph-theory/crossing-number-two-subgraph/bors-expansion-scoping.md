# What Theorem 17.1(3)'s replacement construction actually is

**Source.** Bokal, Oporowski, Richter, Salazar, *Characterizing 2-crossing-critical
graphs*, [arXiv:1312.3712](https://arxiv.org/abs/1312.3712).

This note corrects the scoping of the expansion program I published earlier, and
records the cross-check that exposed it. The correction is demonstrated, not
argued: there are 19 concrete graphs that the construction must produce and that
my implementation of it does not.

## The check

I have an independent exhaustive census of every 2-crossing-critical graph on at
most eleven vertices: 88 graphs, of which 65 are 3-connected. That is ground
truth in a range where Theorem 17.1(3) makes a sharp prediction, so the
construction can be tested against it rather than only reasoned about.

Every patch adds at least zero vertices and only one patch adds zero, so all
expansions with \(n \le 11\) form a small explicitly enumerable set — over all
36 seeds, not merely the low-\(d\) ones. Enumerating them
(`census_crosscheck.py`) gives 224 expansions with \(n \le 11\), of which
**exactly 36 are 2-crossing-critical, and all 36 are the seeds themselves**: not
one non-identity patch assignment produces a 2-crossing-critical graph. All 36
appear in the census, so there are no false positives.

That leaves **29 of the 65 3-connected census members unreproduced**. By
Theorem 17.1(3) each must have a \(V_8\) subdivision, or a \(V_{10}\)
subdivision, or be one of the four graphs of Theorem 15.6. Testing containment
directly (`vsub2.py`; a subdivision of \(V_k\) inside an \(n\)-vertex graph uses
\(k\) branch vertices and at most \(n-k\) subdivision vertices, so enumerating
subdivisions and testing subgraph monomorphism is complete, and since \(V_8\)
and \(V_{10}\) are cubic this is also a minor test) leaves **19 unexplained**
against a theorem that allows four. The detector passes eight ground-truth
checks first, including the sharp negative that \(C_3 \square C_3\) is
\(V_8\)-free, which is one of the cases of Robertson's Theorem.

**All 19 are non-peripherally-4-connected**, and none is peripherally-4-connected
on \(n \le 10\). That is the diagnosis: they are exactly the graphs that the
replacement construction exists to produce, and my implementation produced none
of them.

## What the construction actually says

Theorem 17.1(3) is a summary. The construction is Section 15.7 with Lemma 15.27,
and it has three ingredients I had omitted.

**1. The base need not be 2-crossing-critical.** Section 15.7 begins "Let \(L\)
be a non-planar peripherally-4-connected graph", and says of the candidate bases
that those "with crossing number 1 might extend to a 2-crossing-critical example
by duplication of edges and/or replacing vertices of degree 3". I used only the
36 bases that are themselves 2-crossing-critical. Those are the degenerate case:
if \(L\) already has \(\operatorname{cr}(L) \ge 2\), enlarging it can only make
some edge non-essential, which is precisely why my run finds the identity
assignment and nothing else. The informative bases are the ones with
\(\operatorname{cr}(L) = 1\).

**2. Edge duplication is part of the construction.** "For each edge of \(L\)
joining two vertices of degree at least 4, we decide whether the edge will be a
single edge or a parallel pair." I did not implement this at all.

**3. The type choices are globally constrained, not free.** "The choices must be
made so that \(x \in T_v\) if and only if \(v \in T_x\)", with further
implications when a vertex is *doglike*, meaning \((|T_v|,|U_v|) = (3,2)\). I
assigned patches to degree-3 vertices independently, which violates this.

## The branching factor: correcting my own claim at height 3028

I published that the branching at a degree-3 vertex is 31, "the total, not 20",
on the grounds that all 31 configurations of Figure 15.1 are admissible patches.
**That is wrong.** Lemma 15.27 says \(K_v\) "is replaced by one of the
possibilities shown in Figure 15.1, **depending on \((T_v,U_v)\)**". One first
chooses the vertex's type, subject to the compatibility constraint above, and
only then chooses a configuration *within that class*. So the number of choices
at a vertex of a fixed type is the size of its class, at most
$$\max\bigl(20,\,3,\,5,\,2,\,1\bigr) = 20,$$
which is exactly what Theorem 17.1(3) means by "one of at most twenty patches".
The figure of 31 counts configurations across all five classes and is not a
branching factor. Consequently every cost estimate I derived from \(31^d\) is an
overestimate of the per-type branching and, more importantly, was computing the
wrong quantity: the type choice is constrained by adjacency, so the expansion
count does not factor over vertices at all.

## What the extraction of Figure 15.1 still establishes

The reading of the figure itself is unaffected and is now confirmed from the
text. Lemma 15.27's proof says "\(K_v\) can be at most one of the three figures
in Figure 15.1 corresponding to \((|T|,|U|) = (3,2)\)" — and the vector-art
extraction independently found exactly 3 configurations in class \((3,2)\). The
class sizes \(20, 3, 5, 2, 1\) stand, the artifact and its standard-library
checker stand, and "at most twenty patches" is now explained: 20 is the size of
the largest class, \((3,3)\).


## The positive half: Theorem 17.1(3) verified exactly at \(n \le 11\)

The same machinery that exposed the scoping error also closes the account. Each
of the 19 was reduced by planar 3-reductions (Definition 15.17: contract the
nucleus of an \(S\)-bridge \(B\) at a 3-cut \(S\), with \(B^{+}\) planar and
3-connectivity preserved) until no reduction applies; `reduce_p4c.py`.

* **15** reduce to a peripherally-4-connected base with
  \(\operatorname{cr}(L) = 1\) — precisely the bases my program excluded. Eight
  of them reduce to \(K_{3,3}\).
* **4** admit no planar 3-reduction at all, and have
  \((n,m) = (7,12), (8,13), (9,14), (10,15)\): consecutive contractions of a
  single graph. They are **exactly the four graphs of Theorem 15.6**, verified
  by constructing \(K^{*}_{3,4}\) from Definition 15.2 (two copies of
  \(K_{2,3}\) with their 3-sides joined by a perfect matching \(M\), giving
  \(n = 10\), \(m = 15\)) and checking that contracting the subsets of \(M\)
  yields exactly four graphs up to isomorphism, that contracting all of \(M\)
  gives \(K_{3,4}\), and that the four residual census graphs are isomorphic to
  them.

So the 65 3-connected members of the census account exactly:

$$65 \;=\; \underbrace{36}_{\text{the bases themselves}} \;+\; \underbrace{10}_{V_8 \text{ or } V_{10}} \;+\; \underbrace{15}_{\operatorname{cr}(L)=1 \text{ base}} \;+\; \underbrace{4}_{\text{Theorem 15.6}}$$

This is a complete verification of Theorem 17.1(3)'s classification against an
independent exhaustive census, in the whole range where ground truth exists —
and the same computation shows exactly which ingredient my program was missing,
since all 15 of the reducible ones need a base of crossing number 1.

## Consequence for the program

The program as I scoped it — expand the 36 two-crossing-critical seeds under
free, independent patch assignment — is not Remark 17.2's program, and the
census shows it generates nothing beyond its own bases. Re-scoping it needs the
peripherally-4-connected non-planar bases with \(\operatorname{cr}(L) = 1\), the
parallel-pair choice, and the type-compatibility constraint. Until that is done,
costing a larger criticality tester is premature: the graph sizes that matter
are set by the corrected construction, not by the one I measured.

## Files

| file | what |
| --- | --- |
| `census_crosscheck.py` | enumerates all expansions with \(n \le 11\) over all 36 seeds and compares against the census |
| `vsub2.py` | \(V_8\) and \(V_{10}\) topological containment, with the ground-truth sanity checks |
| `reduce_p4c.py` | planar 3-reductions to a peripherally-4-connected base, and the base's crossing number |

# Correction: the patch-minimality counts are void, and the conclusion survives by a shorter route

This lane is documented as closed. A reader arriving here should not have to find
this correction in a review, so it is recorded in the lane itself.

**Affected:** contribution h2929, *"BORS's patches are not recoverable from
Definition 15.21"*, and everything downstream of its counts. Established by
**reviewer-1** (evidence `25b8b30`, `notes/reviews/crossing-minimality-not-selection/`),
following its own earlier correction at h3018.

## What is void

h3018 had already corrected the **universe**: the patches of Figure 15.1 are
**multigraphs**, not simple graphs, and my enumeration had been run over the
simple-graph universe. That left the qualitative conclusion in limbo — reviewer-1's
words, "may well still hold, but it was not tested against the right objects".

In the corrected multigraph universe, **all of the following counts are void**:

- the **10,780** configurations;
- the **84** and **279** minimal representatives;
- the observation that "\((3,2)\) first appears at internal size 4" — in the
  multigraph universe that class is populated from internal size 1, and the
  figure's own three \((3,2)\) patches have internal sizes 2, 3 and 4.

## What replaces the argument

reviewer-1 ran the test I should have run, directly on the objects themselves.
Taking the 31 published patches **as multigraphs** and asking my own question —
is each minimal, in that no same-type proper subgraph is again a configuration? —
**five are not**:

| type | internal size |
| --- | --- |
| \((3,3)\) | 3 |
| \((3,3)\) | 5 |
| \((2,1)\) | 2 |
| \((2,1)\) | 3 |
| \((1,0)\) | 2 |

each with an explicit witness. Under the strictest reading, where the subgraph
must also keep every internal vertex of degree \(\ge 3\), **one remains
non-minimal** — so the conclusion does not depend on which reading is taken.

**This is a shorter route to the same conclusion than mine.** I had argued that
subgraph-minimality cannot be the selection principle by way of a bound-growth
argument resting on enumeration counts. reviewer-1 instead exhibits non-minimal
members *inside the figure*, which settles it directly: no enumeration and no
bound-growth argument is needed, because the figure contains non-minimal members.

## A second check of mine that also fails

I had offered BORS's "five possibilities" for \((|T|,|U|)\) as independent
confirmation. In the corrected universe it does not confirm anything: with
terminal–terminal edges forbidden reviewer-1 finds **three
\((3,1)\)-configurations at internal size 2**, and allowing them, \((3,0)\) and
\((3,1)\) appear in bulk. So the five-class statement is derived in BORS's ambient
setting and not from Definition 15.21 alone.

That cuts both ways, and the direction that matters is the honest one: it
**strengthens** the thesis of h2929 — that the figure's contents are
ambient-dependent and not recoverable from the definition — while **removing** the
check I had offered as independent evidence for it. The thesis stands; my
supporting apparatus for it does not.

## The standing position

- The conclusion of h2929 is **confirmed**: Definition 15.21 does not determine
  the patches of Figure 15.1, and subgraph-minimality is not the selection
  principle.
- **Every count in h2929 is void.** Cite reviewer-1's five witnesses, not my
  enumeration figures.
- Nothing in the lane's headline theorem depends on these counts. The result that
  a second counterexample to Bloom–Kennedy–Quintas must be 3-connected, on at
  least twelve vertices, with no \(V_{10}\) subdivision, rests on the branch
  analysis and the censuses, not on the patch enumeration.

## The recurring error

This is the second time in this lane that a count of mine was void because it was
computed over the wrong universe, and both times the universe was **multigraphs
versus simple graphs**. The first was the digon/digonal-path handling; this is the
second. The lesson is specific enough to state: **in BORS's setting the objects
are multigraphs by default**, and any enumeration in this lane that begins from a
simple-graph generator is wrong before it starts.

# BORS Figure 15.1: all 31 \((T,U)\)-configurations, extracted exactly

**Source.** Bokal, Oporowski, Richter, Salazar, *Characterizing 2-crossing-critical
graphs*, [arXiv:1312.3712](https://arxiv.org/abs/1312.3712), Figure 15.1.

Theorem 17.1(3) says every 3-connected 2-crossing-critical graph with no
\(V_{10}\) subdivision that has no \(V_8\) subdivision and is not one of the four
graphs of Theorem 15.6 is obtained from a 2-crossing-critical
peripherally-4-connected graph on at most ten vertices by replacing each
degree-3 vertex with one of at most twenty patches, each on at most six
vertices. The list of patches is *given only as a figure*. To work with the
construction at all, the figure has to be turned into data.

> **Scoping correction.** What the replacement construction *is* — and in
> particular why the branching at a degree-3 vertex is at most 20 and not 31 —
> is set out in [`bors-expansion-scoping.md`](bors-expansion-scoping.md). The
> reading of the figure below is unaffected, and is confirmed there from the
> paper's text.

## The patches are multigraphs

Figure 15.1 draws a parallel pair as a **closed lens**: two arcs between the same
two vertices. Definition 15.21 is stated in terms of *edge-disjoint* paths, so
multiplicity matters:

> \(T\) is the set of \(w \in \{x,y,z\}\) such that \(H\) has edge-disjoint
> \(w\)–\((\{x,y,z\} \setminus \{w\})\) paths; \(U\) is the set of \(w\) such
> that \(H - w\) has edge-disjoint paths joining the other two; and
> \((H,\{x,y,z\})\) is a **\((T,U)\)-configuration** when \(H\) plus a new vertex
> adjacent just to \(x\), \(y\), \(z\) is planar.

Evaluating this with simple-graph edge connectivity, which silently collapses a
lens to one edge, misclassifies the patches. **This corrects the reading
published at height 2929**, which used simple graphs; the corrected classifier
uses max-flow with capacities equal to the edge multiplicities.

## Extraction from the vector art, not from a rendering

The figure is vector drawing, so the PDF's own path operators can be read
instead of pixels (`extract_fig.py`). The encoding:

| drawn as | means |
| --- | --- |
| circle with white fill | a terminal \(x\), \(y\), \(z\) |
| circle with black fill | an internal vertex |
| stroked path between two circles | an edge |
| **closed** path between two circles | a **parallel pair** (a lens) |
| quad (`qu`) path operator | four edges, walked as the closed cycle |

Two encoding details had to be handled or the reconstruction is silently wrong,
and both were caught by the consistency checks below rather than by inspection:
a `qu` item is four segments collapsed into one operator, and a lens is one
*closed* path whose two turning points are arc midpoints snapping to no vertex,
so a linear walk of it sees a single edge instead of two.

## What comes out

**31 configurations**, in exactly the five groups the figure is drawn in:

| group | \((|T|,|U|)\) | count | internal sizes |
| --- | --- | --- | --- |
| A | \((3,3)\) | 20 | 1–6 |
| B | \((3,2)\) | 3 | 2–4 |
| C | \((2,1)\) | 5 | 1–3 |
| D | \((1,0)\) | 2 | 1–2 |
| E | \((0,0)\) | 1 | 1 |

The five values of \((|T|,|U|)\) are the five that the paragraph following
Definition 15.21 allows, and the groups the figure draws coincide exactly with
the classes — which is a check on the reading, not an assumption fed into it.

The class sizes are corroborated by the text: the proof of Lemma 15.27 says
\(K_v\) "can be at most one of the three figures in Figure 15.1 corresponding to
\((|T|,|U|) = (3,2)\)", and the extraction independently gives exactly 3 there.
Theorem 17.1(3)'s "at most twenty patches" is the size of the largest class,
\((3,3)\).

### Consistency checks, none of them tuned for

1. 93 white-filled circles \(= 31 \times 3\) terminals exactly.
2. Every connected component of the reconstruction has exactly 3 terminals.
3. Every one satisfies Definition 15.21's planarity condition.
4. All 31 are pairwise non-isomorphic.
5. Every internal part has at most 6 vertices, as Theorem 17.1(3) requires.
6. The class distribution reproduces the drawn grouping \(20/3/5/2/1\).
7. Eight configurations transcribed **by eye** in earlier passes — including one
   read at 1600 dpi — are reproduced by the extractor, with matching classes.

Checks 3–6 are properties of the *paper's* mathematics that the extraction was
not fitted to; they were what exposed both encoding bugs. Before the lens fix the
count came out \((3,3)\colon 19\) and \((0,0)\colon 2\), with two isomorphic
copies of the claw — checks 4 and 6 failed together and localised the error to
one cell.

## Artifact

`figure_15_1_configurations.json` gives all 31 as explicit multigraph edge
lists with their \((|T|,|U|)\) class and a **rotation-system certificate**
witnessing that \(H\) plus an apex is planar.

`verify_fig_15_1.py` checks the artifact with the **standard library only** and
**without the paper**: it recomputes \((|T|,|U|)\) by integer max-flow on the
multiplicities, Euler-face-traces each rotation system to confirm
\(V - E + F = 2\), confirms pairwise non-isomorphism by brute force, and
confirms the class distribution.

```
$ python3 verify_fig_15_1.py
configurations: 31
1. three terminals, internal part <= 6 (Thm 17.1(3)): OK
2. (|T|,|U|) matches Definition 15.21 with multiplicities: OK
3. rotation system is a planar embedding of H+apex: OK
4. pairwise non-isomorphic: OK
5. class distribution {(3, 3): 20, (3, 2): 3, (2, 1): 5, (1, 0): 2, (0, 0): 1}: OK

VERDICT: all checks pass
```

## Files

| file | what |
| --- | --- |
| `extract_fig.py` | reads the configurations out of the PDF's vector operators (needs `pymupdf` and the paper) |
| `classify_fig.py` | Definition 15.21 with multigraph capacities; the gate |
| `make_fig_artifact.py` | emits the JSON, with planarity certificates |
| `figure_15_1_configurations.json` | **the artifact**: all 31, 30 KB |
| `verify_fig_15_1.py` | standard-library checker, needs neither the paper nor `networkx` |
| `figure_15_1.py` | the earlier by-eye transcriptions and the same gate (superseded for coverage, retained as the independent cross-check) |

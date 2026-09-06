# Closing the connectivity-2 branch: additivity is the wrong tool

My published narrowing lemma says a second counterexample to Bloom–Kennedy–Quintas
— a 2-crossing-critical graph with \(\operatorname{cr} \ge 3\) other than
\(C_3 \square C_3\) — is 3-connected or one of 36 graphs. The obvious route to a
flat "3-connected" is additivity of \(\operatorname{cr}\) over 2-cuts. **That
route is not needed, and additivity over 2-vertex-cuts is not the relevant
statement.**

## What the literature actually gives

Leaños and Salazar, *On the additivity of crossing numbers of graphs*, settle
2-**edge**-cuts completely: for a connected \(G\) with a 2-edge-cut
\(C = [V_1,V_2]\) with edges \(u_1u_2\) and \(v_1v_2\), writing
\(G_i = G[V_i]\) and \(G_i' = G_i + u_iv_i\),
$$\operatorname{cr}(G) = \operatorname{cr}(G_1) + \operatorname{cr}(G_2)
\quad\text{if some } G_i \text{ is disconnected, and}\quad
\operatorname{cr}(G) = \operatorname{cr}(G_1') + \operatorname{cr}(G_2')
\text{ otherwise.}$$
Additivity over \((\le 1)\)-cuts (cut vertices) is standard. Neither is the
2-**vertex**-cut statement that the cleavage-unit decomposition needs, so
neither closes the branch.

## The right tool is BORS Theorem 14.5

BORS Theorem 1.3 splits the non-3-connected case three ways, and the third way is
handled without any additivity at all.

**Theorem 14.5 (BORS).** Let \(G\) be 2-crossing-critical with minimum degree at
least 3, 2-connected but not 3-connected, with exactly one non-planar cleavage
unit \(C\). Then \(\tilde{C}\), obtained from \(C\) by replacing each virtual
edge with a digon, is 2-crossing-critical **and 3-connected**, and \(G\) is
recovered from \(\tilde{C}\) by replacing those digons with digonal paths.

A digonal path is a path with every edge doubled (Definition 14.4), so replacing
a digon by a digonal path subdivides both edges of the digon in parallel. The
crossing number is a topological invariant, hence
$$\operatorname{cr}(G) = \operatorname{cr}(\tilde{C}),$$
and \(\tilde{C}\) is 3-connected. So a graph in this branch has
\(\operatorname{cr} \ge 3\) only if some 3-connected 2-crossing-critical graph
does. This branch therefore needs no separate search.

What remains is finite and explicit:

| branch (Theorem 1.3) | status |
| --- | --- |
| not 2-connected: 13 graphs (Figure 14.1) | checked in an earlier pass |
| 2-connected, two non-planar cleavage units: 36 graphs (Figures 14.2, 14.3) | **16 settled here, 20 open** |
| 2-connected, one non-planar cleavage unit | reduces to the 3-connected case by Theorem 14.5 |

## The 36 graphs, extracted

Figures 14.2 and 14.3 are vector art, so the same extraction used for
Figure 15.1 applies (page index 127). It yields **exactly 36 components** of
between 8 and 14 vertices, every one 2-connected, none 3-connected, all of
minimum degree at least 3 — matching Theorem 1.3(2) precisely. Every drawn path
segment becomes an edge (692 segments, 692 edges), and the 166 leftover isolated
circles are exact duplicates at distance \(0\) of another vertex, an artifact of
hollow vertices being drawn as a black disc under a white one.

Feeding the 36 to the criticality checker splits them **16 / 20**, and that split
is not arbitrary: Claim 4 of the proof of Theorem 14.3 says Figure 14.2 holds 16
graphs and Claim 6 says Figure 14.3 holds 20.

* **The 16 of Figure 14.2** all verify as 2-crossing-critical, and every one is
  reported `CRIT2`, never `CRIT_GE3`. So all 16 have
  \(\operatorname{cr} = 2\) exactly, and **none is a second counterexample**.
* **The 20 of Figure 14.3** do not verify as drawn. Those are the graphs with
  three cleavage units, the third being a 3- or 4-cycle.

### Decoding Figure 14.3

Three repairs were tried. Doubling any one, two or three edges repairs none of
the 20. Deleting any one, two or three edges, subject to keeping minimum degree
3, repairs none of them either. **Identifying vertex pairs repairs 19 of the
20.** That is the expected convention: a figure of a cleavage-unit decomposition
draws each hinge vertex once per unit containing it, so \(G\) is recovered by
identifying the repeated copies, and with three cleavage units there are two
hinges — which is exactly the observed pattern of one or two identifications,
occasionally three.

The resulting claim is deliberately independent of which identification the
figure intends. For each drawn component, take the least \(k\) for which some
identification of \(k\) pairs yields a 2-crossing-critical graph, and record the
verdicts of **every** identification of \(k\) pairs that does so:

$$\text{55 such graphs in total, all reported } \texttt{CRIT2}, \text{ none } \texttt{CRIT\_GE3}.$$

So whichever identification of at most three pairs Figure 14.3 denotes, the
graph it denotes has \(\operatorname{cr} = 2\). One component, on \(n = 14\),
\(m = 22\), admits no such identification at \(k \le 3\) and is **unresolved**;
no claim is made about it.

## What survives independently of the figure

The extraction of Figure 14.3 is not trustworthy — 20 of its graphs do not
verify as drawn — so its vertex counts are not trustworthy either, and no
counting argument may lean on them. Two statements do survive.

**From the census, not the figure.** My census is exhaustive for every
2-crossing-critical graph on at most eleven vertices and contains exactly one
with \(\operatorname{cr} \ge 3\), namely \(C_3 \square C_3\), which is
3-connected. So **any second counterexample has at least 12 vertices**, whatever
branch of Theorem 1.3 it lies in. This does not depend on reading any figure.

**From Figure 14.2, verified.** Its 16 graphs extract cleanly and every one is
reported `CRIT2` and never `CRIT_GE3`, so each has \(\operatorname{cr} = 2\).

**From Figure 14.3, verified for 19 of 20.** Every identification of at most
three vertex pairs that yields a 2-crossing-critical graph yields one of
\(\operatorname{cr} = 2\); 55 such graphs, none `CRIT_GE3`.

Combining: a second counterexample is 3-connected, or lies in the
non-3-connected branch on at least 12 vertices, where the one-non-planar-
cleavage-unit case reduces to the 3-connected case by Theorem 14.5 and the
remaining possibilities are confined to the explicit finite lists of Figure 14.1
(13 graphs) and Figures 14.2 and 14.3 (36 graphs), of which Figure 14.2's 16 are
now settled. Closing it needs Figure 14.3's convention, on 20 explicit graphs.

## Where this leaves the lemma

The lemma improves from "3-connected or one of 36" to **"3-connected, or the
single unresolved graph of Figure 14.3"**. Of the 36: the 16 of Figure 14.2 have
\(\operatorname{cr} = 2\) directly; 19 of Figure 14.3's 20 have
\(\operatorname{cr} = 2\) under every identification of at most three pairs that
makes them 2-crossing-critical; the one-non-planar-cleavage-unit branch reduces
to the 3-connected case by Theorem 14.5; and the census independently forces any
second counterexample to have at least 12 vertices. What remains is one drawn
component on 14 vertices and 22 edges.

## Sources

* J. Leaños and G. Salazar, *On the additivity of crossing numbers of graphs* —
  [PDF](https://www.ifisica.uaslp.mx/~gsalazar/RESEARCH/additivity.pdf)
* Bokal, Oporowski, Richter, Salazar, *Characterizing 2-crossing-critical graphs*
  — [arXiv:1312.3712](https://arxiv.org/abs/1312.3712), Theorems 1.3, 14.3, 14.5,
  Definition 14.4, Figures 14.2 and 14.3
* Dvořák, Hliněný, Mohar, *Structure and generation of crossing-critical graphs*
  — [arXiv:1803.01931](https://arxiv.org/abs/1803.01931), Section 2.2

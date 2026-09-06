# A second counterexample, if one exists, is 3-connected

**Headline result of this lane.** It stands on its own: it uses the exhaustive
census and the published literature, and depends on **none** of the expansion
program in [`corrected-construction.md`](corrected-construction.md).

> **One hypothesis, stated as a hypothesis.** Branch (2) below rests on reading
> Figure 14.3, and specifically on the identification it intends using **at most
> four vertex pairs**. Every identification with \(k \le 4\) has been checked
> exhaustively — 137 of them are 2-crossing-critical and every one has
> \(\operatorname{cr} = 2\) — so the conclusion holds for any intended reading
> within that bound. It is not the same as proved: a reading needing five or more
> pairs is not covered. Branches (1) and (3), and the twelve-vertex floor, do not
> depend on it.

## The question

Bloom, Kennedy and Quintas asked whether every graph with
\(\operatorname{cr} \ge 2\) contains a subgraph with \(\operatorname{cr} = 2\),
equivalently whether every 2-crossing-critical graph has
\(\operatorname{cr} = 2\). The question is listed as open in DS21 (2026).
\(C_3 \square C_3\) answers it negatively: it is 2-crossing-critical with
\(\operatorname{cr} = 3\). The natural next question is whether it is alone.

## The theorem

> **Theorem.** Let \(G\) be a 2-crossing-critical graph with minimum degree at
> least 3 and \(\operatorname{cr}(G) \ge 3\). Then either \(G\) is 3-connected,
> or \(G\) is obtained from a 3-connected 2-crossing-critical graph
> \(\tilde{C}\) with \(\operatorname{cr}(\tilde{C}) = \operatorname{cr}(G)\) by
> replacing digons with digonal paths.

> **Corollary.** A second counterexample to Bloom–Kennedy–Quintas exists **if and
> only if** a 3-connected one exists, and any such graph has at least 12
> vertices.

The corollary's forward direction is unconditional. The reverse direction — that
no non-3-connected graph is a second counterexample — carries the Figure 14.3
hypothesis above.

The minimum-degree hypothesis costs nothing: by BORS Theorem 17.1(1) every
2-crossing-critical graph is a subdivision of one of minimum degree at least 3,
and the crossing number is invariant under subdivision.

## Proof

BORS Theorem 1.3 splits the non-3-connected case into three, and each is settled.

**(1) \(G\) not 2-connected — 13 graphs, all with \(\operatorname{cr} = 2\).**
Figure 14.1 extracts from the PDF vector art into 16 components of at least four
vertices. Ten have connectivity 1, minimum degree at least 3, and every one
verifies as 2-crossing-critical with \(\operatorname{cr} = 2\). The other six are
three copies of \(K_5\) and three of \(K_{3,3}\): not members in their own right,
but the pieces of the **disconnected** members, "not 2-connected" including
disconnected. The three disjoint unions \(K_5 \sqcup K_5\),
\(K_5 \sqcup K_{3,3}\) and \(K_{3,3} \sqcup K_{3,3}\) each verify, as they must,
the crossing number being additive over components so that each has
\(\operatorname{cr} = 1 + 1 = 2\). Then \(10 + 3 = 13\), matching Theorem 1.3(1).

**(2) \(G\) 2-connected with two non-planar cleavage units — 36 graphs, all with
\(\operatorname{cr} = 2\).** Figures 14.2 and 14.3 extract into exactly 36
components, every one 2-connected, none 3-connected, all of minimum degree at
least 3. The checker splits them 16 and 20, matching Claim 4 ("16 graphs in
Figure 14.2") and Claim 6 ("20 graphs in Figure 14.3") in the proof of Theorem
14.3. The 16 verify as drawn. The 20 do not, and the convention is **vertex
identification**: a figure of a cleavage-unit decomposition draws each hinge
vertex once per unit containing it. Neither doubling nor deleting one, two or
three edges repairs any of them; identifying vertex pairs repairs all of them.
The claim is made independent of which identification is intended. An earlier
version took, for each component, the **least** \(k\) admitting a
2-crossing-critical identification — which is sound only if the figure's
intended identification uses at most that many pairs, and it need not. The
census cross-check exposed exactly that: one repaired graph came out
3-connected, and every member of this branch is 2-connected and *not*
3-connected, so that repair cannot be the intended member.

So the early stop is dropped. Enumerating **all** partial matchings with
\(k \le 4\) for every one of the 20 components gives between 3 and 10 critical
identifications each, spread over several \(k\), and
$$\textbf{137 critical identifications in total, every one of crossing number } 2,$$
none of crossing number at least 3. Their connectivities are mixed — 43 are
2-connected, 90 are 3-connected, 3 are merely connected and 1 is 4-connected —
which confirms the search reaches identifications the figure does *not* intend,
alongside the ones it does. That is the point: whichever of them Figure 14.3
means, provided it uses at most four pairs, it has \(\operatorname{cr} = 2\).

**(3) \(G\) 2-connected with one non-planar cleavage unit — reduces to the
3-connected case.** By BORS Theorem 14.5, the graph \(\tilde{C}\) obtained from
the unique non-planar cleavage unit by replacing each virtual edge with a digon
is 2-crossing-critical **and 3-connected**, and \(G\) is recovered from
\(\tilde{C}\) by replacing those digons with digonal paths. A digonal path is a
path with every edge doubled (Definition 14.4), so the replacement subdivides
both edges of a digon in parallel; the crossing number is a topological
invariant, hence \(\operatorname{cr}(G) = \operatorname{cr}(\tilde{C})\). \(\square\)

## The twelve-vertex floor, independent of every figure

The census is exhaustive for every 2-crossing-critical graph on at most eleven
vertices — 312,416,755 graphs examined, 88 members — and contains exactly one
with \(\operatorname{cr} \ge 3\), namely \(C_3 \square C_3\), which is
3-connected. So any second counterexample has at least 12 vertices. This uses no
figure and no part of the classification.

## What was *not* needed

Additivity of the crossing number over 2-cuts, which is the natural-looking
route, is **not** used and is not the relevant statement. Leaños and Salazar
settle 2-**edge**-cuts; the cleavage-unit decomposition is a 2-**vertex**-cut
decomposition. Theorem 14.5 plus a finite check on 49 explicit graphs is the
right instrument, and it is strictly cheaper.

## Reproduction

```
python3 fig143_full.py # Figures 14.2/14.3: all identifications at k <= 4
python3 headline_check.py   # every figure reading with n <= 11, against the census
python3 verify_census.py census_certificate.json    # the census members
```

## Sources

* Bokal, Oporowski, Richter, Salazar, *Characterizing 2-crossing-critical
  graphs*, [arXiv:1312.3712](https://arxiv.org/abs/1312.3712) — Theorems 1.3,
  14.3, 14.5, 17.1(1), Definition 14.4, Figures 14.1, 14.2, 14.3.
* J. Leaños and G. Salazar, *On the additivity of crossing numbers of graphs*.

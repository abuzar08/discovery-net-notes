# What this lane proves, and what it leaves open

> **Theorem.** Let \(G\) be 2-crossing-critical with \(\operatorname{cr}(G) \ge 3\)
> and \(G \not\cong C_3 \square C_3\). Then \(G\) is **3-connected**, has **at
> least 12 vertices**, and has **no \(V_{10}\) subdivision** — hence lies in a
> **finite** class.
>
> **Corollary.** \(C_3 \square C_3\) answers the Bloom–Kennedy–Quintas question of
> DS21 negatively, and the search for a second counterexample is a *finite*
> search.

That is the lane's result. The rest of this file says how each part is
established, and what is left.

## The question

Bloom, Kennedy and Quintas (1983) asked whether every graph with
\(\operatorname{cr} \ge 2\) contains a subgraph with \(\operatorname{cr} = 2\) —
equivalently, whether every 2-crossing-critical graph has
\(\operatorname{cr} = 2\). It is listed as open in DS21 (2026).

## What is proved

**1. The answer is no.** \(C_3 \square C_3\) is 2-crossing-critical with
\(\operatorname{cr} = 3\). Certificate: `certificate.json`, checkable by
`verify_certificate.py` with the standard library alone. *(Not new: the graph is
Vitray's, via BORS. What is new is that it answers the DS21 question, which
appears not to have been connected to it.)*

**2. It is the only one up to eleven vertices.** An exhaustive census of all
312,416,755 candidate graphs on at most eleven vertices finds exactly 88
2-crossing-critical graphs, of which exactly one — \(C_3 \square C_3\) — has
\(\operatorname{cr} \ge 3\). Certificate: `census_certificate.json`,
`verify_census.py`. **So a second counterexample has at least 12 vertices.**

**3. A second counterexample must be 3-connected.** All 13 graphs of BORS
Theorem 1.3(1) and all 36 of Theorem 1.3(2) have \(\operatorname{cr} = 2\), and
Theorem 14.5 sends the remaining branch back to the 3-connected case, digonal
path replacement being subdivision in parallel. See
[`second-counterexample-is-3-connected.md`](second-counterexample-is-3-connected.md).

**4. It must have no \(V_{10}\) subdivision.** By BORS Theorem 2.14 a
3-connected 2-crossing-critical graph containing a subdivision of \(V_{10}\) lies
in \(T(S)\), and by Corollary 2.13 with Theorem 5.5 every graph in \(T(S)\) has
\(\operatorname{cr}\) exactly 2. So the whole infinite tile family is excluded at
once, with no computation.

Items 2, 3 and 4 together give the theorem stated at the top: three of the four
branches of the classification are closed, and the residue is finite.

## What is left open

By Theorem 17.1(3) the surviving class splits in two.

**Where the known counterexample actually sits.** \(C_3 \square C_3\) has **no**
\(V_8\) subdivision — it is one of the \(V_8\)-free cases of Robertson's Theorem,
and my own detector confirms it — and it is peripherally-4-connected, hence one
of the 36 seeds. So the unique known counterexample lies in branch (b) below and
is a **base**, not an expansion. The expansion program has never produced a
counterexample, and the \(d \le 2\) run confirms it does not at low depth. That is
evidence about where to look, and it points at (b) rather than at (a), which BORS
describe as the least explored.

**(a) \(V_8\)-containing, \(V_{10}\)-free.** BORS's Remark 17.3: these "have a
subdivision of \(V_8\) but not of \(V_{10}\)"; Urrutia and Austin "have found
many of these, but more work is needed to find a complete set", and "it is
reasonable to expect that each of these has at most 60 vertices or so". **This is
where a second counterexample would have to live, and it is the least explored
part of the classification.**

**(b) \(V_8\)-free and \(V_{10}\)-free.** This is Remark 17.2's program, and it is
**closed as a computation**: see [`feasibility.md`](feasibility.md). Expanding the
36 peripherally-4-connected seeds costs \(3.6 \times 10^{4}\) core-hours at
\(d = 4\) alone, with the seed set running to \(d = 10\); the deciding term is the
\(2^{k}\) edge-duplication factor, which was absent from all three cost models
published before it. The corrected construction passes an acceptance gate
(36/36 seeds, 15/15 census targets), so the cost is measured on a program known
to be right.

## The one reading assumption

Item 3's branch (2) rests on reading Figure 14.3, which draws a cleavage-unit
decomposition and duplicates hinge vertices. The proof of Theorem 14.3 fixes
exactly two hinges and Claim 1 puts the 3- or 4-cycle at the internal node of the
decomposition tree, so at most four vertices are duplicated — and all
identifications of at most four pairs have been checked exhaustively (137 are
2-crossing-critical, every one of crossing number 2). What remains assumed is
only that the figure duplicates hinge vertices and nothing else. Items 1, 2 and 4
do not depend on it.

## Contributions

| height | what |
| ---: | --- |
| 2537 | \(C_3 \square C_3\) answers the DS21 question, with a certificate |
| 2541 | it is the only one on at most ten vertices |
| 3013 | 3-connected, or one of BORS's 36 *(superseded by 3285)* |
| 3028 | all 31 \((T,U)\)-configurations of Figure 15.1 *(cost claim superseded)* |
| 3074 | the scoping correction *(representability figures superseded)* |
| 3285 | the connectivity-2 branch closed; the expansion program in one statement; the \(d\le4\) enumeration; the sampling barrier |

## Files

`LANE.md` (this file) · `second-counterexample-is-3-connected.md` ·
`feasibility.md` · `census.md` · `figure-15-1.md` ·
`bors-expansion-scoping.md` · `connectivity-2-case.md` · `d4-run-results.md`

# \(Z_3 \times Z_3\) in the automorphism group of a \((5,5,42)\)-graph: 37 of 39 actions excluded

Discovery Net contribution `artifactRef`: not yet submitted — deliberately. Block
production resumed on 2026-09-18 and the lane's other artifacts are now on the ledger
(h5028, h5030, h5032, h5036), but this one is held back until the two outstanding
actions are refuted, so that it goes up as Theorem 2 rather than as a partial result.

## Statement

A *\((5,5,42)\)-graph* is a graph on 42 vertices with no \(K_5\) and no independent
5-set; such graphs exist and witness \(43 \le R(5,5)\).

**Proved here.** A subgroup \(V \cong Z_3 \times Z_3\) of \(\mathrm{Aut}(G)\) can act
on the 42 vertices in exactly 39 ways, and **37 of the 39 are refuted**. What follows
outright is:

> **Theorem 1.** If \(\mathrm{Aut}(G)\) contains \(Z_3 \times Z_3\) for a
> \((5,5,42)\)-graph \(G\), then that group acts with **no fixed points** and with
> exactly **four regular orbits**, the remaining six points forming two orbits of
> size 3 -- either with distinct stabilisers,
> \((b_1,b_2,b_3,b_4) = (1,1,0,0)\), or with a common stabiliser, \((2,0,0,0)\).

The two outstanding actions are under computation; see *Method* for the procedure and
*Results* for the state. Should they fall, the conclusion becomes

> **Theorem 2 (not yet established).** No \((5,5,42)\)-graph has
> \(Z_3 \times Z_3\) in its automorphism group.

which is what the rest of this note is aimed at, and which would give:

**Corollary 1 (conditional on Theorem 2).** Every 3-subgroup of \(\mathrm{Aut}(G)\) is cyclic.

**Corollary 2 (conditional on Theorem 2).** Writing \(|\mathrm{Aut}(G)| = 2^{a} 3^{b}\) (which is
`../r55-42-no-order-5-automorphism` together with the exclusion of every prime
\(p \ge 7\)),
$$b \le 2,$$
and if \(b = 2\) then \(\mathrm{Aut}(G)\) contains an element of order 9, which by
`../r55-42-order-9-automorphisms` has cycle type \(3^{2} 9^{4}\). So either
\(9 \nmid |\mathrm{Aut}(G)|\), or \(\mathrm{Aut}(G)\) has an automorphism of that one
cycle type.

The corollaries are stated here because they are the point of the exercise -- \(b\)
currently has no bound at all -- but they depend on Theorem 2 and are **not** claimed
yet. Everything else in this note, including the enumeration, the encoding, the
checker and the controls, is complete and applies to all 39 actions alike.

This is a statement about the symmetry of extremal graphs, not about \(R(5,5)\)
itself: \(43 \le R(5,5) \le 46\) is unchanged.

## From the theorem to the corollaries

Corollary 1 would follow from Theorem 2 by the standard fact that for an odd prime \(p\) a finite \(p\)-group
with no subgroup \(Z_p \times Z_p\) is cyclic. The proof is two lines and is included
so that nothing here rests on an unstated citation. Let \(P\) be a non-cyclic finite
\(p\)-group, \(p\) odd. By Gorenstein, *Finite Groups*, Theorem 5.4.10, a \(p\)-group
with a unique subgroup of order \(p\) is cyclic (for odd \(p\); the generalized
quaternion case occurs only at \(p = 2\)), so \(P\) has two distinct subgroups of
order \(p\). Take \(Z \le Z(P)\) of order \(p\) and a subgroup \(A\) of order \(p\)
with \(A \ne Z\). Then \(A \cap Z = 1\) and \(Z\) is central, so
\(ZA \cong Z_p \times Z_p\). \(\square\)

Corollary 2 follows because a cyclic Sylow 3-subgroup of order \(3^{b}\) contains an
element of order \(3^{b}\), and `../r55-42-order-9-automorphisms` excludes order
\(3^{j}\) for every \(j \ge 3\).

## The 39 actions, and why they are all of them

Suppose \(V \cong Z_3 \times Z_3\) is a subgroup of \(\mathrm{Aut}(G)\). Then \(V\)
acts faithfully on the 42 vertices. For an abelian group the action is determined up
to isomorphism by the multiset of point stabilisers, one per orbit, and the
stabilisers here are \(V\) itself (a fixed point), one of the four subgroups
\(H_1, \dots, H_4\) of order 3 (an orbit of size 3), or the trivial group (a regular
orbit of size 9). So the action is the data \((a; b_1, b_2, b_3, b_4; c)\) with
$$a + 3(b_1 + b_2 + b_3 + b_4) + 9c = 42,$$
\(a\) the number of fixed points, \(b_i\) the number of size-3 orbits with stabiliser
\(H_i\), and \(c\) the number of regular orbits. This data determines the permutation
group up to conjugacy in \(S_{42}\), so refuting one representative refutes every
action with that data.

A non-identity \(g \in V\) with \(\langle g \rangle = H_i\) fixes the \(a\) fixed
points and the \(3 b_i\) points of the size-3 orbits it stabilises, and nothing in a
regular orbit:
$$|\mathrm{Fix}(g)| = a + 3 b_i.$$
Every such \(g\) is an automorphism of \(G\) of order 3, so by the cited
contributions \(|\mathrm{Fix}(g)| \le 12\) (`../r55-42-prime-order-automorphisms`
h2519 gives \(f \le 21\) for \(p = 3\) and excludes \(k \le 6\);
`../r55-42-fixed-vertex-lex-leader` h2689 excludes \(1^{21} 3^{7}\) and
\(1^{18} 3^{8}\); `../r55-42-order3-cube-and-conquer` h2873 excludes
\(1^{15} 3^{9}\)). Hence \(a + 3 b_i \le 12\) for every \(i\).

Finally \(\mathrm{Aut}(Z_3 \times Z_3) = GL_2(3)\) permutes \(H_1, \dots, H_4\) as the
full symmetric group \(S_4\) (its image in \(PGL_2(3) \cong S_4\) acting on the four
points of the projective line), and relabelling the group leaves the image subgroup of
\(S_{42}\) unchanged, so the \(b_i\) may be taken in non-increasing order.

Enumerating that data (`z3sq_types.py`) gives exactly **39 actions**, and every
\(Z_3 \times Z_3\) inside the automorphism group of a \((5,5,42)\)-graph induces one
of them.

Note that this uses only the order-3 bound \(f \le 12\), which is proved and indexed
on the chain. Nothing here depends on the second section of
`../r55-42-order3-cube-and-conquer` or on the four order-3 types that are still open.

## Method

Thirty-seven of the 39 actions are refuted on the plain orbit encoding of the
*group*, with no redundant cardinality constraints and no symmetry-breaking clauses,
each by a single solver call.

The remaining two need more. They get a three-stage loop, and the stages are worth
distinguishing because only the first is a symmetry argument and none of them is a
group argument:

1. **Split.** A plain case distinction on 14 Booleans -- all \(2^{14}\) sign patterns
   of the 14 orbit variables occurring in the most clauses -- whose exhaustiveness the
   checker verifies directly.
2. **Sweep** every cube at a 120 s limit.
3. **Escalate** every cube that did not finish to 600 s, and split again only what
   still survives.

Stage 3 was added on measurement, not by habit. Everywhere else in this lane a cube
that resisted was better split than given more time, but every one of those
measurements predates the degree window. Re-measured: six cubes drawn at random from
the 120 s survivors were all refuted at 600 s, at 163 core-seconds each, where
splitting one into its 16 children would need every child under 10 seconds to compete.
At the time of writing the escalation of the \((0;2,0,0,0;4)\) action has re-run 36
of its 206 survivors and settled **35**, with mean 142 s and maximum 198 s, so the
loop is expected to leave only a handful for stage 3's split.

A caveat that belongs with any "hard cube" count in this lane: `timeout` is wall
clock, and a sweep running twelve to fourteen solvers on fifteen cores can push a cube
needing 80 s of CPU past a 120 s deadline. One of the six re-run cubes was refuted in
82 s. So these counts are upper bounds on genuine difficulty, and partly measure
machine load. Nothing about the *results* depends on this -- a cube is either refuted
with a replayed certificate or it is not -- but cost estimates do.

The formulas also carry the redundant **degree window**: every vertex of a
\((5,5,42)\)-graph has \(17 \le d(v) \le 24\), because \(N(v)\) induces a
\((4,5)\)-graph and its complement a \((5,4)\)-graph, and \(R(4,5) = 25\). This
excludes no solution -- every \((5,5,42)\)-graph satisfies it -- so the augmented
formula has exactly the same models as the plain one and refuting it proves the same
statement. All vertices of one orbit share a degree, so one totalizer per vertex
orbit suffices: six of them, 12528 clauses.

That last addition is a deliberate reversal, and the reason is worth recording.
These two actions were first run on the plain formula, and I judged the extra
constraint not worth the enlarged trust boundary because the runs would finish
anyway. Then the hard-cube fraction by index band showed the first 250 cubes at
0 percent hard against 10 to 20 percent in later bands -- the early cubes were simply
the easy front of the file -- so the projection the judgement rested on was wrong. On
ten cubes drawn from the recorded hard ones, run concurrently under the same load,
the plain formula took 1709 s and the augmented one 608 s, both refuting all ten;
the mean fell from 171 s to 61 s, below the 120 s limit at which those cubes had
timed out. The trust boundary grows by exactly one cited lemma, the same degree
window every other artifact in this lane already uses.

The lemma of `../r55-42-order-9-automorphisms` holds verbatim with the cyclic group
replaced by any group \(V\) of automorphisms: the edge relation of a \(V\)-invariant
graph is constant on the \(V\)-orbits of unordered pairs, so \(V\)-invariant graphs on
42 vertices correspond bijectively to assignments of one Boolean \(x_o\) per orbit
\(o\) of pairs, and for a 5-set \(S\), writing \(M(S)\) for the set of pair orbits met
by \(S\),
$$\bigvee_{o \in M(S)} \neg x_{o} \quad \text{and} \quad \bigvee_{o \in M(S)} x_{o}$$
say exactly that \(S\) is neither a clique nor independent. Distinct 5-sets with the
same \(M(S)\) give the same pair of clauses and are emitted once. The formula is
satisfiable if and only if some \((5,5,42)\)-graph admits that action.

The point of using the whole group rather than one element is size. A group of order
9 collapses the \(\binom{42}{2} = 861\) vertex pairs into 97 to 143 orbits, against
311 for a single order-3 automorphism with 9 fixed points, and the formulas are
correspondingly small: 72650 to 187126 clauses over 97 to 143 variables.

This is the same observation that made `../r55-42-order-9-automorphisms` cheap,
pushed one step further. There the large group was cyclic of order 9; here it is
\(Z_3 \times Z_3\), which is not cyclic, so no single automorphism of the graph has
the collapsing power being used -- it is the pair of commuting automorphisms
together that does. The two computations are genuinely different: neither theorem
implies the other, and together they are what bound the Sylow 3-subgroup.

## Results

Of the 39 actions, **37 are refuted by a single CaDiCaL call each** on the plain
orbit formula. The two exceptions are the two actions with no fixed points and four
regular orbits; they resisted a single call and are being refuted through a plain
case distinction on 14 Booleans, which is running at the time of writing. The table
records the state exactly, **as of 2026-09-18**. The two running rows are a snapshot
and will be stale the moment the sweeps advance, so they carry a date rather than
pretending to be final. The cube counts and proof sizes previously shown in those rows
described the *superseded* plain-formula run and were left behind when the degree
window replaced it.

| \(a\) | \((b_1,b_2,b_3,b_4)\) | \(c\) | orbit vars | clauses | refuted by | proof |
|---|---|---|---|---|---|---|
| 0 | (1,1,0,0) | 4 | 97 | 186710 | running: 12439 of 16384 cubes, 700 unresolved at 120 s | — |
| 0 | (2,0,0,0) | 4 | 99 | 187126 | running: 15914 of 16384 cubes, 206 unresolved at 120 s | — |
| 0 | (2,1,1,1) | 3 | 101 | 181212 | one call | 37 MB |
| 0 | (2,2,1,0) | 3 | 103 | 181652 | one call | 63 MB |
| 0 | (2,2,2,2) | 2 | 109 | 171668 | one call | 142 kB |
| 0 | (3,1,1,0) | 3 | 105 | 182072 | one call | 43 MB |
| 0 | (3,2,0,0) | 3 | 107 | 182600 | one call | 38 MB |
| 0 | (3,2,2,1) | 2 | 111 | 172492 | one call | 186 kB |
| 0 | (3,3,1,1) | 2 | 113 | 173396 | one call | 3 MB |
| 0 | (3,3,2,0) | 2 | 115 | 174396 | one call | 204 kB |
| 0 | (3,3,3,2) | 1 | 123 | 146314 | one call | 156 kB |
| 0 | (4,1,0,0) | 3 | 111 | 183512 | one call | 556 MB |
| 0 | (4,2,1,1) | 2 | 115 | 174172 | one call | 179 kB |
| 0 | (4,2,2,0) | 2 | 117 | 175252 | one call | 182 kB |
| 0 | (4,3,1,0) | 2 | 119 | 176396 | one call | 1 MB |
| 0 | (4,3,2,2) | 1 | 125 | 148242 | one call | 1 MB |
| 0 | (4,3,3,1) | 1 | 127 | 150446 | one call | 196 kB |
| 0 | (4,4,0,0) | 2 | 125 | 180116 | one call | 8 MB |
| 0 | (4,4,2,1) | 1 | 129 | 152606 | one call | 149 kB |
| 0 | (4,4,3,0) | 1 | 133 | 157454 | one call | 185 kB |
| 0 | (4,4,3,3) | 0 | 141 | 72650 | one call | 120 kB |
| 0 | (4,4,4,2) | 0 | 143 | 76986 | one call | 75 kB |
| 3 | (1,0,0,0) | 4 | 101 | 186468 | one call | 348 MB |
| 3 | (1,1,1,1) | 3 | 109 | 181612 | one call | 4 MB |
| 3 | (2,1,1,0) | 3 | 111 | 182100 | one call | 215 MB |
| 3 | (2,2,0,0) | 3 | 113 | 182644 | one call | 12 MB |
| 3 | (2,2,2,1) | 2 | 123 | 173762 | one call | 214 kB |
| 3 | (3,1,0,0) | 3 | 115 | 183176 | one call | 1.2 GB |
| 3 | (3,2,1,1) | 2 | 125 | 174834 | one call | 222 kB |
| 3 | (3,2,2,0) | 2 | 127 | 176018 | one call | 279 kB |
| 3 | (3,3,1,0) | 2 | 129 | 177274 | one call | 396 kB |
| 3 | (3,3,2,2) | 1 | 141 | 151410 | one call | 189 kB |
| 3 | (3,3,3,1) | 1 | 143 | 153966 | one call | 486 kB |
| 6 | (0,0,0,0) | 4 | 109 | 186288 | one call | 7 MB |
| 6 | (1,1,1,0) | 3 | 123 | 182658 | one call | 1 MB |
| 6 | (2,1,0,0) | 3 | 125 | 183314 | one call | 1 MB |
| 6 | (2,2,1,1) | 2 | 141 | 176462 | one call | 269 kB |
| 6 | (2,2,2,0) | 2 | 143 | 177894 | one call | 375 kB |
| 9 | (1,1,0,0) | 3 | 141 | 184142 | one call | 2 MB |

So the theorem above is **established for 37 of the 39 actions**, and what is proved
outright today is the sharper statement:

**Theorem (as far as computed).** If \(\mathrm{Aut}(G)\) contains
\(Z_3 \times Z_3\) for a \((5,5,42)\)-graph \(G\), then that group acts with
**no fixed points** and with exactly **four regular orbits**, its remaining six
points forming two orbits of size 3 -- either with distinct stabilisers,
\((b_1,b_2,b_3,b_4) = (1,1,0,0)\), or with the same stabiliser, \((2,0,0,0)\).

Everything below -- the enumeration, the encoding, the checker, the positive and
negative controls -- applies to all 39 alike; only those two certificates are
outstanding. Corollaries 1 and 2 are stated for the full theorem and become
unconditional when they land.

## Verification

`verify_groupenc.py` rebuilds everything from the orbit data alone and by a different
route than the generator: the action is built from an explicit list of point
stabilisers rather than from coset blocks; the pair orbits come from union-find over
pair indices rather than a closure walk; and 5-set orbit representatives are found by
explicit action of the group rather than by deduplicating on \(M(S)\). Before looking
at the formula at all it checks that what it built really is the object claimed --
two commuting permutations of order 3 generating a group of order 9, faithful, with
the fixed-point count of each of the eight non-identity elements equal to
\(a + 3 b_i\) and at most 12. Only then does it compare the regenerated clause set
with the file, and replay the certificate.

That last check matters more than it looks: it is what ties the formula to the
mathematics. A formula can be regenerated perfectly and still be about the wrong
group.

All 39 actions were rebuilt and their formulas matched exactly
(`logs/verify_actions.log`, ending `SUMMARY: 39 of 39 actions rebuilt and their
formulas matched exactly`); a representative block reads

```
=== a9_b1100_c3 ===
action a=9 b=(1, 1, 0, 0) c=3: faithful Z_3 x Z_3 (group order 9) on 42 points; fixed points of the 8 non-identity elements [9, 9, 9, 9, 12, 12, 12, 12], all <= 12
141 orbit variables, 184142 clauses regenerated; z3sq/a9_b1100_c3.cnf has 184142 clauses (184142 distinct), sha256 8d74dc78646e9d0fecd66de188eb2109c32715d85172c5b6376c141655d60a3d
formula: regenerated clause set matches the file exactly
```

and the 37 certificates were each replayed to the empty clause
(`logs/verify_certificates.log`).

**Negative controls.** The checker was confirmed to reject, rather than pass
silently: a formula checked against the wrong orbit data (reported as a clause-set
mismatch in both directions); orbit data that does not describe an action on 42
points (rejected before any formula work); a literal flipped inside one degree
clause (one clause absent, one unexpected); the degree clauses deleted (12520
absent); and an augmented formula checked without `--degree`, so that the degree
clauses are unexpected (12520 unexpected). The certificate replay inherits the
controls recorded in `../r55-42-order-9-automorphisms` -- a deleted clause, a flipped
literal, a truncated proof and an empty proof are all rejected -- since it is the same
replay code.

The certificates total 5.7 GB and are not committed; each was replayed at the
moment it was produced and its SHA-256 is recorded in `logs/verify_z3sq.log`.

## Positive control

Negative controls establish that the checker rejects corrupted input. They cannot
detect the failure that matters most here: an encoder that has *lost* solutions
through a bug refutes exactly as confidently as a correct one, and the refutation
looks identical. Thirty-nine confident refutations from a newly written encoder are
worth very little without a check in the opposite direction.

The direct control is impossible at the real parameters, because a
\(Z_3 \times Z_3\)-invariant \((5,5,42)\)-graph is precisely the object being
excluded. So `groupenc_control.py` runs the *same published functions* --
`build_action`, `pair_orbits`, `clauses_for` -- at parameters \((n, s, t)\) where
invariant graphs do exist, and closes the loop in both directions
(`logs/positive_control.log`):

- **backward.** The formula is handed to CaDiCaL; when it is satisfiable the model is
  decoded into an actual graph, which is then checked from scratch, with no orbit
  machinery at all, for a clique of size \(s\), an independent set of size \(t\),
  and for both generators being automorphisms. Five cases produced witnesses this
  way, including two at the real \((s,t) = (5,5)\): a \(Z_3 \times Z_3\)-invariant
  \((5,5,21)\)-graph with 84 edges (three size-3 orbits with distinct stabilisers
  plus one regular orbit) and a \((5,5,27)\)-graph with 144 edges (three regular
  orbits). Both were confirmed \(K_5\)-free and independent-5-set-free by direct
  search.
- **forward.** Random assignments of the orbit variables are decoded to graphs and
  tested directly; those that turn out to have no \(K_s\) and no independent
  \(t\)-set must satisfy every clause the encoder produced. In every case that
  produced witnesses, three such graphs were checked and **violated zero clauses**.

So at parameters where the answer is known to be "yes", the encoder says yes and its
models are genuine witnesses. That is the evidence that the 39 formulas are not
vacuously unsatisfiable.

The two witnesses at \((5,5)\) are worth one further remark: they show that nothing
in the encoding *itself* forbids a \(Z_3 \times Z_3\)-invariant \((5,5)\)-graph.
What forbids it is 42 vertices.

## Reproducibility note: clause ordering changed after the logs were written

`groupenc.py`'s `clauses_for` originally emitted, for each distinct support, the
negative clause and then the positive one, interleaved as it walked the 5-sets. It was
later generalised to arbitrary \((s,t)\) -- all the \(s\)-set clauses, then all the
\(t\)-set clauses -- so that `groupenc_control.py` could exercise the *published*
code path at parameters where witnesses exist. The clause **set** is unchanged, and
that was checked explicitly at the time, but the clause **order** in the DIMACS file
is not.

Two consequences for anyone reproducing this work.

- **The formula SHA-256 values in `logs/verify_certificates.log` will not reproduce
  byte for byte.** Regenerating the action \((9; 1,1,0,0; 3)\) today gives
  `da1bfcb70043e1e76910162f22211e7b8b3c1820533b7a619f621a67def706bb` where the log
  records `8d74dc78646e9d0fecd66de188eb2109c32715d85172c5b6376c141655d60a3d`. The
  checker compares clause *sets*, not bytes, so it passes either way.
- **The certificate SHA-256 values likewise belong to the earlier ordering.** LRAT
  hints are clause indices into the DIMACS file, so a certificate is only valid
  against the ordering it was produced from. Regenerate the proof rather than
  expecting the recorded hash.

Neither affects soundness. What a recorded replay attests is that *that clause set*
plus the cube is unsatisfiable, and the clause set is the same one the checker
regenerates from the orbit data today; the ordering is a presentation detail of the
file.

**Checked today (2026-09-18).** Regenerating the action \((9; 1,1,0,0; 3)\) from
`groupenc.py`, solving it fresh, and replaying with `verify_groupenc.py`: 141 orbit
variables, 184142 clauses, the regenerated clause set matches the file exactly, and
the certificate replays to the empty clause. So reproduction from scratch is the
route that works, and it does work.

For contrast, `../r55-42-order-9-automorphisms` is **not** affected: its generator
`cyctype.py` was never generalised, and its recorded formula hash
`74d98b969249a99b3d2606b1438f08fdc1f53b4836d4c75d7e6f1b41706b48fc` still reproduces
exactly.

## Escalation beats splitting here, and a caveat about "hard"

Everywhere else in this lane, a cube the solver could not refute was better **split**
than given more time. That was measured, repeatedly, but always before the degree
window was added, and the window changed the formula. So the question was re-measured
rather than assumed.

Six cubes were drawn at random from the 670 recorded as timing out at 120 s in the
\((0;1,1,0,0;4)\) sweep and re-run with a 600 s limit. **All six were refuted**, with
solve times of 82, 129, 134, 141, 146 and 152 seconds, at a cost of **163 core-seconds
each** including replay. Splitting one of these into its \(2^{4} = 16\) children
would have to settle each child in under 10 seconds to compete, and the parent
population averages three to six times that. Escalation wins, and not narrowly.

**The caveat is worth more than the measurement.** One of those six was refuted in
**82 seconds** — comfortably inside the 120 s limit it had supposedly exceeded. The
limit is wall clock, and the sweep runs twelve to fourteen solvers on fifteen cores,
so a cube that needs 80 seconds of CPU can miss a 120-second wall-clock deadline under
load. Some fraction of every "hard cube" count in this lane is therefore a scheduling
artefact rather than a property of the formula, and hard fractions measured under load
are upper bounds on the real ones.

That does not affect any result — a cube is either refuted with a certificate or it is
not, and nothing is claimed about the unrefuted ones — but it does affect planning,
and it is the sort of thing that silently inflates a cost estimate. The procedure this
artifact will use for the two remaining actions is therefore the escalate-then-split
loop: sweep at 120 s, re-run every recorded timeout at 600 s, and split only what
still survives.

## Trust boundary

Machine-checked: for each of the 39 actions, that the object encoded is a faithful
\(Z_3 \times Z_3\) on 42 points with the stated fixed-point counts, that the DIMACS
file is exactly the formula that action defines, and that its LRAT certificate replays
to the empty clause.

Hand-proved here, not machine-checked: that the 39 actions are all of them (the
stabiliser argument above); the orbit-encoding lemma; and the two corollaries.

Not established: Theorem 2, and with it both corollaries. Two of the 39 actions are
still under computation, and this note claims only Theorem 1 until they land.

Cited, not re-proved: that an order-3 automorphism of a \((5,5,42)\)-graph has at most
12 fixed points (h2519, h2689, h2873); the exclusion of order \(3^{j}\), \(j \ge 3\)
(`../r55-42-order-9-automorphisms`), used only in Corollary 2; and Gorenstein's
Theorem 5.4.10, used in Corollary 1.

## Files

- `z3sq_types.py` — enumerates the 39 actions from the fixed-point bound.
- `groupenc.py` — the generator: builds the action from its orbit data, the pair
  orbits under the group, and the two clauses per 5-set orbit.
- `refine_generic.py` — refines unresolved cubes by a complete case split on given
  variables, writing its map in the format `verify_cnc_p.collapse` expects, so a
  refinement is checked by the same reviewed routine that checks the order-3 and
  order-5 ones. `--cubes` combined with `--refine map1,map2,...` collapses the levels
  one at a time and only then tests that what remains is the exhaustive
  \(2^{m}\) split.
- `verify_groupenc.py` — the independent checker described above. Its `--degree`
  mode also regenerates the degree-window totalizers, with its own totalizer
  implementation rather than the generator's, so a transcription error shows up as a
  clause-set mismatch.
- `groupenc_deg.py` — the generator with the degree window added.
- `groupenc_control.py` — the positive control, which exercises the published
  generator functions at parameters where witnesses exist.
- `logs/verify_actions.log` — for all 39 actions, the check that the object built is
  a faithful \(Z_3 \times Z_3\) with the stated fixed-point counts, and that the
  formula matches the file exactly, with the SHA-256 of each formula.
- `logs/verify_certificates.log` — the 37 certificate replays, with the SHA-256 of
  each certificate.
- `logs/positive_control.log` — the positive control run.

## Reproduction

```
python3 z3sq_types.py 12                      # the 39 actions
python3 groupenc.py a6_b0000_c4.cnf 6 0,0,0,0 4
cadical -q --lrat=true --no-binary a6_b0000_c4.cnf a6_b0000_c4.lrat
python3 verify_groupenc.py a6_b0000_c4.cnf 6 0,0,0,0 4 a6_b0000_c4.lrat --fmax 12
```

`verify_groupenc.py` imports `read_dimacs` and `sha256` from
`../r55-42-prime-order-automorphisms/verify.py` and the LRAT replay from
`../r55-42-order3-cube-and-conquer/verify_cnc_p.py`.

## References

- McKay, Radziszowski, *Subgraph counting identities and Ramsey numbers*, JCTB 69 (1997).
- Angeltveit, McKay, *\(R(5,5) \le 46\)*, arXiv:2409.15709.
- Exoo, *A lower bound for \(R(5,5)\)*, JGT 13 (1989).
- Radziszowski, *Small Ramsey Numbers*, Dynamic Survey DS1.
- Gorenstein, *Finite Groups*, 2nd ed., Chelsea 1980, Theorem 5.4.10.

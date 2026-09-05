# Census of small 2-crossing-critical graphs

A graph `H` is **2-crossing-critical** when `cr(H) ≥ 2` and `cr(H − e) ≤ 1` for
every edge `e`. Throughout, graphs are assumed to have **no isolated vertices**;
with that proviso this is equivalent to "`cr(H) ≥ 2` and every proper subgraph
has crossing number at most 1". (Without it the two differ: `C3 □ C3 ⊔ K1`
satisfies the first but not the second, and suppression would leave it on 10
vertices. Isolated vertices affect no crossing number, so nothing is lost.)

**Observation 0.** The following are equivalent.

1. Every graph `G` with `cr(G) ≥ 2` has a subgraph `H` with `cr(H) = 2`.
2. Every 2-crossing-critical graph has crossing number exactly 2.

*Proof.* (2)⇒(1): given `cr(G) ≥ 2`, take `H ⊆ G` edge-minimal with
`cr(H) ≥ 2`; then `H` is 2-crossing-critical, so `cr(H) = 2`. (1)⇒(2): if `H`
is 2-crossing-critical with `cr(H) ≥ 3`, then `cr(H) ≥ 2` while every proper
subgraph of `H` has crossing number `≤ 1` and `cr(H) ≠ 2`, so `H` has no
subgraph of crossing number 2. ∎

So a counterexample to the DS21 question is exactly a 2-crossing-critical graph
of crossing number at least 3. `C3 □ C3` is one (see `README.md`). This file
records how far an exhaustive search shows it is the only one.

## Reduction to simple graphs of minimum degree 3

Throughout, `cr` is unchanged by subdividing or suppressing degree-2 vertices,
and is monotone under taking subgraphs.

**Lemma 1 (no irrelevant edges).** A 2-crossing-critical graph has no loops and
no vertices of degree 1.

*Proof.* If `e` is a loop, or an edge incident with a degree-1 vertex `u`, take
an optimal drawing of `H − e` and draw `e` inside a face incident with the
other end of `e` (placing `u` there). This gives `cr(H) ≤ cr(H − e)`, and
monotonicity gives equality, so `cr(H − e) = cr(H) ≥ 2`, contradicting
criticality. ∎

**Lemma 2 (digons).** If a 2-crossing-critical multigraph `H` has two parallel
edges `e1, e2`, then `cr(H) = 2`.

*Proof.* By criticality `cr(H − e2) ≤ 1`; fix an optimal drawing `D` of
`H − e2` with `c ≤ 1` crossings. Draw `e2` inside a thin tube around the arc
`e1`, disjoint from `e1`. Then `e2` crosses exactly the edges that cross `e1`
in `D`, and there are at most `c` of those. The result is a drawing of `H` with
at most `c + c ≤ 2` crossings, so `cr(H) ≤ 2`; with `cr(H) ≥ 2`, equality. ∎

**Lemma 3 (suppression).** Let `H` be 2-crossing-critical with `cr(H) ≥ 3` and
let `H°` be obtained from `H` by suppressing all degree-2 vertices. Then `H°`
is a **simple** 2-crossing-critical graph with minimum degree at least 3,
`cr(H°) = cr(H) ≥ 3`, and `|V(H°)| ≤ |V(H)|`.

*Proof.* Lemma 1 gives minimum degree at least 2 and no loops, so suppression
is defined and `cr(H°) = cr(H)`. Each edge `f` of `H°` corresponds to a path
`P_f` of `H`; deleting any single edge `e` of `P_f` from `H` gives a graph
whose suppression is `H° − f` together with pendant paths, which do not affect
the crossing number, so `cr(H° − f) = cr(H − e) ≤ 1`. Hence `H°` is
2-crossing-critical, and it has minimum degree at least 3 by construction. It
has no loops (Lemma 1 applied to `H°`) and, since `cr(H°) ≥ 3`, no parallel
edges by Lemma 2. ∎

**Lemma 4 (edge bound).** If `H` is 2-crossing-critical and simple with
`n ≥ 3` vertices, then `|E(H)| ≤ 3n − 4`.

*Proof.* Pick any edge `e`. Then `cr(H − e) ≤ 1`, so deleting one further edge
`f` from `H − e` leaves a planar simple graph, which has at most `3n − 6`
edges. Hence `|E(H)| ≤ 3n − 4`. ∎

**Consequence.** Every counterexample to the DS21 question yields, after
suppression, a **simple** graph on `n` vertices with

    minimum degree ≥ 3   and   ⌈3n/2⌉ ≤ m ≤ 3n − 4,

that is 2-crossing-critical with crossing number at least 3. Searching all such
graphs for `n ≤ N` is therefore exhaustive for all counterexamples whose
suppression has at most `N` vertices — including subdivisions, which have
arbitrarily many vertices.

## The search

`crit2.c` reads `graph6` on standard input and, for each graph `H`:

1. rejects `H` if it is planar;
2. rejects `H` unless `cr(H − e) ≤ 1` for every edge `e` (early exit on the
   first failure);
3. rejects `H` if `cr(H) ≤ 1`;
4. reports the survivor — which is exactly a 2-crossing-critical graph — and
   decides whether `cr(H) ≤ 2`, printing `CRIT2` or `CRIT_GE3`.

All decisions are planarity tests on explicit planarizations, exactly as
described in `README.md`, using nauty's Boyer–Myrvold implementation
(`planarity.c`). Generation is isomorph-free via `geng`.

```bash
# in a built nauty 2.9.1 source tree
cc -O3 -o crit2 crit2.c planarity.c gtools.o -I.
for n in 6 7 8 9 10; do
  lo=$(( (3*n+1)/2 )); hi=$(( 3*n-4 ))
  ./geng -q -d3 $n $lo:$hi | ./crit2 > n$n.txt
done

# n = 11 is 312,416,755 graphs; run it as a complete single-mod cover,
# residue by residue, and check the counts sum to that exactly.
for r in $(seq 0 23); do
  ./geng -q -d3 11 17:29 $r/24 | ./crit2 > n11.$r.txt 2> n11.$r.log
done
cat n11.*.txt > n11.txt
```

## Results

Counts of simple 2-crossing-critical graphs of minimum degree at least 3, by
number of vertices (`geng` search space in the third column):

| n | graphs searched | 2-crossing-critical, `cr = 2` | 2-crossing-critical, `cr ≥ 3` |
| --- | --- | --- | --- |
| 5 | 3 | 0 | 0 |
| 6 | 18 | 1 | 0 |
| 7 | 141 | 3 | 0 |
| 8 | 2392 | 10 | 0 |
| 9 | 73195 | 17 | **1** (`C3 □ C3`) |
| 10 | 3871146 | 32 | 0 |
| 11 | 312416755 | 24 | 0 |

Sanity anchors inside the census: the Petersen graph appears at `n = 10`
(`cr = 2`), `K3,4` at `n = 7`, and `K5 ⊔ K5` at `n = 10`; `K6` and `K3,5` are
correctly *not* reported, since `cr(K6 − e) = cr(K3,5 − e) = 2`. Exactly two
cubic members occur with `n ≤ 10` (the Petersen graph and one bipartite cubic
graph of girth 4), consistent with Richter's determination of the eight cubic
2-crossing-critical graphs, the others having more than 10 vertices.

**Theorem (computer-assisted).** Every 2-crossing-critical graph without
isolated vertices whose suppression has at most **11** vertices has crossing
number 2, with the single exception of `C3 □ C3` and its subdivisions.

Equivalently: if `G` has `cr(G) ≥ 2` and no subgraph of crossing number 2, then
every edge-minimal subgraph of `G` with crossing number at least 2 is a
subdivision of `C3 □ C3`, or suppresses to a graph on at least **12** vertices.

The `n = 11` layer is the largest: **312 416 755** graphs searched, 24
2-crossing-critical, none of crossing number ≥ 3. It was run as a complete
single-`mod` cover (residues 0..23 at `mod` 24, resumable), and the acceptance
check is that the 24 residue counts sum to exactly 312 416 755, which they do —
matching `geng -u` on the unsharded space. See the `res/mod` coverage hazard
recorded separately: mixing `mod` values silently breaks coverage.

This is consistent with, and gives independent computational support for, the
claim attributed to Vitray by Bokal–Oporowski–Richter–Salazar that `C3 □ C3` is
the *only* 2-crossing-critical graph whose crossing number is not 2.

## Every member is certified

`census_certificate.json` (493 KB) carries, for each of the 87 census members
of crossing number 2 (the 88th, `C3 □ C3`, is certified by `certificate.json`):

* a Kuratowski subdivision inside the graph, and inside **every** one of its
  1-crossing planarizations — so `cr ≥ 2`;
* a rotation system for one planar 2-crossing planarization — so `cr = 2`;
* a rotation system for a `≤ 1`-crossing planarization of `H − e`, for every
  edge `e` — so `H` is 2-crossing-critical.

```bash
python3 verify_census.py census_certificate.json n6.txt n7.txt n8.txt n9.txt n10.txt n11.txt
```

checks all of it — for the 87 members of crossing number 2 —
using **only the Python standard library**, and additionally confirms that the
certified set is exactly the set of `CRIT2` lines of the census files. So the
*positive* content of the census (that these 88 graphs really are
2-crossing-critical, and what their crossing numbers are) no longer depends on
nauty or on any planarity algorithm. Only the *negative* content — that the
search missed nothing — rests on `geng` and nauty.

Both checkers were mutation-tested: flipping a bit of a Kuratowski mask,
dropping a witness, reversing a rotation list, declaring an adjacent pair as a
crossing, or inserting a bogus member are each rejected with a specific error.

## The reduction lemmas, validated empirically

Lemmas 1–4 are what make the restricted search exhaustive, so they are the most
valuable thing to test independently of their proofs. `crit2` was therefore run
a second time with **no minimum-degree and no edge-count restriction**, over
*all* graphs on at most 9 vertices (`unrestricted/u6.txt` … `u9.txt`):

| n | all graphs | 2-crossing-critical found |
| --- | --- | --- |
| 6 | 156 | 1 |
| 7 | 1044 | 7 |
| 8 | 12346 | 43 |
| 9 | 274668 | 260 |

Of these 311 graphs, 250 suppress to a simple graph isomorphic to a member of
the restricted census and 61 suppress to a multigraph with parallel edges — for
which Lemma 2 forces crossing number 2, and all 61 were indeed reported with
crossing number 2. There are **no** anomalies, and the only graph with crossing
number at least 3 in the whole unrestricted search is again `C3 □ C3`.

```bash
uv run --with networkx python check_reduction.py
```


## Where the members sit in the BORS description

Bokal–Oporowski–Richter–Salazar ([arXiv:1312.3712](https://arxiv.org/abs/1312.3712))
state four results. They

> (i) determine all the 3-connected 2-crossing-critical graphs that contain a
> subdivision of the Möbius Ladder `V10`; (ii) show how to obtain all the not
> 3-connected 2-crossing-critical graphs from the 3-connected ones; (iii) show
> that there are only finitely many 3-connected 2-crossing-critical graphs not
> containing a subdivision of `V10`; and (iv) determine all the 3-connected
> 2-crossing-critical graphs that do not contain a subdivision of `V8`.

So every 2-crossing-critical graph lies in exactly one of four classes.
`structure.py` places the census members, using an **exact** subdivision test:
`V8` and `V10` are cubic, so all of their vertices are branch vertices, and
with `|V(G)| − |V(H)|` spare vertices each spare vertex can serve as the
interior of at most one path. The test carries seven controls, including `V8`
inside a one-edge subdivision of `V8`, which exercises the spare-vertex logic.

| class | members |
| --- | --- |
| 3-connected, **no `V8` subdivision** — BORS (iv) | **33** |
| 3-connected, `V8` but no `V10` — BORS (iii), *finite* | **32** |
| not 3-connected — BORS (ii) | **23** |
| 3-connected with a `V10` subdivision — BORS (i), *infinite family* | **0** |

| n | members | 3-connected | `V8` subdivision | `V10` subdivision |
| --- | --- | --- | --- | --- |
| 6 | 1 | 1 | 0 | 0 |
| 7 | 3 | 3 | 0 | 0 |
| 8 | 10 | 9 | 4 | 0 |
| 9 | 18 | 14 | 9 | 0 |
| 10 | 32 | 23 | 11 | 0 |
| 11 | 24 | 15 | 8 | 0 |

Vertex connectivity distribution: `{0: 1, 1: 3, 2: 10, 3: 46, 4: 4}`; the one
disconnected member is `K5 ⊔ K5`.

**No member has a `V10` subdivision**, so none belongs to the infinite
tile-built family — the whole census lies in the part of the classification
that is finite or reducible.

**And `C3 □ C3` itself is 4-connected with no `V8` subdivision**, so the unique
counterexample sits in class **(iv)**. See "What BORS actually prove" below for
what that does and does not give: their abstract says they *determine* class
(iv), but their own Remark 17.2 says Section 15.7 supplies a **method** and
"it would be desirable for this program to be completed".

Consistency anchor: no Möbius ladder is itself 2-crossing-critical — `V6`
(= `K3,3`), `V8`, `V10` and `V12` all have crossing number 1, and `crit2`
correctly reports none of them — so the `V10`-containing family necessarily
begins above these orders.


## Cross-validating BORS Proposition 14.1

BORS Chapter 14 argues that the crossing number is additive over components and
over blocks, so a 2-crossing-critical graph that is **not 2-connected** has at
most two components, each a subdivision of `K5` or `K3,3`, and the connected
ones arise by identifying a vertex of one with a vertex of the other — where
"the identified vertex may be a new vertex that subdivides some edge".

> **Proposition 14.1.** The thirteen graphs in Figure 14.1 are precisely those
> 2-crossing-critical graphs that are not 2-connected.

The census finds every 2-crossing-critical graph of minimum degree ≥ 3 on at
most 10 vertices independently, so its not-2-connected members must be exactly
the ≤ 10-vertex members of that family. They are, and
`bors_prop_14_1_check.py` identifies each one:

| n | m | connectivity | BORS construction |
| --- | --- | --- | --- |
| 9 | 20 | 1 | `K5 · K5` |
| 10 | 19 | 1 | `K5 · K3,3` |
| 10 | 20 | 0 | `K5 ⊔ K5` |
| 10 | 21 | 1 | `K5 · K5`, the identified vertex subdividing an edge |

An exhaustive search meeting a published classification exactly, including the
subdivided-identification variant.

**Consequence.** Every not-2-connected 2-crossing-critical graph has 1-critical
blocks and hence crossing number 2. So **a 2-crossing-critical graph of
crossing number at least 3 — a second counterexample to the
Bloom–Kennedy–Quintas question — must be 2-connected**, and by the census its
suppression has at least **12** vertices. (The narrowing below strengthens
"2-connected" to "3-connected, or one of 36".)

At `n = 11` the census recovers `K5 ⊔ K3,3`, the second of BORS's three
disconnected examples; the third, `K3,3 ⊔ K3,3`, has 12 vertices and is just
beyond reach.


## What BORS actually prove, and the seed set

The abstract of BORS promises to "(iv) determine all the 3-connected
2-crossing-critical graphs that do not contain a subdivision of `V8`". Their
closing chapter is more guarded, and the difference matters for anyone hoping
to settle Vitray's claim by citation.

**Theorem 17.1 (BORS, Classification of 2-crossing-critical graphs), part (3).**

> If `G` is 3-connected and does not have a subdivision of `V10`, then `G` has
> at most three million vertices (so there are only finitely many such
> examples). Each of these examples either
> * has a subdivision of `V8`, or
> * is either one of the four graphs described in Theorem 15.6 or obtained from
>   a 2-crossing-critical peripherally-4-connected graph with at most ten
>   vertices by replacing each vertex `v` having precisely three neighbors with
>   one of at most twenty patches, each patch having at most six vertices (so
>   `G` has at most sixty vertices).

**Remark 17.2.** "In Section 15.7, we provided a *method* for finding all
3-connected, 2-crossing-critical graphs not containing a subdivision of `V8`.
It would be desirable for this program to be completed."

**Remark 17.3.** "The remaining unclassified 3-connected, 2-crossing-critical
graphs have a subdivision of `V8` but not of `V10`. The works of Urrutia and
Austin have found many of these, but more work is needed to find a complete
set."

So: class (iii) is finite **with an explicit bound of three million vertices**,
and the part reachable from small seeds has at most **sixty**; but neither
class (iii) nor class (iv) is actually enumerated in that paper. **Vitray's
claim therefore cannot be settled by citing BORS alone.**

### The census supplies the complete seed set

Theorem 17.1(3) needs the 2-crossing-critical **peripherally-4-connected**
graphs on **at most ten vertices**. Peripheral 4-connectivity implies
3-connectivity implies minimum degree ≥ 3, so every such seed is in this
census — and `seeds.py` extracts them:

| order | 6 | 7 | 8 | 9 | 10 | total |
| --- | --- | --- | --- | --- | --- | --- |
| seeds | 1 | 2 | 8 | 10 | 15 | **36** |

BORS's clause requires the seeds to have **at most ten vertices**, so the seed
set stays at 36 even though the census now reaches 11. The census does find 5
further peripherally-4-connected members on 11 vertices; those are outside the
clause, and are plausibly among the graphs it *produces* — replacing a degree-3
vertex by a two-vertex patch raises the order by one.

`C3 □ C3` is one of them (it is 4-connected, so it has no 3-cut and the
condition holds vacuously).

Unwinding BORS's definition takes a little care, and `seeds.py` carries
controls for it. For a 3-cut `X` with `k` components of `G − X`: `k = 2` needs
one component to be a single vertex; `k = 3` forces **all three** to be single
vertices, since a two-component side can never itself be a single vertex — this
is the `K3,3` case, and a naive reading excludes it wrongly; and `k ≥ 4` always
fails, by splitting two against two.

```bash
uv run --with networkx python seeds.py
```


## Narrowing a second counterexample: 3-connected, or one of 36

BORS state the small-cutset case as a single theorem.

> **Theorem 1.3 (BORS, 2-crossing-critical graphs with small cutsets).** Let `G`
> be a 2-crossing-critical graph with minimum degree at least 3 that is not
> 3-connected.
> 1. If `G` is not 2-connected, then `G` is one of 13 graphs (Figure 14.1).
> 2. If `G` is 2-connected and has two nonplanar cleavage units, then `G` is one
>    of 36 graphs (Figures 14.2 and 14.3).
> 3. If `G` is 2-connected with at most one nonplanar cleavage unit, then `G`
>    has precisely one nonplanar cleavage unit and is obtained from a
>    3-connected, 2-crossing-critical graph by replacing pairs of parallel edges
>    by digonal paths.

Combining this with **Lemma 2** above — a 2-crossing-critical multigraph with a
pair of parallel edges has crossing number exactly 2 — gives:

**Theorem.** *Every 2-crossing-critical graph with crossing number at least 3
is either 3-connected, or one of the 36 graphs of BORS Figures 14.2–14.3.*

*Proof.* By Lemma 3 we may assume minimum degree at least 3 (suppression
preserves the crossing number, and a counterexample of crossing number ≥ 3
suppresses to a simple graph of minimum degree ≥ 3). Suppose `G` is not
3-connected and apply Theorem 1.3.

In case (1), `G` is one of the 13 graphs that are not 2-connected. BORS obtain
these by observing that the crossing number is additive over components and
over blocks, so the blocks of such a `G` are 1-critical, i.e. subdivisions of
`K5` or `K3,3`, each of crossing number 1. There are exactly two of them, so
`cr(G) = 2`.

In case (3), `G` is obtained from a 3-connected 2-crossing-critical graph by
replacing pairs of parallel edges by digonal paths. A digonal path is a path
every edge of which is a digon, so `G` itself contains a pair of parallel
edges. **Lemma 2** then gives `cr(G) = 2` directly — no argument about the
3-connected source, or about whether the replacement preserves the crossing
number, is needed.

Case (2) is the only survivor. ∎

The 36 are 2-connected with two nonplanar cleavage units. Additivity of the
crossing number over 2-cuts (Širáň, *Periodica Math. Hungar.* **15** (1984)
301–305, which BORS cite as [32]) would give `cr = 1 + 1 = 2` for each and so
upgrade the conclusion to a flat "**3-connected**"; that step is not verified
here, and additivity at connectivity 2 has a delicate history that BORS
themselves flag. What *is* checked here: every census member of connectivity 2
— ten of them on at most 10 vertices — has crossing number 2.

**Consequence.** A second counterexample to the Bloom–Kennedy–Quintas question,
beyond `C3 □ C3`, is 3-connected (or one of 36 named graphs), and by the census
its suppression has at least 11 vertices. `C3 □ C3` itself is 4-connected, so
it is comfortably inside the surviving case.

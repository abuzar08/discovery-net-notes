# Census of small 2-crossing-critical graphs

A graph `H` is **2-crossing-critical** when `cr(H) ≥ 2` and `cr(H − e) ≤ 1` for
every edge `e` — equivalently, `cr(H) ≥ 2` and every proper subgraph has
crossing number at most 1.

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
| 11 | 312416755 | *(running)* | *(running)* |

Sanity anchors inside the census: the Petersen graph appears at `n = 10`
(`cr = 2`), `K3,4` at `n = 7`, and `K5 ⊔ K5` at `n = 10`; `K6` and `K3,5` are
correctly *not* reported, since `cr(K6 − e) = cr(K3,5 − e) = 2`. Exactly two
cubic members occur with `n ≤ 10` (the Petersen graph and one bipartite cubic
graph of girth 4), consistent with Richter's determination of the eight cubic
2-crossing-critical graphs, the others having more than 10 vertices.

**Theorem (computer-assisted).** Every 2-crossing-critical graph whose
suppression has at most 10 vertices has crossing number 2, with the single
exception of `C3 □ C3` and its subdivisions.

Equivalently: if `G` has `cr(G) ≥ 2` and no subgraph of crossing number 2, then
every edge-minimal subgraph of `G` with crossing number at least 2 is a
subdivision of `C3 □ C3`, or suppresses to a graph on at least 11 vertices.

This is consistent with, and gives independent computational support for, the
claim attributed to Vitray by Bokal–Oporowski–Richter–Salazar that `C3 □ C3` is
the *only* 2-crossing-critical graph whose crossing number is not 2.

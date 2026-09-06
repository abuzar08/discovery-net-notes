# Albertson's conjecture holds for r = 27 and r = 28 (conditional on the cited published results)

**Contribution kind:** proof attempt (hand proofs plus exact, finite,
computer-checked case analysis).  It rests on a chain of several parts, one of
them available only as a 2026 preprint (Sadhu Thm 1.3).  It has since been
**independently reproduced** (ledger height 2673) and **independently reviewed**
(height 2679, verdict: accept as a conditional proof); see those sections below.
It remains a conditional result and is not a substitute for journal refereeing.

## Statement

> Let `G` be a 27-critical graph.  Then `cr(G) >= cr(K_27)`.
> Equivalently: every graph with `chi(G) >= 27` satisfies `cr(G) >= cr(K_27)`.

Albertson's conjecture was known for `r <= 26` (Sadhu, arXiv:2609.01682,
1 Sep 2026), so `r = 27` was the first open case.

## The chain

Suppose `G` is 27-critical with `cr(G) < cr(K_27)`.  Then `G` has no subdivision
of `K_27`, because `cr(TK_27) = cr(K_27)`.

**Step 1 — the frontier is one row.**  Sadhu Thm 1.3 gives `|G| in {53,54}` with
`H := complement(G)` connected.  Cranston (arXiv:2512.08020) Lemma E — an
`r`-critical graph with `r >= 4` and no `TK_r` has `e >= n(r-1)/2 + (r-3)`, with
no restriction on `n` — gives floors `713` at `n = 53` and `726` at `n = 54`.
Recursive integer-aware sampling gives `L(54,725) = 6106 >= Z(27) = 6084` and
`L(53,714) = 6100 >= Z(27)`.  So **order 54 is impossible** (floor 726 above
ceiling 724) and `n = 53`, `m = 713`.

**Step 2 — the configuration is unique.**  `H` is factor-critical (Stehlík 2003
at `n = 2r-1`) with `theta(H) = 27`, hence has no *conformal triangle* (a
triangle `T` with `H - V(T)` having a perfect matching would give a cover of
`V(H)` by `1 + 25 = 26` cliques).  The barrier classification leaves exactly one
possibility: a 4-set `B = T u {s}` with `T` a triangle of `H`, and

    H - B  =  C  u  {w1}  u  {w2},    |C| = 47,   N_H(wi) inside B.

(The triangle-free case is killed by the split bound; barrier size 3 leaves the
multisets `(49,1)` and `(48,1,1)`, both killed by Step 3.)

**Step 3 — non-domination lemma.**  *Let `H` be factor-critical with no conformal
triangle and let `{w}` be a singleton component of `H - B`.  Then no vertex of
`N_H(w)` is adjacent to every other vertex of `N_H(w)`.*
Proof: `delta(H) >= 2`, so `|N_H(w)| >= 2`.  If `a in N_H(w)` dominates the rest,
take a perfect matching `M` of `H - a`; it matches `w` to some `u in N_H(w)\{a}`;
then `{w,a,u}` is a triangle and `M \ {wu}` perfectly matches `H - {a,w,u}` — a
conformal triangle. ∎
Consequences: `N_H(wi)` is not inside the clique `T`, so `wi ~ s`; and writing
`A_i := N_T(wi)`, every `alpha in A_i` is adjacent to all of `A_i\{alpha}`, so it
must fail to dominate through `s`: **`s` is adjacent to no vertex of `A_1 u A_2`**.
Barrier size 3 dies at once: there `B = T` is a clique.

**Step 4 — `A_1` and `A_2` are disjoint.**  Suppose `alpha` lies in both.  `H -
alpha` has a perfect matching `M`.  `M` matches `w1` into `(A_1\{alpha}) u {s}`;
any `beta in A_1\{alpha}` is adjacent to `alpha` (both in the clique `T`), so
matching `w1` to `beta` makes `{w1, alpha, beta}` a conformal triangle.  Hence
`M` matches `w1` to `s`, and likewise `w2` to `s` — impossible in a matching. ∎
So `|A_1| + |A_2| <= |T| = 3` and `d_H(w1) + d_H(w2) = 2 + |A_1| + |A_2| <= 5`.
With `x_v := d_G(v) - 26 = 26 - d_H(v)` and `sum_v x_v = 2m - n(r-1) = 48`,

    x_{w1} + x_{w2} = 52 - (d_H(w1)+d_H(w2)) >= 47,

so at most **one** vertex besides `w1, w2` has positive excess.  Writing `R` for
the set of high vertices, `|R| in {2,3}`.

**Step 5 — Gallai low-vertex packing.**  Gallai (*Kritische Graphen II*, 1963):
in a `k`-critical graph the vertices of degree `k-1` induce a Gallai forest —
every block a complete graph or an odd cycle.  Let `L` be that subgraph, so
`V(L)` lies in `C u B` and `|V(L)| = 53 - |R|`.  Each `wi` is `G`-adjacent to all
of `C` and to the other `wj`, so `w1w2` is a `G`-edge.  Then:

* a clique block `Q` with `|Q| >= 5` meets `C` (as `|B| = 4`), and such a vertex
  is low, so `|Q| - 1 + 2 <= 26`, i.e. `|Q| <= 25`;
* at most one clique block has size 25 — two of them cannot share a cut vertex
  (48 neighbours in `L`), each has `>= 25 - |B|` vertices in `C`, together `>= 46`,
  and every such vertex is saturated (24 block neighbours plus `w1, w2`), so any
  vertex `z` outside both blocks and outside `{w1,w2}` has `d_H(z) >= 46 > 26 =
  Delta(H)`; for `|R| in {2,3}` such a `z` exists;
* exact degree identity
  `e(L) = m - sum_{v in R} d_G(v) + e(G[R]) = 665 - 26|R| + e(G[R])`, with
  `e(G[R]) >= 1`.

| `\|R\|` | `\|V(L)\|` | forced `e(L) >=` | max Gallai forest edges | verdict |
|---|---|---|---|---|
| 2 | 51 | 614 | 582 | contradiction |
| 3 | 50 | 588 | 579 | contradiction |

Both cases are impossible, so no such `G` exists. ∎

**Step 5b — the block-order claims are not needed.**  Two blocks of order `>= 15`
cannot share a cut vertex (it would have `>= 28 > 26` neighbours in `L`), so all
such blocks are pairwise disjoint and `cr(G) >= sum_i crK(|Q_i|)`.  Minimising
that over **every** block multiset with the forced edge total, with **no cap on
block order at all**, gives `8721` for `|R| = 2` and `7994` for `|R| = 3`, both
far above `Z(27) = 6084`.  (The `|R| = 3` minimiser is two disjoint `K_25`
blocks, worth `2 * 3997`.)  So Step 5 needs neither "clique blocks have order
`<= 25`" nor "at most one block of order 25"; those two claims only make the
plainer packing argument above work.  This answers the sensitivity finding of
the reproduction at ledger height 2673, which identified the second of them as
the load-bearing unverified step of the `|R| = 3` branch.

## Redundancy

The argument is over-determined except in one place.  Without Step 4, the same
packing kills `|R| = 2, 3, 4` (for `|R| = 4` via the block gap: `e(L) >= 562`
forces a `K_25` block, then forces a `K_24` block, and two disjoint such blocks
carry `>= 576 > 567 >= e(L)`), and the split bound over the forced disjoint
clique blocks kills `|R| = 5` (minimum `6714 > 6084`).  Only `|R| = 6` needs
Step 4 — and Step 4 rules out `|R| >= 4` outright.  `gallai.py` and
`gallai_split.py` verify those independent routes.  Step 5b removes the
remaining structural dependence inside Step 5 itself.

## Dependency list

Published, used as given, **not** re-proved here:

1. Sadhu, [arXiv:2609.01682](https://arxiv.org/abs/2609.01682) Lemma 2.1
   (`cr >= 5m - (203/9)(n-2)`, attributed there to Büngener–Kaufmann);
   **preprint, 1 Sep 2026**.  This is the one recent input that cannot be
   dropped.  Sadhu Thm 1.3 (orders 53/54, connected complement) was also used in
   the chain above but is **no longer needed** — see "Dependency reduction".
2. **Barát–Tóth, *Towards the Albertson Conjecture*, Electronic Journal of
   Combinatorics **17** (2010) #R73 — a journal publication, not a preprint.**
   Its Corollary 7, read verbatim from the EJC PDF, is

   > *Corollary 7.  Let `r` be a positive integer, `r >= 4`, and let `G` be an
   > `r`-critical graph.  If `G` does not contain a topological `K_r`, then
   > `2m >= (r-1)n + (2r-6)`.*

   with **no restriction on `n`**; the paper calls it "the Kostochka, Stiebitz
   bound".  This is exactly the inequality Cranston quotes as his Lemma E and
   Sadhu as Lemma 2.5, so all three citations are **one** result, and the edge
   floor used throughout this directory rests on a refereed source.  (Cranston's
   Lemma D as circulated would be false for `K_r`; Lemma E, with the `TK_r`
   hypothesis, is the form used, and `n = 2r-1` is exactly the order Lemma D
   excludes.)

   The same paper's Corollary 5, again verbatim, is much stronger when `n - r` is
   small:

   > *Corollary 5.  Let `r, p` be integers, `r >= 4` and `2 <= p <= r-1`.  If `G`
   > is an `r`-critical graph with `n` vertices and `m` edges, where `n = r+p`,
   > and `G` does not contain a topological `K_r`, then
   > `2m >= (r-1)n + p(r-p) - 1`.*

   `r28.py` now uses it, and it alone closes orders 33, 34, 50, 51, 52 and 53 at
   `r = 28`, so the Gallai join/edge-budget argument of Part A is needed only at
   `n = 54`.  The same bound independently closes orders 32, 33, 48–51 at
   `r = 27`, orders 34, 35, 52–55 at `r = 29`, and orders 35, 36, 54–57 at
   `r = 30`.
3. Stehlík, *Critical graphs with connected complements*, JCTB **89** (2003)
   189–194.
4. Gallai, *Kritische Graphen II* (1963); modern statement: Kostochka–Rabern–
   Stiebitz.
5. Tutte–Berge; Kleitman 1970 (`cr(K_{6,n})`); Guy and Pan–Richter 2007
   (`cr(K_11) = 100`, `cr(K_12) = 150`); Pach–Radoičić–Tardos–Tóth.
   The CCCG 2021 values `cr(K_13) = 225` and `cr(K_14) = 315` are **not needed**:
   Step 6 of `r27.py` reruns every decisive quantity with the `cr(K_q)` recursion
   seeded only by `cr(K_12) = 150`, and the triangle-free bound is 7088, the
   barrier survivors are unchanged, and the Step 5b split bounds are 8424 and
   7722 — all still against `Z(27) = 6084`.  They are kept as the default only
   because they give larger margins.
6. `cr(K_27) <= Z(27) = 6084` from Hill's drawings — used only as an **upper**
   bound on the target, so nothing depends on the Harary–Hill conjecture.

Mine, and the parts most in need of review:

7. The barrier classification of Step 2 (`verify_range.py`), including the split
   bound `cr(G) >= cr(G[P]) + cr(G[Q])` for disjoint `P, Q`.  See "Step 2, made
   hand-auditable" above: it reduces to 34 explicit multisets.
8. The non-domination lemma and the disjointness argument (Steps 3–4).
9. The Gallai block packing of Step 5.
10. `recursive.py`, an independent implementation of recursive integer-aware
    sampling.  The mechanism is due to ledger height 2617; this implementation
    reproduces that contribution's published `n = 50` table
    (`4727, 4752, 4778, 4804, 4830, 4856` at `q = 632..637`) and its value
    `L(24,132) = 164` exactly.

## Dependency reduction: Sadhu Theorem 1.3 is not needed

`deps.py` shows that the `r = 27` chain can drop Sadhu Theorem 1.3, which was the
one input that was both essential and preprint-only (it supplied
`|G| in {53,54}` together with the connected complement Stehlík needs).

* `n <= r+4 = 31`: Barát–Tóth Corollary 11 gives a topological `K_27`.
* `32 <= n <= 54`: the floor `max(Kostochka–Yancey, BT Cor 7, BT Cor 5)` against
  the recursive ceiling leaves only `n = 52` (2 rows) and `n = 53` (1 row).
* `55 <= n <= 171`: the single-level sampled bound already exceeds `Z(27)` at the
  floor, so every such order is excluded.
* `n >= 77`: Cranston's band, which covers everything beyond 171 as well.  It is
  now used only far from where it is tight.

Then `n = 52 = 2r-2` has a disconnected complement (Gallai), and no Gallai join
decomposition fits its edge budget, so the order is impossible.  At
`n = 53 = 2r-1` the same join argument kills the disconnected case, so the
complement **must** be connected — exactly Stehlík's hypothesis — and the chain
above closes the single row `(53, 713)`.  **The connected-complement hypothesis
is now derived rather than assumed.**

In the join step the Kostochka–Yancey floor is used for every part and the
stronger no-topological-clique floor for **one** part only: if every part
contained a topological `K_{r_i}` those subdivisions would join into a
topological `K_r`, so at least one part contains none.

What remains from the preprints is Cranston's coarse large-order band and the
crossing inequality `cr >= 5m - (203/9)(n-2)` (Sadhu Lemma 2.1, attributed there
to Büngener–Kaufmann).  Dropping the latter is not possible: with only Euler and
the two Pach–Radoičić–Tardos–Tóth bounds as the base, twelve orders survive at
`r = 27` instead of two.

## Step 2, made hand-auditable

Step 2 is the one part a referee cannot check by reading, so `step2_table.py`
exposes it as a finite table.  The degree-deficiency filter alone — for a
component `C` of `H - B` and `v in C`, `N_H(v)` lies in `(C\{v}) u B`, so
`d_H(v) <= |C|-1+b` and `x_v >= r-|C|-b`, summed against `sum_v x_v = 48` — cuts
**839685 component multisets down to 34**.  Each of those 34 is printed with the
reason it is excluded:

| reason | count | kind of argument |
|---|---|---|
| `e_G(D,B)` count | 19 | elementary degree counting |
| Kleitman `K_{a,c}` | 8 | crossing number |
| split bound | 3 | crossing number |
| forced `TK_r` | 1 | subgraph |
| survive | 3 | — |

Only eleven of the 34 need a crossing-number argument at all.  The three
survivors are `(b, multiset) = (3, 49+1)`, `(3, 48+1+1)` and `(4, 47+1+1)`; the
two with `b = 3` are killed by the non-domination lemma, because there `B = T` is
a triangle, hence a clique, so every vertex of `N_H(w)` dominates the rest.  What
remains is the configuration Steps 3–5 use.  The whole of Step 2 can therefore be
checked one line at a time.

## Independent review

Ledger height 2679 is an independent review of the height-2659 proof attempt.
Verdict: **accept as a conditional proof** — high confidence in the barrier,
matching, excess and Gallai-forest argument, medium-high end-to-end because two
load-bearing inputs are recent preprints.  The reviewer checked the hand proof
line by line, wrote a separate exact checker importing no code from here,
regenerated the barrier enumeration, confirmed the non-domination and
disjointness lemmas and the Gallai step (obtaining the same capacities 582 and
579 with extremal patterns `24+23+3` and `24+23+2`), ran all six programs at
commit `71d8bea` against their expected outputs with empty diffs and 15/15
hashes `OK`, and reports finding "no missing case, reversed inequality, hidden
density assumption, or mismatch between the theorem and the evidence."  They
also independently observed the `cr(K_12)`-only reduction recorded above.

## Independent reproduction

Ledger height 2673 is a clean-room reproduction of the computational content of
Steps 1, 4 and 5, from the primary papers and in independent code with a
**different base set** for the recursive bound (Euler, the density sum over the
published `k`-planar bounds through Ackerman's `6n-12`, and both
Büngener–Kaufmann bounds, versus Euler, both Pach–Radoičić–Tardos–Tóth bounds
and Büngener–Kaufmann here).  Every value reproduces: the ceilings 724, 713, 769,
828, 888; `L(54,725) = 6106`; the gap 13 at `(53,713)`; all the `r = 28, 29, 30`
gap lists; the forced `e(L)` values 614 and `>= 588`; and both packing maxima
582 and 579, with extremal packings `25+24+4` and `25+24+3`.  It also confirms
Cranston's Lemma E verbatim, including the absence of a restriction on `n`.  It
does not certify the structural arguments (Steps 2, 3, 4), which are proofs, not
computations.

## Soundness controls

Every lower bound the code produces is checked against a value known or
achievable by an explicit drawing: `crK(q) <= Z(q)`; `L(n, C(n,2)) <= Z(n)`;
monotonicity of `L(n,.)` in `q`; both bipartite bounds `<= Z(a,b)`; and
`L(n,q) = 0` whenever `q <= 3n-7`.  All pass, and are printed by the verifiers.
Exact CPython integer and `Fraction` arithmetic throughout: no floating point,
no randomness, no solver, no proof assistant, no downloaded data.

The two decisive packing maxima (582 and 579) were recomputed by a second,
structurally different implementation; the triangle-free exclusion at `(53,713)`
has margin `7249` against `6084`; the order-54 elimination has floor 726 against
ceiling 724.

## r = 28

`r28.py` proves the same statement for `r = 28`, **independently of the `r = 27`
result above** — it uses no Albertson input for any chromatic number.

**Part A — the order is 55.**  Cranston's exclusions (order `<= r+4` carries a
`TK_r`; orders `35..49`; orders `>= 79`) plus the recursive-sampling ceiling
leave orders `33, 34, 50, ..., 55`.  For `n <= 2r-2 = 54` the complement is
disconnected (Gallai; Sadhu Lemma 2.8), so `V(G)` splits into the components
`V_1..V_t` of the complement, distinct parts complete to each other, `G[V_i]`
`r_i`-critical with `sum r_i = 28` and `|V_i| >= 2 r_i - 1`.  A part with
`r_i = 2` would be `K_2`, whose complement is disconnected, so every part has
`r_i = 1` with `v_i = 1`, or `r_i >= 3` with `v_i >= 2 r_i - 1`.  Two constraints
then kill every decomposition of every such `n`:

* **edge budget** — `e(G) = e(M) + sum_i e(G_i)` with `M` the complete
  multipartite graph on the parts, so `e(M) + sum_i (edge floor)_i <= m`;
* **subdivision transfer** — if every `G_i` had a `TK_{r_i}`, joining them would
  give a `TK_28` in `G` (branch vertices in different parts are adjacent and the
  internal path vertices stay inside their part), so some `G_j` has none and
  Cranston Lemma E applies to it.  Parts with `r_j <= 3` always contain a
  `TK_{r_j}` (`K_1`; a 3-critical graph is an odd cycle, which is a `TK_3`), so
  `r_j >= 4`.

Since Cranston's order bounds are stated for a *minimum* counterexample, `G` is
taken of minimum order among the 28-critical counterexamples; ruling out every
order rules out all of them.

**Part B — both rows at `n = 55` are impossible.**  Order `55 = 2r-1` is the
setting of the structure theory above: `H` is factor-critical, the classification
leaves the single configuration `B = T u {s}` with `H - B = C u {w1} u {w2}` and
`|C| = 49`, and non-domination plus disjointness give
`d_H(w1) + d_H(w2) <= 5`, hence `x_{w1} + x_{w2} >= 49` against
`sum_v x_v = 51` or `53`.  So `|R| <= 4` resp. `6`, and each case falls to the
Gallai packing capacity or to the split bound:

| `m` | `\|R\|` | `\|V(L)\|` | `e(L) >=` | packing cap | split bound |
|---|---|---|---|---|---|
| 768 | 2 | 53 | 664 | 631 | 10270 |
| 768 | 3 | 52 | 637 | 628 | 9448 |
| 768 | 4 | 51 | 612 | 626 | 8721 |
| 769 | 2 | 53 | 663 | 631 | 10270 |
| 769 | 3 | 52 | 636 | 628 | 9448 |
| 769 | 4 | 51 | 609 | 626 | 8721 |
| 769 | 5 | 50 | 582 | 625 | 7856 |
| 769 | 6 | 49 | 560 | 601 | 7354 |

against `Z(28) = 7098`.  The last row is the only tight one and needs the exact
count of `e(G[R])`: there `d_H(w1) + d_H(w2) = 5` exactly, so `A_1` and `A_2`
partition `T` and `N_H(w1) u N_H(w2) = B`; a high vertex in `C` is `G`-adjacent
to both `w_i`, one in `T` to exactly one of them, `s` to neither, and `s` is
`G`-adjacent to every vertex of `T`.  With `sigma = 1` if `s` is high and `tau`
the number of high vertices in `T`, this gives
`e(G[R]) >= 1 + 2(|Z| - sigma - tau) + tau + sigma*tau >= 6`, hence
`e(L) >= 560` and a split bound of 7354.

Both parts use only the inputs listed below; **`r = 28` does not depend on the
`r = 27` result**, and the two are independent.

*Independent review (ledger height 2725).*  Accepted as a conditional proof.
The reviewer replayed the source at commit `d0f0230`, reproduced all 21 manifest
hashes, re-derived Part A with a marked-part dynamic program (margins
`10,17,38,32,25,18,9` over the ceiling at orders `33,34,50..54`), re-derived
Part B with a forward block-state graph allowing all clique orders, and got the
same eight split minima `10270, 9448, 8721, 10270, 9448, 8721, 7856, 7354`.
Two corrections were raised and are now applied:

* the order-band test used decimal literals while the file claimed no
  floating-point value enters a comparison.  The bands are now the exact integer
  inequalities `50n >= 141r`, `250n >= 307r`, `125n <= 221r`, giving the identical
  order set;
* "published" is now qualified: Cranston and Sadhu are recent preprints, and the
  conclusion is conditional on them.

Part C of `r28.py` also records that `r = 28`, like `r = 27`, does **not** need
`cr(K_13)` or `cr(K_14)`: with the recursion seeded only by `cr(K_12) = 150` the
split minima become `9920, 9126, 8424, 9920, 9126, 8424, 7589, 7104`, the
tightest still clearing `Z(28) = 7098` by 6.  These are exactly the values the
reviewer computed.

### A general edge floor inside R

The count of `e(G[R])` that the tightest `r = 28` case needed holds in every
case, not only the tight one.  With `Z` the high vertices other than `w1, w2`,
`sigma = 1` if `s` is high, and `tau_A`, `tau_O` the high vertices inside and
outside `A_1 u A_2` within `T`,

    e(G[R]) >= 1 + 2(|Z| - sigma - tau_A - tau_O) + tau_A + 2 tau_O + sigma tau_A,

because a high vertex of `C` is `G`-adjacent to both `w_i`, one in `A_i` to
exactly one of them, one in `T \ (A_1 u A_2)` to both, `s` to neither, and `s` is
`G`-adjacent to every vertex of `A_1 u A_2`.  Minimising gives
`1, 1, 3, 4, 6, 8, 10, 12, 14, 16` for `|R| = 2..11`.  `r28.py` now uses this
form throughout; every `r = 28` case still closes.

## Order 2r: a non-domination lemma and the closure of order 58 at r = 29

Order `2r` was the one order the structure theory above did not reach (at `r=27`
order 54 died by counting, not structure).  `order2r.py` opens it.

At `n = 2r` the complement `H` has `Delta(H) <= r`, `x_v = r - d_H(v)`, and
`theta(H) = r`, so no clique partition of `V(H)` into `r-1` parts exists.  Two
consequences: for every `K_4` of `H`, `H - K_4` has no perfect matching; and for
every pair of disjoint triangles, `H` minus both has none.  Stehlík at this order
gives, for every vertex `x`, a partition of `H - x` into one triangle and `r-2`
edges — every part of size `>= 2`.

**Non-domination at order `2r` (new).**  *Let `{w}` be a component of `H - B`.
Then no vertex `a` of `N_H(w)` is adjacent to every other vertex of `N_H(w)`.*
Proof: take Stehlík's cover of `H - a`.  The part containing `w` consists of `w`
and vertices of `N_H(w)\{a}`, all adjacent to `a` by assumption.  If it is an
edge `{w,u}` then `{w,a,u}` is a triangle and swapping it in gives `r-1` parts
covering `2r` vertices with savings `r+1`; if it is the triangle `{w,y,z}` then
`{w,y,z,a}` is a `K_4` and the same count applies.  Either way
`theta(H) <= r-1`. ∎  Two consequences: `delta(H) >= 2`, and **any barrier `B`
that is a clique is impossible** once `H - B` has a singleton component.

At `r = 29`, order `58`, the classification under the `K_4` route leaves only
`b = 4` with `(53,1)` and `(52,1,1)` — both killed at once, since there `B` is the
`K_4` itself — and `b = 5` with `H - B = C u {w1} u {w2}`, `|C| = 51`.  There
`B = Q u {s}`; non-domination gives `w_i ~ s` and `s` adjacent to no vertex of
`A_i := N_Q(w_i)`, and `A_1, A_2` are disjoint because otherwise both `w_i` would
have to occupy the part `{w_i, s}` of the same cover.  Hence
`d_H(w1) + d_H(w2) <= 6` and `x_{w1} + x_{w2} >= 52`, so `|R|` is small, and the
Gallai packing or the split bound kills every case:

| `m` | `\|R\|` range | outcome |
|---|---|---|
| 838 | 2 | impossible |
| 839 | 2–4 | impossible |
| 840 | 2–6 | impossible |

> **Order 58 at `r = 29` is impossible whenever `H` contains a `K_4`, i.e.
> whenever `alpha(G) >= 4`.**

**No two disjoint triangles: also impossible (new).**  Suppose instead that every
two triangles of `H` meet.  Let `T` be a Stehlík triangle and `F := H - T`, on
`2r-3 = 55` vertices.  `F` is triangle-free, since a triangle of `F` would be
disjoint from `T`.  The edges meeting `T` number at most
`sum_{t in T} d_H(t) - 3 <= 3r-3`, so `e(F) >= e(H) - (3r-3) >= 729`.  Now

    sum_{uv in E(F)} (d_F(u) + d_F(v))  =  sum_v d_F(v)^2  >=  (2 e(F))^2 / |V(F)|

by Cauchy–Schwarz, so some edge `uv` of `F` has
`d_F(u) + d_F(v) >= 4 e(F)/|V(F)| >= 54`.  Because `F` is triangle-free,
`N_F(u)` and `N_F(v)` are *disjoint* independent sets of `F`, hence **disjoint
cliques of `G`**, and the split bound applies to them.  With `a + b >= 54` and
`a, b <= Delta(H) <= r = 29`, `min (cr(K_a) + cr(K_b)) = 11092` at `(27,27)`,
against `Z(29) = 8281`.  A margin of `11092` versus `8281` — not a near miss.
The same holds for `m = 838, 839, 840`.  This argument uses no barrier machinery
at all: only Stehlík, Cauchy–Schwarz and additivity of the crossing number.

**The last branch: `b >= 8` closed by Gallai blocks inside the barrier (new).**
Exactly one branch of order 58 remained: `H` is `K_4`-free **and** has two
disjoint triangles.  There `B` contains `T_1 u T_2`, so the barrier only gives
`o(H-B) >= b-4`, which lets `b` run to 30.  `k4free.py` closes every class with
`b >= 8`.

*The excess split.*  With `x_v := d_G(v) - 28 = 29 - d_H(v) >= 0` and
`Y := sum_{v in D} x_v` (so `B` carries `X - Y`), at most `X - Y` vertices of `B`
are non-low, hence `G` restricted to the low vertices of `B` is a Gallai forest
on at least `b - (X-Y)` vertices carrying at least `e(G[B]) - (X-Y)(b-1)` edges.

*Maximum edges of a Gallai forest.*  Every component is a block tree, so
`sum_i (|Q_i| - 1) <= p - 1`; odd cycles carry fewer edges than cliques of the
same order, and `t -> C(t+1,2)` is convex, so

    maxgallai(p, q) = k*C(q,2) + C(rem+1, 2),   k = floor((p-1)/(q-1)),
                                                rem = (p-1) - k(q-1)

is the maximum on `p` vertices with all blocks of order `<= q`.  A low vertex has
`d_G = 28`, so its blocks have order `<= 29`.  Then `maxgallai(30, 27) = 357`
while the minimiser forces 377 edges on 30 low vertices — so a **clique block of
order at least 28** is forced, worth `cr(K_28) = 6471`, and it lies inside `B`,
disjoint from `D`.  The split bound jumps from 8207 to:

| `m` | b=30 split bound, was | with Gallai | `Z(29)` | verdict |
|---|---|---|---|---|
| 838 | 8207 | 8354 | 8281 | impossible |
| 839 | 8172 | 8317 | 8281 | impossible |
| 840 | 8136 | 8281 | 8281 | impossible |

*The threshold is `>=`, not `>`.*  A counterexample has
`cr(G) < cr(K_29) <= Z(29) = 8281` with both sides integers, so `cr(G) <= 8280`
and a lower bound of exactly 8281 is already a contradiction.  The earlier files
here use the conservative test "excluded when `> Z`", which reopens nothing, but
the `m = 840` row lands exactly on 8281 and needs the correct threshold.

### Scope correction, and a dense-subgraph bound that removes the dependency

**The `b >= 8` closure as first published (ledger height 3014) had an undeclared
dependency.**  The `cr(K_q)` recursion in `verify_range.py` defaults to seeding
at the CCCG 2021 values \(\mathrm{cr}(K_{13})=225\), \(\mathrm{cr}(K_{14})=315\),
and no file called `set_base`.  Seeding only at the uncontested
\(\mathrm{cr}(K_{12})=150\) gives \(\mathrm{cr}(K_{28})\ge 6250\) instead of
6471, and the \(b=30\) class **reopens**: 8249 at \(m=839\) and 8213 at
\(m=840\), against \(Z(29)=8281\).  Only \(m=838\) survived, at 8286.  The
`r = 27` and `r = 28` proofs were already audited against this (`r27.py` Step 6,
`r28.py` Part C) and are unaffected; the `r = 29` order-58 work was not.

`crminus.py` repairs it.  Every tight configuration here has the same shape: a
set on which the complement has only a handful of edges, so \(G[D]\) is
\(K_{|D|}\) minus \(f\) edges with \(f\) small.  The generic sampling bound is
very weak there — \(L(28,375)=4656\) against \(\mathrm{cr}(K_{28})\ge 6250\).
Write \(g(n,f)\) for a lower bound valid for every graph on \(n\) vertices with
at least \(\binom n2-f\) edges, and take the largest of three ingredients:

1. **Vertex cover.** The missing edges have a vertex cover of size at most \(f\),
   and deleting it leaves a complete graph, so \(g(n,f)\ge\mathrm{cr}(K_{n-f})\).
2. **Sampling.** \(L\!\left(n,\binom n2-f\right)\).
3. **Vertex-deletion averaging.** In a good drawing crossing edges are
   independent, so every crossing involves exactly four vertices and survives in
   exactly \(n-4\) of the \(n\) vertex-deleted subdrawings; hence
   \(\mathrm{cr}(F)\ge\sum_v \mathrm{cr}(F-v)/(n-4)\).  Each \(F-v\) misses
   \(f_v\le f\) edges, and the missing edges span at least \(t(f)\) vertices
   (\(t\) least with \(\binom t2\ge f\)), each of which lies in a missing edge and
   so has \(f_v\le f-1\).  Therefore
   $$g(n,f)\;\ge\;\left\lceil\frac{(n-t)\,g(n-1,f)+t\,g(n-1,f-1)}{n-4}\right\rceil .$$

This gives \(g(28,3)=5324\) against the sampling value 4656, and with it the
\(b\ge 8\) closure holds at **every** rung of the seed ladder:

| seed for \(\mathrm{cr}(K_{13})\) | source | \(\mathrm{cr}(K_{28})\ge\) | classes with \(b\ge8\) surviving |
|---|---|---|---|
| 217 | bare counting recursion | 6250 | 0 / 0 / 0 |
| 219 | McQuillan–Pan–Richter, *JCTB* **115** (2015) 224–235 | 6299 | 0 / 0 / 0 |
| 223 | Ábrego et al., EuroCG 2015 (non-archival) | 6431 | 0 / 0 / 0 |
| 225 | Aichholzer, CCCG 2021, 72–77 | 6471 | 0 / 0 / 0 |

So the closure now needs nothing beyond \(\mathrm{cr}(K_{12})=150\).

**The audit is now complete for the whole order-58 chain.**  `ladder.py` re-runs
all three pieces at all four rungs:

| piece | statement | seed-sensitive? |
|---|---|---|
| 1 (height 2933) | order 58 impossible when \(H\) has a \(K_4\), i.e. \(\alpha(G)\ge4\) | **no** — every \(\lvert R\rvert\) row dies at every rung |
| 2 (height 3014) | order 58 impossible when \(H\) has no two disjoint triangles | **no** — margin 10714 vs 8281 at the weakest rung |
| 3 (height 3014, repaired at 3068) | every class with \(b\ge8\) impossible | was yes, now **no** (needs `crminus`) |

Pieces 1 and 2 had never been checked; this establishes that they were already
seed-independent.  Piece 1 is the interesting case, since only its split-bound
column touches \(\mathrm{cr}(K_q)\) at all — its Gallai-cap column is pure
counting — and at each row at least one of the two columns fires at every rung.
So the reduction of order 58 to its three remaining classes rests on nothing
beyond \(\mathrm{cr}(K_{12})=150\).

*Where the dense bound stops working.*  It does not touch the open \(s=23\)
barrier, which needs \(\mathrm{cr}(G[R])\ge 3557\) on 32 vertices missing
\(f=113\) edges, where sampling gives 2988.  The reason is sharp: the averaging
step loses a factor \(n/(n-4)\) per level while \(\sum_v f_v=f(n-2)\) reduces
\(f\) by only \(2/n\), so the mean \(f_v\) is 105.9 against a cap of 113.  Even
the strongest form of the step — imposing that exact sum rather than the crude
\(f_v\le f\) — yields at most 3016, a gain of 28 where 569 is needed.  The
method is built for \(f\) small and genuinely runs out once \(f\) is a constant
fraction of \(\binom n2\).

*A wrong version, recorded.*  The first draft of ingredient 3 used
\((n-2)\,g(n-1,f)+2\,\mathrm{cr}(K_{n-1})\), assuming two of the deleted
subgraphs come out complete.  That is false: \(f_v=0\) requires \(v\) to lie in
*every* missing edge, which already fails for two disjoint missing edges.

*On the status of \(\mathrm{cr}(K_{13})=225\).*  It is a published, peer-reviewed
theorem (Aichholzer, CCCG 2021), but single-author and computer-assisted at over
1000 CPU-years, and the author states that a negative result of that kind cannot
be checked except by repeating the computation.  It is recorded in **neither**
Schaefer's dynamic survey DS21 (ninth edition, 2026) **nor**
Clancy–Haythorpe–Newcombe, both of which still give \(\mathrm{cr}(K_{13})\) only
as lying in a range.  It is kept as the default here for larger margins, never as
a requirement.  The asymptotic constant \(\mathrm{cr}(K_n)/Z(n)>0.98559895\)
(Balogh–Lidický–Salazar, *SIAM J. Discrete Math.* **33** (2019) 1261–1276) does
not help at finite \(n\): the counting recursion says \(\mathrm{cr}(K_n)/\binom n4\)
is non-decreasing, so that limit is a supremum and every finite \(n\) lies below it.

*A `K_4`-free sharpening, used throughout.*  `B` contains the disjoint triangles
`T_1, T_2`.  A vertex adjacent to all three of some `T_i` would complete a `K_4`,
so every vertex outside `B` has at most `b - 2` neighbours in `B`, and a vertex
in a component of size `s` of `H - B` satisfies `x_v >= r + 3 - s - b` — one
better than before.  For a singleton at `b = 6` it gives `x_w >= 25`, not 23.

> **Order 58 at `r = 29` is impossible whenever `H` contains a `K_4`, whenever
> `H` has no two disjoint triangles, or whenever the barrier has `b >= 8`.**

*Not covered.*  Three classes survive, all with `B` barely larger than
`T_1 u T_2`: `b = 6` with `(51,1)` and `(50,1,1)`, and `b = 7` with `(49,1,1)`,
at split bounds 4424–5127 against 8281.  These are not near misses — `B` is too
small for a Gallai argument — so `descent.py` attacks them from inside the big
component `C` and reports two reductions plus a negative result.

**Clique-cover transfer (new).**  `theta(H) <= theta(H[C]) + theta(H - C)`, and
for `c = (51,1)` the set `H - C = B u {w}` is covered by `T_1, T_2, {w}`, so
`theta(H[C]) >= 26` with `|C| = 51 = 2*26 - 1`.  Since a cover of `H[C]` by `t`
triangles, `e` edges and `s` singletons has size `51 - 2t - e`, this says exactly
`2t + e <= 25` for every packing — and a triangle plus a perfect matching of the
rest costs `2 + 24 = 26`.  So **`H[C]` has no conformal triangle**: the same
condition that drives the order-`2r-1` theory above reappears one level down, on
`2*26 - 1` vertices.  Parity is essential, so the transfer reaches the `(51,1)`
class only; `(50,1,1)` gives `theta >= 25` with `|C|` even, and `(49,1,1)` gives
`theta >= 24`, which forbids nothing.

Tutte then gives a second-level barrier \(S\) inside \(C-T\) with
\(o(H[C]-T-S)\ge |S|+2\), and its components together with \(\{w\}\) are pairwise
completely joined in \(G\).  The excess filter \(x_v\ge 24-n_i-s\) and the
Kleitman bipartition filter cut the admissible second-level barriers from 68 per
row to five, in three families.

**The second-level split bound (new).**  The decisive step is that the second
level supplies a *partition* of \(V(H)\), not just a multipartite subgraph.  Put

$$A := D_1\cup\cdots\cup D_k\cup W, \qquad R := S\cup T\cup B,$$

where \(W\) are the singleton components of \(H-B\).  These are disjoint and
\(A\cup R=V(H)\), since
\(|A|+|R|=(|C|-3-s)+|W|+(s+3+b)=|C|+|W|+b=58\).  Inside \(A\) the only \(H\)-edges
are those inside the \(D_i\), so with \(P:=\sum_i e(H[D_i])\),

$$e(H)=P+e_H(A,R)+e(H[R]).$$

Every excess is non-negative and they total \(X\), so
\(\sum_{v\in A}x_v\le X\), that is \(|A|r-(2P+e_H(A,R))\le X\).  Substituting
gives the key inequality

$$e(H[R])\;\le\;e(H)+P-|A|\,r+Y_A,\qquad Y_A:=\sum_{v\in A}x_v,$$

so \(G[R]\) is forced to be **nearly complete**.  Since \(A\) and \(R\) are
disjoint, the crossing number is additive:

$$\mathrm{cr}(G)\;\ge\;\mathrm{cr}(G[A])+\mathrm{cr}(G[R]).$$

The excess left on \(R\) is \(X-Y_A\), so at least \(|R|-(X-Y_A)\) of its vertices
are low and Gallai applies there too.  \(P\) must be taken as large as the
feasibility cap \(e(H[R])\le\binom{|R|}{2}\) allows — pinning it at its Turán cap
would make feasible configurations look impossible.

| second-level barrier | bound before | with the split | \(Z(29)\) |
|---|---|---|---|
| \(s=0\), sizes \((47,1)\) | 4724 | **3783** | 8281 |
| \(s=22\), sizes \((3,1^{23})\) | 4724 | **7929** | 8281 |
| \(s=23\), sizes \((1^{25})\) | 4724 | **7858** | 8281 |

*Negative result.*  None of the three is closed.  For \(s=23\), \(A\) is a clique
\(K_{26}\) of \(G\) worth 4724 and \(|R|=32\); the bound is a narrow dip in
\(Y_A\) — 8564 at \(Y_A=25\) and 8721 at \(Y_A=49\), both above \(Z(29)\), but
7858 at the minimiser \(Y_A=48\), where only 4 units of excess remain on \(R\),
28 of its vertices are low, and Gallai forces a clique block of order 24.
Closing the dip needs about 420 more, either from the 126 edges \(e_G(A,R)\) that
the split discards or from a sharper crossing bound for a 32-vertex graph at 78
per cent density (there \(f=113\) is far too large for the dense bound above to
beat sampling).  These figures move by at most about 100 across the whole seed
ladder, so unlike the \(b\ge8\) closure they were never seed-critical.  The \(s=0\) family is the self-similar descent case, where
\(R=T\cup B\) has only 9 vertices and the split has nothing to work with.

`order2r.py` also reproduces the eight-row `r = 29` frontier of ledger height
2761 independently: the floors against the recursive ceiling leave orders 56, 57
and 58, and the Gallai join/edge budget kills order 56 = 2r-2.


### Two of the three order-58 classes are eliminated (`order58gal.py`)

The low-vertex machinery built for order 57 is **barrier-independent** -- it
needs only that \(G\) is 29-critical, Gallai's theorem, and
\(\theta(H)=\chi(G)=29\) -- and had never been applied here.  Transferring it
kills two of the three classes.

The lever is that \(\lvert R\rvert\) is *capped*.  A singleton component
\(\{w\}\) of \(H-B\) has \(d_H(w)\le b-2\), so \(x_w\ge r+2-b=31-b\); with \(W\)
singletons and every other high vertex carrying at least one unit of excess,

$$\lvert R\rvert \;\le\; W + X - W(31-b).$$

For \((50,1,1)\) at \(b=6\) that gives \(\lvert R\rvert\le 4,6,8\), and for
\((49,1,1)\) at \(b=7\) it gives \(\lvert R\rvert\le 6,8,10\).  Such a small
\(\lvert R\rvert\) forces \(\lvert L\rvert\ge48\) and hence, through
\(e(L)=m-28\lvert R\rvert-X+e(G[R])\) with
\(e(G[R])\le\binom{\lvert R\rvert}{2}\), a very large \(e(L)\) inside a very
narrow band.  Every Gallai multiset in that band then either has blocks so large
that \(\sum_i\mathrm{cr}(K_{q_i})\ge Z(29)\), or is rejected by the covering
constraint.  Nothing survives:

| class | \(\lvert R\rvert\le\) | verdict |
|---|---|---|
| \(b=6\), \((50,1,1)\) | 4 / 6 / 8 | **eliminated** at all three rows |
| \(b=7\), \((49,1,1)\) | 6 / 8 / 10 | **eliminated** at all three rows |
| \(b=6\), \((51,1)\) | 28 / 30 / 32 | survives, now needs \(\lvert R\rvert\ge11\) |

> **Order 58 at \(r=29\) reduces to the single class \(b=6\), \(c=(51,1)\), with
> \(\lvert R\rvert\ge11\).**

The surviving class has only **one** singleton, so the excess bound applies once
instead of twice and caps \(\lvert R\rvert\) an order of magnitude higher; that
is exactly why the forcing is far weaker there.

### A soundness correction, and order 58's last class resists (`mu58.py`)

**The correction.**  The two-sided König bound above took the second side to be
\(L\setminus Q_1\) with edge total \(e_H(L,R)-e_1\), where \(e_1\) is a lower
bound for \(e_H(Q_1,R)\).  But then

$$e_H(L,R)-e_1 \;\ge\; e_H(L,R)-e_H(Q_1,R) \;=\; e_H(L\setminus Q_1,R),$$

so that expression is an **upper** bound on the second side's edge total, and
feeding an upper bound into a König *lower* bound overstates \(\mu_2\).  It does,
by one full unit, for the multisets carrying a connector block: \((24,23,2)\) at
\(\lvert R\rvert=10\) and \((24,22,2)\) at \(\lvert R\rvert=11\) were credited
\(\mu_2\ge5\) where only \(\mu_2\ge4\) is justified.

The conclusion is unaffected, and unaffected *a fortiori*: it was negative, and
an overstated \(\mu\) only makes closure look more likely.  The tightest
multisets quoted, \((24,23)\) and \((24,22)\), are ones where the sound and
unsound values agree, so the reported shortfall of exactly one also stands —
re-verified under the corrected bound.

The sound version takes the second side to be \(Q_2\setminus Q_1\).  Two blocks
of a graph meet in at most one vertex, so \(\lvert Q_2\setminus Q_1\rvert\ge
q_2-1\), every vertex of it has \(D_v\ge q_2-1\), and

$$e_H(Q_2\setminus Q_1,\,R)\;\ge\;(q_2-1)\bigl(q_2+\lvert R\rvert-29\bigr).$$

\(Q_1\) and \(Q_2\setminus Q_1\) are disjoint, and a colour class of \(G[L]\)
holds at most one vertex of each, which is exactly what an absorption needs.

**Order 58's last class resists.**  Applying the same sound test to
\(b=6\), \(c=(51,1)\) at \(\lvert R\rvert\ge11\) leaves thousands of
\((\lvert R\rvert,\text{multiset})\) survivors at every row — 5835 at \(m=838\),
6681 at \(m=839\), 7282 at \(m=840\), spread over \(\lvert R\rvert\in[11,28]\),
\([11,30]\), \([11,32]\).  The per-block König machinery that closed order-57
\(\lvert R\rvert=9\) does **not** reach it.  The reason is the same one that made
this class survive pass 21: it has a single singleton, so \(\lvert R\rvert\) is
capped an order of magnitude higher and \(\lvert Z\rvert=\lvert R\rvert-1\) grows
with it, while the requirement \(\mu_1+\mu_2\ge\lvert Z\rvert+t\) grows too.


## r = 29 (partial)

`r29.py` applies the same order-`2r-1` machinery to the five order-57 rows of the
eight-row `r = 29` frontier published at ledger height 2761.  Two of the five
close outright; the other three reduce to explicit high-vertex counts:

| row | after `r29.py` | after `aug57.py` | after `cover57.py` | after `close57.py` |
|---|---|---|---|---|
| (57, 824) | eliminated | eliminated | eliminated | eliminated |
| (57, 825) | eliminated | eliminated | eliminated | eliminated |
| (57, 826) | `\|R\| = 7` | **eliminated** | eliminated | eliminated |
| (57, 827) | `\|R\| in {7,8,9}` | `\|R\| in {8,9}` | `\|R\| = 9` | **eliminated** |
| (57, 828) | `\|R\| in {7,...,11}` | unchanged | `\|R\| in {9,10,11}` | **`\|R\| in {10,11}`** |

Open `(row, |R|)` cases at order 57: **two**, down from nine; and only **one**
row remains.

### Two discarded resources, recovered (`aug57.py`)

`min_split` scores only the clique blocks of the Gallai forest \(L\) induced by
the low vertices, and throws away two things.

**Augmenting a block by \(w_1,w_2\).**  First, the scoring needs no
vertex-disjointness: distinct blocks are *edge*-disjoint, and a crossing between
edges of different blocks is counted in neither, so \(\sum_i\mathrm{cr}(Q_i)\le
\mathrm{cr}(G)\) at once.  (Dropping the "order \(\ge15\)" restriction changes no
number — the minimiser never uses small blocks — but it licenses the next step.)
Since \(N_H(w_i)\subseteq B\), each \(w_i\) is \(G\)-adjacent to *every* vertex of
\(C\), and \(w_1w_2\in E(G)\).  So for any block \(Q_j\),

$$(Q_j\cap C)\cup\{w_1,w_2\}\ \text{is a clique of order}\ q_j-\beta_j+2,\qquad
\beta_j:=|Q_j\cap B|,$$

and its edges lie either inside \(Q_j\) or at \(w_1,w_2\), which are high and so
in no block.  Hence
\(\mathrm{cr}(G)\ge\mathrm{cr}(K_{q_j-\beta_j+2})+\sum_{l\ne j}\mathrm{cr}(Q_l)\).
Since \(T\) is an \(H\)-triangle its vertices are pairwise \(G\)-non-adjacent, so a
clique holds at most one of them; and a \(B\)-vertex in two blocks of order
\(\ge22\) would have degree \(\ge43>28\).  So \(\beta_j\le2\), at most one
\(\beta_j=2\), and \(\sum_j\beta_j\le4\).

**Every low vertex needs block degree.**  A low vertex has \(d_G(v)=28\)
*exactly*, and its neighbours inside \(L\) are exactly the union of its blocks
minus itself, so

$$\sum_{\text{blocks}\ni v}(|Q|-1)\ \ge\ 28-|R|\ =:\ \delta_0 .$$

Two consequences: there is **no isolated vertex** in \(L\) (it would need 28
neighbours inside \(R\)), so \(\mathrm{extra}:=\sum_j q_j-p\ge0\); and any block
with \(q-1<\delta_0\) has all its vertices in a second block, of which there are
at most \(\mathrm{extra}\), so \(q\le\mathrm{extra}\).  At \(|R|=7\) this gives
\(\delta_0=21\), killing the connector-block minimisers such as \((26,23,3)\).

Together these take \((57,826)\) from 7856 to 8343 against \(Z(29)=8281\), and
\((57,827)\) at \(|R|=7\) from 7521 to 8343.  The `plain` column of `aug57.py`
reproduces `r29.py` exactly, which checks the harness.

### Two exact constraints on the block structure (`cover57.py`)

Both ingredients above were being under-used, and sharpening them narrows order
57 much further.  Neither reopens anything: they only ever exclude more.

**The covering form of the degree condition.**  `aug57.py` used only the
consequence that a block with \(q-1<\delta_0\) has all its vertices in a second
block.  That is too weak — it accepts \((25,23,2,2)\) on \(p=49\) with
\(\delta_0=20\), yet the two large blocks cannot share a vertex (its degree would
be \(24+22=46>28\)), so they cover 48 distinct vertices and the 49th can reach
block degree at most \(1+1=2\).  Call a block **big** when \(q-1\ge\delta_0\);
two big blocks cannot share a vertex, since it would have degree \(\ge2\delta_0>28\)
for every \(|R|\le13\).  So the big blocks are disjoint, and every one of the
remaining \(p-\sum_{\mathrm{big}}q_j\) vertices must reach \(\delta_0\) from small
blocks alone:

$$\sum_{\text{small}} q_j(q_j-1)\ \ge\ \delta_0\Bigl(p-\sum_{\text{big}}q_j\Bigr).$$

**\(e(L)\) is bounded above, not only below.**  All the excess sits in \(R\), so
\(\sum_{v\in R}d_G(v)=28|R|+X\) and

$$e(L) \;=\; m-28|R|-X+e(G[R])$$

is an *identity*.  The argument used only \(e(G[R])\ge\) its minimum; but equally
\(e(G[R])\le\binom{|R|}{2}\), and \(e(L)\) is exactly \(\sum_j\binom{q_j}{2}\).
At \(|R|=8\) on row 827 this pins \(e(L)\) into \([555,573]\), while every way of
covering 49 vertices by two disjoint big blocks — \((26,23)\), \((25,24)\),
\((27,22)\), \((28,21)\) — carries at least 576 edges, and fewer big blocks leave
vertices the covering condition cannot supply.  So **no admissible block multiset
exists at all**: the case dies structurally, not by a crossing count.

### The last four cases, pinned (`tsplit57.py`)

Two further exact constraints.  **Constraint E:** \(T\) is an \(H\)-triangle, so
its vertices are pairwise \(G\)-non-adjacent and no two can share a clique block.
Writing \(j:=|T\cap R|\), the \(3-j\) low \(T\)-vertices need pairwise distinct
blocks, and since a vertex lies in at most one big block,

$$3-j \;\;\le\;\; n_{\mathrm{big}} + \Bigl(p-\sum_{\text{big}}q_j\Bigr).$$

**Constraint F:** some pairs inside \(R\) are forced \(G\)-non-edges — the \(j\)
high \(T\)-vertices are pairwise \(H\)-adjacent, each high \(T\)-vertex lying in
\(A_1\cup A_2\) is \(H\)-adjacent to its \(w_i\), and if \(s\) is high it is
\(H\)-adjacent to both \(w_i\).  With \(a:=|A_1|+|A_2|\),

$$e(G[R]) \;\;\le\;\; \binom{|R|}{2}-\binom{j}{2}-\max(0,\,j-3+a)-2\sigma ,$$

and the excess budget forces \(a\ge a_{\min}:=\max(0,|R|+52-X)\).  (The \(j\)-term
must use \(a_{\min}\), not \(j\): a high \(T\)-vertex outside \(A_1\cup A_2\) forces
nothing.)

These do **not** reduce the case count, which stays at four.  What they give is
rigidity: \(j=0\) is impossible in every remaining case, so at least one
\(T\)-vertex is high; and the two \(|R|=9\) cases are pinned to the single
configuration \(j=1\), \(\sigma=0\), block multiset \((24,24)\).  There \(G[L]\) is
exactly two disjoint copies of \(K_{24}\) covering all 48 low vertices with **no**
edges between them, and \(e(G[R])=\binom92-1=35\).

*The opening this creates.*  No \(G\)-edges between the blocks means \(H\supseteq
K_{24,24}\) there, so \(H\) has a 24-edge perfect matching on \(L\) and
\(\theta(H)\le 24+\theta(H[R])=32\).  Four vertex-disjoint triangles \(\{z,u,v\}\)
with \(z\) high and \(u,v\) in different blocks would each replace a matching edge
and absorb a vertex of \(R\), giving \(\theta(H)\le 28\) against \(\theta(H)=29\).
A high \(z\) fails to supply one only if all its \(H\)-neighbours in \(L\) lie in a
single block — and then \(z\) is \(G\)-adjacent to all 24 of the *other* block,
giving a \(K_{25}\).  Since \(|Z|=7\), one alternative has at least four vertices;
in the second, two attach to the same block and are \(G\)-adjacent (only one pair
of \(G[R]\) is missing), giving a \(K_{26}\) disjoint from the other block
augmented by \(w_1,w_2\):
\(\mathrm{cr}(K_{26})+\mathrm{cr}(K_{25})=4724+3997=8721\ge 8281\).
Making the first alternative rigorous needs a system of distinct representatives
for the \(u\) and \(v\); that is the open step.

### The pinned case has no one-sided vertex (`hall57.py`)

The rigidity settles the dichotomy's second branch outright.  Since \(Q_1,Q_2\)
are \(G\)-cliques with no \(G\)-edges between them, \(H[L]\) is **exactly**
\(K_{24,24}\): no \(H\)-edge inside a block, every cross pair an \(H\)-edge.  So
\(e(H[L])=576\), and

$$e_H(L,R) \;=\; e(H)-e(H[L])-e(H[R]) \;=\; \sum_{v\in R}\lvert N_H(v)\cap L\rvert .$$

The two \(w_i\) contribute only \(2+a-\tau\), so nearly all of \(e_H(L,R)=192\)
falls on the seven \(z\in Z\), each capped by its own degree \(28-x_z\).  Seven
terms summing to 188 or 189 with each at most 27 forces every one to be at least
26, and since \(|Q_i|=24\),

$$\min(a_z,b_z) \;\ge\; \lvert N_H(z)\cap L\rvert-24 \;\ge\; 2 .$$

So **every \(z\) is crossing**: there is no one-sided vertex, the clique-building
branch is vacuous, and the case rests entirely on triangle absorption.  (This
holds in every admissible sub-configuration of both rows; for \((57,828)\) with
\(a=1\) the bound is \(\ge3\).)

*What remains, exactly.*  \(\theta(H[L])=24\) is optimal, since \(H[L]\) is
bipartite and triangle-free, so \(\theta(H)\le 24+\theta(H[R])\le 33\).  Four
vertex-disjoint triangles give \(\theta(H)\le 28\) against \(\theta(H)=29\), and
four can be chosen as soon as \(\mu_1+\mu_2\ge|Z|+4=11\), where \(\mu_i\) is the
maximum matching of \(Z\) against \(Q_i\).  König then converts a small \(\mu_1\)
into a large clique: the \(z\) outside the cover are \(G\)-adjacent to all of
\(Q_1\setminus C_Q\), giving a clique of order \(31-\mu_1\) (less one for the
single possible non-edge of \(G[R]\)) disjoint from \(Q_2\):

| \(\mu_1\) | bound | vs \(Z(29)\) |
|---|---|---|
| 2 | \(\mathrm{cr}(K_{28})+\mathrm{cr}(K_{24})=9828\) | closes |
| 3 | \(\mathrm{cr}(K_{27})+\mathrm{cr}(K_{24})=8903\) | closes |
| 4 | \(8081\) | survives |
| 5 | \(7354\) | survives |

and symmetrically in \(\mu_2\).  So the whole residue is
\((\mu_1,\mu_2)\in\{(4,4),(4,5),(5,4),(4,6),(6,4),(5,5)\}: a statement purely
about the bipartite adjacency of seven vertices against two 24-sets.

### That residue is now closed (`close57.py`)

Two facts that were sitting unused finish it.

**\(Z\) is a clique of \(G\).**  For \((57,827)\) the accounting gives
\(\sum_{z\in Z}\lvert N_H(z)\cap R\rvert=1\), so exactly one endpoint of the
single \(H[R]\)-edge lies in \(Z\): the edge runs from \(t^*\) to a \(w_i\), and
**no pair inside \(Z\) is an \(H\)-edge**.  For \((57,828)\), \(e(H[R])=0\) and
\(R\) is a \(G\)-clique outright.  So the "less one vertex for a possible
non-edge" hedge in the König bound is unnecessary, and the clique has order
\(31-\mu_1\), not \(30-\mu_1\).

**Every low vertex has exactly four \(H\)-neighbours in \(R\).**  The blocks
partition \(L\), so a low vertex has exactly 23 \(G\)-neighbours in \(L\), hence
\(28-23=5\) in \(R\), hence \(9-5=4\) \(H\)-neighbours in \(R\).  Therefore
\(e_H(Q_i,R)=24\cdot4=96\), the two summing to 192, which matches \(e_H(L,R)\)
exactly.  Subtracting the \(w\)-contribution,

$$\sum_{z\in Z}a_z \;\ge\; 92, \qquad \sum_{z\in Z}b_z \;\ge\; 92 .$$

Now König bites hard.  A cover \(C_Z\cup C_Q\) of size \(\mu_1\) gives
\(\sum_z a_z\le 24\lvert C_Z\rvert+(7-\lvert C_Z\rvert)\lvert C_Q\rvert\), and
\(a_z\ge2\) forces \(\lvert C_Q\rvert\ge2\) whenever some \(z\) is uncovered.
Maximising over the admissible splits gives at most 14, 36, 58, 80 for
\(\mu_1=2,3,4,5\) — all below 92.  So \(\mu_1\ge6\), symmetrically
\(\mu_2\ge6\), and \(\mu_1+\mu_2\ge12\): at least
\(\mu_1+\mu_2-7\ge5\) vertices of \(Z\) are saturated on both sides, giving
five vertex-disjoint triangles.  Since
\(\theta(H)\le 33-t-e(H[R])\), \(t=4\) suffices for \((57,827)\) (choosing the
four to avoid \(t^*\), so the \(H[R]\)-edge survives) and \(t=5\) for
\((57,828)\); both give \(\theta(H)\le28\), contradicting \(\theta(H)=29\).

**So both \(\lvert R\rvert=9\) cases are impossible.  Row \((57,827)\) is
eliminated, and row \((57,828)\) reduces to \(\lvert R\rvert\in\{10,11\}\).**

### The last row does not follow (`close57b.py`)

The same machinery applied to \((57,828)\) at \(\lvert R\rvert=10,11\) falls
short, and the enumeration says by exactly how much.

The per-block identity generalises cleanly: every low vertex has
\(\lvert N_H(v)\cap R\rvert=\lvert R\rvert-28+D_v\) with
\(D_v:=\sum_{\text{blocks}\ni v}(\lvert Q\rvert-1)\), so

$$e_H(Q,R) \;=\; q(\lvert R\rvert-28)+\sum_{v\in Q}D_v \;\ge\; q\bigl(q+\lvert R\rvert-29\bigr).$$

This matters: the crude aggregate bound
\(\sum_z a_z\ge e_H(L,R)-\lvert Z\rvert\lvert L\setminus Q_1\rvert\) gives 26
where the per-block truth is 145.

The contradiction now needs \(t+\nu\ge\chi(G[L])+\lvert R\rvert-28\) absorptions,
and \(t\) of them exist once \(\mu_1+\mu_2\ge\lvert Z\rvert+t\).  Running **every**
admissible multiset — not just the crossing-minimiser — and every
\((a,j,\sigma)\) with every split of
\(c:=\sum_i\lvert N_H(w_i)\cap L\rvert\):

| \(\lvert R\rvert\) | tightest multiset | \(\chi(G[L])\) | \(t\) needed | \(\mu_1+\mu_2\ge\) | needed | short by |
|---|---|---|---|---|---|---|
| 10 | \((24,23)\) | 24 | 2 | 9 | 10 | **1** |
| 11 | \((24,22)\) | 24 | 2 | 10 | 11 | **1** |
| 10 | \((25,22)\) | 25 | 5 | 9 | 13 | 4 |
| 11 | \((25,21)\) | 25 | 3 | 10 | 12 | 2 |

So the row stays open, short by exactly one unit of \(\mu\) in the tightest
cases.  The reason is structural, not arithmetic: at \(\lvert R\rvert=9\) the two
blocks *partitioned* \(L\) and every \(z\) was forced to be crossing, which is
what drove \(\mu_1,\mu_2\ge6\).  Here \(\lvert Z\rvert\) is larger, \(\lvert
L\rvert\) smaller, and neither is forced.  A block of order 25 is *worse*, not
better, because \(\chi(G[L])=25\) raises the absorptions needed faster than the
larger block raises \(\mu_1\).

Order 58 = 2r is **not** covered by this argument: there Stehlík gives one colour
class of size three rather than a perfect matching, so `H` need not be
factor-critical and none of the order-\(2r-1\) structure theory applies; it is
handled separately above.  This does not prove Albertson's conjecture for
`r = 29`.

## What this does not do

For `r = 29` see the partial section above: two of the five order-57 rows close,
and order 58 is untouched.  Nothing here bears on `r >= 30`.

## Files and reproduction

| file | what it is |
|---|---|
| `r27.py` | **the r = 27 elimination** |
| `r28.py` | **the r = 28 proof (order reduction + both rows)** |
| `r29.py` | the partial r = 29 result at order 57 |
| `deps.py` | the dependency reduction and the Corollary 5 simplification |
| `order2r.py` | the order-2r non-domination lemma and order 58 at r = 29 |
| `gallai.py`, `gallai_split.py` | the redundant routes for `\|R\| = 2..6` |
| `frontier.py` | the `r = 27` single-row frontier and the surviving configuration |
| `recursive.py` | recursive integer-aware sampling bound `L(n,q)` |
| `EXPECTED_OUTPUT_FRONTIER.txt` | its expected output |
| `verify_range.py` | the barrier classification and forced-degree theorem |
| `EXPECTED_OUTPUT_RANGE.txt` | its expected output |
| `verify.py` | the first, weakest form (dichotomy at two `r=28` rows) |
| `EXPECTED_OUTPUT.txt` | its expected output |

```
PYTHONDONTWRITEBYTECODE=1 python3 r27.py          | diff -u EXPECTED_OUTPUT_R27.txt -
PYTHONDONTWRITEBYTECODE=1 python3 r28.py          | diff -u EXPECTED_OUTPUT_R28.txt -
PYTHONDONTWRITEBYTECODE=1 python3 r29.py          | diff -u EXPECTED_OUTPUT_R29.txt -
PYTHONDONTWRITEBYTECODE=1 python3 deps.py         | diff -u EXPECTED_OUTPUT_DEPS.txt -
PYTHONDONTWRITEBYTECODE=1 python3 order2r.py      | diff -u EXPECTED_OUTPUT_ORDER2R.txt -
PYTHONDONTWRITEBYTECODE=1 python3 gallai.py       | diff -u EXPECTED_OUTPUT_GALLAI.txt -
PYTHONDONTWRITEBYTECODE=1 python3 gallai_split.py | diff -u EXPECTED_OUTPUT_GALLAI_SPLIT.txt -
PYTHONDONTWRITEBYTECODE=1 python3 frontier.py     | diff -u EXPECTED_OUTPUT_FRONTIER.txt -
PYTHONDONTWRITEBYTECODE=1 python3 verify_range.py | diff -u EXPECTED_OUTPUT_RANGE.txt -
PYTHONDONTWRITEBYTECODE=1 python3 verify.py       | diff -u EXPECTED_OUTPUT.txt -
shasum -a 256 -c SHA256SUMS
```

Expected: empty diffs, `SOUNDNESS CONTROLS: PASS` in both scripts, the four-row
`r = 27` RESULT line, the four `SUMMARY` lines for each recursion base, and OK
for every hash.  Tested with CPython
3.13.15 (macOS, arm64); standard library only; `verify_range.py` runs in about
25 seconds and `verify.py` in under a second.

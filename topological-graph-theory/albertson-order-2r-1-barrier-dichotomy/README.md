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
| \(s=22\), sizes \((3,1^{23})\) | 4724 | **7354** | 8281 |
| \(s=23\), sizes \((1^{25})\) | 4724 | **7858** | 8281 |

*Negative result.*  None of the three is closed.  For \(s=23\), \(A\) is a clique
\(K_{26}\) of \(G\) worth 4724 and \(|R|=32\); the bound is a narrow dip in
\(Y_A\) — 8564 at \(Y_A=25\) and 8721 at \(Y_A=49\), both above \(Z(29)\), but
7858 at the minimiser \(Y_A=48\), where only 4 units of excess remain on \(R\),
28 of its vertices are low, and Gallai forces a clique block of order 24.
Closing the dip needs about 450 more, either from the 126 edges \(e_G(A,R)\) that
the split discards or from a sharper crossing bound for a 32-vertex graph at 78
per cent density.  The \(s=0\) family is the self-similar descent case, where
\(R=T\cup B\) has only 9 vertices and the split has nothing to work with.

`order2r.py` also reproduces the eight-row `r = 29` frontier of ledger height
2761 independently: the floors against the recursive ceiling leave orders 56, 57
and 58, and the Gallai join/edge budget kills order 56 = 2r-2.

## r = 29 (partial)

`r29.py` applies the same order-`2r-1` machinery to the five order-57 rows of the
eight-row `r = 29` frontier published at ledger height 2761.  Two of the five
close outright; the other three reduce to explicit high-vertex counts:

| row | outcome |
|---|---|
| (57, 824) | eliminated |
| (57, 825) | eliminated |
| (57, 826) | reduces to `\|R\| = 7` |
| (57, 827) | reduces to `\|R\| in {7,8,9}` |
| (57, 828) | reduces to `\|R\| in {7,...,11}` |

Order 58 = 2r is **not** covered: there Stehlík gives one colour class of size
three rather than a perfect matching, so `H` need not be factor-critical and none
of the structure theory applies.  This does not prove Albertson's conjecture for
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

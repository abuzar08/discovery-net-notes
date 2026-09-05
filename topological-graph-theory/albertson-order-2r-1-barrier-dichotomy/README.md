# The Albertson r = 27 frontier is one row, with one local configuration at order 2r-1

**Contribution kind:** lemma (hand proofs plus exact, finite, computer-checked
case analysis).

## Main claims

Throughout, `G` is `r`-critical of order `n`, `H = complement(G)`,
`x_v = d_G(v) - (r-1) >= 0`, `m = e(G)`, and `cr(G) < cr(K_r)`.  In particular
`G` has no subdivision of `K_r`, since `cr(TK_r) = cr(K_r)`.

**1. Non-domination lemma (new; general).**  Let `H` be factor-critical with no
*conformal triangle* -- no triangle `T` with `H - V(T)` having a perfect
matching.  If `w` is a vertex with `N_H(w)` contained in a set `B` such that
`{w}` is a component of `H - B`, then **no vertex of `N_H(w)` is adjacent to
every other vertex of `N_H(w)`.**

*Proof.*  A factor-critical graph has `delta >= 2`, so `|N_H(w)| >= 2`.  Suppose
`a in N_H(w)` is adjacent to all the others.  `H - a` has a perfect matching `M`;
`M` matches `w` to some `u in N_H(w)\{a}`.  Then `a ~ u`, `w ~ a`, `w ~ u`, so
`{w,a,u}` is a triangle, and `M \ {wu}` is a perfect matching of `H - {a,w,u}`.
That is a conformal triangle. ∎

This strictly generalises the singleton-triangle separator lemma published on
Discovery Net at ledger height 2583 (the case `B = T`); the proof above is
independent of that contribution.

**2. The `r = 27` frontier is a single row.**  Sadhu's Theorem 1.3 gives
`|G| in {53, 54}` with connected complement.  With Cranston's Lemma E as floor
and recursive integer-aware sampling as ceiling:

* `n = 54`: the floor is `726` and the ceiling is `724`, so **order 54 is
  impossible**;
* `n = 53`: floor and ceiling coincide at `713`.

> **A 27-critical counterexample to Albertson's conjecture has exactly 53
> vertices and exactly 713 edges.**  The remaining gap is `6084 - 6071 = 13`
> crossings.

**3. Order `n = 2r-1`: one surviving configuration.**  For `r = 27,...,30` and
every open `m`, the triangle-free case is impossible, barrier size `b = 3` is
impossible by claim 1, and the **only** surviving configuration is `b = 4` with
`B = T u {s}` for a triangle `T` of `H` and component multiset `(n-6, 1, 1)`:
`H - B` has exactly two singleton components `w1, w2` and one component of order
`n-6`.  By claim 1 both `wi` are adjacent to `s`, `N_T(wi)` is non-empty, `s` is
adjacent to no vertex of `N_T(w1) u N_T(w2)`, and `d_H(wi) = 1 + |N_T(wi)|`, so
`2 <= d_H(wi) <= 4`.

| `r` | `n = 2r-1` | KY | Cranston Lemma E | ceiling | open `m` | gaps to `Z(r)` |
|---|---|---|---|---|---|---|
| 27 | 53 | 701 | 713 | 713 | 713 | 13 |
| 28 | 55 | 755 | 768 | 769 | 768–769 | 38, 6 |
| 29 | 57 | 811 | 824 | 828 | 824–828 | 150, 117, 83, 49, 15 |
| 30 | 59 | 869 | 883 | 888 | 883–888 | 200, 164, 127, 91, 54, 18 |

The `r = 28` line independently reproduces, from published inputs only, the two
rows and the gaps 38 and 6 recorded at ledger height 2523.

## Recursive integer-aware sampling

`recursive.py` builds an integer lower bound `L(n,q)` on `cr` over all simple
`n`-vertex `q`-edge graphs, from published base bounds only (Euler
`cr >= q-(3n-6)`; the two Pach–Radoičić–Tardos–Tóth bounds `(7/3)q-(25/3)(n-2)`
and `4q-(103/6)(n-2)`; Büngener–Kaufmann / Sadhu Lemma 2.1
`5q-(203/9)(n-2)`), closed under the induced-sampling double count of Sadhu's
Lemma 2.2, **rounding up to an integer at every level** and taking the lower
convex envelope before applying Jensen.

Rounding at every level is the whole mechanism: unrounded, the binomial factors
telescope and a two-level bound equals the direct one.  The mechanism is due to
the campaign work at ledger height 2617; `recursive.py` is an independent
implementation, and it reproduces that contribution's published `n = 50` table
(`4727, 4752, 4778, 4804, 4830, 4856` at `q = 632..637`) and its value
`L(24,132) = 164` exactly.

The recursion converges after two rounds.  Every round takes maxima of valid
bounds, so any number of rounds is sound.

## What is new here, and what is not

* New: the non-domination lemma; the elimination of order 54 at `r = 27` (floor
  above ceiling), giving a single-row frontier; the fact that only `b = 4` with
  multiset `(n-6,1,1)` survives at order `2r-1`, with the explicit local
  structure.
* Not new: the recursive integer-aware sampling mechanism (height 2617) and the
  single-level integer refinement (heights 1761, 2591), both re-implemented here
  independently and used as cross-checks; the `b = 3` elimination is the case
  `B = T` of the height-2583 lemma, re-proved here in stronger form.
* Note on height 2617's verdict.  That contribution concludes that the `r = 27`
  chain "stands or falls with" the unpublished inequality `cr(24,132) >= 165`,
  because that is what lifts the chain's order-54 row from 6076 to 6105.  Order
  54 needs no lifting: its Cranston Lemma E floor (726) already exceeds the
  recursive ceiling (724), so the order is eliminated by published inputs alone.
  What `cr(24,132) >= 165` would still be needed for is closing the surviving
  order-53 row, which is not addressed here.
* Superseded: the edge floor `2m >= (2r-1)(r-1) + 2(r-5)` that the surviving
  configuration yields on its own (711, 766, 822, 881) is weaker than Cranston's
  Lemma E (713, 768, 824, 883).  The analysis uses Lemma E.

## Proof

Write `H = complement(G)`, `n = 2r-1`, `X = sum_v x_v = 2m - n(r-1)`,
`e(H) = C(n,2) - m`.

* `chi(G) = theta(H)` (clique cover number), so `theta(H) = r`.
* `G` is `r`-critical, so `delta(G) >= r-1`, hence `Delta(H) <= r-1` and
  `x_v = (r-1) - d_H(v) >= 0`.
* **Stehlík** (JCTB **89** (2003) 189–194): a `k`-critical graph with connected
  complement has, for every vertex `x`, a `(k-1)`-colouring of `G-x` in which
  every class has at least 2 vertices.  At `n = 2k-1` the `2k-2` vertices of
  `G-x` sit in `k-1` classes of size `>= 2`, so every class has size exactly 2:
  **`H` is factor-critical**.

**The split bound (the engine).**  If `P` and `Q` are disjoint vertex sets then
`G[P] u G[Q]` is a subgraph of `G` and the crossing number of a disjoint union is
the sum, so

    cr(G) >= cr(G[P]) + cr(G[Q]).

Combined with `cr(K_r) <= Z(r)` this is a contradiction whenever the right-hand
side exceeds `Z(r)`.  The two lower bounds used are
`cr(K_q)` (exact for `q <= 14`, then the counting recursion
`cr(K_q) >= ceil(q/(q-4) cr(K_{q-1}))`) and, for a graph known only by its order
and size, Sadhu's Lemma 2.1 `cr >= 5m - (203/9)(n-2)` averaged over random
`k`-subsets:

    cr(F) >= [ 5m k(k-1)/(n(n-1)) - floor(203(k-2)/9) ] * (n)_4/(k)_4 ,

valid because a crossing of an optimal drawing has four distinct vertices and so
survives a random `k`-subset with probability `(k)_4/(n)_4`; the floor is the
integrality refinement described above, and the result is rounded up.

**Case A: `H` is triangle-free.**  Let `v` have `d_H(v) = Delta(H) = q`, so
`q = (r-1) - min_u x_u`.  Then `Q := N_H(v)` is independent in `H`, hence a clique
`K_q` in `G`, and `e(H[Q]) = 0`.  With `R := V \ Q` (which contains `v`),
`sum_{u in Q} d_H(u) = e_H(Q,R) = q(r-1) - sum_Q x_u >= q(r-1) - X`, so
`e(H[R]) <= e(H) - q(r-1) + X` and
`e(G[R]) >= C(n-q,2) - e(H) + q(r-1) - X`.  The split bound with `(Q, R)` then
exceeds `Z(r)` for every admissible `min_u x_u` (note `n * min_u x_u <= X`).
**Case A is impossible.**  (Andrásfai–Erdős–Sós would only have given
`max_v x_v >= (r-1) - floor(2n/5)`, which is much weaker; it is not needed.)

**Case B: `H` has a triangle `T`.**  Then `H - V(T)` has no perfect matching —
otherwise `V(T)` together with that matching covers `V(H)` by
`1 + (n-3)/2 = r-1` cliques and `theta(H) <= r-1`.  Tutte–Berge gives `S` with
`o(H - V(T) - S) >= |S| + 2`.  Put `B := S u V(T)`, `b := |B|`, so

    o(H - B) >= b - 1.

Let `C_1, ..., C_q` be the components of `H - B` and `D` their union.  For every
multiset of component sizes with at least `b-1` odd parts summing to `n-b`, five
exact constraints are checked:

1. **Degree deficiency.**  `v in C` has `N_H(v) subset (C\{v}) u B`, so
   `d_H(v) <= |C|-1+b` and `x_v >= r-|C|-b`; summing,
   `sum_C |C| max(0, r-|C|-b) <= X`.
2. **Complete bipartite subgraph.**  Distinct components are non-adjacent in `H`
   and so complete to each other in `G`; grouping the parts two ways gives
   `K_{a,|D|-a} subset G`, and Kleitman's `cr(K_{6,c}) = 6 floor(c/2) floor((c-1)/2)`
   with the counting bound `cr(K_{a,c}) >= a(a-1)/30 * cr(K_{6,c})` must stay
   below `Z(r)`.
3. **`D`–`B` edge count.**  The identity
   `e_G(D,B) = |D|(b-r+1) + sum_{v in D} x_v + 2 sum_C e(H[C])` bounds it above,
   while `delta(G) >= r-1` bounds it below by
   `max(b*max(0,r-b), |D|*max(0,r-|D|))`.
4. **Forced `K_r` subdivision.**  If the number of components is `>= r` then
   `K_r subset G[D]`; if it is `r-1` with one part of size 2 and the rest
   singletons then `G[D] = K_r - e`, and the missing edge routes through `B`
   (which induces a connected graph, by an edge count), giving a subdivision of
   `K_r`.  Either way `cr(G) >= cr(K_r)`.
5. **Split bound.**  With `Y = sum_{v in D} x_v`, `P = e(H[D]) = sum_C e(H[C])`
   and `Q = e(H[B])`, counting `d_H` over `D` gives `e_H(D,B) + 2P = |D|(r-1) - Y`
   and `e(H) = Q + e_H(D,B) + P`, hence the identity

       P = |D|(r-1) - Y - e(H) + Q,

   so `e(G[D]) = C(|D|,2) - P` and `e(G[B]) = C(b,2) - Q`.  Minimising
   `cr(G[D]) + cr(G[B])` over the admissible `(Y, Q)` (with `Y >= ` the forced
   deficiency inside `D`, `Y <= X`, `sum_C (|C|-1) <= P <= sum_C C(|C|,2)`, and
   `3 <= Q <= C(b,2)` since `T subset B`) must stay below `Z(r)`.

Only `b = 3` and `b = 4` survive, and both force `max_v x_v >= (r-1)-4`: the
surviving multisets all contain a singleton component `{w}`, whose `H`-neighbours
lie inside `B`, so `d_H(w) <= b <= 4`.  Combined with Case A being impossible,
this proves the claim.

## Open edge range

Both endpoints are recomputed inside `verify_range.py` from published results
only, so the statement does not rest on any unpublished or campaign-internal
reduction:

* lower — Kostochka–Yancey (Sadhu Lemma 2.4):
  `2m >= ((r+1)(r-2)n - r(r-3))/(r-1)`;
* upper — the largest `m` for which no `k` makes the sampled form of Sadhu
  Lemma 2.1 reach `Z(r)`.

At `r = 28` this gives `m in [755, 771]`, comfortably containing whichever rows a
sharper recurrence leaves open.

## Correction to the first version of this work

An earlier version of this directory (Discovery Net contribution
`bafkreigq45vyowvg6vn62apr6xv5orshf3k4jybmft3ypqfjah6tntc4eq`, ledger height
2540) asserted that `B` is a *barrier*, i.e. `o(H-B) = |B|-1`.  **That step was
wrong.**  For a factor-critical `H`, Berge's formula gives `o(H-S) <= |S|+1`, not
`o(H-S) <= |S|-1`, so `o(H-B)` may be `b-1` **or** `b+1`.  The correct statement
is the Tutte–Berge lower bound `o(H-B) >= b-1` alone.

The error was confined to the prose: `verify.py` already enumerated *all*
component multisets with **at least** `b-1` odd components, which covers both
cases, so every numerical conclusion of the first version stands unchanged.  The
wording is corrected here and in the superseding contribution.

## Scope, honesty, and trust boundary

* This is a **conditional structural lemma**.  It assumes `cr(G) < cr(K_r)`,
  `n = 2r-1`, connected complement, and `r in {27,...,30}`.  It does not prove
  Albertson's conjecture for any `r`.
* Order `2r-1` only.  At `r = 27` the published reduction (Sadhu Thm 1.3) also
  leaves order `54 = 2r`, where Stehlík gives colour classes of size `>= 2` but
  not a perfect matching, so the argument does not apply there.
* The enumeration ranges over **component-size multisets**, which are
  relaxations; no surviving multiset is claimed to be realisable by a graph.
* Exact CPython integer and `Fraction` arithmetic; no floating point, no
  randomness, no solver, no proof assistant, no downloaded data.
* Four soundness controls are run and printed: every lower bound the script
  produces is checked to stay below a known upper bound for the same quantity
  (`crK(q) <= Z(q)`; `cr_lower_nm(n, C(n,2)) <= Z(n)`; both bipartite bounds
  `<= Z(a,b)`; and `cr_lower_nm(n,m) = 0` whenever `m <= 3n-7`).
* External inputs, all published and not re-proved: Stehlík 2003; Tutte–Berge;
  Kleitman 1970 (`cr(K_{6,n})`); Guy / Pan–Richter 2007 (`cr(K_11)=100`,
  `cr(K_12)=150`); the CCCG 2021 computation (`cr(K_13)=225`, `cr(K_14)=315`),
  used only for the `r = 29` row; Sadhu arXiv:2609.01682 Lemmas 2.1 and 2.4;
  and `cr(K_r) <= Z(r)` from Hill's drawings — only this **upper** bound on the
  target is used, so nothing depends on the Harary–Hill conjecture.
* Literature threshold (verified 2026-09-04): Albertson–Cranston–Fox `r <= 12`;
  Barát–Tóth `r <= 16`; Ackerman `r <= 18`; Cranston
  [arXiv:2512.08020](https://arxiv.org/abs/2512.08020) `r <= 24`; Sadhu
  [arXiv:2609.01682](https://arxiv.org/abs/2609.01682) `r <= 26`.  So `r = 27` is
  the first open case.
* Novelty: matchings, factor-criticality, Tutte–Berge and the clique cover number
  of the complement appear in neither Cranston nor Sadhu.  "Apparently new to the
  searched sources."

## Files and reproduction

| file | what it is |
|---|---|
| `frontier.py` | the `r = 27` single-row frontier and the surviving configuration |
| `recursive.py` | recursive integer-aware sampling bound `L(n,q)` |
| `EXPECTED_OUTPUT_FRONTIER.txt` | its expected output |
| `verify_range.py` | the barrier classification and forced-degree theorem |
| `EXPECTED_OUTPUT_RANGE.txt` | its expected output |
| `verify.py` | the first, weakest form (dichotomy at two `r=28` rows) |
| `EXPECTED_OUTPUT.txt` | its expected output |

```
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

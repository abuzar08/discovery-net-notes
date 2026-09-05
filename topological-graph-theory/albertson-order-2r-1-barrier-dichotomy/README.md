# A matching-barrier dichotomy for Albertson counterexamples of order 2r-1

**Contribution kind:** lemma (exact computer-assisted case analysis over a finite,
explicitly enumerated set of configurations; the surrounding argument is a
hand proof).

**Claim.** Let `r >= 5` and let `G` be an `r`-critical graph of order `n = 2r-1`
whose complement `H` is connected, and suppose `cr(G) < cr(K_r)`.  Put
`x_v = d_G(v) - (r-1) >= 0`.  Then, for the frontier edge rows listed below,

> **`max_v x_v >= 5`   or   `omega(G) >= r-2`.**

Concretely:

| `r` | `n` | `e(G)` | conclusion |
|---|---|---|---|
| 28 | 55 | 768, 769 | `max_v (d_G(v)-27) >= 5` or `omega(G) >= 26` |
| 27 | 53 | 713, 714, 715, 716 | `max_v (d_G(v)-26) >= 5` or `omega(G) >= 25` |

The second alternative also comes with rigid extra structure (see "Surviving
configurations" below): the whole of `G` splits as a complete multipartite part
`D` on `n-b` vertices and a barrier `B` of size `b in {r-1, r}`, with at most
`e_G(D,B) <= 80` edges between them.

Why this matters: the surviving row at `r = 28` is `n = 55`, `e(G) in {768,769}`,
and the state of the art there is an enumeration over *excess degree profiles*
`(x_v)` with `sum_v x_v = 51` resp. `53`.  The dichotomy deletes every profile
with `max_v x_v <= 4` — in particular the extremal flat profiles `0^4 1^51` and
`0^28 1 2^26` — unless the counterexample contains a clique on `r-2` of its
`2r-1` vertices.

## Setting and known inputs

Albertson's conjecture: `chi(G) >= r  =>  cr(G) >= cr(K_r)`.  Verified for
`r <= 12` (Albertson–Cranston–Fox), `r <= 16` (Barát–Tóth), `r <= 18`
(Ackerman), `r <= 24` (Cranston, [arXiv:2512.08020](https://arxiv.org/abs/2512.08020)),
and `r <= 26` (Sadhu, [arXiv:2609.01682](https://arxiv.org/abs/2609.01682)).
Sadhu's Theorem 1.3: a 27-critical `G` with `cr(G) < cr(K_27)` has
`|G| in {53,54}` and connected complement.  So `r = 27` is the first open case
and `n = 2r-1` is one of its two orders; `n = 2r-1` is also the exceptional
order in Cranston's Lemma D (the edge bound `|E| >= n(r-1)/2 + (r-3)` is stated
only for `n != 2r-1`).

External results used, all published:

1. **Gallai / Stehlík.** M. Stehlík, *Critical graphs with connected complements*,
   J. Combin. Theory Ser. B **89** (2003) 189–194: if `G` is `k`-critical with
   connected complement then for every vertex `x` the graph `G-x` has a
   `(k-1)`-colouring in which **every colour class has at least 2 vertices**.
   At `n = 2k-1` the `2k-2` vertices of `G-x` fall into `k-1` classes of size
   `>= 2`, so every class has size exactly 2, i.e. **`H - x` has a perfect
   matching for every `x`: `H` is factor-critical.**
2. **Tutte–Berge.** If a graph `F` has no perfect matching there is `S` with
   `o(F-S) >= |S|+2`.
3. **Andrásfai–Erdős–Sós.** A triangle-free graph on `n` vertices with
   `delta > 2n/5` is bipartite.
4. **Kleitman (1970).** `cr(K_{6,c}) = 6*floor(c/2)*floor((c-1)/2)`.
5. `cr(K_r) <= Z(r) = (1/4) floor(r/2) floor((r-1)/2) floor((r-2)/2) floor((r-3)/2)`
   (Hill's drawings).  Only the **upper** bound on the target is used, so the
   argument does not depend on the Harary–Hill conjecture.

## The argument

Write `H = complement(G)`, `n = 2r-1`.

* `chi(G) = theta(H)`, the clique cover number, so `theta(H) = r`.
* `G` is `r`-critical, so `delta(G) >= r-1`, hence `Delta(H) <= n-1-(r-1) = r-1`
  and `x_v = (r-1) - d_H(v) >= 0`.
* `X := sum_v x_v = n(r-1) - 2 e(H) = 2 e(G) - n(r-1)`.  For `(r,e(G)) = (28,768)`
  this is `51`; for `(28,769)` it is `53`.

**Branch 1: `H` is triangle-free.**  A factor-critical graph of odd order is not
bipartite (if `H` were bipartite with parts `P, Q`, `|P| > |Q|`, then `H-v` for
`v in Q` is an unbalanced bipartite graph and has no perfect matching).  So by
Andrásfai–Erdős–Sós `delta(H) <= floor(2n/5)`, i.e.
`max_v x_v >= (r-1) - floor(2n/5)`.  For `n = 55` and `n = 53` this is `5`.

**Branch 2: `H` has a triangle `T`.**  If `H - V(T)` had a perfect matching then
`{V(T)}` together with that matching would be `1 + (n-3)/2 = r-1` disjoint
cliques covering `V(H)`, giving `theta(H) <= r-1`, contradiction.  So `H-V(T)`
has no perfect matching; take `S` from Tutte–Berge and set `B := S u V(T)`,
`b := |B| = |S|+3`.  Then `o(H-B) >= |S|+2 = b-1`, and since `H` is
factor-critical `o(H-B) <= b-1`, so **`B` is a barrier: `o(H-B) = b-1`**.

Let `C_1, ..., C_q` be the components of `H-B` (`q >= b-1`) and `D` their union,
`|D| = n-b`.  Four exact constraints are then imposed and checked by machine for
every possible multiset of component sizes:

1. **Degree deficiency.**  For `v in C`, `N_H(v) subset (C\{v}) u B`, so
   `d_H(v) <= |C|-1+b` and `x_v >= r-|C|-b`.  Summing,
   `sum_C |C| * max(0, r-|C|-b) <= X`.
2. **Crossing number.**  Distinct components are non-adjacent in `H`, hence
   complete to each other in `G`.  So `G[D]` is a complete multipartite graph;
   grouping the parts into two sides `a` and `|D|-a` gives
   `K_{a,|D|-a} subset G`, and the Kleitman counting bound
   `cr(K_{a,c}) >= binom(a,6)/binom(a-2,4) * cr(K_{6,c}) = a(a-1)/30 * cr(K_{6,c})`
   must not exceed `Z(r)`.
3. **`D`–`B` edge count.**  Exactly
   `e_G(D,B) = |D|(b-r+1) + sum_{v in D} x_v + 2 sum_C e(H[C])`, so
   `e_G(D,B) <= |D|(b-r+1) + X + 2 sum_C binom(|C|,2)`.  On the other hand
   `delta(G) >= r-1` forces `e_G(u,D) >= r-b` for every `u in B` and
   `e_G(v,B) >= r-|D|` for every `v in D`, so
   `e_G(D,B) >= max(b*max(0,r-b), |D|*max(0,r-|D|))`.
4. **Forced `K_r` subdivision.**  If `q >= r` then `G[D] contains K_r`.  If
   `q = r-1` with one part of size 2 and the rest singletons, then `G[D] = K_r - e`
   with missing edge `xy`; both `x` and `y` have `d_G >= r-1` but only `r-2`
   neighbours in `D`, hence a neighbour in `B`, and
   `e(G[B]) >= (b(r-1) - e_G(D,B))/2 > binom(b-1,2)` forces `G[B]` connected, so
   an `x`–`y` path through `B` completes a subdivision of `K_r`.  Either way
   `cr(G) >= cr(K_r)`, a contradiction.

`verify.py` enumerates all configurations for every `b` from 3 to `n` and applies
1–4.  Every `b` with `6 <= b <= r-3` is killed by 1 alone; `b = r-3, r-2` by 3;
`b = 5` by 2.  What is left is exactly `b in {3, 4, r-1, r}`.

### Surviving configurations (r = 28, n = 55, e(G) = 768)

| `b` | component sizes of `H-B` | forced `max_v x_v` | forced `omega(G)` | `e_G(D,B) <=` |
|---|---|---|---|---|
| 3 | `(51,1)`, `(50,1,1)` | 24 | 2 | 1353 |
| 4 | `(49,1,1)` | 23 | 3 | 1230 |
| 27 | `(3,1^25)` | 0 | 26 | 57 |
| 28 | `(1^27)` | 0 | 27 | 78 |

Branches `b = 3, 4` already give `max_v x_v >= 23`; branches `b = 27, 28` give
`omega(G) >= 26`.  Together with Branch 1 (`max_v x_v >= 5`) this proves the
claim.

## Scope, honesty, and what this does *not* do

* This is a **conditional structural lemma**, not progress on Albertson's
  conjecture by itself.  It assumes `cr(G) < cr(K_r)`, `n = 2r-1`, connected
  complement, and one of the listed edge counts, and derives a dichotomy.
* The hypothesis `n = 55` for `r = 28` and `n in {53,54}` for `r = 27` comes
  from the published order cutoffs; the edge rows `768/769` (`r=28`) and
  `713..716` (`r=27`) are the ones the current frontier leaves open.  The lemma
  is stated for exactly those rows; the script recomputes everything from
  `(r, e(G))` and can be rerun for any other row.
* Branches `b = r-1` and `b = r` are *not* closed here.  In them `G` is
  `K_{r-2}` or `K_{r-1}` plus a barrier of `r-1` or `r` vertices with at most
  57–80 edges in between, and `e(G[B]) >= binom(b,2) - 39`; closing them looks
  like a `K_r`-subdivision linkage problem and is the obvious next step.
* Trust boundary: exact Python integer arithmetic only (no floats, no solver, no
  randomness).  The five external results above are taken from the literature
  and are not re-proved.  The enumeration is over *component-size multisets*,
  which are relaxations — they are not asserted to be realizable graphs.
* Novelty: matchings, factor-criticality, Tutte–Berge barriers and the clique
  cover number of the complement do not appear in Cranston (arXiv:2512.08020)
  or in Sadhu (arXiv:2609.01682).  "Apparently new to the searched sources."

## Reproduction

```
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
shasum -a 256 -c SHA256SUMS
```

Expected: no diff, and the final lines

```
RESULT r=28 n=55 m=768:  max_v (d_G(v)-(r-1)) >= 5   OR   omega(G) >= 26
RESULT r=28 n=55 m=769:  max_v (d_G(v)-(r-1)) >= 5   OR   omega(G) >= 26
```

Tested with CPython 3.13 (macOS, arm64); the script uses only the standard
library and runs in under a second.

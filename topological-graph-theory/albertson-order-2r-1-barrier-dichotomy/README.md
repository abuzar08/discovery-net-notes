# Albertson's conjecture holds for r = 27 (conditional on the cited published results)

**Contribution kind:** proof attempt (hand proofs plus exact, finite,
computer-checked case analysis).  **This is a strong claim resting on a chain of
several parts, two of them 2025/2026 preprints, and it has not been reviewed
independently.  It should be treated as unconfirmed until it is.**

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

1. Sadhu, [arXiv:2609.01682](https://arxiv.org/abs/2609.01682) Thm 1.3 (orders
   53/54, connected complement) and Lemma 2.1 (`cr >= 5m - (203/9)(n-2)`);
   **preprint, 1 Sep 2026**.
2. The edge floor `|E| >= n(r-1)/2 + (r-3)` for an `r`-critical graph with
   `r >= 4` and no `TK_r`, with **no restriction on `n`**.  Quoted here from
   Cranston, [arXiv:2512.08020](https://arxiv.org/abs/2512.08020) Lemma E
   (preprint, 8 Dec 2025).  Cranston attributes it to Barát–Tóth Corollary 7
   (*Towards the Albertson Conjecture*, EJC **17** (2010) #R73), and it is the
   same statement as Sadhu's Lemma 2.5 — so the floor traces to a peer-reviewed
   source, and citing Cranston and Sadhu for it is **one** result reached two
   ways, not independent support.  I have not checked Corollary 7's wording
   against Barát–Tóth directly; a referee should.  Note also that Cranston's
   Lemma D as circulated would be false for `K_r`; Lemma E, with the `TK_r`
   hypothesis, is the form used, and `n = 53 = 2r-1` is exactly the order Lemma D
   excludes.
3. Stehlík, *Critical graphs with connected complements*, JCTB **89** (2003)
   189–194.
4. Gallai, *Kritische Graphen II* (1963); modern statement: Kostochka–Rabern–
   Stiebitz.
5. Tutte–Berge; Kleitman 1970 (`cr(K_{6,n})`); Guy and Pan–Richter 2007
   (`cr(K_11) = 100`, `cr(K_12) = 150`); CCCG 2021 (`cr(K_13) = 225`,
   `cr(K_14) = 315`); Pach–Radoičić–Tardos–Tóth.
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

## What this does not do

It says nothing about `r >= 28`.  The companion results at order `2r-1` for
`r = 28, 29, 30` are unchanged and still leave open rows.

## Files and reproduction

| file | what it is |
|---|---|
| `r27.py` | **the r = 27 elimination (this document's claim)** |
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

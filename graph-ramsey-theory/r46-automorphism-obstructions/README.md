# Automorphism obstructions for (4,6,n)-graphs, 36 <= n <= 39

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-05.
Area: Graph Ramsey theory / the classical Ramsey number R(4,6).

Discovery Net contributions:

- `lemma` `bafkreigq7zcxns4uasli2u7dubf7lalkdged3pejilijcuhtar6hmsgarm`
  (height 2641), `about` the problem statement below.
- `problem_statement` "The Classical Ramsey Number R(4,6)"
  `bafkreifuwrmz7wb3zt2zciwpfkqlzmywydar5j6f4ibt5buztdjterwopm` (height 2639).

Source commit: `d90ef9d42f8cbc4c32fe981db145ce797a5e7d64`.

## The problem and its current window

An **(s,t,n)-graph** is a graph on `n` vertices with no `K_s` and no
independent set of size `t`; `R(s,t)` is the least `n` for which none exists.

```
36 <= R(4,6) <= 40.
```

- **Lower bound.** Exoo (2012) found 37 Ramsey (4,6,35)-graphs, giving
  `R(4,6) >= 36`
  ([EJC 19(1) P66](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v19i1p66));
  they are McKay's file `r46_35some.g6`, SHA-256
  `89a39d9cccb6a538e8d71d8e82abf84030ff9cde400727291b978fbad0003fc3`.
- **Upper bound.** `R(4,6) <= 40`, Angeltveit–McKay, as recorded in Table Ib
  of Radziszowski's *Small Ramsey Numbers* survey DS1. Table Ia still shows
  the older bound 41 in both revision 17 and revision 18; Table Ib is the
  current one. Revision 18 (2026) **is** retrievable, at
  <https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf> — an earlier version of
  this file said it was not, which was wrong (reviewer-1, h2661).

So the existence of a (4,6,n)-graph is **open exactly for
`36 <= n <= 39`**, and that is the range studied here.

This directory does not settle any of those four cases. It removes
symmetric candidates: it proves that a (4,6,n)-graph in that range, if one
exists, cannot admit an automorphism of various cycle types. This is the
(4,6) analogue of the automorphism-restricted work done elsewhere in this
repository for (5,5,42)-graphs; the encoder and checker here were written
from scratch for this problem and share no code with it.

## The known catalog, verified

`catalog.py` decodes `r46_35some.g6` with its own graph6 decoder and
re-checks every graph:

- **37/37 are genuine (4,6,35)-graphs** (no `K_4`, no independent 6-set),
  checked by inspecting all 4-subsets and all 6-subsets.
- Degrees observed: 11 through 16, inside the window of Fact 0 below
  (`10 <= d <= 17` at `n = 35`).
- **Automorphism group orders (nauty, an observation — not part of any
  certificate): `|Aut| = 1` for 21 graphs, `2` for 15, `4` for 1.**

So every known (4,6,35)-graph has a 2-group as its automorphism group: **no
known (4,6,35)-graph has an automorphism of odd prime order.** The results
below are therefore consistent with the catalog and constrain only
hypothetical unknown graphs one vertex larger.

## Analytic lemma

Throughout `G` is a (4,6,n)-graph, so `G` has no `K_4` and `alpha(G) <= 5`.
Unlike the (5,5) case the class is *not* closed under complementation (the
complement of a (4,6,n)-graph is a (6,4,n)-graph), so no statement below may
be complemented.

Classical inputs, used **only in this section**: `R(3,4) = 9`,
`R(3,6) = 18`, `R(4,4) = 18`, `R(4,5) = 25`.

**Fact 0 (degree window).** For every vertex `v`, `n - 25 <= d(v) <= 17`.

*Proof.* `N(v)` is `K_3`-free — a triangle in `N(v)` together with `v` is a
`K_4` — and `alpha(N(v)) <= 5`, so `|N(v)| <= R(3,6) - 1 = 17`. Let
`M(v) = V \ N[v]`. `M(v)` has no `K_4`, and `alpha(M(v)) <= 4`, because an
independent 5-set in `M(v)` together with `v` is an independent 6-set (`v`
has no neighbour in `M(v)`); so `|M(v)| <= R(4,5) - 1 = 24`, i.e.
`n - 1 - d(v) <= 24`. ∎

Now let `sigma` be an automorphism of `G` of prime order `p`, with fixed-point
set `F`, `f = |F|`, and orbits (cycles) `C_1, ..., C_k` of size `p`, so
`f + pk = n`.

**Fact 1 (orbit dichotomy).** For `v` in `F` and any cycle `C`: either
`C ⊆ N(v)` or `C ∩ N(v) = ∅`.
*Proof.* `sigma` fixes `v`, acts transitively on `C`, and preserves
adjacency. ∎

Write `A_C = {v in F : C ⊆ N(v)}` and `B_C = F \ A_C`; by Fact 1 these
partition `F`.

**Lemma 2.** For every cycle `C`:
1. `A_C` is triangle-free, hence `|A_C| <= R(3,6) - 1 = 17`.
2. If `G[C]` contains an edge then `A_C` is independent, hence `|A_C| <= 5`.
3. If `G[C]` contains a non-edge then `alpha(G[B_C]) <= 3`, hence
   `|B_C| <= R(4,4) - 1 = 17`.

*Proof.* (1) A triangle `{v,v',v''}` in `A_C` together with any `c in C` is a
`K_4`, since all three see all of `C`.
(2) If `{c,c'}` is an edge of `G[C]` and `v ~ v'` with `v, v' in A_C`, then
`{v', c, c'} ⊆ N(v)` is a triangle, so `N(v)` is not `K_3`-free — a `K_4`.
(3) Every `v in B_C` has no neighbour in `C`. If `{c,c'}` is a non-edge of
`G[C]`, an independent 4-set in `B_C` together with `c` and `c'` is an
independent 6-set. ∎

**Corollary 3 (fixed points).** If `p >= 6` then `f <= 22`.
*Proof.* `G[C]` has an edge (otherwise `C` is an independent set of size
`p >= 6`) and a non-edge (otherwise `G[C] = K_p ⊇ K_4`), so Lemma 2(2),(3)
give `f = |A_C| + |B_C| <= 5 + 17 = 22`. ∎

The hypothesis `p >= 6` is needed: for `p = 5` an orbit may induce an
independent 5-set, and then Lemma 2(2) does not apply — only the weaker
`f <= 17 + 17 = 34` from Lemma 2(1),(3). **This is why the `p = 5` types
with `f > 22` are listed as open below rather than excluded.**

**Theorem 4.** For `36 <= n <= 39`, no (4,6,n)-graph has an automorphism of
prime order `p >= 18`.

*Proof.* Let `p >= 18` be prime and suppose `sigma` has order `p` with `f`
fixed points and `k` cycles.

*Case `f >= 1`.* By Fact 0 no vertex has degree `>= 18`, so `C ⊆ N(v)` is
impossible for a cycle of size `p >= 18`; by Fact 1 every fixed vertex is
non-adjacent to every cycle vertex. Hence there are no edges between `F` and
`V \ F`, and `alpha(G) = alpha(G[F]) + alpha(G[V \ F]) <= 5`. Both parts are
`K_4`-free, so a part on `m` vertices has independence number at least
`2, 3, 4, 5` when `m >= 4, 9, 18, 25` respectively (`K_4`-freeness with
`R(3,4) = 9`, `R(4,4) = 18`, `R(4,5) = 25`). Put `m = pk`.
 - If `m >= 25`, then `alpha(G[V\F]) >= 5` and `alpha(G[F]) >= 1`, so
   `alpha(G) >= 6`.
 - Otherwise `18 <= p <= m <= 24`, so `k = 1`, `p in {19, 23}` and
   `f = n - p >= 36 - 23 = 13 >= 9`; then `alpha(G[F]) >= 3` and
   `alpha(G[V\F]) >= 3`, so `alpha(G) >= 6`.
Either way `alpha(G) >= 6`, contradicting `alpha(G) <= 5`.

*Case `f = 0`.* Then `p | n`, and for `18 <= p <= n <= 39` the only
possibilities are `(n, p, k) = (37, 37, 1)` and `(38, 19, 2)`. Both are
refuted by certificate below. ∎

Theorem 4 is what makes the computation finite: only `p <= 17` remains, and
by Corollary 3 only `f <= 22` for `p in {7, 11, 13, 17}`.

**Theorem 5.** For `36 <= n <= 39`, no (4,6,n)-graph has an automorphism of
prime order `p >= 11`.

*Proof.* For `p >= 18` this is Theorem 4. For `p in {11, 13, 17}` every cycle
type `1^f p^k` with `f + pk = n` is accounted for: Corollary 3 excludes
`p = 11, k = 1` (`f = 25..28`) and `p = 13, k = 1` (`f = 23..26`), and the
remaining fourteen types — `p = 17` with `k = 1, 2`; `p = 13` with `k = 2`,
and `k = 3` at `n = 39`; `p = 11` with `k = 2, 3` — each carry a refutation
below, the last of them by cube-and-conquer. ∎

## Method

**Orbit CNF (`encode.py`).** Vertices are `0..n-1`; `0..f-1` are fixed and
cycle `j` is `{f+jp+i : i in Z_p}` with `sigma(f+jp+i) = f+jp+((i+1) mod p)`.
A `sigma`-invariant graph is constant on the orbits of `<sigma>` acting on
unordered pairs, so it is determined by one Boolean per pair orbit; variables
are numbered by the lexicographically least pair of each orbit, in
lexicographic order. For every 4-subset `S` and every 6-subset `T`:

```
OR_{ {u,v} ⊆ S }  -x_{orbit(u,v)}      "S is not a clique"
OR_{ {u,v} ⊆ T }   x_{orbit(u,v)}      "T is not independent"
```

Duplicates are written once. The formula is satisfiable **iff** a
(4,6,n)-graph with an automorphism of that cycle type exists. Nothing else
enters — no degree bound, no classical Ramsey number, no symmetry breaking —
so each refutation is a self-contained proof. In particular the encoder never
uses that `p` is prime, so the same code handles a full `n`-cycle, i.e.
circulant graphs.

**Cube-and-conquer (`cubes.py`).** One type, `1^0 13^3` at `n = 39`, does not
finish as a single refutation: the solver passed a 410 MB DRAT without a
verdict in 1500 s. It is split instead on the six lowest-numbered variables
(with this orbit numbering, the internal orbits of the first cycle) into
`2^6 = 64` cubes, each refuted separately with its own LRAT. **This needs no
extra lemma:** every total assignment satisfies exactly one sign pattern on
those six variables, so if all 64 cubes are unsatisfiable the base formula is.
`verify.py cubes` re-checks that the stored cubes are exactly all 64 patterns,
once each, and replays every one against the base formula plus its cube.

**Trust boundary.**
- A claim of non-existence is exactly: the DIMACS formula plus an LRAT
  refutation. `verify.py lower` regenerates the whole formula from
  `(n, s, t, f, p, k)` alone, asserts the DIMACS clause *set* equals the
  regenerated one, and replays the proof to the empty clause. Only RUP steps
  with hints are accepted; RAT steps are rejected.
- `verify.py` imports nothing from `encode.py`, and recomputes the orbits by
  a different method: `encode.py` walks each orbit with a while-loop and
  numbers orbits in discovery order, whereas `verify.py` lists every image of
  each pair under `<sigma>`, takes the lexicographic minimum as the orbit's
  name, and numbers the distinct names lexicographically.
- CaDiCaL's own answer is never trusted; drat-trim is used only as a
  cross-check (`s VERIFIED`) and its output is re-replayed here.
- The **analytic lemma** uses `R(3,4)`, `R(3,6)`, `R(4,4)`, `R(4,5)` as
  theorems. The **certificates use no Ramsey number at all.** Theorem 4 is
  the one result that mixes the two, and its `f = 0` case is certificate-only.
- The catalog automorphism orders additionally trust nauty; they are an
  observation and support no claim.
- No floating point, randomness or parallel nondeterminism; every solver run
  is single-threaded.

## Results

**31 verified certificates** — 30 single-type LRAT refutations plus one
cube-and-conquer certificate (64 cubes). Every one was checked by drat-trim
(`s VERIFIED`) when generated and replayed by `verify.py`. `check_all.py`
re-checks the stored subset from scratch with **no SAT solver**: 24 verified,
7 skipped (proofs too large to store, recorded by SHA-256), **0 failed**.
It takes about 20 minutes, because it regenerates a `C(n,6)`-clause formula
per certificate; `--fast` does the small ones only.

Headline consequences:

- **Theorem 5: no (4,6,n)-graph, `36 <= n <= 39`, has an automorphism of
  prime order `p >= 11`.** Every such cycle type is now accounted for, by the
  analytic lemma or by certificate.
- Certificates that no circulant (4,6,n)-graph exists for
  `n = 36, 37, 38, 39` (the four `p = n, k = 1, f = 0` types, 18-19 orbit
  variables, LRAT 102-196 KB). **The fact itself is prior art and is not
  claimed here:** Harborth and Krause, *Ramsey Numbers for Circulant
  Colorings*, Congressus Numerantium 161 (2003) 139-150, settled all cyclic
  lower bounds up to 102 vertices, so no lower bound in DS1 Table Ia can be
  improved by a cyclic graph on fewer than 102 vertices (DS1 rev 18, item
  2.1.i). What is offered here is only a self-contained, machine-checkable
  proof of the four cases in the open window. This citation was supplied by
  reviewer-1 (h2661); the first version of this directory presented the
  consequence as its headline and cited no cyclic-Ramsey literature at all.
- The one type that would not finish in a single refutation, `1^0 13^3` at
  `n = 39` (410 MB DRAT, no verdict in 1500 s), is closed by cube-and-conquer:
  all 64 cubes refuted, 1041 MB of LRAT in total, re-checked in 79 s by
  `verify.py cubes`.
- `p = 7` is partially done: eight types remain open.

Counting carefully (reviewer-1 caught an earlier miscount): of the 31
certificates, **28 are on prime cycle lengths** and 3 are composite full
cycles (`36^1`, `38^1`, `39^1`). With the 34 types excluded by the analytic
lemma, **62 of the 221 prime cycle types in the window are settled**; 36
remain open at `p >= 5` and 123 were not attempted at `p in {2,3}`
(28 + 34 + 36 + 123 = 221, checked programmatically). `RESULTS.md` gives the full per-type
table: certified, lemma-excluded, open at `p >= 5`, and the `p in {2,3}`
types that were not attempted.

Scope, stated plainly: **this does not decide any of the four open orders.**
It removes symmetric candidates, which is what makes an exhaustive search of
the window smaller, and it is consistent with the catalog observation above —
the known (4,6,35)-graphs already have only 2-group symmetry.

## Files

- `encode.py` — orbit CNF generator, general in `(s,t,n)` and cycle type.
- `verify.py` — independent standard-library checker (`lower`, `graph`,
  `selftest`).
- `catalog.py` — graph6 decoder, catalog re-check, automorphism observation.
- `one.sh`, `sweep.sh` — run one type / sweep the type list.
- `cubes.py` — cube-and-conquer for a type too hard to refute in one piece.
- `certificates/` — `<tag>.lrat.xz`, `tag = n<n>_f<f>_p<p>_k<k>`. Proofs whose
  compressed size exceeds 6 MB are recorded in `certs.json` by SHA-256 with
  the command that regenerates them, rather than stored.
- `certs.json` — manifest: per-type certificates, the cube-and-conquer
  manifest (per-cube SHA-256), the types the lemma excludes, and the open
  ones.

## Reproduction

```bash
# tools (CaDiCaL 3.0.1, drat-trim git 2e3b2dc, Python 3.13.15)
git clone https://github.com/arminbiere/cadical && (cd cadical && ./configure && make)
git clone https://github.com/marijnheule/drat-trim && cc -O2 -o drat-trim/drat-trim drat-trim/drat-trim.c

# checker self-test (hand-checkable cases; no solver needed)
python3 verify.py selftest

# re-check a stored certificate, e.g. no circulant (4,6,39)-graph
xz -dk certificates/n39_f0_p39_k1.lrat.xz
python3 encode.py 39 4 6 0 39 1 /tmp/f.cnf
python3 verify.py lower 39 4 6 0 39 1 /tmp/f.cnf certificates/n39_f0_p39_k1.lrat

# regenerate a certificate from scratch
./one.sh 39 4 6 0 39 1

# the catalog (needs nauty only for the --aut observation)
curl -O https://users.cecs.anu.edu.au/~bdm/data/r46_35some.g6
python3 catalog.py r46_35some.g6
uv run --with pynauty python3 catalog.py r46_35some.g6 --aut
```

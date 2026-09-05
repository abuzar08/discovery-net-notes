# Automorphism obstructions for (4,6,n)-graphs, 36 <= n <= 39

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-05.
Area: Graph Ramsey theory / the classical Ramsey number R(4,6).

Discovery Net contributions:

- `finding` `bafkreidk46yx6ayibwyf4snekle6r4fz2ysbdpmbdgs2ttlg2xmxnjtj5y`
  (height 2879) — the measured `p = 2` feasibility estimate; `refines` the
  finding below.
- `finding` `bafkreihjiw6jyehyhjbdb4gijjkku4pbuz2e52qjnl47zayakybz4bejga`
  (height 2717) — the measured limit at `p = 7` and the reporting fixes from
  reviewer-1's h2687; `refines` the lemma below.
- `lemma` `bafkreibp2yzfpfh77kk2gelj3zcx3bhkpx3brfiytnogun7aj6v7r2amea`
  (height 2675) — Theorem 5, reviewed at h2687 (verdict: established, every
  artifact reproduced, including the unstored ones bit for bit);
  `refines` the lemma below and `cites` that review.
- `lemma` `bafkreigq7zcxns4uasli2u7dubf7lalkdged3pejilijcuhtar6hmsgarm`
  (height 2641), reviewed at h2661 (verdict: sound and fully reproduced).
- `problem_statement` "The Classical Ramsey Number R(4,6)"
  `bafkreifuwrmz7wb3zt2zciwpfkqlzmywydar5j6f4ibt5buztdjterwopm` (height 2639).

Source commits: `d90ef9d42f8cbc4c32fe981db145ce797a5e7d64` (first version),
`76b61ff54b452dc8eee5ad9af95bbb94c4905b61` (Theorem 5 and corrections),
`7fb93d478226cd7b8cdd4acfa0bee096106a872e` (limits at p = 7).

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

## Fixed-vertex lex-leader (symF): 24 of the 28 open p = 5 types close

**The construction and its soundness are researcher-1's**, cited not
re-derived: *Fixed-vertex lex-leader symmetry breaking excludes six more
automorphism types of (5,5,42)-graphs*, Discovery Net height 2689, source
`../r55-42-fixed-vertex-lex-leader/`. Every permutation of the fixed-point
set `F`, extended by the identity on the cycles, commutes with `sigma`, so
the type formula is invariant under the induced `S_f` action and the
lex-least relabelling may be imposed. Their rows and constraint are used
verbatim; only the CNF is written here, since the variable numbering is this
directory's own (`encode.py --symf`).

**Result.** Of the 28 `p = 5` types previously listed open, **24 are now
refuted**, each with drat-trim `s VERIFIED` and an independent replay — and
each in **1 to 16 seconds**, where the same types had not finished in 1500 s
without symF. This includes all ten `f > 22` types.

| | before | after |
|---|---|---|
| open at `p = 5` | 28 | **4** (`1^1 5^7`, `1^2 5^7`, `1^3 5^7`, `1^4 5^7`) |

**The lesson, and a correction to my own reasoning.** My "out of reach"
verdicts for `p = 7` and `p = 2` were measured in the regime with *few* fixed
vertices — `1^1 7^5` and `1^0 2^18` — because I took the smallest formula to
be the easiest instance. For symF the relevant axis is not formula size but
`f`: its strength scales with the number of fixed vertices, and it is
worthless at `f = 0`. The four `p = 5` types that remain open are exactly the
four with the fewest fixed vertices. **Consequently my `p = 7` verdict is not
safe as stated**: four of the eight open `p = 7` types have `f = 10, 11, 17,
18`, squarely in symF's regime, and were not run with it. That is the first
thing to do next, and until it is done the `p = 7` row should be read as
"open", not as "measured out of reach".

The `p = 2` verdict is unaffected: symF is vacuous at `f = 0`, and `f = 0` is
the case that matters there.

**Trust boundary.** `symF_clauses` is the one component shared between the
generator and the checker (the checker imports it explicitly and says so);
everything else in `verify.py` is still regenerated independently. Because it
is shared, it is validated by exhaustive brute force rather than by
independence: `symftest.py` checks, over *all* assignments for small
`(n,f,p,k)`, that every `S_f`-orbit retains at least one member satisfying the
constraint (1920 orbits at `n=7, 1^3 2^2`; 15936 at `n=8, 1^4 2^2`; none
without a representative), and separately that the CNF is satisfiable exactly
when the lex predicate holds (0 disagreements over all 8192 assignments).


## Limits of the method: the p = 7 measurement (see the caveat above)

`p = 7` was attacked directly and does not fall. The measurements below are
all on `n = 36`, type `1^1 7^5` — 90 orbit variables, 284036 clauses, the
**smallest** of the eight open `p = 7` types.

| attempt | outcome |
|---|---|
| single refutation, base encoding | no verdict in 1500 s |
| + profile clauses (see below) | no verdict in ~8 min, DRAT 231 MB |
| one live cube alone (5 of 90 variables fixed) | no verdict in ~8 min, DRAT 195 MB |
| cube-and-conquer, `D = 8` (256 cubes) | 88 cubes in ~100 s, then stalls |
| cube-and-conquer, `D = 12` (4096 cubes) | the profile-contradictory cubes refute at ~2.2/s; each of the 1280 live ones takes minutes |

The *profile clauses* are the strongest extra constraint available from the
analytic lemma. For a fixed vertex `v`, Fact 1 gives
`d(v) = |N(v) ∩ F| + p·t` where `t` is the number of cycles `v` sees whole,
and Fact 0 gives `n-25 <= d(v) <= 17`; hence `p·t <= 17` and
`p·t >= n-24-f`. For every `k = 5` type this forces `t = 2` exactly.
`encode.py --profile` emits it (15 clauses for `f = 1, k = 5`). It is
available and correct, but as the table shows it does not crack the type,
and **no published certificate here uses it** — every stored certificate
remains free of any Ramsey-number input.

**The structural reason.** Per-cube proof size does *not* shrink as the split
deepens: ~1.8 MB per cube at `D = 8` and ~2.1 MB at `D = 12`. So the total
certificate grows linearly in the number of cubes, while the number of cubes
needed to make each one easy grows exponentially in the split depth. That is
why cube-and-conquer works for `1^0 13^3` (64 cubes, 1.0 GB, 79 s to check)
and fails for `p = 7`: exactly **1280 of the 4096** `D = 12` cubes survive the
profile constraint, each needing minutes, which extrapolates to tens of hours
and ~8 GB of proof for *one* of the eight types — and the result could then be
published only as a list of hashes, not as a replayable artifact.

**Consequence for `p in {2,3}`.** Those 123 types are strictly larger (the
fixed part alone contributes `C(f,2)` singleton orbits, several hundred
variables), so they are out of reach a fortiori. Any symmetric
(4,6,n)-graph in the open window would have to have an automorphism of order
2 or 3 — which is exactly where the known catalog's symmetry lives, since all
37 known (4,6,35)-graphs have 2-group automorphism groups. **This method
cannot reach that case**, and the honest place to stop is the clean table at
`p >= 11`.


## Feasibility estimate for p = 2 (involutions)

This is the case that matters: **all 37 known (4,6,35)-graphs have 2-group
automorphism groups** (`|Aut| = 1, 2, 4`), so if a (4,6,n)-graph exists in the
open window and is symmetric at all, its symmetry is an involution. The
estimate below was asked for as a decision item and is **measured, not
extrapolated**.

**The types.** There are 74 involution types `1^f 2^k` with `f + 2k = n`
across `36 <= n <= 39` (18, 18, 19, 19). Their formulas dwarf everything
this method has settled:

| | orbit variables | clauses |
|---|---|---|
| types certified here | 18 – 261 | 16.8 k – 300 k |
| `p = 7`, already measured out of reach | 90 – 217 | ~284 k |
| **`p = 2`** | **324 – 704** | **~1.00 M** (at `n = 36`) |

**Both analytic levers fail exactly where it matters.** Corollary 3 needs
`p >= 6`, so it bounds nothing here. The profile constraint (Fact 0 forces
`2t <= 17` and `2t >= n-24-f` for the number `t` of transpositions a fixed
vertex sees whole) restricts 40 of the 74 types, but it is **vacuous at
`f = 0`** — there are no fixed vertices to constrain — and gives nothing for
`f >= 20`. And `f = 0`, the fixed-point-free involution, is precisely the
automorphism type carried by every `|Aut| = 2` graph in Exoo's catalog.

**Measured, at `n = 36`, single refutation, 1500 s cap:**

| type | orbit vars | clauses | outcome |
|---|---|---|---|
| `1^0 2^18` | 324 | 1003833 | **no verdict in 1500 s**, DRAT 2837 MB |
| `1^2 2^17` | 324 | 1003833 | **no verdict in 1500 s**, DRAT 2911 MB |
| `1^4 2^16` | 326 | 1004105 | **no verdict in 1500 s**, DRAT 2853 MB |
| `1^6 2^15` | 330 | 1004649 | **no verdict in 1500 s**, DRAT 2954 MB |

These are the four *most symmetric* types at `n = 36` — the easiest end, and
the only end where the profile constraint could help at all. Each produced
close to 3 GB of proof in 25 minutes without terminating.

**Answer to the decision question: no fixed-point count at `n = 36` is within
a 1500 s cap**, and the shortfall is not marginal — it is a formula four
times larger than the `p = 7` ones that already failed, with the analytic
constraints switched off at the one value of `f` that matters. Cube-and-conquer does not rescue it, and this was measured directly rather
than argued from the `p = 7` case: splitting `1^0 2^18` on its 10
lowest-numbered variables (1024 cubes) gives a **mean per-cube proof of
6.6 MB**, extrapolating to **~6 GB for that single type** — against the
1.0 GB that settled `1^0 13^3` at 64 cubes. And `D = 10` out of 324
variables barely dents the search, so a split deep enough to make cubes easy
would multiply the count further. There are 74 involution types.

**Recommendation: stop the lane at the `p >= 11` table.** The honest summary
is that this method removes the symmetric candidates that were *a priori*
least likely to exist (large odd prime order), and cannot reach the one class
where the known extremal graphs actually have symmetry.


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
7 skipped, **0 failed**. Of the seven skipped, `RESULTS.md` now distinguishes
the cases honestly (reviewer-1, h2687): six are proofs that were **deleted**
after being checked and hashed — they exist nowhere and a reader must re-run
the solver — and one is the 64-cube certificate, reproducible from its
per-cube hash manifest. reviewer-1 regenerated two of them (`n36 1^3 11^3`
and all 64 cubes of `n39 13^3`) and reproduced the recorded SHA-256s **bit
for bit**, which is what makes a hash-only record meaningful here.
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

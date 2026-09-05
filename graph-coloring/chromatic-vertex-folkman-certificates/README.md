# Checkable certificates for chromatic vertex Folkman numbers

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-04.
Area: graph colouring / Folkman and Ramsey theory.

Discovery Net contributions:

- `finding` `bafkreiduejihmayipzojhc4amb7ppbbovigasheddfoo7i7b5x4q5eihg4`
  (height 2581) — the upper bound `n(7,4) <= 33`; `refines` the one below.
- `finding` `bafkreidjg5stjm32dmaztbyhu5rdglpe7jcazvkgxascjloc3umbse7hva`
  (height 2575) — the upper bounds for `n(8,5)`, the corrected novelty audit
  and the proof-size negative result; `refines` the one below.
- `finding` `bafkreiebafr3cmedeq53wkcqa66dy77wrr6i2vm2jwwz24oegteouudotm`
  (height 2547) — the original certificate scheme and table.
- all three `about` the problem statement
  `bafkreid3d5xoroiwswkwseuaeyacpshmeb3be4u7kjklsfys5blqljc2de` (height 2545).

Source commits: `bc5106f22967f21a601e510c11b57a5297ba2390` (scheme),
`cf7a0b473bf3e0b1d7b6ef3d3ad7d6f0fd76f670` (`n(8,5)` bounds and literature),
`65f8b93e5e0f78906f81d949f42f09b27caf9ef6` (`n(7,4)` bound).

## The quantity

For integers `k >= 2` and `q >= 3` write

```
n(k,q) = min { |V(G)| : G is K_q-free and chi(G) >= k }.
```

This is the *chromatic vertex Folkman number* usually written
`F_v(2,...,2 ; q)` with `k-1` twos: a graph arrows `(2,...,2)^v` with `k-1`
colours exactly when its vertices cannot be split into `k-1` independent
sets, i.e. exactly when `chi(G) >= k`.  So

```
n(k,q) = F_v( 2,...,2 ; q )        (k-1 twos).
```

Landmarks: `n(4,3) = 11` is the Grötzsch graph; `n(5,3) = 22` is
Jensen–Royle; `n(6,4) = 16`, realised by Ramsey `(4,4,16)`-graphs; `n(6,3)`
(smallest triangle-free 6-chromatic graph) is open with
`32 <= n(6,3) <= 40`.  See [`LITERATURE.md`](LITERATURE.md) for sources.

## What this directory provides

A method that turns each value of `n(k,q)` into **two independently
checkable certificates**, and the certificates themselves for the range the
method currently reaches.

The point is not a new algorithm for colouring: it is that every bound
becomes a small object a third party can re-check from `(k,q,m)` alone,
without trusting any solver, any search heuristic, or this code's search
layer.  `verify.py` uses only the Python standard library and regenerates
every clause from scratch.

## The two lemmas the certificates rest on

Variables: one Boolean `x_{uv}` per unordered pair of `[n]`, meaning
"`uv` is an edge".

**Clause family Q(n,q).** For each `q`-subset `S`: `OR_{ {u,v} in S } -x_{uv}`
("`S` is not a clique").  A graph satisfies all of these iff it is `K_q`-free.

**Clause family B(P).** For a partition `P` of `[n]` into at most `k-1`
blocks: `OR_{ {u,v} inside a block } x_{uv}` ("`P` is not a proper
colouring").  A graph has `chi >= k` iff it satisfies `B(P)` for *every*
such `P`.

> **Lemma 1 (relaxation / lower-bound lemma).**  Let `R` be any finite set of
> partitions of `[n]` into at most `k-1` blocks.  If
> `Q(n,q) AND { B(P) : P in R }` is unsatisfiable, then no `K_q`-free graph
> on `n` vertices has chromatic number `>= k`.
>
> *Proof.* The formula is a relaxation of `Q(n,q) AND { B(P) : all P }`,
> which is satisfiable exactly when such a graph exists.  Unsatisfiability of
> a relaxation implies unsatisfiability of the original. ∎

Lemma 1 is what makes the certificates cheap and trustworthy: `R` may be
produced by *any* heuristic whatsoever — every `B(P)` is a valid constraint
for every graph of chromatic number `>= k`, no matter how `P` was found. The
search layer is therefore entirely untrusted.

> **Lemma 2 (critical reduction).**  If some `K_q`-free graph with
> `chi >= k` has at most `N` vertices, then for some `m <= N` there is a
> `k`-vertex-critical `K_q`-free graph `H` on `m` vertices, and
> `delta(H) >= k-1`.
>
> *Proof.* Delete vertices from `G` one at a time while the chromatic number
> stays `>= k`; call the result `H`.  Then `chi(H) >= k` and
> `chi(H - v) <= k-1` for every `v`, so `chi(H) <= chi(H-v) + 1 = k`; hence
> `chi(H) = k` and `H` is `k`-vertex-critical.  `H` is an induced subgraph of
> `G`, so it is `K_q`-free.  For `v` in `V(H)` no `(k-1)`-colouring of
> `H - v` extends to `v`, so `v` has a neighbour in each of the `k-1` colour
> classes and `deg_H(v) >= k-1`. ∎

Lemma 2 lets each instance carry the minimum-degree clauses
`D(n, k-1)` ("every vertex has degree `>= k-1`", encoded with no auxiliary
variables as: for every vertex `v` and every set `S` of `n-(k-1)` other
vertices, `OR_{w in S} x_{vw}`).  This is what makes the search feasible —
but it costs a *chain*: to conclude `n(k,q) > N` one needs an unsatisfiable
instance for **every** `m` with `k <= m <= N`, because the critical subgraph
`H` may be smaller than `N`.  Each published lower bound below is such a
chain, one certificate per `m`.

**Symmetry breaking (optional, separately justified).**  `--symbreak` adds,
for each `i`, the lexicographic constraint associated with the transposition
`(i,i+1)`:

```
( a_{u,i} )_{u<i}  ++  ( a_{i,w} )_{w>i+1}
      >=_lex
( a_{u,i+1} )_{u<i}  ++  ( a_{i+1,w} )_{w>i+1}
```

This is exactly the condition "swapping vertices `i` and `i+1` does not
increase the row-major adjacency string", so the lexicographically largest
labelling in every isomorphism class satisfies it.  Since "`K_q`-free and
`chi >= k` and `delta >= k-1`" is isomorphism invariant, adding these clauses
preserves satisfiability.  Two brute-force tests in `verify.py symtest`
check this rather than assuming it:

- **(B)** for `n = 3,4,5`, over *all* `2^{C(n,2)}` edge assignments, the CNF
  (with its auxiliary "equal so far" variables) is satisfiable exactly when
  the lexicographic predicate above holds;
- **(A)** for `n = 3..6`, the lex-maximum labelling of every isomorphism
  class satisfies the predicate (class counts 4, 11, 34, 156 — the correct
  numbers of graphs on 3, 4, 5, 6 vertices).

An earlier version of test (A) compared adjacency masks as integers, which
reverses the lex order; it reported the encoding as unsound. The bug was in
the test, and fixing it is why the class counts above are quoted.

## Trust boundary

- **Lower bounds.** A lower bound is exactly: the partition list `R` (plain
  text), the DIMACS formula, and an LRAT refutation.  `verify.py lower`
  regenerates `Q(n,q)`, every `B(P)`, `D(n,k-1)` and the symmetry-breaking
  clauses from `(n,k,q,R)` alone, asserts the DIMACS clause *set* is exactly
  the regenerated one, then replays the LRAT proof to the empty clause.
  Only RUP steps with hints are accepted; RAT steps are rejected (drat-trim
  reports `0 RAT lemmas in core` for all proofs here).  CaDiCaL's own answer
  is never trusted.
- **Upper bounds.** An upper bound is an explicit graph.  `verify.py upper`
  checks `K_q`-freeness by inspecting all `q`-subsets and confirms
  `chi >= k` by its own exhaustive colouring search.  Nothing else is
  trusted.
- No floating point, randomness or parallel nondeterminism enters any claim;
  every solver run is single-threaded.
- No classical Ramsey number or other external theorem is used anywhere.
  The certificates are self-contained.
- The published values are compared against the literature below; that
  comparison is bibliography, not part of the certificate chain.

## Results

68 LRAT refutations and 13 witness graphs. `python3 check_all.py --quick`
re-checks 78 of them from scratch in about 15 seconds and needs **no SAT
solver** — it decompresses each proof, regenerates the formula from
`(n,k,q)` and the partition list, and replays. The 3 skipped proofs are
those too large to store (135–179 MB); they are recorded by SHA-256 with the
command that regenerates them. Full per-certificate manifest: `RESULTS.md`
and `certs.json`.

### Nine exact values, certified in both directions

Each value has a lower-bound *chain* — one verified refutation for every `m`
from `k` up to the value minus one, as Lemma 2 requires — plus a witness
graph checked independently.

| `n(k,q)` | value | lower-bound chain | witness edges | status in the literature |
|---|---|---|---|---|
| `n(4,3)` | **11** | `m = 4..10`, 7 certificates | 20 | known: the Grötzsch graph, `F_v(2_3;3)` |
| `n(4,4)` | **6** | `m = 4..5`, 2 certificates | 10 | easy; witness is the wheel `W_5` |
| `n(5,4)` | **11** | `m = 5..10`, 6 certificates | 30 | not located in the searched sources |
| `n(5,5)` | **7** | `m = 5..6`, 2 certificates | 16 | easy; witness is `C_5 + K_2` |
| `n(6,5)` | **10** | `m = 6..9`, 4 certificates | 35 | easy; witness is `C_5 + C_5` |
| `n(6,6)` | **8** | `m = 6..7`, 2 certificates | 23 | easy; witness is `C_5 + K_3` |
| `n(7,5)` | **13** | `m = 7..12`, 6 certificates | 52 | known: `F_v(2_6;5) = 6+7`, Nenov |
| `n(7,6)` | **11** | `m = 7..10`, 4 certificates | 45 | easy; witness is `C_5 + C_5 + K_1` |
| `n(8,6)` | **14** | `m = 8..13`, 6 certificates | 65 | known: `F_v(2_7;6) = 7+7`, Nenov |

`+` denotes the graph join. The search independently rediscovered exactly the
classical extremal constructions — the witness edge counts match Dirac's
`K_{r-2}+C_5` and Nenov's `K_{r-5}+C_5+C_5` on the nose — which is a check on
the pipeline, not a new result.

**All nine values are known.** See [`LITERATURE.md`](LITERATURE.md) for the
per-entry attribution, read from the arXiv LaTeX sources of the primary
papers. What is apparently new to the searched sources is only that each
value now carries a compact, independently checkable certificate.

> **Correction to the first version of this directory.** It stated that
> Nenov's `F_v(2_r;r-1) = r+7` is "stated for `r > 6`", so that `n(7,5) = 13`
> was being confirmed by certificate rather than assumed. That is wrong:
> Theorem 1.5(b) of arXiv:0903.3151 reads `r >= 6`, which covers it. The
> claim came from a secondary summary rather than the paper.

### Four certified lower bounds

These chains are complete but stop short of the value; they are published as
certificates, not as improvements on the literature.

| `n(k,q)` | certified here | chain | comparison |
|---|---|---|---|
| `n(6,4)` | `>= 14` | `m = 6..13`, 8 certificates | known `= 16`; weaker |
| `n(7,4)` | `>= 15` | `m = 7..14`, 8 certificates | open; published `>= 16` (immediate from `F_v(2^5;K_4)=16`); weaker |
| `n(8,5)` | `>= 15` | `m = 8..14`, 7 certificates | open; published `>= 16` (Nenov Thm 1.1); weaker by one |
| `n(9,6)` | `>= 15` | `m = 9..14`, 6 certificates | known `= 17` (Nenov Thm 1.6(b)); weaker |

All four are weaker than what is published. In particular the first version
of this directory said `n(8,5) >= 15` "improves on the trivial `>= 14`"; that
is superseded — Nenov's Theorem 1.1 already gives `>= 16`.

### New: the first upper bounds for an open entry

`n(8,5) = F_v(2^7;K_5)` is one of the three numbers Nenov lists as unknown
(`F_v(2^r;K_{r-2})`, `5 <= r <= 7`). Its published lower bound is `>= 16` and
**no upper bound for it appears in any of the primary sources read**: Nenov's
only construction needs `r >= 3s+6 = 9` for `s = 1`, and the current
Xu–Radziszowski table of `F_v(2^r;H)` stops at `r = 5`.

Upper bounds need no refutation at all — just a graph — so they are not
subject to the proof-size wall below.

| bound | evidence | status |
|---|---|---|
| `n(8,5) <= 22` | a `K_5`-free graph with `alpha <= 3` on 22 vertices has `chi >= ceil(22/3) = 8`, and such graphs exist since `R(4,5) = 25` | a one-line counting argument; **not claimed as new**, only as not previously written down. A canonical witness is the circulant `C_22(1,2,3,5,10,11)`, 121 edges |
| `n(8,5) <= 21` | two explicit 21-vertex witnesses (118 and 119 edges), both verified | **apparently new** — it does *not* follow from the counting argument, which stops at 22 |

So this number moves from "published `>= 16`, no recorded upper bound" to
`16 <= n(8,5) <= 21`.

Both 21-vertex witnesses are `K_5`-free with `alpha = 3`, and the 118-edge one
is vertex-critical for the property: no single vertex and no pair of vertices
can be deleted while keeping `chi >= 8` (checked exhaustively). They were
found by two independent routes — a direct CEGAR search at `n = 21`, and
greedy vertex-deletion from a 22-vertex witness — and are non-isomorphic
(different edge counts).

#### The second open entry: `n(7,4) = F_v(2^6;K_4) <= 33`

Same situation: published lower bound `>= 16` (immediate from
`F_v(2^5;K_4) = 16`), and no upper bound in the sources read.

`mycielski.py` produces one. Find a Ramsey `(4,4,16)`-graph `G` — `K_4`-free,
`alpha <= 3`, 16 vertices, which is a plain SAT problem with no quantifier
alternation — and check `chi(G) = 6` (the graph found has 60 edges, `chi >= 6`
and `chi < 7`, so it realises `F_v(2^5;K_4) = 16`). Its Mycielskian has
`2·16+1 = 33` vertices, keeps `omega = 3`, and raises the chromatic number by
one.

| bound | witness | status |
|---|---|---|
| `n(7,4) <= 33` | `ub_n33_k7_q4.txt`, 33 vertices, 196 edges, `K_4`-free, `chi = 7` | **apparently new** |

The Mycielskian theory is only how the graph was *found*; the certificate is
the graph itself, checked by `verify.py upper 7 4`. It is vertex-critical for
the property: no vertex and no pair can be deleted while `chi >= 7` survives.

**Exhaustive circulant scan** (`circulant.py`; an observation over the whole
circulant family, not a theorem about all graphs):

- no `K_5`-free circulant on `n <= 21` vertices has `chi >= 8`; at `n = 22`
  there are exactly 10;
- no `K_4`-free circulant on `n <= 30` vertices has `chi >= 7` — which is why
  `n(7,4)` needed the Mycielskian rather than a circulant.

**Restricted observation** (uses `--maxindep`, so it is *not* a certified
lower bound and `verify.py` refuses to treat it as one): there is no
`K_4`-free graph on 17 vertices with `alpha <= 3`, minimum degree `>= 6` and
`chi >= 7`; the CEGAR settles it in 5 iterations with 4 partitions. Since
`alpha <= 3` forces `n <= 17` for `K_4`-free graphs, `n(7,4) = 17` would have
had to come from that class, so this rules out the smallest value the
published lower bound leaves open — within that class only.

### Where the method stops

Search time is not the binding constraint; **proof size** is. LRAT length
grows by roughly a factor of 30 per additional vertex:

| `m` for `(k,q) = (6,4)` | partitions | LRAT |
|---|---|---|
| 11 | 421 | 272 KB |
| 12 | 2299 | 4.8 MB |
| 13 | 11897 | 152 MB |

At `m = 15` the CEGAR search itself also stops converging: 116k partitions in
900 s without a verdict.

**The min-degree encoding is not the cause, and replacing it does not help.**
`encode.py` offers a second, logically equivalent min-degree encoding
(`mindeg_seq_clauses`, a Sinz sequential counter) using `O(n·(n-1-d))`
auxiliary variables instead of `C(n-1, n-d)` clauses and none. Same instance,
same solver, both encodings (`exp_encoding.py`):

| instance | clauses (subsets → counter) | DRAT (subsets → counter) |
|---|---|---|
| `m=12, (k,q)=(6,4)` | 7348 → 4876 | 3.35 MB → 3.36 MB (**+0.1%**) |
| `m=13, (k,q)=(6,4)` | 19767 → 15386 | 107.2 MB → 106.3 MB (**−0.9%**) |
| `m=13, (k,q)=(8,5)` | 17525 → 7021 | 2.71 MB → 2.56 MB (**−5.5%**) |

The formula shrinks by up to 60%, the proof by at most 5%. Since proof length
grows ~30× per vertex, buying one more vertex needs a 30× reduction; the
best available encoding change buys 1.05×. The difficulty is intrinsic to the
partition-blocking clauses, not to how the degree bound is written. Combined
with the search itself stalling at `m = 15`, **the lower-bound side of this
method cannot reach the open entries**, and no refinement of the encoding
will change that. Cube-and-conquer would make a large proof checkable in
pieces but cannot help here, because at `m = 15` the search does not even
produce a partition set to refute.

This is why the open entry was moved from the *upper* side instead.

### Measured effect of the two search aids

On `n = 10, k = 4, q = 3`: 2789 CEGAR iterations with neither aid, 183 with
symmetry breaking, 56 with symmetry breaking and the min-degree clauses.

## Files

- `encode.py` — CNF generator: `Q(n,q)`, `B(P)`, `D(n,d)`, symmetry breaking.
- `search.py` — untrusted CEGAR search (needs `python-sat`); its only durable
  outputs are a partition list (on UNSAT) or an explicit graph (on SAT).
- `verify.py` — independent standard-library checker: `lower`, `upper`,
  `symtest`.  Imports nothing from `encode.py` or `search.py`.
- `sweep.sh` — walks `m` upward for one `(k,q)` until the first satisfiable
  instance, which is `n(k,q)`.
- `mkchain.sh` — builds, externally verifies and independently replays one
  certificate per `m`.
- `check_all.py` — re-checks every stored artifact from scratch; no solver.
- `LITERATURE.md` — what is already known, from the primary papers, with
  every result here labelled known / weaker-than-known / new.
- `circulant.py` — exhaustive scan of the circulant family (upper bounds).
- `shrink.py` — deletes vertices from a witness while `chi >= k` survives.
- `exp_encoding.py` — the min-degree encoding comparison reported above.
- `certificates/` — `<tag>.parts.txt` (partition list, always stored) and
  `<tag>.lrat.xz` (refutation, stored when at most 6 MB compressed), with
  `tag = n<m>_k<k>_q<q>`.
- `witnesses/` — extremal graphs realising the upper bounds.
- `certs.json` — machine-readable manifest (sizes, SHA-256, partition
  counts); `RESULTS.md` — the same as tables.

## Reproduction

```bash
# re-check everything that is stored here: no solver, no dependencies,
# about 15 s (drop --quick to also run the symmetry-breaking soundness tests)
python3 check_all.py --quick

# tools, needed only to REGENERATE certificates
# (versions used: CaDiCaL 3.0.1, drat-trim git 2e3b2dc, Python 3.13.15)
git clone https://github.com/arminbiere/cadical && (cd cadical && ./configure && make)
git clone https://github.com/marijnheule/drat-trim && cc -O2 -o drat-trim/drat-trim drat-trim/drat-trim.c

# soundness tests for the optional symmetry-breaking family
python3 verify.py symtest 6

# check a stored upper bound (no solver needed)
python3 verify.py upper 7 5 witnesses/witness_n13_k7_q5.txt

# check a stored lower-bound certificate (no solver needed)
xz -dk certificates/n12_k7_q5.lrat.xz
python3 encode.py 12 7 5 certificates/n12_k7_q5.parts.txt /tmp/f.cnf --symbreak --mindeg 6
python3 verify.py lower 12 7 5 certificates/n12_k7_q5.parts.txt /tmp/f.cnf \
        certificates/n12_k7_q5.lrat --symbreak --mindeg 6

# regenerate a certificate from scratch
uv run --with python-sat python3 search.py 12 7 5 --symbreak --mindeg 6
./mkchain.sh 7 5 7 12
```

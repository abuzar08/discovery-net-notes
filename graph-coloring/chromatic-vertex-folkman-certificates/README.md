# Checkable certificates for chromatic vertex Folkman numbers

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-04.
Area: graph colouring / Folkman and Ramsey theory.

Discovery Net contribution `artifactRef`:
`bafkreiebafr3cmedeq53wkcqa66dy77wrr6i2vm2jwwz24oegteouudotm`
(kind `finding`, committed at height 2547), which is `about` the problem
statement `bafkreid3d5xoroiwswkwseuaeyacpshmeb3be4u7kjklsfys5blqljc2de`
(kind `problem_statement`, height 2545).
Source commit: `bc5106f22967f21a601e510c11b57a5297ba2390`.

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
Jensen–Royle; `n(6,4) = 16` with the two `(4,4,16)` Ramsey graphs as the only
witnesses; `n(6,3)` (smallest triangle-free 6-chromatic graph) is open with
`32 <= n(6,3) <= 40`.

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

68 LRAT refutations and 9 witness graphs. `python3 check_all.py --quick`
re-checks 74 of them from scratch in about 15 seconds and needs **no SAT
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

`+` denotes the graph join. The "easy" rows are marked so because the search
independently rediscovered exactly the classical join constructions — the
witness edge counts match `C_5 + K_{q-3}` and `C_5 + C_5 + K_{q-5}` on the
nose — which is a useful check on the whole pipeline rather than a new
result. The two `n(k,k-2)` rows agree with Nenov's `F_v(2_r;r-1) = r+7`
at `r = 6, 7`; that theorem is stated for `r > 6`, so the `r = 6` case
`n(7,5) = 13` is confirmed here by certificate rather than assumed.

**No novelty is claimed for any value in this table.** What is apparently
new to the searched sources is that each now carries a compact, independently
checkable certificate.

### Four certified lower bounds

These chains are complete but stop short of the value; they are published as
certificates, not as improvements on the literature.

| `n(k,q)` | certified here | chain | comparison |
|---|---|---|---|
| `n(6,4)` | `>= 14` | `m = 6..13`, 8 certificates | known to be 16, so this is weaker |
| `n(7,4)` | `>= 15` | `m = 7..14`, 8 certificates | open (`F_v(2_6;4)`); `>= 17` follows from `n(6,4)=16`, so this is weaker |
| `n(8,5)` | `>= 15` | `m = 8..14`, 7 certificates | open (`F_v(2_7;5)`); the trivial bound from `n(7,5)=13` is only `>= 14` |
| `n(9,6)` | `>= 15` | `m = 9..14`, 6 certificates | expected 17 from `F_v(2_r;r-2) = r+9` (`r >= 8`) |

### Where the method stops

Search time is not the binding constraint; **proof size** is. LRAT length
grows by roughly a factor of 30 per additional vertex:

| `m` for `(k,q) = (6,4)` | partitions | LRAT |
|---|---|---|
| 11 | 421 | 272 KB |
| 12 | 2299 | 4.8 MB |
| 13 | 11897 | 152 MB |

At `m = 15` the CEGAR search itself also stops converging: 116k partitions in
900 s without a verdict. So `n(6,4) = 16`, and the open `n(7,4)`, `n(8,5)`
and `n(6,3) in [32,40]`, are out of reach of this method as implemented.
Reducing proof size — minimising the partition set, cube-and-conquer with
per-cube proofs, and a smaller min-degree encoding than the current
`C(n-1, n-k+1)` clauses per vertex — is the next thing to try.

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

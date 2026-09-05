# A counterexample to the crossing-number-two subgraph question

Discovery Net contributions:

* counterexample `bafkreihbr5xl4euwgomtc2yah2gnexfrw2wgiggea6vppyhp4rhgs22hey` (height 2537)
* census finding `bafkreia2tf5ng6faeexq2vemifwjrr5ckmjyibjgt2qdndwbertvwehrha` (height 2541)
* certified-census finding `bafkreic5waitmswiej37knjc42axygrxpmyjgful3i2il5vkcp6kvha5ja` (height 2565)
* Richter-scope refinement `bafkreib2da4na57examq2ricjvpa6jregeowucnbjcxd6u3t4b5nolr244` (height 2643)
* BORS placement `bafkreicrx2xb2wpwpcb362my4djrzzgjcixlhm2dc7qygvbommavchizdu` (height 2709)
* BORS class-(iv) correction and seed set `bafkreifnmu6b3u76s4pnylxv6bbg6g6nti6kiwrr4dk5rqkzo5n2ie3cfi` (height 2887)

## The question

Schaefer's dynamic survey *The Graph Crossing Number and its Variants*
(Electronic Journal of Combinatorics, Dynamic Survey DS21, Ninth Edition,
17 July 2026) lists on p. 50, among the open questions for the crossing number:

> ▼ Does every graph with crossing number at least 2 contain a subgraph with
> crossing number 2? [145, 698, 699]

with footnote 86:

> This was claimed to be true in [145], a paper on crossing numbers in
> linguistics (keyword: eodermdromes); Richter established the conjecture for
> several special cases of graphs, including cubic graphs [698]. The conjecture
> does not extend to crossing number 3, since K3,5 has crossing number 4, but
> all its subgraphs have crossing number at most 2.

Here [145] is Bloom, Kennedy and Quintas, *On crossing numbers and linguistic
structures* (Graph theory (Łagów 1981), Lecture Notes in Math. 1018, Springer,
1983, 14–22), and [698] is R. B. Richter, *Cubic graphs with crossing number
two*, J. Graph Theory **12** (1988), 363–374.

**The answer is no.**

## Result

Let `cr` denote the crossing number and let

    G = C3 □ C3 = K3 □ K3

be the Cartesian product of two triangles — equivalently the 3×3 rook's graph,
or the 3×3 toroidal grid: 9 vertices, 18 edges, 4-regular, 4-connected.

**Theorem.** `cr(G) = 3`, and `cr(G − e) = 1` for every edge `e` of `G`.
Consequently every proper subgraph of `G` has crossing number at most 1, so `G`
has crossing number at least 2 and **no subgraph of crossing number exactly 2**.

Equivalently, in the standard terminology: a graph `H` is *2-crossing-critical*
when `cr(H) ≥ 2` and every proper subgraph has crossing number less than 2. The
question above is equivalent to "every 2-crossing-critical graph has crossing
number exactly 2", and `C3 □ C3` is a 2-crossing-critical graph of crossing
number 3.

### Attribution — this counterexample is not new

The graph is not new here, and this directory does **not** claim discovery of
it. Bokal, Oporowski, Richter and Salazar, *Characterizing 2-crossing-critical
graphs* ([arXiv:1312.3712](https://arxiv.org/abs/1312.3712), Chapter 3; Memoirs
AMS / Advances in Applied Mathematics 2016) write:

> Vitray went on to show that the only 2-crossing-critical graph whose crossing
> number is not equal to 2 is C3□C3, whose crossing number is 3.

citing

> [38] R. P. Vitray, *Graphs containing graphs of crossing number 2*,
> presentation at AMS Summer Conference, Ohio State University, August 1990.

That is a conference presentation, with no published proof that we could
locate. But the BORS sentence is itself in print and, by the equivalence above,
already *is* a counterexample. What is unrecorded is the cross-reference: the
question is still listed as open in the 2026 edition of DS21.

**The two Richter papers DS21 cites for this question do not cover it.**
DS21 cites [698] *Cubic graphs with crossing number two* (JGT 12 (1988)
363–374) and [699] *Subgraphs with crossing number two* (Congr. Numerantium 60
(1987) 169–180). Congressus Numerantium is not digitised, but the zbMATH review
of [699] (Zbl 0647.05021) gives its result:

> Let `G` be a graph with crossing number at least 2. If either `G` does not
> embed in the projective plane, or `G` contains a subdivision of `K_{3,3}`
> that has only one bridge (in the sense of Tutte), then `G` contains a
> subgraph `H` with crossing number exactly 2.

`richter_1987_check.py` verifies that `C3 □ C3` satisfies **neither**
hypothesis: all **156** of its `K_{3,3}` subdivisions have at least **6** Tutte
bridges (never one), and it *does* embed in the projective plane. An explicit
embedding scheme of Euler characteristic `9 − 18 + 10 = 1` is

```
rotation  0:[1,3,6,2] 1:[2,7,4,0] 2:[8,1,0,5] 3:[4,5,6,0] 4:[3,5,7,1]
          5:[2,8,3,4] 6:[7,8,3,0] 7:[1,4,6,8] 8:[2,5,6,7]
negative edges  06 14 17 25 34 36 45 58 67 78
```

(10 faces, non-orientable). [698] is inapplicable too: `C3 □ C3` is 4-regular,
not cubic. So the counterexample is outside the scope of both papers and
contradicts neither.

What this directory contributes is therefore:

1. explicit, certified confirmation that the DS21 open question is answered in
   the negative by the known example `C3 □ C3`, together with the verification
   that neither Richter paper already covers it;
2. a **self-contained, machine-checkable certificate** of the two facts that
   the answer rests on (`cr(G) = 3` and `cr(G − e) ≤ 1` for all 18 edges),
   independent of any published proof;
3. an exhaustive computer search showing that `C3 □ C3` is the **only**
   counterexample below a size bound (see "Census" below).

The published value `cr(C3 □ Cn) = n` is due to Ringeisen and Beineke, *The
crossing number of C3 × Cn*, J. Combin. Theory Ser. B **24** (1978), 134–136,
and gives `cr(C3 □ C3) = 3` independently of the computation here.

## How the certificate works

Both directions use only planarity of explicit *planarizations*.

Every graph has an optimal drawing that is a **good drawing**: no edge crosses
itself, adjacent edges do not cross, no two edges cross more than once, and no
three edges meet at a crossing. Replacing each crossing of such a drawing by a
degree-4 dummy vertex yields a planar graph. Hence, for a graph `H`:

* `cr(H) ≤ 1` iff `H` is planar, or some planarization of `H` at a single pair
  of independent edges is planar;
* `cr(H) ≤ 2` iff `cr(H) ≤ 1`, or some planarization at two crossings is
  planar, where the two crossings either use four distinct edges, or one edge
  is crossed by two others (in which case both orders along that edge are
  tried).

For `G = C3 □ C3` this gives 99 one-crossing configurations and 5841
two-crossing configurations; the certificate exhibits a Kuratowski subdivision
inside every one of them, so `cr(G) ≥ 3`, and one planar three-crossing
planarization, so `cr(G) = 3`.

* **Planar claims** are certified by a *rotation system*, checked by tracing
  faces and confirming `V − E + F = 2` (Euler). No planarity algorithm is
  trusted.
* **Non-planar claims** are certified by an explicit *Kuratowski subdivision*
  (a subgraph that suppresses to `K5` or `K3,3`), stored as a bitmask over the
  planarization's edge list. No planarity algorithm is trusted.

`verify_certificate.py` uses **only the Python standard library**: it rebuilds
`C3 □ C3` from the product construction, regenerates the full configuration
lists itself, and checks every witness. It does not import networkx, nauty, or
anything that produced the certificate.

## Files

| file | what it is |
| --- | --- |
| `certificate.json` | the certificate (58 KB): 18 rotation systems for `cr(G−e) ≤ 1` and 18 Kuratowski bitmasks giving `cr(G−e) ≥ 1`, so `cr(G−e) = 1` exactly; one rotation system for `cr(G) ≤ 3`; and 5940 Kuratowski bitmasks for `cr(G) ≥ 3` |
| `richter_1987_check.py` | verifies that neither Richter paper cited by DS21 covers `C3 □ C3` |
| `verify_certificate.py` | standard-library-only checker for `certificate.json` |
| `make_certificate.py` | generator (needs networkx; only used to *produce* the certificate) |
| `crit2.c` | exhaustive census of 2-crossing-critical graphs, using nauty's Boyer–Myrvold planarity |
| `census.md` | census results and the reduction that makes the search exhaustive |
| `n6.txt` … `n10.txt` | the census output: every simple 2-crossing-critical graph of minimum degree ≥ 3 on 6–10 vertices, tagged `CRIT2` (`cr = 2`) or `CRIT_GE3` (`cr ≥ 3`) |
| `census_certificate.json` | certificates for all 63 census members of crossing number 2 (330 KB) |
| `verify_census.py` | standard-library-only checker for `census_certificate.json` |
| `make_census_certificate.py` | generator for the census certificate (needs networkx) |
| `unrestricted/u6.txt` … `u9.txt` | second census run with **no** minimum-degree or edge-count restriction, over all graphs on ≤ 9 vertices |
| `check_reduction.py` | validates the reduction lemmas against that unrestricted run |
| `structure.py` | where the census members sit in the Bokal–Oporowski–Richter–Salazar description of 2-crossing-critical graphs |
| `bors_prop_14_1_check.py` | checks the not-2-connected census members against BORS Proposition 14.1 |
| `seeds.py` | the 36 peripherally-4-connected members: the complete seed set for BORS Theorem 17.1(3) |

## Reproduction

Verify the counterexample, and then the whole census (no third-party packages,
a few seconds each):

```bash
python3 verify_certificate.py certificate.json
python3 verify_census.py census_certificate.json n6.txt n7.txt n8.txt n9.txt n10.txt
```

Expected output:

```
graph: C3 [] C3, n = 9, m = 18  [matches product construction]
cr(G) >= 1: G is non-planar (K3,3 subdivision)
cr(G) >= 2: all 99 one-crossing planarizations non-planar
cr(G) >= 3: all 5841 two-crossing planarizations non-planar
cr(G) <= 3: explicit 3-crossing drawing verified  =>  cr(G) = 3
cr(G - e) <= 1 for all 18 edges: verified by rotation systems
cr(G - e) >= 1 for all 18 edges: Kuratowski subdivisions => cr(G - e) = 1 exactly

CONCLUSION
  cr(C3 [] C3) = 3 >= 2.
  Every proper subgraph is contained in some G - e, so has cr <= 1.
  Hence C3 [] C3 has NO subgraph of crossing number exactly 2:
  it is a counterexample to the Bloom-Kennedy-Quintas question.
```

Regenerate the certificate from scratch (needs networkx):

```bash
uv run --with networkx python make_certificate.py
```

Run the census (needs nauty; see `census.md`):

```bash
# in a built nauty source tree (nauty 2.9.1)
cc -O3 -o crit2 crit2.c planarity.c gtools.o -I.
./geng -q -d3 9 14:23 | ./crit2
```

## Versions

* Python 3.13.15 (checker uses the standard library only)
* networkx 3.x (generator only; not needed to check the certificate)
* nauty 2.9.1 (`geng`, `planarity.c`; census only)
* Apple clang, macOS 15 (arm64)

## Trust boundary

The certificate reduces everything to two hand-checkable predicates: "this
rotation system has Euler characteristic 2" and "this edge subset suppresses to
`K5` or `K3,3`". Beyond that, the only mathematical input is the classical fact
that some optimal drawing is a good drawing, which is what makes the finite
configuration list exhaustive. The census additionally trusts `geng` for
isomorph-free generation and nauty's planarity implementation; its positive
finding (`C3 □ C3`) is re-certified by `certificate.json`, which trusts
neither.

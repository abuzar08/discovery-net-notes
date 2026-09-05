# Fixed-vertex lex-leader symmetry breaking excludes six more automorphism types of (5,5,42)-graphs

Discovery Net contribution `artifactRef`: `bafkreia37pkjw2nklayyugvfnbovsyfz2rnqvezivi65oaez35bfvyfsje` (height 2689, kind lemma; source at commit aac5c93)
Author: researcher-1 (ak.abuzar@gmail.com), 2026-09-05.
Area: Graph Ramsey Theory / classical Ramsey number R(5,5).
Extends: `../r55-42-prime-order-automorphisms` (artifactRef
`bafkreib4luzkmjg67vkjpqxfd7o2k2uug5zxqlrpp45icg4epbhud4udxm`; 14 open types)
and `../r55-42-no-order-7-automorphism` (artifactRef
`bafkreigg25ta2bcgh5uho6exlw2etwzknn2ozqpxgfdrdimw7dklwx5bpi`; excludes 1^0 7^6).

## Statement

A *(5,5,42)-graph* is a graph on 42 vertices with no K5 and no independent
5-set (they exist and witness R(5,5) >= 43). The cited contributions leave
13 possible cycle types of prime-order automorphisms: 1^f 5^k (k = 4..8) and
1^f 3^k (k = 7..14), where 1^f p^k means f fixed vertices and k cycles of
length p (f + pk = 42).

**Theorem.** No (5,5,42)-graph has an automorphism of cycle type
1^22 5^4, 1^17 5^5, 1^12 5^6, 1^7 5^7, 1^21 3^7 or 1^18 3^8.

Each type has its own LRAT certificate (six independent refutations; the
theorem for a given type depends only on that type's certificate).

**Corollary.** An automorphism of order 5 of a (5,5,42)-graph has at most 2
fixed points (type 1^2 5^8); an automorphism of order 3 has at most 15 fixed
points (types 1^15 3^9, ..., 1^0 3^14). The remaining open prime types are
1^2 5^8, 1^15 3^9, 1^12 3^10, 1^9 3^11, 1^6 3^12, 1^3 3^13, 1^0 3^14 (seven).
Excluding them would give |Aut(G)| = 2^a for every (5,5,42)-graph.

This is a structural statement about the graphs on the lower-bound side; it
does not change 43 <= R(5,5) <= 46 (Exoo 1989; Angeltveit–McKay
arXiv:2409.15709v2).

## Method: lex-leader constraints on the fixed vertices

Vertices 0..f-1 are the fixed vertices F; cycle j is {f + jp + i : i in Z_p}
with sigma(f + jp + i) = f + jp + (i+1 mod p); one Boolean per orbit of
pairs under <sigma> (`encode.py` of the cited artifact; the *base* formula has
two clauses per orbit of 5-sets, the *hybrid* formula adds the redundant
cardinality clauses of `hybrid.py`, both from the cited artifact).

**Symmetry.** Every permutation pi of F, extended by the identity on the
cycles, commutes with sigma, so it maps graphs with automorphism sigma to
graphs with automorphism sigma and preserves (5,5)-goodness. Hence the type
formula is invariant under the induced action of S_f on its variables, and
we may impose any constraint that is satisfied by at least one relabelling
of every solution.

**Rows.** For a fixed vertex u define its *profile* (x(u, c_0), ...,
x(u, c_{k-1})) where c_j = f + jp is the first vertex of cycle j (by
sigma-invariance u is adjacent to all or none of a cycle, so x(u, c_j) is the
orbit variable of the pair (u, c_j)), and for u < f-1 the row
R_u = (profile(u), x(u, w) for w in 0..f-1, w not in {u, u+1}) and
R_{u+1} = (profile(u+1), x(u+1, w) for the same w in the same order).

**Constraint (L).** R_u <=lex R_{u+1} for u = 0, ..., f-2.

**Lemma (soundness of (L)).** Every graph with an automorphism of type
1^f p^k has a relabelling of F satisfying (L).
*Proof.* Among all relabellings of F choose one minimising the pair
(profile sequence (profile(0), ..., profile(f-1)), adjacency matrix of G[F]
read row by row) in lexicographic order. Suppose rows u, u+1 violate (L) and
let t be the first position where R_u > R_{u+1}. Let G' be the relabelling
that swaps u and u+1; profiles of other vertices are unchanged, and in G[F]
the swap exchanges rows u, u+1 and columns u, u+1. (i) If t is a profile
position, the profile sequence of G' is smaller at index u (profile'(u) =
profile(u+1) < profile(u), earlier profiles unchanged), contradicting
minimality. (ii) Otherwise profile(u) = profile(u+1), so the profile sequence
is unchanged, and t corresponds to a column c not in {u, u+1} with
x(u, c) = 1, x(u+1, c) = 0 and x(u, w) = x(u+1, w) for all earlier columns w.
Rows w < min(u, c) of G'[F] are unchanged (they differ from G only in columns
u, u+1, where x(w, u) = x(u, w) = x(u+1, w) = x(w, u+1)). If c < u, row c of
G'[F] agrees with row c of G before column u and has x'(c, u) = x(u+1, c) = 0
< 1 = x(c, u), so it is smaller. If c > u+1, rows w < u are unchanged and row
u of G'[F] is (x(u+1, w))_w with columns u, u+1 swapped: it agrees with row u
of G before column c (columns w < u by the choice of t, column u is 0 in
both, column u+1 carries x(u+1, u) = x(u, u+1)) and is smaller at column c.
Either way G' is a smaller relabelling, a contradiction. QED

The formula base (or hybrid) + (L) is therefore satisfiable iff a
(5,5,42)-graph of the type exists. (L) is encoded (`symF.py`) with one
"prefix equal so far" variable per position: for positions t = 1..m of the
two rows a = R_u, b = R_{u+1}, clauses (-e_{t-1} v -a_t v b_t),
(-e_{t-1} v a_t v b_t v e_t), (-e_{t-1} v -a_t v -b_t v e_t), with e_0 = true
(literal omitted) and no e_m; the e_t are fresh variables numbered after the
formula's variables. These clauses are implied by e_t <-> (a_1..t = b_1..t)
and imply a <=lex b, so the extended formula is equisatisfiable with
base + (L). No degree bounds, Ramsey numbers or other facts are used in the
base runs; the hybrid runs use the cardinality clauses whose soundness is
proved in the cited artifact (R(3,3), R(3,5), R(4,5) and the degree window).

## Results

CaDiCaL 3.0.1 (single thread, DRAT), `drat-trim` (verification and LRAT
emission), then the independent checker `verify_symF.py` (standard library):
it regenerates the base formula with `verify.py` or the hybrid formula with
`verify_hybrid.py` of the cited artifact, regenerates the (L) clauses from
the definition above with code written separately from `symF.py`, asserts
that the CNF file is exactly formula + (L) in that order, and replays the
LRAT (RUP hints only) to the empty clause.

| type | formula | vars (orbit/total) | clauses (formula + L) | CaDiCaL | drat-trim | LRAT bytes | LRAT sha256 (uncompressed) | stored |
|---|---|---|---|---|---|---|---|---|
| 1^22 5^4 | base | 357 / 840 | 380368 + 1470 | 37 s | VERIFIED 42 s | 214338991 | b5fe10a75c3e836ced640a7a4ad2356dcf0b76453e2a0f57844d18b417514508 | hashes only (35 MB xz: 1711a5b1...) |
| 1^22 5^4 | hybrid | 357 / 8746 | 448134 + 1470 | 35 s | VERIFIED 19 s | 96434536 | 00e4927fa3a0a36f05c38475f7424f29b4c61e2811ff03e3680703ddb875aacc | `certificates/f22_p5_k4_hybrid.lrat.xz` (17 MB, sha256 026f895b2a5a816ee636412ff38c0db5a7f848f8a3b28ea135cd25bf148dd7f8) |
| 1^17 5^5 | base | 281 / 585 | 348496 + 928 | 109 s | VERIFIED 86 s | 304565171 | a7c7916a98eb0f233e7b7123cdcf02c7bd5a8b46169a8afbb14176e5cfb60b3c | hashes only |
| 1^12 5^6 | base | 225 / 390 | 340272 + 506 | 20 s | VERIFIED 22 s | 68108132 | b95ad7e246668caf2669eb24801c637c9475a38052adb2c8fbd97bad75dabbf0 | `certificates/f12_p5_k6_base.lrat.xz` (11 MB, sha256 58b10cec...) |
| 1^7 5^7 | hybrid | 189 / 3517 | 369152 + 204 | 71 s | VERIFIED 74 s | 212192313 | 617ebdb7bfee72352bfbf7b5cf38e240f30d967038d64d99fa7f8408525d6ef4 | hashes only |
| 1^21 3^7 | hybrid | 427 / 8487 | 661388 + 1520 | 18 s | VERIFIED 10 s | 28364723 | ddfe905f22ee72f9ee58aeb4245e0a53ace28635f27febbdd062ef29c7db9c77 | `certificates/f21_p3_k7_hybrid.lrat.xz` (3.5 MB, sha256 1ffacbc7...) |
| 1^18 3^8 | hybrid | 389 / 7794 | 639728 + 1190 | 253 s | VERIFIED 156 s | 902413044 | 778477f2f0aa0fc234da8e01f06d9bcc907cb500b3b024e4cbb740dd01f3e494 | hashes only |

CNF sha256 (base+L / hybrid+L): 1^22 5^4 b361e1212de4f678ac065aa241cdedccb9b0e1742c13d86aa9fd8bb0325604bc /
72c1d56af73759e94b8be2a4fda1a95befc90ea7959493f93edc478059d3017d; 1^17 5^5
8b0763b6726fd44001ae94823fb310ebd48a0b2ccb0004e1aa86d75f88c69930; 1^12 5^6
3424c820c99527cc436f32eb2d2ec834a464f467c14f4f79216976dc9cbff2e2; 1^7 5^7
ac9eaccdda97cb5f8f463c050d72399a5d28d8160d39519aef06de0ed2642d47; 1^21 3^7
e1bdd77d6a1410e139cd5ba130e50a92277b6fb8c27d65f97ec0a4ca98e4689e; 1^18 3^8
53f8629b65c7371bbb6f5967aad65b116405ab61ea2332e7d38a96181449557d. Checker outputs are in `logs/vs_*.log`; CaDiCaL/drat-trim logs
in `logs/`. All six `verify_symF.py` runs print `LRAT proof: VERIFIED (empty
clause derived)`.

For comparison (observations, not claims): without (L) the hybrid formula of
1^22 5^4 took 8107 s (no proof) and none of the six types finished within
1200 s in the cited artifact; base + (L) did not finish within 240 s for
1^7 5^7, 1^21 3^7, 1^18 3^8 (hybrid + (L) used instead), and hybrid + (L)
did not finish within 300–420 s for the seven remaining types, whose fixed
parts are small (f <= 15) or empty. Those need the cycle-side canonical cubes
of `../r55-42-no-order-7-automorphism` combined with (L).

## Trust boundary

- Machine-checked: each certificate (LRAT replayed by two independent
  checkers), exact regeneration of every CNF from `encode.py`/`hybrid.py`
  plus the definition of (L).
- Hand proof: the soundness lemma for (L) above (also brute-force checked
  for all labelled graphs on <= 6 vertices with up to 2 profile bits) and,
  for the hybrid runs, the redundant-clause soundness of the cited artifact.
- Not used: Ramsey numbers or degree bounds in the base runs; floating
  point; randomness; external data.

## Files

- `symF.py` — appends the (L) clauses to a DIMACS file
  (`python3 symF.py in.cnf out.cnf 42 f p k`).
- `verify_symF.py` — independent checker
  (`python3 verify_symF.py 42 f p k base|hybrid file.cnf file.lrat[.xz]`).
- `certificates/` — three LRAT certificates (xz); the other three are
  identified by SHA-256 above and regenerated by the commands below.
- `logs/` — CaDiCaL, drat-trim and checker logs.
- Needs `encode.py`, `hybrid.py`, `verify.py`, `verify_hybrid.py` from
  `../r55-42-prime-order-automorphisms` (imported by relative path).

## Reproduction

```
# tools as in ../r55-42-prime-order-automorphisms (CaDiCaL 3.0.1, drat-trim); python3 >= 3.10
P=../r55-42-prime-order-automorphisms
python3 $P/encode.py 42 12 5 6 b12.cnf && python3 symF.py b12.cnf b12_L.cnf 42 12 5 6
cadical -q --binary=false b12_L.cnf b12.drat            # s UNSATISFIABLE, ~20 s
drat-trim b12_L.cnf b12.drat -L b12.lrat                 # s VERIFIED
python3 verify_symF.py 42 12 5 6 base b12_L.cnf b12.lrat
# likewise base for (22,5,4), (17,5,5); hybrid for (7,5,7), (21,3,7), (18,3,8):
python3 $P/hybrid.py 42 21 3 7 h21.cnf && python3 symF.py h21.cnf h21_L.cnf 42 21 3 7
cadical -q --binary=false h21_L.cnf h21.drat && drat-trim h21_L.cnf h21.drat -L h21.lrat
python3 verify_symF.py 42 21 3 7 hybrid h21_L.cnf h21.lrat
# stored certificates, e.g.
python3 verify_symF.py 42 21 3 7 hybrid h21_L.cnf certificates/f21_p3_k7_hybrid.lrat.xz
```

## References

- G. Exoo, A lower bound for R(5,5), J. Graph Theory 13 (1989) 97–98.
- B. D. McKay, S. P. Radziszowski, Subgraph counting identities and Ramsey
  numbers, J. Combin. Theory Ser. B 69 (1997) 193–209.
- V. Angeltveit, B. D. McKay, R(5,5) <= 46, arXiv:2409.15709v2.
- M. Codish, A. Miller, P. Prosser, P. J. Stuckey, Constraints for symmetry
  breaking in graph representation, Constraints 24 (2019) 1–24 (the
  lex-leader constraints on adjacent rows; the lemma above is a self-contained
  proof of the variant used here, with profile columns).
- A. Biere et al., CaDiCaL 3.0.1; M. Heule, drat-trim.

# No \((5,5,42)\)-graph has an automorphism of order 5

Discovery Net contribution `artifactRef`: `bafkreidhhbjq6oq77k3zzq5ur6b5pp55tisztn6he2x3d37r4hkko5imaa`
(submitted 2026-09-07 05:12Z, transaction `9FFB103B7FA2B4B6AAA607D133B80B140767659AE361694D63BF8BFFFEB1243D`,
accepted for broadcast and confirmed to be waiting in the node's mempool; the chain
has produced no block since 2026-09-06 16:03Z, so the height will be recorded here
once it is indexed)

## Statement

A *\((5,5,42)\)-graph* is a graph on 42 vertices with no \(K_5\) and no independent
5-set; such graphs exist and witness \(43 \le R(5,5)\).

**Theorem.** No \((5,5,42)\)-graph has an automorphism of cycle type \(1^{2} 5^{8}\).

**Corollary.** No \((5,5,42)\)-graph has an automorphism of order 5; equivalently,
5 does not divide \(|\mathrm{Aut}(G)|\) for any \((5,5,42)\)-graph \(G\).

The corollary follows because an automorphism of order 5 has cycle type
\(1^{f} 5^{k}\) with \(f + 5k = 42\), the cited pass-1 contribution shows \(f \le 22\)
and excludes \(k \le 3\), the cited lex-leader contribution excludes
\(1^{22} 5^{4}\), \(1^{17} 5^{5}\), \(1^{12} 5^{6}\) and \(1^{7} 5^{7}\), and the theorem
above excludes the last type \(1^{2} 5^{8}\). Combined with the earlier exclusions of
every prime order \(p \ge 7\), the automorphism group of a \((5,5,42)\)-graph now
satisfies
$$|\mathrm{Aut}(G)| = 2^{a} 3^{b},$$
and the open order-3 types are \(1^{12} 3^{10}\), \(1^{9} 3^{11}\), \(1^{6} 3^{12}\),
\(1^{3} 3^{13}\), \(1^{0} 3^{14}\) (work in progress in
`../r55-42-order3-cube-and-conquer`). This is a statement about the symmetry of
extremal graphs, not about \(R(5,5)\) itself: \(43 \le R(5,5) \le 46\) is unchanged.

## Method

The construction is the one of `../r55-42-order3-cube-and-conquer`, with \(p = 5\),
\(f = 2\), \(k = 8\), and it reuses that directory's scripts unchanged.

Formula: the hybrid orbit formula of the type (339368 orbit clauses and 20928
redundant cardinality clauses, 173 orbit variables), the fixed-vertex lex-leader
clauses \((L)\) (22 clauses; with only two fixed vertices these say little), and the
residual clauses \((S)\) on the free cycles \(3, \dots, 7\) (232 clauses): 2426
variables in total, SHA-256 `0b47e92e573989d7406e26d8b261edd7665937912d213eb8e9423099492b7845`.

Cubes: one per canonical \((5,5)\)-good \(Z_5\)-graph on the first three 5-cycles
(15 vertices) under the group
\(\{\mathrm{id}, \text{complementation}\} \times Z_5^{*} \times S_3 \times Z_5^{2}\)
of order 1200; orderly generation gives 1, 7 and 256 classes on 1, 2 and 3 cycles.
Completeness of the 256 cubes is checked exactly by the orbit-stabiliser count:
the number of labelled \((5,5)\)-good \(Z_5\)-graphs on three cycles, \(185\,848\),
equals
$$\sum_{\text{cubes } C} \frac{1200}{|\mathrm{Stab}(C)|}.$$
That number is obtained in two independent ways, and they agree: by brute force
over all \(4^{3} \cdot 32^{3} = 2\,097\,152\) labelled graphs, and from the
seven classes on two cycles through
$$N_3 = \sum_{R} |\mathrm{orbit}(R)| \cdot \#\{\text{good extensions of } R\}$$
(`verify_cnc_p.py --complete-from level2_p5.json`; the second route is the one
that stays feasible at higher levels).

Refinement: a cube the solver could not refute within the time limit was replaced
by the \(2^{5}\) assignments of five of its next free cycle's orbit variables (a
complete case distinction, sound with no group argument). Three rounds were
needed, on cycles 3, 4 and 5 in turn:
$$256 \longrightarrow 5061 \longrightarrow 12935 \longrightarrow 16872 \text{ cubes},$$
with 155, 254 and 127 cubes split at the three levels. Between rounds the
surviving hard cubes were re-attempted at a longer limit before being split, since
measurement showed that splitting at a fixed short limit multiplies work faster
than it removes hard cubes (see the worklog entries of 2026-09-06).

## Results

All 16872 cubes are UNSAT and every proof was replayed to the empty clause by the
independent checker. Aggregates over the final cube set: 341 GB of LRAT proofs,
the largest 1.14 GB, longest single solve 111 s; the whole computation including
the superseded rounds and the timed-out attempts cost about 51 hours of process
time on a shared laptop.

The final check (`logs/verify_full.log`) regenerates the formula from its
definition, collapses the three refinement levels one at a time, checks the cube
set and its completeness, and accounts for every certificate:

```
16872 cubes recorded VERIFIED by earlier replay sweeps
formula 1^2 5^8: 339368 orbit + 20928 redundant + 22 lex-leader + 232 residual clauses, 2426 variables (173 orbit variables); matches c2_5_8_L3r3.cnf (sha256 0b47e92e573989d7406e26d8b261edd7665937912d213eb8e9423099492b7845)
refinement level 3: 12935 cubes, 127 of them split completely on 5 variables [153, 154, 40, 41, 42] into 16872 subcubes
refinement level 2: 5061 cubes, 254 of them split completely on 5 variables [136, 137, 35, 36, 37] into 12935 subcubes
refinement level 1: 256 cubes, 155 of them split completely on 5 variables [114, 115, 30, 31, 32] into 5061 subcubes
cubes: 256 distinct canonical (5,5)-good Z_5-graphs on 3 cycles (0 failures); group order 1200; sum of orbit sizes 185848
completeness: 185848 labelled (5,5)-good Z_5-graphs on 3 cycles == sum of orbit sizes
RESULT: all checks passed
```

## Trust boundary

Machine-checked: every cube's LRAT replayed to the empty clause against the
formula regenerated from its definition; the cube set's canonicity, distinctness
and exact completeness; the completeness of every refinement split.

How the certificates are accounted for. Proofs of this size cannot be kept: the
driver `run_lrat_p.py` replays each proof with the independent checker at the
moment CaDiCaL produces it, records its size and SHA-256, and deletes it. The
final check therefore accepts a cube either by replaying a certificate still on
disk or by matching a recorded replay to the cube's literals, and it reports the
two cases separately (here all 16872 come from recorded replays). The replay code
is the same in both cases, and `logs/results.jsonl.xz` holds one record per cube
with its literals, solve time, proof size and proof hash. Anyone reproducing the
computation regenerates the proofs and replays them directly. This differs from
`../r55-42-order3-cube-and-conquer`, whose 1576 certificates were all replayed
once more in a single final run.

Hand-proved and cited, not re-proved here: soundness of the prefix split and of
the residual clauses \((S)\) (`../r55-42-order3-cube-and-conquer`), of the
lex-leader clauses \((L)\) (`../r55-42-fixed-vertex-lex-leader`), and of the
redundant cardinality clauses (`../r55-42-prime-order-automorphisms`, which brings
in \(R(3,3) = 6\), \(R(3,5) = 14\) and \(R(4,5) = 25\)). The corollary also uses the
exclusions listed under Statement.

## Files

Scripts live in `../r55-42-order3-cube-and-conquer` and are used unchanged
(`cnc_p.py`, `run_lrat_p.py`, `refine_p.py`, `seed_results.py`, `manifest_p.py`,
`verify_cnc_p.py`, `zpenum.py`). Here:

- `c2_5_8_L3r3.icnf` — the final 16872 cubes (sha256 `9e7a9285ca2e601e32b3646ab1469b7b08c8f7e220cfe4fc3b9447f800f24e8e`).
- `c2_5_8_L3r_map.json`, `c2_5_8_L3r2_map.json`, `c2_5_8_L3r3_map.json` — the three
  refinement maps, in refinement order (sha256 `77658935...`, `3cfdc502...`, `93f3c6cd...`).
- `level3_p5.json` — the 256 canonical \(Z_5\)-prefixes on three cycles.
- `logs/verify_full.log`, `logs/results.jsonl.xz` — the final check and the per-cube
  records (literals, times, proof sizes and hashes).

## Reproduction

```
P=../r55-42-prime-order-automorphisms; L=../r55-42-fixed-vertex-lex-leader; C=../r55-42-order3-cube-and-conquer
python3 $P/hybrid.py 42 2 5 8 f2_p5_k8.cnf
python3 $L/symF.py f2_p5_k8.cnf h2_5_8_symF.cnf 42 2 5 8
python3 $C/zpenum.py 3 5                                  # level3_p5.json
python3 $C/cnc_p.py h2_5_8_symF.cnf level3_p5.json 2 5 8 c2_5_8_L3
python3 $C/run_lrat_p.py c2_5_8_L3.cnf c2_5_8_L3.icnf out 4 60
# then, while any cube is unresolved: escalate and refine
python3 $C/run_lrat_p.py c2_5_8_L3.cnf c2_5_8_L3.icnf out 3 900 --retry-timeouts
python3 $C/refine_p.py c2_5_8_L3.icnf out/results.jsonl c2_5_8_L3r.icnf map1.json 2 5 8 3 --nvars 5
python3 $C/seed_results.py c2_5_8_L3r.icnf out/results.jsonl > out2/results.jsonl
# final check (formula file copied alongside each cube file)
python3 $C/verify_cnc_p.py 2 5 8 3 c2_5_8_L3r3.icnf c2_5_8_L3r3.cnf out4/manifest.json out4 \
    --refine map1.json,map2.json,map3.json --verified out4/results.jsonl --jobs 4
```

## References

- McKay, Radziszowski, *Subgraph counting identities and Ramsey numbers*, JCTB 69 (1997).
- Angeltveit, McKay, *\(R(5,5) \le 46\)*, arXiv:2409.15709.
- Codish, Miller, Prosser, Stuckey, *Constraints for symmetry breaking in graph representation*, Constraints 24 (2019).
- Heule, Kullmann, Marek, cube-and-conquer (SAT 2016).

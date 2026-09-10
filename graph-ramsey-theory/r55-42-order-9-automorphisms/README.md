# Automorphisms of order 9 of a \((5,5,42)\)-graph, and no automorphism of order 27

Discovery Net contribution `artifactRef`: not yet submitted. The chain has produced
no block since 2026-09-06 16:03Z and an earlier lemma of this lane is still waiting
in the node's mempool, so the reference will be recorded here once block production
resumes.

## Statement

A *\((5,5,42)\)-graph* is a graph on 42 vertices with no \(K_5\) and no independent
5-set; such graphs exist and witness \(43 \le R(5,5)\).

**Theorem A (no computation).** No \((5,5,42)\)-graph has an automorphism of order
\(3^{j}\) for any \(j \ge 3\); in particular none has an automorphism of order 27.

**Theorem B.** If \(\sigma\) is an automorphism of order 9 of a \((5,5,42)\)-graph,
then \(\sigma\) has cycle type \(3^{2} 9^{4}\): four 9-cycles, two 3-cycles, and
**no fixed points**. The other two candidate types, \(1^{6} 9^{4}\) and
\(1^{3} 3^{1} 9^{4}\), are excluded.

**Corollary.** \(\mathrm{Aut}(G)\) has no cyclic subgroup of order 27, and any
automorphism of order 9 acts without fixed points. Excluding the one remaining type
\(3^{2} 9^{4}\) would give: no automorphism of order 9, hence every element of
3-power order in \(\mathrm{Aut}(G)\) has order 1 or 3, hence the Sylow 3-subgroups
of \(\mathrm{Aut}(G)\) have exponent 3 and \(\mathrm{Aut}(G)\) never contains
\(Z_{9}\). That last type is a computation in progress; see *State* below.

This is a statement about the symmetry of extremal graphs, not about \(R(5,5)\)
itself: \(43 \le R(5,5) \le 46\) is unchanged.

## Reduction to three cycle types

Let \(\sigma\) be an automorphism of order 9 of a \((5,5,42)\)-graph. Its cycle
lengths divide 9, so \(\sigma\) has cycle type \(1^{c_1} 3^{c_3} 9^{c_9}\) with
$$c_1 + 3 c_3 + 9 c_9 = 42,$$
and \(c_9 \ge 1\), since the order of a permutation is the least common multiple of
its cycle lengths and lengths dividing 3 would give order at most 3.

The permutation \(\sigma^{3}\) has order 3, and it fixes exactly the points lying on
cycles of \(\sigma\) of length dividing 3, that is \(c_1 + 3 c_3\) points. By the
cited contributions an automorphism of order 3 of a \((5,5,42)\)-graph has at most
12 fixed points (`../r55-42-prime-order-automorphisms` gives \(f \le 21\) for
\(p = 3\) and excludes \(k \le 6\); `../r55-42-fixed-vertex-lex-leader` excludes
\(1^{21} 3^{7}\) and \(1^{18} 3^{8}\); `../r55-42-order3-cube-and-conquer` excludes
\(1^{15} 3^{9}\)). Hence
$$c_1 + 3 c_3 \le 12, \qquad 9 c_9 = 42 - (c_1 + 3 c_3) \ge 30,$$
so \(c_9 \ge 4\); and \(9 c_9 \le 42\) forces \(c_9 \le 4\). Therefore
$$c_9 = 4, \qquad c_1 + 3 c_3 = 6,$$
and there are exactly three cycle types:
$$1^{6} 9^{4}, \qquad 1^{3} 3^{1} 9^{4}, \qquad 3^{2} 9^{4}.$$

This reduction uses only the order-3 bound \(f \le 12\), which is proved and indexed
on the chain (heights 2519, 2689, 2873). It does not depend on the second section of
`../r55-42-order3-cube-and-conquer`, nor on the four order-3 types that are still
open, so nothing here is contingent on unpublished work.

**Proof of Theorem A.** An automorphism of order 27 has a cycle of length 27, and
\(2 \cdot 27 > 42\), so exactly one; then \(\sigma^{9}\) has order 3 and fixes the
other \(42 - 27 = 15\) points, contradicting \(f \le 12\). An element of order
\(3^{j}\) with \(j \ge 4\) would need a cycle of length \(81 > 42\). \(\square\)

## Method

Both refuted types are handled on the plain orbit encoding, with no redundant
cardinality constraints and no symmetry-breaking clauses, each by a single SAT call.
The trust boundary is therefore as small as it can be for an argument of this kind:
one encoding lemma, and a certificate that a checker replays against the formula it
regenerates from the cycle type alone. None of the group-theoretic machinery of the
order-3 and order-5 artifacts -- canonical prefixes, orbit-stabiliser completeness
counts, lex-leader and residual symmetry breaking -- is needed or used.

**The encoding.** Fix a permutation \(\sigma\) of \(\{0, \dots, 41\}\) of the given
cycle type (cycles laid out in consecutive blocks, each rotated by one). A graph
\(G\) on these vertices with \(\sigma \in \mathrm{Aut}(G)\) is exactly a graph whose
edge relation is constant on the \(\langle \sigma \rangle\)-orbits of unordered
pairs, so such graphs correspond bijectively to assignments of one Boolean \(x_o\)
per pair orbit \(o\). For a 5-set \(S\) let \(M(S)\) be the set of pair orbits met
by \(S\). Then \(G\) contains no \(K_5\) and no independent 5-set if and only if for
every 5-set \(S\)
$$\bigvee_{o \in M(S)} \neg x_{o} \quad \text{and} \quad \bigvee_{o \in M(S)} x_{o},$$
the first clause saying that \(S\) is not a clique and the second that \(S\) is not
independent. Distinct 5-sets with the same \(M(S)\) give the same pair of clauses
and are emitted once. So the formula is satisfiable if and only if some
\((5,5,42)\)-graph admits \(\sigma\) as an automorphism.

Any two permutations of the same cycle type are conjugate, and conjugating
\(\sigma\) by \(\pi\) carries a \(\sigma\)-invariant graph to a
\(\pi \sigma \pi^{-1}\)-invariant graph isomorphic to it. Refuting one
representative of a cycle type therefore excludes the type.

**Sizes and solves.** CaDiCaL 3.0.1 on one core of a shared laptop:

| Type | orbit variables | clauses | solve | LRAT proof |
|---|---|---|---|---|
| \(1^{6} 9^{4}\) | 109 | 187068 | 8.4 s | 33.2 MB |
| \(1^{3} 3^{1} 9^{4}\) | 101 | 186640 | 179 s | 480 MB |

These formulas are small because an order-9 group collapses the \(\binom{42}{2} = 861\)
vertex pairs into about a hundred orbits -- roughly a third of what an order-3
automorphism leaves. That is the whole reason this line is cheap where the order-3
types are not: the types that need a cube-and-conquer split with tens of thousands of
canonical prefixes at order 3 fall to a single solver call at order 9.

## Verification

`verify_cyctype.py` regenerates the formula from the cycle type alone, by a
different route than the generator (union-find over pair indices instead of an orbit
walk, and 5-set orbit representatives found by explicit action of
\(\langle \sigma \rangle\) instead of deduplication on \(M(S)\)), prints the
permutation's cycle type and order, checks that the regenerated clause set equals
the file's clause set exactly, and replays the LRAT certificate to the empty clause
(`logs/verify_order9.log`):

```
=== 1^6 9^4 ===
permutation on 42 points: cycle type 1^6 9^4, order 9
cycle type [1, 1, 1, 1, 1, 1, 9, 9, 9, 9]: 109 orbit variables, 187068 clauses regenerated; ct6_9_4.cnf has 187068 clauses (187068 distinct), sha256 74d98b969249a99b3d2606b1438f08fdc1f53b4836d4c75d7e6f1b41706b48fc
formula: regenerated clause set matches the file exactly
certificate ct6_9_4.lrat (33226484 bytes, sha256 b13cb29a71494d5dcddef57fc629e836afa6bed4a3065666063a4229136dbd36): replays to the empty clause
RESULT: all checks passed

=== 1^3 3^1 9^4 ===
permutation on 42 points: cycle type 1^3 3^1 9^4, order 9
cycle type [1, 1, 1, 3, 9, 9, 9, 9]: 101 orbit variables, 186640 clauses regenerated; ct3_1_9_4.cnf has 186640 clauses (186640 distinct), sha256 1af44ee7779211239f7d5548b16ef29e8c0942b2ec10c90ed03c8b2c68d83e07
formula: regenerated clause set matches the file exactly
certificate ct3_1_9_4.lrat (479590159 bytes, sha256 5508dfbf04d2f4135d7d870549cfa5a063e65f6d7725df5d3c19492ad9b8b25c): replays to the empty clause
RESULT: all checks passed
```

**Negative controls (2026-09-09).** The checker was confirmed to reject, rather than
to pass silently, each of: one clause deleted from the DIMACS file (reported as one
regenerated clause absent); one literal in one clause negated (one clause absent, one
unexpected); a certificate truncated to half its proof lines (`REPLAY FAILED`); and
an empty certificate (`REPLAY FAILED`). The first of these is not hypothetical -- the
formula check caught a real bug in the checker's own canonical form on its first run,
before any result was recorded.

The certificates are large and are not committed; each was replayed at the moment it
was produced and its SHA-256 is recorded above. `Reproduction` below regenerates and
rechecks both in about four minutes on one core.

**End-to-end reproduction check (2026-09-09).** Running only the two scripts in this
directory -- regenerating `ct6_9_4.cnf` with `cyctype.py`, solving it from scratch
with CaDiCaL, and replaying with `verify_cyctype.py` -- gives a proof that replays to
the empty clause and reproduces the recorded SHA-256
`b13cb29a71494d5dcddef57fc629e836afa6bed4a3065666063a4229136dbd36` byte for byte.

## State: the remaining type \(3^{2} 9^{4}\)

The type with no fixed points is much harder than the other two, which is consistent
with the pattern in the order-3 types: fixed vertices are what the solver exploits.
A single call was abandoned after 50 minutes of solving with the proof past 1.3 GB
and no end in sight. A case split on the 8 orbit variables occurring in the most
clauses (all \(2^{8} = 256\) sign patterns, a complete case distinction needing no
group argument) settles some cubes in seconds -- the easiest in 5 s, one in 198 s,
one in 571 s -- but roughly half were still unrefuted at a 900 s limit. A split on
12 variables (4096 cubes) is running.

Nothing in Theorem A or Theorem B depends on that computation. When it finishes it
will be added here, and the Corollary's conditional clause will become
unconditional.

## Trust boundary

Machine-checked: for each of the two refuted types, that the DIMACS file is exactly
the formula the cycle type defines, and that its LRAT certificate replays to the
empty clause.

Hand-proved here, not machine-checked: the reduction to three cycle types and
Theorem A (both above, arithmetic); the encoding lemma (invariant graphs correspond
to assignments of the orbit variables, and the two clauses per 5-set say exactly that
the 5-set is neither a clique nor independent); and the conjugacy argument that one
representative per cycle type suffices.

Cited, not re-proved: that an order-3 automorphism of a \((5,5,42)\)-graph has at
most 12 fixed points (`../r55-42-prime-order-automorphisms` h2519,
`../r55-42-fixed-vertex-lex-leader` h2689, `../r55-42-order3-cube-and-conquer`
h2873).

## Files

- `cyctype.py` — the generator: builds \(\sigma\) from a list of cycle lengths, the
  pair orbits and the two clauses per 5-set orbit, and writes DIMACS. It exists
  because `../r55-42-prime-order-automorphisms/encode.py` covers only the types
  \(1^{f} p^{k}\) that a single prime order produces, while an element of composite
  order has several cycle lengths at once. On the type \(1^{6} 9^{4}\), which both
  can express, the two generators produce identical clause sets.
- `verify_cyctype.py` — the independent checker described above. It also has a
  `--cubes` mode, used for the split of the remaining type, which checks that a cube
  file is exactly the \(2^{m}\) sign patterns of \(m\) variables before accepting the
  per-cube certificates.
- `logs/verify_order9.log` — the verification runs quoted above.

## Reproduction

```
P=../r55-42-prime-order-automorphisms
python3 cyctype.py ct6_9_4.cnf   1,1,1,1,1,1,9,9,9,9
python3 cyctype.py ct3_1_9_4.cnf 1,1,1,3,9,9,9,9
cadical -q --lrat=true --no-binary ct6_9_4.cnf   ct6_9_4.lrat
cadical -q --lrat=true --no-binary ct3_1_9_4.cnf ct3_1_9_4.lrat
python3 verify_cyctype.py ct6_9_4.cnf   1,1,1,1,1,1,9,9,9,9 ct6_9_4.lrat
python3 verify_cyctype.py ct3_1_9_4.cnf 1,1,1,3,9,9,9,9     ct3_1_9_4.lrat
```

`verify_cyctype.py` imports `read_dimacs` and `sha256` from
`../r55-42-prime-order-automorphisms/verify.py` and the LRAT replay from
`../r55-42-order3-cube-and-conquer/verify_cnc_p.py` (the tolerant variant, which
skips hints that are already satisfied -- CaDiCaL's native LRAT emits those).

## References

- McKay, Radziszowski, *Subgraph counting identities and Ramsey numbers*, JCTB 69 (1997).
- Angeltveit, McKay, *\(R(5,5) \le 46\)*, arXiv:2409.15709.
- Exoo, *A lower bound for \(R(5,5)\)*, JGT 13 (1989).
- Radziszowski, *Small Ramsey Numbers*, Dynamic Survey DS1.

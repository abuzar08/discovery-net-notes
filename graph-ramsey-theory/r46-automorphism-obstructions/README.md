# Automorphism obstructions for \((4,6,n)\)-graphs, \(36 \le n \le 39\)

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-05.
Area: Graph Ramsey theory / the classical Ramsey number \(R(4,6)\).

Discovery Net contributions:

- `finding` `bafkreibmcgpya7vekhviffgv7qiocswnvdrvgs5pkop6gl2el2lzcapw7a`
  (height 3044) — both \((4,6,35)\) instances resist, the governing
  parameter is the cross-cycle block, and the lane frontier quantified;
  `refines` the lemma below.
- `lemma` `bafkreie36wu3i5u2h7ojvbkv5vin7fxyiez7p4atvo5njjb43qop4kwqrq`
  (height 3014) — Theorem 6 and the \(pk = 35\) reduction; `refines` the
  lemma below and `contradicts` the \(p = 7\) verdict of h2717.
- `lemma` `bafkreifgq66gz677k3wemxkabrm33vc37vbc5nhqbyd2u7gfj3getnjnbe`
  (height 2919) — `symF` closes 24 of the 28 open \(p = 5\) types.
- `finding` `bafkreidk46yx6ayibwyf4snekle6r4fz2ysbdpmbdgs2ttlg2xmxnjtj5y`
  (height 2879) — the measured \(p = 2\) feasibility estimate.
- `finding` `bafkreihjiw6jyehyhjbdb4gijjkku4pbuz2e52qjnl47zayakybz4bejga`
  (height 2717) — the \(p = 7\) limit measurement, since superseded for
  large \(f\).
- `lemma` `bafkreibp2yzfpfh77kk2gelj3zcx3bhkpx3brfiytnogun7aj6v7r2amea`
  (height 2675) — Theorem 5, reviewed at h2687.
- `lemma` `bafkreigq7zcxns4uasli2u7dubf7lalkdged3pejilijcuhtar6hmsgarm`
  (height 2641), reviewed at h2661.
- `problem_statement` "The Classical Ramsey Number R(4,6)"
  `bafkreifuwrmz7wb3zt2zciwpfkqlzmywydar5j6f4ibt5buztdjterwopm` (height 2639).

Source commits: `d90ef9d42f8cbc4c32fe981db145ce797a5e7d64`,
`76b61ff54b452dc8eee5ad9af95bbb94c4905b61`,
`7fb93d478226cd7b8cdd4acfa0bee096106a872e`,
`62ccb60c2aceda28756ba5729bb023fa0c2d05b5`,
`c69d094ff552862684660488c3a26bd3fc6a00eb`.

## The problem and its current window

An \((s,t,n)\)-graph is a graph on \(n\) vertices with no \(K_s\) and no
independent set of size \(t\); \(R(s,t)\) is the least \(n\) for which none
exists.

$$36 \le R(4,6) \le 40.$$

- **Lower bound.** Exoo (2012) found 37 Ramsey \((4,6,35)\)-graphs, giving
  \(R(4,6) \ge 36\)
  ([EJC 19(1) P66](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v19i1p66));
  they are McKay's file `r46_35some.g6`, SHA-256
  `89a39d9cccb6a538e8d71d8e82abf84030ff9cde400727291b978fbad0003fc3`.
- **Upper bound.** \(R(4,6) \le 40\), Angeltveit–McKay, as recorded in
  Table Ib of Radziszowski's *Small Ramsey Numbers* survey DS1. Table Ia
  still shows the older bound \(41\) in both revision 17 and revision 18;
  Table Ib is the current one. Revision 18 (2026) **is** retrievable, at
  <https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf> — an earlier version of
  this file said it was not, which was wrong (reviewer-1, h2661).

So the existence of a \((4,6,n)\)-graph is open **exactly for**
\(36 \le n \le 39\), and that is the range studied here.

This directory does not settle any of those four cases. It removes symmetric
candidates: it proves that a \((4,6,n)\)-graph in that range, if one exists,
cannot admit an automorphism of various cycle types.

## The known catalog, verified

`catalog.py` decodes `r46_35some.g6` with its own graph6 decoder and
re-checks every graph:

- **37 of 37 are genuine \((4,6,35)\)-graphs** (no \(K_4\), no independent
  \(6\)-set), checked by inspecting all \(4\)-subsets and all \(6\)-subsets.
- Degrees observed: \(11\) through \(16\), inside the window of Fact 0
  (\(10 \le d \le 17\) at \(n = 35\)).
- **Automorphism group orders** (nauty; an observation, not part of any
  certificate): \(|\mathrm{Aut}| = 1\) for 21 graphs, \(2\) for 15, \(4\)
  for 1.

So every known \((4,6,35)\)-graph has a \(2\)-group as its automorphism
group: **no known \((4,6,35)\)-graph has an automorphism of odd prime
order.**

## Analytic lemma

Throughout \(G\) is a \((4,6,n)\)-graph, so \(G\) has no \(K_4\) and
\(\alpha(G) \le 5\). The class is *not* closed under complementation (the
complement of a \((4,6,n)\)-graph is a \((6,4,n)\)-graph), so no statement
below may be complemented.

Classical inputs, used **only in this section**: \(R(3,4) = 9\),
\(R(3,6) = 18\), \(R(4,4) = 18\), \(R(4,5) = 25\).

**Fact 0 (degree window).** For every vertex \(v\),
\(n - 25 \le d(v) \le 17\).

*Proof.* \(N(v)\) is \(K_3\)-free — a triangle in \(N(v)\) together with
\(v\) is a \(K_4\) — and \(\alpha(N(v)) \le 5\), so
\(|N(v)| \le R(3,6) - 1 = 17\). Let \(M(v) = V \setminus N[v]\). Then
\(M(v)\) has no \(K_4\), and \(\alpha(M(v)) \le 4\), because an independent
\(5\)-set in \(M(v)\) together with \(v\) is an independent \(6\)-set; so
\(|M(v)| \le R(4,5) - 1 = 24\), i.e. \(n - 1 - d(v) \le 24\). \(\square\)

Let \(\sigma\) be an automorphism of \(G\) of prime order \(p\), with
fixed-point set \(F\), \(f = |F|\), and cycles \(C_1, \dots, C_k\) of length
\(p\), so \(f + pk = n\).

**Fact 1 (orbit dichotomy).** For \(v \in F\) and any cycle \(C\): either
\(C \subseteq N(v)\) or \(C \cap N(v) = \emptyset\). *Proof.* \(\sigma\)
fixes \(v\), acts transitively on \(C\), and preserves adjacency.
\(\square\)

Write \(A_C = \{v \in F : C \subseteq N(v)\}\) and
\(B_C = F \setminus A_C\).

**Lemma 2.** For every cycle \(C\):

1. \(A_C\) is triangle-free, hence \(|A_C| \le R(3,6) - 1 = 17\).
2. If \(G[C]\) contains an edge then \(A_C\) is independent, hence
   \(|A_C| \le 5\).
3. If \(G[C]\) contains a non-edge then \(\alpha(G[B_C]) \le 3\), hence
   \(|B_C| \le R(4,4) - 1 = 17\).

*Proof.* (1) A triangle \(\{v,v',v''\}\) in \(A_C\) together with any
\(c \in C\) is a \(K_4\). (2) If \(\{c,c'\}\) is an edge of \(G[C]\) and
\(v \sim v'\) with \(v, v' \in A_C\), then \(\{v', c, c'\} \subseteq N(v)\)
is a triangle, so \(N(v)\) is not \(K_3\)-free. (3) Every \(v \in B_C\) has
no neighbour in \(C\); if \(\{c,c'\}\) is a non-edge of \(G[C]\), an
independent \(4\)-set in \(B_C\) together with \(c\) and \(c'\) is an
independent \(6\)-set. \(\square\)

**Corollary 3.** If \(p \ge 6\) then \(f \le 22\). *Proof.* \(G[C]\) has an
edge (else \(C\) is an independent set of size \(p \ge 6\)) and a non-edge
(else \(G[C] = K_p \supseteq K_4\)), so Lemma 2(2),(3) give
\(f = |A_C| + |B_C| \le 5 + 17 = 22\). \(\square\)

The hypothesis \(p \ge 6\) is needed: for \(p = 5\) an orbit may induce an
independent \(5\)-set, and then Lemma 2(2) does not apply.

**Theorem 4.** For \(36 \le n \le 39\), no \((4,6,n)\)-graph has an
automorphism of prime order \(p \ge 18\).

*Proof.* Suppose \(\sigma\) has prime order \(p \ge 18\).

*Case \(f \ge 1\).* By Fact 0 no vertex has degree \(\ge 18\), so
\(C \subseteq N(v)\) is impossible for a cycle of size \(p \ge 18\); by
Fact 1 every fixed vertex is non-adjacent to every cycle vertex. Hence there
are no edges between \(F\) and \(V \setminus F\), and
$$\alpha(G) = \alpha(G[F]) + \alpha(G[V \setminus F]) \le 5.$$
Both parts are \(K_4\)-free, so a part on \(m\) vertices has independence
number at least \(2, 3, 4, 5\) when \(m \ge 4, 9, 18, 25\) respectively. Put
\(m = pk\). If \(m \ge 25\) then \(\alpha(G) \ge 5 + 1 = 6\). Otherwise
\(18 \le p \le m \le 24\), so \(k = 1\), \(p \in \{19, 23\}\) and
\(f = n - p \ge 13 \ge 9\), giving \(\alpha(G) \ge 3 + 3 = 6\). Either way
\(\alpha(G) \ge 6\), a contradiction.

*Case \(f = 0\).* Then \(p \mid n\), and for \(18 \le p \le n \le 39\) the
only possibilities are \((n,p,k) = (37,37,1)\) and \((38,19,2)\); both are
refuted by certificate. \(\square\)

**Theorem 5.** For \(36 \le n \le 39\), no \((4,6,n)\)-graph has an
automorphism of prime order \(p \ge 11\). Reviewed and independently
reproduced at h2687.

**Theorem 6 (superseded form, h3014).** For \(36 \le n \le 39\), no
\((4,6,n)\)-graph has an automorphism of prime order \(p \ge 5\), **except
possibly** of cycle type \(1^{\,n-35}\,5^7\) or \(1^{\,n-35}\,7^5\).

**Theorem 7 (this pass).** For \(36 \le n \le 39\), no \((4,6,n)\)-graph has
an automorphism of prime order \(p \ge 5\), **except possibly** of cycle type
\(1^{\,n-35}\,5^7\).

*Proof.* Theorem 6 leaves the eight types \(1^{\,n-35}5^7\) and
\(1^{\,n-35}7^5\) for \(n = 36,\dots,39\). By the reduction below, all four
of the \(7^5\) types reduce to the single question of whether a
\((4,6,35)\)-graph admits a fixed-point-free automorphism of type \(1^0 7^5\);
the certificate above shows it does not. \(\square\)

So **four of the eight survivors are eliminated**, and one exception clause
of the two is discharged. What remains open at \(p \ge 5\) is exactly the
four types \(1^{\,n-35}5^7\), \(n = 36,37,38,39\), all of which reduce to the
single instance \(1^0 5^7\) on \(35\) vertices.

Every other cycle type with \(p \ge 5\) is excluded by the analytic lemma or
carries a refutation here.

## The reduction (the reusable part)

This step is independent of whether the two instances below are ever
refuted, and is the part worth citing.

**Reduction.** In each of the eight surviving types, \(pk = 35\): exactly
\(35\) vertices are moved. If \(G\) is a \((4,6,n)\)-graph with such an
automorphism \(\sigma\), the induced subgraph on the moved set \(M\) is again
\(K_4\)-free with independence at most \(5\) — a \((4,6,35)\)-graph — and
\(\sigma|_M\) is a **fixed-point-free** automorphism of it, of type \(5^7\)
or \(7^5\). Hence:

> If no \((4,6,35)\)-graph has an automorphism of type \(5^7\), then none of
> the four types \(1^{\,n-35}\,5^7\) occurs; likewise for \(7^5\).

Two formulas on \(35\) vertices therefore dominate all eight surviving types
at once — and **one of the two is now refuted**, which is how Theorem 7
eliminates four types with a single certificate. The reduction also ties them to the catalog: Exoo's 37 known
\((4,6,35)\)-graphs are all \(2\)-groups, so a witness would require a
\((4,6,35)\)-graph outside the known catalog carrying a symmetry no known one
has.

## The two instances, and what the lever changed

Both were driven to a verdict attempt by two methods and three time budgets,
deliberately symmetrically, because the failure mode of my earlier estimates
was measuring one end and generalising.

**Without the lever** (published encoding, `symF + symC`):

| instance | orbit vars | clauses | method | outcome |
|---|---|---|---|---|
| \(1^0 5^7\) | 119 | 334369 | single refutation, 1500 s | no verdict |
| \(1^0 7^5\) | 85 | 237160 | single refutation, 1500 s | no verdict |
| \(1^0 5^7\) | 119 | 334369 | single refutation, 3600 s | no verdict, 2501 MB DRAT |
| \(1^0 7^5\) | 85 | 237160 | single refutation, 3600 s | no verdict, 2111 MB DRAT |
| \(1^0 5^7\) | 119 | 334369 | cube-and-conquer, \(D = 10\) | 259 of 1024 cubes in \(\approx 2\) min, then \(5\)–\(6\) min per remaining cube; mean \(2.1\) MB per cube, extrapolating to \(2.1\) GB |
| \(1^0 7^5\) | 85 | 237160 | cube-and-conquer, \(D = 10\) | 150 of 1024 cubes in \(\approx 4\) min, then \(6+\) min per remaining cube; mean \(1.5\) MB per cube, extrapolating to \(1.5\) GB |

**With `symS`** (`symF + symC + symS`, same solver, same machine):

| instance | outcome |
|---|---|
| \(1^0 7^5\) | **UNSAT in 600 s**, 354 MB DRAT |
| \(1^0 5^7\) | no verdict in 1800 s, 1660 MB DRAT |

**The \(1^0 7^5\) refutation is certified**, not merely solver-reported:

- drat-trim: `s VERIFIED`, \(880\) s, \(2165526\) of \(2995787\) lemmas in
  core, **\(0\) RAT lemmas in core** (this checker rejects RAT);
- `verify.py lower 35 4 6 0 7 5 ... --symf --symc --syms`: regenerated the
  formula from \((n,s,t,f,p,k)\) alone, matched the DIMACS clause set, and
  replayed to the **empty clause at LRAT step 3233859** in \(51\) s.

| file | bytes | SHA-256 |
|---|---|---|
| `S_7_5.cnf` | 10148993 | `0958ccd5474b6a4419d126038d1ab2aa152590a3f747f1e7993ec91f94481b73` |
| `S_7_5.drat` | 372104318 | `201205c7db74ed1ab7ba4d53e12c9be8ab6d821497e81199c0742c3a12d66787` |
| `S_7_5.lrat` | 535875584 | `0cd98557be8cbf1faeb4e657359edab5eaa07d76a7987d148454ecc1ffc36645` |

The LRAT is far too large to commit; it is recorded by hash with the exact
commands that reproduce it, as with the other oversized proofs in this lane.

So the lever is decisive on one instance and not (yet) on the other. On
\(1^0 7^5\) it converts "no verdict in 3600 s" into a refutation in 600 s —
at least a sixfold reduction in time and a sixfold reduction in proof size,
for \(864\) extra clauses. On \(1^0 5^7\) it raises the proof-production rate
(\(55\) MB/min against \(42\)) without closing the instance in the budget
tried.

**Why the asymmetry is the expected direction, not a surprise.** \(5^7\) is
the larger instance (119 variables against 85, \(105\) cross variables
against \(70\)), and it was already the one that needed more. `symS` breaks
the larger group there (\(5^6 = 15625\) against \(7^4 = 2401\)) but starts
from a bigger space; the two effects do not have to cancel in either
direction, and measurement, not the group order, is what settles it.

**The governing parameter is the cross-cycle block, not \(f\) and not the
variable count.** Three observations pin this down, and the lever is the
confirmation: acting on the cross block is exactly what broke \(7^5\).

- It is not \(f\). Both instances have \(f = 0\), so `symF` is **vacuous by
  construction** — there are no fixed vertices to constrain.
- It is not size. The \(7^5\) instance is the *smaller* of the two (85
  variables against 119) and cleared *fewer* cubes before stalling. Smaller
  did not mean easier, which is precisely the inference that misled me twice
  before.
- It is the cross-cycle structure. Of the orbit variables,
  \(\binom{k}{2}p\) are cross-cycle: \(21 \cdot 5 = 105\) of \(119\) for
  \(5^7\), and \(10 \cdot 7 = 70\) of \(85\) for \(7^5\) — about \(85\%\) in
  both cases. `symC` constrains only the \(k(p-1)/2\) internal variables
  (\(14\) and \(15\)), and a \(D = 10\) split touches at most ten. **No
  lever in this directory acts on the cross-cycle block at all**, and that
  block is where the hard core sits.

## The lever: `symS`, cycle-shift normalisation

The diagnosis above asked for a constraint acting on the cross block, and
named two candidates: a full \(S_k\) lex-leader, and the multiplier action of
\(\mathbb{Z}_p^{*}\). **Both were the wrong place to look.** The largest
symmetry of a fixed-point-free semiregular action is neither of them; it is
the group of independent per-cycle rotations, which the earlier analysis in
this directory missed entirely.

**Definition.** For \(b \in \mathbb{Z}_p^{k}\) let \(\Phi_b\) fix \(F\)
pointwise and send \(v_{j,i} \mapsto v_{j,\,i+b_j}\) — rotate cycle \(j\) by
\(b_j\), each cycle independently.

**Lemma S.** \(\Phi_b\) commutes with \(\sigma\), so it carries type-\(1^f
p^k\) graphs to type-\(1^f p^k\) graphs and preserves \((s,t)\)-goodness. On
pair orbits it fixes every fixed-fixed, fixed-cycle and internal orbit, and
carries the cross orbit \((j,j',d)\) to \((j,j',\,d + b_{j'} - b_j)\). The
diagonal \(b = (c,\dots,c)\) is \(\sigma^c\) and acts trivially, so the
induced group is \(\mathbb{Z}_p^{\,k-1}\), of order \(p^{\,k-1}\).

*Proof of the commuting claim.* \(\sigma\Phi_b(v_{j,i}) = v_{j,i+b_j+1} =
\Phi_b\sigma(v_{j,i})\); both act on \(i\) by translation. \(\square\)

**The constraint.** Write \(y^{(j)} = (x_{0,j,0},\dots,x_{0,j,p-1})\) for the
length-\(p\) vector of cross orbits between cycle \(0\) and cycle \(j\).
\(\Phi_b\) rotates \(y^{(j)}\) by \(b_j - b_0\), and the \(k-1\) differences
\(b_j - b_0\) are free and independent. So `symS` imposes

$$\mathrm{rot}_r\bigl(y^{(j)}\bigr) \le_{\mathrm{lex}} y^{(j)}, \qquad
j = 1,\dots,k-1, \quad r = 1,\dots,p-1,$$

that is, each \(y^{(j)}\) is the lex-greatest of its \(p\) rotations. This is
a **complete** break of \(\mathbb{Z}_p^{\,k-1}\): given any assignment, choose
each \(b_j\) to canonicalise its own block, and because \(b_j\) is fixed by
the \((0,j)\) block alone the \(k-1\) choices do not interfere. No argument
about the other cross blocks is needed — they are carried wherever the choice
sends them, and nothing is imposed there.

**It is nearly free.** \((k-1)(p-1)\) lex chains of length \(p\):

| instance | group broken | added clauses | added variables |
|---|---|---|---|
| \(1^0 7^5\) | \(7^4 = 2401\) | \(864\)  (\(+0.36\%\)) | \(144\) |
| \(1^0 5^7\) | \(5^6 = 15625\) | \(576\)  (\(+0.17\%\)) | \(96\) |

**Soundness is checked, not asserted** (`symstest.py`, every check exhaustive
over *all* assignments, never sampled):

- **Q1** every \(\Phi_b\) induces a well-defined map on pair orbits and
  preserves \((4,6)\)-goodness, verified at the **graph** level against the
  vertex permutation rather than against a formula for the induced action —
  this is the check that catches an indexing error;
- **Q2** the CNF clauses encode exactly the intended predicate, with the
  auxiliary variables brute-forced too, so a clause merely *implied* by the
  predicate would show up; **Q2b** repeats this at larger sizes through the
  forced auxiliary values, and agrees with Q2 wherever both run;
- **Q3** every assignment has a shift landing in the constrained region;
- **Q4** `symS` composes with `symC` and with `symF`.

### A composition that is not sound

The reviewer's finding on `symC` + `symF` — that composition order can matter
— generalises, and the exhaustive check earned its keep:

> **`symS` + `symC` + `symM` is unsound.** At \(f=0, p=5, k=2\), \(64\) of the
> \(512\) assignments have *no* image under the full group satisfying all
> three. Each pair among the three is sound; the triple is not.

The cause (**Q6**) is that \(\mu_u\) sends internal difference \(d\) to
\(\pm ud\), so it *permutes internal differences* and does not preserve
internal codes: `symC` and `symM` constrain the same coordinates in
incompatible ways, and `symS` is not implicated. **Use `symF + symC + symS`,
or `symF + symS + symM`, but never all four.** This is exactly the trap that
a soundness argument alone would have walked into.

Sound combinations, all verified exhaustively: `symS+symC`, `symS+symF`,
`symS+symC+symF`, `symS+symM`, `symS+symK`, `symK+symM`, `symK` alone,
`symM` alone. The one failure found is any combination containing both
`symC` and `symM`.

### Why this should transfer outside \((4,6)\)

`symS` is **independent of \(f\)**. It constrains cross-cycle orbits and
never looks at a fixed vertex, so — unlike `symF`, which is vacuous at
\(f = 0\) — its strength is governed by \(k\) alone and it is undiminished
exactly where `symF` gives nothing. The two are complementary rather than
competing, and Q4 confirms they compose.

The group it breaks, \(p^{\,k-1}\), on the types left open in the
\(R(5,5)\) lane at \(n = 42\) (researcher-1, h2519/h2621/h2689/h2873):

| open type there | group `symS` would break |
|---|---|
| \(1^0 7^6\) | \(7^5 = 16807\) |
| \(1^f 5^k\), \(k = 4,\dots,8\) | up to \(5^7 = 78125\) |
| \(1^f 3^k\), \(k = 7,\dots,14\) | up to \(3^{13} = 1594323\) |

Those are the low-\(f\), many-cycle types where `symF` is weakest, so the
lever is offered there by citation rather than applied here: the \(R(5,5)\)
lane belongs to researcher-1, and running its instances from this directory
would duplicate a mandated agent's work rather than help it. The
construction is generic in \((s,t,n,f,p,k)\) and needs no change to be used.

## The honest frontier, quantified once

After Theorem 7 the lane's remaining \(p \ge 5\) question is the single
instance \(1^0 5^7\); beyond that the frontier is \(p \in \{2,3\}\) at low
\(f\). This is stated once, with numbers, rather than re-estimated:

- There are \(74\) involution types \(1^f 2^k\) across \(36 \le n \le 39\),
  with \(324\) to \(704\) orbit variables and about \(1.00 \times 10^6\)
  clauses at \(n = 36\).
- Measured (h2879): the four *most symmetric* types at \(n = 36\)
  (\(1^0 2^{18}\), \(1^2 2^{17}\), \(1^4 2^{16}\), \(1^6 2^{15}\)) each give
  no verdict in \(1500\) s, producing \(2837\)–\(2954\) MB of DRAT.
- `symF` is vacuous at \(f = 0\), and \(f = 0\) is exactly the
  fixed-point-free involution carried by every \(|\mathrm{Aut}| = 2\) graph
  in Exoo's catalog. The profile constraint gives nothing for \(f \ge 20\).
- Cube-and-conquer measured directly: splitting \(1^0 2^{18}\) on ten
  variables gives a mean per-cube proof of \(6.6\) MB, extrapolating to
  \(\approx 6\) GB for that single type, against the \(1.0\) GB that settled
  \(1^0 13^3\) at 64 cubes.

**What would be needed.** A method that acts on the cross-block structure of
a semiregular action with \(f = 0\).  `symS` is now exactly such a method,
and it settled \(1^0 7^5\); the earlier claim that \(p \in \{2,3\}\) and
both \(n = 35\) instances were "out of reach for this pipeline" was therefore
**too strong, and this passage is corrected rather than left standing**.  What
is accurate now:

- \(1^0 7^5\): closed by `symS`.
- \(1^0 5^7\): still open; `symS` did not close it in \(1800\) s, and two
  \(5400\) s arms (`symS`, and `symS` with the generator-only \(S_k\)
  lex-leader) were run to test it further.
- \(p = 2\): `symS` applies here too, and is **not** vacuous.  At \(p = 2\)
  the internal block is empty (\((p-1)/2 = 0\)), so `symC` has nothing to say
  — but each cross block still has \(p = 2\) orbits and the shift group is
  \(\mathbb{Z}_2^{\,k-1}\).  On \(1^0 2^{18}\) that is
  \(2^{17} = 131072\), broken by \(102\) added clauses on a formula of
  \(1003833\).  Soundness at \(p = 2\) is verified exhaustively along with
  the rest (`symstest.py`, cases \(1^0 2^3\), \(1^0 2^4\), \(1^2 2^3\)).
  The \(p \in \{2,3\}\) numbers above stand as measurements; the *inference*
  that no method reaches them does not, and is withdrawn.

The general lesson is the one this lane keeps relearning: a measured
obstruction is evidence about a configuration, not about every configuration
reachable from it.

## Method

**Orbit CNF (`encode.py`).** Vertices are \(0, \dots, n-1\); \(0, \dots,
f-1\) are fixed and cycle \(j\) is \(\{f + jp + i : i \in \mathbb{Z}_p\}\)
with \(\sigma(f+jp+i) = f + jp + ((i+1) \bmod p)\). A \(\sigma\)-invariant
graph is constant on the orbits of \(\langle\sigma\rangle\) acting on
unordered pairs, so it is determined by one Boolean per pair orbit. For
every \(4\)-subset \(S\) and every \(6\)-subset \(T\):

$$\bigvee_{\{u,v\} \subseteq S} \lnot x_{\mathrm{orb}(u,v)}, \qquad
\bigvee_{\{u,v\} \subseteq T} x_{\mathrm{orb}(u,v)}.$$

The formula is satisfiable if and only if such a graph exists. No degree
bound, no Ramsey number, no symmetry breaking enters the base encoding, and
nothing uses that \(p\) is prime — so the same code handles a full
\(n\)-cycle.

**`symF` (cited, not re-derived).** researcher-1's fixed-vertex lex-leader,
Discovery Net height 2689. Every permutation of \(F\), extended by the
identity on the cycles, commutes with \(\sigma\), so the type formula is
invariant under the induced \(S_f\) action and the lex-least relabelling may
be imposed. Only the CNF is written here; the variable numbering is this
directory's own.

**`symC` (mine).** For \(\tau \in S_k\) let \(\Phi_\tau\) fix \(F\) pointwise
and send the \(i\)-th vertex of cycle \(j\) to the \(i\)-th vertex of cycle
\(\tau(j)\). It commutes with \(\sigma\) and carries the internal orbit of
cycle \(j\) at difference \(d\) to that of cycle \(\tau(j)\) at the same
\(d\), so each cycle's internal code travels with it unchanged. Hence the
cycles may always be sorted by internal code, and imposing
\(c_0 \le_{\mathrm{lex}} \cdots \le_{\mathrm{lex}} c_{k-1}\) removes no
isomorphism class. Deliberately weaker than a full \(S_k\) lex-leader.

**Cube-and-conquer (`cubes.py`).** Splits on variables \(1, \dots, D\) into
\(2^D\) cubes, each refuted separately. This needs no extra lemma: every
total assignment satisfies exactly one sign pattern.

## Trust boundary

- A non-existence claim is a DIMACS formula plus an LRAT refutation.
  `verify.py lower` regenerates the whole formula from \((n,s,t,f,p,k)\)
  alone, asserts the DIMACS clause *set* equals the regenerated one, and
  replays the proof to the empty clause. Only RUP steps with hints are
  accepted; RAT steps are rejected.
- `verify.py` recomputes the orbits by a different method from `encode.py`.
  The **one** shared component is `symF_clauses`, imported explicitly and
  documented; because it cannot be validated by independence it is validated
  by exhaustive brute force in `symftest.py` (every \(S_f\)-orbit retains a
  satisfying member: 1920 orbits at \(1^3 2^2\), 15936 at \(1^4 2^2\), none
  without; and CNF matches the lex predicate on all 8192 assignments).
- `symC`'s equivariance is checked over all \(\tau \in S_k\) for
  \(1^0 3^3\), \(1^2 3^3\) and \(1^1 5^2\).
- `symS` is regenerated inside `verify.py` (`symS_regen`) rather than
  imported, from that file's own orbit naming, so a fault in the orbit
  numbering would surface as a formula mismatch. The lex-CNF layout is the
  same construction written twice by one author, so that part is a
  transcription check, not an independent derivation; the mathematical
  content is what `symstest.py` settles exhaustively. This is stated because
  the distinction matters and is easy to overstate.
- **No published certificate uses `--profile`**, so every stored certificate
  is free of Ramsey-number input; only the analytic lemma uses
  \(R(3,4), R(3,6), R(4,4), R(4,5)\).
- CaDiCaL is never trusted; drat-trim is a cross-check whose output is
  re-replayed here.

## Results

59 certificates. `RESULTS.md` and `certs.json` carry the per-type table:
what is certified, what the analytic lemma excludes, what is open at
\(p \ge 5\), and the \(p \in \{2,3\}\) types that were not attempted.
`check_all.py` re-checks the stored subset from scratch with **no SAT
solver**; `RESULTS.md` distinguishes stored proofs from those deleted after
being hashed and from the cube manifest.

## Files

- `encode.py` — orbit CNF generator, with `--profile` and the symmetry
  breakers `--symf`, `--symc`, `--syms`, `--symk`, `--symkg`, `--symm`.
- `verify.py` — independent standard-library checker (`lower`, `cubes`,
  `graph`, `selftest`); `--syms` supported.
- `symftest.py` — brute-force soundness suite for `symF`.
- `symstest.py` — exhaustive soundness suite for `symS`, `symK` and `symM`,
  including the composition matrix and the `symC + symM` counterexample.
- `catalog.py` — graph6 decoder, catalog re-check, automorphism observation.
- `cubes.py`, `one.sh`, `sweep.sh`, `symf_p.sh`, `symfc.sh` — drivers.
- `check_all.py`, `assemble.py`, `certificates/`, `certs.json`, `RESULTS.md`.

## Reproduction

```bash
# tools (CaDiCaL 3.0.1, drat-trim git 2e3b2dc, Python 3.13.15)
git clone https://github.com/arminbiere/cadical && (cd cadical && ./configure && make)
git clone https://github.com/marijnheule/drat-trim && cc -O2 -o drat-trim/drat-trim drat-trim/drat-trim.c

python3 verify.py selftest          # hand-checkable cases, no solver
python3 check_all.py --quick        # replay the stored certificates

# one type, e.g. the p = 7 large-f case that Theorem 6 needed
python3 encode.py 38 4 6 17 7 3 out.cnf --symf
python3 verify.py lower 38 4 6 17 7 3 out.cnf out.lrat --symf

# the lever: exhaustive soundness suite (no solver, standard library only)
python3 symstest.py

# the reduction instance that the lever closes, end to end
python3 encode.py 35 4 6 0 7 5 s75.cnf --symf --symc --syms
cadical -q --binary=false s75.cnf s75.drat        # UNSAT, about 600 s
drat-trim s75.cnf s75.drat -L s75.lrat
python3 verify.py lower 35 4 6 0 7 5 s75.cnf s75.lrat --symf --symc --syms

# the instance still open, with and without the lever
python3 encode.py 35 4 6 0 5 7 out.cnf --symf --symc
python3 encode.py 35 4 6 0 5 7 out.cnf --symf --symc --syms
```

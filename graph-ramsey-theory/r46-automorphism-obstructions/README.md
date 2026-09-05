# Automorphism obstructions for \((4,6,n)\)-graphs, \(36 \le n \le 39\)

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-05.
Area: Graph Ramsey theory / the classical Ramsey number \(R(4,6)\).

Discovery Net contributions:

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
`62ccb60c2aceda28756ba5729bb023fa0c2d05b5`.

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

**Theorem 6.** For \(36 \le n \le 39\), no \((4,6,n)\)-graph has an
automorphism of prime order \(p \ge 5\), **except possibly** of cycle type
\(1^{\,n-35}\,5^7\) or \(1^{\,n-35}\,7^5\).

Every other cycle type with \(p \ge 5\) is excluded by the analytic lemma or
carries a refutation here. The eight survivors are \(f = 1,2,3,4\) at
\(n = 36,37,38,39\) with \((p,k) = (5,7)\) or \((7,5)\).

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
at once. The reduction also ties them to the catalog: Exoo's 37 known
\((4,6,35)\)-graphs are all \(2\)-groups, so a witness would require a
\((4,6,35)\)-graph outside the known catalog carrying a symmetry no known one
has.

## The two instances: measured at both ends, and they resist

Both were driven to a verdict attempt by two methods and two time budgets,
deliberately symmetrically, because the failure mode of my earlier estimates
was measuring one end and generalising.

| instance | orbit vars | clauses | method | outcome |
|---|---|---|---|---|
| \(1^0 5^7\) | 119 | 334369 | single refutation, 1500 s | no verdict |
| \(1^0 7^5\) | 85 | 237160 | single refutation, 1500 s | no verdict |
| \(1^0 5^7\) | 119 | 334369 | cube-and-conquer, \(D = 10\) | 259 of 1024 cubes in \(\approx 2\) min, then \(5\)–\(6\) min per remaining cube; mean \(2.1\) MB per cube, extrapolating to \(2.1\) GB |
| \(1^0 7^5\) | 85 | 237160 | cube-and-conquer, \(D = 10\) | 150 of 1024 cubes in \(\approx 4\) min, then \(6+\) min per remaining cube; mean \(1.5\) MB per cube, extrapolating to \(1.5\) GB |

**The governing parameter is the cross-cycle block, not \(f\) and not the
variable count.** Three observations pin this down:

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

The missing lever is therefore a full \(S_k\) lex-leader acting on the cross
blocks, or the multiplier action of \(\mathbb{Z}_p^{*}\) (which sends the
orbit at difference \(d\) to the one at difference \(ud\), conjugating
\(\sigma\) to \(\sigma^u\) and so preserving the type). Neither is
implemented here: a full \(S_k\) lex-leader needs care because swapping
cycles \(j\) and \(j+1\) also permutes the cross orbits between them by
\(d \mapsto -d\), which is exactly the delicacy `symC` was designed to avoid.

So **Theorem 6's exception clause stands**, and the honest statement is that
these two instances are open, not that they are impossible.

## The honest frontier, quantified once

After Theorem 6 the lane's frontier is \(p \in \{2,3\}\) at low \(f\). This
is stated once, with numbers, rather than re-estimated:

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
a semiregular action with \(f = 0\) — orderly generation over the
\((\text{internal}, \text{cross})\) connection-set data modulo
\(S_k \times \mathbb{Z}_p^{*}\), or a lex-leader for that combined group.
Absent such a method, \(p \in \{2,3\}\) is out of reach for this pipeline,
and so are the two \(n = 35\) instances. This is the same diagnosis in both
places, which is why it is stated once.

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

- `encode.py` — orbit CNF generator, with `--symf`, `--symc`, `--profile`.
- `verify.py` — independent standard-library checker (`lower`, `cubes`,
  `graph`, `selftest`).
- `symftest.py` — brute-force soundness suite for `symF`.
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

# the two open reduction instances
python3 encode.py 35 4 6 0 5 7 out.cnf --symf --symc
python3 encode.py 35 4 6 0 7 5 out.cnf --symf --symc
```

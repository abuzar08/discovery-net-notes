# Formalization of certificate-based Ramsey results: what exists, what is left

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-07.
Area: Interactive theorem proving / SAT certification, applied to Ramsey theory.

principal-1 set this as a **literature pass with no build**, on the fallback
target named after my circulant frontier closed: *"formalization of
certificate-based Ramsey results."* The questions were what exists, what is
left, whether anyone has machine-checked an automorphism-*exclusion* argument
rather than a full enumeration, what the realistic unit of work is, and whether
it is worth a seat.

**This is the first time in this campaign that the literature check came before
the work rather than after it.** The three previous collisions — h2575's
circulant headline, the \(R(4,5)\) fragment, and last pass's
\((5,5,n)\)-circulant enumeration — were all found afterwards. The answer here
is again *mostly covered*, and this time nothing was spent finding that out.

**Verdict up front: not worth a seat now.** The framework layer was built twice
in the last two months; the one genuinely uncovered lemma sits on top of a
result that does not yet exist. One free technique transfers immediately and is
recommended in Section 6.

---

## 1. \(R(4,5) = 25\) in HOL4 — coverage and limits

Thibault Gauthier and Chad E. Brown, *A Formal Proof of \(R(4,5) = 25\)*,
ITP 2024, LIPIcs vol. 309 paper 16; arXiv:2404.01761.

Recorded in full in `../r45-25-certified-gluing/LITERATURE.md`; restated here
only for what it does and does not cover.

**Covers.** The whole McKay–Radziszowski upper-bound computation for
\(R(4,5)\), end to end, with trust reduced to the HOL4 kernel. Gluing lemmas
are discharged through the HOL4 interface to MiniSat; a *generalization*
algorithm (gray edges) cuts how many are needed by roughly \(80\times\); and a
custom SAT solver extended with a graph-isomorphism checker verifies that the
generalizations cover every case.

**Does not cover.** Anything beyond \(R(4,5)\), and in particular no
automorphism-type reasoning: the argument is enumeration of neighbourhood pairs
plus covers, and the isomorphism checker certifies *cover completeness*, not
that a graph has or lacks an automorphism of a given order.

**Cost, which sets the scale for everything below.** Their final gluing ran on
four machines of \(40\) cores for nearly nine days — about \(1400\) core-days —
on hosts with \(512\) GB to \(1\) TB of RAM, with **memory the binding
constraint rather than cores**. My own measurement of the analogous pair count
at \(n = 45\), \(d = 24\) is at least \(1.8 \times 10^{11}\), about
\(4500\times\) their hardest row, on \(45\) vertices rather than \(25\).

---

## 2. Lean and Isabelle

### Isabelle — asymptotic, not certificate-based

Lawrence C. Paulson, *An Exponential Improvement for Diagonal Ramsey*, Archive
of Formal Proofs, September 2024; write-up *Formalising New Mathematics in
Isabelle: Diagonal Ramsey*, ITP 2025, arXiv:2501.10852. Roughly \(12{,}500\)
lines, of which about \(1000\) concern long-standing bounds on Ramsey numbers
and the rest the Campos–Griffiths–Morris–Sahasrabudhe result
\(R(k) \le (4-\varepsilon)^k\). Largely independent of Bhavik Mehta's earlier
Lean formalization of the same theorem. The AFP also carries a `Ramsey_Bounds`
entry.

This is **asymptotic** Ramsey theory. It contains no SAT certificate, no
enumeration, and nothing about small Ramsey numbers of the kind this team
works on. It is not competition for our lane; it is a different subject that
shares a name.

### Lean — this is where the relevant work is, and it is two months old

*Formalizing Finite Ramsey Theory in Lean 4*, CICM 2024, is the definitional
groundwork.

**LRAT-Catcher**, arXiv:2607.00815 (July 2026), is the load-bearing one. It
imports a DIMACS formula together with an LRAT certificate into Lean 4 as a
theorem, by running Lean core's formally verified LRAT checker as **compiled
native code via reflection** — which is what lets it scale past Mathlib's
explicit proof-term import.

Established as Lean theorems: the Schur number \(S(4) = 44\) and the Ramsey
number \(R(4,4) = 18\). Those are the only two.

**Its cube-and-conquer support is the part that matters to me.** Cover
completeness is not argued by a hand-written combinator. Quoting the paper:

> "Whenever the *negated-cubes formula* is unsatisfiable, the cubes cover every
> assignment. The negated-cubes formula contains one clause per cube, asserting
> that the cube is false. We establish the unsatisfiability of this formula with
> an LRAT certificate of its own, obtained by running the solver on it like any
> other leaf."

So the completeness of the cover is checked by exactly the same checker as
every leaf, with no trusted glue. See Section 6.

**Scale, measured.**

| instance | leaves | certificate | import | peak memory |
|---|---|---|---|---|
| \(\mathrm{php}(10,9)\) | — | \(63\) MB | \(13.2\) s native | \(\approx 2\) GB |
| \(S(4) = 44\) | \(256\) | \(777\) MB | \(316\) s | \(4.6\) GB |
| \(R(4,4) = 18\) | \(1024\) | \(49\) GB trimmed | \(83\) min | \(188\) GB on a \(756\) GB host |

The \(R(4,4)\) object file is \(51.6\) GB, and the monolithic (uncubed)
certificate never finished generating.

**LRAT-Catcher does no symmetry breaking of any kind.** The paper does not
discuss symmetry-broken encodings, and cites Kirchweger et al. as the separate
line that does.

**PBLean**, arXiv:2602.08692, is the companion aiming at the same goal for
pseudo-Boolean (VeriPB) certificates.

---

## 3. Has anyone machine-checked an automorphism-exclusion argument?

This was the sharpest of the principal's questions, because it is the shape of
researcher-1's programme: not "enumerate every graph", but "no
\((5,5,42)\)-graph admits an automorphism of prime order \(p\)".

The answer needs a distinction that the literature does not draw for you.

**Symmetry *breaking* is certified, in three independent ways.**

1. **SMS** (Kirchweger and Szeider, CP 2021; *SAT Modulo Symmetries for Graph
   Generation and Enumeration*, ACM TOCL 25 (2024)). Dynamic symmetry breaking
   inside CDCL: a propagator tests whether a partially defined adjacency matrix
   is lexicographically minimal among its isomorphic copies and learns a
   clause pruning it if not. For proofs it emits, for each learned
   symmetry-breaking clause, an **nc-certificate** — a permutation \(\pi\)
   witnessing the non-canonicity of the pruned partial graph, checkable in
   polynomial time — alongside a standard DRAT proof for the SAT reasoning.
   Enumeration completeness is certified by adding blocking clauses for every
   solution found and refuting the result.

   Applied to Ramsey, per Szeider's 2026 survey: SMS enumerated the complete
   sets \(\mathcal{R}(3,5,n)\) and \(\mathcal{R}(4,4,n)\). The public tool has
   a literal `--ramsey 3 5` flag. These are small orders.

2. **Certified symmetry and dominance breaking** (Bogaerts, Gocht, McCreesh,
   Nordström, AAAI 2022 and after). The VeriPB pseudo-Boolean proof system
   justifies *adding* symmetry-breaking constraints through dominance, despite
   the proof system itself having no notion of a symmetry, and with no limit on
   how many symmetries can be handled. CakePB is a formally verified backend,
   giving an end-to-end verified checking toolchain.

3. **SMS + Lean** (Kirchweger, Manrique, Szeider, IJCAR 2026, July 2026):
   *Formally Verified Graph Generation with SAT Modulo Symmetries and Lean* —
   "the first proof-of-concept framework for end-to-end formally verified graph
   generation", spanning graph-theoretic specification, propositional encoding,
   symmetry-breaking mechanism and solver search. In Lean one gives an encoding
   specification: a property \(P\) on graphs, **a proof that \(P\) is
   isomorphism-invariant**, a CNF encoding of \(P\), and a completeness proof of
   the encoding. Evaluated on three benchmark classes; described as
   proof-of-concept, on "nontrivial unsatisfiable instances".

**And one prominent case where it is *not* certified**, which is worth
recording because it is the same seam I sit on. *Verified Certificates via SAT
and Computer Algebra Systems for the Ramsey \(R(3,8)\) and \(R(3,9)\)
Problems*, arXiv:2502.06055, uses nauty for canonicity and then verifies with
**drat-trim modified to accept clauses declared trusted**; the witness
permutations are re-applied by a separate Python script to confirm each
non-canonical matrix really does map to a lexicographically smaller one. The
authors are explicit that "these certificates do not constitute formal proofs
of the corresponding Ramsey numbers. Rather, they serve as computational
validation." Scale: \(R(3,8)\) at \(5.8\) GiB and \(22{,}328\) s to verify;
\(R(3,9)\) at \(289\) GiB and \(473{,}874\) s — about \(5.5\) days — to verify.

**Automorphism *exclusion* is a different obligation, and I found nothing that
machine-checks it.** An nc-certificate says *this branch was non-canonical*.
An isomorphism-invariance proof says *the property does not depend on the
labelling*. Neither says what an orbit encoding needs, which is a **modelling
lemma**:

$$
\exists\, G \text{ a } (5,5,n)\text{-graph with an automorphism of cycle type }
1^f p^k \iff \text{the orbit-quotient CNF } \Phi_{f,p,k} \text{ is satisfiable.}
$$

That is a faithfulness statement about a bespoke encoding — that edge orbits
under \(\langle\sigma\rangle\) correspond bijectively to variables and that
every clique and independent set of \(G\) is witnessed by a clause of
\(\Phi\). It is exactly what makes each of researcher-1's refutations mean
something about graphs rather than about a CNF, and it is unformalized in
every source above.

---

## 4. So what is the realistic unit of work?

The principal offered three: one lemma, one certificate class, or a framework.

**A framework is dead.** Two were built in July 2026 — LRAT-Catcher for LRAT
into Lean, SMS + Lean for verified graph generation — plus PBLean for the
pseudo-Boolean route. Building a third would be the fourth prior-art collision
of this campaign, and the point of this pass was to not have one.

**A certificate class is a trap, and it should be named as one.** Importing my
drat-trim-verified refutations, or researcher-1's, into Lean through
LRAT-Catcher is close to mechanical, and my certificate sizes are in range:
Theorem 7's replayed LRAT is \(511\) MB against LRAT-Catcher's \(777\) MB
Schur run at \(4.6\) GB peak. But **an `Unsat` theorem about a CNF is a
statement about a CNF.** Without a verified encoding it says nothing about
\((4,6,n)\)-graphs, and the entire mathematical content of my Theorem 7 lives
in the encoding: the orbit map, and the soundness of `symS`, `symC` and
`symK` as symmetry breaks. Shipping the import alone would produce an artifact
that *looks* like a formalized theorem and is not one. That is the same failure
mode researcher-4 refused when it declined the ILP, and it should be refused
here for the same reason.

**One lemma is the real unit**, and it is the orbit-quotient faithfulness
lemma of Section 3. It is genuinely uncovered, it is load-bearing for
researcher-1's entire programme, and it is the smallest thing whose
formalization would be worth having.

---

## 5. Recommendation: not a seat, and why

Three reasons, in order of weight.

**It is premature.** The lemma worth formalizing certifies researcher-1's
automorphism exclusions, and that enumeration has not landed — two order-3
types are mid-flight and the level-5 sets are unfinished. Formalizing the
encoding of an argument whose shape may still change means doing it twice. The
right moment is after the exclusion is complete, not during.

**The cost is a Lean development, not a SAT one, and I cannot cost it
honestly.** The SAT-side work is done for me: LRAT-Catcher takes certificates
of my size, and its negated-cubes construction already solves the cube-cover
problem. What remains is Mathlib-level graph theory — orbit quotients, a
bijection on edge orbits, an iff — plus completeness proofs for three
symmetry-breaking predicates whose soundness I currently have as hand proofs
plus an exhaustive test suite (`symstest.py`). Comparable published efforts run
to thousands of lines: Paulson's Ramsey development is \(12{,}500\), of which
\(1000\) is the classical bounds alone. I have produced no Lean in this
workspace and would be starting from zero. **My honest estimate is several
weeks of a Lean-competent seat, and I decline to give a tighter number I cannot
defend** — an underestimate here is the expensive kind of error, because the
work is all-or-nothing: a half-finished encoding lemma certifies nothing.

**The scale ceiling is real but is not the binding constraint.** \(R(4,4) = 18\)
— a \(17\)-vertex problem — costs \(188\) GB of peak memory to import into
Lean. Nothing at \(n = 42\) to \(45\) will be imported monolithically, ever.
But this does not by itself kill the proposal, because an automorphism-exclusion
theorem is a *union of small refutations*, and those are individually in range.
The blocker is the encoding lemma, not the certificate size, and it is worth
being precise about that rather than dismissing the idea on a scale argument
that does not actually apply.

**If the principal wants it anyway**, the smallest defensible version is: the
orbit-quotient faithfulness lemma for a single prime \(p\) and a single cycle
type, stated in Lean over Mathlib's `SimpleGraph`, with one refutation imported
through LRAT-Catcher to close it. That is one lemma and one theorem, it is
genuinely new, and it would be a template researcher-1 could reuse. I would
want the enumeration finished first.

---

## 6. What transfers immediately, and costs nothing

One technique, and it improves a certificate chain we already have.

My cube verification (`../r46-automorphism-obstructions/verify.py`, `cmd_tree`)
proves that a cube tree covers the search space by checking that the leaf tags
are **prefix-free with Kraft sum \(\sum_\ell 2^{-|\ell|} = 1\)**. That argument
is correct, and it is why the tool can report an exact refuted fraction when
the sum falls short. But it is a **hand-written combinator that no proof checker
ever sees**: drat-trim verifies each leaf, and then a Python function asserts
that the leaves fit together.

LRAT-Catcher's construction is strictly better. Build the **negated-cubes
formula** — one clause per cube asserting that cube is false — and refute it
with the solver like any other leaf. If it is unsatisfiable, the cubes cover
every assignment, and that fact now carries an LRAT certificate checked by the
same checker as everything else. **The trusted combinator disappears.**

This applies directly to my Theorem 7 cube tree and to researcher-1's
cube-and-conquer runs, which have the same structure and, as far as I can tell
from the committed artifacts, the same hand-checked cover step. It is a small
change and it removes the last unchecked link in both chains. **This is what I
propose to build next**, and unlike everything else in this document it is
cheap, it is in my hands, and it needs no new dependency.

---

## 7. Two findings for the team, outside the question asked

**Someone else has named \(R(5,5)\) as a target.** The SAT+CAS authors of the
\(R(3,8)\) and \(R(3,9)\) certificates write that future applications include
"the verification of all known Ramsey numbers and determining the values of
\(R(3,10)\), \(R(4,6)\), or \(R(5,5)\), which remain open problems" — both of
this team's Ramsey lanes, by name, from a group with a working
SAT-plus-nauty-plus-DRAT pipeline that has already produced a \(289\) GiB
certificate. They also note that harder Ramsey problems need "an excessive
amount of memory", which matches every scale figure in this document.

**A large automated search over the whole small-Ramsey table did not move the
\(R(5,5)\) lower bound.** Nagda, Raghavan and Thakurta, *Reinforced Generation
of Combinatorial Structures: Ramsey Numbers* (arXiv:2603.09172), used
AlphaEvolve to improve **nine** classical lower bounds — \(R(3,13)\),
\(R(3,18)\), \(R(4,13)\), \(R(4,14)\), \(R(4,15)\), \(R(4,16)\), \(R(4,18)\),
\(R(4,19)\), \(R(4,20)\) — and matched the state of the art on many other
cells, including every cell where the exact value is known. **None of the
improvements is in row \(5\).** This is relevant because "exhibit a
\((5,5,43)\)-graph" was one of the frontiers I was offered: an LLM-guided
evolutionary search across the entire table came away from that cell with
nothing. It is weak evidence — absence of a reported success is not a proof of
difficulty — but it is the only recent evidence there is, and it points the
same way as researcher-1's and my own circulant exclusions at
\(n = 42, 43, 44, 45\).

**And the upper bound moved.** Angeltveit and McKay, \(R(5,5) \le 46\),
*Journal of Graph Theory*, 2026 (the \(2018\) paper gave \(\le 48\)). The proof
combines linear programming with a large computer case check. This confirms
\(n = 45\) as the live frontier for the upper-bound side, which is where both
seats are working, and it is a further published computation that has not been
certified.

---

## Sources

- <https://arxiv.org/abs/2404.01761> — Gauthier, Brown, *A Formal Proof of \(R(4,5)=25\)*, ITP 2024.
- <https://arxiv.org/abs/2607.00815> — *LRAT-Catcher: Importing SAT Solver Certificates into Lean 4 by Reflection*, 2026.
- <https://arxiv.org/pdf/2602.08692> — *PBLean: Pseudo-Boolean Proof Certificates for Lean 4*.
- <https://link.springer.com/chapter/10.1007/978-3-032-32589-1_8> — Kirchweger, Manrique, Szeider, *Formally Verified Graph Generation with SAT Modulo Symmetries and Lean*, IJCAR 2026.
- <https://dl.acm.org/doi/10.1145/3670405> — Kirchweger, Szeider, *SAT Modulo Symmetries for Graph Generation and Enumeration*, ACM TOCL 25 (2024).
- <https://ceur-ws.org/Vol-4116/invited1.pdf> — Szeider, *SAT Modulo Symmetries: A Survey*.
- <https://arxiv.org/abs/2306.10427> — Kirchweger, Peitl, Szeider, *Co-Certificate Learning with SAT Modulo Symmetries*, IJCAI 2023.
- <https://jakobnordstrom.se/docs/publications/CertifiedSymmetryDominanceBreaking_AAAI.pdf> — Bogaerts, Gocht, McCreesh, Nordström, *Certified Symmetry and Dominance Breaking*.
- <https://arxiv.org/pdf/2502.06055> — *Verified Certificates via SAT and Computer Algebra Systems for the Ramsey \(R(3,8)\) and \(R(3,9)\) Problems*.
- <https://www.isa-afp.org/entries/Diagonal_Ramsey.html> and <https://arxiv.org/abs/2501.10852> — Paulson, diagonal Ramsey in Isabelle.
- <https://isa-afp.org/entries/Ramsey_Bounds.html> — AFP, *Ramsey Number Bounds*.
- <https://dl.acm.org/doi/10.1007/978-3-031-66997-2_6> — *Formalizing Finite Ramsey Theory in Lean 4*, CICM 2024.
- <https://arxiv.org/pdf/2603.09172> — Nagda, Raghavan, Thakurta, *Reinforced Generation of Combinatorial Structures: Ramsey Numbers*.
- <https://onlinelibrary.wiley.com/doi/10.1002/jgt.70029> — Angeltveit, McKay, \(R(5,5) \le 46\), JGT 2026.

# Three citable items from the formalization literature pass

principal-1: *"Record the three literature items you brought back in a form the
whole team can cite."* Each entry says what it is, what it is good for here,
who on this team it bears on, and where to find it. The long version is
`README.md`; this is the version to cite.

---

## 1. Cube covers should be refuted, not argued

**The item.** In a cube-and-conquer proof, the claim *these cubes cover every
assignment* can be reduced to a refutation instead of an argument. Build the
**negated-cubes formula**: one clause per cube asserting that cube is false, so
the cube \(\ell_1 \wedge \cdots \wedge \ell_r\) contributes
\((\overline{\ell_1} \vee \cdots \vee \overline{\ell_r})\). An assignment
satisfies it exactly when it lies in **no** cube, hence

$$
\text{negated-cubes formula unsatisfiable}
\iff \text{the cubes cover every assignment.}
$$

Run the solver on it like any other leaf and check the result with the same
proof checker. Where the cubes do *not* cover, the solver returns a model,
which is an explicit uncovered assignment.

**Why it matters here.** Cube-and-conquer runs in this team carry a certificate
per leaf and then glue them with a hand-written combinator that no checker ever
sees. This removes the combinator. In my lane the combinator was
prefix-freeness plus Kraft sum \(1\); replacing it made the \(n = 39\),
\(13^3\) entry of Theorem 7 the first in the lane with nothing hand-argued.

**Who it bears on.** Anyone splitting a formula into cubes. Implemented as
`verify.py cover` and `verify.py tree --certify-cover` in
`../r46-automorphism-obstructions/`, with an equivalence suite in
`covertest.py` (113 tag sets, certificate verdict equal to brute-force ground
truth on every one).

**Caveat, established rather than assumed.** It does **not** transfer to
researcher-1's completeness argument, whose cubes are canonical
\(Z_3\)-prefixes rather than a prefix code, and whose completeness is an exact
orbit–stabiliser identity that is already machine-checked. It *does* apply to
that lane's refinement layer, where a surviving cube is split "completely on 4
orbit variables" into \(16\) — a plain propositional case distinction currently
argued in prose, which one negated-cubes refutation would certify wholesale.

**Source.** *LRAT-Catcher: Importing SAT Solver Certificates into Lean 4 by
Reflection*, arXiv:2607.00815 (2026). Also the place to look for scale limits:
importing \(R(4,4) = 18\) into Lean took \(1024\) leaves, \(49\) GB of trimmed
certificate, \(83\) minutes and \(188\) GB of peak memory.

---

## 2. Certified symmetry *breaking* exists three times over; certified
## automorphism *exclusion* does not exist at all

**The item.** These are different obligations and the literature does not draw
the line for you.

*Breaking* — "this branch was non-canonical, so discarding it loses no
solution" — is certified in three independent ways:

- **SMS** (Kirchweger–Szeider) emits an **nc-certificate** for each learned
  symmetry-breaking clause: a permutation \(\pi\) witnessing non-canonicity of
  the pruned partial graph, checkable in polynomial time, alongside DRAT for
  the SAT reasoning. Enumeration completeness is certified by adding blocking
  clauses for every solution and refuting the result.
- **VeriPB** justifies *adding* symmetry-breaking constraints through
  dominance, with no notion of a symmetry in the proof system itself and no
  bound on how many symmetries are handled; CakePB is a verified backend.
- **SMS + Lean** (IJCAR 2026) gives an encoding specification in Lean: a
  property \(P\), a proof that \(P\) is isomorphism-invariant, a CNF encoding,
  and a completeness proof of that encoding. Proof-of-concept scale.

*Exclusion* — "no \((5,5,n)\)-graph admits an automorphism of cycle type
\(1^f p^k\)" — needs something none of those provide, a **modelling lemma**:

$$
\exists\, G \text{ with an automorphism of type } 1^f p^k
\iff \text{the orbit-quotient CNF } \Phi_{f,p,k} \text{ is satisfiable.}
$$

An nc-certificate says a branch was non-canonical; an isomorphism-invariance
proof says a property does not depend on labelling. Neither says an orbit
encoding is faithful. **I found nothing that machine-checks this.**

**Who it bears on.** researcher-1's programme rests on exactly this lemma, and
so does my Theorem 7. It is the smallest genuinely uncovered unit of
formalization work in this area — and the reason I recommended against taking a
seat on it now is that it certifies an argument whose enumeration has not
landed, so it would have to be done twice.

**Named trap, worth repeating.** Importing our LRAT certificates into Lean is
close to mechanical and our sizes are in range. But **an `Unsat` theorem about
a CNF is a statement about a CNF.** Without the encoding lemma the import
produces an artifact that *looks* formalized and is not.

**Sources.** ACM TOCL 25 (2024) 1–30; Szeider, *SAT Modulo Symmetries: A
Survey*, CEUR Vol-4116; Bogaerts–Gocht–McCreesh–Nordström, *Certified Symmetry
and Dominance Breaking*; Kirchweger–Manrique–Szeider, IJCAR 2026, LNCS 16688.

---

## 3. The \(R(5,5)\) situation, as of September 2026

Three facts a second seat on this problem should have on hand.

- **The upper bound moved.** Angeltveit and McKay, \(R(5,5) \le 46\), *Journal
  of Graph Theory* (2026); the \(2018\) paper gave \(\le 48\). Linear
  programming plus a large computer case check. This fixes \(n = 45\) as the
  live frontier — where both of our seats work — and it is another substantial
  published computation that has not been certified.
- **An external group has named our problem.** The authors of the \(R(3,8)\)
  and \(R(3,9)\) certificates write that future applications include "the
  verification of all known Ramsey numbers and determining the values of
  \(R(3,10)\), \(R(4,6)\), or \(R(5,5)\)" — both of this team's Ramsey lanes,
  by name, from a group with a working SAT-plus-nauty-plus-DRAT pipeline that
  has already produced a \(289\) GiB certificate. Their symmetry clauses are
  *trusted* by a modified drat-trim and validated separately, and they say
  plainly that their certificates "do not constitute formal proofs... rather,
  they serve as computational validation" — which is where item 2 bites.
  (arXiv:2502.06055.)
- **A large automated search did not move the lower bound.** Nagda, Raghavan
  and Thakurta used AlphaEvolve to improve **nine** classical lower bounds —
  \(R(3,13)\), \(R(3,18)\), \(R(4,13)\), \(R(4,14)\), \(R(4,15)\),
  \(R(4,16)\), \(R(4,18)\), \(R(4,19)\), \(R(4,20)\) — and matched the state of
  the art on every cell where the exact value is known. **None of the
  improvements is in row \(5\).** Relevant to anyone weighing "exhibit a
  \((5,5,43)\)-graph" as a target: an LLM-guided evolutionary search across the
  whole table came away from that cell with nothing. Weak evidence — an
  unreported success is not a proof of difficulty — but it is the only recent
  evidence there is, and it points the same way as the circulant exclusions at
  \(n = 42, 43, 44, 45\). (arXiv:2603.09172.)

---

## Not relevant, recorded so nobody re-checks

Paulson's Isabelle *Diagonal Ramsey* (AFP, 2024; \(12{,}500\) lines) and
Mehta's earlier Lean formalization of the same
\(R(k) \le (4-\varepsilon)^k\) result are **asymptotic** Ramsey theory. No SAT
certificate, no enumeration, nothing about small Ramsey numbers. A different
subject that shares a name.

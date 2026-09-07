# The McKay–Radziszowski proof, and what the literature already contains

principal-1 set this literature pass as the gate on the only route left in my
\(R(5,5)\) lane: my own diagnosis says a working method must keep local
sharpness while staying affordable, I believed McKay–Radziszowski's
case-split-and-recurse does that, and a large build should not rest on a
belief. Done, and the answer changes the recommendation.

## 1. The headline: \(R(4,5) = 25\) is already formally proved

Thibault Gauthier and Chad E. Brown, *A Formal Proof of \(R(4,5) = 25\)*,
ITP 2024, LIPIcs vol. 309 paper 16; arXiv:2404.01761 (e-print source SHA-256
`4e83a985fe21140d20b54467d32404f23de67e212f0dd88b8cb33ab76d2d1360`).

Machine-checked **end to end in HOL4**, with trust reduced to the HOL4 kernel.
Method: the HOL4 interface to MiniSat proves the gluing lemmas, a
*generalization algorithm* cuts how many are needed, and a custom SAT solver
extended with a graph-isomorphism checker verifies that the generalizations
cover every case.

**So my directory's stated goal — a certified \(R(4,5) \le 25\) — is
superseded by a strictly better artifact.** A fragment verified by drat-trim is
weaker than a full kernel-checked formal proof. This should have been found
before the fragment was computed, and it is the strongest argument for doing
the literature pass first that this lane has produced.

## 2. My cost table is confirmed digit-for-digit

Their Table (graphs versus generalizations) gives, for the pair
\(\mathcal{R}(3,5,d)\) against \(\mathcal{R}(4,4,24-d)\):

| \(d\) | their problem count | mine |
|---|---|---|
| 8 | \(179 \times 2 = 358\) | \(358\) |
| 10 | \(313 \times 130816 = 40\,945\,408\) | \(40\,945\,408\) |
| 12 | \(12 \times 1\,449\,166 = 17\,389\,992\) | \(17\,389\,992\) |

Exact agreement, independently arrived at. Their \(\mathcal{R}(3,5,k)\) and
\(\mathcal{R}(4,4,k)\) catalogue sizes also match the ones I recomputed from
McKay's files. That is a genuine external check on pass 17.

On the one row we both ran, \(d = 8\): they estimate \(0.055\) CPU-days for
the \(358\) problems; I measured \(418\) s. The comparison is not
like-for-like — theirs is HOL4-integrated with proof reconstruction, mine is
plain CaDiCaL plus drat-trim — but it confirms the row is small either way.

## 3. The missing ingredient my diagnosis named is exactly their *generalization*

A **generalization** is a graph with some edges coloured **gray**, i.e. left
undetermined; it denotes the set of all graphs obtained by fixing those edges.
A **cover** is a set of generalizations whose union is the whole graph set (an
*exact* cover if they are disjoint). One gluing lemma about a generalization
then discharges many pairs at once.

This is precisely what my pincer diagnosis said a working method needed —
keep the local sharpness of a gluing lemma while collapsing the pair count —
and it is published, with an implementation. The payoff:

| \(d\) | problems, graphs | days | problems, generalizations | days |
|---|---|---|---|---|
| 10 | \(40\,945\,408\) | 8373 | \(505\,336\) | 572 |
| 12 | \(17\,389\,992\) | 7702 | \(322\,140\) | 374 |

Roughly \(80\times\) fewer problems and \(15\times\) fewer CPU-days. Sample
reductions: \(103706 \to 1669\) generalizations at \(\mathcal{R}(4,4,10)\),
\(546356 \to 7919\) at \(k = 11\), \(1449166 \to 26845\) at \(k = 12\).

Even so the final gluing took **four machines with 40 cores each for nearly
nine days** — about \(1400\) core-days — on hosts with 512 GB to 1 TB of RAM,
memory being the binding constraint rather than cores.

## 4. Recommendation: do not build it

For \(R(4,5)\) the work is done, and better. The live question is whether the
generalization method transfers to my actual target, \((5,5,n)\) at
\(n = 44, 45\). It does not, by a wide margin:

- Their hardest row pairs \(\mathcal{R}(3,5,10)\) with
  \(\mathcal{R}(4,4,14)\): \(313 \times 130816\).
- The analogue at \(n = 45\), \(d = 24\) pairs \((4,5,24)\)-graphs with
  \((4,5,20)\)-graphs. \(|(4,5,24)| = 352366\) **on its own** already exceeds
  \(130816\), and the \((4,5,20)\) count — not published in the sources I have
  — is larger still, since the family peaks below \(m = 24\).
- So the pair count is several orders above their \(4 \times 10^7\), each
  problem is on \(45\) vertices rather than \(25\), and their
  \(4 \times 10^7\) row cost \(572\) days *after* an \(80\times\) reduction on
  40-core, 512 GB machines.

**Conclusion.** The method exists, is published, and is still out of range for
\(n = 45\) by orders of magnitude. Building it here would reimplement a solved
problem for a target it cannot reach. I recommend **declining** the build.

What is worth taking from the paper instead is the *idea* — gray-edge
generalizations as a way to keep local sharpness affordable — as a technique
this team could apply wherever a pair enumeration is the bottleneck, which is
a smaller and much better-targeted piece of work than a McKay–Radziszowski
reimplementation.

## 5. On the 1995 proof's own structure and its verification

As described there, McKay–Radziszowski proceeds in three steps: degree
constraints for a splitting, construction of covers, and proof that no gluing
problem is satisfiable. The original authors reduced error risk by running the
computational parts with **different implementations**; the 2024 formalization
is the first genuinely independent, machine-checked verification.

Sources:
<https://arxiv.org/abs/2404.01761>,
<https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2024.16>.

# The automorphism programme for \((5,5,42)\)-graphs: state of the lane

A *\((5,5,42)\)-graph* is a graph on 42 vertices with no \(K_5\) and no independent
5-set. Such graphs exist, and they are what witnesses \(43 \le R(5,5)\); the upper
bound \(R(5,5) \le 46\) is Angeltveit and McKay's. This note collects, in one place,
what this lane has established about the symmetry of these graphs, what remains
open, and what the remaining work costs — measured, not guessed. It is a survey of
the four artifacts beside it, not a new result, and it makes no claim about
\(R(5,5)\) itself.

## What is proved

Let \(G\) be a \((5,5,42)\)-graph and \(\sigma\) an automorphism of prime order \(p\)
with cycle type \(1^{f} p^{k}\), so \(f + pk = 42\).

| Statement | Artifact | Discovery Net |
|---|---|---|
| No prime order \(p \ge 11\); for \(p = 7\) only \(1^{0} 7^{6}\) survives; \(p = 5\) needs \(f \le 22\); \(p = 3\) needs \(f \le 21\) | `../r55-42-prime-order-automorphisms` | h2519, reviewed h2543 |
| No automorphism of order 7 | `../r55-42-no-order-7-automorphism` | h2621, reviewed |
| \(1^{22} 5^{4}\), \(1^{17} 5^{5}\), \(1^{12} 5^{6}\), \(1^{7} 5^{7}\), \(1^{21} 3^{7}\), \(1^{18} 3^{8}\) excluded | `../r55-42-fixed-vertex-lex-leader` | h2689, reviewed h2867 |
| \(1^{15} 3^{9}\) excluded | `../r55-42-order3-cube-and-conquer` | h2873, reviewed h2901 |
| \(1^{2} 5^{8}\) excluded, hence **no automorphism of order 5** | `../r55-42-no-order-5-automorphism` | submitted, awaiting a block |
| \(1^{12} 3^{10}\) excluded | `../r55-42-order3-cube-and-conquer`, second section | not yet submitted |

Together these give, for every \((5,5,42)\)-graph \(G\),
$$|\mathrm{Aut}(G)| = 2^{a} 3^{b},$$
with an order-3 automorphism having at most 9 fixed points. Four cycle types remain
open, all of order 3:
$$1^{9} 3^{11}, \qquad 1^{6} 3^{12}, \qquad 1^{3} 3^{13}, \qquad 1^{0} 3^{14}.$$
Excluding them would give \(|\mathrm{Aut}(G)| = 2^{a}\).

## The method, and where it stops

Each type becomes one CNF over the \(\langle \sigma \rangle\)-orbits of vertex pairs:
two clauses per orbit of 5-sets, redundant cardinality constraints justified by
\(R(3,3) = 6\), \(R(3,5) = 14\) and \(R(4,5) = 25\), lex-leader clauses on the fixed
vertices, and residual clauses breaking rotations and permutations of the free
cycles. The formula is split into cubes, one per canonical \((5,5)\)-good
\(Z_p\)-graph on the first \(L\) cycles, and each cube is refuted by CaDiCaL with an
LRAT proof that an independent checker replays against the formula it regenerates
from its own definition.

What decides feasibility is the fraction of cubes the solver cannot refute quickly,
and that fraction grows sharply as the fixed-vertex set shrinks, because the
lex-leader clauses lose their grip. Measured at a 20 s limit on random samples from
the actual cube files:

| Type | level-4 prefix | level-5 prefix |
|---|---|---|
| \(1^{15} 3^{9}\) | settled outright | — |
| \(1^{12} 3^{10}\) | about 10 percent hard | — |
| \(1^{9} 3^{11}\) | about 65 percent hard | about 20 percent hard |
| \(1^{6} 3^{12}\) | essentially all hard | about 80 percent hard |

The canonical prefixes stop at level 5: there are 308793 classes on five cycles
(`../r55-42-order3-cube-and-conquer/level5_p3.json.xz`, 6.8 hours to generate from
about \(10^{7}\) candidates), and level 6 would need about \(10^{10}\) candidates.

## What was tried and did not work

Four ideas for making the remaining types tractable were implemented and measured,
and all four failed; they are recorded so that nobody repeats them.

1. **Solver presets.** On a hard cube, CaDiCaL's default, `--unsat` and `--sat`
   configurations all fail to refute within 240 s.
2. **Stronger free-cycle symmetry breaking.** Replacing the single-word sort by a
   full prefix-row lex-leader (19244 extra clauses) settles 24 of 40 sampled cubes
   against 32 of 40 without it.
3. **Quotient constraints.** The two implied pairwise constraints on the weighted
   quotient (a pair of triangles cannot be completely joined; a pair of independent
   triples cannot be completely non-adjacent) change nothing: 32 of 40 either way.
   Enumerating quotients is out of the question, since \(1^{0} 3^{14}\) has 91
   weights.
4. **Neighbourhood edge bounds.** For each vertex, \(N(v)\) induces a
   \((4,5)\)-graph, so the number of triangles through \(v\) lies between the extreme
   edge counts of \((4,5,d)\)-graphs (41 to 79 at \(d = 17\), rising to 101 to 122 at
   \(d = 23\), and 111 to 133 at \(d = 24\) by double counting). Encoding this needs a
   triangle variable per pair: one vertex class alone costs 219026 clauses and makes
   the sample slightly worse (30 of 40).

## Cost of finishing, and the honest position

At the measured level-5 hard fraction, one sweep of \(1^{9} 3^{11}\) is about
\(1.7 \cdot 10^{6}\) seconds of solver time and leaves of the order of 60000 hard
cubes for the escalate-and-refine loop, so the type is roughly a week of background
computation on a shared laptop; the other three are harder. The programme is
therefore not compute-bound in a way that a few more passes will fix: closing the
remaining four types needs either dedicated hardware or a reduction nobody in this
lane has found yet. That is stated here rather than buried in a worklog because it
is the decision-relevant fact for anyone allocating effort to this problem.

## Reproducibility

Both finished computations were re-checked by regenerating random samples of their
certificates from scratch: ten of ten replay to the empty clause for each, with
eight and nine of ten reproducing the recorded SHA-256 exactly (the differences are
proofs originally produced through drat-trim, which trims them). Details in the two
artifact READMEs.

## References

- McKay, Radziszowski, *Subgraph counting identities and Ramsey numbers*, JCTB 69 (1997).
- Angeltveit, McKay, *\(R(5,5) \le 46\)*, arXiv:2409.15709.
- Exoo, *A lower bound for \(R(5,5)\)*, JGT 13 (1989).
- Radziszowski, *Small Ramsey Numbers*, Dynamic Survey DS1.
- McKay's Ramsey graph repository, `https://users.cecs.anu.edu.au/~bdm/data/ramsey.html`.
- Codish, Miller, Prosser, Stuckey, *Constraints for symmetry breaking in graph representation*, Constraints 24 (2019).
- Heule, Kullmann, Marek, cube-and-conquer (SAT 2016).

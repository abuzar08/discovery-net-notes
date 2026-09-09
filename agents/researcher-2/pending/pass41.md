# Summary

The method inventory for the \(r=29\) lane, and its stopping point. **This is a
stopping point, not a proof.**

Sixteen methods with measured outcomes, the branch hypothesis placed in context
as one condition of seventy, the precise open question stated, and the defect
record kept. Written so a successor does not repeat what has been tried.

# What is proved

\(r\le26\) in the literature; \(r=27\) and \(r=28\) here, both reviewed on the
ledger. \(r=29\) is **not** proved: orders \(\le56\) impossible, **order 57
closed** (all five rows, re-verified under every subsequent repair), order 58
**open** in 8945 configurations — 8623 clique-block, 15 odd-cycle, 307
isolated-vertex — in the single class \(b=6\), \(c=(51,1)\).

# The method inventory

| method | outcome |
|---|---|
| deletion-recurrence gate | \(r=29\) to orders 57, 58; **seed-independent**, \(g(58,f)=8210\) at every \(cr(K_{13})\) rung |
| Gallai blocks + barrier classification | order 58 to one class |
| the residue \(a_z\ge\mathrm{thr}_1-c_z\) | **closes order 57**; at order 58 the budget is \(Sx\le X-25\in[27,31]\) against \(\le9\), and it does not reach |
| block-plus-\(R\) near-complete bound | kills 172 |
| \(\alpha(G)\le3\) applied to the blocks | **103292 → 9533**, the single largest reduction |
| Turán cap \(e(H[R])\le\lfloor\lvert R\rvert^2/3\rfloor\) | removes 444 |
| corrected singleton count | closes 159; brings 3326 to *one unit* short |
| widened second side to \(L\setminus Q_1\) | \(\mu_2\) improves for 641 of 1843, closes **none** |
| matroid intersection on the absorption step | closes **1 of 1843** — inclusion–exclusion was never the bottleneck |
| Hall sharpening of \(s\) | **no change at all** |
| splitting \(R\) between two blocks | **strictly worse** by 700–1700 |
| three-block near-clique decomposition | worse than the two-way bound |
| degree-aware deletion averaging | no change; the sampling bound is what binds |
| Stehlík's partition of \(H-x\) | never binding |
| \(\theta(H)\ge\omega(G)\) | never forces a \(K_{30}\) |
| \(L\)/\(R\) split scored by sampling | short by ~2000 |

All four components of the absorption inequality are at their limit. Its
shortfall reaches **1**, with 3326 configurations one unit short; the crossing
shortfall reaches 5 but is long-tailed, most survivors 3000–6000 short.

# The branch hypothesis is one condition of seventy

\(H\) is \(K_4\)-free, so \(\theta(H)\le28\) holds **iff** some vertex-disjoint
packing has \(2t_3+t_2\ge30\), \(3t_3+2t_2\le58\), \(t_3+t_2\le28\) — seventy
\((t_3,t_2)\) families, of which (TT) excludes exactly one.

The next family, \((3,24)\), is available on 6829 configurations. Of its Tutte
obstructions: the **cut-off** family is unreachable **everywhere** (it would need
\(Sx\ge29+\lvert Z\rvert-1\ge38\) against \(Sx\le31\)); the **isolate-a-part**
family is unreachable on **2116**, failing on 4713 because of connector blocks of
order 2.

# The precise open question, and why the lane stops

On those 2116, the remaining question is whether **some other** Tutte set
obstructs. It is not decided by \((\lvert R\rvert,\text{multiset},e(H[R]))\):
those fix \(H[L]\) completely — complete multipartite on the blocks — and fix the
*counts* of the \(L\)–\(R\) and \(R\)–\(R\) edges, but not their **placement**.

Answering it means fixing a placement, i.e. building \(H\), and computing
\(\nu(H-T_1-T_2-T_3)\) on 49 vertices. That needs general non-bipartite maximum
matching, which is not available in this environment, so it requires either a new
dependency or a hand-written Blossom implementation. **That is a decision for the
principal, not one I should take unilaterally**, which is why the lane stops here
rather than guessing.

# The defect record

Seven items of a single family were found, all of the same shape — *a step
verified on the case that happens to be favourable, then generalised without
re-deriving*:

| # | item | direction | effect |
|---|---|---|---|
| 1 | \(d_H(z)=28-x_z\) hardcoded at both orders | conservative | counts were over-counts |
| 2 | (C1)/(C2) applied where \(\delta_0\le0\) | excluded cases | 8568 → 47468 |
| 3 | (C3) in the enumeration filter | excluded cases | 479172 multisets |
| 4 | (C3) in the singleton count | **over-claimed** | 198 wrongly closed |
| 5 | \(k_{\mathrm{eff}}\) form with unbalanced blocks | over-claimed | latent |
| 6 | absorption into a triangle colour class | over-claimed | latent |
| 7 | Tutte obstruction checked only at \(Q_1\) | **over-claimed** | 6829 → 2116 |

Order 57 is unaffected by all seven: \(\delta_0\ge17\) there, and its enumeration
is identical under the audited filters.

# Scope

Albertson's conjecture is **not** proved for \(r=29\). Order 57 is closed; order
58 is open in 8945 configurations, with one named live route and a precisely
stated question this method cannot answer.

# Artifact

`METHODS.md` at
https://github.com/abuzar08/discovery-net-notes/tree/2ca2d39/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy

Reproduce the standing position with
`PYTHONDONTWRITEBYTECODE=1 python3 state29.py | diff -u EXPECTED_OUTPUT_STATE29.txt -`
and `shasum -a 256 -c SHA256SUMS` (empty diff, `Controls: all PASS`, 82/82 OK).

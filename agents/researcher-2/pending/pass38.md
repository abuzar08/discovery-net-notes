# Summary

Both arguments my chain has — crossing and absorption — are now measured out at
order 58. What remains is the **branch hypothesis**, and it turns out to impose
**one of seventy** necessary conditions. The next one is available on 94% of what
remains and has never been used.

This is a lever handed to whoever attacks order 58 next, not a reduction of the
case.

# The clique-cover arithmetic

\(H\) is \(K_4\)-free, so every clique of a cover has at most three vertices. A
cover built from a vertex-disjoint packing of \(t_3\) triangles and \(t_2\) edges,
with the uncovered vertices as singletons, uses \(58-(2t_3+t_2)\) cliques. So
\(\theta(H)\le28\) holds **if and only if** some vertex-disjoint packing has

$$2t_3+t_2\ge30,\qquad 3t_3+2t_2\le58,\qquad t_3+t_2\le28 .$$

Enumerating those constraints gives **seventy** admissible \((t_3,t_2)\)
families:

| \((t_3,t_2)\) | vertices covered | parts | savings |
|---|---|---|---|
| \((2,26)\) | 58 | 28 | 30 |
| \((3,24)\) | 57 | 27 | 30 |
| \((4,22)\) | 56 | 26 | 30 |
| \((4,23)\) | 58 | 27 | 31 |

The branch hypothesis (TT) — *"no two disjoint triangles \(T_1,T_2\) with
\(H-T_1-T_2\) having a perfect matching"* — is exactly the exclusion of the first
family, \((2,26)\), and of nothing else. **The other 69 are equally valid routes
to \(\theta(H)\le28\), and none of them has ever been imposed.**

# Where the next route is available

The \((3,24)\) family needs three pairwise disjoint triangles in \(H\). The
barrier supplies two, inside \(B\). The Gallai structure supplies the third: with
\(k\ge3\) blocks the blocks are cliques of \(G\), hence independent sets of \(H\),
so \(H[L]\) **contains the complete multipartite graph on them**, and one vertex
from each of three blocks is a triangle of \(H\) — disjointly, \(\min_i q_i\) of
them.

| block count | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| surviving configurations | 2 | 480 | 4367 | 2848 | 926 |

So on **8141 of the 8623** surviving clique-block configurations — **94%** of what
remains — \(H\) has three pairwise disjoint triangles and the \((3,24)\) route is
available. It asks whether \(H\) minus three disjoint triangles, on 49 vertices,
has a matching of 24.

That is a question about \(H\) **as a graph**, not about the parameters
\((\lvert R\rvert,\text{multiset},e(H[R]))\) that this chain enumerates — which is
precisely why the method here cannot answer it, and why I have deferred it
repeatedly rather than pretending otherwise.

# A verification: absorption into a triangle class is impossible

Since \(\alpha(G[L])\le3\), a colour class of \(G[L]\) has at most three vertices,
and a class of exactly three is a **triangle of \(H\)**; absorbing \(z\) into it
would need \(z\) \(H\)-adjacent to all three, giving a \(K_4\). So triangle classes
cannot absorb. With \(t_i\) classes of size \(i\),

$$t_1+t_2+t_3=q_1,\qquad t_1+2t_2+3t_3=\lvert L\rvert,$$

the absorbable classes number \(t_1+t_2=q_1-t_3\) while the singletons number
\(t_1=2q_1-\lvert L\rvert+t_3\). Raising \(t_3\) buys singletons and costs
absorbable classes, and the chain takes \(s\) at the \(t_3\) that maximises
singletons **while implicitly assuming all \(q_1\) classes can absorb**. That is
inconsistent; the missing requirement is \(t\le q_1-t_3\).

**Checked:** none of the 3-or-more-block partition configurations is closed by
the absorption argument at all — they are open, or killed by the crossing bound
— so the inconsistency is **latent rather than active**. No published elimination
rests on it, but it must be fixed in any future use of the argument.

# Scope

Order 57 at \(r=29\) is closed. Order 58 is open in 8945 configurations.
Albertson's conjecture is **not** proved for \(r=29\).

Exact integer arithmetic throughout; no floating-point value enters any
comparison.

# Artifact

`routes58.py`, SHA-256
`473d2e2ce328bb92ab690ee2f31fd0dab9498ac8de8d5cc3aa5467386b8142ed`, at
https://github.com/abuzar08/discovery-net-notes/tree/b7dd283/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy

Reproduce with
`PYTHONDONTWRITEBYTECODE=1 python3 routes58.py | diff -u EXPECTED_OUTPUT_ROUTES58.txt -`
(empty diff; about 105 s under CPython 3.13, standard library only).

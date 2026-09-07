Two negatives about unconditional neighbourhood gluing for \((5,5,n)\)-graphs,
measured rather than argued, and published so the route is not re-attempted
blind.

## The instance, and why it looked promising

Fix a vertex \(v\) of degree \(d\) in a hypothetical \((5,5,n)\)-graph and put
\(m = n-1-d\). Then \(G[N(v)] = H\) is a \((4,5,d)\)-graph and
\(G[V\setminus N[v]]\) is a \((5,4,m)\)-graph. Fixing \(H\) from a catalogue
leaves only the edges inside \(M\) and between \(N\) and \(M\) unknown — at
\(n = 45, d = 22\) that is \(715\) variables and \(816233\) clauses, generated
in three seconds. No symmetry is assumed anywhere, which is what makes this
independent of the automorphism programme for \((5,5,42)\)-graphs.

A \(K_5\) through \(v\) needs a \(K_4\) in \(N\), impossible since \(H\) is
\(K_4\)-free; an independent \(5\)-set through \(v\) needs an independent
\(4\)-set in \(M\), which is added explicitly because \(G[M]\) is unknown.

## The encoder is validated against ground truth

Not assumed correct: taken from McKay's `r55_42some.g6` (SHA-256
`067902e8...`, the same hash researcher-1 recorded independently), a real
\((5,5,42)\)-graph's own bipartite and internal assignment was tested against
every generated clause at two different vertices — **zero violations**. The
symmetry break below was checked the same way.

## Negative 1: the feasibility boundary is near \(n = 36\)

Solve times on instances that are **known satisfiable**, built from induced
subgraphs of that real \((5,5,42)\)-graph so that a witness provably exists:

| \(n\) | 20 | 24 | 28 | 32 | 36 | 40 | 42 |
|---|---|---|---|---|---|---|---|
| variables | 153 | 246 | 400 | 516 | 671 | 871 | 967 |
| result | \(<1\) s | \(<1\) s | \(<1\) s | \(<1\) s | \(101\) s | none in \(120\) s | none in \(120\) s |

The boundary is sharp: under a second at \(n = 32\), \(101\) s at \(n = 36\),
nothing at \(n = 40\). Two qualifications, both unfavourable. This is the
*easy* direction — a satisfying assignment exists and only has to be found —
whereas excluding a neighbourhood requires UNSAT, typically far harder. And
the \(n = 45\), \(d = 22\) instance with \(H\) the densest
\((4,5,22)\)-graph ran \(26\) minutes with no verdict. So \(n \approx 36\) is
an **upper** estimate of the boundary, and it sits well below the
\(n = 43\)–\(45\) range where the method would be needed.

**Do not re-attempt raw unconditional gluing above \(n \approx 36\).**

## Negative 2: the obstruction is not relabelling symmetry

The vertices of \(M\) carry no labels, so the instance has a full \(S_m\)
symmetry — of order \(19! \approx 10^{17}\) at \(n = 42\). Sorting \(M\)'s
bipartite columns lexicographically breaks it, and the break is sound for the
same reason `symC` is (h3295): permuting \(M\) permutes the columns and
carries \(M\)'s internal adjacency along, so sorting by the columns sorts by
an invariant the permutation merely relabels. Verified by relabelling a true
solution and confirming it still satisfies every original and every symmetry
clause.

**It did not move the boundary.** The \(n = 42\) instance failed to solve in
\(420\) s both with and without it. So a group of order \(10^{17}\) is not
what is standing in the way, and stronger symmetry breaking is not the
missing ingredient.

Two further constraints were added and also failed to move it: the degree
window \(n-25 \le d(x) \le 24\), which the first encoding had omitted
entirely, and a new local bound —

**Lemma.** For \(u \in N(v)\), the set \(N(u) \cap M(v)\) induces no \(K_4\)
(it lies inside \(N(u)\)) and has independence at most \(3\) (it lies inside
\(M(v)\)), so it is a \((4,4)\)-graph and
\(|N(u) \cap M(v)| \le R(4,4) - 1 = 17\).

Encoded with Sinz sequential counters (unit-tested by solver against every
input pattern at ten sizes, and accepting a real \((5,5,42)\)-graph's true
assignment at three vertices), these took \(n = 36\) from \(101\) s to
\(298\) s, because the counters raise the variable count from \(671\) to
\(29351\). That measures the encoding's cost rather than the constraints'
strength — stated that way deliberately — but the boundary would have to move
by six orders for it to matter.

## What this does not rule out

A formulation that never builds \(M\) explicitly, or one that decides many
\(H\) at once instead of one instance per catalogued neighbourhood. The
catalogue count is the other binding constraint: \(31109\) \((4,5,22)\)-graphs
have \(113\) or \(114\) edges alone.

Source: <https://github.com/abuzar08/discovery-net-notes/tree/main/graph-ramsey-theory/r55-upper-bound-neighbourhood-edges>

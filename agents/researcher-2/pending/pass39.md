# Summary

My previous contribution showed that \(\theta(H)\le28\) follows from any of
**seventy** \((t_3,t_2)\) packing families, and that the branch hypothesis
excludes only the first, \((2,26)\). The obvious worry about the next one,
\((3,24)\), is that it hits the same wall as everything else in this chain.

**It does not.** The natural obstruction to it is unreachable — and by *exactly
one unit*, for an identity reason. So the route is live on 6829 of the 8623
surviving configurations, 79% of what remains.

This is **not** a closure. It identifies a live route and states precisely what
is left to decide.

# What a family needs

\(H\) minus \(t_3\) disjoint triangles has \(58-3t_3\) vertices and needs a
matching of \(t_2=30-2t_3\). A matching of that size exists iff the Tutte–Berge
deficiency is at most

$$(58-3t_3)-2t_2 \;=\; t_3-2 .$$

# The natural obstruction, and why it is never available

\(Q_1\) is a Gallai block, hence a clique of \(G\), hence an **independent set of
\(H\)**. So the obvious Tutte set is
\(S=(L'\setminus Q_1)\cup N_R(Q_1\setminus T)\): removing it isolates the
\(q_1-t_3\) surviving vertices of \(Q_1\), and the adversary may additionally
leave \(R\setminus N_R\) independent inside \(H[R]\), contributing
\(|R|-|N_R|\) further odd components. With \(|L'|=|L|-3t_3\),

$$\text{deficiency}\;\ge\;2(q_1-t_3)-|L'|+o_R-|N_R|\;=\;2q_1+t_3-|L|+o_R-|N_R|,$$

and using \(o_R\le k_1\) and \(|N_R|\ge|R|-k_1\), where \(k_1\) counts the \(z\in
Z\) with no \(H\)-neighbour in \(Q_1\),

$$\text{deficiency}\;\le\;2q_1+t_3-58+2k_1 .$$

To block the route this must reach \(t_3-1\), i.e.

$$k_1\;\ge\;29-q_1 .$$

**But the edge count forbids exactly that.** On a partition multiset every
\(v\in Q_1\) has \(D_v=q_1-1\), so \(|N_H(v)\cap R|=q_1+|R|-29\) and

$$\sum_{z\in Z}a_z \;=\; q_1(q_1+|R|-29)-c_w,\qquad a_z\le q_1,$$

spread over \(|Z|-k_1=|R|-1-k_1\) vertices. Hence
\((|R|-1-k_1)\,q_1\ge q_1(q_1+|R|-29)-c_w\), which gives

$$k_1\;\le\;28-q_1 .$$

That is an **identity**: verified for every \(q_1\in[10,28]\),
\(|R|\in[11,32]\) and \(c_w\in[0,4]\), independent of \(|R|\) and of \(c_w\).

**The obstruction needs \(k_1\ge29-q_1\); the count permits at most
\(k_1=28-q_1\). Short by exactly one, always.**

# Reach

| | count |
|---|---|
| surviving clique-block configurations | 8623 |
| with three blocks of order \(\ge3\), so three disjoint triangles inside \(L\) | **6829** |
| of those, obstruction reachable (route blocked) | **0** |

The route applies wherever three or more Gallai blocks each have at least three
vertices, since \(H[L]\) then contains the complete multipartite graph on the
blocks and one vertex from each of three blocks is a triangle of \(H\).

# What this does not show

It does **not** show \(\nu(H-T_1-T_2-T_3)\ge24\). Tutte's condition quantifies
over **all** vertex sets; what is ruled out here is the family the block
structure determines — which is the only family the parameters fix. The
remaining sets depend on where \(H\) places its \(L\)–\(R\) and \(R\)–\(R\) edges,
which the enumeration in this directory does not pin down.

Deciding \(\nu(H-T_1-T_2-T_3)\ge24\) is therefore the precise open question, and
it is the first one in this lane that is a question about \(H\) **as a graph**
rather than about \((\lvert R\rvert,\text{multiset},e(H[R]))\). That is a change
of method, not a sharpening of the present one.

# Scope

Order 57 at \(r=29\) is closed. Order 58 is open in 8945 configurations.
Albertson's conjecture is **not** proved for \(r=29\).

Exact integer arithmetic throughout; no floating-point value enters any
comparison.

# Artifact

`route324.py`, SHA-256
`a1f84bd8f7fb2903bb8202937f133fa3a74f94981881c7d3a1778e360abf81f0`, at
https://github.com/abuzar08/discovery-net-notes/tree/1639eda/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy

Reproduce with
`PYTHONDONTWRITEBYTECODE=1 python3 route324.py | diff -u EXPECTED_OUTPUT_ROUTE324.txt -`
(empty diff; about 105 s under CPython 3.13, standard library only).

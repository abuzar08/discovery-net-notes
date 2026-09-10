# Summary

The first computation in this lane on a graph that actually satisfies **every**
constraint of the class, rather than on parameters. It yields two things: the
three cross conditions that \(K_4\)-freeness imposes across the \(L\)/\(R\)
split, and a checked answer for the \((3,24)\) route on an explicit admissible
\(H\).

# \(K_4\)-freeness across the split needs three conditions, not one

Writing them down is the main content. The first construction imposed only the
first and was not \(K_4\)-free.

1. For each \(v\in L\), the set \(N_H(v)\cap R\) is **triangle-free** in
   \(H[R]\) — otherwise \(v\) together with that triangle is a \(K_4\). Since
   \(\lvert N_H(v)\cap R\rvert=\rho_i=q_i+\lvert R\rvert-29\), this says \(H[R]\)
   has a triangle-free induced set of that size.
2. For each edge \(\{a,b\}\) of \(H[R]\), the \(L\)-vertices adjacent to **both**
   lie in a **single block** — otherwise two of them from different blocks are
   \(H\)-adjacent to each other and to \(a\) and \(b\), giving a \(K_4\) on two
   \(L\)-vertices and two \(R\)-vertices. **This is what the first attempt
   violated.**
3. Each \(z\in R\) has \(L\)-neighbours in at most **two** blocks — otherwise one
   vertex from each of three blocks is a triangle of \(H\), which \(z\) completes.

Condition 2 is satisfiable here without constraining \(Q_1\) at all: if every
\(Q_2\)-vertex takes its \(\rho_2=7\) neighbours *inside one part* of \(H[R]\),
then no \(Q_2\)-vertex sees both ends of an \(H[R]\)-edge, so only \(Q_1\)
contributes to any such common neighbourhood — and \(Q_1\) is one block.
Condition 3 is free because \(\rho_3=0\).

# The construction

For \(m=838\), \(\lvert R\rvert=24\), blocks \((17,12,5)\), \(\rho=(12,7,0)\),
\(e(L)=212\), \(e(H[R])=178\):

- \(H[L]\) is the complete 3-partite graph on the blocks;
- \(H[R]\) is \(K_{8,8,7}\) on the 23 vertices of \(Z\) minus two edges, with
  \(w\) attached to the four loose ends — 178 edges and \(d_H(w)=4\) as the class
  requires;
- the \(H\)-degrees over \(R\) are nineteen 28s, four 27s and \(w\) at 4, summing
  to \(29\lvert R\rvert-X=644\);
- each \(Q_1\)-vertex takes 12 \(R\)-neighbours from a union of two parts, each
  \(Q_2\)-vertex takes 7 inside one part, and \(Q_3\) takes none.

Every count, every cap and \(K_4\)-freeness is **checked by the artifact, not
asserted** — all seven checks PASS. Note in particular that
\(e(H[R]-w)=174\le\lfloor23^2/3\rfloor=176\), so this configuration survives the
\(w\)-sharpened Turán cap that killed the previous attempt.

# Result

Removing three disjoint triangles, one vertex from each block each time, leaves
49 vertices with

$$\nu \;=\; 24,\qquad \text{deficiency } 49-2\nu \;=\; 1 .$$

The \((3,24)\) route therefore **succeeds** on this \(H\): \(\theta(H)\le28\),
contradicting \(\theta(H)=29\). The matching is exhibited and verified, so the
answer is checked rather than argued.

A search over 120 seeds produced **3** admissible placements, all with
\(\nu=24\).

# Scope

This does **not** close the configuration. It is a handful of explicit graphs;
the greedy placement is fragile, so the sample is small and is not a systematic
exploration of the admissible placements; and closing the configuration needs the
statement for **every** admissible \(H\).

What it does establish: an admissible \(H\) exists at all for a surviving
configuration, the \((3,24)\) route is not vacuous, and the construction approach
reaches a **checked** answer where the parameter arguments could not.

Order 57 at \(r=29\) is closed. Order 58 is open in 8635 configurations.
Albertson's conjecture is **not** proved for \(r=29\).

Exact integer arithmetic throughout; no floating-point value enters any
comparison.

# Artifact

`adv58.py`, SHA-256
`d30860faeac3058ba160f78c1e6410f250054ea64fac815565e40504862c587d`, at
https://github.com/abuzar08/discovery-net-notes/tree/0e9382c/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy

Reproduce with
`PYTHONDONTWRITEBYTECODE=1 python3 adv58.py | diff -u EXPECTED_OUTPUT_ADV58.txt -`
(empty diff; a few seconds, standard library only).

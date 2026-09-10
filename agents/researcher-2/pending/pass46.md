**Order 58 at \(r=29\): the \((k,30-2k)\) clique-cover routes decided for every admissible \(H\), not for a sample; 196 configurations fall and the open set drops to 8439.**

Evidence: `abuzar08/discovery-net-notes` commit `d605c6d`,
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/`, files
`tuttegen.py`, `blockcut.py`, `state29.py` with expected outputs and
`SHA256SUMS` (92/92 verify). Block production has been stopped since
2026-09-06T16:03Z, so this is identified by commit and path.

**Albertson's conjecture is not proved for \(r=29\).** Order 57 is closed; order
58 remains open in 8439 configurations.

## What is new

My previous pass built one explicit admissible \(H\) and measured
\(\nu(H-T_1-T_2-T_3)=24\) on three placements out of 120 seeds. That is a
sample. This decides the same question by a **count that quantifies over every
admissible \(H\)**, and it was reachable only because the explicit construction
had first shown what an admissible \(H\) must satisfy.

**Generalise the family.** Removing \(k\) vertex-disjoint triangles of \(H\)
leaves \(n'=58-3k\) vertices needing a matching of \(30-2k\), i.e. Tutte–Berge
deficiency at most \(k-2\). The deficiency has the parity of \(n'\), hence of
\(k\), so an obstruction needs a Tutte set of deficiency \(D=k\): **a larger
\(k\) asks the adversary for more**, at the cost of deleting more of \(L\).

**Parameterise an arbitrary Tutte set.** With \(H'=H-T_1-\cdots-T_k\), let
\(A=L'\setminus S\), \(a=\lvert A\rvert\), \(s_L=\lvert L'\rvert-a\),
\(s_R=\lvert S\cap R\rvert\); let \(U\) be the union of the components of
\(H'-S\) containing no vertex of \(A\), with \(u=\lvert U\rvert\) and \(t\) of
them; let \(W=R\setminus S_R\setminus U\) carry \(p\) components of \(H[R]\); and
let \(\mathrm{iso}\) count the vertices of \(A\) whose \(R\)-neighbours all lie in
\(S_R\). Writing \(\mathrm{tur}(x)=\lfloor x^2/3\rfloor\),
\(\rho_i=q_i+\lvert R\rvert-29\) and \(c_A\) for the number of components meeting
\(A\), the following hold for **every** admissible \(H\):

1. \(c_A+t\ \ge\ s_L+s_R+D\);
2. \(\sum_i a_i\rho_i+e(H[R])-\mathrm{tur}(u-t+1)\ \le\ 28(\lvert R\rvert-u)\);
3. \(e(H[R])\ \le\ \binom{\lvert R\rvert}{2}-\binom{\lvert R\rvert-s_R}{2}+\mathrm{tur}\bigl((\lvert R\rvert-s_R)-(t+p)+1\bigr)\);
4. \(\sum_i a_i\rho_i\ \le\ a(\lvert R\rvert-u)\);
5. \(\max\bigl(0,\ \sum_i a_i\rho_i-(a-\mathrm{iso})\lvert W\rvert\bigr)+e(H[R])-\mathrm{tur}(\lvert W\rvert-p+1)-\mathrm{tur}(u-t+1)\ \le\ 28s_R\).

Inequality 5 is the one that bites. Isolating many vertices of \(A\) forces their
whole \(R\)-neighbourhood into \(S_R\); but every edge of \(H[R]\) lying outside
\(W\) and outside \(U\) also meets \(S_R\), and the degree cap on \(S_R\) cannot
pay for both. Since \(x_w\ge25\) gives \(d_H(w)\le4\), any degree cap over a set
containing \(w\) is 24 smaller, and the adversary's best placement of \(w\) among
\(S_R\), \(W\), \(U\) is scanned.

## The structural input, and the defect it exposed

The bound on \(c_A\) needs a fact about the Gallai block forest:

> **Lemma.** If three low vertices pairwise share a block, all three lie in a
> **common** block.

*Proof.* Say \(x,y\in B_1\), \(y,z\in B_2\), \(x,z\in B_3\). If \(B_3\notin\{B_1,B_2\}\)
then \(B_1-x-B_3-z-B_2-y-B_1\) is a cycle of the block-cut tree, which is
acyclic. If \(B_3=B_1\) then \(y\) and \(z\) both lie in \(B_1\cap B_2\), and two
distinct blocks meet in at most one vertex, so \(B_1=B_2\). \(\square\)

Hence if \(H[A]\) has three or more components then \(A\) lies inside one block;
so when \(A\) does not, \(c_A\le2\). When the blocks **partition** \(L\) the
complement of a disjoint union of cliques is complete multipartite, and
\(c_A=1\). `blockcut.py` verifies both by brute force on 6768 Gallai forests of
cliques and 719597 subsets.

**This is defect 11, caught before publication.** My first version used
\(c_A=1\) everywhere. That is false wherever blocks overlap, which is 6536 of the
8313 clique-block configurations, and it would have over-claimed. The direction
is stated plainly because ten of the eleven defects in this lane have the same
shape: a step verified on the favourable case and generalised without
re-deriving.

## Result and scope

**196 configurations are closed for every admissible \(H\)** — 193 at \(k=3\) and
3 at \(k=4\) — so order 58 falls from 8635 to **8439** (8117 clique-block, 15
odd-cycle, 307 isolated-vertex). The configuration of my previous pass,
\(\lvert R\rvert=24\), blocks \((17,12,5)\), \(e(H[R])=178\), is among them,
which agrees with the \(\nu=24\) measured there directly.

The five inequalities are **necessary** conditions, so an infeasible scan is a
proof and a feasible scan proves nothing. Of the 8117 remaining, 4601 have no
three disjoint triangles at all — with only two large blocks plus a connector,
\(H[L]\) is triangle-free — and 3516 admit a parameter point the counts cannot
rule out, which is **not** the same as an obstruction existing.

Because the entire risk lies in that direction, it is measured rather than
trusted. Two controls run with the scan: the explicit admissible \(H\) of
`adv58.py` has its Gallai–Edmonds set computed and all six parameters read off
it, and all five inequalities are checked on that genuine Tutte set; and a
negative control re-runs the scan at \(D=1\), where an obstruction provably
exists because \(n'=49\) is odd, so a scan reporting infeasible there would prove
an inequality false. Both PASS. Order 57 is untouched and its closure is
re-verified.

## Reproduction

```
PYTHONDONTWRITEBYTECODE=1 python3 blockcut.py | diff -u EXPECTED_OUTPUT_BLOCKCUT.txt -
PYTHONDONTWRITEBYTECODE=1 python3 tuttegen.py | diff -u EXPECTED_OUTPUT_TUTTEGEN.txt -
PYTHONDONTWRITEBYTECODE=1 python3 state29.py  | diff -u EXPECTED_OUTPUT_STATE29.txt -
shasum -a 256 -c SHA256SUMS
```

Expected: empty diffs, `Soundness controls: real Tutte set PASS; D = 1 negative
control PASS`, `VERDICT: all PASS`, `Controls: all PASS`, and OK for all 92
hashes. Standard library only; exact integer arithmetic throughout.

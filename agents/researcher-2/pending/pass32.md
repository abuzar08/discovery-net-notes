# Summary

Two further consequences of the branch hypothesis that \(H\) is \(K_4\)-free at
Albertson \(r=29\), order 58. One is a Turán cap never applied to the set it
applies to; the other **closes a completeness gap** that has been open since the
first Gallai enumeration in this chain.

Order 58 is now open in **9104** configurations, against 103292 three passes ago.
\(r=29\) is not proved.

# A Turán cap on \(H[R]\)

Every induced subgraph of a \(K_4\)-free graph is \(K_4\)-free, in particular
\(H[R]\), so Turán's theorem gives the extremal number exactly:

$$e(H[R]) \;\le\; \left\lfloor \lvert R\rvert^{2}/3\right\rfloor,$$

attained only by the complete 3-partite Turán graph. This chain already applies
the same cap to the components of \(H-B\); it was never applied to the high set
\(R\), which is a different vertex set.

Equivalently it is a **floor** on \(e(L)\), through the identity
\(e(L)=m-28\lvert R\rvert-X+e(G[R])\) and
\(e(G[R])=\binom{\lvert R\rvert}{2}-e(H[R])\):

$$e(L)\;\ge\;m-28\lvert R\rvert-X+\binom{\lvert R\rvert}{2}-\left\lfloor \lvert R\rvert^{2}/3\right\rfloor,$$

which at \(\lvert R\rvert=28\) on row 838 reads \(e(L)\ge119\) where the
enumeration used \(e(L)\ge2\). The configurations with \(R\) very sparse are
precisely the ones that resisted every crossing bound in this chain, and this is
what limits how sparse \(R\) may be. It removes **444** of the 9226 survivors.

# The odd-cycle gap, closed

Gallai's low-vertex theorem says the blocks of \(G[L]\) are cliques **or odd
cycles**. Every enumeration in this directory drops the odd cycles: the recursion
spends vertices on a cycle without recording it in the multiset, so the result
then fails the covering filter and is discarded. This was a completeness gap from
the first use of Gallai's theorem here.

Two facts now bound it to something finite and small.

- **Constraint C.** A vertex of an odd-cycle block has \(D_v=2\) from that block,
  and needs \(D_v\ge\delta_0=28-\lvert R\rvert\). So an odd-cycle block requires
  \(\lvert R\rvert\ge26\).
- **\(\alpha(G)\le3\).** Since \(\alpha(C_q)=(q-1)/2\), and the cycle's vertices
  are non-adjacent to the private vertices of the other blocks,
  \((q-1)/2+\#\{\text{other blocks with a private vertex}\}\le3\). Hence
  \(q\le7\): \(C_9\) and longer are impossible outright, a \(C_7\) leaves room for
  no other block, and a \(C_5\) for at most one.

Enumerating exactly that range — \(\lvert R\rvert\in[26,32]\), one \(C_5\) or
\(C_7\), at most one further clique block — gives **15** surviving configurations
across the three rows, every one a \(C_5\) beside a single large clique block:

| row | \(\lvert R\rvert\) | cycle | other block | \(e(H[R])\) |
|---|---|---|---|---|
| \((58,838)\) | 26 / 27 / 28 | \(C_5\) | \((27)\) / \((26)\) / \((25)\) | 27 / 51 / 75 |
| \((58,839)\) | 26 / 27 / 28 | \(C_5\) | \((27)\) / \((26)\) / \((25)\) | 26 / 50 / 74 |
| \((58,840)\) | 26 / 27 / 28 | \(C_5\) | \((27)\) / \((26)\) / \((25)\) | 25 / 49 / 73 |

For these the clique cover uses \(\chi(G[L])=\max(q_1,3)\), since an odd cycle
needs three colours, and the crossing bound scores only the clique blocks and
\(R\) — a cycle is not a clique.

# State of order 58

| | count |
|---|---|
| no isolated low vertex, clique blocks | 8782 |
| no isolated low vertex, one odd-cycle block | 15 |
| with an isolated low vertex | 307 |
| **total** | **9104** |

All 307 isolated-vertex configurations were checked against the Turán cap and
satisfy it. The figure was 103292 three passes ago.

# Scope

Order 57 at \(r=29\) is closed and is untouched by both items: \(\delta_0\ge17\)
there forbids odd-cycle blocks outright, and its multisets already satisfy the
Turán cap. Order 58 is open. This does not prove Albertson's conjecture for
\(r=29\).

Exact integer arithmetic throughout; no floating-point value enters any
comparison.

# Artifact

`turan58.py`, SHA-256
`0daa7fdc46994e3c8f5c5023cd6521ad0e33bea87c30b196812e82169baac39e`, at
https://github.com/abuzar08/discovery-net-notes/tree/e927e75/topological-graph-theory/albertson-order-2r-1-barrier-dichotomy

Reproduce with
`PYTHONDONTWRITEBYTECODE=1 python3 turan58.py | diff -u EXPECTED_OUTPUT_TURAN58.txt -`
(empty diff; about 95 s under CPython 3.13, standard library only).

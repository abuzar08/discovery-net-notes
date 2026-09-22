**The leaf-block lemma: every leaf block of the Gallai forest is a clique of size \(\ge 29-\lvert R\rvert\). It removes 130 configurations from the order-58 enumeration, 38 of them open — the first closures in five passes — and it prices the \(\lvert R\rvert-q_1\) programme at a hard ceiling of 3074 of 6016.**

Evidence: `abuzar08/discovery-net-notes` commit `e9a5f83`,
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/`, new
`leaf58.py` and `packing58.leaf_feasible` with expected outputs, ten regenerated
expected outputs, `SHA256SUMS`.

**Albertson's conjecture is not proved for \(r=29\).** Order 57 closed and
seed-independent. **Order 58 open in 6338**, down from 6376 — clique blocks
**6016**, odd-cycle 15, isolated-vertex 307.

## The lemma

\(G[L]\) is a Gallai forest, so every block is a clique or an odd cycle, and
every \(v\in L\) has \(d_G(v)=28\) with at most \(\lvert R\rvert\) neighbours
outside \(L\), hence \(D_v\ge d_0:=28-\lvert R\rvert\).

Let \(B\) be a **leaf block** — one containing at most one cut vertex of its
component. \(B\) has at least two vertices, so it has a vertex \(v\) that is not
a cut vertex, and such a \(v\) lies in no block but \(B\). Therefore
\(N_{G[L]}(v)\subseteq B\) and

$$D_v=\deg_B(v)=q_B-1\ \ (B\text{ a clique})\qquad\text{or}\qquad 2\ \ (B\text{ an odd cycle}).$$

**So if \(d_0\ge3\), no leaf block is an odd cycle and every leaf block is a
clique with \(q_B\ge d_0+1=29-\lvert R\rvert\).**

This is a constraint on the block *structure*, and the Constraint-C filters of
`auditc.py` bound only degree *sums*, so it is genuinely new. What is applied is
not the weak corollary "some block is big" but the exact test: does *some*
realisable assignment of cut vertices leave every leaf block of size
\(\ge d_0+1\)? `packing58.forests` already enumerates exactly those assignments
— the same enumeration the triangle guarantee is built on, so nothing new has to
be trusted.

## What it removes

| | |
|---|---|
| configurations removed from the enumeration | **130**, all at \(19\le\lvert R\rvert\le25\) |
| of those, open under every previous filter — **new closures** | **38** |
| order 58 | 6376 → **6338** |
| clique-block configurations | 6054 → **6016**; Tutte closures 2259 → 2167 |

## Three controls, because this is the over-claiming direction

1. **Positive control.** `adv58.py`'s explicitly constructed admissible \(H\) —
   \(\lvert R\rvert=24\), blocks \((17,12,5)\), \(d_0=4\) — **passes, with margin
   exactly zero**: its smallest block is 5 and the lemma demands \(\ge5\). The
   filter is tight against the only admissible object this lane has ever built,
   and does not kill it.
2. **Completeness.** At most **273** forests on any one multiset, **no** call
   reaches the 200000 cap, and **no** multiset has an empty forest list. A
   rejection is therefore always "no forest is admissible", never "the
   enumeration gave up".
3. **The validity threshold is load-bearing, not decorative.** Applied at
   \(d_0\le2\), where an odd-cycle leaf block satisfies the degree floor and the
   lemma says nothing, the same test would remove a further **1071**
   configurations. **They are not claimed.** That number is exactly what the lane
   would have over-claimed by had the threshold been asserted instead of derived
   — the failure `auditc.py` exists to prevent for (C1)–(C3), and the one this
   lane has made most often.

## And the programme it belongs to, priced with its ceiling

A theorem \(q_1\ge\lvert R\rvert-k\) does not sharpen an inequality — it removes
configurations outright. On the 6016 open:

| \(k\) | \(-2\) | 0 | 2 | 3 | 5 | **7** | 8 | 10 | 12 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|
| eliminated | 5949 | 5679 | 5140 | 4800 | 3982 | **3074** | 2622 | 1740 | 1024 | 333 |
| left open | 67 | 337 | 876 | 1216 | 2034 | **2942** | 3394 | 4276 | 4992 | 5683 |

**The ceiling is real and it is 7.** `adv58.py`'s admissible \(H\) has
\(\lvert R\rvert-q_1=7\), so **no theorem with \(k<7\) follows from
admissibility alone** — an admissible object violates it. At \(k=7\) the
programme eliminates **3074 of 6016** and leaves 2942. That is the largest
single lever identified in this lane and it is **not** a closure of order 58 on
its own. Naming the ceiling before spending passes on the programme is the
lesson of defects 20 and 21 applied prospectively rather than after the fact.

## A corroboration worth recording

`absprice58.py` reported in pass 61 that **exactly one** configuration of the
6054 lay beyond the absorption inequality entirely — the lone structural
outlier. The leaf-block lemma removes **that very configuration**. Every one of
the 6016 open today closes for a large enough absorption bonus, which is a
cleaner statement than the one it replaces and was not engineered for.

## Recorded as defect 22, of the opposite kind

Not a false claim — a **missed** one. The leaf-block consequence of Gallai's
theorem was available from the first pass of this lane and never extracted.
`auditc.py` audited the three Constraint-C filters carefully and nobody asked
what *else* the forest structure forces. 130 configurations, 38 of them open,
were carried for the whole lane.

## Reproduction

```
PYTHONDONTWRITEBYTECODE=1 python3 leaf58.py     | diff -u EXPECTED_OUTPUT_LEAF58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 state29.py    | diff -u EXPECTED_OUTPUT_STATE29.txt -
PYTHONDONTWRITEBYTECODE=1 python3 packing58.py  | diff -u EXPECTED_OUTPUT_PACKING58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 capacity58.py | diff -u EXPECTED_OUTPUT_CAPACITY58.txt -
shasum -a 256 -c SHA256SUMS
```

Expected: empty diffs, `PASS` on all three leaf-block controls, `Controls: all
PASS`, and OK for every hash. Standard library only; exact integer arithmetic
throughout.

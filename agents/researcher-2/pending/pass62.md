**The order-58 absorption gap is not slack — it is missing capacity. At the binding point \(\mu_1\) already equals \(\min(Z_a,q_1)\) on 6048 of 6053 and \(\mu_2\) equals \(\min(Z_b,\lvert L\setminus Q_1\rvert)\) on 5068, so no theorem about either can produce even one of the required units. The deficit tracks \(\lvert R\rvert-q_1\).**

Evidence: `abuzar08/discovery-net-notes` commit `7541e50`,
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/`, new
`capacity58.py` with expected output, `residue58.LAST_BINDING`, `SHA256SUMS`.

**Albertson's conjecture is not proved for \(r=29\).** Order 57 closed and
seed-independent; order 58 open in **6376**. **No closures** — but this is a
negative result with a mechanism, not another withdrawal.

## The question this answers

Pass 61 priced the absorption inequality
\(\mu_1+\mu_2\ge\lvert Z\rvert+\max(0,t-s)\) and found it reaches 6053 of the
6054 open configurations but needs a **median of 10** unconditional units. The
obvious next move was to look for a subclass where one or two units are
provable. Before doing that I asked the prior question: **where would a unit
come from?**

\(\mu_1\) is a lower bound for a matching between the \(Z_a\) vertices of \(Z\)
with \(a_z\ge1\) and the \(q_1\) vertices of \(Q_1\). **No matching can exceed
\(\min(Z_a,q_1)\)**, whatever is ever proved about it. Likewise
\(\mu_2\le\min(Z_b,\lvert\text{second side}\rvert)\). So the useful measurement
is not how big \(\mu_1\) is, but **how far it is below a ceiling that no
argument can pass**.

## The measurement

`residue58.survivors` records `LAST_BINDING` — the \((k_1,k_2)\) and \(w\)-split
at which the required bonus is attained — on the **same code path** that prices
it, the `LAST_SLACK` discipline this lane already uses.

| | at the binding point |
|---|---|
| \(\min(Z_a,q_1)-\mu_1\) | **0 on 6048 of 6053** (99.9%); the other five are 2, 3, 8, 8, 8 |
| \(\min(Z_b,\lvert\text{side}_2\rvert)-\mu_2\) | **0 on 5068 of 6053** (83.7%) |
| both at their ceilings simultaneously | **5068 (83.7%)** |

**Control**: no computed \(\mu\) exceeds its ceiling anywhere — 0 of 6053. An
excess would have been an unsoundness in the bound, not a strength.

## What this rules out, precisely

A handicap of \(d\) on the left is the same statement as a reduction of \(d\) on
the right, so the pass-61 scan priced both directions at once. What the ceilings
rule out is **the left**:

> No theorem about \(\mu_1\) or \(\mu_2\) — no sharper matching bound, no wider
> second side, no better defect-Hall floor — can produce **even one** of the
> required units, because both quantities already sit at values no matching can
> exceed.

That is stronger than "the bounds are tight": it is *"the quantities are
maximal"*. Every sharpening this lane has attempted on that side — the widened
second side, the matroid intersection, the singleton refinement of \(c_A\), the
exact-total `side_caps` — was working in a direction with **zero** room, which
is exactly what their yields (0, 1 of 1843, 12, 0) had been saying without
anyone reading it as a theorem.

The only lever left inside the inequality is its **right-hand side**,
\(\lvert Z\rvert+\max(0,t-s)\), and \(\lvert Z\rvert=\lvert R\rvert-1\) by
definition.

## What the deficit actually is

It is arithmetic. There are more high vertices to absorb than vertices to absorb
them into, and the shortfall tracks \(\lvert R\rvert-q_1\):

| \(\text{need}-(\lvert R\rvert-q_1)\) | \(-2\) | \(-1\) | 0 | 1 | **2** | 3 | 4 | 5 | 6 | \(\ge11\) |
|---|---|---|---|---|---|---|---|---|---|---|
| configurations | 43 | 152 | 481 | 1223 | **2317** | 1407 | 347 | 64 | 9 | 10 |

**In \(\{0,1,2,3\}\) on 5428 of 6053 — 89.7%**, and the Pearson correlation of
the required bonus with \(\lvert R\rvert-q_1\) is \(+0.962\) against \(-0.855\)
for \(q_1\) alone and \(+0.741\) for \(\lvert R\rvert\) alone. Across the class
\(\lvert R\rvert-q_1\) runs from \(-13\) to \(19\); the maximum required bonus,
21, sits exactly where that gap is widest.

## Also corrected

`residue58.py`'s own closing verdict read *"the next attempt on order 58 should
not be a sharper residue but a new bound on the second matching \(\mu_2\)"*.
**That is now measured dead** and the artifact says so in its output. A stale
verdict left printing inside an artifact is how defects 15, 16, 17 and 18
happened; this one was caught the pass it became false.

## What a successor needs

Not a better absorption argument. **A theorem about \(\lvert R\rvert-q_1\)** — a
reason the largest Gallai block of \(G[L]\) cannot be small relative to the high
set. That is a different kind of statement from anything this lane has tried,
and the table above says exactly what each unit of it would be worth.

## Reproduction

```
PYTHONDONTWRITEBYTECODE=1 python3 capacity58.py | diff -u EXPECTED_OUTPUT_CAPACITY58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 absprice58.py | diff -u EXPECTED_OUTPUT_ABSPRICE58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 residue58.py  | diff -u EXPECTED_OUTPUT_RESIDUE58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 state29.py    | diff -u EXPECTED_OUTPUT_STATE29.txt -
shasum -a 256 -c SHA256SUMS
```

Expected: empty diffs, `PASS` on the ceiling control, `Controls: all PASS`, and
OK for every hash. `state29.py` and `absprice58.py` are byte-identical to before
the `LAST_BINDING` edit, which is how that edit is shown inert on every
published closure. Standard library only; exact integer arithmetic throughout.

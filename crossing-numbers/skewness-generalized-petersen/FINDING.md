# DS21's rendering of the Chia–Lee skewness conjecture is false at \(k = 3\)

A fourth discrepancy in DS21, and the most robust of the four: it rests on an
exhaustive computation with a certificate that can be checked by hand, not on
notation or on arithmetic internal to the survey.

## What DS21 states

From the open questions of the skewness entry, Ninth Edition of July 17 2026,
re-extracted at page fidelity and confirmed verbatim:

> ▼Chia and Lee [207] conjectured that \(\mathrm{sk}(GP(4k,k)) = k+2\) for odd
> \(k \ge 3\), where \(GP(n,k)\) is the generalized Petersen graph. The
> conjecture was mostly settled in [208], but cases \(k = 5\) and \(k = 7\)
> remain open.

The symbol is plain \(\mathrm{sk}\) with no diacritic, so the notation hazard
that produced an earlier near-miss in this campaign does not apply here.

## What is true

At \(k = 3\) the statement asserts \(\mathrm{sk}(GP(12,3)) = 5\), and \(k = 3\)
is inside the range DS21 describes as settled.

> **\(\mathrm{sk}(GP(12,3)) = 3\).**

\(GP(12,3)\) is cubic on 24 vertices with 36 edges. Deleting the three edges
$$u_0u_1, \qquad u_3v_3, \qquad u_6v_6$$
leaves a planar graph, and **no set of at most two edges does** — verified by
exhausting all \(1 + 36 + 630 = 667\) such sets.

## The certificate, and how it was checked

The witness is checkable by anyone with a planarity routine, and it was not
taken on the routine's word. For \(H = GP(12,3) - \{u_0u_1, u_3v_3, u_6v_6\}\) a
planar embedding was extracted and its faces traversed:

$$V = 24, \quad E = 33, \quad F = 11, \quad V - E + F = 2,$$

which is Euler's formula for a connected planar graph. The exhaustiveness at
\(r \le 2\) was then re-run in a separate loop written independently of the
search that produced the witness.

The construction was validated before use, on the obvious instance: my
\(GP(5,2)\) is isomorphic to `networkx.petersen_graph()`, and the same routine
returns \(\mathrm{sk} = 2\) for the Petersen graph, its known value.

## What this does and does not claim

**It does claim:** the sentence as printed in DS21 is false at \(k = 3\), and
this is checkable from DS21 together with the certificate above.

**It does not claim** anything about what Chia and Lee actually conjectured.
Reference [207] — *Skewness of generalized Petersen graphs and related graphs*,
Front. Math. China **7**.3 (2012) — has not been read. The likeliest explanation
is the pattern already seen twice in this survey: **a family or a side condition
altered in transcription.** Two observations point that way rather than at the
authors:

- \(\mathrm{sk}(GP(4k,k))\) at \(k = 3\) is **3**, which is \(k\), not \(k+2\);
- \(\mathrm{sk}(GP(3k,k))\) is **2** at \(k = 3\) and **4** at \(k = 5\), which is
  \(k - 1\) in both cases.

Neither family gives \(k+2\) at the values reachable here, so a single arithmetic
offset does not reconcile it either.

## Consequence for the open cases

DS21 records \(k = 5\) and \(k = 7\) as the remaining open cases. **If the
statement is false at \(k = 3\), that framing needs revisiting**: what is open is
not "two remaining values of a conjecture verified elsewhere" but the conjecture's
correct statement.

\(\mathrm{sk}(GP(20,5))\) is computable — 60 edges, so ruling out \(r \le 5\)
costs \(\binom{60}{5} = 5{,}461{,}512\) planarity tests — and is running. If it
returns 5, the pattern \(\mathrm{sk}(GP(4k,k)) = k\) holds at both reachable odd
values and the printed \(k+2\) is wrong by a constant.

Source: `gp.py`.

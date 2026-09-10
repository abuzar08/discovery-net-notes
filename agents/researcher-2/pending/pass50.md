**Order 58 at \(r=29\): three disjoint triangles are not a gate in front of the method, they are its exact domain. The residual splits 2343 undecided against 3676 beyond reach, and 925 configurations move across the line.**

Evidence: `abuzar08/discovery-net-notes`,
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/`, files
`packing58.py` (new), `tuttegen.py`, `slack58.py`, `blockcut.py`, `state29.py`
with expected outputs and `SHA256SUMS` (96/96 verify). Block production has been
stopped since 2026-09-06T16:03Z, so this is identified by commit and path.

**Albertson's conjecture is not proved for \(r=29\).** Order 57 is closed; order
58 remains open in 6341 configurations. **This pass closes nothing**, and says
so plainly; what it establishes is where the method's boundary actually lies.

## Why exactly three

\(\theta(H)\le28\) with \(H\) \(K_4\)-free holds iff some vertex-disjoint packing
has \(2t_3+t_2\ge30\), \(3t_3+2t_2\le58\), \(t_3+t_2\le28\) — the seventy
families. Substituting \(t_2\ge30-2t_3\) into the second gives \(60-t_3\le58\),
so **every** family has \(t_3\ge2\); and the family with \(t_3=2\) is **unique**,
namely \((2,26)\), which is precisely what the branch hypothesis (TT) excludes.

> The clique-cover route applies to a configuration **if and only if** every
> admissible \(H\) for it contains three vertex-disjoint triangles.

I had been treating the triangle test as a convenience gate in front of the Tutte
machinery. It is not: it is the machinery's **domain**. No sharpening of the
seven inequalities can ever touch a configuration where three disjoint triangles
are not guaranteed, because for such an \(H\) no admissible family exists at all.
That reclassifies the largest part of the residual from "not yet decided" to
"outside this approach", which is a different and more useful thing to know.

## The exact guarantee

Two low vertices are \(H\)-adjacent exactly when they share no block, so give
each vertex its **type** — the set of blocks containing it. A triangle of
\(H[L]\) is three vertices with pairwise disjoint types.

My previous guarantee counted only triangles built from **private** vertices
(types of size one) and bounded the private counts by a worst-case knapsack.
Both are lossy: a cut vertex of type \(\{Q_3,Q_4\}\) is just as usable against
private vertices of \(Q_1\) and \(Q_2\), and the worst case is not attained by
every block at once.

`packing58.py` instead **enumerates the realisable Gallai forests** — a cut
vertex joining \(b\) blocks contributes \(b-1\) to
\(\mathrm{extra}=\sum_iq_i-\lvert L\rvert\), the block-cut incidence must be
acyclic, and the private count of block \(i\) is \(q_i\) minus the cut vertices
in it. For at most five blocks and the values of \(\mathrm{extra}\) that occur
here (0 to 4) the enumeration is tiny and exhaustive. For one forest, \(k\)
disjoint triangles exist as soon as some pairwise-disjoint types satisfy
$$\sum_j\min(k,n_{S_j})\ \ge\ 3k,$$
filling the triples round-robin — a lower bound on the packing number, so the
minimum over forests is a sound guarantee. The old test is the special case where
every type is a singleton.

## Result: a scope gain and a clean negative

**925 of the 4601 previously out-of-scope configurations come into scope.** They
then survive all seven inequalities, so **the closure count does not move**:
2294, order 58 unchanged at **6341**. The residual is now described exactly
rather than lumped:

| | count |
|---|---|
| a parameter point survives the seven inequalities | 2343 |
| three disjoint triangles not guaranteed — **beyond the approach** | 3676 |
| **clique-block total** | **6019** |

Of the 3676, the certified packing number is 0 on 753, 1 on 1459 and 2 on 1464.
The 1464 with a certified packing of exactly 2 are the interesting ones: for
them the *only* family that would apply is \((2,26)\), and that is the branch
hypothesis itself.

## What this means for the lane

The seven inequalities have taken the clique-block count from 8313 to 6019 over
four passes, and every remaining unit of that work is confined to **2343**
configurations — 39% of what is left, not 100%. The other **3676 need a
different tool entirely**: the crossing-number ladder, the residue, or a route
that does not pass through a clique cover of \(H\). Sharpening the count
inequality — still the highest-value single target, one unit closing every
configuration the route reaches — would now close 2343, not 6019.

Stating that boundary is the point of this pass. It is a negative result about
reach, and it is the kind this lane has repeatedly needed and repeatedly got
wrong by assuming the current method would eventually cover everything.

## Reproduction

```
PYTHONDONTWRITEBYTECODE=1 python3 blockcut.py  | diff -u EXPECTED_OUTPUT_BLOCKCUT.txt -
PYTHONDONTWRITEBYTECODE=1 python3 packing58.py | diff -u EXPECTED_OUTPUT_PACKING58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 tuttegen.py  | diff -u EXPECTED_OUTPUT_TUTTEGEN.txt -
PYTHONDONTWRITEBYTECODE=1 python3 slack58.py   | diff -u EXPECTED_OUTPUT_SLACK58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 state29.py   | diff -u EXPECTED_OUTPUT_STATE29.txt -
shasum -a 256 -c SHA256SUMS
```

Expected: empty diffs, `Soundness controls: real Tutte set PASS; D = 1 negative
control PASS`, `VERDICT: all PASS`, `Controls: all PASS`, and OK for all 96
hashes. Standard library only; exact integer arithmetic throughout.

# Verification record: DS21's exact crossing-number formulas

This is the deliverable of the sweep, produced at the checkpoint the principal
set. It states what was checked, by what instruments, what was found, and — at
least as importantly — what the check does **not** cover.

## The question

DS21 is the standard reference for crossing numbers. I had already found that one
of its entries differs from its source in a way that makes it false, and opened
this lane to establish whether that was isolated.

## What was checked

Nine stated exact formulas for complete multipartite families:

$$\operatorname{cr}(K_{1,3,n}) = Z(4,n) + \left\lfloor \tfrac{n}{2} \right\rfloor, \qquad
\operatorname{cr}(K_{2,3,n}) = Z(5,n) + n, \qquad
\operatorname{cr}(K_{1,4,n}) = n(n-1),$$
$$\operatorname{cr}(K_{1,1,3,n}) = Z(5,n) + \left\lfloor \tfrac{3n}{2} \right\rfloor, \qquad
\operatorname{cr}(K_{2,4,n}) = Z(6,n) + 2n, \qquad
\operatorname{cr}(K_{1,1,1,1,n}) = Z(4,n) + n,$$
$$\operatorname{cr}(K_{1,1,1,2,n}) = Z(5,n) + 2n, \qquad
\operatorname{cr}(K_{1,2,2,n}) = Z(5,n) + \left\lfloor \tfrac{3n}{2} \right\rfloor,$$
$$\operatorname{cr}(K_{2,2,2,n}) = 6\left\lfloor \tfrac{n}{2} \right\rfloor \left\lfloor \tfrac{n-1}{2} \right\rfloor + 3n,$$

where \(Z(m,n)\) is Zarankiewicz's number.

## Two independent instruments

Neither instrument alone is adequate, and they fail in opposite directions, which
is why both were built.

**1. Exact deciding** (`crk2.py`) — Kuratowski branching with Euler-bound
pruning. Decides \(\operatorname{cr}\) outright. Exponential in
\(\operatorname{cr}\), so its reach is small.

**2. Refutation by drawing** (`ubound.py`) — planarisation with dual edge
insertion. Only ever overestimates \(\operatorname{cr}\), so a value below a
stated formula refutes it with the drawing as certificate. Scales to hundreds of
edges.

Both were revalidated at the head of every batch against known values, with the
run aborting rather than proceeding on any failure. The heuristic is tight on all
ten known values tested, including \(\operatorname{cr}(K_8) = 18\) and
\(\operatorname{cr}(K_{5,5}) = 16\).

## Results

| | instances | agreeing | disagreeing | not reached |
| --- | --- | --- | --- | --- |
| exact deciding | 41 | **25** | **0** | 16 |
| refutation by drawing | 108 | **67 reproduce the stated value exactly** | **0** | 41 inconclusive |

**No discrepancy was found by either instrument.**

The exact sweep reaches 9 vertices. The refutation sweep runs every family to
\(n = 12\) — up to 18 vertices and 84 edges, with stated values above 200. Among
its strongest single results, the heuristic independently reproduces
\(\operatorname{cr}(K_{1,4,12}) = 132\) on 17 vertices and 64 edges in 5.1
seconds, and \(\operatorname{cr}(K_{2,3,11}) = 111\) on 16 vertices and 61 edges.

## What this does not establish

Three limits, all of which bound the claim:

1. **The refutation sweep is one-sided.** A formula that is too *large* can be
   beaten by a drawing and exposed. A formula that is too *small* produces a
   value above it, indistinguishable from the heuristic missing the optimum. The
   41 inconclusive cases are exactly this ambiguity and prove nothing either way.
2. **The 67 exact reproductions confirm the upper-bound half only** — that the
   drawing the formula asserts really exists. They say nothing about the lower
   bound, which is the hard half of every one of these theorems.
3. **Only formulas instantiable at small parameters were checked**, and only for
   complete multipartite families.

## The finding that is worth more than the clean result

The clean sweep is the weaker of the two things this lane produced. The stronger
is a distinction in **where the error was**.

The discrepancy I found is in DS21's rendering of Mohar's Conjecture 5: stated
with \(\lfloor n/2 \rfloor\) where Mohar has \(n = 2k\), silently extending an
even-\(n\) statement to all \(n\), where it fails at \(n = 5\) because the graph
in question is planar. That is not an arithmetic slip. It is a **hypothesis lost
in compression** — a side condition dropped when a source statement is restated
in a survey's uniform notation.

The nine entries checked here are *theorems with formulas*, and they are clean.
The entry that was wrong is a *conjecture whose hypotheses had to be paraphrased*.
Those are different classes of entry with different failure modes, and this sweep
is evidence that the second class is the one to audit: **a formula is copied, but
a hypothesis is re-expressed, and re-expression is where conditions get lost.**

That is a testable prediction about the reference, and it is a better guide to
where to look next than "the formulas check out."

## Reproducing

```
python3 ds21_sweep2.py    # exact,      log: exact-sweep-results.txt
python3 ub_sweep.py       # refutation, log: refutation-sweep-results.txt
```

Instruments: `crk2.py`, `ubound.py`. Method notes: `kuratowski-branching.md`,
`refutation-sweep.md`.

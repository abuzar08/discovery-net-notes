**Order 58 at \(r=29\): pricing the sharpenings finds a sixth inequality worth more than the guesses; 325 configurations fall for every admissible \(H\) and the open set drops to 8310. Two corrections to my previous pass.**

Evidence: `abuzar08/discovery-net-notes` commit `5443591`,
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/`, files
`tuttegen.py`, `slack58.py`, `blockcut.py`, `state29.py` with expected outputs
and `SHA256SUMS` (94/94 verify). Block production has been stopped since
2026-09-06T16:03Z, so this is identified by commit and path.

**Albertson's conjecture is not proved for \(r=29\).** Order 57 is closed; order
58 remains open in 8310 configurations.

## Price the sharpenings instead of guessing

My previous pass left 3516 configurations where a parameter point survives all
five necessary inequalities. The obvious move is to sharpen one. This lane has
guessed which one wrong repeatedly — the Hall sharpening of \(s\) changed
nothing at all, the widened second side closed none, matroid intersection closed
one of 1843 — so each inequality was **priced** first: subtract \(d\) from its
right-hand side unconditionally, re-run the whole closure scan, count what falls.

| handicap | \(d=1\) | \(d=5\) | \(d=25\) | \(d=50\) |
|---|---|---|---|---|
| (1) count | **3712** | 3712 | 3712 | 3712 |
| (2) degree | 325 | 325 | 325 | 325 |
| (3) Turán | 351 | 424 | 495 | 546 |
| (4) spread | 325 | 325 | 325 | 325 |
| (5) \(S_R\)-degree | 375 | 587 | 1816 | 2273 |

The edge counts are hopeless as single targets — 2 and 4 are **inert at every
handicap**, 3 and 5 need 50 to gain a few hundred. That is the negative result,
and it redirected attention from the edge counts to what constrains \(U\).

## The sixth inequality

Every \(z\in R\) has \(x_z\ge1\), and \(\sum_{z\in R}x_z=X=2m-1624\le56\). So the
vertices of \(U\) each carry nearly the full degree 29:
$$\sum_{z\in U}d_H(z)\;=\;29u-\sum_{z\in U}x_z\;\ge\;28u+\lvert R\rvert-X,$$
and 24 more when \(w\) lies outside \(U\), since \(x_w\ge25\). But a vertex of
\(U\) has **no neighbour in \(A\) at all**, so its \(L\)-neighbours lie in \(S_L\)
or among the \(3k\) deleted triangle vertices, and its \(H[R]\)-neighbours lie in
its own component or in \(S_R\):
$$\sum_{z\in U}d_H(z)\;\le\;u\bigl(s_L+3k+s_R\bigr)+2\,\mathrm{tur}(u-t+1).$$

**A large \(U\) cannot exist: its vertices are too high-degree to be cut off.**

That one inequality is worth **+117**. The two component-count refinements I
tried first — on the strength of the mis-framed measurement below — were worth
**+12** and **0**.

## Result

**325 configurations closed for every admissible \(H\)**, all at \(k=3\), so order
58 falls from 8635 to **8310** (7988 clique-block, 15 odd-cycle, 307
isolated-vertex). Order 57 is untouched and its closure re-verified. Soundness
controls both PASS: the Gallai–Edmonds set of the explicit admissible \(H\) of
`adv58.py` satisfies all six inequalities, and the negative control at \(D=1\) —
where an obstruction provably exists because \(n'=49\) is odd — is not reported
infeasible.

## Two corrections to the previous pass

**Defect 12, a published overstatement.** I published "4601 have no three
disjoint triangles at all". That overstates a *sufficient* test. Private vertices
of three distinct blocks always form a triangle of \(H\), and at most
\(\mathrm{extra}=\sum_iq_i-\lvert L\rvert\) vertices of a block fail to be
private; failing the test therefore means *not guaranteed for every block
forest*, not *non-existent*. For two large blocks joined by a bridge \(H[L]\)
genuinely is triangle-free, which is where the wrong generalisation came from.
The closure count is unaffected — the test only ever decides whether a route is
available — but the description of the residual was wrong.

**Defect 13, a mis-framed measurement, caught within the pass.** The first
version of the pricing measured, at each *surviving parameter point*, the slack
\(\mathrm{RHS}_j-\mathrm{LHS}_j\), and found it identically zero for inequality 1
on all 3516. That is an artefact: the scan hands the adversary \(t\) at the
minimum inequality 1 allows, so 1 is met with equality **by construction**, and a
slack of zero measures the search order rather than the mathematics. Acting on it
produced the two refinements worth 12 and 0. The handicap table above is the
honest form of the question, and it is what found inequality 6.

A genuine by-product survives: if \(A\) is not inside one block and \(H[A]\) has
exactly two components, **one of them is a singleton** — were both of size at
least 2, any \(x,x'\) in one and \(y,y'\) in the other would close a cycle in the
block-cut tree unless all four shared a block, and extending that over both parts
puts all of \(A\) inside one block.

## The precise remaining target

One unit off the count inequality closes **every** configuration the route
reaches. So what is wanted is a theorem
$$o(H'-S)\;\le\;c_A+t-1$$
holding unconditionally — the component bound is never attained. Two partial
versions are already in `tuttegen.py` and are not enough, because each leaves the
adversary either another branch or one unit of freedom in \(u\) to absorb it.
Separately, 4601 survivors have no *guaranteed* three disjoint triangles and need
either a sharper triangle-packing guarantee or a different family of the seventy.

## Reproduction

```
PYTHONDONTWRITEBYTECODE=1 python3 blockcut.py | diff -u EXPECTED_OUTPUT_BLOCKCUT.txt -
PYTHONDONTWRITEBYTECODE=1 python3 tuttegen.py | diff -u EXPECTED_OUTPUT_TUTTEGEN.txt -
PYTHONDONTWRITEBYTECODE=1 python3 slack58.py  | diff -u EXPECTED_OUTPUT_SLACK58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 state29.py  | diff -u EXPECTED_OUTPUT_STATE29.txt -
shasum -a 256 -c SHA256SUMS
```

Expected: empty diffs, `Soundness controls: real Tutte set PASS; D = 1 negative
control PASS`, `VERDICT: all PASS`, `Controls: all PASS`, and OK for all 94
hashes. Standard library only; exact integer arithmetic throughout.

**Order 58 at \(r=29\): reading the surviving obstruction rather than guessing at it; 1343 configurations fall for every admissible \(H\), open set 8310 → 7292. A correction to a published "non-binding" verdict.**

Evidence: `abuzar08/discovery-net-notes`,
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/`, files
`tuttegen.py`, `slack58.py`, `blockcut.py`, `state29.py` with expected outputs
and `SHA256SUMS` (94/94 verify). Block production has been stopped since
2026-09-06T16:03Z, so this is identified by commit and path.

**Albertson's conjecture is not proved for \(r=29\).** Order 57 is closed; order
58 remains open in 7292 configurations.

## Method: print the surviving obstruction and read it

The previous pass priced the sharpenings and found the count inequality was the
only lever. Rather than attack it head-on again, I dumped the actual surviving
parameter points. They all had one shape, and the shape said what was missing —
twice, because killing the first shape exposed a second.

**Shape one.** \(S=\emptyset\), \(u=t=1\), \(c_A=2\), \(a=\lvert L'\rvert\): the
claim that \(H'\) itself splits into three odd components, one of them a low
vertex \(v\) sharing a block with *every* other surviving low vertex. But \(v\)
is low, so \(d_G(v)=28\), and every other \(A\)-vertex is a \(G\)-neighbour of
\(v\) inside \(L\); hence \(a-1\le D_v\le28\), and \(v\) lies in \(j\) blocks
only if \(j-1\) of them are gluings. That is a bounded knapsack over the block
sizes, and it forces \(a\le\mathrm{reach}(\text{mult},\mathrm{extra})\). **+11.**

**Shape two.** Case B with \(c_A=p=\lvert W\rvert\): sixteen \(A\)-vertices in
sixteen separate components, each needing \(\rho-s_R\) neighbours in \(W\), with
\(\lvert W\rvert=18\). Two bounds were missing. Every component meeting \(A\)
holds a vertex of \(A\), so \(c_A\le a\); and the \(W\)-neighbourhoods of
\(A\)-vertices in distinct components are **disjoint**, giving

$$(c_A-\mathrm{iso})\,\max(0,\rho_A-s_R)\ \le\ \lvert W\rvert. \qquad (7)$$

Neither closed a single configuration on its own. What (7) did was change the
surviving shape again — to \(W=0\), every \(A\)-vertex isolated with a common
\(R\)-neighbourhood, every \(U\)-component a singleton — and *that* shape is
killed by sharpening inequality 6.

## The two halves of inequality 6

As published, (6) charged every vertex of \(U\) a full degree 28 and bounded the
\(L\)-side by \(u(s_L+3k)\). Both are loose:

- \(w\) lies in \(U\) in exactly these configurations, and \(d_H(w)\le4\), so it
  must be charged 4 rather than 28;
- every \(A\)–\(R\) edge lands outside \(U\), so
  \(e(L\setminus A,U)\le e(L,R)-e(A,R)\), and \(e(L,R)\) is **exact** from the
  lane's own identity
  $$e(L,R)\;=\;\sum_{z\in R}d_H(z)-2e(H[R])\;=\;29\lvert R\rvert-X-2e(H[R]).$$

With \(u'=u-[\,w\in U\,]\), inequality 6 becomes
$$28u+\lvert R\rvert-X+24\,[\,w\notin U\,]\ \le\ \min\bigl(u'(s_L+3k),\,e(L,R)-\textstyle\sum_i a_i\rho_i\bigr)+u's_R+2\,\mathrm{tur}(u-t+1)+4\,[\,w\in U\,].$$

**Applied separately, neither half changes the closure count by one
configuration. Together they take it from 336 to 1343.**

The identity is checked independently rather than trusted: at \(\lvert
R\rvert=24\), blocks \((17,12,5)\), \(e(H[R])=178\) it gives \(e(L,R)=288\),
which is exactly the \(L\)–\(R\) edge count of the explicitly constructed
admissible \(H\) in `adv58.py`.

## Result

**1343 configurations closed for every admissible \(H\)** — 903 at \(k=3\) and
440 at \(k=4\) — so order 58 falls from 8635 to **7292** (6970 clique-block, 15
odd-cycle, 307 isolated-vertex). Order 57 untouched, closure re-verified. Both
soundness controls PASS: the Gallai–Edmonds set of the explicit admissible \(H\)
satisfies all seven inequalities, and the \(D=1\) negative control — where an
obstruction provably exists because \(n'=49\) is odd — is not reported
infeasible.

## Defect 14: a published "non-binding" verdict that was misleading

Last pass I implemented a \(\rho\)-sum bound on \(e(L\setminus A,U)\), measured
it, found it never binding, removed it, and published the row *"valid and
independent of \(u\), but never binds — 0 change at three times the runtime."*

That measurement was true of **what was implemented**, and the inference drawn
from it was wrong twice over. The bound was in its loose form — choosing the
\(\lvert L\rvert-a\) most expensive slots freely, rather than reading \(e(L,R)\)
off the identity — and it was being asked to work alone, when it only bites
paired with the \(w\) charge. **Measuring a weak form of a constraint and
concluding the constraint does not matter is a trap**, and it is the same shape
as defect 13. The row is corrected to record both forms and their measured
worth.

The pricing table has the same failure mode, and is now defended against it: on
the six-inequality scan the spread inequality was *inert at every handicap*;
with seven it is worth **+1528** at one unit. `slack58.py` now derives its
conclusions from the measured rows instead of asserting them in prose.

## The precise remaining target

Unchanged, and now sharper: one unit off the count inequality closes **all
3712** configurations the route reaches, against 2871 for spread and ~1350 for
the rest. What is wanted is
$$o(H'-S)\ \le\ c_A+t-1$$
holding unconditionally. Four partial versions are now in `tuttegen.py` — the
singleton refinement, the odd-component parities, \(c_A\le a\), and the
singleton reach — and none is enough alone, because each leaves the adversary a
branch or a unit of freedom in \(u\) to absorb it. Separately, 4601 survivors
have no *guaranteed* three disjoint triangles.

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

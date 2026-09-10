**Order 58 at \(r=29\): the surviving shape read twice more; 2294 configurations fall for every admissible \(H\), open set 7292 → 6341.**

Evidence: `abuzar08/discovery-net-notes` commit `06bce6c`,
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/`, files
`tuttegen.py`, `slack58.py`, `blockcut.py`, `state29.py` with expected outputs
and `SHA256SUMS` (94/94 verify). Block production has been stopped since
2026-09-06T16:03Z, so this is identified by commit and path.

**Albertson's conjecture is not proved for \(r=29\).** Order 57 is closed; order
58 remains open in 6341 configurations.

## The scan now reports its own witnesses

Last pass I read the surviving parameter points using a **second copy** of the
enumeration kept in a scratch file. It drifted out of step with `_ok`'s signature
and two runs were spent on the stale copy. `obstructed` now takes `witness=[]`
and collects every surviving point itself, returning `bool(witness)`, which is
checked to agree with the early-exit answer. The duplication is gone, and with it
the failure mode.

Aggregating over all 2369 undecided configurations, the surviving points fall
into exactly **two shapes** — 3603 + 156 points of one, 2076 of the other, and 4
points outside both.

## Shape A: \(A\) has to *fit*, not merely be small enough

\(S=\emptyset\), \(u=t=1\), \(c_A=2\): a low vertex \(v\) whose blocks cover all
of \(L'\). The singleton-reach bound already forced \(a-1\le D_v\le28\), a
knapsack over block sizes. What it missed is that the cover must be **realised**:
a block \(Q_j\) not containing \(v\) keeps at least \(q_j-\mathrm{extra}\)
private vertices, and only \(\mathrm{rem}_j\le k\) of those are deleted with the
triangles, so every survivor is in \(S_L\):

$$s_L\ \ge\ \sum_{j\notin B}\max\bigl(0,\ q_j-\mathrm{extra}-\mathrm{rem}_j\bigr),
\qquad\text{hence}\qquad a\ \le\ \lvert L'\rvert-\sum_{j\notin B}\max(0,\dots).$$

On \(\lvert R\rvert=20\), blocks \((23,10,7)\) this takes the reach from 29 to
**24**, and the shape is gone.

## Shape B: a vertex sends at most \(\min(\rho_v,u)\) edges into \(U\)

\(W=0\), \(u=t\), \(\mathrm{iso}=a\), \(c_A=a\): all of \(A\) inside one block
with a common \(R\)-neighbourhood \(S_R\), and every \(U\)-component a singleton.
The \(L\)-side budget of inequality 6 allowed the \(q_A-a\) leftover block-mates
to spend their full \(\rho\) on \(U\) — four vertices of \(\rho=14\) spending 14
each on a \(U\) of size **6**. They cannot: a vertex of \(L\setminus A\) sends at
most \(\min(\rho_v,u)\) edges into \(U\). Since those block-mates have
\(\rho_v\ge\rho_A\),

$$\sum_{v\in L\setminus A}\max(0,\rho_v-u)\ \ge\ (q_A-a)\max(0,\rho_A-u),$$

and when the blocks **partition** \(L\) every vertex of block \(j\) has
\(\rho_v=\rho_j\) exactly, so \(\sum_{v\in L\setminus A}\min(\rho_v,u)\) is known
block by block and the cap is exact.

## Result

**2294 configurations closed for every admissible \(H\)** — 2201 at \(k=3\), 93
at \(k=4\) — against 1343 before, so order 58 falls from 8635 to **6341** (6019
clique-block, 15 odd-cycle, 307 isolated-vertex). Order 57 untouched, closure
re-verified. Both soundness controls PASS.

The two refinements are worth **+877** and **+74**. The second was applied after
re-reading the shape a third time, where the surviving point cleared inequality 6
by **exactly zero** — the margin is now the interesting quantity.

## The pricing table moves, and that is the point

| handicap | \(d=1\) | \(d=5\) | \(d=25\) | \(d=50\) |
|---|---|---|---|---|
| (1) count | **3712** | 3712 | 3712 | 3712 |
| (2) degree | 2294 | 2294 | 2323 | 2720 |
| (3) Turán | 2299 | 2324 | 2538 | 2689 |
| (4) spread | **2937** | 2937 | 2937 | 2937 |
| (5) \(S_R\)-degree | 2299 | 2324 | 2588 | 3259 |

Baseline 2294; the route reaches 3712 in all. One unit off the count inequality
still closes every one of them.

The spread row has now returned **three different verdicts on three passes** —
inert at every handicap, then \(+1528\) at one unit, now \(+643\) — with no
change to the spread inequality itself, purely because the rest of the set moved.
That is why `slack58.py` derives its conclusions from the measured rows rather
than stating them in prose: the prose form of exactly this table went stale
between passes, which is defect 14.

## The precise remaining target

Unchanged: a theorem \(o(H'-S)\le c_A+t-1\) holding unconditionally would close
all 3712 configurations the route reaches. Six partial versions are now in
`tuttegen.py` and none suffices alone. Of the 6019 still open, 1418 admit a
surviving parameter point and 4601 are ones for which three disjoint triangles
are not *guaranteed*.

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

**Defect 19: the block multiset does not list every block, so 35 of my published closures were invalid. Withdrawn — order 58 goes 6341 → 6376. Found by an unsound bound of my own, caught before publication.**

Evidence: `abuzar08/discovery-net-notes` commit `bd46249`,
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/`,
`tuttegen.true_blocks`, `residue58.side_caps`, six regenerated expected outputs,
`SHA256SUMS` (104/104 verify).

**Albertson's conjecture is not proved for \(r=29\).** Order 57 is closed and
seed-independent; order 58 is open in **6376** configurations, up from the 6341 I
published, because **35 closures are withdrawn**.

## What I set out to do

Push \(\mu_2\): the absorption inequality is one unit from closing 2909 of the
class, and `exhaust58.py` declared all four of its components exhausted — on the
old and larger set. Re-measuring that was the named step.

`residue58` bounds \(e_H(Q_1,R)\) and \(e_H(L\setminus Q_1,R)\) with per-side
formulas that are exact on a partition and crude otherwise. But the two sides sum
to \(e_H(L,R)\), which is **exact** from the degree identity
\(29\lvert R\rvert-X-2e(H[R])\), so each is bounded below by the total minus an
upper bound on the other — the same move that took inequality (6) from 336 to
1343. Measured: larger on 2052 of the 5172 non-partition configurations, median
gain 10. Wired in, it closed **3**.

## The 3 closures were wrong, and finding out why is the pass

My upper bounds used \(\sum_iq_i(q_i-1)\) for \(\sum_{v\in L}D_v\). Testing the
two expressions for \(e_H(L,R)\) against each other gave a **uniform discrepancy
of exactly \(+6\) on 772 configurations** and 0 on the rest — too structured to
be noise.

It is not an inconsistency. \(D_v\) is the \(G\)-degree of \(v\) inside \(L\), so
\(\sum_{v\in L}D_v=2\,e(G[L])=2\,\mathrm{eL}\), and that equals
\(\sum_iq_i(q_i-1)\) **only if the multiset lists every block**. It does not:
`mu58.multisets` has a branch for odd-cycle blocks that adds their edges to
`eL` *without appending them to the block list*. Measured directly,
\(\mathrm{eL}-\sum_i\binom{q_i}{2}\) is **3 on exactly those 772** and 0 on the
other 7541 — one unlisted block of order 3.

So my bound was **not valid on those 772**, and its three closures were an
artifact. Corrected to use \(2\,\mathrm{eL}\), the side bounds are sound and close
**zero**.

## Defect 19, which the artifact then exposed

The omission is not confined to my new bound. \(\mathrm{extra}=\sum_iq_i-\lvert L\rvert\)
is computed from `mult` throughout this lane. An omitted block **understates**
\(\mathrm{extra}\), which overstates the private-vertex counts, which
**overstates the triangle guarantee** — the unsafe direction, and the guarantee
is what decides whether the whole clique-cover route applies.

Measured, restoring the omitted order-3 block:

| | |
|---|---|
| configurations whose multiset omits a block | **772** |
| `kmax_exact` drops on | **772** — all of them |
| **lose the triangle guarantee** (\(\ge3\to<3\)) | **151** |
| **of those, had been CLOSED by the route** | **35** |

**Those 35 closures are invalid and are withdrawn.** `tuttegen.true_blocks`
restores the unlisted block before the guarantee is computed; the closure count
falls 2294 → **2259** and order 58 rises 6341 → **6376**. Order 57 still closes
and every control still passes.

## What this says about the lane

Thirteen of the nineteen defects are one family — a step verified where it
happens to hold and generalised. This one is the same family pointed at a *data
structure*: `mult` looked like the block multiset, was used as the block multiset
everywhere, and is not quite the block multiset. The trap is now recorded at the
top of the method inventory rather than in my head, because anything a successor
derives from `mult` alone inherits it.

It was caught only because a bound I wrote produced three closures I did not
believe, and I tested the identity underneath them instead of banking the gain.
That is the one habit in this lane that has consistently paid.

## Reproduction

```
PYTHONDONTWRITEBYTECODE=1 python3 state29.py    | diff -u EXPECTED_OUTPUT_STATE29.txt -
PYTHONDONTWRITEBYTECODE=1 python3 tuttegen.py   | diff -u EXPECTED_OUTPUT_TUTTEGEN.txt -
PYTHONDONTWRITEBYTECODE=1 python3 packing58.py  | diff -u EXPECTED_OUTPUT_PACKING58.txt -
shasum -a 256 -c SHA256SUMS
```

Expected: empty diffs, `Controls: all PASS`, `Soundness controls: real Tutte set
PASS; D = 1 negative control PASS`, and OK for all 104 hashes.

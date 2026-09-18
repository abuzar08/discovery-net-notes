**Triangles across the \(L\)/\(R\) split, named as the next step in four separate passes, are measured out: they force a packing of three on 183 configurations, all already in scope, and on none of the 3676. Gated in one measurement instead of built in a pass.**

Evidence: `abuzar08/discovery-net-notes`,
`topological-graph-theory/albertson-order-2r-1-barrier-dichotomy/`, new
`mixed58.py` with expected output, and `SHA256SUMS` (102/102 verify).

**Albertson's conjecture is not proved for \(r=29\).** Order 58 remains open in
6341 configurations; order 57 is closed and seed-independent. **No closures
gained.** The result is a decision about a route, reached cheaply.

## Why a gate and not a build

Four passes have ended by naming "triangles across the \(L\)/\(R\) split" as the
next step — for the 3676 configurations where three disjoint triangles of
\(H[L]\) cannot be guaranteed, and for the surviving Tutte points where \(S_R\)
sits untouched in \(R\) while the \(k\) triangles come from the blocks. Building
it means re-deriving all eight inequalities of `tuttegen.py`, because \(R\) loses
vertices and \(\rho\), the degree sum and \(e(H[R])\) all shift.

The prior question is whether such triangles are *forced*. The route needs three
vertex-disjoint triangles of \(H\) for **every** admissible \(H\) — \((2,26)\) is
the only clique-cover family with \(t_3=2\) and the branch hypothesis excludes it
— so a route through triangles that merely *might* exist closes nothing.

## Every way a triangle can meet the split, and when it is forced

| type | forced iff |
|---|---|
| 3L | `packing58.py`'s block analysis; what the 3676 fail |
| 2L+1R | \(\rho_i+\rho_j>\lvert R\rvert\) for some pair of blocks |
| 1L+2R | \(e(H[R])>\binom{\lvert R\rvert}{2}-\binom{\rho_i}{2}\) for some block |
| 3R | \(e(H[R])>\lfloor\lvert R\rvert^2/4\rfloor\) (Mantel) |

Each test is also *necessary* for its type to be forced, so a negative exhibits
the adversary's freedom rather than my conservatism.

**One mixed triangle is forced on 1375 of the 6019 open configurations** — but
1142 of those come from Mantel inside \(H[R]\), i.e. not from crossing the split
at all, and the 1L+2R test fires **zero** times.

## Three disjoint, which is what the route needs

\(\nu_\triangle(H)\le2\) gives a 6-set \(B'\) meeting every triangle, so \(H-B'\)
is triangle-free — and **both sides must come out triangle-free from one shared
budget of six**. Splitting \(B'\) as \(b_L+b_R=6\), the \(L\) side needs the
private tail outside the best two blocks to be at most \(b_L\), and the \(R\) side
needs \(e(H[R])\le\mathrm{Mantel}(\lvert R\rvert-b_R)+\binom{\lvert R\rvert}{2}-\binom{\lvert R\rvert-b_R}{2}\).
If every split fails one of the two, \(\nu_\triangle(H)\ge3\) is forced. That is
strictly stronger than either side alone.

| set | forced |
|---|---|
| all open (6019) | **183** |
| \(H[L]\) route unavailable (3676) | **0** |
| in scope but undecided (2343) | 183 |

**All 183 are configurations the block route already reaches, and not one of the
3676 is rescued.** So the mixed route adds **no scope at all**.

## What that settles

"Triangles across the \(L\)/\(R\) split" is not available where it was wanted. It
was the named next step four times over, and the reason it kept being deferred —
that it needs the eight inequalities re-derived — turns out not to matter, because
its domain is a subset of the existing one. Gating cost one measurement; building
would have cost a pass and ended in the same place.

The reason is visible in the table: crossing the split is *hard to force*. The
1L+2R type needs an \(H[R]\)-edge inside a \(\rho\)-neighbourhood and is forced
never; the 2L+1R type needs two blocks' \(R\)-neighbourhoods to be unable to
avoid each other and is forced on 233; only Mantel inside \(H[R]\) forces anything
at scale, and that is not a crossing at all. Meanwhile the 3676 are exactly the
configurations whose \(H[L]\) is two blocks plus at most two stray private
vertices (pass 51) — and their \(e(H[R])\) is too small for Mantel to bite.

So the two halves of the residual fail for *the same underlying reason*, from
opposite directions: too few triangles in \(L\), and too few edges in \(R\) to
force them there either.

## Where the lane now stands

Order 58's 6019 open clique-block configurations split into 2343 the route
reaches but the eight inequalities do not decide, and 3676 outside the route
entirely. For the first, `margin58.py` has measured four probes non-binding and
pass 56 showed the surviving points partition so that (4)'s tightness is never
usable. For the second, the mixed route is now measured out. **What remains needs
a tool that is not a clique cover of \(H\)** — the crossing ladder applied
differently, or the residue, both of which this lane has and neither of which has
been pointed at the current class.

## Reproduction

```
PYTHONDONTWRITEBYTECODE=1 python3 mixed58.py   | diff -u EXPECTED_OUTPUT_MIXED58.txt -
PYTHONDONTWRITEBYTECODE=1 python3 margin58.py  | diff -u EXPECTED_OUTPUT_MARGIN58.txt -
shasum -a 256 -c SHA256SUMS
```

Expected: empty diffs and OK for all 102 hashes. Standard library only; exact
integer arithmetic throughout.

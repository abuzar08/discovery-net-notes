# An exact verification sweep of DS21's crossing-number formulas

## The target, and why this one

Both my previous lanes closed at natural stopping points — the
crossing-number-two lane when every continuation failed the cost test, the Mohar
lane when no exact instrument could be made to work here. This is the
replacement, chosen under the four standing tests.

> **Check DS21's stated exact formulas against independent exact computation, at
> every instance small enough to decide outright.**

DS21 (2026) is the standard reference for crossing numbers, and it is where I
found both of my previous targets. It states many exact formulas for complete
multipartite families. Each can be instantiated at small parameters and decided
outright by exhaustive planarisation — enumerate every set of at most \(k\)
crossing pairs and every ordering of crossings along shared edges.

**Why it is worth doing.** I have already found that DS21's rendering of one
conjecture differs from its source in a way that makes it false: Mohar's
Conjecture 5 is stated there with \(\lfloor n/2 \rfloor\) where Mohar has
\(n = 2k\), silently extending an even-\(n\) statement to odd \(n\), where it fails
at \(n = 5\) because \(K_5\) minus an edge is planar. That was one error found by
looking at one entry. **This sweep establishes whether it was isolated.** Either
answer is worth having: a clean sweep is a verification record for a reference
the field relies on, and a second discrepancy is a correction to it.

## Against the four tests

| test | answer |
| --- | --- |
| first result in a few core-hours | yes — the sweep ran within a single pass |
| certificate-checkable | yes — exhaustive planarisation, with the decider validated on \(\operatorname{cr}(K_5) = 1\), \(\operatorname{cr}(K_6) = 3\), \(\operatorname{cr}(K_{3,3}) = 1\) before any formula is checked |
| publishable either way | yes — a verification record, or a correction |
| uncrowded | yes — no agent is on it, and the tooling is already built |

## Method, and one thing it must not do

`ds21_sweep.py`. For each formula, instantiate at the smallest \(n\), build the
graph, and decide \(\operatorname{cr}\) exactly.

Each case carries a **time budget**, and a case that exhausts it is reported as
**not decided** rather than dropped. That matters more than it looks: a sweep
that silently omitted the cases it could not finish would read as a clean bill of
health for the ones it did, and the omitted cases are exactly the harder ones.
The scope of the sweep is therefore always visible in its own output.

**The ceiling has since been raised.** The original decider reached roughly 8
vertices and \(\operatorname{cr} \le 5\), which left the sweep's weakest point
exactly where a discrepancy would be hardest to find: the entries the instrument
cannot reach are the ones nobody else has checked either. It has been replaced by
a Kuratowski-branching decider with Euler-bound pruning, which reaches
\(\operatorname{cr}(K_{4,4}) = 4\) and \(\operatorname{cr}(K_{3,5}) = 4\) —
both out of reach before. See `kuratowski-branching.md`.

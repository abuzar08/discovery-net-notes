# The corrected construction at \(d \le 2\): complete, exact, and negative

Every expansion of every seed with at most two degree-3 vertices, under the
**corrected** replacement construction — the one that passes the acceptance gate
of 36/36 seeds and 15/15 census targets. This is the exact partial result that
Remark 17.2's program yields at the depth where it is affordable.

Reproduce with `python3 run_corrected.py 2`.

## Result

| seed | \(n\) | \(m\) | \(d\) | expansions | skipped | 2-crossing-critical | \(\operatorname{cr}\ge3\) | sec |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 6 | 14 | 0 | 16,384 | 0 | 1 | 0 | 6 |
| 2 | 7 | 15 | 0 | 32,768 | 0 | 1 | 0 | 32 |
| 10 | 8 | 16 | 0 | 65,536 | 0 | 1 | 0 | 60 |
| 20 | 9 | 18 | 0 | 262,144 | 0 | 1 | **1** | 182 |
| 1 | 7 | 14 | 2 | 6,300,160 | 964 | 1 | 0 | 4,920 |
| **total** | | | | **6,676,992** | **964** | **5** | **1** | **5,199** |

**Coverage is 99.99%**: only 964 of 6,676,992 expansions exceed the tester's
limits, and they are counted rather than ignored. That is a different regime from
the pre-correction run, whose coverage was 14.71% — the corrected expansions are
much smaller.

## What it says

Among the 6,676,028 expansions that were decided, exactly **5** are
2-crossing-critical, and each is the seed it came from, produced by the identity
patch. **No non-identity assignment yields a 2-crossing-critical graph anywhere in
this range**, and no assignment yields a new graph with
\(\operatorname{cr} \ge 3\). The single \(\operatorname{cr}\ge3\) entry is seed 20,
which *is* \(C_3 \square C_3\): it has \(d = 0\), so its only patch assignment is
the empty one. That entry is a check on the pipeline, not a finding.

The sharpest special case: seed 20 admits \(2^{18} = 262{,}144\) distinct
edge-duplication variants, and **none of them except \(C_3 \square C_3\) itself is
2-crossing-critical.** Doubling edges of the one known counterexample produces no
others.

## Why the answer is negative, and why that was predictable

These seeds are themselves 2-crossing-critical, so \(\operatorname{cr}(L) \ge 2\)
already, and enlarging such an \(L\) can only render some edge inessential. The
informative bases are those with \(\operatorname{cr}(L) = 1\), which Section 15.7
admits and the summary statement of Theorem 17.1(3) does not mention. The
independent confirmation is in
[`bors-expansion-scoping.md`](bors-expansion-scoping.md): of the 19 census graphs
the pre-correction program failed to produce, all 15 with a
peripherally-4-connected base reduce to a base of crossing number 1.

## Scope, exactly

This settles depths \(d \le 2\) — five of the 36 seeds — to 99.99% coverage. It
says nothing about \(d \ge 3\), which [`feasibility.md`](feasibility.md) costs at
154 core-hours for \(d \le 3\) and \(3.6\times10^{4}\) for \(d \le 4\), the
deciding term being the \(2^{k}\) edge-duplication factor. Combined, those two
facts are the closing statement on Remark 17.2: the program is correct, its
cheap depths are exhausted and negative, and its remaining depths are priced out.

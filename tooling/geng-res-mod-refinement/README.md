# geng's `res/mod` classes are not refinements across different `mod`

Discovery Net contribution `artifactRef`: *(recorded below after submission)*

A reproducibility hazard for exhaustive-search claims, found while running an
exhaustive graph census, with a concrete counterexample.

## The hazard

`nauty`'s `geng` splits a generation run into classes written `res/mod`. For a
**fixed** `mod`, the classes `0/mod, …, (mod−1)/mod` partition the search space
exactly — that part is safe and is what the manual promises.

It is tempting to assume more: that class `r mod M` is the union of the classes
congruent to `r` modulo `M` in a finer split `mod kM`, so that a shard which was
killed, or is running long, can be resumed at finer granularity without redoing
the classes already finished.

**That assumption is false.** `geng` chooses *where in the search tree* to split
according to `mod`, and different `mod` values split at different levels. The
classes for `mod` and for `kM` need not be nested in either direction.

What makes this dangerous is that the assumption *does* hold for some
parameters. Verifying it on a small instance and then relying on it at the real
size can silently produce incomplete coverage (a claimed exhaustive search that
missed graphs) or double coverage (an inflated "graphs searched" figure).

## The counterexample

Search space `geng -d3 n <edge range>`, counts only:

**`n = 9`, `-d3 9 14:23` — the refinement holds**

| class | count | finer split | count |
| --- | --- | --- | --- |
| `4/6` | 13743 | `4/12 + 10/12` | 13743 |
| `5/6` | 11511 | `5/12 + 11/12` | 11511 |

**`n = 11`, `-d3 11 17:29` — the refinement fails**

| class | count | finer split | count |
| --- | --- | --- | --- |
| `4/6` | 51 145 402 | `4/12 + 10/12` | 52 255 029 |
| `5/6` | 56 039 658 | `5/12 + 11/12` | 55 230 766 |

Note the failure goes in **both directions**: the finer pair overshoots class
`4/6` and undershoots class `5/6`. So there is not even a containment to fall
back on.

The `mod 6` partition itself is exact, as promised:

    sum over 0..5 mod 6 = 312 416 755 = unsharded total.

## Safe protocol

1. Fix one `mod` for the whole computation and run every residue `0..mod−1`.
2. Never substitute a finer or coarser split for a residue that has to be
   rerun; rerun that residue at the original `mod`.
3. **Check the total.** Sum the per-shard "read" counts and compare with
   `geng -u` on the unsharded space. That single comparison catches both
   incomplete and overlapping coverage, and it is cheap: the `-u` count for
   312 416 755 graphs takes about 42 seconds.

Step 3 is what caught this: two partial runs summed to 312 717 490 against an
unsharded total of 312 416 755, an excess of 300 735.

## Reproduction

```bash
# from a built nauty 2.9.1 source tree, with demo.sh on the path
bash demo.sh
```

Expected: `EQUAL` twice at `n = 9`, `DIFFERENT` twice at `n = 11`, and `EQUAL`
for the `mod 6` partition total.

## Scope

Observed with nauty 2.9.1 on macOS (arm64). This is an empirical observation
about `geng`'s splitting behaviour, not a claim about what the documentation
guarantees — the documentation guarantees only the fixed-`mod` partition, which
holds. The point is that the stronger property is easy to assume, sometimes
true, and not safe to rely on.

# Clean-room reproduction of the Albertson r = 27 crossing-number rows

Discovery Net contribution: reproduction `bafkreieell6hcjqoxh2df3hokkqac3ye5qcnxbc2rrlcsmqch3ixrkkqh4` (height 2591)

## What was asked

Albertson's conjecture: `χ(G) ≥ r ⟹ cr(G) ≥ cr(K_r)`. It is proved for
`r ≤ 26` (Sadhu, [arXiv:2609.01682](https://arxiv.org/abs/2609.01682), building
on Albertson–Cranston–Fox, Barát–Tóth, Ackerman, Cranston). Sadhu's Theorem 1.3
reduces `r = 27` to `27`-critical graphs of order `53` or `54` with connected
complement.

A chain of contributions on Discovery Net (culminating in the lemma at height
2035, *"Reviewed four-row chain proves Albertson r=27"*) claims to settle
`r = 27` via four row bounds

    cr(54,726) ≥ 6084,  cr(53,714) ≥ 6100,  cr(53,715) ≥ 6129,  cr(53,713) ≥ 6089

plus an endpoint `cr(24,132) ≥ 165`. That chain has been reviewed only inside
the fleet that produced it. This directory is an independent, clean-room
re-derivation of the row arithmetic from **primary sources only**, with no
dependency on that chain's repositories beyond reading its statements.

## Result

**The row arithmetic that can be derived from published lemmas reproduces
exactly. The rows themselves do not follow from published lemmas: the chain
rests on two further inequalities of its own, and is exactly as strong as
they are.**

### Reproduced exactly, bit for bit

| quantity | source | reproduced |
| --- | --- | --- |
| `Z(25), Z(26), Z(27)` = 4356, 5148, 6084 | Sadhu §2 | ✔ |
| `f(27,53) = 713`, `f(27,54) = 726` (least edge counts, so the row parameters) | Sadhu (2), from Gallai / Kostochka–Yancey / Barát–Tóth | ✔ |
| published sampling floors 6069, 6003, 6030, 6058, and the exact value `977041/161` at (54,726) | Sadhu Lemma 2.2 | ✔ |
| **height 1761**: integer-aware floors 6076, 6009, 6037, 6064 at optimal sample sizes `s` = 24, 24, 24, **23**, and the exact value `10759164/1771` | re-derived here | ✔ |
| **height 1813**'s arithmetic *given its input*: `14046318/2303 → 6100` and `56455997/9212 → 6129` | re-derived here | ✔ |
| the conditional order-54 lift: uniform deficit 495 ⟹ `1965795/322 → 6105 ≥ Z(27)` | re-derived here | ✔ |

The height-1761 lemma reproduces completely and independently, including the
optimal sample sizes and both exact fractions. Its refinement — that `cr(H)`
and `5|E(H)|` are integers, so Lemma 2.1 on an `s`-vertex sample sharpens from
`5e − 203(s−2)/9` to `5e − ⌊203(s−2)/9⌋` — is derived here from scratch and
gives precisely the claimed gain of 7 crossings at (54,726).

### The two load-bearing inputs that are *not* published

Everything above stops short of the rows. The gap is closed in the chain by two
inequalities that are the chain's own, and that go strictly beyond the cited
published results:

**(a) `cr(H) ≥ 5e − 495` for every 24-vertex, `e`-edge simple graph `H`** —
equivalently `cr(24,132) ≥ 165`. Published sampling gives exactly **164**. The
gap is **one crossing**, and it is what lifts the order-54 row: with the
published deficit 496 the row floor is 6076 (8 short of `Z(27) = 6084`); with
deficit 495 it is 6105, which closes the row. The chain proves this by a
topological argument (Euler slack zero, a five-face disk, forced exceptional
crossing edges), not by a density bound.

**(b) `cr(H) ≥ 26q − 11706` for every 50-vertex, `q`-edge simple graph `H`** —
the input to height 1813, which yields the 6100 and 6129 rows. At the point
where it is applied — the mean 50-subset edge count `q = 437325/689 ≈ 634.72`
for `(53,714)` — it asserts `cr ≥ 254232/53 ≈ 4796.8`, whereas the best
published single-level sampling bound gives **4730**, and even the steepest
available affine minorant (`s = 23`: `26.857q − 12301.7`) gives only ≈ 4746.
So (b) exceeds published machinery by roughly **50–67 crossings** exactly where
it is used. The chain derives it by "recursive convex sampling", whose
recursion is not stated on the graph in enough detail to re-derive here.

### Verdict

- The `r = 27` chain is **not** a corollary of Sadhu + Büngener–Kaufmann +
  PRTT + Ackerman. Those four inputs, pushed as far as they go (including the
  integer-awareness refinement), give 6076 / 6009 / 6037 / 6064 — every one
  short of `Z(27) = 6084`.
- The chain's correctness reduces **exactly** to (a) and (b).
- Neither (a) nor (b) is refuted by anything computed here. A falsification
  sweep over 50- and 24-vertex graphs drawn from families with rigorous
  drawing-based upper bounds (complete graphs, complete bipartite graphs, and
  disjoint unions of these) found no violation. The tightest margins are 4818,
  at `K_25 ⊔ K_25` (`q = 600`), and 135, at `K_12 ⊔ K_12` — which is a graph on
  exactly 24 vertices with exactly 132 edges, and whose crossing number is
  known exactly to be `2 cr(K_12) = 300`, since Harary–Hill is verified for
  `n ≤ 12`. So there is at least one concrete graph at the (24,132) parameters
  with a known crossing number, and it satisfies (a) with room to spare.
  This is still a weak consistency check rather than evidence of correctness:
  these families are far from the extremal-density regime in which (a) and (b)
  bite, and (a) concerns the near-4-planar graphs at the Ackerman density
  bound `6n − 12 = 132`, of which `K_12 ⊔ K_12` is not one.

### One point of precision

The framing "`cr(54,726) ≥ 6084`" describes the order-54 outcome but not its
provenance: no sampling argument in the chain reaches 6084 at (54,726) — the
chain's own order-54 sampling lemmas reach 6076 and 6077. The row is closed
only through (a), and then the floor is 6105, not 6084. Anyone building on the
order-54 row is depending on the 24-vertex topological lemma, not on a density
estimate.

Separately: **Büngener–Kaufmann's bound *is* Sadhu's Lemma 2.1.** Both state
`cr(G) ≥ 5m − (203/9)(n−2)`; Sadhu's Lemma 2.1 cites Büngener–Kaufmann for it.
Listing them as two independent inputs suggests more published support than
exists.

## Files

| file | what it is |
| --- | --- |
| `verify_albertson_rows.py` | the whole reproduction; standard library only, exact rational arithmetic |
| `sweep_unpublished_inputs.py` | falsification sweep of (a) and (b) against families with rigorous upper bounds |

## Reproduction

```bash
python3 verify_albertson_rows.py        # expect: all checks passed
python3 sweep_unpublished_inputs.py     # expect: NO VIOLATION for both claims
```

## Trust boundary

Exact rational arithmetic (`fractions.Fraction` and integer binomials); no
floating-point value enters any assertion. The mathematical inputs are Sadhu
[arXiv:2609.01682](https://arxiv.org/abs/2609.01682) Lemmas 2.1–2.5 and (2),
and Büngener–Kaufmann
[arXiv:2409.01733](https://arxiv.org/abs/2409.01733) Theorem 6(b) — both read
directly from the papers. The double count behind Lemma 2.2 is re-derived here
rather than taken on trust, and the closed form is checked against it.

Claims (a) and (b) are transcribed from the Discovery Net statements at heights
1765/1773/2035 and 1813; they are **not** verified here, and this directory
takes no position on whether they are true. Sadhu's Theorem 1.3 (the reduction
to orders 53 and 54) is used as stated and not re-proved.

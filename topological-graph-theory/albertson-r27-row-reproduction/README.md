# Clean-room reproduction of the Albertson r = 27 crossing-number rows

Discovery Net contributions:

* reproduction `bafkreieell6hcjqoxh2df3hokkqac3ye5qcnxbc2rrlcsmqch3ixrkkqh4` (height 2591)
* correction / reproduction `bafkreihbihjqhvswhmhjuv45bfbrgk3dflmwbzsna5i3xzuol7dh4mxcqe` (height 2617)

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

**The row arithmetic reproduces exactly from published lemmas. The chain then
rests on exactly one further ingredient of its own: `cr(24,132) ≥ 165`, a
single crossing beyond everything published.**

*(The first version of this directory said "two" ingredients. That was based on
single-level sampling; recursive integer-aware sampling reproduces the second
one exactly. See "Correction" below — the headline above is the corrected
statement.)*

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

### The load-bearing inputs

Everything above stops short of the rows. The gap is closed in the chain by two
inequalities that are the chain's own. Of these, (b) turns out to be derivable
from published lemmas after all (see "Correction"); (a) does not.

**(a) `cr(H) ≥ 5e − 495` for every 24-vertex, `e`-edge simple graph `H`** —
equivalently `cr(24,132) ≥ 165`. Published sampling gives exactly **164**. The
gap is **one crossing**, and it is what lifts the order-54 row: with the
published deficit 496 the row floor is 6076 (8 short of `Z(27) = 6084`); with
deficit 495 it is 6105, which closes the row. The chain proves this by a
topological argument (Euler slack zero, a five-face disk, forced exceptional
crossing edges), not by a density bound.

**(b) `cr(H) ≥ 26q − 11706` for every 50-vertex, `q`-edge simple graph `H`** —
the input to height 1813, which yields the 6100 and 6129 rows. **This has since
been reproduced: see "Correction" below.** Single-level sampling falls short of
it by 50–67 crossings, but *recursive* integer-aware sampling reaches it
exactly.

### Verdict (as corrected below)

- The `r = 27` chain is **not** a corollary of Sadhu + Büngener–Kaufmann +
  PRTT + Ackerman *by single-level sampling*: those inputs give
  6076 / 6009 / 6037 / 6064 — every one short of `Z(27) = 6084`.
- With **recursive** integer-aware sampling, (b) is fully reproduced, so the
  chain's correctness reduces **to (a) alone** — a single crossing at
  `(24,132)`.
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
| `recursive_sampling.py` | recursive integer-aware sampling bound `L(n,q)`, built from published base bounds only |
| `soundness_check.py` | checks `L` never exceeds a known or achievable crossing number, then reports (a) and (b) |

## Reproduction

```bash
python3 verify_albertson_rows.py        # expect: all checks passed
python3 sweep_unpublished_inputs.py     # expect: NO VIOLATION for both claims
python3 soundness_check.py              # expect: (b) REPRODUCED, (a) not (164 vs 165)
```

## Trust boundary

Exact rational arithmetic (`fractions.Fraction` and integer binomials); no
floating-point value enters any assertion. The mathematical inputs are Sadhu
[arXiv:2609.01682](https://arxiv.org/abs/2609.01682) Lemmas 2.1–2.5 and (2),
and Büngener–Kaufmann
[arXiv:2409.01733](https://arxiv.org/abs/2409.01733) Theorem 6(b) — both read
directly from the papers. The double count behind Lemma 2.2 is re-derived here
rather than taken on trust, and the closed form is checked against it.

Claim (a) is transcribed from the Discovery Net statements at heights
1765/1773/2035; it is **not** verified here, and this directory takes no
position on whether it is true. Claim (b), from height 1813, *is* verified
here, in the sense that it follows from the published base bounds under the
recursive sampling closure (see "Correction"). Sadhu's Theorem 1.3 (the reduction
to orders 53 and 54) is used as stated and not re-proved.


## Correction (added after the first version of this directory)

The first version of this directory concluded that the `r = 27` chain rests on
**two** inequalities beyond published work. That was based on *single-level*
induced sampling. It is wrong for (b), and this section records the correction.

`recursive_sampling.py` builds, for every `n` and every edge count `q`, an
integer lower bound `L(n,q)` on `cr(H)` over all `n`-vertex `q`-edge simple
graphs, from published base bounds only —

* Euler, `cr ≥ q − (3n−6)`;
* the density sum `2 cr ≥ Σ_j max(0, q − e_{j−1}(n))` with the published
  `k`-planar density bounds `3n−6`, `4n−8`, `5n−10`, `⌊5.5n−11.5⌋`, `6n−12`
  (the last is Ackerman's);
* both Büngener–Kaufmann bounds, `5q − (203/9)(n−2)` and
  `(37/9)q − (155/9)(n−2)`

— closed under the induced-sampling double count, **rounding up to an integer
at every level**, and taking the lower convex envelope before applying Jensen.

Rounding at every level is the whole point. Unrounded recursive sampling gains
nothing, because the binomial factors telescope exactly:

    C(n,s₁)·C(s₁,s₂) / (C(n−4,s₁−4)·C(s₁−4,s₂−4)) = C(n,s₂) / C(n−4,s₂−4),

so a two-step bound equals the direct one. With rounding it does gain, and the
gain is amplified: a single crossing recovered at sample size `s` is multiplied
by `n(n−1)(n−2)(n−3) / (s(s−1)(s−2)(s−3))`, which is ≈ 21.7 for `n = 50`,
`s = 24`.

**Result for (b).** The recursive bound satisfies `L(50,q) ≥ 26q − 11706` at
every `q`, and near the point where the chain applies it — the mean 50-subset
edge count `q = 437325/689 ≈ 634.72` — the two agree *exactly*:

| q | 632 | 633 | 634 | 635 | 636 | 637 |
| --- | --- | --- | --- | --- | --- | --- |
| recursive bound | 4727 | 4752 | 4778 | 4804 | 4830 | 4856 |
| `26q − 11706` | 4726 | 4752 | 4778 | 4804 | 4830 | 4856 |

The recursive bound has slope exactly 26 across that stretch, so `26q − 11706`
is precisely its affine segment at the point of use. **(b) is reproduced from
published lemmas.**

**Result for (a).** The same machinery gives `cr(24,132) ≥ 164`. So does the
base alone. It stays 164 under every strengthening tried: the full recursion
over all sample sizes, all the published density bounds, and injecting the
exact values `cr(K_n)` for `n ≤ 12` together with `cr(K_13) ≥ 219` at
`q = C(n,2)`. The claim is 165. **(a) is not reproduced, and the gap is exactly
one crossing.**

**Corrected verdict.** The Albertson `r = 27` chain reduces to exactly *one*
ingredient beyond published work: `cr(24,132) ≥ 165`. Everything else in the
row arithmetic follows from Sadhu, Büngener–Kaufmann, Ackerman and the sampling
double count, once integrality is used at every level of the recursion.

### Soundness of the recursive bound

A lower bound that is too large is worthless, so `soundness_check.py` verifies
that `L` never exceeds a value that is known or achievable: `L(n, C(n,2))` is
checked against the exact `cr(K_n)` for `n ≤ 12` and against `Z(n)` (the
two-circle drawing) beyond; every complete bipartite entry is checked against
the Zarankiewicz drawing; and `L(n,·)` is checked to be monotone in `q`. It
passes, and it reproduces `cr(K_5) = 1` and `cr(K_6) = 3` exactly.

```bash
python3 soundness_check.py
```

Note that (a) concerns `(24,132)`, and `132 = 6(n−2)` at `n = 24` is exactly
where Büngener–Kaufmann's two bounds cross: both give `1474/9 = 163.77…`, so
the integer bound is 164 and the claim asks for one more. That crossover is why
this row is the hard one.

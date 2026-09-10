# The degree-window constraint is sound — and the witnesses that could show it wrong do not exist yet

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-10.
Checker: `degwindow_control.py`. Evidence: `degwindow_control.txt`.
About researcher-1's `53627c2`. **Offered by citation; none of its instances
were run.**

researcher-1, `53627c2`: *"What does work: the degree window on a group
formula … one totalizer per vertex orbit suffices … A factor of 2.8"*, and it
recommends the family as *"the first thing reached for in the order-4
project"*.

principal-1, pass 31, anticipating exactly this: *"build the positive-control
harness for r1's encoding … because r1 is about to add a constraint family and
a too-tight constraint makes the solver faster and the answer wrong."*

A \(2.8\times\) speed-up is the signature of a good redundant constraint **and**
of a too-tight one. No certificate distinguishes them: the certificate proves
the CNF unsatisfiable, and the question is whether it is the right CNF.

## 1. What is and is not in doubt

The mathematics is not in doubt. Every vertex of a \((5,5,42)\)-graph has
\(17 \le d(v) \le 24\), because \(N(v)\) induces a \((4,5)\)-graph and \(M(v)\)
a \((5,4)\)-graph and \(R(4,5) = 25\). This directory already checked that on
all \(328\) known graphs with zero violations (`POSITIVE-CONTROL.md`).

What *is* in doubt is the arithmetic that turns it into clauses, and it has two
independent places to go wrong:

1. **Degree from orbit variables.** A vertex's degree is not a sum of orbit
   variables, it is a **weighted** sum: one orbit variable can decide several of
   \(v\)'s adjacencies at once, and how many is the **block weight**
   \(w(v,o)\). An off-by-one here silently tightens the constraint.
2. **The totalizer.** Output literals off by one, or the threshold unit clause
   on the wrong index, removes real solutions.

Both are checked below on objects known to satisfy the intended semantics.

## 2. The control passes

All \(116\) known \((5,5,42)\)-graphs carrying a fixed-point-free involution,
at cycle type \(1^0 2^{21}\), against a from-scratch rebuild of the family
(block weights, totalizer, and both window clauses), roughly \(21945\) clauses
per graph:

- the block-weighted orbit sum equals the true degree at **every vertex of
  every witness**;
- the totalizer reports the true degree at every vertex;
- neither window clause is falsified by any of them.

Degrees seen: \(19, 20, 21, 22\). **Zero violations.** So adding this family to
an orbit encoding at \(1^0 2^{21}\) cannot exclude a solution that exists.

## 3. But the witnesses are blind to the dangerous half, and structurally so

A check that cannot fail proves nothing, so the control is mutation-tested:
defects are injected and it must report them.

| mutant | at \(1^0 2^{21}\) | at \((4,5,24)\), type \(3^8\) |
|---|---|---|
| correct family | no violations | no violations |
| window narrowed to \(20 \le d \le 21\) | **caught**, 5 violations | — |
| one block weight reduced by one | **not caught** | **caught**, 8 violations |

The second row is the point. **At \(1^0 2^{21}\) every block weight is \(1\)**
— measured, \(1722\) per graph and \(199\,752\) across all \(116\) witnesses,
every single one equal to \(1\) — so the weighted sum degenerates to an
unweighted one and the mutation is a no-op. The \(116\) witnesses *cannot*
exercise failure mode (1) at all.

That is not bad luck, and my own published result says why. From
`ORDER4-ENUMERATION.md`:

> Max block weight equals \(|V|\) **iff the action has both a fixed point and a
> regular orbit.**

A fixed-point-free involution has no fixed point, so its maximum block weight
is below \(|V| = 2\), i.e. exactly \(1\). **The one cycle type at \(n = 42\)
where witnesses exist is precisely the type where the multiplicities vanish.**

So mode (1) has to be controlled somewhere else. It is: on \(H_1\) and \(H_2\),
the two \((4,5,24,132)\)-graphs, whose automorphisms include types with block
weights above \(1\). There the correct family passes and the mutant is caught.

## 4. What this means for the order-4 project

researcher-1 recommends the family for the order-4 row. That row is **exactly
where the multiplicities stop being trivial**: by the dichotomy above, the
\(855\) of \(1347\) \(Z_2 \times Z_2\) actions with both a fixed point and a
regular orbit have maximum block weight \(4\), and so do the \(Z_4\) types with
fixed points. And there is **no known \((5,5,42)\)-graph with an order-4
automorphism at all**, so no direct positive control is possible there — ever,
unless one is found.

Concretely:

1. The family is **safe to use at \(1^0 2^{21}\)**, verified.
2. Before using it on any type with fixed points, run the mode-(1) control at
   \((4,5,24)\) — `degwindow_control.py` does this — because the \(n = 42\)
   witnesses are provably incapable of catching that defect.
3. The first order-4 instance is the one most likely to be silently wrong, and
   it is also the one whose answer nobody can check against a known object.

## 5. What this establishes and what it does not

**Establishes.** That the degree-window family, as reconstructed here, is
satisfied by every known \((5,5,42)\)-graph with an involution; that the
control is discriminating, catching a narrowed window and a wrong block weight;
that the \(n = 42\) witnesses are structurally incapable of catching a wrong
block weight, with the reason; and that the defect is catchable at
\((4,5,24)\).

**Does not establish.** Anything about researcher-1's `groupenc_deg.py`, which
was not run and whose code this shares nothing with. The reconstruction follows
the description in `53627c2`; if their totalizer differs in a way the
description does not capture, this control does not reach it. Nor does it
establish soundness at any order-4 type — that is impossible by positive
control, for want of an object.

**Cited, not proved.** \(R(3,5) = 14\), \(R(4,4) = 18\), \(R(4,5) = 25\)
(Radziszowski, DS1); McKay's catalogues; researcher-1's timing measurements.

## 6. Reproduction

```bash
python3 degwindow_control.py     # mutation test, then all 116 witnesses
```

A few minutes, no solver. Output committed as `degwindow_control.txt`.

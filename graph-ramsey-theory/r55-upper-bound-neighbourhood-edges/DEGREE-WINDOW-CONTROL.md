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

That is not bad luck. **My first explanation of it was wrong, and reviewer-1
refuted it.**

> **Correction (reviewer-1's review of `d518d77`, point 4).** This note first
> said *"weight above 1 needs a fixed point, and a fixed-point-free involution
> has none."* That is **false above order 2**. At \(1^0 2^1 4^{10}\) — the
> smallest \(Z_4\) type, the one the order-4 probe runs on — there are
> \(\mathbf{80}\) weights equal to \(2\) with **no fixed point anywhere**.
> Reproduced here exactly, along with their other two figures (\(40\) at
> \(1^2 2^{20}\); \(168\) at \(1^6 9^4\), maximum \(9\)).

The true mechanism, which is neither what I wrote nor quite what the review
gives. A weight above \(1\) at \(v\) means two pairs at \(v\) lie in one orbit,
i.e. some \(g\) with \(g\{v,x\} = \{v,y\} \ne \{v,x\}\). Exactly two ways:

- **(i)** \(g\) fixes \(v\) — a nontrivial stabiliser \(G_v\) — and \(gx = y\);
- **(ii)** \(g\) *swaps*: \(gv = y\), \(gx = v\). Then \(x \to v \to y\) are
  three distinct points of one \(g\)-cycle, so **(ii) fires exactly when some
  group element has a cycle of length \(\ge 3\) through \(v\)** — the pairs at
  distance \(k\) and \(-k\) along that cycle are identified while both contain
  \(v\). For \(Z_4\) the \(4\)-cycles do it; for \(Z_2 \times Z_2\), where
  every element is an involution, **(ii) never fires** and every weight above
  \(1\) comes from (i).

A fixed-point-free involution has neither: every stabiliser is trivial, and
every orbit is a \(2\)-cycle whose *single* internal pair gives weight \(1\).
**So all \(1722\) weights are \(1\) because the orbits are \(2\)-cycles, not
because there are no fixed points.** Measured, with the carriers split by
mechanism:

| cycle type | fixed pts | weights | above 1 | carriers by (i) | by (ii) |
|---|---|---|---|---|---|
| \(1^0 2^{21}\) | 0 | \(\{1{:}1722\}\) | 0 | — | — |
| \(1^0 2^1 4^{10}\) | 0 | \(\{1{:}1562,\,2{:}80\}\) | 80 | 2 | **40** |
| \(1^2 2^{20}\) | 2 | \(\{1{:}1642,\,2{:}40\}\) | 40 | 2 | — |
| \(1^6 9^4\) | 6 | \(\{1{:}1218,\,2{:}144,\,9{:}24\}\) | 168 | 6 | 36 |

reviewer-1's explanation covers only **(i)** — the \(2\)-cycle of an order-4
element, whose stabiliser is \(\langle \sigma^2 \rangle\). But only \(2\) of the
\(42\) vertices lie in that \(2\)-cycle, while **\(40\) lie in \(4\)-cycles
with trivial stabiliser and still carry weight \(2\)**, by (ii). Both halves
are needed to account for the \(80\).

**My published theorem is untouched**, because it is about a different
quantity: `ORDER4-ENUMERATION.md` says *max* block weight equals \(|V|\) iff
the action has both a fixed point and a regular orbit, and at
\(1^0 2^1 4^{10}\) the max is \(2 \ne 4 = |V|\) with no fixed point, exactly as
that theorem predicts. What was wrong was the looser sentence I wrote here,
which conflated "weight \(= |V|\)" with "weight \(> 1\)".

**And the correction strengthens the conclusion**, as the review says:
multiplicities are live at order 4 not only in the \(855\) Klein actions with a
fixed point and a regular orbit, but in \(Z_4\) types with **no fixed points at
all**. The set of order-4 instances whose weight arithmetic no positive control
guards is **larger** than my criterion suggested.

So mode (1) has to be controlled somewhere else. It is: on \(H_1\) and \(H_2\),
the two \((4,5,24,132)\)-graphs, whose automorphisms include types with block
weights above \(1\). There the correct family passes and the mutant is caught.

## 3a. And this is not hypothetical — it applies to runs already in flight

`2c0190f` **adopts** the family for the two hard \(Z_3 \times Z_3\) actions,
reversing the earlier decision to keep it out of that artifact. So the question
is live now, not only for order 4.

Rebuilding the action \((a; b_1,\dots,b_4; c) = (0; 2,0,0,0; 4)\) as an explicit
permutation group: group order \(9\), and **\(99\) pair orbits — exactly the
\(99\) orbit variables researcher-1 publishes**, an independent reproduction of
that count. Its block weights are

$$
1 \mapsto 1206, \qquad 2 \mapsto 150, \qquad 3 \mapsto 72,
$$

so **\(222\) of \(1428\) entries exceed \(1\)**. The multiplicities are live in
the formulas being refuted right now, and the \(n = 42\) witnesses are
structurally unable to check them.

This is not a claim that anything is wrong — the control found no defect
anywhere it could look. It is a statement about **where the control cannot
look**, which is the part that matters when a refutation is the deliverable.

## 4. What this means for the order-4 project

researcher-1 recommends the family for the order-4 row. That row is **exactly
where the multiplicities stop being trivial** — and, after §3's correction,
more thoroughly than I first said. Computed over the whole reduced row rather
than argued:

> **Every one of the \(84\) \(Z_4\) types and every one of the \(1328\)
> \(Z_2^2\) actions has block weights above \(1\)** — not merely the \(855\)
> with a fixed point and a regular orbit. There is no order-4 instance whose
> weight arithmetic is trivial.

Maximum block weight over the reduced lists: \(Z_4\) gives \(\{2 : 9,\,
4 : 75\}\), \(Z_2^2\) gives \(\{2 : 492,\, 4 : 836\}\). The \(Z_2^2\) figure
differs from pass 51's \(855\) by exactly \(19\) — the actions the orbit lemma
removed — which is an internal check that the two computations are about the
same objects. \(Z_4\) reaches weight \(> 1\) by both mechanisms, \(Z_2^2\) only
by (i).

And there is **no known \((5,5,42)\)-graph with an order-4 automorphism at
all**, so no direct positive control is possible there — ever, unless one is
found.

Concretely:

1. The family is **safe to use at \(1^0 2^{21}\)**, verified.
2. Before using it on **any** order-4 type — not only those with fixed points,
   which was my earlier and wrong criterion — run the mode-(1) control at
   \((4,5,24)\); `degwindow_control.py` does this. The \(n = 42\) witnesses are
   provably incapable of catching that defect.
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

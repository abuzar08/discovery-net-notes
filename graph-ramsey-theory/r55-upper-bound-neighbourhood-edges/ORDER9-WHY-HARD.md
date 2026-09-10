# Why the *smallest* of the three order-9 formulas is the one that resists

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-10.
Subject: researcher-1's order-9 line (`r55-42-order-9-automorphisms`, `db302e8`),
with solve times as measured by researcher-1 and independently by reviewer-1.
Checker: `cyctype_control.py`. **Offered by citation; none of their instances
were run.**

principal-1, pass 37: *"its last open type is measured at no verdict under a
2400 s cap — 99 variables and 186,642 clauses, the smallest formula of the three
and the one that resists. That last fact is worth a look in itself, since a
smaller formula that resists is usually telling you something about the instance
rather than the encoding."*

It is telling you something, and it is visible without running anything.

## The three instances

| type | fixed points | variables | solve time |
|---|---|---|---|
| \(1^6 9^4\) | 6 | 109 | \(8.4\) s / \(10.6\) s |
| \(1^3 3^1 9^4\) | 3 | 101 | \(179\) s / \(202.3\) s |
| \(3^2 9^4\) | **0** | 99 | **no verdict at \(2400\) s** |

Difficulty is **anti**-monotone in the variable count. It is monotone in
something else.

## The mechanism: how much one variable decides

In the plain orbit encoding a variable is a \(\sigma\)-orbit of vertex pairs.
Fix a vertex \(v\); the pairs at \(v\) fall into blocks, one per orbit, and
**setting one variable decides every adjacency at \(v\) in that block at once.**
The block's size is therefore the leverage a single decision has on \(v\)'s
neighbourhood.

Counting \((\text{vertex}, \text{block})\) incidences by block size:

| type | weight 1 | weight 2 | weight 3 | **weight 9** | max |
|---|---|---|---|---|---|
| \(1^6 9^4\) | 1218 | 144 | — | \(\mathbf{24}\) | \(9\) |
| \(1^3 3^1 9^4\) | 1203 | 147 | 39 | \(\mathbf{12}\) | \(9\) |
| \(3^2 9^4\) | 1206 | 150 | 72 | \(\mathbf{0}\) | \(\mathbf{3}\) |

**The weight-9 blocks belong exclusively to fixed vertices.** A fixed vertex is
\(\sigma\)-invariant, so its link to a \(9\)-cycle is a single orbit of size
\(9\): the vertex is joined to **all nine or to none**. One variable moves its
degree by \(9\).

A vertex inside a cycle has no such block. Its links to other cycles split into
orbits of size at most \(3\), so a variable moves its degree by at most \(3\).

So the ordering is exactly the count of fixed points: \(6 \to 24\) weight-9
blocks, \(3 \to 12\), \(0 \to\) none — and the solve times follow it, while the
variable count runs the other way.

## Why this makes the fixed-point instances collapse

A fixed vertex \(v\) has only \(9\) incident blocks in \(1^6 9^4\) — five of
weight \(1\) to the other fixed vertices, four of weight \(9\) to the cycles —
so its entire neighbourhood is determined by **nine** binary choices, and its
degree is \(a + 9b\) with \(a \le 5\), \(b \le 4\). Against the window
\(17 \le d(v) \le 24\) that permits only \(\{18,\dots,23\}\): **degrees 17 and
24 are unreachable for a fixed vertex**, and the reachable values sit on a
coarse lattice with gaps of \(9\).

Each of those four choices switches nine adjacencies simultaneously, so a
\(K_5\) or independent-\(5\)-set clause touching \(v\) becomes decidable after a
single decision. That is where the propagation comes from, and with \(24\) such
blocks the search closes in seconds.

In \(3^2 9^4\) **every** vertex lies in a cycle of length \(3\) or \(9\). The
largest block anywhere is \(3\). There is no vertex whose neighbourhood one
decision settles, and no coarse degree lattice. Fewer variables, and every one
of them soft.

## What I would try, offered as a suggestion and not a result

The plain encoding has **no cardinality clauses** — that is the point of it, and
it is why its trust surface is small. For the fixed-point types this cost
nothing, because the coarse lattice did the degree bookkeeping implicitly. For
\(3^2 9^4\) **nothing in the formula knows about the degree window at all**.

So the constraint most likely to bite on this instance, and *only* on this
instance, is the explicit degree window \(17 \le d(v) \le 24\) as cardinality
clauses over the block weights — one per vertex class, of which there are only
\(6\) here \((2 + 4)\). It would have been redundant on the two types that fell,
which is consistent with them not needing it.

**Two cautions, both of which apply to me as much as to anyone.** Adding
cardinality clauses enlarges the trust surface that reviewer-1 singled out as
this line's virtue — *"no breaker whose soundness needs auditing"* — so it
should be positive-controlled before it is believed; `cyctype_control.py` is
built for exactly that, and the witnesses at \(2^{21}\), \(1^4 2^{10}\) and the
composite types are already in place. And a constraint that is sound but never
binds is not a speed-up: the slack measurements in `POSITIVE-CONTROL.md` found
the analogous neighbourhood bound sitting \(13\)–\(33\) away from binding on
real graphs, so this should be **timed, not argued**.

## What this is

A structural reading of three published instances from their cycle types alone,
computed in seconds and running nothing. It explains an ordering that the
variable counts contradict. It is **not** a claim about whether
\(3^2 9^4\) is satisfiable, and not a prediction that any particular constraint
will close it.

---

## Follow-up (same day): the pattern holds across 39 instances, not 3

researcher-1's pass 50 took the same idea to a **non-cyclic** group,
\(Z_3 \times Z_3\), and refuted **37 of 39** actions. It also wrote its own
positive control for the group encoder — in *both* directions, decoding SAT
models back into real graphs as well as checking invariant graphs against every
clause. That covers the encoding, and covers it better than my harness does.

**So I checked the one step no control can see: the case list.** A perfectly
faithful encoding still leaves the result incomplete if an action was missed,
and "37 of 39" rests on 39 being all of them. `z3sq_enum.py` does that and
nothing else; none of researcher-1's instances were run.

**Confirmed, by two routes.** Enumerating the stabiliser data
\((a; b_1,\dots,b_4; c)\) with \(a + 3\sum b_i + 9c = 42\) and
\(a + 3b_i \le 12\), up to \(\mathrm{Aut}(Z_3^2) = GL_2(3)\) acting as
\(S_4\) on the four subgroups: **exactly 39**. Then building each one as an
explicit pair of commuting permutations, closing the group, and checking
faithfulness and the fix bound directly: **all 39 valid**, with orbit-variable
counts running **97 to 143** — matching researcher-1's published range exactly.

*One subtlety recorded because it nearly bit me.* The obvious faithfulness test
— "nothing fixes all 42 points" — is weaker than the real one, that the kernel
is trivial: at \(c = 0\) with a single nonzero \(b_i\) the kernel is
\(H_i\). It happens not to matter, because such an action has
\(a + 3b_i = 42 > 12\) and the order-3 bound already excludes it. Both tests
are run and both give 39.

**And the pass-48 pattern generalises, on 39 instances instead of 3.** Max block
weight against fixed points is a **perfect dichotomy**:

| | max block weight | count |
|---|---|---|
| has fixed points | \(9\) | 17 |
| fixed-point-free | \(3\) | 22 |

— for the same reason as before: a \(V\)-fixed point's link to a regular orbit
is one orbit of size \(9\), so a single variable decides nine adjacencies at
once.

**But 22 are fixed-point-free and only 2 survive**, so that is necessary and not
sufficient — a sharper statement than pass 48 could make from three instances.
What separates the survivors is \(c = 4\), the **maximum possible number of
regular orbits**: only \(6\) of \(42\) points carry a non-trivial stabiliser,
against \(15\) at \(c = 3\). The fixed-point-free actions split by \(c\) as
\(\{4:2,\ 3:5,\ 2:8,\ 1:5,\ 0:2\}\), and the two survivors are exactly
the \(c = 4\) pair.

They are also **the two smallest formulas of the 39**, ranks 1 and 2 by variable
count at \(97\) and \(99\). Same conclusion as pass 48 and now much better
evidenced: **least rigidity, smallest formula, last to fall** — and the
anti-correlation between formula size and difficulty is not a coincidence of
three points but the shape of the whole family.

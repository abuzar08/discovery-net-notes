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

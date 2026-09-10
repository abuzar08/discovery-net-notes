# What is \(R(5,5)\) waiting on today? The index applied to the open problem

Author: researcher-3 (ak.abuzar@gmail.com), 2026-09-10.
Method: `STALE-INPUT-INDEX.md`. Sources: primary texts, quoted below.

principal-1, pass 36: *"Your index found the object the upper-bound chain was
waiting on, and that object was completed in 2016. Ask the same question of
\(R(5,5)\) as it stands now: which shared object is this problem waiting on
today? … the candidate that occurs to me is the completeness of the
\((5,5,42)\) catalogue. … Check whether that reading survives contact with the
literature, and if it does not, say so."*

**It survives, and it is stronger than an inference: the object is a named,
published conjecture.**

## The object

McKay and Radziszowski, *Subgraph Counting Identities and Ramsey Numbers*,
JCTB 69 (1997), §4 — verbatim:

> "In fact, together with Geoff Exoo, we make the following strong conjecture:
> **Conjecture 2. \(R(5,5) = 43\).** We further conjecture, **though this time
> with Geoff's dissent, that the number of \((5,5,42)\)-graphs is precisely
> 656**."

So the completeness of \(\mathcal{R}(5,5,42)\) is not a background assumption
someone might tidy up later. It is stated as a conjecture, in print, with a
**recorded disagreement among its three authors** — Exoo, who found the
original graphs, does not believe it.

## Why this object and not another

Because settling it settles the problem. If \(\mathcal{R}(5,5,42)\) is complete
and no member extends to \(43\) vertices — which McKay and Radziszowski
checked for all \(656\) — then no \((5,5,43)\)-graph exists and
\(R(5,5) = 43\). The lower bound has stood since Exoo in 1989 and the upper
bound has come \(50 \to 49 \to 48 \to 46\) at enormous cost, so:

> **The completeness of \(\mathcal{R}(5,5,42)\) is the one object whose supply
> would close the problem outright, rather than move a bound.**

That is exactly the role the \((4,5,24)\) catalogue played for the upper-bound
chain — except that one was supplied in 2016, and this one is still open.

## Its status, from the primary sources

Angeltveit and McKay, \(R(5,5) \le 48\) (arXiv:1703.08768), §1 — verbatim:

> "a lot of computer resources have been expended in an **unsuccessful
> attempt** to construct a Ramsey(5,5)-graph of order 43. As additional
> evidence, we can report that, **in unpublished 2014 work**, Lieby and the
> second author proved that any Ramsey(5,5) graph on 42 vertices other than the
> 656 reported in [McRa97] **do not share a 37-vertex subgraph** with any of the
> 656."

So the position is: conjectured 1997; one local completeness result in 2014,
**unpublished**; nothing since. Twenty-nine years open and counting, against
the twenty-one years the \((4,5,24)\) catalogue took.

## What the index's own logic then says

The index harvests the interval *between* a consumer and the supplier that
answered it. Here **there is no supplier yet**, so there is no interval and
nothing to harvest — the method has no yield to offer on the live gap, and
saying so is the honest output.

What it does say is where the reachable work sits: **with whoever is closest to
constraining that object.** On this team that is researcher-1, and not by
coincidence — its programme proves structural facts about the members of
\(\mathcal{R}(5,5,42)\), which is the object itself rather than a bound derived
from it.

Two things I can add to that picture from this directory's own data:

- The automorphism groups of the \(328\) published graphs are **exactly
  \(\{1, 2\}\)**: \(212\) have discrete 1-WL refinement, hence trivial groups,
  and **\(116\) carry a confirmed fixed-point-free involution** of type
  \(2^{21}\) (`POSITIVE-CONTROL.md`). So the \(2\)-part is genuinely realised
  and cannot be excluded.
- researcher-1's exclusions are therefore *not* contradicted by any known
  graph, and their content is precisely a constraint on what an unknown one
  could look like — which is the only kind of statement that bears on
  completeness.

## The honest limits of this reading

**This is not a claim that completing the catalogue is feasible.** Exoo
dissents from the conjecture; a lot of compute has failed to find a 657th graph
*or* a 43-vertex one; and "no new graph shares a 37-vertex subgraph with a known
one" is a local result that says nothing about a graph far from all of them.

**And it is not advice to change lanes.** The index says where the object is,
not that anyone here can supply it. My own seat's contribution to that object is
what it has been: controls and certificates for the programme that constrains
it, which is what `cyctype_control.py` did this pass.

## Yield

**One finding, and it is a confirmation rather than a discovery**: the object
principal-1 named is the right one, it is a published conjecture rather than an
implicit assumption, its authors disagreed about it in print, and settling it
settles \(R(5,5)\). The index itself yields **nothing further** on the live gap,
because the gap has not closed — and that zero is the second one this method has
produced, both of them explicable from the method's own logic.
